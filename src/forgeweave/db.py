"""SQLite backend for jobs, memory, and traces.

Three tables:
  - jobs: long-running operation state
  - memory: key/value persistent store with TTL
  - traces: execution trace events
"""

import json
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

_locals = threading.local()


def _get_conn(db_path: Path) -> sqlite3.Connection:
    if not hasattr(_locals, "conn") or _locals.conn is None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        _locals.conn = conn
    return _locals.conn


def init_db(db_path: Path) -> None:
    conn = _get_conn(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'running',
            stage TEXT,
            progress_pct INTEGER DEFAULT 0,
            message TEXT,
            input_json TEXT,
            result_json TEXT,
            error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value_json TEXT NOT NULL,
            namespace TEXT NOT NULL DEFAULT 'default',
            size_bytes INTEGER,
            created_at TEXT NOT NULL,
            expires_at TEXT
        );
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT,
            timestamp TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
        CREATE INDEX IF NOT EXISTS idx_jobs_type ON jobs(type);
        CREATE INDEX IF NOT EXISTS idx_memory_namespace ON memory(namespace);
        CREATE INDEX IF NOT EXISTS idx_traces_job ON traces(job_id);
    """)
    conn.commit()


# ── Job operations ──────────────────────────────────────────────


def create_job(
    db_path: Path,
    job_type: str,
    input_data: dict | None = None,
) -> str:
    job_id = f"{job_type}_{uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    conn = _get_conn(db_path)
    conn.execute(
        "INSERT INTO jobs (job_id, type, status, stage, progress_pct, message, input_json, created_at, updated_at) "
        "VALUES (?, ?, 'running', ?, 0, 'started', ?, ?, ?)",
        (
            job_id,
            job_type,
            "initializing",
            json.dumps(input_data or {}),
            now,
            now,
        ),
    )
    conn.commit()
    return job_id


def update_job(
    db_path: Path,
    job_id: str,
    *,
    status: str | None = None,
    stage: str | None = None,
    progress_pct: int | None = None,
    message: str | None = None,
    result: dict | None = None,
    error: str | None = None,
) -> None:
    now = datetime.utcnow().isoformat()
    conn = _get_conn(db_path)
    fields = ["updated_at = ?"]
    values: list = [now]
    if status is not None:
        fields.append("status = ?")
        values.append(status)
    if stage is not None:
        fields.append("stage = ?")
        values.append(stage)
    if progress_pct is not None:
        fields.append("progress_pct = ?")
        values.append(progress_pct)
    if message is not None:
        fields.append("message = ?")
        values.append(message)
    if result is not None:
        fields.append("result_json = ?")
        values.append(json.dumps(result))
    if error is not None:
        fields.append("error = ?")
        values.append(error)
    values.append(job_id)
    conn.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE job_id = ?", values)
    conn.commit()


def get_job(db_path: Path, job_id: str) -> dict | None:
    conn = _get_conn(db_path)
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        return None
    result = dict(row)
    if result.get("input_json"):
        result["input_json"] = json.loads(result["input_json"])
    if result.get("result_json"):
        result["result_json"] = json.loads(result["result_json"])
    return result


def add_trace(db_path: Path, job_id: str, event_type: str, event_data: dict | None = None) -> None:
    conn = _get_conn(db_path)
    conn.execute(
        "INSERT INTO traces (job_id, event_type, event_data, timestamp) VALUES (?, ?, ?, ?)",
        (job_id, event_type, json.dumps(event_data or {}), datetime.utcnow().isoformat()),
    )
    conn.commit()


def get_traces(db_path: Path, job_id: str) -> list[dict]:
    conn = _get_conn(db_path)
    rows = conn.execute("SELECT * FROM traces WHERE job_id = ? ORDER BY id", (job_id,)).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        if d.get("event_data"):
            d["event_data"] = json.loads(d["event_data"])
        result.append(d)
    return result


# ── Memory operations ───────────────────────────────────────────


def memory_write(
    db_path: Path,
    key: str,
    value: object,
    namespace: str = "default",
    ttl_seconds: int = 0,
) -> dict:
    now = datetime.utcnow()
    expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat() if ttl_seconds > 0 else None
    value_json = json.dumps(value)
    conn = _get_conn(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO memory (key, value_json, namespace, size_bytes, created_at, expires_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (key, value_json, namespace, len(value_json), now.isoformat(), expires_at),
    )
    conn.commit()
    return {
        "key": key,
        "size_bytes": len(value_json),
        "expires_at": expires_at,
    }


def memory_read(db_path: Path, key: str) -> dict | None:
    conn = _get_conn(db_path)
    row = conn.execute(
        "SELECT * FROM memory WHERE key = ? AND (expires_at IS NULL OR expires_at > ?)",
        (key, datetime.utcnow().isoformat()),
    ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["value_json"] = json.loads(result["value_json"])
    return result


def memory_list_namespace(db_path: Path, namespace: str) -> list[str]:
    conn = _get_conn(db_path)
    rows = conn.execute(
        "SELECT key FROM memory WHERE namespace = ? AND (expires_at IS NULL OR expires_at > ?)",
        (namespace, datetime.utcnow().isoformat()),
    ).fetchall()
    return [r["key"] for r in rows]
