# SMTP Protocol Flow Diagram

This diagram illustrates the SMTP message delivery flow from sender to recipient.

## Email Delivery Architecture

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           EMAIL DELIVERY FLOW                                   │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐  │
│  │  Alice   │  SMTP   │  MTA     │  SMTP   │  MTA     │ POP3/   │   Bob    │  │
│  │  (MUA)   │────────>│ (sender) │────────>│ (recvr)  │ IMAP    │  (MUA)   │  │
│  └──────────┘  :587   └──────────┘  :25    └──────────┘────────>└──────────┘  │
│                                                                                 │
│  Thunderbird    smtp.alice.com      mx.bob.com          mail.bob.com           │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘

Legend:
  MUA = Mail User Agent (email client)
  MTA = Mail Transfer Agent (server)
  :587 = Submission port (client → server)
  :25  = Relay port (server → server)
```

## SMTP Dialogue State Machine

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SMTP STATE MACHINE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────┐                                                                     │
│  │ CONNECT │ ─────────────> Server sends 220 greeting                           │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │  EHLO   │ ─────────────> Server responds 250 (multi-line with extensions)    │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │MAIL FROM│ ─────────────> Server responds 250 OK                              │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │ RCPT TO │ ─────────────> Server responds 250 OK (can repeat for multiple)    │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │  DATA   │ ─────────────> Server responds 354 Start mail input  ⚠️ NOT 250!   │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │ CONTENT │ ─────────────> Send headers + blank line + body + "." on own line  │
│  └────┬────┘                                                                     │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────┐                                                                     │
│  │  QUIT   │ ─────────────> Server responds 221 Bye                             │
│  └─────────┘                                                                     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Response Code Classes

```
┌───────────────────────────────────────────────────────────────────┐
│              SMTP RESPONSE CODE CLASSES                           │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│   2xx  ────────>  SUCCESS                                        │
│                   250 OK, 220 Ready, 221 Bye                     │
│                                                                   │
│   3xx  ────────>  INTERMEDIATE (waiting for more)                │
│                   354 Start mail input                           │
│                                                                   │
│   4xx  ────────>  TEMPORARY FAILURE (try again)                  │
│                   421 Service unavailable                        │
│                                                                   │
│   5xx  ────────>  PERMANENT FAILURE (don't retry)                │
│                   550 Mailbox not found                          │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

*See `docs/misconceptions.md` for common errors with SMTP response codes.*
