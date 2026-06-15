---
name: Pull Request
about: Submit a pull request to ForgeWeave
---

## Description

<!-- Briefly describe what this PR does and why. -->

```
<!-- Paste a summary of the changes (2-4 sentences) -->
```

Closes #<!-- issue number -->

---

## Type of Change

<!-- Check all that apply -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🆕 New adapter (new TUI support)
- [ ] 📦 New skill or agent
- [ ] 📝 Documentation update
- [ ] ♻️ Refactor (no functional changes)
- [ ] 🔧 Tooling / CI / Chore
- [ ] ⚠️ Breaking change (fix or feature that changes existing behavior)

---

## Checklist

Before submitting, confirm the following:

### Code Quality

- [ ] Branch is up to date with `dev` (rebased, not merged or pulled)
- [ ] All pre-commit hooks pass locally (`pre-commit run --all-files`)
- [ ] All existing tests pass (`pytest`)
- [ ] No new warnings introduced

### Testing

- [ ] New tests added for new behavior
- [ ] Test coverage meets project minimum **80%** (check with `pytest --cov`)
- [ ] Tests are deterministic (no network calls, no ordering dependencies)
- [ ] Edge cases and failure modes are tested

### Documentation

- [ ] Docstrings added or updated (Google Python style)
- [ ] Relevant documentation updated:
  - [ ] README.md
  - [ ] PROJECT_CONTEXT.md
  - [ ] SKILL_SPEC.md / AGENT_SPEC.md / ADAPTER_SPEC.md (if applicable)
- [ ] CHANGELOG.md updated under `[Unreleased]`

### Commits

- [ ] PR title follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format
- [ ] Commits are clean, scoped, and atomic
- [ ] No merge commits in the PR branch

---

## Screenshots (if applicable)

<!-- Paste screenshots of UI changes or CLI output -->

---

## Review Notes

<!-- Anything reviewers should pay special attention to. Examples: -->
<!-- - Performance implications -->
<!-- - Security considerations -->
<!-- - Migration impact for existing users -->
<!-- - Decisions that were made and why -->

---

## Related Issues

<!-- Link related issues or discussions -->
- Related to #
- Discussion: #

---

## Acknowledgements

- [ ] I have read the [CONTRIBUTING.md](../CONTRIBUTING.md) document
- [ ] I have read the [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) document
- [ ] My contribution is my own work or I have the right to contribute it
