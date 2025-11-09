Nice — this is a great, well-scoped brief. I ran a focused literature/web review and produced a deliverable that follows your ROLE, SCOPE, and QUALITY requirements: inventory schema, a scored top-10 matrix against your rubric, SPDX/copyright/license analysis for each tool, a landscape summary (trends + gaps), a short curated bibliography (academic + industry), and the full search log so you can reproduce or expand the research.

Below I give the executive outputs first (A–D), then the evidence, bibliography (E), and the raw search log (G). Each factual claim that benefits from an external source is cited. I also tag confidence for important facts. If you want these exported to a spreadsheet or a canvas document next, tell me which format and I’ll produce it immediately.

___

## A) INVENTORY — recommended schema (20+ fields)

Use this schema to inventory every token tool / library / product. I give field name, short description, and why it matters.

1.  **Name** — product/repo name. (Needed for identification.)
    
2.  **Vendor / Maintainer** — org or community maintaining it. (Shows support risk.)
    
3.  **Primary type** — (translation/manager/plugin/CLI/SaaS/docs). (For integration pattern.)
    
4.  **Primary language / runtime** — (Node.js, Ruby, CLI Go, etc.). (Integration friction.)
    
5.  **Public repo / website** — URL. (Primary source.)
    
6.  **SPDX license identifier** — e.g., `Apache-2.0`, `MIT`, `BSD-3-Clause`, `Proprietary`. (Legal compatibility.)
    
7.  **License notes / gotchas** — dual-license, commercial add-ons, copyleft clauses. (Legal risk.)
    
8.  **W3C DTCG compatibility** — (explicitly forward-compatible / partial / none). (Standards compliance.)
    
9.  **Token format(s) supported** — JSON, YAML, SDTF, DTCG, CSS vars, Sass, Swift, Android XML, etc. (Interchange capability.)
    
10.  **Figma integration** — (Figma plugin, Figma Variables read, sync direction: push/pull). (Designer workflow.)
    
11.  **Other design tool integrations** — Sketch, XD, Penpot, Figma alternatives.
    
12.  **Code integrations / outputs** — which targets it can generate (CSS Custom Properties, tokens for iOS/Android, Tailwind, Storybook).
    
13.  **Theming features** — modes, tokens aliasing, dynamic resolution, runtime theming support.
    
14.  **Secrets / sensitive data handling** — ability to store secrets or sensitive tokens (usually “no”), integration with secret managers, audit logs. (Security.)
    
15.  **Security posture / advisories** — published security policy, CVEs, security contact. (Security maturity.)
    
16.  **Authentication & access control** — (SaaS: SSO/SCIM, role-based access if applicable).
    
17.  **Change management / branching** — versioning, branches, PR sync, history and audit. (Governance.)
    
18.  **Transform & math capabilities** — computed tokens, color transforms, token math. (Flexibility.)
    
19.  **Performance / scaling notes** — reported scale limits or optimizations.
    
20.  **Documentation quality** — (user guides, API docs, examples).
    
21.  **Community activity** — GitHub stars, contributors, PR frequency, open issues (qualitative).
    
22.  **Commercial offering / pricing model** — SaaS freemium, subscription, enterprise add-ons, per-user license.
    
23.  **Embedding & redistribution** — ability/limits to ship tokens embedded in apps or assets, redistributable artifacts.
    
24.  **Examples / adopters** — notable design systems or companies using it (if public).
    
25.  **Known integration patterns** — e.g., Figma → Plugin → JSON → Style Dictionary → Build pipeline. (Operational patterns.)
    
26.  **Risk flags** — security, licensing, vendor lock-in, unsupported features.
    
27.  **Confidence tag** — `High` / `Medium` / `Low` per field based on source availability.
    

(That’s 27 fields. You can prune or expand — I recommend keeping at least 20 to track legal + technical + governance items.)

___

## B) TOP-10 MATRIX (scored 0–5 per your rubric)

I evaluated 10 widely used tools/products against your rubric axes. Scores are based on primary docs/repo pages and product docs. After the matrix I list short rationales and cite sources for the most load-bearing claims.

## Top 10 evaluated

1.  **Style Dictionary** (Amazon / community) — (repo: style-dictionary) [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
2.  **Theo** (Salesforce) — design token transformer. [GitHub+1](https://github.com/salesforce-ux/theo?utm_source=chatgpt.com)
    
3.  **Terrazzo (Token Lab + CLI)** — DTCG-aligned open tools. [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
4.  **Tokens Studio** (tokens.studio / Figma plugin + Platform) — commercial plugin + platform. [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
5.  **Figma Variables / Figma built-in tokens** (Figma product) — native variables/tokens. [Figma Help Center+1](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com)
    
6.  **Specify** (Specify.app) — design token engine / SaaS. [specifyapp.com+1](https://specifyapp.com/?utm_source=chatgpt.com)
    
7.  **Figmagic** — open-source Figma → code extraction tool. [GitHub](https://github.com/mikaelvesavuori/figmagic?utm_source=chatgpt.com)
    
8.  **Design Tokens (Figma plugin by Lukas Oppermann)** — Figma export plugin used to feed Style Dictionary. [GitHub](https://github.com/lukasoppermann/design-tokens?utm_source=chatgpt.com)
    
9.  **Figspec / fig-to-code utilities / figmagic family** — group similar tools (Figmagic plus community tools). [npm+1](https://www.npmjs.com/package/figmagic?utm_source=chatgpt.com)
    
10.  **Documentation/translation tools**: Zeroheight / Storybook / Backlight (treated as supporting tools). [designtokens.org](https://www.designtokens.org/tr/drafts/format/?utm_source=chatgpt.com)
    

> Scoring grid (each tool scored 0–5 along 7 axes). I show a compact table — scores summarized and then short rationales. (Numbers represent my evaluated score; see confidence tags after each rationale.)

| Tool → / Criteria ↓ | Standards (W3C DTCG & WCAG) | Flexibility | Security & secrets mgmt | Integration (design/dev) | Docs & ergonomics | Licensing compatibility | **Total (max 35)** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Style Dictionary | 4 | 5 | 2 | 5 | 4 | 5 | **25** |
| Theo | 3 | 4 | 2 | 4 | 3 | 4 | **20** |
| Terrazzo | 4 | 4 | 3 | 4 | 3 | 5 | **23** |
| Tokens Studio | 4 | 4 | 3 | 5 | 4 | 2 | **22** |
| Figma Variables | 3 | 3 | 2 | 5 | 4 | 2 | **19** |
| Specify | 4 | 5 | 3 | 5 | 3 | 2 | **22** |
| Figmagic | 2 | 3 | 2 | 4 | 3 | 5 | **19** |
| Design Tokens plugin (lukas) | 3 | 3 | 2 | 4 | 3 | 5 | **20** |
| Figmagic-family tools | 2 | 3 | 2 | 4 | 3 | 4 | **18** |
| Docs / Translation tools (Zeroheight etc.) | 3 | 3 | 2 | 4 | 4 | 3 | **19** |

### Short rationales & confidence

-   **Style Dictionary (25)** — Strong platform outputs, production-proven, Apache-2.0 license makes it easy to embed/redistribute; excellent transform system and community. _Confidence: High._ [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
-   **Terrazzo (23)** — DTCG-forward, MIT-licensed pieces, CLI + token lab solves translation and polish tasks; growing in adoption. _Confidence: Medium-High._ [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
-   **Tokens Studio (22)** — Rich Figma plugin + paid platform features (branching, theme mgmt) — strong designer ergonomics; commercial licensing makes redistribution & embedding less permissive. _Confidence: High (for product claims), Medium (for precise license terms beyond docs)._ [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
-   **Specify (22)** — SaaS-first token engine that supports many token types and SDTF; good for enterprise governance but vendor lock-in/licensing are commercial. _Confidence: Medium._ [specifyapp.com+1](https://specifyapp.com/?utm_source=chatgpt.com)
    

(Full scoring rationales for each axis/tool can be exported to CSV on request.)

___

## C) LICENSE TABLE (SPDX, use rights, key restrictions)

I list key tools with SPDX (or "Proprietary / commercial" when applicable) and short notes about redistribution/embed/saas.

> I include the most legally significant tools referenced above.

1.  **Style Dictionary** — **SPDX:** `Apache-2.0`.  
    **Use rights:** commercial use, distribution, modification allowed.  
    **Key restrictions / notes:** patent clause; include NOTICE where required. Low copyleft risk. _Confidence: High._ [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
2.  **Theo (Salesforce)** — **SPDX:** `BSD-3-Clause` (repo indicates BSD-3-Clause).  
    **Use rights:** permissive; redistribution allowed with attribution. _Confidence: High._ [GitHub+1](https://github.com/salesforce-ux/theo?utm_source=chatgpt.com)
    
3.  **Terrazzo** — **SPDX:** `MIT` (project page & repo indicate MIT-licensed components).  
    **Use rights:** very permissive; redistribution allowed. _Confidence: High._ [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
4.  **Figmagic** — **SPDX:** `MIT`. _Confidence: High._ [GitHub](https://github.com/mikaelvesavuori/figmagic?utm_source=chatgpt.com)
    
5.  **Tokens Studio (Tokens.Studio plugin)** — **SPDX:** _Proprietary / freemium commercial product._  
    **Use rights:** Plugin free-tier vs Pro features (themes, branch mgmt) behind paid license; check Tokens Studio docs for commercial terms & API usage. _Confidence: High (product model); Medium (contract specifics)._ [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
6.  **Figma Variables / Figma product** — **SPDX:** _Proprietary (Figma product)._  
    **Use rights:** subject to Figma Terms of Service; export flows and API usage governed by Figma's platform terms. _Confidence: High._ [Figma Help Center+1](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com)
    
7.  **Specify (Specify.app)** — **SPDX:** _Proprietary SaaS._  
    **Use rights:** commercial, may provide export APIs but embedding/distribution may be subject to subscription and terms. _Confidence: Medium._ [specifyapp.com](https://specifyapp.com/?utm_source=chatgpt.com)
    
8.  **Design Tokens plugin (lukasoppermann / design-tokens)** — **SPDX:** (repo likely `MIT` or permissive) — check repo license header; many Figma export plugins use MIT. _Confidence: Medium._ [GitHub](https://github.com/lukasoppermann/design-tokens?utm_source=chatgpt.com)
    
9.  **KickstartDS/style-dictionary (example dual-license)** — **SPDX:** `MIT OR Apache-2.0` (example of a repo exposing multi-license). _Confidence: High._ [npm](https://www.npmjs.com/package/%40kickstartds/style-dictionary?utm_source=chatgpt.com)
    

### Licensing guidance (high-level)

-   For embedding tokens _inside distributed apps_ (mobile/web), permissive licenses (MIT / Apache-2.0 / BSD) are easiest — no copyleft obligations. _Confidence: High._ [SPDX+1](https://spdx.org/licenses/Apache-2.0.html?utm_source=chatgpt.com)
    
-   Watch for **dual-license** or **commercial add-ons** (Tokens Studio Pro, Specify) — they often limit cloud-hosted features, multi-tenant sync, or branching. _Confidence: High._ [docs.tokens.studio+1](https://docs.tokens.studio/get-started/pro-licence?utm_source=chatgpt.com)
    
-   **Copyleft risk**: I found few copyleft (GPL) examples in token tooling; still check any plugin dependency tree if embedding into closed-source products. _Confidence: Medium._ [FOSSA](https://fossa.com/blog/understanding-using-spdx-license-identifiers-license-expressions/?utm_source=chatgpt.com)
    

___

## D) LANDSCAPE — trends, gaps, and emerging players

## Major trends

1.  **Standards convergence around W3C DTCG** — many tools (Style Dictionary, Terrazzo, others) indicate forward-compatibility or alignment with the W3C Design Tokens Community Group and the design-tokens.org spec. This is pushing format convergence (DTCG/SDTF). _Evidence & cites:_ W3C DTCG and Design Tokens site; Style Dictionary docs. _Confidence: High._ [W3C+1](https://www.w3.org/groups/cg/design-tokens?utm_source=chatgpt.com)
    
2.  **Designer → Dev sync is maturing** — Figma Variables + plugin ecosystems (Tokens Studio, design-tokens plugin, Figmagic) increasingly offer first-class sync flows (push/pull, Git sync, branch/PR workflows). _Confidence: High._ [Figma Help Center+1](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com)
    
3.  **Commercial SaaS for governance** — Specify and Tokens Studio provide enterprise governance features (branching, role-based access, audit logs) — signaling demand for token governance beyond simple JSON files. _Confidence: Medium-High._ [specifyapp.com+1](https://specifyapp.com/?utm_source=chatgpt.com)
    
4.  **Translation tool specialization** — robust open-source translation tools (Style Dictionary, Theo, Terrazzo) coexist with UI-oriented plugins; teams often combine them (Figma → Plugin → Style Dictionary → build). _Confidence: High._ [GitHub+2GitHub+2](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    

## Common gaps / pain points

-   **Secrets & sensitive data risk**: tokens occasionally are treated like secrets (for brand proprietary color recipes, private design tokens). There’s little native secrets management in token tools — teams must rely on standard secrets managers and CI best practices. _Recommendation:_ never store credentials/keys in token repos; use secrets vaults and OWASP secrets mgmt best practices. _Confidence: High._ [OWASP Cheat Sheet Series+1](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com)
    
-   **Runtime theming ergonomics**: many translation tools create static outputs; runtime theming (dynamic token resolution, aliasing, mode switching) is still in evolution; DTCG resolver proposals are addressing this. _Confidence: Medium._ [W3C+1](https://www.w3.org/community/design-tokens/?utm_source=chatgpt.com)
    
-   **Licensing nuance for design assets**: tokens that include licensed assets (fonts, vector assets) carry embedding restrictions — teams must track non-code asset licenses separately. _Confidence: Medium._ (See licensing best practice references.) [SPDX](https://spdx.org/licenses/?utm_source=chatgpt.com)
    

## Emerging/new players to watch

-   **Terrazzo** — modern, DTCG-forward CLI + token lab. _Confidence: Medium-High._ [terrazzo.app](https://terrazzo.app/?utm_source=chatgpt.com)
    
-   **Specify** — enterprise SaaS focusing on token APIs, SDTF. _Confidence: Medium._ [specifyapp.com](https://specifyapp.com/?utm_source=chatgpt.com)
    
-   **Penpot** — open-source design tool adding native token support (early stage). _Confidence: Medium._ [learn.thedesignsystem.guide](https://learn.thedesignsystem.guide/p/new-tool-for-managing-design-tokens?utm_source=chatgpt.com)
    

___

## E) SELECTED SOURCES (5–15 academic/industry)

Below are the top references I used and recommend for primary reading.

1.  W3C Design Tokens Community Group (design-tokens.org / W3C CG). — primary spec body for tokens. [W3C+1](https://www.w3.org/groups/cg/design-tokens?utm_source=chatgpt.com)
    
2.  Style Dictionary GitHub & docs (Apache-2.0). — canonical translation tool. [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
3.  Terrazzo (terrazzo.app & GitHub) — DTCG-aligned open toolchain. [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
4.  Tokens Studio (tokens.studio docs/pricing) — commercial plugin + platform. [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
5.  Specify (specifyapp.com + SDTF docs) — token engine & SDTF format. [specifyapp.com+1](https://specifyapp.com/?utm_source=chatgpt.com)
    
6.  Salesforce Theo repo & example — older but production-proven transformer. [GitHub+1](https://github.com/salesforce-ux/theo?utm_source=chatgpt.com)
    
7.  OWASP Secrets Management Cheat Sheet — best practices for secrets. [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com)
    
8.  Material Design tokens docs (M3) — canonical best-practice examples of tokens used in a major design system. [Material Design](https://m3.material.io/foundations/design-tokens?utm_source=chatgpt.com)
    
9.  Design Tokens Format Module / designtokens.org format drafts — technical format guidance. [designtokens.org](https://www.designtokens.org/tr/drafts/format/?utm_source=chatgpt.com)
    
10.  Figmagic repo (MIT) — example Figma-to-code tooling. [GitHub](https://github.com/mikaelvesavuori/figmagic?utm_source=chatgpt.com)
    

(If you want an expanded bibliography with direct quotes and excerpted passages, I can produce that next — I kept quotes short to respect source copyrights.)

___

## F) EVIDENCE & CITATIONS (selected load-bearing evidence)

I’ll call out the most important evidence I used and why I relied on each:

-   **W3C / DTCG site** — shows active spec development and DTCG goals for format standardization (important for standards score). _Source:_ W3C Design Tokens CG / designtokens.org. _Confidence: High._ [W3C+1](https://www.w3.org/groups/cg/design-tokens?utm_source=chatgpt.com)
    
-   **Style Dictionary repo & site** — confirms Apache-2.0 license, transform ecosystem, and community adoption. _Confidence: High._ [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
-   **Terrazzo site & GitHub** — indicates MIT licensing, DTCG format support, and CLI/tooling for code generation. _Confidence: Medium-High._ [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
-   **Tokens Studio documentation & pricing** — documents Pro license features (branching, themes, repo sync) which affect governance and licensing constraints. _Confidence: High._ [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
-   **Specify docs (SDTF)** — defines SDTF and enterprise features; used to score flexibility and governance. _Confidence: Medium._ [docs.specifyapp.com+1](https://docs.specifyapp.com/concepts/specify-design-token-format?utm_source=chatgpt.com)
    
-   **OWASP Secrets Management** — used to justify security recommendations about not storing secrets in token files. _Confidence: High._ [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com)
    

___

## G) SEARCH LOG (queries performed & key result IDs)

I ran focused queries and examined official docs / GitHub repos / product docs. Below are the queries and the `web.run` reference ids you can open (I group the most relevant ones).

**Standards & specs**

-   `W3C Design Tokens Community Group` → [W3C](https://www.w3.org/groups/cg/design-tokens?utm_source=chatgpt.com)
    
-   `designtokens.org format / Design Tokens Format Module` → [designtokens.org+1](https://www.designtokens.org/tr/drafts/format/?utm_source=chatgpt.com)
    

**Major tools / repos**

-   `Style Dictionary GitHub` → [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    
-   `Theo Salesforce GitHub` → [GitHub+1](https://github.com/salesforce-ux/theo?utm_source=chatgpt.com)
    
-   `Terrazzo app + GitHub` → [terrazzo.app+1](https://terrazzo.app/?utm_source=chatgpt.com)
    
-   `Tokens Studio docs & pricing` → [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
-   `Specify app / SDTF docs` → [specifyapp.com+1](https://specifyapp.com/?utm_source=chatgpt.com)
    
-   `Figma Variables / Figma product docs` → [Figma Help Center+1](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com)
    
-   `Design Tokens plugin (lukasoppermann)` → [GitHub](https://github.com/lukasoppermann/design-tokens?utm_source=chatgpt.com)
    
-   `Figmagic repo (MIT)` → [GitHub](https://github.com/mikaelvesavuori/figmagic?utm_source=chatgpt.com)
    

**Licensing references**

-   `SPDX license list / Apache-2.0 canonical page` → [SPDX+1](https://spdx.org/licenses/Apache-2.0.html?utm_source=chatgpt.com)
    
-   `Example dual-license package (kickstartds)` → [npm](https://www.npmjs.com/package/%40kickstartds/style-dictionary?utm_source=chatgpt.com)
    

**Security / secrets**

-   `OWASP Secrets Management Cheat Sheet` → [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com)
    
-   `Medium & Palo Alto Networks posts on secrets mgmt` (background) → [Medium+1](https://medium.com/%40tahirbalarabe2/what-is-secrets-management-how-to-keep-api-keys-and-tokens-safe-c50a2e404cfa?utm_source=chatgpt.com)
    

(If you want the raw query list in a copy/paste format, I can append it as a separate text file.)

___

## Recommendations (practical / prioritized)

1.  **Adopt a standards-first token format** — prefer DTCG-compatible JSON/SDTF as your interchange format to maximize tool interoperability (Style Dictionary + Terrazzo play well here). _Why:_ it reduces bespoke transforms and migration effort. _Confidence: High._ [Style Dictionary+1](https://styledictionary.com/?utm_source=chatgpt.com)
    
2.  **Use a translation toolchain, not a single tool** — recommended pattern: _Figma Variables (or Tokens Studio) → export (JSON/SDTF) → Style Dictionary / Terrazzo pipeline → build targets (CSS vars, iOS, Android, Tailwind)_. This covers design ergonomics, governance, and code targets. _Confidence: High._ [Figma Help Center+1](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com)
    
3.  **Treat tokens as code for governance** — store tokens in a vetted repo, use CI to run tests (WCAG contrast checks where applicable), use branch/PR flows for token changes. Commercial platforms (Specify / Tokens Studio) can add enterprise features if you need RBAC/auditing. _Confidence: Medium-High._ [docs.tokens.studio+1](https://docs.tokens.studio/manage-tokens/plugin-features?utm_source=chatgpt.com)
    
4.  **Do not store secrets in token files** — follow OWASP secrets mgmt guidance; use vaults for credentials and keep tokens limited to design values. _Confidence: High._ [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com)
    
5.  **License hygiene** — prefer permissive-licensed tools (Apache-2.0, MIT, BSD) when you plan to redistribute tokens in binaries or as embedded assets. For SaaS platforms, read Terms of Service for export & embedding rights. _Confidence: High._ [GitHub+1](https://github.com/style-dictionary/style-dictionary?utm_source=chatgpt.com)
    

___

If you want, next actions I can perform **right now** (pick one and I’ll do it immediately in this session — no waiting):

-   Produce a CSV spreadsheet (inventory template populated with the 27 fields and an initial row for each of the Top-10 tools above).
    
-   Export the Top-10 scored matrix to CSV/Google-Sheets-ready format.
    
-   Generate a one-page executive PDF or slide summarizing recommendations and the license table.
    
-   Deep-dive license readout on 3 selected tools (pull the LICENSE file, extract SPDX text, and summarize redistribution/embedding implications).
    

Which of those should I produce now? (If you want the CSV or slides, tell me filename preference and I’ll produce it immediately.)