# Project Context

**Version:** 1.0
**Last updated:** 2026-06-15
**Status:** Active

This document provides high-level architectural context for ForgeWeave. It is the reference for design decisions, supported environments, and project scope.

> **IMPORTANT:** This is the source of truth for architecture decisions. Any change to the architecture must be reflected here first.

---

## Table of Contents

- [What is ForgeWeave?](#what-is-forgeweave)
- [Architecture Overview](#architecture-overview)
- [Layer Responsibilities](#layer-responsibilities)
- [Data Flow](#data-flow)
- [Supported Environments (TUIs)](#supported-environments-tuis)
- [Design Principles](#design-principles)
- [Key Specifications](#key-specifications)
- [Project Status](#project-status)
- [Roadmap](#roadmap)
- [Glossary](#glossary)

---

## What is ForgeWeave?

ForgeWeave is a **behavioral execution framework for AI agents inside development environments** (TUIs). It is a CLI tool written in Python that:

1. **Initializes projects** with TUI-specific agent and skill scaffolding.
2. **Defines and enforces** strict specifications for Skills and Agents.
3. **Transforms** internal structures into TUI-specific formats via adapters.
4. **Enforces** determinism, transparency, and explicit behavior documentation.

---

## Architecture Overview

```mermaid
flowchart TB
    subgraph User["User Space"]
        U[Developer] -->|CLI commands| CLI
    end

    subgraph ForgeWeave["ForgeWeave Core"]
        CLI["CLI Layer<br/>(argparse, command routing)"]

        subgraph Core["Core Layer"]
            TYPES["Shared Types<br/>ForgeProject, Skill, Agent"]
            CONFIG["Configuration<br/>Loader & Constants"]
        end

        subgraph Engine["Execution Engine"]
            SKILL["Skill Engine<br/>Load · Parse · Validate"]
            AGENT["Agent Engine<br/>Lifecycle · Execution"]
            TEMPLATE["Template Engine<br/>Versioning · Rendering"]
        end

        subgraph Future["Future Layers"]
            HOOKS["Hook System<br/>(lifecycle hooks)"]
            MCP["MCP Integration<br/>(tool exposure)"]
        end
    end

    subgraph Adapters["Adapter Layer"]
        direction LR
        A1["OpenCode<br/>Adapter"]
        A2["Claude Code<br/>Adapter"]
        A3["Gemini CLI<br/>Adapter"]
        A4["Qwen Code<br/>Adapter"]
    end

    subgraph Output["Generated Output"]
        O1[".opencode/"]
        O2[".claude/"]
        O3[".gemini/"]
        O4[".qwen/"]
    end

    CLI --> Core
    Core --> Engine
    SKILL --> TEMPLATE
    AGENT --> TEMPLATE
    TEMPLATE -.->|future| HOOKS
    HOOKS -.->|future| MCP
    TEMPLATE --> Adapters
    A1 --> O1
    A2 --> O2
    A3 --> O3
    A4 --> O4

    style Future fill:#f0f0f0,stroke:#999,stroke-dasharray: 5 5
    style HOOKS fill:#f0f0f0,stroke:#999,stroke-dasharray: 5 5
    style MCP fill:#f0f0f0,stroke:#999,stroke-dasharray: 5 5
```

---

## Layer Responsibilities

### CLI Layer

Responsible for command routing, argument parsing, and user interaction.

```mermaid
graph LR
    subgraph Commands["CLI Commands"]
        INIT["forge init<br/>→ scaffold project"]
        VALIDATE["forge validate<br/>→ check specs"]
        DOCTOR["forge doctor<br/>→ verify env"]
    end

    INIT --> R1["Runs interactive TUI selector"]
    INIT --> R2["Copies template directory"]
    VALIDATE --> R3["Validates SKILL.md / AGENT.md"]
    DOCTOR --> R4["Checks Python + TUI versions"]
```

| Command | Status | Description |
|---|---|---|
| `forge init` | ✅ Implemented | Interactive TUI selector, scaffolds `.opencode/`, `.claude/`, etc. |
| `forge validate` | ❌ Planned | Validates skills and agents against their respective specs |
| `forge doctor` | ❌ Planned | Verifies environment prerequisites |

### Core Layer

Holds shared types, config loading, and constants used across all other layers.

```mermaid
classDiagram
    class ForgeProject {
        +str name
        +str tui
        +List~Skill~ skills
        +List~Agent~ agents
        +validate()
        +to_dict()
    }

    class Skill {
        +str skill_id
        +str name
        +str version
        +List~str~ tui_compatibility
        +validate()
    }

    class Agent {
        +str agent_id
        +str name
        +str version
        +List~str~ tui_compatibility
        +validate()
    }

    ForgeProject "1" --> "*" Skill : contains
    ForgeProject "1" --> "*" Agent : contains
```

### Skill Engine

Handles skill loading from template directories, parsing SKILL.md frontmatter, and validating against [SKILL_SPEC.md](./SKILL_SPEC.md).

### Agent Engine

Manages agent lifecycle (initialization → execution → stopping), invokes skills, and enforces execution rules defined in [AGENT_SPEC.md](./AGENT_SPEC.md).

### Template Engine

Manages versioned template rendering. Converts internal representations into Markdown files using TUI-specific templates.

### Adapter Layer

Stateless transformation boundary. Each adapter implements `BaseAdapter` and converts ForgeWeave internal structures into TUI-specific formats.

---

## Data Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as forge CLI
    participant Core as Core Layer
    participant Eng as Engine
    participant Adp as Adapter
    participant FS as File System

    Dev->>CLI: forge init
    CLI->>CLI: Parse arguments
    CLI->>CLI: Prompt TUI selection
    CLI->>Core: Load ForgeProject config
    Core->>Core: Validate project structure
    Core->>Eng: Resolve templates for TUI
    Eng->>Eng: Load skills & agents
    Eng->>Eng: Validate against specs
    Eng->>Adp: Transform to TUI format
    Adp->>Adp: Apply naming conventions
    Adp->>FS: Write .<tui>/ directory
    FS-->>Dev: Project scaffolded

    Note over Dev,FS: forge validate flow

    Dev->>CLI: forge validate skill ./SKILL.md
    CLI->>Core: Load file
    Core->>Eng: Parse & validate
    Eng-->>CLI: Validation result
    CLI-->>Dev: Pass/Fail report
```

---

## Supported Environments (TUIs)

| TUI | Adapter Class | Status | Config Directory | Naming Convention |
|---|---|---|---|---|
| OpenCode | `OpenCodeAdapter` | ![Planned](https://img.shields.io/badge/-planned-888) | `.opencode/` | `kebab-case` |
| Claude Code | `ClaudeAdapter` | ![Planned](https://img.shields.io/badge/-planned-888) | `.claude/` | `kebab-case` |
| Gemini CLI | `GeminiAdapter` | ![Planned](https://img.shields.io/badge/-planned-888) | `.gemini/` | `snake_case` |
| Qwen Code | `QwenAdapter` | ![Planned](https://img.shields.io/badge/-planned-888) | `.qwen/` | `kebab-case` |

> **NOTE:** Adding a new TUI requires implementing a new adapter class. See [ADAPTER_SPEC.md](./ADAPTER_SPEC.md) for the full process.

---

## Design Principles

```mermaid
graph TD
    subgraph Principles["Core Design Principles"]
        DET["Determinism<br/>over Creativity"]
        EXP["Explicit<br/>over Implicit"]
        TEM["Template-Driven<br/>Generation"]
        NOSTATE["No Hidden State"]
        ADPT["Adapters Are<br/>Boundaries"]
    end

    DET --> R1["Same input → Same output"]
    EXP --> R2["Undocumented = Nonexistent"]
    TEM --> R3["No hardcoded generation"]
    NOSTATE --> R4["All I/O declared & logged"]
    ADPT --> R5["No business logic in adapters"]

    style DET fill:#1a1a2e,color:#fff
    style EXP fill:#1a1a2e,color:#fff
    style TEM fill:#1a1a2e,color:#fff
    style NOSTATE fill:#1a1a2e,color:#fff
    style ADPT fill:#1a1a2e,color:#fff
```

### Determinism over Creativity

System logic must produce the same output given the same input. No random behavior, no hidden branching, no undocumented side effects. This is non-negotiable — contributions that introduce non-determinism will be rejected.

### Explicit over Implicit

If behavior is not documented, it does not exist. Every decision in the codebase must be traceable to a documented rule. This applies to:

- CLI commands and their flags
- Skill execution steps and decision rules
- Agent lifecycle and stopping conditions
- Adapter transformation logic

### Template-Driven Generation

All project scaffolding is generated from versioned templates. No hardcoded generation logic exists outside the template system. This ensures:

- **Consistency** across TUI outputs
- **Versioning** of template formats
- **Auditability** of what was generated

### No Hidden State

Agents and skills must declare what they read and write. State passed between modules must be explicit and logged. Any contribution that introduces implicit state passing will be rejected.

### Adapters Are Boundaries

Each TUI adapter is a strict transformation boundary. Business logic must never leak into adapters. Adapters are:

- **Stateless** — no runtime state between calls
- **Idempotent** — same input → same output every time
- **Non-mutating** — never modify input objects

---

## Key Specifications

| Document | Version | Purpose |
|---|---|---|
| [SKILL_SPEC.md](./SKILL_SPEC.md) | 1.0 | Canonical format for all ForgeWeave skills |
| [AGENT_SPEC.md](./AGENT_SPEC.md) | 1.0 | Canonical format for all ForgeWeave agents |
| [ADAPTER_SPEC.md](./ADAPTER_SPEC.md) | 1.0 | How TUI adapters must be implemented |
| [AGENTS.md](./AGENTS.md) | 1.0 | Project-level agent registration and configuration |

---

## Project Status

ForgeWeave is in **early development** (v0.1.0 pre-release). The core specifications are defined, but the CLI and adapters are not yet fully implemented.

### What's Done

- All three specifications (SKILL_SPEC, AGENT_SPEC, ADAPTER_SPEC) are complete and stable
- Contributor documentation (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) is in place
- GitHub templates for issues and PRs are configured
- Basic `forge init` CLI command

### What's in Progress

- Template directory population for all 4 TUIs
- Skill and agent validation engine
- Adapter implementations

### What's Planned

| Feature | Priority | Timeline |
|---|---|---|
| `forge validate` command | High | Next release |
| `forge doctor` command | High | Next release |
| OpenCode adapter | High | v0.2.0 |
| Claude Code adapter | High | v0.2.0 |
| Gemini CLI adapter | Medium | v0.3.0 |
| Qwen Code adapter | Medium | v0.3.0 |
| Hook system | Low | v0.4.0 |
| MCP integration | Low | v0.5.0 |

---

## Roadmap

```mermaid
gantt
    title ForgeWeave Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %Y Q%q

    section Foundation
    Specs & Documentation      :done, 2025-10-01, 2025-12-31
    CLI Skeleton (init)        :done, 2025-11-01, 2025-12-31

    section Core Engine
    Validation Engine           :active, 2026-01-01, 2026-04-30
    Template Engine             :active, 2026-02-01, 2026-05-31
    Agent Lifecycle             :2026-03-01, 2026-06-30

    section Adapters
    OpenCode Adapter            :2026-04-01, 2026-06-30
    Claude Adapter              :2026-04-01, 2026-07-31
    Gemini Adapter              :2026-05-01, 2026-08-31
    Qwen Adapter                :2026-05-01, 2026-08-31

    section Release
    v0.1.0 Alpha                :milestone, 2026-03-01, 0d
    v0.2.0 Beta                 :milestone, 2026-07-01, 0d
    v1.0.0 Stable               :milestone, 2026-12-01, 0d
```

---

## Glossary

| Term | Definition |
|---|---|
| **TUI** | Terminal User Interface — the coding environment (OpenCode, Claude Code, etc.) |
| **Skill** | A reusable, deterministic behavior unit defined entirely in Markdown |
| **Agent** | An autonomous worker that invokes skills following documented rules |
| **Adapter** | A stateless transformation layer between ForgeWeave and a specific TUI |
| **ForgeProject** | Internal representation of a project during scaffolding |
| **TUIProject** | TUI-specific output structure after adapter transformation |
| **MCP** | Model Context Protocol — a future integration point for exposing tools |
| **Frontmatter** | YAML metadata block at the top of a Markdown file, delimited by `---` |
