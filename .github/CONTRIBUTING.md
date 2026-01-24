# Contributing to netENwsl

Thank you for your interest in contributing to the Computer Networks Laboratory Kits. This document explains how you can help improve these educational materials while respecting the project's licensing terms.

## Important Notice on Licensing

This repository is distributed under a **Restrictive Educational Licence**. Please read and understand the [LICENCE.md](../LICENCE.md) before contributing. Key points:

- Contributions you make become part of the licensed materials
- You retain copyright on your original contributions but grant the authors the right to include them
- Your contributions will be subject to the same restrictive terms as the existing materials
- By contributing, you agree to these terms

## Types of Contributions Welcome

### Highly Encouraged

| Contribution Type | Examples |
|-------------------|----------|
| **Bug Reports** | Script errors, incorrect expected outputs, Docker configuration issues |
| **Documentation Fixes** | Typos, unclear instructions, broken links |
| **Environment Issues** | WSL compatibility, Docker version problems, dependency updates |
| **Suggestions** | Ideas for new exercises, improved explanations, better analogies |

### Considered on Case-by-Case Basis

| Contribution Type | Notes |
|-------------------|-------|
| **New Exercises** | Must align with weekly learning objectives |
| **Script Improvements** | Must maintain educational clarity over code elegance |
| **Translation Corrections** | For netROwsl/netENwsl alignment |

### Not Accepted

- Redistribution of materials in derivative repositories
- Commercial adaptations
- Content that conflicts with course learning objectives
- Changes that reduce educational accessibility

## How to Report Issues

### Before Submitting

1. **Search existing issues** — Your problem may already be reported
2. **Read the documentation** — Check README, troubleshooting guide and FAQ
3. **Try the standard fixes** — Restart WSL, prune Docker, verify environment

### Submitting an Issue

1. Navigate to the Issues tab
2. Click "New Issue"
3. Select the appropriate template:
   - **Bug Report** — For code and script problems
   - **Environment Issue** — For WSL, Docker, Portainer problems
   - **Documentation** — For text improvements
   - **Feature Request** — For suggestions
   - **Question** — For general queries
4. Fill in all required fields
5. Provide clear reproduction steps if applicable

### Good Issue Examples

**Effective Bug Report:**
> **Title:** [BUG] Week 05 — start_lab.py fails with port 5005 already in use
>
> **Description:** Running start_lab.py in 05enWSL fails because port 5005 is already bound.
>
> **Steps:** Run `python3 scripts/start_lab.py` after completing Week 04 without running cleanup.
>
> **Expected:** Lab should start or provide clear error about conflicting containers.
>
> **Environment:** Windows 11, WSL2 Ubuntu 22.04, Docker 28.2.2

**Less Helpful Report:**
> The lab does not work. Please fix.

## How to Suggest Improvements

For documentation fixes and minor improvements:

1. Open an issue describing the problem and your suggested fix
2. If the fix is straightforward (typo, link), include the exact correction
3. Wait for confirmation before expecting implementation

For larger suggestions:

1. Open a Feature Request issue
2. Describe the motivation and educational benefit
3. Outline your proposed approach
4. Discuss with maintainers before investing significant effort

## Code Style Guidelines

If you submit code suggestions, follow these conventions:

### Python

- Follow PEP 8 style guidelines
- Use clear, educational variable names (avoid single letters except in loops)
- Include docstrings for functions
- Add inline comments explaining networking concepts
- Prefer clarity over brevity — this is educational code

### Documentation

- Use British English spelling (e.g., "colour", "behaviour", "organisation")
- Avoid the serial comma before "and" (e.g., "A, B and C" not "A, B, and C")
- Use active voice where possible
- Include practical examples
- Structure content with clear headings

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Use fenced code blocks with language specification
- Keep line lengths reasonable (under 120 characters for prose)
- Use reference-style links for repeated URLs

## Recognition

Contributors who provide valuable bug reports, documentation fixes or suggestions will be acknowledged in the repository's acknowledgements section upon request.

## Questions About Contributing

If you are unsure whether a contribution is appropriate, open a Question issue to discuss before investing time. We appreciate your interest in improving these materials.

---

**Thank you for helping make these materials better for all students.**
