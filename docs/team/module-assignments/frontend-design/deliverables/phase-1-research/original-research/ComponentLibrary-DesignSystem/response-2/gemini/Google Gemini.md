## The Modern UI Architecture: A Due Diligence Report on Design Tokens and Theming

## Executive Summary

The analysis of the modern UI architecture reveals that design tokens have evolved from a mere technical convenience into a central, strategic asset for UI development. The ecosystem is maturing, driven by a growing recognition of tokens as the authoritative "single source of truth" for design decisions. This shift is solidified by the proliferation of specialized tooling and the momentum behind the W3C Design Tokens Community Group (DTCG) specification.

**Key Findings:**

-   **Strategic Function:** Design tokens are fundamentally a communication tool that creates a shared language between design and engineering, significantly reducing guesswork and manual handoffs.  
    
-   **Architectural Maturity:** The most effective design systems adopt a multi-layered token taxonomy (Primitive, Semantic, Component-specific) to provide a scalable and maintainable foundation. Case studies show this approach yields tangible business benefits, such as reduced dead code and improved page performance.  
    
-   **Ecosystem Dynamics:** The market is bifurcated. On one side, powerful, flexible open-source tools like Style Dictionary serve as unopinionated transformation engines. On the other, commercial SaaS platforms like Supernova and Specify provide a complete, managed, and highly automated end-to-end pipeline from design to code, effectively commoditizing the manual orchestration process.  
    
-   **Standardization:** The DTCG draft, while not a formal W3C standard, is the de facto reference for the community, with major tools already building for forward-compatibility. This proactive adoption, however, creates a potential for fragmentation in implementations.  
    
-   **Legal Nuances:** The open-source licensing landscape for design tokens is complex. While permissive licenses (e.g., MIT, Apache-2.0) are prevalent, the use of strong copyleft licenses presents a legal risk, as the generated code could be classified as a derivative work.  
    

**Strategic Recommendations:** Teams should prioritize the adoption of a layered token architecture and select tools that align with the DTCG draft to ensure future-proofing. It is critical to invest in an automated pipeline from design to code to achieve significant efficiency gains and reduce technical debt. For a successful implementation, a thoughtful change management plan and a formal governance model must be established from the outset.

## 1\. Foundational Concepts: Design Tokens & Theming

### 1.1. Defining the Single Source of Truth: What are Design Tokens?

Design tokens are defined as "design decisions, translated into data". They are not merely static variables or hardcoded values; they are a sophisticated communication tool that creates a "shared language between design and engineering" for building user interfaces. The core of a design token is a key-value pair, such as a color, a spacing measurement, or a typography setting. For instance, a token can represent an RGBA color value, a numerical opacity, or Bezier coordinates for an animation ease.  

The significance of this methodology lies in its ability to replace hardcoded values with self-explanatory, purpose-driven names. This approach fundamentally changes how design and development teams collaborate. Without tokens, a team would have to manually find and update every instance of a color or font across design files, documentation, and code. This process is slow, prone to error, and creates significant bottlenecks. By centralizing these decisions in a single, updatable source, a simple change to a token's value can instantly propagate across an entire product or suite of products, ensuring consistency and drastically accelerating workflows. The value of this approach extends beyond technical efficiency. It positions the design system as a living, operational layer of the product. The return on investment is not realized simply in creating the tokens, but in their daily, collaborative use as an official, sanctioned vocabulary that eliminates ambiguity during handoff.  

### 1.2. Token Taxonomy: A Layered Architecture

A robust design token system is structured in a layered, hierarchical manner. This taxonomy is a critical best practice that addresses the challenges of scalability and maintainability. The most common model consists of three distinct layers :  

-   **Primitive/Global Tokens:** These tokens represent the foundational, raw values of a design system. They are the building blocks that are not intended for direct application to UI components. Examples from Adobe Spectrum include `gray-100` and `corner-radius-75`. Material Design refers to these as "reference tokens". They provide a single, central repository of raw style options.  
    
-   **Semantic/Alias Tokens:** This layer provides context and meaning by referencing primitive tokens. These tokens describe _how_ a design decision should be used within the UI. For example, a token named `status.brand.background.color` might reference the primitive token `color.purple.100`. Adobe Spectrum recommends using alias tokens whenever possible, as they are a "shared language" that helps associate intent with a token, making a product more resilient to future changes in the design system. Material Design calls these "system tokens," noting that this is where theming occurs.  
    
-   **Component-specific Tokens:** This is the most specific layer, with tokens used exclusively for a particular component. For example, a token might be named `button-primary-bg`. These tokens can reference either semantic or primitive tokens, providing a final layer of specificity for individual components.  
    

The adoption of this layered model is a direct response to a common problem: an unmanaged, flat token structure leads to redundancy and "decision fatigue". When every team uses a different name for the same color (  

`primary-color`, `main-color`, `brand-main`), the system becomes bloated and confusing. The layered model elegantly solves this by providing a stable, semantic API for developers, while allowing designers to update core primitive values without breaking the application logic. The benefits of this architectural approach are tangible. A case study on the Forbes design system demonstrated a 50% reduction in type styles and a 25% reduction in dead code by implementing a primitive and semantic token system. This evidence links a well-governed token architecture directly to improved performance and efficiency.  

## 2\. The Standards and the Ecosystem

### 2.1. The W3C Design Tokens Community Group (DTCG)

The Design Tokens Community Group (DTCG) is the primary body working to standardize a "platform-agnostic" file format for design tokens. The group's work is guided by core principles: being inclusive, focused, and stable. The specification defines the file format as JSON, recommending the  

`.tokens` and `.tokens.json` file extensions.  

The specification mandates a design token object to have a `$value` property, and it outlines optional properties prefixed with a dollar sign (`$`) to avoid naming collisions. These properties include `$description`, `$type` (e.g., `color`, `dimension`), and `$deprecated`. The document also describes "groups" for organizing tokens and "composite types" for closely related style properties, such as a typography style composed of a font name, size, and line height.  

While the DTCG's work is influential, it is crucial to note that the document is a "Draft Community Group Report" and "not a W3C Standard". This creates a unique dynamic. Instead of waiting for a finalized specification, the market has actively adopted and built tools that are "forward-compatible" with the evolving draft. This preemptive adoption demonstrates the spec's undeniable influence but also introduces an element of risk, as different tool creators may implement slightly different interpretations of the standard, potentially leading to future interoperability challenges. This shows that the ecosystem is not passively waiting for a standard to be handed down, but is actively shaping it through real-world implementation.  

### 2.2. The Design-to-Code Pipeline

The power of design tokens is fully realized when a streamlined pipeline connects design to development. This workflow typically follows four steps:

1.  **Creation:** Designers define tokens within a design tool, such as Figma, or using a dedicated plugin like Tokens Studio.  
    
2.  **Synchronization:** The token data is exported, usually as a JSON file, and synced to a central repository like a Git codebase.  
    
3.  **Transformation:** A specialized build system, such as Style Dictionary, consumes the platform-agnostic token data. It then transforms the tokens into platform-specific code artifacts, such as CSS variables for web, XML files for Android, or Swift files for iOS.  
    
4.  **Consumption:** The generated code is consumed directly by developers in their component libraries or applications, ensuring all visual decisions are derived from the same source of truth.  
    

This automated pipeline replaces manual, error-prone processes, providing a scalable and efficient way to manage and update a design system across multiple platforms.  

## 3\. Tool and Integration Analysis

### 3.1. Design Tool Integration: Figma and Beyond

The integration of design tokens into design tools is paramount. Figma has significantly influenced the landscape with its native variable feature, which a recent report noted had a 74% adoption rate among surveyed professionals. This feature allows designers to create and manage tokens for various modes, such as light and dark themes.  

However, the native variables do not provide a complete solution for a mature design system. Tools like Tokens Studio for Figma have emerged to enhance these native capabilities. A review from a design system specialist notes, "Even with Figma's new variables feature, I still prefer using Tokens Studio because it's easier than managing variables in Figma". Tokens Studio provides advanced features that Figma's native variables lack, such as bidirectional synchronization with a Git repository and support for composite token types. This dynamic reveals a common pattern in the design tool ecosystem: the introduction of a new native feature spurs the development of specialized third-party tooling that builds on or provides a better user experience for that feature. This hybrid workflow is a sign of a maturing market, where teams are not waiting for native tools to catch up but are instead building custom solutions to address their needs.  

When integrating with component libraries, the common practice is to centralize styling in a token file. For a React application, this can be done by using a theme provider to make tokens accessible across the component tree, ensuring consistent styling and simplifying updates.  

### 3.2. Core Transformation Engine: Style Dictionary

Style Dictionary, an open-source tool, has become a central component of the design token ecosystem. It is an unopinionated "build-system" that takes design tokens from a single source and exports them to "any platform or language". The tool’s architecture is designed for flexibility and scalability. It performs a deep merge of all token files, resolves references between tokens, and then transforms the values specifically for each platform based on a  

`config.json` file.  

A significant aspect of Style Dictionary's success is its extensibility. The platform allows for the creation of custom parsers, preprocessors, and transforms, enabling it to handle a wide variety of advanced use cases and output formats beyond the standard CSS or mobile files. This architectural decision to be a flexible  

_engine_ rather than a monolithic _platform_ has made it a de facto standard. Its core strength lies in this limited scope; it solves a single, difficult problem exceptionally well. This has led to its adoption as a foundational layer by other projects and commercial products that build on top of its capabilities.  

### 3.3. Commercial Platforms: Automation and Cloud Solutions

Commercial platforms like Supernova and Specify offer an alternative to the manually orchestrated, open-source pipeline. These platforms position themselves as comprehensive, cloud-based solutions that provide a higher level of automation and centralized control. Supernova, for instance, touts itself as a "one source of truth" that automates token imports from Figma or Tokens Studio, manages documentation, and delivers code via a managed pipeline. Specify describes itself as a "Design API" that can automatically detect updates in Figma and update agnostic design token files for consumption by a tool like Style Dictionary.  

The key value proposition of these commercial tools is the automation layer they provide over the open-source ecosystem. The manual work of setting up and maintaining the synchronization and build process, which is necessary with tools like Style Dictionary, is a pain point that these companies commoditize. While Style Dictionary is a powerful generator, it does not handle the syncing of data. Commercial platforms solve this end-to-end orchestration problem, which is particularly appealing to larger, more complex organizations. It should be noted, however, that public metrics on the adoption and growth of these commercial platforms are not readily available from the provided sources, a stark contrast to the transparent, open data on community contributions found in open-source repositories.  

## 4\. Comparative Evaluation and Scoring

The following matrix provides a comparative evaluation of the top design token tools and platforms based on the analysis of available data. The scores are derived from a rubric of 0 to 5, where 5 represents the highest performance.

**Scoring Justification:**

-   **Standards Compliance:** **USWDS**, **Adobe Spectrum**, and **Material Design** score a 5 for their explicit alignment with and promotion of WCAG guidelines in their design tokens and components.  
    
    **Style Dictionary** and **Terrazzo** score highly for their forward-compatibility with the DTCG draft.  
    
-   **Flexibility/Extensibility:** **Style Dictionary** and **Tokens Studio** score a 5 due to their open-source nature, documented extensibility, and the ability to create custom transforms and formats.  
    
-   **Security:** This metric is largely **unknown** for most open-source tools from the provided sources. Style Dictionary's GitHub repository explicitly states, "No security policy detected".  
    
    **USWDS**, **Adobe Spectrum**, and **Material Design** are part of large organizations with assumed security protocols, warranting a higher score, while **Supernova** claims SOC2 Type II certification and SSO support.  
    
-   **Integration:** **Tokens Studio**, **Supernova**, and **Specify** score a 5 for their direct and automated integration with design tools like Figma and their ability to push tokens to development environments.  
    
-   **Documentation and Ergonomics:** **USWDS**, **Adobe Spectrum**, and **Material Design** score a 5 for their comprehensive public-facing documentation and clear usage guidelines.  
    
    **Tokens Studio** also provides a comprehensive learning site and in-plugin documentation features.  
    
-   **Licensing Compatibility:** **Style Dictionary** (Apache-2.0) and **Tokens Studio** (MIT) score a 5 due to their permissive licenses that allow broad use in proprietary projects with minimal restrictions.  
    
    **Supernova** scores lower as a commercial SaaS with a proprietary license, which may have more restrictive terms for commercial use.  
    

## 5\. Licensing and Legal Framework

### 5.1. Open Source Licensing: A Framework for Design Systems

The licensing of open-source design token tools and repositories is a critical due diligence consideration. Open-source licenses generally fall into two categories: permissive and copyleft.  

-   **Permissive Licenses:** These are the most common licenses for design system tools. Examples include the MIT License and the Apache-2.0 License. These licenses grant the recipient broad freedoms to use, modify, and redistribute the software, even for commercial purposes, with minimal requirements, typically just attribution and a disclaimer of liability.  
    
-   **Copyleft Licenses:** These licenses require that any derivative work—a project that incorporates or is built upon the original licensed work—must also be distributed under the same license. This is often described as a "viral" effect because the terms propagate to new codebases. A primary example is the GNU General Public License (GPL).  
    

### 5.2. Table: License and Use Rights Analysis

### 5.3. Analysis of Copyleft Risks and Commercial Use

The legal risk of a copyleft license is significant and extends beyond the realm of traditional software. A key risk, as explained by one source, is that a product developed using a copyleft-licensed component could be considered a "derivative of that copyleft open-source software". If this occurs, the entire product may need to be re-licensed under the same terms, which could result in the loss of control over intellectual property and the ability to charge for the software.  

This risk is particularly nuanced in the context of design tokens, which are data, not code. However, given that a design token repository is intrinsically linked to the build pipeline that generates the final source code, a legal expert would have to determine if the generated code constitutes a "derivative work." This creates a legal gray area and a significant risk for commercial enterprises. Therefore, legal due diligence must not only review the licenses of code dependencies but also the licenses of upstream data sources, such as design token files, to avoid inadvertently adopting a "viral" license.  

## 6\. The Market Landscape and Future Trends

### 6.1. Trends in Adoption and Community Growth

The design token ecosystem is experiencing rapid growth, marked by several key trends. The adoption of Figma's native variables is a significant indicator, with a 74% adoption rate reported in a recent survey. This signals a widespread shift towards incorporating tokenization at the design-tool level. Another trend is the increased importance of engineering involvement in the design token ecosystem. This collaboration ensures that tokens are not just a design asset but a functional part of the development workflow. Community growth is also a strong indicator of a project's health. Open-source projects like USWDS thrive on active communities of engineers and designers, which serve as a source of innovation and provide public, transparent documentation on their contributions.  

### 6.2. Common Gaps and Pain Points

Despite the growing adoption, several common challenges persist:

-   **Governance:** The lack of a clear naming convention can lead to "confusion and duplicate tokens" and slow down decision-making.  
    
-   **Over-engineering:** The creation of too many abstraction layers or redundant tokens can lead to "decision fatigue" for developers and unnecessary code bloat.  
    
-   **Adoption Friction:** Without a formal change management strategy, introducing a new token system can force developers to refactor their entire codebase, leading to resistance and inconsistencies. A thoughtful, small-scale initial implementation is critical to working out process gaps before a full-scale rollout.  
    

### 6.3. Emerging Best Practices and Recommendations

Based on the analysis, several best practices are emerging to address these challenges:

-   **Start Small:** Begin by tokenizing a few key components or a single product to work out the process and demonstrate value.  
    
-   **Collaborate:** Bring designers, developers, and other key stakeholders together early in the process to establish a common language and an implementation plan.  
    
-   **Automate:** Automate the design-to-code pipeline to reduce manual errors, ensure consistency, and streamline the workflow.  
    
-   **Prioritize a Single Source of Truth:** Establish a central repository for the tokens, whether it's a design file or a codebase, to ensure all changes are tracked and propagated from one source.  
    

## 7\. Metrics Collection and Missing Data

The analysis identified several critical, quantitative metrics that demonstrate the value of design tokens in real-world applications:

-   **Dead Code Reduction:** A case study of the Forbes design system found a 25% reduction in dead code by eliminating unnecessary style overrides.  
    
-   **Type Style Reduction:** The same project resulted in a 50% reduction in the number of type styles in the design system.  
    
-   **Development Time Savings:** The USWDS project has helped participating government agencies cut development time by up to 30 percent.  
    
-   **Page Performance:** Improved font usage from a tokenized system led to a Largest Contentful Paint (LCP) time of 1.39 seconds on "slow" mobile connections for Forbes, establishing them as a leader in page speed benchmarks.  
    

It is important to note that certain metrics were unavailable from the provided sources:

-   **Adoption and Growth for Commercial Tools:** Public metrics on active user numbers, revenue growth, or community contributions for commercial tools like Supernova and Specify are unknown.
    
-   **Security for Open-Source Tools:** Style Dictionary's GitHub repository explicitly states, "No security policy detected". While this does not indicate a security vulnerability, it is a critical missing piece of data for enterprise-level due diligence.  
    

## 8\. Inventory of Schema Fields

The following inventory compiles a comprehensive list of design token schema fields, synthesized from the W3C DTCG draft, major design systems like Material Design, and common industry practices.

 

## 9\. Cited Evidence & Search Log

### Search Log

-   “design tokens library comparison”
    
-   “open-source theming engine”
    
-   “design token standards roadmap”
    
-   “token management security”
    
-   “design tokens WCAG”
    
-   “license analysis design-token repo”
    
-   “Figma design token integration”
    
-   “Style Dictionary integration patterns”
    
-   “design tokens component library integration”
    
-   “commercial design token management platforms”
    
-   “W3C Design Tokens Community Group specification”
    
-   “design tokens accessibility WCAG”
    
-   “WCAG 2.2 design tokens”
    
-   “open-source design token frameworks”
    
-   “copyleft risk design tokens”
    
-   “design tokens adoption trends”
    
-   “design system case studies tokens”
    
-   “state of design tokens report”
    
-   “design systems report 2024”
    
-   “best design token tools 2024”
    
-   “design token tool alternatives to Style Dictionary”
    
-   “Style Dictionary license”
    
-   “Style Dictionary GitHub repository license”
    
-   “Tokens Studio GitHub license”
    
-   “Supernova.io license agreement”
    
-   “Supernova pricing plans commercial use”
    
-   “Tokens Studio documentation”
    
-   “Style Dictionary documentation quality”
    
-   “Style Dictionary security features”
    
-   “Supernova design tokens features”
    
-   “Tokens Studio for Figma features”
    
-   “Style Dictionary GitHub stats”
    
-   “Tokens Studio for Figma GitHub stars”
    
-   “Supernova.io public metrics”
    
-   “state of design systems report public data”
    
-   “open source design token CLI”
    
-   “What is the Design Tokens Format Module?”
    
-   “How do design tokens help with WCAG 2.1 compliance?”
    
-   “What is the architecture and core functionality of Style Dictionary?”
    
-   “How to integrate Figma with Tokens Studio and component libraries?”
    
-   “What metrics and best practices were used in this design tokens case study?”
    

### Evidence

-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 4/5, Reputable dev blog.
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design tool help documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 5/5, Primary source (W3C Community Group draft specification).
    
-   :  
    
    Confidence: 5/5, Primary source (W3C Community Group official page).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 5/5, Primary source (W3C official recommendation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 3/5, Dev blog/consulting firm.
    
-   :  
    
    Confidence: 3/5, Dev blog/consulting firm.
    
-   :  
    
    Confidence: 5/5, Primary source (official product website).
    
-   :  
    
    Confidence: 5/5, Primary source (official product documentation).
    
-   :  
    
    Confidence: 3/5, Dev blog/commercial product.
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 4/5, Wikipedia (well-cited legal overview).
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official SPDX website).
    
-   :  
    
    Confidence: 5/5, Primary source (official SPDX website).
    
-   :  
    
    Confidence: 3/5, Commercial product blog.
    
-   :  
    
    Confidence: 4/5, Wikipedia (well-cited legal overview).
    
-   :  
    
    Confidence: 3/5, Dev blog.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing video (summary of a report).
    
-   :  
    
    Confidence: 3/5, Dev blog.
    
-   :  
    
    Confidence: 4/5, Case study by an individual consultant.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page (paywalled report).
    
-   :  
    
    Confidence: 5/5, Primary source (W3C Community Group draft).
    
-   :  
    
    Confidence: 3/5, Dev blog.
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 5/5, Primary source (official design system documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (W3C Community Group draft).
    
-   :  
    
    Confidence: 3/5, Industry report summary (paywalled).
    
-   :  
    
    Confidence: 3/5, Dev blog.
    
-   :  
    
    Confidence: 5/5, Primary source (official product documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (official product website).
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub repository security page).
    
-   :  
    
    Confidence: 3/5, Commercial product blog (AWS).
    
-   :  
    
    Confidence: 5/5, Primary source (official product documentation).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing video (AWS).
    
-   :  
    
    Confidence: 3/5, Dev blog/consultant.
    
-   :  
    
    Confidence: 3/5, Commercial product documentation.
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product blog.
    
-   :  
    
    Confidence: 3/5, Commercial product documentation.
    
-   :  
    
    Confidence: 3/5, Commercial product documentation.
    
-   :  
    
    Confidence: 3/5, Dev blog/consulting firm.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 2/5, Product aggregation site.
    
-   :  
    
    Confidence: 3/5, Dev blog/commercial product.
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub repository).
    
-   :  
    
    Confidence: 4/5, Open source project documentation.
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub repository).
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub documentation).
    
-   :  
    
    Confidence: 5/5, Primary source (commercial terms of service).
    
-   :  
    
    Confidence: 5/5, Primary source (commercial privacy policy).
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 3/5, Commercial product pricing page.
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub repository).
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub organization page).
    
-   :  
    
    Confidence: 5/5, Primary source (W3C Community Group draft).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 4/5, Dev blog/consulting firm.
    
-   :  
    
    Confidence: 5/5, Primary source (official design system website).
    
-   :  
    
    Confidence: 5/5, Primary source (official product website).
    
-   :  
    
    Confidence: 5/5, Primary source (GitHub repository).
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.
    
-   :  
    
    Confidence: 3/5, Commercial product documentation.
    
-   :  
    
    Confidence: 3/5, Commercial product marketing page.