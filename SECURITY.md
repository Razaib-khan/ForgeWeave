# Security Policy

ForgeWeave operates inside developer environments and handles file system operations, agent execution, and MCP integrations. Security is treated as a first-class concern, not an afterthought.

---

## Supported Versions

Only the latest stable release and the current `dev` branch receive security fixes.

| Version | Supported |
|---|---|
| Latest stable | ✅ Yes |
| `dev` branch | ✅ Yes |
| Older releases | ❌ No — please upgrade |

---

## Reporting a Vulnerability

**Do not open a public GitHub Issue for security vulnerabilities.**

Public disclosure before a fix is available puts all ForgeWeave users at risk.

### How to Report

Send a detailed report to:

**razaibkhanofficial@gmail.com**

Use the subject line: `[SECURITY] <brief description>`

If you want to encrypt your report, our PGP public key is available upon request.

### What to Include

A useful security report contains:

- **Description:** What is the vulnerability? What component does it affect?
- **Impact:** What can an attacker do by exploiting this? (e.g., arbitrary file write, agent command injection, template escape)
- **Reproduction steps:** Exact steps to reproduce the issue.
- **Environment:** Python version, OS, ForgeWeave version, TUI adapter in use.
- **Proof of concept:** Code or commands that demonstrate the vulnerability (do not include live exploits targeting other systems).
- **Suggested fix:** Optional, but appreciated.

---

## Response Timeline

| Milestone | Target |
|---|---|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 5 business days |
| Status update | Every 7 days until resolved |
| Fix release | Depends on severity (see below) |

### Severity-Based Fix Schedule

| Severity | Description | Target Fix Time |
|---|---|---|
| **Critical** | Remote code execution, arbitrary file write, agent escape | 48 hours |
| **High** | Privilege escalation, template injection, data exfiltration | 7 days |
| **Medium** | Denial of service, unintended file access | 30 days |
| **Low** | Minimal impact, hardening improvements | Next release cycle |

---

## Disclosure Policy

ForgeWeave follows **coordinated vulnerability disclosure**:

1. Reporter submits vulnerability privately.
2. Maintainers assess, develop, and test a fix.
3. Fix is released.
4. A security advisory is published on GitHub (typically 7 days after fix release).
5. Reporter is credited (unless they prefer anonymity).

We do not support immediate full public disclosure before a fix is available. If a reporter disagrees with our assessment or timeline, we ask for direct communication before any public action.

---

## Known Security Considerations

Given the nature of ForgeWeave, contributors and users should be aware of these inherent risk surfaces:

### File System Operations
ForgeWeave generates and modifies files in the user's project directory. All destructive operations (overwrite, delete) require explicit confirmation. **Any PR that bypasses this confirmation requirement will be rejected.**

### Agent Execution
Agents execute structured workflows. No agent may spawn subprocesses, make network calls, or access paths outside the project directory without explicit user configuration and documented behavior.

### Template Injection
Templates are processed before being written to disk. Template variables must be sanitized before rendering. Untrusted input must never reach the template engine directly.

### MCP Integration (Future)
When MCP integration is implemented, tools exposed to TUIs must be explicitly scoped. No MCP tool may grant write access beyond the project directory without configuration-level opt-in.

### No External API Dependencies for Core System
The core ForgeWeave system must function without external network calls. Any contribution that introduces a mandatory external API dependency in the core execution path will be rejected.

---

## Bug Bounty

ForgeWeave does not currently offer a paid bug bounty program. We do offer:

- Public credit in the security advisory and CHANGELOG.
- A contributor badge on your GitHub profile (if desired).
- Our genuine gratitude.

---

## Out of Scope

The following are not considered security vulnerabilities for ForgeWeave:

- Issues in third-party TUI tools (OpenCode, Claude Code, Gemini CLI, Qwen Code) — report these to their respective maintainers.
- Theoretical vulnerabilities with no practical exploitation path.
- Vulnerabilities requiring physical access to the user's machine.
- Self-inflicted issues from deliberately misconfigured environments.
