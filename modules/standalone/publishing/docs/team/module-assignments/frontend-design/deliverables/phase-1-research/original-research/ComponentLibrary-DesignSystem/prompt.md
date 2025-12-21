==== PROMPT 1 of 6: Comparative Analysis of Major Open-Source UI Libraries ====
ROLE DEFINITION:
Act as a senior technology & market researcher, open-source licensing analyst (SPDX-aware), and competitive intelligence specialist with deep expertise in frontend development frameworks and UI component libraries.

SCOPE SPECIFICATION:

    Analyze MUI, Ant Design, Chakra UI, Mantine, and Tailwind CSS as primary candidates.

    Include both open-source and commercial variants, if any.

    Consider mature and emerging alternatives where relevant.

    Cover self-hosted, managed/cloud, and hybrid models for each.

    Explore adjacent approaches such as other major React/Vue/Svelte libraries.

SEARCH METHODOLOGY:

    Use search queries: “mui vs antd vs chakra vs mantine vs tailwind comparison,” “top react ui libraries,” “opensource ui libraries benchmark,” “component library security,” “ui library accessibility,” “npm popularity,” “ui system roadmap,” and “license analysis.”

    Source order: official documentation, GitHub/wikis, reputable tech blogs and reviews, npm statistics, academic and analyst studies (ACM/IEEE/arXiv), and package indexers.

    Maintain a search log with queries and encountered dead ends.

LICENSING ANALYSIS FRAMEWORK:

    Assign SPDX IDs for each library and any bundled dependencies.

    Analyze terms for internal, public SaaS, on-prem distribution, embedding.

    Flag copyleft triggers, network clauses, commercial/patent terms, dual licenses, and CLAs.

EVALUATION RUBRIC (0-5 score per criterion):

    Fit to common use cases (enterprise/web/mobile)

    Maturity & stability

    Maintenance & community health

    Security posture and patching practices

    Performance characteristics

    Accessibility support (WCAG/ARIA)

    Theming/customization options

    Interoperability/compatibility

    Licensing compatibility and risk

    Depth/quality of documentation

METRICS COLLECTION:

    Popularity: GitHub stars/forks, npm/month downloads, package age

    Momentum: monthly/annual growth rates, release cadence, new contributors

    Explain unavailable metrics

REQUIRED OUTPUTS:
A) INVENTORY: CSV/JSONL with 20+ fields per library
B) COMPARATIVE MATRIX: Top 10-20 options scored
C) LICENSING MATRIX: SPDX ID, permissions, restrictions, mitigations
D) LANDSCAPE SUMMARY: Clustering leaders, gaps, emerging players
E) ACADEMIC SNAPSHOT: 5-15 core papers, one-line takeaway each
F) EVIDENCE PACK: Citation + ≤40-word quote per claim
G) SEARCH LOG: All queries + rationale + dead ends

QUALITY REQUIREMENTS:

    Prioritize primary sources

    Confidence tagging per fact

    Use “unknown” for conjecture

    Flag issues when direct browsing unavailable
    ==== END PROMPT 1 ====

==== PROMPT 2 of 6: Design Tokens, Theming, and Customization in Design Systems ====
ROLE DEFINITION:
Function as a senior technology & market researcher, UX engineer, and design systems expert with open-source licensing acumen.

SCOPE SPECIFICATION:

    Map the role of design tokens and theming in modern UI architecture.

    Include both open-source and commercial token management tools, open standards (e.g., W3C Design Tokens Community Group), and emerging best practices.

    Examine integration patterns with Figma, Style Dictionary, and major component libraries.

SEARCH METHODOLOGY:

    Search: “design tokens library comparison,” “open-source theming engine,” “design token standards roadmap,” “token management security,” “design tokens WCAG,” “license analysis design-token repo.”

    Source order: official docs/specs, GitHub repos, reputable dev blogs, design system case studies, academic and industry whitepapers.

    Document search strategy and rationale.

LICENSING ANALYSIS FRAMEWORK:

    SPDX IDs for core token tools, theming frameworks, and related assets.

    Analyze legal terms for use, redistribution, cloud/SaaS, and asset embedding.

    Highlight dual licenses, copyleft risks, commercial add-on terms.

EVALUATION RUBRIC (0-5 score):

    Standards compliance (e.g., W3C, WCAG)

    Flexibility/extensibility

    Security and secrets management

    Integration with design/dev tools

    Documentation and tool ergonomics

    Licensing compatibility

METRICS COLLECTION:

    Adoption by design systems/brands

    Growth indicators (community/PRs/releases)

    Documentation quality

    Address missing metrics

REQUIRED OUTPUTS:
A) INVENTORY: 20+ schema fields
B) MATRIX: Top 10 scored
C) LICENSE TABLE: SPDX, use rights, key restrictions
D) LANDSCAPE: Trends, common gaps, new players
E) 5-15 academic/industry sources quoted
F) EVIDENCE cited
G) SEARCH LOG

QUALITY REQUIREMENTS:

    As above, with confidence ranking per assertion
    ==== END PROMPT 2 ====

==== PROMPT 3 of 6: Accessibility (WCAG/ARIA) in UI Libraries and Design Systems ====
ROLE DEFINITION:
Senior technology researcher and digital accessibility lead, with open-source licensing expertise.

SCOPE SPECIFICATION:

    Survey accessible component libraries, ARIA support, WCAG compliance tools/material.

    Cover both React/JS and platform-agnostic approaches.

    Highlight open-source vs. proprietary accessibility solutions.

SEARCH METHODOLOGY:

    Queries: “WCAG component library comparison,” “UI libraries ARIA support,” “automated accessibility testing benchmarks,” “accessibility license risk,” “accessible design tokens.”

    Prioritize: official docs, accessibility orgs (W3C, ARIA WG), web dev/accessibility advocacy sites, code repos, academic studies.

    Maintain query logs and evaluation notes.

LICENSING ANALYSIS FRAMEWORK:

    SPDX for libraries and accessibility tools

    Note accessibility-specific patent clauses if present

EVALUATION RUBRIC (0-5):

    Built-in WCAG/ARIA support

    Testing utilities

    Documentation, guidance, and patterns

    Ecosystem/community involvement

    Interoperability and plugin support

METRICS COLLECTION:

    Usage/adoption by major brands

    Accessibility-fixes PR frequency

    Tooling integration rates

REQUIRED OUTPUTS: (A-G as in prompt 1)

QUALITY REQUIREMENTS:

    Source/citation rigor, confidence scores, “unknown” for missing
    ==== END PROMPT 3 ====

==== PROMPT 4 of 6: Atomic Design Methodology Implementation ====
ROLE DEFINITION:
Senior UX technology/process researcher and systems architect with open-source licensing literacy.

SCOPE SPECIFICATION:

    Evaluate approaches, frameworks, and tools for adopting atomic design (atoms, molecules, organisms, etc.) in component libraries.

    Cover open-source/project templates, generators, and commercial frameworks.

    Include adjacent methodologies where relevant.

SEARCH METHODOLOGY:

    Search: “atomic design react library review,” “atomic design boilerplate,” “component breakdown strategies,” “atomic design standards,” “license analysis for templates.”

    Preference: origin sources (Brad Frost et al), reputable code showcases, academic/pedagogical papers, corporate case reports.

LICENSING ANALYSIS FRAMEWORK:

    SPDX for templates and tools used

    Custom code licensing and extension rights

EVALUATION RUBRIC (0-5):

    Structural flexibility

    Fit to scaling/enterprise needs

    Ease of integration

    Documentation/examples

    Licensing risk

METRICS COLLECTION:

    Community adoption

    Project update cadence

    Learning curve evidence

REQUIRED OUTPUTS: (A-G as in prompt 1)

QUALITY REQUIREMENTS:

    Evidence-based with direct source citations
    ==== END PROMPT 4 ====

==== PROMPT 5 of 6: Enterprise Design System Architecture and Scaling Strategies ====
ROLE DEFINITION:
Enterprise technology researcher, open-source analyst, and design systems strategist.

SCOPE SPECIFICATION:

    Analyze prevailing architectures for large-scale design systems.

    Include reference architectures (mono-repo, micro-frontends, modular, etc.), scaling strategies, and tooling.

    Assess both open-source and commercial system examples.

SEARCH METHODOLOGY:

    Search: “enterprise design system architecture survey,” “scalable component library patterns,” “large org design system case study,” “multi-brand theming,” “license and contribution policies.”

    Sequence: vendor whitepapers, company tech blogs, peer-reviewed studies, GitHub repos, system showcases.

    Comprehensive query and approach documentation.

LICENSING ANALYSIS FRAMEWORK:

    SPDX for all system components/tools

    Analyze organization-level reuse/redistribution rights

EVALUATION RUBRIC (0-5):

    Scalability (tech/process/culture)

    Modularity and maintainability

    Multi-brand/theming support

    Documentation/process rigor

    Governance/licensing fit

METRICS COLLECTION:

    System adoption (internal/external users)

    Release/versioning cadence

    Contributor growth

REQUIRED OUTPUTS: (A-G as in prompt 1)

QUALITY REQUIREMENTS:

    Strict sourcing, marking confidence, flagging gaps
    ==== END PROMPT 5 ====

==== PROMPT 6 of 6: Documentation Strategies and Long-Term Maintenance for Custom Component Libraries ====
ROLE DEFINITION:
Senior engineering process researcher and documentation technologist, with open-source compliance specialization.

SCOPE SPECIFICATION:

    Survey tooling, templates, and best practices for documenting and maintaining custom component libraries.

    Include live docs, auto-generated API ref, usage guides, versioned changelogs.

    Benchmark maintenance strategies, including contribution models and community engagement.

SEARCH METHODOLOGY:

    Search: “component library documentation best practices,” “living docs tools UI,” “API doc generators comparison,” “component library maintenance patterns,” “license analysis doc template.”

    Order: official tool/project docs, developer case studies, academic/industry whitepapers, OSS community posts.

LICENSING ANALYSIS FRAMEWORK:

    SPDX review for doc tooling/templates

    Note documentation artifacts licensing

EVALUATION RUBRIC (0-5):

    Documentation completeness

    Ease of update and maintenance

    Contributor on-boarding/support

    Reference/example quality

    Tooling integration

    Licensing/redistribution clarity

METRICS COLLECTION:

    Library documentation usage metrics

    Changelog PR frequency

    External contributor rates

REQUIRED OUTPUTS: (A-G as in prompt 1)

QUALITY REQUIREMENTS:

    High-confidence evidence, explicit “unknown” when unclear
    ==== END PROMPT 6 ====
