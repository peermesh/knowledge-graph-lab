# Phase 6: Polish & Integration

## Objective

Connect all the pieces, add transitions and animations, handle edge cases, and polish the overall experience.

## What to Build

### 1. Cross-Mode Integration

**Domain Assignment from Discover**
- When user assigns a finding to a domain in Discover mode, update the domain's finding count
- Toast notification: "Added to [Domain Name]"

**Quick Access Between Modes**
- From domain detail in Organize → "View findings" opens Discover filtered to that domain
- From finding in Discover → Domain tag is clickable, opens that domain in Organize
- From publication in Publish → Source finding link opens finding detail

**Badge Updates**
- Pending publications count in nav updates when items approved/skipped
- Unread findings indicator in Discover (optional, nice-to-have)

### 2. State Synchronization

Create a simple app-level state (Context or lightweight store):

```typescript
interface AppState {
  domains: DomainNode[];
  findings: Finding[];
  pendingPublications: PendingPublication[];
  destinations: Destination[];
  user: User;
  preferences: Preferences;
}
```

Actions that update state:
- Add/remove/move domains
- Assign finding to domain
- Approve/skip publication
- Toggle destination
- Update preferences

State persists to localStorage.

### 3. Transitions & Animations

**Mode Transitions**
- Smooth crossfade or slide between modes
- Keep nav fixed during transitions
- Duration: 200-300ms

**Card Interactions**
- Hover lift on desktop
- Press feedback on mobile
- Approval/skip animations (card slides away)

**Panel Animations**
- Settings panel slides from right
- Domain selector fades in with slight scale
- Context menus appear with subtle fade

**Loading States**
- Skeleton loaders for cards during "loading"
- Subtle pulse animation
- Show briefly even with mock data to demonstrate the pattern

**Toast Notifications**
- Slide in from bottom or top
- Auto-dismiss after 3 seconds
- Action button for undo where appropriate

### 4. Empty & Error States

**Empty States Needed:**
- No findings yet (Discover) - "Your research streams will appear here"
- No domains yet (Organize) - "Create your first domain to organize findings"
- No pending publications (Publish) - "All caught up!"
- No destinations configured - "Add a destination to start publishing"

**Error States Needed:**
- Network error placeholder (even if mocked)
- Failed action toast: "Couldn't save. Try again."

### 5. Responsive Polish

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Mobile Adjustments:**
- Single column layouts
- Bottom sheet modals instead of side panels
- Touch-friendly tap targets (44px minimum)
- Swipe gestures where appropriate

**Desktop Adjustments:**
- Multi-column layouts
- Hover states
- Keyboard shortcuts (nice-to-have):
  - `1/2/3` to switch modes
  - `n` to create new domain
  - `Enter` to approve, `Backspace` to skip

### 6. Accessibility Basics

- Semantic HTML (buttons, headings, lists)
- Focus visible states
- ARIA labels on icon-only buttons
- Keyboard navigation works
- Color contrast meets WCAG AA

### 7. Final Checklist Review

Walk through complete user journey:

1. [ ] New user sees onboarding
2. [ ] Can complete onboarding and land in Discover
3. [ ] Feed shows findings with suggestions interspersed
4. [ ] Can assign finding to domain
5. [ ] Can switch to Organize mode
6. [ ] Domain tree displays and is interactive
7. [ ] Can create, rename, delete, move domains
8. [ ] Can switch to Publish mode
9. [ ] Pending items display, can approve/skip
10. [ ] Destinations list shows, can manage
11. [ ] Settings panel opens and functions
12. [ ] Return user skips onboarding
13. [ ] State persists across refresh
14. [ ] Mobile layout works for all screens
15. [ ] No console errors
16. [ ] Transitions are smooth

## Acceptance Criteria

- [ ] All modes work together coherently
- [ ] Cross-links between modes function
- [ ] State is synchronized across modes
- [ ] Transitions are smooth and consistent
- [ ] Loading states display properly
- [ ] Empty states display properly
- [ ] Error handling exists (even if mocked)
- [ ] Mobile experience is complete
- [ ] Desktop experience is complete
- [ ] Keyboard navigation works
- [ ] No accessibility errors from axe or similar tool
- [ ] App feels polished and intentional

## Design Notes

- Consistency is key - same patterns everywhere
- Animations should feel quick and responsive, not slow
- Empty states are opportunities for personality
- Error messages should be helpful, not technical
- The app should feel calm and capable

## Final Deliverables

After this phase, you should have:
- Complete working prototype
- All mock data in fixture files
- Documented component library
- README with setup instructions
- Notes on known limitations and future work
