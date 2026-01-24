# Support

## Getting Help with netENwsl

This document explains how to get help when using the Computer Networks Laboratory Kits.

## Self-Help Resources

Before requesting support, please consult these resources:

### Documentation

| Resource | Location | Content |
|----------|----------|---------|
| **Main README** | [README.md](../README.md) | Complete overview, installation, weekly guides |
| **Troubleshooting Guide** | [Section 29 of README](../README.md#29-complete-troubleshooting-guide) | Common problems and solutions |
| **FAQ** | [Section 33 of README](../README.md#33-faq--frequently-asked-questions) | Frequently asked questions |
| **Command Reference** | [Section 30 of README](../README.md#30-essential-commands--quick-reference-sheet) | Quick command lookup |

### Weekly Documentation

Each week folder contains:
- `README.md` — Week-specific instructions and exercises
- `docs/troubleshooting.md` — Week-specific problem solutions
- `docs/glossary.md` — Technical terms explained
- `homework/README.md` — Additional exercises

### Environment Verification

Run the verification script to diagnose common issues:
```bash
cd <week-folder>
python3 setup/verify_environment.py
```

This script checks all prerequisites and provides specific guidance for any failures.

## Support Channels

### GitHub Issues (Primary)

For technical problems, bug reports and feature requests, use GitHub Issues:

1. Navigate to the [Issues tab](https://github.com/antonioclim/netENwsl/issues)
2. Search existing issues (your problem may already be addressed)
3. If not found, click "New Issue"
4. Select the appropriate template
5. Fill in all requested information

**Issue templates available:**
- Bug Report — Script errors, unexpected behaviour
- Environment Issue — WSL, Docker, Portainer problems
- Documentation — Typos, unclear instructions
- Feature Request — Suggestions for improvements
- Question — General queries about usage

### Response Expectations

| Issue Type | Typical Response Time |
|------------|----------------------|
| Critical bugs | 30–60 days |
| Environment issues | 30–60 days |
| Feature requests | Reviewed periodically |
| Questions | 30–60 days |
| Documentation issues | 30–60 days |

**Important**: This is an educational project maintained alongside teaching responsibilities. Response times may extend during examination periods, academic breaks and semester peaks. Your patience is appreciated.

## What Information to Provide

When requesting support, include:

### For Environment Issues
```
Operating System: Windows 11 Pro 23H2
WSL Version: 2.3.26.0 (from `wsl --version`)
Ubuntu Version: 22.04.4 LTS (from `lsb_release -a`)
Docker Version: 28.2.2 (from `docker --version`)
Python Version: 3.11.8 (from `python3 --version`)

Verification Output: [paste full output of verify_environment.py]
```

### For Script Errors
```
Week: 05enWSL
Script: scripts/start_lab.py
Command run: python3 scripts/start_lab.py
Error message: [paste exact error]
Steps taken: [what you tried]
```

### For Exercise Problems
```
Week: 07enWSL
Exercise: ex_07_02_packet_filter.py
Expected behaviour: [what should happen]
Actual behaviour: [what happens]
Your approach: [brief explanation of your attempt]
```

## Academic Support

### During University Courses

If you are enrolled in the Computer Networks course at ASE Bucharest:

- **Lab sessions**: Ask your laboratory instructor during scheduled sessions
- **Course forums**: Use the university's learning management system
- **Office hours**: Contact the course coordinator during published hours

### Independent Learners

For those using these materials independently:
- GitHub Issues is your primary support channel
- Review all documentation thoroughly before asking
- Provide complete context in your questions

## Language

Support is provided in:
- **English** — For netENwsl repository
- **Romanian** — For netROwsl repository

Please use the language matching your repository version.

## What Support Cannot Help With

- General Python programming questions (use Stack Overflow)
- Network theory beyond course scope (consult textbooks)
- Personal computer hardware issues
- Non-standard environment configurations
- Urgent requests outside academic schedule

## Licence Enquiries

For institutional licence applications or licence clarifications, open an issue using the "Licence Request" template.

---

**Thank you for using these materials. We are here to help you succeed in learning computer networking.**
