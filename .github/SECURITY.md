# Security Policy

## Scope

This security policy applies to the netENwsl repository and its associated laboratory materials. Given the educational nature of these materials, security considerations focus on:

- Ensuring exercises do not inadvertently expose student systems
- Maintaining safe default configurations in Docker containers
- Protecting the integrity of the educational content

## Reporting a Vulnerability

If you discover a security issue in these materials, please report it responsibly.

### What Constitutes a Security Issue

| Category | Examples |
|----------|----------|
| **Configuration Risks** | Default passwords exposed on non-localhost ports, containers with excessive privileges |
| **Code Vulnerabilities** | Scripts that could be exploited if run in unexpected contexts |
| **Dependency Issues** | Known vulnerabilities in required packages |
| **Documentation Risks** | Instructions that could lead to insecure configurations |

### How to Report

**For Non-Critical Issues:**

Open a standard issue with the title prefix `[SECURITY]`. These are issues that:
- Affect only the local laboratory environment
- Require intentional misuse to exploit
- Have no impact beyond the educational context

**For Critical Issues:**

If you believe the issue could affect students' systems beyond the intended laboratory scope:

1. **Do not** open a public issue
2. Contact the maintainers directly through GitHub (use the repository owner's profile)
3. Include a clear description of the vulnerability
4. Provide steps to reproduce if possible
5. Allow reasonable time for a fix before any public disclosure

### Response Timeline

| Severity | Initial Response | Resolution Target |
|----------|------------------|-------------------|
| Critical | Within 7 days | 30 days |
| High | Within 14 days | 60 days |
| Medium | Within 30 days | 90 days |
| Low | Within 60 days | Next release |

## Security Considerations in These Materials

### Intentional Educational Simplifications

The laboratory materials include certain configurations that prioritise educational clarity over production security:

| Configuration | Reason | Mitigation |
|---------------|--------|------------|
| Standard credentials (`stud/stud`) | Easy student access | Services bound to localhost only |
| Simple passwords | Reduced friction in learning | Not exposed externally |
| Verbose logging | Educational visibility | Disabled in production examples |
| Disabled HTTPS (some exercises) | Protocol observation | Separate exercises cover TLS |

### Safe Defaults

All Docker configurations in this repository:
- Bind ports to `127.0.0.1` (localhost) by default
- Use isolated Docker networks
- Do not require elevated privileges
- Do not persist sensitive data outside the container

### Student Responsibility

Students using these materials should:
- Run exercises only on personal development machines
- Not expose laboratory services to external networks
- Not use laboratory credentials for any other purpose
- Clean up containers after completing exercises

## Supported Versions

Security updates are provided for the current major version only.

| Version | Supported |
|---------|-----------|
| 5.x.x | Yes |
| 4.x.x | No |
| < 4.0 | No |

## Dependency Updates

The materials include third-party dependencies that may have their own security considerations:

- **Docker images**: Updated periodically; students should pull fresh images
- **Python packages**: Listed in `requirements.txt`; students should update when advised
- **Documentation links**: Checked regularly for validity

If you notice an outdated dependency with known vulnerabilities, please open an issue.

---

Thank you for helping keep these educational materials safe for all students.
