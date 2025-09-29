Nice — I’ll treat this like a deliverable-ready research brief for your role (senior tech researcher + accessibility lead). Below is a compact, evidence-backed survey you can use, share, or paste into a report. I used official docs, project repos, and high-quality tool reviews as primary sources (search log and citations are at the end). If you want, I can convert this to a CSV/Excel or a canvas doc next — say the format and I’ll produce it immediately.

## Executive summary (TL;DR)

-   Strong, accessible component toolkits exist across two camps: (A) **opinionated design systems** that ship components + guidelines (MUI, Ant Design, Carbon, Fluent, React Spectrum) and (B) **accessibility-first primitives / headless libraries** (React Aria / React Spectrum primitives, Radix, Ariakit, Headless UI). Both camps are useful: pick (A) for speed/consistency; pick (B) for design freedom with accessible behavior guaranteed. [Empathy First Media+1](https://empathyfirstmedia.com/best-react-component-libraries/?utm_source=chatgpt.com)
    
-   Automated test tooling (axe-core, Lighthouse, Pa11y, WAVE) is mature but catches "low-hanging fruit" only — manual testing + AT (VoiceOver/NVDA/JAWS) + usability testing remain essential. [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    
-   Design tokens are actively being discussed as a vehicle for encoding accessibility constraints (contrast, type scales, motion). W3C discussions and industry talks recommend including accessibility metadata in tokens. [W3C+1](https://www.w3.org/2023/09/13-inclusive-design-tokens-minutes.html?utm_source=chatgpt.com)
    
-   Licensing: most prominent UI libs use permissive licenses (MIT or Apache-2.0). Apache grants an explicit patent license; MIT is permissive but lacks an explicit patent grant. Check “pro/paid” editions (MUI Pro/Chakra Pro) for commercial clauses. [mui.com+1](https://mui.com/legal/?utm_source=chatgpt.com)
    

___

## A) INVENTORY: recommended schema (≥20 fields) — _use this to collect per-library data_

1.  Name
    
2.  Primary language / platform (React / Web Components / Platform-agnostic)
    
3.  Public repo URL
    
4.  Official docs URL (accessibility guide page)
    
5.  License (SPDX identifier)
    
6.  License notes (patent clause / commercial add-ons)
    
7.  Focus: opinionated components / headless primitives / design system
    
8.  WCAG/ARIA claim (explicit support for which WCAG level if stated)
    
9.  Built-in ARIA roles & patterns coverage (yes/partial/no + examples)
    
10.  Keyboard navigation completeness (modal, menu, combobox, grid, table)
    
11.  Focus management utilities (trap, restore)
    
12.  Screen reader testing notes (authors claim/third-party audit/WebAIM)
    
13.  Automated-testing integrations (axe, jest-axe, Pa11y, Storybook addon)
    
14.  Developer docs: accessibility patterns & cookbooks (quality score)
    
15.  Design tokens support / recommended token tooling
    
16.  Theming/contrast utilities (semantic tokens, color modes, contrast checks)
    
17.  Web components / multi-framework support
    
18.  Community & corporate backing (stars, contributors, corporate steward)
    
19.  Accessibility fix PR frequency (metric or qualitative)
    
20.  Known accessibility audits or case studies (links)
    
21.  Interoperability & plugin ecosystem (storybook archetypes, linters)
    
22.  Commercial offerings & risk (paid modules, non-open components)
    
23.  Mobile/native support (React Native, iOS/Android guidance)
    
24.  Maintenance status (release frequency, recent commits)
    
25.  Confidence tag (High / Medium / Low) — based on primary-source evidence
    

___

## B) MATRIX: Top 10 libraries evaluated (rubric 0–5 per criterion)

Rubric columns: Built-in WCAG/ARIA support | Testing utilities | Docs & patterns | Community/maintenance | Interoperability/plugin support  
(Short justification + 1–2 citations each; numeric scores are my assessment based on docs/repo & reviews — confidence tags included)

> Sources used for scoring (examples): MUI docs/legal, React Aria / React Spectrum repo, Radix repo, Chakra repo, Ant Design repo, Carbon repo, FluentUI repo, Ariakit, Headless UI docs, axe/tooling reviews. [GitHub+5mui.com+5GitHub+5](https://mui.com/legal/?utm_source=chatgpt.com)

1.  **React Aria / React Spectrum (Adobe)**
    
    -   WCAG/ARIA: 5 — accessibility-first primitives; built specifically against WAI-ARIA practices. [React Spectrum+1](https://react-spectrum.adobe.com/react-aria/index.html?utm_source=chatgpt.com)
        
    -   Testing utilities: 4 — integrates with React Stately / Spectrum patterns; examples & testing guidance. [npm](https://www.npmjs.com/package/%40adobe/react-spectrum?utm_source=chatgpt.com)
        
    -   Docs/patterns: 5 — extensive docs & internationalization guidance. [GitHub](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
        
    -   Community: 4 — Adobe-backed, active repo; Apache-2.0 license. [GitHub](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
        
    -   Interop: 4 — style-free primitives integrate into any design. **Overall**: 4.4 (High confidence)
        
2.  **Radix Primitives**
    
    -   WCAG/ARIA: 5 — primitives focused on keyboard/ARIA behavior. [radix-ui.com](https://www.radix-ui.com/primitives/docs/overview/introduction?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — examples & docs; less formalized testing infra than Adobe. [GitHub](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
        
    -   Docs/patterns: 4 — solid docs, examples. [radix-ui.com](https://www.radix-ui.com/primitives/docs/overview/introduction?utm_source=chatgpt.com)
        
    -   Community: 4 — active repo, MIT license. [GitHub](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
        
    -   Interop: 4 — unstyled primitives for any style system. **Overall**: 4.0 (High confidence)
        
3.  **MUI (Material UI)**
    
    -   WCAG/ARIA: 4 — many components ship with ARIA attributes & focus handling; docs include a11y guidance. [mui.com](https://mui.com/legal/?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — integrations with testing libraries; community axe examples. [Empathy First Media](https://empathyfirstmedia.com/best-react-component-libraries/?utm_source=chatgpt.com)
        
    -   Docs/patterns: 4 — very extensive docs, patterns and examples. [mui.com](https://mui.com/x/introduction/?utm_source=chatgpt.com)
        
    -   Community: 5 — very large user base; MIT license for core. [mui.com](https://mui.com/legal/?utm_source=chatgpt.com)
        
    -   Interop: 4 — theme system, token support (MUI System). **Overall**: 4.0 (High confidence)
        
4.  **Chakra UI**
    
    -   WCAG/ARIA: 4 — explicitly markets accessible components; many built-in a11y behaviors. [GitHub](https://github.com/chakra-ui/chakra-ui?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — community tooling & examples for axe. [Empathy First Media](https://empathyfirstmedia.com/best-react-component-libraries/?utm_source=chatgpt.com)
        
    -   Docs/patterns: 4 — clear docs with accessibility sections; also offers paid Pro components (commercial). [pro.chakra-ui.com+1](https://pro.chakra-ui.com/legal/license?utm_source=chatgpt.com)
        
    -   Community: 4 — active, MIT base license. [GitHub](https://github.com/chakra-ui/chakra-ui?utm_source=chatgpt.com)
        
    -   Interop: 4 — design tokens/semanitc tokens support. **Overall**: 3.8 (High confidence)
        
5.  **Ant Design (Antd)**
    
    -   WCAG/ARIA: 3 — good component breadth; historically enterprise-first (some a11y work). [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
        
    -   Testing utilities: 2 — less focused on a11y tooling out of the box (user projects add axe). [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
        
    -   Docs/patterns: 3 — thorough component docs but accessibility docs are less prominent. [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
        
    -   Community: 5 — huge enterprise adoption, MIT license for most. [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
        
    -   Interop: 3 — theme/customization available. **Overall**: 3.2 (Medium confidence)
        
6.  **Carbon (IBM)**
    
    -   WCAG/ARIA: 4 — enterprise-grade design system with accessibility guidelines and Apache license. [GitHub](https://github.com/carbon-design-system/carbon?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — enterprise testing examples, design guidance. [Carbon Design System](https://carbondesignsystem.com/designing/get-started/?utm_source=chatgpt.com)
        
    -   Docs/patterns: 4 — good accessibility guidance & patterns. [Carbon Design System](https://carbondesignsystem.com/designing/get-started/?utm_source=chatgpt.com)
        
    -   Community: 3 — IBM-backed, steady but less community than MUI. [GitHub](https://github.com/carbon-design-system/carbon?utm_source=chatgpt.com)
        
    -   Interop: 3 — Figma kits + web components. **Overall**: 3.4 (High confidence)
        
7.  **Fluent UI (Microsoft)**
    
    -   WCAG/ARIA: 4 — Microsoft-grade components with accessibility patterns. [GitHub](https://github.com/microsoft/fluentui?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — examples and testing pipelines exist. [npm](https://www.npmjs.com/package/%40fluentui/react?utm_source=chatgpt.com)
        
    -   Docs/patterns: 3 — good docs, mixed guidance across variants. [Microsoft Developer](https://developer.microsoft.com/en-us/fluentui?utm_source=chatgpt.com)
        
    -   Community: 4 — corporate backing + MIT license. [GitHub](https://github.com/microsoft/fluentui?utm_source=chatgpt.com)
        
    -   Interop: 3 — multiple framework implementations. **Overall**: 3.4 (High confidence)
        
8.  **Ariakit**
    
    -   WCAG/ARIA: 5 — marketed as accessibility primitives/toolkit. [ariakit.org](https://ariakit.org/?utm_source=chatgpt.com)
        
    -   Testing utilities: 3 — examples & documentation; some paid “Plus” content exists (license nuance). [GitHub](https://github.com/ariakit/ariakit?utm_source=chatgpt.com)
        
    -   Docs/patterns: 4 — strong focused docs. [ariakit.org](https://ariakit.org/?utm_source=chatgpt.com)
        
    -   Community: 3 — smaller than giants but active. [npm](https://www.npmjs.com/package/ariakit?utm_source=chatgpt.com)
        
    -   Interop: 4 — primitive focus; integrates with styling solutions. **Overall**: 3.8 (Medium–High confidence)
        
9.  **Headless UI (Tailwind Labs)**
    
    -   WCAG/ARIA: 4 — unstyled components designed with accessibility in mind (MIT). [GitHub](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
        
    -   Testing utilities: 2 — mostly examples; heavier reliance on developer testing. [GitHub](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
        
    -   Docs/patterns: 3 — solid docs for primitives. [headlessui.com](https://headlessui.com/?utm_source=chatgpt.com)
        
    -   Community: 4 — Tailwind backing + many users. [GitHub](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
        
    -   Interop: 4 — unstyled + Tailwind synergy. **Overall**: 3.4 (High confidence)
        
10.  **React Spectrum / Reach UI (Reach as separate alternative)**
    
    -   Reach UI: 4 — older project explicitly focused on accessibility testing across ATs; MIT. [GitHub+1](https://github.com/reach/reach-ui?utm_source=chatgpt.com)
        
    -   React Spectrum (Adobe) accounted for earlier; Reach is lightweight but proven. **Overall**: 3.8 (Medium confidence)
        

___

## C) LICENSE TABLE (SPDX, key use-rights/restrictions, patent notes)

(Short list for the top libraries above — confirm license files before legal decisions.)

| Library | SPDX | Key notes / commercial add-ons | Patent clause / risk |
| --- | --- | --- | --- |
| MUI (Core) | MIT. [mui.com](https://mui.com/legal/?utm_source=chatgpt.com) | Core/MUI X community MIT; some MUI X Pro components are commercial (paid). Check package you install. [mui.com](https://mui.com/pricing/?utm_source=chatgpt.com) | MIT — permissive; no explicit patent grant. |
| React Aria / React Spectrum | Apache-2.0. [GitHub+1](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com) | Adobe-backed; Apache gives broader patent language. | Apache-2.0 includes explicit patent grant & termination clauses. |
| Radix Primitives | MIT. [GitHub](https://github.com/radix-ui/primitives?utm_source=chatgpt.com) | MIT. No paid core. | MIT — permissive; no explicit patent grant. |
| Chakra UI | MIT (core). [GitHub](https://github.com/chakra-ui/chakra-ui?utm_source=chatgpt.com) | Chakra Pro / paid components exist — review their license terms. [pro.chakra-ui.com](https://pro.chakra-ui.com/pricing?utm_source=chatgpt.com) | MIT — permissive. |
| Ant Design | MIT. [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com) | Enterprise-focused; look for “Pro” services. | MIT — permissive. |
| Carbon (IBM) | Apache-2.0. [GitHub](https://github.com/carbon-design-system/carbon?utm_source=chatgpt.com) | IBM-backed; design assets may have additional terms (Figma). [Carbon Design System](https://carbondesignsystem.com/designing/design-resources/?utm_source=chatgpt.com) | Apache-2.0 patent grant present. |
| Fluent UI | MIT. [GitHub](https://github.com/microsoft/fluentui?utm_source=chatgpt.com) | Fonts/icons may have separate asset licenses. [GitHub](https://github.com/microsoft/fluentui/discussions/18407?utm_source=chatgpt.com) | MIT — permissive. |
| Ariakit | MIT (core) + proprietary "Plus" examples. [GitHub+1](https://github.com/ariakit/ariakit?utm_source=chatgpt.com) | Some site/examples are proprietary — read the repo layout. | MIT for core; check proprietary sections. |
| Headless UI | MIT. [GitHub+1](https://raw.githubusercontent.com/tailwindlabs/headlessui/refs/heads/main/LICENSE?utm_source=chatgpt.com) | MIT. | MIT — permissive. |
| Reach UI | MIT. [GitHub](https://github.com/reach/reach-ui?utm_source=chatgpt.com) | Focused on ARIA-compliant components and AT testing coverage. | MIT — permissive. |

**Practical license guidance**

-   Apache-2.0 gives an express patent license and is often preferred when corporate patent risk is a concern. [Apache Software Foundation](https://www.apache.org/licenses/LICENSE-2.0?utm_source=chatgpt.com)
    
-   MIT is permissive and widely used but _does not_ include an explicit patent grant — in practice widely adopted but review if patent risk matters. (Legal teams often prefer Apache for explicit patent language.) [SPDX+1](https://spdx.org/licenses/MIT.html?utm_source=chatgpt.com)
    
-   Always check: (a) whether the package you install is the MIT/Apache-licensed _core_ or a commercial “Pro” package, (b) bundled assets (icons/fonts) that may have separate licenses. Several repos include mixed licenses for docs/assets — inspect `LICENSE` files. [GitHub+1](https://github.com/adobe/react-spectrum/discussions/6028?utm_source=chatgpt.com)
    

___

## D) LANDSCAPE: trends, common gaps, and new players

**Trends**

-   Accessibility-first primitives (Radix, React Aria, Ariakit) rising in popularity — they separate behavior from style so teams don't break a11y when re-styling. [radix-ui.com+1](https://www.radix-ui.com/primitives/docs/overview/introduction?utm_source=chatgpt.com)
    
-   Design tokens are becoming the vehicle to encode accessibility constraints (contrast, motion reduction, typography scales) and sync them across platforms; W3C working/notes exist. [W3C+1](https://www.w3.org/2023/09/13-inclusive-design-tokens-minutes.html?utm_source=chatgpt.com)
    
-   Automation + CI integration of accessibility tooling (axe, Pa11y, Lighthouse) is mainstream; product teams integrate automated checks but still pair with manual audits. [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    

**Common gaps**

-   Automated tools miss contextual or cognitive issues; they detect ~30–40% of failures (low-hanging fruit). Manual testing with AT and people with disabilities is still required. [DEV Community+1](https://dev.to/eevajonnapanula/automated-accessibility-testing-is-a-good-start-but-you-need-to-test-manually-too-13f2?utm_source=chatgpt.com)
    
-   Documentation gaps: some large libraries (AntD, some enterprise kits) have less overt a11y pattern cookbooks compared to accessibility-first libs. [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
    
-   Licensing surprises: mixed-license repos and non-code assets (Figma kits, icons) sometimes carry different licenses; watch for CC-BY-ND or commercial content bundled into otherwise open projects. [GitHub](https://github.com/adobe/react-spectrum/discussions/6028?utm_source=chatgpt.com)
    

**New / emerging players to watch**

-   **Ariakit** — smaller but focused; good primitives and docs. [ariakit.org](https://ariakit.org/?utm_source=chatgpt.com)
    
-   **Radix** — rapidly adopted for primitives and design-system foundations. [GitHub](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
    
-   **Headless UI / Shadcn stacks** — comfortable for Tailwind/unstyled patterns and growing in usage. [GitHub+1](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
    

___

## E) Key academic & industry sources (5–15 quoted)

(Selected authoritative sources used to justify claims)

1.  W3C WCAG 2.1 (standards). [W3C](https://www.w3.org/TR/WCAG21/?utm_source=chatgpt.com)
    
2.  Adobe React Spectrum / React Aria (repo & docs). [GitHub+1](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
    
3.  Radix Primitives (official docs & GitHub). [GitHub+1](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
    
4.  MUI legal/docs & MUI X licensing. [mui.com+1](https://mui.com/legal/?utm_source=chatgpt.com)
    
5.  CKEditor / Dev guides on automated accessibility tool comparisons (axe, Lighthouse, Pa11y). [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    
6.  Sparkbox reviews of automated accessibility tools. [sparkbox.com](https://sparkbox.com/foundry/automated_accessibility_tool_reviews?utm_source=chatgpt.com)
    
7.  IBM Carbon Design System docs (design & accessibility guidance). [Carbon Design System](https://carbondesignsystem.com/designing/get-started/?utm_source=chatgpt.com)
    
8.  Tailwind Labs Headless UI (accessibility-first unstyled primitives). [GitHub](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
    

___

## F) Evidence & citations (short list of landing pages used)

-   W3C WCAG 2.1 spec. [W3C](https://www.w3.org/TR/WCAG21/?utm_source=chatgpt.com)
    
-   React Spectrum / React Aria (Adobe GitHub & site). [GitHub+1](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
    
-   Radix Primitives GitHub & docs. [GitHub+1](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
    
-   MUI legal & docs. [mui.com+1](https://mui.com/legal/?utm_source=chatgpt.com)
    
-   Chakra UI GitHub (README shows MIT & accessibility statements). [GitHub](https://github.com/chakra-ui/chakra-ui?utm_source=chatgpt.com)
    
-   Ant Design GitHub. [GitHub](https://github.com/ant-design/ant-design?utm_source=chatgpt.com)
    
-   Carbon Design System docs/repo. [GitHub+1](https://github.com/carbon-design-system/carbon?utm_source=chatgpt.com)
    
-   Headless UI repo & docs. [GitHub+1](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
    
-   Axe/automation tool comparisons (CKEditor, TestGuild). [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    

(If you want, I’ll expand this to 15+ academic references — I focused on high-quality primary sources and authoritative industry reviews.)

___

## G) SEARCH LOG (queries I ran + representative result refs)

I ran a series of targeted searches; below are the query phrases and example result refs you can inspect.

1.  “WCAG component library comparison” → results & WCAG spec. (see: W3C WCAG 2.1). [W3C](https://www.w3.org/TR/WCAG21/?utm_source=chatgpt.com)
    
2.  “UI libraries ARIA support” → React Aria / Radix / Headless UI comparisons. [LogRocket Blog+1](https://blog.logrocket.com/headless-ui-alternatives-radix-primitives-react-aria-ark-ui/?utm_source=chatgpt.com)
    
3.  “automated accessibility testing benchmarks” → CKEditor review, TestGuild lists. [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    
4.  “accessible design tokens” → W3C notes & design-token talks. [W3C+1](https://www.w3.org/2023/09/13-inclusive-design-tokens-minutes.html?utm_source=chatgpt.com)
    
5.  “MUI license MIT” → MUI legal/licensing pages. [mui.com](https://mui.com/legal/?utm_source=chatgpt.com)
    
6.  “React Aria license Apache-2.0” → Adobe react-spectrum repo (Apache-2.0). [GitHub](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
    
7.  “Radix license MIT” → Radix GitHub. [GitHub](https://github.com/radix-ui/primitives?utm_source=chatgpt.com)
    
8.  “Chakra UI license” → Chakra GitHub README (MIT) and Pro licensing pages. [GitHub+1](https://github.com/chakra-ui/chakra-ui?utm_source=chatgpt.com)
    
9.  “Headless UI license” → Headless UI GitHub (MIT). [GitHub](https://github.com/tailwindlabs/headlessui?utm_source=chatgpt.com)
    
10.  “Carbon design system license” → Carbon GitHub (Apache-2.0). [GitHub](https://github.com/carbon-design-system/carbon?utm_source=chatgpt.com)
    
11.  “axe vs Lighthouse vs Pa11y comparison” → CKEditor & Sparkbox reviews. [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    

___

## Confidence tagging & caveats

-   **High confidence**: license for major repos (MUI, React Spectrum, Radix, Chakra, Carbon, Fluent, HeadlessUI) — verified via official repo/legal pages. [GitHub+3mui.com+3GitHub+3](https://mui.com/legal/?utm_source=chatgpt.com)
    
-   **Medium confidence**: exact WCAG level claims for some libraries (some say "WCAG friendly" but do not publish full audit reports). Where a formal audit exists (e.g., React Spectrum/Adobe), confidence is higher. [GitHub](https://github.com/adobe/react-spectrum?utm_source=chatgpt.com)
    
-   **Unknown / verify**: precise PR frequency for accessibility fixes (requires per-repo automated metric collection). I recommend a short script (GitHub API) to measure PR activity if you want exact numbers — I can produce that on request.
    

___

## Recommendations & next steps (practical)

1.  **If you need fast shipping with good accessibility defaults:** use MUI or Chakra and add automation (axe + CI) + manual AT testing. (MUI: large community + strong docs.) [mui.com+1](https://mui.com/legal/?utm_source=chatgpt.com)
    
2.  **If you need complete design freedom while guaranteeing a11y behavior:** pick Radix or React Aria (primitives) so behavior stays correct when you apply your style system. [radix-ui.com+1](https://www.radix-ui.com/primitives/docs/overview/introduction?utm_source=chatgpt.com)
    
3.  **Add toolchain:** integrate axe-core (or axe-core via jest-axe) in unit/CI, Lighthouse for perf/SEO/a11y checks in pipelines, and Pa11y for page-level monitoring. Continue to run manual AT sessions with users. [ckeditor.com+1](https://ckeditor.com/blog/automated-accessibility-testing/?utm_source=chatgpt.com)
    
4.  **Encode accessibility in tokens:** create tokens for semantic color (with contrast metadata), type scales, motion-reduction flags — align token exports to platforms (CSS vars, JSON tokens). W3C conversations are trending here. [W3C+1](https://www.w3.org/2023/09/13-inclusive-design-tokens-minutes.html?utm_source=chatgpt.com)
    
5.  **License checklist for procurement:** confirm that the packages used are core open-source (MIT/Apache) not paid-pro variants; check asset licenses (fonts, icons, Figma files). Flag Apache vs MIT depending on corporate patent comfort. [mui.com+1](https://mui.com/legal/?utm_source=chatgpt.com)
    

___

If you want, next I can:

-   produce a **CSV** with the 20+ inventory fields pre-filled for the top 10 libraries (I can export it immediately), or
    
-   run a **GitHub PR/issue activity script** to measure accessibility-fix PR frequency per repo (requires me to run a script now and return results), or
    
-   expand the sources to a full bibliography of 15+ academic/industry papers.
    

Which of those (CSV / PR-metrics / full bibliography) should I produce now?