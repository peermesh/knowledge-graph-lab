# Developer Handoffs

This directory contains complete, tested integrations ready for developer handoff.

## Available Handoffs

### Email Integration (`email-integration/`)

AWS SES email sending integration - complete and tested.

**Status:** ✅ Ready for handoff

**What's included:**
- Working example that sends actual emails
- Complete documentation
- Code examples (Node.js, Python, Go)
- Docker configuration
- Tested and verified (2025-11-08)

**Developer instructions:** See `email-integration/START-HERE.md`

**Admin notes:** Provide .env file separately (stored in `.dev/mail/working-example-env-PRIVATE.txt`)

---

## How to Use This Directory

Each subdirectory is a complete handoff package:

1. **Point developer to the directory**
2. **Developer reads START-HERE.md**
3. **Admin provides .env file separately**
4. **Developer runs working example**
5. **Developer integrates into their app**

All handoffs are self-contained with:
- Complete documentation
- Working code examples
- Test instructions
- No secrets (provided separately)
