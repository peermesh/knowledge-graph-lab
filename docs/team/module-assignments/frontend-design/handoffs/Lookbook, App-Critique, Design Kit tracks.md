# Frontend Module Brief: Three Focus Tracks

You are taking point on a frontend-focused module that has three possible focus tracks:

1. Collecting and organizing high-quality interface inspiration (Lookbook)
2. Critiquing our current app interface from first principles (App Critique)
3. Stress-testing and refining the Design Kit (Design Kit Track)

You can choose which of these to start with.

* The **Lookbook** and **App Critique** tracks are the primary priorities.
* The **Design Kit** track is lower priority **unless** you are specifically interested in helping turn our current ideas into structures that can drive a new interface design via AI.

Over time it would be ideal for you to touch all three, but you have discretion on where to begin.

---

## Track 1: Interface Inspiration and Lookbook (Primary)

### Goal

Build a curated, annotated lookbook of high-quality interfaces and layouts that are directly relevant to the product’s user journeys.

This is not about random pretty websites. It is about patterns, flows, and UX decisions that we can learn from and adapt.

### What you do

1. **Research sources** that collect and catalog web and product UI:

   * Interface galleries and pattern libraries
   * Sites that list “top” or “award-winning” designs
   * Website award projects and curated directories
   * Mobile/product UI flow libraries

2. **Build a lookbook** in Pinterest or an equivalent tool that allows you to:

   * Save references from multiple sites
   * Organize boards/collections (e.g., `landing-pages`, `onboarding`, `dashboards`, `mobile-flows`, `chat-UIs`, `discovery`, `profile-settings`)
   * Add short notes to each saved example

3. **Annotate each example** with 1–2 sentences answering:

   * What is interesting about this layout or interaction?
   * How might this apply (or not apply) to our product’s user journeys?

### Example sources to start from

Use these as a starting point and then expand beyond them:

* **Awwwards** – Highly curated, award-based website gallery with strong visual and interaction quality.
* **CSS Design Awards** – Award site with strict submission standards and detailed case studies.
* **SiteInspire** – Curated gallery of clean, modern websites with strong layout and typography.
* **Godly** – Opinionated collection of unusual, experimental, and highly polished sites.
* **Mobbin** – Curated repository of real-world mobile and web app flows with component-level breakdowns.
* **Pttrns** – Mobile UI pattern library organized by interaction type and screen purpose.
* **Lapa Ninja** – Landing page gallery focused on marketing and product pages.
* **UI Garage** – UI patterns and component examples across web and mobile.

Be selective. Favor interfaces that:

* Show clear, thoughtful user flows
* Have unique or refined interaction patterns
* Demonstrate strong hierarchy, spacing, and typography
* Feel modern and product-ready (not just visual experiments)

### Suggested AI research prompt (optional)

You can use or adapt the following prompt with an AI assistant to discover additional high-quality sources.

```markdown
You are a researcher focused on high-quality digital product design. Your task is to identify and summarize the best online resources for **interface inspiration and layout patterns** that go beyond generic design galleries.

Constraints and selection criteria:
- Focus on curated, opinionated collections known for being picky about quality.
- Prioritize sites that highlight interaction patterns, flows, and UX decisions, not just static screenshots.
- Include both web and mobile product interfaces (SaaS apps, dashboards, onboarding flows, chat UIs, etc.).
- Avoid low-effort "design spam" sites that scrape Dribbble/Behance without real curation.
- Favor resources designers actually use in practice when working on serious products.

Deliverables:
1. Shortlist of 15–30 resources, grouped by type:
   - Award galleries (e.g., Awwwards-like)
   - Curated product/UI pattern libraries (e.g., SiteInspire-/Godly-like)
   - Flow- and component-level libraries (e.g., Mobbin-like)
   - Niche or specialist collections (mobile-only, dashboard-only, UX pattern–focused)

2. For each resource, provide:
   - Name and URL
   - Type (award gallery, pattern library, flow library, etc.)
   - What makes its curation high quality and non-generic
   - Specific strengths (e.g., great mobile flows, strong dashboards, unusual navigation)
   - Any limitations or caveats (paywalled, outdated sections, inconsistent quality)

3. A "starting set" of 6–10 resources that would be most useful for:
   - a) Building a Pinterest-style lookbook of inspiring interfaces
   - b) Selecting 3–5 example apps to run through our Design Kit for analysis

Use clear headings and bullet points so the results can be quickly scanned, bookmarked, and referenced.
```

### Deliverables for this track

* A curated lookbook with at least a first-pass set of 40–60 annotated examples.
* Coverage across several categories (landing, onboarding, discovery/feed, dashboards, mobile flows, chat/interaction).
* A short written summary of:

  * Top 5 patterns that feel most relevant to our product.
  * 3–5 specific examples you think we should study deeply or emulate.

---

## Track 2: App Interface Critique from First Principles (Primary)

### Goal

Evaluate the current app interface from the ground up, using user needs and journeys as the frame, not the current layout. The aim is to identify where the existing design fails users and to propose better flows and end states.

### What you do

1. **Start from user needs and jobs-to-be-done**

   * For each core need (from the product context / user journey doc):

     * State the need clearly.
     * Describe what “success” looks like for the user.

2. **Map how the current interface tries to address each need**

   * Describe the current flow step by step (what they see, click, scroll, etc.).
   * Pay particular attention to:

     * Entry points.
     * Mid-journey states.
     * Final/end states.

3. **Identify friction and failure modes**

   * Where does the flow break down or feel like more work than help?
   * Where do users hit dead ends or low-value screens?
   * Where does the interface feel confusing, heavy, or demotivating?

4. **Pay special attention to**:

   * **Mobile usage**:

     * Assume many users are primarily on their phones.
     * Ask whether the flow and layout make sense on a small screen.
   * **End states**:

     * The last screen of a journey should feel:

       * Rewarding
       * Clearly useful
       * Like real progress, not a dumping ground of more content
   * **Social/chat-like patterns**:

     * Consider whether chat-centric or conversational patterns could help.
     * Avoid gimmicks; focus on flows that feel natural and familiar.

A concrete example already identified as a failure pattern: a build where the “end state” of the experience is a long, undifferentiated list of articles that looks like more work rather than a helpful outcome.

### Suggested critique template

Use a structured format like this for each major need or journey:

```markdown
## Need: <short description>

- Description of the need and desired outcome:
- Current flow (step-by-step):
- Problems / friction:
- Mobile-specific issues:
- Social/chat pattern opportunities:
- Proposed alternative flow (described in words):
- Notes / open questions:
```

### Deliverables for this track

* A document covering all primary user needs / journeys that includes:

  * For each need:

    * Current flow description.
    * Specific problems.
    * Proposed alternative flows or layouts.
  * At least a few concepts for:

    * Mobile-first variations.
    * Chat-centric or socially inspired flows where appropriate.

The goal is depth and clarity of thinking, not pixel-perfect designs.

---

## Track 3: Design Kit Stress-Testing and Refinement (Lower Priority, Optional)

### Priority note

This track is **lower priority by default**. Choose it first only if:

* You are particularly interested in structured thinking about interfaces, and
* You want to help turn our current conceptual model into something that can directly drive a new interface design via AI.

Otherwise, it is better to start with the Lookbook or App Critique tracks and return to this later.

### Goal

Use the existing Design Kit to:

* Run real interfaces through a structured representation of user journeys and UI elements.
* Discover where the kit is unclear, incomplete, or inefficient.
* Propose improvements that make the kit more usable and more directly useful as an AI input format.

Design Kit repository:

* **[https://github.com/grigb/design-kit](https://github.com/grigb/design-kit)**

### What you do

1. **Onboard into the Design Kit**

   * Read the README and any overview docs to understand:

     * The purpose of the kit.
     * The fields and structures it expects.
     * How outputs are intended to be used by AI agents.

2. **Run test interfaces through the kit**

   * Choose interfaces from:

     * Your lookbook.
     * Our current app.
   * For each test interface:

     * Apply the kit step by step.
     * Produce a complete output using the existing fields and templates.

3. **Log issues and gaps**
   While you work, note where:

   * Instructions are unclear or ambiguous.
   * Important aspects of the interface can’t be captured cleanly.
   * Steps feel redundant, out of order, or too vague.
   * The final output doesn’t feel structured enough to hand straight to an AI agent.

4. **Propose and test improvements**

   * For each case, propose concrete changes to the kit:

     * New or renamed fields.
     * Reordered steps.
     * Additional examples or clarifications.
     * Constraints that force more consistent structure.
   * Where feasible, apply your proposed improvements to a different interface and compare:

     * Old vs. new outputs.
     * Which version would give an AI clearer instructions to design or improve an interface.

5. **Document each case as a mini-study**

```markdown
## Case: <interface name>

- Source / URL:
- Screens / flows covered:
- Notes while applying the current kit:
- Problems / gaps in the kit:
- Proposed changes to the kit:
- (If tested) Updated output summary:
- Assessment: which version works better and why:
```

At first, treat the core Design Kit files as read-only. Capture all proposed changes in notes or issues so they can be reviewed and integrated.

### Deliverables for this track

* Several fully completed Design Kit analyses of real interfaces.
* A structured list of issues and proposed improvements to the kit.
* At least one example showing how a refined kit output can be turned into a strong AI prompt for designing a new or improved interface.

---

## Choosing where to start

You are free to choose your starting track:

* If you want to build intuitive design vocabulary and see a lot of patterns quickly, start with **Track 1 (Lookbook)**.
* If you want to engage directly with our product and how it fails or succeeds for users, start with **Track 2 (App Critique)**.
* If you are motivated by structured thinking and AI-ready schemas, and you want to help distill the current concept into a new interface design format, choose **Track 3 (Design Kit)**, understanding that it is lower priority unless you deliberately opt into it.

The only hard requirement is that your outputs are:

* Structured and reusable.
* Grounded in real user needs and flows.
* Clear enough that they can be handed off to design, engineering, or AI agents without needing you in the loop to explain them.
