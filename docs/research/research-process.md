# Research Process Guide

**Purpose**: Learn how to organize, store, and share your technical research  
**Audience**: CS undergraduates working on the Knowledge Graph Lab project  
**Read time**: 15 minutes

---

## Overview

This guide covers the practical aspects of research: what prompts to use with AI tools, how to organize your findings, and how to collaborate using Git.

While the [Research Methodology Guide](./research-methodology.md) teaches you WHAT to research using the SEARCH framework, this guide teaches you HOW to execute that research efficiently using modern tools and workflows.

Think of this as your research cookbook - specific recipes and techniques you can use immediately.

---

## AI Research Tools Available

### Your Research Toolkit

You have access to several powerful AI tools for Week 1 research:

**Primary Research Tool:**
- **Perplexity** (Shared Account) - Your main research tool for comprehensive searches with citations
  - Best for: Finding and comparing platforms, understanding technologies, market research
  - Provides sources and citations for all claims
  - Access details will be provided on Day 1

**Development & Deep Research:**
- **Cursor** (Individual Accounts) - AI-powered IDE that can help with code research
  - Best for: Understanding code implementations, exploring GitHub repos, technical deep dives
  - Can analyze entire codebases and explain complex patterns
  - Especially useful Week 1 for researching how existing tools are built
  - Setup instructions provided during onboarding

**Supplementary Tools (Browser-Based):**
- **ChatGPT** - General research and explanation of concepts
- **Claude** - Detailed technical analysis and code examples
- **Gemini** - Google's AI with access to recent information
- **Grok** - Real-time information from X/Twitter
- **DeepSeek** - Technical and mathematical problem-solving

### How to Use Multiple Tools Effectively

1. **Start with Perplexity** for broad research - it shows sources
2. **Use Cursor** to explore actual code implementations on GitHub
3. **Verify with ChatGPT/Claude** for second opinions on complex topics
4. **Cross-reference** findings across tools for accuracy

---

## Part 1: Effective AI Research Prompts

### Understanding Prompt Engineering

With your toolkit of AI tools, you need clear, specific prompts to get helpful results. A good prompt is like a good Google search - specific enough to get relevant results, broad enough to discover unexpected insights.

### Discovery Prompts

Use these when you're exploring what exists in a domain:

```markdown
"What are the top 5 platforms that creators use for [specific purpose] 
that have launched or significantly updated in the last 6 months? 
For each, include their pricing model and API availability."

Example:
"What are the top 5 platforms that creators use for scheduling social media posts 
that have launched or significantly updated in the last 6 months? 
For each, include their pricing model and API availability."
```

```markdown
"Compare [Platform A] vs [Platform B] vs [Platform C] for [specific use case]. 
Create a table showing features, pricing, API capabilities, and limitations."

Example:
"Compare Buffer vs Hootsuite vs Later for Instagram content scheduling. 
Create a table showing features, pricing, API capabilities, and limitations."
```

```markdown
"Find 3 open-source alternatives to [commercial product] on GitHub. 
For each, include star count, last update, main language, and license type."

Example:
"Find 3 open-source alternatives to Linktree on GitHub. 
For each, include star count, last update, main language, and license type."
```

### Deep Dive Prompts

Use these when you need detailed information about a specific tool or platform:

```markdown
"Analyze [platform]'s API documentation and tell me:
1. Authentication method required
2. Rate limits and quotas  
3. Available endpoints for [specific feature]
4. Data format (JSON/XML/GraphQL)
5. Any costs or approval process
6. Common integration patterns"

Example:
"Analyze Patreon's API documentation and tell me:
1. Authentication method required
2. Rate limits and quotas
3. Available endpoints for creator earnings data
4. Data format (JSON/XML/GraphQL)
5. Any costs or approval process  
6. Common integration patterns"
```

```markdown
"Explain how [technical concept] works in the context of [domain].
Include a simple example with actual code if applicable."

Example:
"Explain how OAuth 2.0 works in the context of YouTube API integration.
Include a simple example with actual code if applicable."
```

### Synthesis Prompts

Use these to combine and analyze multiple pieces of information:

```markdown
"Based on these 3 platforms [A, B, C], identify:
1. Common features all platforms share
2. Unique differentiators for each
3. Technical patterns they all use
4. Gaps none of them address"

Example:
"Based on these 3 platforms [Substack, Ghost, ConvertKit], identify:
1. Common features all platforms share
2. Unique differentiators for each
3. Technical patterns they all use
4. Gaps none of them address"
```

```markdown
"What are the emerging trends in [domain] based on the last 3 months of developments?
Include specific examples and their implications for developers."

Example:
"What are the emerging trends in creator monetization based on the last 3 months of developments?
Include specific examples and their implications for developers."
```

### Technical Evaluation Prompts

Use these to assess feasibility and complexity:

```markdown
"What would be required to build a basic version of [feature] similar to [platform]?
Break down into:
1. Core technical components needed
2. Estimated complexity (1-5 scale)
3. Key libraries or services to use
4. Potential technical challenges
5. Simpler alternatives if any"

Example:
"What would be required to build a basic version of subscriber management similar to Patreon?
Break down into:
1. Core technical components needed
2. Estimated complexity (1-5 scale)
3. Key libraries or services to use
4. Potential technical challenges
5. Simpler alternatives if any"
```

### Prompt Tips

**DO:**
- Be specific about what format you want (table, list, code example)
- Include context about your technical level
- Ask for recent information (specify timeframe)
- Request sources and documentation links

**DON'T:**
- Ask vague questions like "tell me about APIs"
- Assume the AI knows your project context
- Trust outdated information (always verify dates)
- Skip verification of critical technical details

---

## Part 2: Document Storage Structure

### Directory Organization

Your research needs a consistent structure so others can find and understand your work. Here's the required organization:

```
knowledge-graph-lab/
└── research/
    └── week-1/
        └── [yourname]/
            ├── raw-research/
            │   ├── 2025-09-10-platform-comparison.md
            │   ├── 2025-09-10-youtube-api-analysis.md
            │   ├── 2025-09-11-payment-platforms.md
            │   └── 2025-09-11-grant-opportunities.md
            ├── synthesis/
            │   ├── week-1-findings.md
            │   └── technology-recommendations.md
            └── final/
                └── research-brief-[yourname].md
```

### File Naming Convention

Every file follows this pattern: `YYYY-MM-DD-topic-subtopic.md`

**Good examples:**
- `2025-09-10-patreon-api-authentication.md`
- `2025-09-10-creator-platforms-comparison.md`
- `2025-09-11-stripe-integration-complexity.md`

**Bad examples:**
- `notes.md` (no date or topic)
- `api stuff.md` (spaces in filename)
- `research.md` (too vague)

### Raw Research Files

These capture your immediate findings. Don't worry about perfect formatting - focus on capturing information.

Example structure for a raw research file:

```markdown
# YouTube Data API Research
Date: 2025-09-10
Source: https://developers.google.com/youtube/v3

## Key Findings
- Requires Google Cloud Platform account
- 10,000 quota units per day (free tier)
- Each search costs 100 units (= 100 searches/day)

## Authentication
- OAuth 2.0 for user data
- API key for public data only

## Relevant Endpoints
- `/search` - Find videos/channels
- `/videos` - Get video details
- `/channels` - Get channel info

## Limitations Discovered
- No revenue/earnings data available
- Comments API heavily rate-limited
- Real-time data not available

## Code Example Found
[Include any useful code snippets here]

## Questions for Further Research
- How to handle quota limits?
- Alternative APIs for missing data?
```

### Synthesis Documents

After collecting raw research, create synthesis documents that identify patterns and connections.

Example synthesis structure:

```markdown
# Week 1 Platform Analysis Synthesis
Date: 2025-09-14
Author: [yourname]

## Platforms Analyzed
1. YouTube - Video monetization
2. Patreon - Subscription management
3. Stripe - Payment processing
4. Buffer - Content scheduling
5. Linktree - Link aggregation

## Common Technical Patterns
- All use REST APIs with JSON
- OAuth 2.0 is standard for authentication
- Webhook support for real-time updates
- Rate limiting is universal (plan for it)

## Integration Complexity Ranking
1. Stripe (easiest) - Excellent SDK, clear docs
2. Buffer - Good API, some limitations
3. YouTube - Complex auth, quota management
4. Patreon - Approval process required

## Key Technical Decisions
- Use abstraction layer for platform APIs
- Implement caching to handle rate limits
- Design for async processing
```

### Final Research Brief

Your final brief follows the template in `/docs/research-brief-template.md`. This is your polished deliverable that others will use to understand your recommendations.

---

## Part 3: Git Workflow

### Initial Setup

First time only - create your research branch:

```bash
# Make sure you're on main branch with latest changes
git checkout main
git pull origin main

# Create your personal research branch
git checkout -b research/week-1-[yourname]

# Example:
git checkout -b research/week-1-alice
```

### Creating Your Research Directory

Set up your folder structure:

```bash
# Create your personal research directory
mkdir -p research/week-1/[yourname]/raw-research
mkdir -p research/week-1/[yourname]/synthesis  
mkdir -p research/week-1/[yourname]/final

# Example:
mkdir -p research/week-1/alice/raw-research
mkdir -p research/week-1/alice/synthesis
mkdir -p research/week-1/alice/final
```

### Daily Research Workflow

Follow this pattern every day you do research:

```bash
# 1. Start your research session
git checkout research/week-1-[yourname]
git pull origin main  # Get any updates

# 2. Do your research, create files
# ... create your markdown files ...

# 3. Save your work at end of day
git add research/week-1/[yourname]/*
git commit -m "research: [module] - [what you researched]"

# Examples of good commit messages:
git commit -m "research: data-ingestion - analyzed 5 creator platforms"
git commit -m "research: knowledge-graph - evaluated graph databases"
git commit -m "research: frontend - compared React component libraries"

# 4. Push to GitHub
git push origin research/week-1-[yourname]
```

### Commit Message Guidelines

Your commit messages should be informative:

**Good commit messages:**
- `research: data-ingestion - analyzed YouTube and TikTok APIs`
- `research: knowledge-graph - added Neo4j complexity assessment`
- `research: reasoning - investigated AI model options`

**Bad commit messages:**
- `updated stuff`
- `research`
- `fixed`

### Handling Merge Conflicts

If others update main while you're working:

```bash
# Get latest changes
git checkout main
git pull origin main

# Merge into your branch
git checkout research/week-1-[yourname]
git merge main

# If conflicts occur:
# 1. Open conflicted files
# 2. Look for <<<<<<< markers
# 3. Choose which version to keep
# 4. Remove conflict markers
# 5. Save the file

# After resolving conflicts
git add .
git commit -m "merged main branch updates"
git push origin research/week-1-[yourname]
```

### Final Submission

When your research is complete:

```bash
# 1. Ensure everything is committed
git status  # Should show "nothing to commit"

# 2. Push final changes
git push origin research/week-1-[yourname]

# 3. Create Pull Request on GitHub
# Go to: https://github.com/[repo-name]
# Click "Pull requests" → "New pull request"
# Base: main ← Compare: research/week-1-[yourname]
# Title: "Research Week 1: [Your Name] - [Module Name]"
# Description: Summary of your findings and recommendations

# 4. Link to your issue
# In PR description, add: "Closes #[issue-number]"
```

---

## Part 4: Completion Criteria

### How to Know You're Done

Research can feel endless - there's always more to learn. Use these criteria to know when you've done enough.

### Minimum Requirements Checklist

You must have:

- [ ] At least 5 platform/tool evaluations documented
- [ ] At least 3 funding/grant opportunities for creators identified
- [ ] Complexity assessment (1-5 scale) for each technology
- [ ] Time estimates that include AI assistance factors
- [ ] Risk assessment with mitigation strategies for top 3 risks
- [ ] Clear tier classification (Tier 1/2/3) for all features
- [ ] At least 10 raw research files
- [ ] At least 2 synthesis documents
- [ ] 1 complete research brief following the template

### Quality Indicators

Your research is good quality if:

- [ ] Each platform evaluation includes API documentation review
- [ ] Time estimates have clear reasoning and calculations
- [ ] Multiple sources support each major conclusion
- [ ] Conflicting information is noted and resolved
- [ ] All URLs and sources are documented
- [ ] Technical decisions have clear justification
- [ ] Assumptions are explicitly stated
- [ ] Fallback plans exist for risky components

### Coverage Checklist

Your research covers enough ground if:

- [ ] Addresses all focus areas from your module assignment
- [ ] Includes both commercial and open-source options
- [ ] Considers beginner-friendly and advanced approaches
- [ ] Identifies integration points with other modules
- [ ] Documents what's NOT possible or practical

### Evidence Standards

Your research has sufficient evidence if:

- [ ] Every technology choice links to documentation
- [ ] Complexity scores reference specific technical details
- [ ] Time estimates based on actual examples found
- [ ] Risk assessments cite real cases or documentation
- [ ] Claims about "best" or "easiest" have comparisons

### Red Flags That You Need More Research

You're not done if:

- ❌ You only looked at one option for a critical component
- ❌ Your time estimates are all guesses without basis
- ❌ You haven't actually read any API documentation
- ❌ All your sources are blog posts (no official docs)
- ❌ You can't explain WHY you chose each technology
- ❌ You haven't identified any risks or challenges
- ❌ Your recommendations would cost money we don't have

---

## Common Process Mistakes

### Mistake 1: Not Committing Daily

**Problem**: Losing work or creating massive commits  
**Solution**: Commit at the end of each research session, even if incomplete

```bash
# Even incomplete research should be saved
git add .
git commit -m "research: WIP - investigating payment platforms"
```

### Mistake 2: Research Without Recording

**Problem**: "I looked into that yesterday but didn't write it down"  
**Solution**: Always create a markdown file, even for quick searches

```markdown
# Quick Search: Graph Databases
Date: 2025-09-10
Time Spent: 20 minutes

Looked at Neo4j - seems complex, needs Java
Found ArangoDB - multi-model, might be simpler
TODO: Deep dive on both tomorrow
```

### Mistake 3: Perfect vs. Done

**Problem**: Trying to research everything before documenting anything  
**Solution**: Document as you go, refine later

```markdown
# First pass (raw research):
"Stripe looks good for payments, has Python SDK"

# Later refinement (synthesis):
"Stripe provides the best developer experience with 
comprehensive SDK support, handling 92% of edge cases
automatically. Integration time: 2-3 days."
```

### Mistake 4: Working in Wrong Branch

**Problem**: Committing research to main branch  
**Solution**: Always check your branch before committing

```bash
# Always verify where you are
git branch  # Shows current branch with asterisk
* research/week-1-alice  # Good!
  main                   # Not here!
```

---

## Time Management Tips

### Daily Research Schedule

Here's a suggested daily workflow:

```markdown
Morning (2 hours):
- 30 min: Review yesterday's findings
- 90 min: Deep dive on 1-2 specific topics

Afternoon (2 hours):  
- 60 min: Explore new platforms/tools
- 30 min: Document findings
- 30 min: Commit and push changes

End of Day:
- Update synthesis document
- Note questions for tomorrow
- Commit all changes
```

### Research Sprint Pattern

Organize your week for maximum efficiency:

```markdown
Monday-Tuesday: Broad exploration (Scope & Survey)
- Cast wide net
- Identify all options
- Document everything

Wednesday: Deep dives (Evaluate & Estimate)
- Focus on promising options
- Read API docs thoroughly  
- Test critical assumptions

Thursday: Analysis (Risk & Complexity)
- Score all options
- Identify risks
- Create comparisons

Friday: Documentation (Handoff)
- Create synthesis documents
- Write research brief
- Submit pull request
```

---

## Getting Help

### When You're Stuck

If you're struggling with research:

1. **Check existing research**: Others may have investigated similar topics
   ```bash
   ls research/week-1/*/raw-research/
   ```

2. **Ask specific questions** in your team channel:
   - ❌ "How do I research APIs?"
   - ✅ "I'm comparing YouTube and TikTok APIs - which endpoints are most important for analytics?"

3. **Share partial findings** for feedback:
   ```markdown
   "I've found 3 payment platforms but unsure about complexity.
   Here's my analysis so far: [link to file]"
   ```

### Research Resources

**AI Research Tools (Your Accounts)**:
- Perplexity (shared account) - Primary research tool
- Cursor (individual accounts) - Code and GitHub exploration
- Browser-based tools - Supplementary research

**Technical Documentation**:
- Official API docs (always primary source)
- GitHub README files
- Stack Overflow (for common problems)
- Dev.to tutorials (for practical examples)

**Creator Economy Specific**:
- Creator Economy Report 2024
- Platform developer blogs
- IndieHackers discussions
- Product Hunt launches

---

## Final Checklist

Before submitting your research:

### Files and Structure
- [ ] All files follow naming convention
- [ ] Directory structure matches requirements
- [ ] Raw research → Synthesis → Final brief flow

### Git and Collaboration  
- [ ] Working in correct branch
- [ ] Daily commits with clear messages
- [ ] Pull request created and linked to issue

### Content Completeness
- [ ] Minimum requirements met
- [ ] Quality indicators satisfied
- [ ] All module focus areas covered

### Documentation Quality
- [ ] Sources and URLs included
- [ ] Technical decisions explained
- [ ] Assumptions stated clearly
- [ ] Someone else could implement from your research

---

*Remember: Good research is thorough but not perfect. Focus on gathering enough information to make informed decisions, not on researching every possible option. Your time is limited - use it wisely.*