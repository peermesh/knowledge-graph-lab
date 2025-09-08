# Documentation Style Guide

**Purpose**: Unified standards for all Knowledge Graph Lab documentation
**Target Audience**: Computer Science interns with limited professional experience, project leads, and external reviewers
**Application**: All documentation created by humans or AI agents must follow these standards

---

## Core Writing Philosophy

**"Write as if the reader is smart but has never built production software before."**

Every document we create must be self-contained and self-explanatory. Readers should never need to ask "What does this mean?" or "Why are we doing this?" or "How does this connect to everything else?" The documentation should anticipate questions and answer them proactively.

## Target Reading Level

Our documentation targets Computer Science undergraduate students in their junior or senior year. They understand programming concepts, data structures, and algorithms, but may not have experience with:
- Production system architecture
- Professional development workflows
- Real-world API design
- Knowledge graphs and entity resolution
- AI/ML integration patterns
- Microservices and distributed systems

## Writing Standards

### Clarity Over Brevity
Never sacrifice understanding for conciseness. It's better to use three clear sentences than one dense, jargon-filled sentence. Every technical term must be explained on first use, even if it seems obvious.

**Bad Example**: "The KGL implements a morphing ontology with neuro-symbolic reasoning."

**Good Example**: "Knowledge Graph Lab uses an evolving data structure (ontology) that can adapt as it learns new information. It combines neural network pattern recognition with symbolic logic rules to make intelligent decisions about the data it processes."

### Progressive Disclosure
Start with the simple concept, then add complexity. Each section should build on the previous one. Never introduce advanced concepts before establishing the foundation.

### Concrete Examples
Abstract concepts must always be followed by concrete examples. When describing a system capability, show what it looks like in practice with real data.

**Pattern**: Concept → Explanation → Example → Impact

### Complete Thoughts
Every paragraph should be complete and coherent on its own. Avoid forward references ("as we'll see later") or undefined concepts. If you must reference something not yet explained, provide a brief inline explanation.

## Formatting Standards

### Document Structure
```markdown
# Main Title (Only one per document)

Brief introduction paragraph that explains what this document covers and why it matters.

## Major Section (Core concept or component)

Introduction paragraph for the section explaining what will be covered.

### Subsection (Specific aspect of the major section)

Content paragraphs with 3-4 sentences each. Each paragraph makes one clear point.

Never go deeper than three heading levels. If you need more hierarchy, restructure the content.
```

### Paragraph Guidelines
- **Length**: 3-4 sentences that form a complete thought
- **Opening**: Topic sentence that states the main point
- **Body**: Supporting details or explanation
- **Connection**: How this relates to the broader context

### Technical Content
- **Code blocks**: Always include language identifier and brief comment explaining purpose
- **Data examples**: Use realistic data, not "foo" and "bar"
- **API examples**: Include both request and response with actual values
- **Configuration**: Show complete examples with all required fields

### Visual Markers
- **Diagram placeholders**: Clear `<!-- DIAGRAM NOTE: Description -->` comments
- **Important concepts**: Bold on first use only
- **Emphasis**: Use italics sparingly for subtle emphasis
- **Lists**: Use bullets for unordered items, numbers only for sequential steps

## Language Guidelines

### Active Voice
Write in active voice to make responsibility and action clear.

**Passive**: "Data is ingested by Module 1"
**Active**: "Module 1 ingests data"

### Present Tense
Describe the system as it will exist, not in conditional future tense.

**Conditional**: "The system would process requests"
**Present**: "The system processes requests"

### Plain English
Replace technical jargon with clear explanations. When technical terms are necessary, define them immediately.

**Jargon**: "Implement pub-sub for loose coupling"
**Clear**: "Modules communicate by publishing messages that other modules can subscribe to, which means they don't need to know about each other directly"

### Positive Framing
Explain what the system does, not what it doesn't do.

**Negative**: "The system doesn't require manual updates"
**Positive**: "The system updates automatically"

## Explanation Framework

For every major concept or component, follow this structure:

1. **What**: Define the concept in one clear sentence
2. **Why**: Explain why this matters to the project
3. **How**: Describe how it works in practice
4. **Example**: Provide a concrete instance
5. **Connection**: Relate it to other parts of the system

## Specific Guidelines for Each Document Type

### Vision Documents (project-vision.md)
- Start with relatable problems using storytelling
- Use analogies to familiar systems
- Avoid technical implementation details
- Focus on impact and outcomes
- Include real-world scenarios

### Overview Documents (project-overview.md)
- Balance technical accuracy with accessibility
- Use system diagrams and flow charts
- Define all components before discussing interactions
- Include user perspectives throughout
- Provide clear boundaries of what's included/excluded

### Architecture Documents (project-architecture.md)
- Progress from high-level to detailed
- Justify every technical decision
- Include alternative approaches considered
- Provide troubleshooting guidance
- Link implementation to requirements

### Technical Specifications (API, Data Model)
- Complete examples for every concept
- Include error cases and edge conditions
- Provide test commands or queries
- Show progression from simple to complex
- Include integration patterns

## Quality Checklist

Before considering any document complete, verify:

### Content Quality
- [ ] No undefined technical terms
- [ ] No forward references without explanation
- [ ] Every concept has an example
- [ ] All examples use realistic data
- [ ] Clear connection between sections

### Readability
- [ ] Paragraphs are 3-4 sentences
- [ ] No more than 3 heading levels
- [ ] Active voice throughout
- [ ] Present tense for system descriptions
- [ ] Plain English with technical terms defined

### Completeness
- [ ] Document answers its stated purpose
- [ ] No "TODO" or "TBD" markers
- [ ] All sections have introduction paragraphs
- [ ] Cross-references are accurate
- [ ] Diagram placeholders are descriptive

### Consistency
- [ ] Terminology matches across all documents
- [ ] Formatting follows the style guide
- [ ] Examples build on each other
- [ ] Technical depth is appropriate for audience
- [ ] Voice and tone are uniform

## Common Pitfalls to Avoid

### The Curse of Knowledge
Don't assume readers know what you know. What seems obvious to you may be completely new to them. Always err on the side of over-explaining rather than under-explaining.

### The Jargon Trap
Technical terms are shortcuts for experts but barriers for learners. Always define terms on first use and consider whether a simpler word would work better.

### The Forward Reference
Avoid "as we'll see later" or "this will make sense soon." Each section should be comprehensible on its own.

### The Abstract Example
Don't use variables like "X" and "Y" or entities like "foo" and "bar." Use concrete, realistic examples that readers can relate to.

### The Dense Paragraph
If a paragraph tries to make more than one point, split it. If a sentence needs multiple commas and subclauses, rewrite it as two sentences.

## Writing Process

1. **Outline First**: Structure the document before writing
2. **Write Clearly**: Focus on understanding, not impressiveness
3. **Add Examples**: Every concept needs concrete illustration
4. **Review for Jargon**: Replace or define technical terms
5. **Check Connections**: Ensure smooth flow between sections
6. **Verify Completeness**: Use the quality checklist
7. **Read as a Beginner**: Approach with fresh eyes

---

*This style guide ensures consistency, clarity, and quality across all Knowledge Graph Lab documentation. All contributors, whether human or AI, must follow these standards.*