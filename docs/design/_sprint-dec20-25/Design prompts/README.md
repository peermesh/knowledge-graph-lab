# Knowledge Graph Lab - UI Prototype

## For the Developer

This package contains everything you need to build the Knowledge Graph Lab interface prototype. Read through the documents in order.

## Document Index

| File | Purpose |
|------|---------|
| `00-vision-and-overview.md` | **Read first.** What we're building and why. |
| `01-phase-foundation-navigation.md` | Phase 1: App shell and navigation setup |
| `02-phase-discover-feed.md` | Phase 2: Discover mode feed interface |
| `03-phase-organize-domains.md` | Phase 3: Organize mode domain hierarchy |
| `04-phase-publish-queue.md` | Phase 4: Publish mode review queue |
| `05-phase-onboarding-settings.md` | Phase 5: Onboarding flow and settings |
| `06-phase-polish-integration.md` | Phase 6: Polish and connect everything |
| `07-component-inventory.md` | Reference: All components and types |
| `08-design-document.md` | What "done" looks like - return here when lost |
| `09-complete-specification.md` | **Single-file version** for one-prompt agents |

## Two Approaches

This package supports two different ways of working with AI agents:

**Phased approach (documents 00-08):** Feed one phase at a time. Better for agents that get confused by large specs. Start with 00 for context, then work through 01-06 in order. Use 07 and 08 as references.

**Single-prompt approach (document 09):** Feed the complete specification in one shot. Better for agents that handle large context well and prefer having everything upfront.

Test both to see which produces better results with your tools.

## How to Use These Documents

1. Read the vision document to understand what you're building
2. Work through phases 1-6 in order
3. Each phase builds on the previous one
4. Use the component inventory as a reference
5. Each phase has acceptance criteria - check them off as you complete them

## Tech Stack

- React with TypeScript
- React Router for navigation
- Tailwind CSS for styling
- localStorage for persistence (no backend)

## AI Tool Tips

If using an AI coding assistant (Cursor, Copilot, AI Studio, etc.):

**Do:**
- Feed it one phase document at a time
- Start with the component structure before styling
- Ask it to create the types first
- Build static layouts before adding interactivity
- Test each phase before moving to the next

**Don't:**
- Try to build everything at once
- Skip the foundation phase
- Add features not in the spec
- Worry about backend integration (it's all mocked)

## Success Criteria

When complete, you should be able to:

1. Go through onboarding as a new user
2. See a feed of research findings
3. Assign findings to domains
4. Manage a hierarchy of research domains
5. Review and approve pending publications
6. Configure publishing destinations
7. Access settings and preferences
8. Have everything work on mobile and desktop

## Questions?

If something is unclear in the spec, make a reasonable decision and document it. The goal is a working prototype that demonstrates the interaction patterns, not a production-ready application.

## Time Estimate

- Phase 1: 2-4 hours
- Phase 2: 4-6 hours
- Phase 3: 4-6 hours
- Phase 4: 3-5 hours
- Phase 5: 3-5 hours
- Phase 6: 4-6 hours

Total: 20-32 hours for a complete prototype

Good luck!
