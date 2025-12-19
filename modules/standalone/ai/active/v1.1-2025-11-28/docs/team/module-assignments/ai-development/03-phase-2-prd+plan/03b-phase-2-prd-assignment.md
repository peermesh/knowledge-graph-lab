# AI Development - Phase 2 Assignment

## Your Mission

Write a complete plan for the AI module that explains exactly how to build a system that creates high-quality news articles. Other developers should be able to read your plan and build the AI system without asking questions.

---

## Before You Start

Make sure you have:
- [ ] Read the overview document (`03a-phase-2-prd-overview.md`)
- [ ] Reviewed your Phase 1 research about AI tools and APIs
- [ ] Understood that you create complete articles, NOT emails

---

## Task 1: Talk to the Backend Module Owner

**Why**: You need to understand exactly how to send articles to the Backend so they can be stored properly.

### Key Questions to Ask
- What format should articles be in when you send them?
- What information is required for each article?
- How do you send articles to the Backend system?
- What should happen if sending an article fails?
- How do you avoid creating duplicate articles?

### Information You Need
- The exact web address (URL) to send articles to
- What security token or password you need
- Examples of correctly formatted articles
- Error handling procedures

**Write down all their answers** - you'll need them for your plan.

---

## Task 2: Define Your Article Format

You need to decide exactly what information goes in each article.

### Required Article Information
Create a simple template like this:
```
Every Article Must Have:
- Unique ID (so we can track it)
- Headline (clear, attention-grabbing title)
- Summary (2-3 sentence overview)
- Full Content (complete article text, several paragraphs)
- Topics (like "technology", "business")
- Article Type (breaking news, analysis, feature, roundup)
- Date Created
- People/Companies Mentioned
- Quality Score (how confident the AI is)
```

### Article Examples
Write 3 different example articles:

**Example 1: Breaking News**
```
Headline: "Tesla Announces New Electric Truck"
Summary: "Tesla revealed its new electric truck design today, promising 500-mile range and competitive pricing for commercial use."
Content: "Tesla CEO Elon Musk took the stage today in Austin, Texas, to unveil the company's latest electric vehicle..."
Topics: ["technology", "automotive", "business"]
Type: "breaking_news"
People: ["Elon Musk"]
Companies: ["Tesla"]
Quality Score: 0.9
```

**Example 2: Feature Article**
```
Headline: "The Rise of Remote Work in Tech Companies"
Summary: "Technology companies are embracing permanent remote work policies, changing how teams collaborate and hire talent."
Content: "The traditional office cubicle may soon become a relic of the past..."
Topics: ["technology", "workplace", "trends"]
Type: "feature"
Quality Score: 0.85
```

**Example 3: Analysis**
```
Headline: "Why Electric Vehicle Sales Are Growing"
Summary: "Electric vehicle sales increased 60% this year due to better battery technology, government incentives, and changing consumer preferences."
Content: "Electric vehicles are no longer a niche market..."
Topics: ["automotive", "environment", "market-analysis"]
Type: "analysis"
Quality Score: 0.88
```

---

## Task 3: Plan Your Article Writing Process

Break down how the AI will create articles step by step.

### Step 1: Understand the Input
- What types of information will you receive? (press releases, news articles, data feeds)
- How will you identify the most important facts?
- What makes something worth writing about?

### Step 2: Create the Article Structure
- How will you write attention-grabbing headlines?
- How will you create clear, informative summaries?
- How will you organize the full article content?

### Step 3: Add Tags and Metadata
- How will you identify relevant topics?
- How will you classify article types?
- How will you extract people and company names?

### Step 4: Quality Control
- How will you check if articles make sense?
- What makes a "high quality" vs "low quality" article?
- How will you handle articles that don't meet standards?

**Write out each step clearly** with simple examples.

---

## Task 4: Design Quality Checking

Your AI needs to make sure articles are good before sending them.

### Basic Quality Rules
```
A Good Article Must:
- Have a headline between 5-15 words
- Have a summary between 20-100 words
- Have main content of at least 200 words
- Mention at least 1 specific fact or number
- Be written in clear, simple English
- Not contain obvious errors or nonsense
```

### Quality Checking Process
1. **Check Required Parts**: Does the article have all required sections?
2. **Check Length**: Are headline, summary, and content the right length?
3. **Check Facts**: Does the content make logical sense?
4. **Check Language**: Is it written clearly and professionally?
5. **Assign Score**: Give the article a quality score from 0-1

### What to Do with Low Quality Articles
- Articles scoring below 0.7: Try rewriting them
- Articles that can't be improved: Mark as "failed" and don't send
- Keep track of how many articles fail for improvement

---

## Task 5: Plan Connection to Backend

Figure out exactly how to send finished articles to the Backend storage.

### Sending Process
1. **Format the Article**: Put all information in the exact format Backend expects
2. **Add Required Headers**: Include any security tokens or identifiers
3. **Send the Article**: Use the Backend's web address to send the article
4. **Check Response**: Make sure Backend received and accepted the article
5. **Handle Errors**: What to do if sending fails

### Error Handling
- **Connection Failed**: Try sending again up to 3 times
- **Article Rejected**: Log the error and don't try again
- **Timeout**: Wait and try again later
- **Duplicate Article**: Check if article already exists before sending

### Simple Example
```
1. AI finishes writing an article about robots
2. AI formats article in Backend's required format
3. AI sends article to Backend at: POST /api/v1/reports
4. Backend responds: "Success! Article saved at /reports/2025-09-22/robot-news"
5. AI logs the success and moves to next article
```

---

## Task 6: Plan Different Article Types

You need to handle different types of articles appropriately.

### Breaking News Articles
- **When to use**: Major announcements, urgent developments
- **Writing style**: Direct, factual, immediate
- **Length**: Shorter (200-400 words)
- **Example topics**: Company announcements, market changes, new technology launches

### Feature Articles
- **When to use**: In-depth topics, explanatory content
- **Writing style**: Detailed, informative, engaging
- **Length**: Longer (400-800 words)
- **Example topics**: Trend analysis, how-to guides, background stories

### Analysis Articles
- **When to use**: Interpreting data, explaining significance
- **Writing style**: Thoughtful, analytical, balanced
- **Length**: Medium (300-600 words)
- **Example topics**: Market analysis, technology impact, industry changes

### Roundup Articles
- **When to use**: Summarizing multiple related events
- **Writing style**: Organized, comprehensive, clear
- **Length**: Medium (300-500 words)
- **Example topics**: Weekly summaries, multiple product launches

---

## Task 7: Write Your Complete Plan (PRD)

Put everything together into one comprehensive document:

### Section 1: What This System Does (1 page)
- Explain the AI module in simple terms
- Who uses it and why
- How it fits with other modules

### Section 2: The 6 Main Features (3-4 pages)
- Feature 1: Read and understand information
- Feature 2: Create complete news articles
- Feature 3: Add important information (tags, metadata)
- Feature 4: Quality checking
- Feature 5: Send to Backend storage
- Feature 6: Simple admin tools

For each feature, explain:
- What it does
- How it works
- Examples of using it
- What happens when something goes wrong

### Section 3: Article Format (1-2 pages)
- Exact format for all article information
- Examples of each article type
- Quality requirements for articles

### Section 4: AI Writing Process (2-3 pages)
- Step-by-step process for creating articles
- How to handle different input types
- Quality control procedures

### Section 5: Backend Integration (1-2 pages)
- How to send articles to Backend
- Required format and security
- Error handling procedures

### Section 6: Testing and Quality (1 page)
- How to test that the AI works correctly
- Examples of good vs bad articles
- Quality measurement methods

---

## Quality Checklist

Before submitting, make sure:

- [ ] **Clear Language**: A new developer can understand everything
- [ ] **Specific Examples**: Real examples of articles and processes
- [ ] **Complete Process**: Every step from input to Backend is explained
- [ ] **Error Handling**: What happens when things go wrong
- [ ] **Quality Focus**: How to ensure articles are well-written
- [ ] **No Email Content**: Focus on news articles, not email formatting

---

## Common Mistakes to Avoid

❌ **Mixing Up Outputs**: Don't confuse news articles with email content
❌ **Too Complex**: Don't plan overly sophisticated AI features
❌ **Vague Process**: Be specific about each step in article creation
❌ **Missing Quality Control**: Always plan how to check article quality
❌ **Ignoring Backend**: Make sure you understand how to send articles

---

## Getting Help

**Confused about article types?** Look at real news websites for examples

**Unclear about AI prompts?** Ask: "How would I tell someone to write a good news article?"

**Backend integration problems?** Talk to the Backend module owner

---

## Timeline

**Week 1**:
- Day 1-2: Talk to Backend owner, study article examples
- Day 3-4: Plan article format and writing process
- Day 5: Plan quality control and error handling

**Week 2**:
- Day 1-3: Write complete PRD
- Day 4: Review and test with example articles
- Day 5: Final version and submit

---

## Submission

When your PRD is complete:
1. Save it as `deliverables/PRD.md` in your module directory
2. Create a pull request with your changes
3. Ask the Backend module owner to review the integration parts
4. Get approval from your team lead

Remember: **Focus on creating complete, high-quality news articles!** The better your articles, the better the entire system works.