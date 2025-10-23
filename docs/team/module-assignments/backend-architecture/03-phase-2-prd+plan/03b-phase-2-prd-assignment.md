# Backend - Phase 2 Assignment

## Your Mission

Write a complete plan (PRD) for the Backend module that explains exactly how to build a system that stores and shares news articles. Other developers should be able to read your plan and build the system without asking questions.

---

## Before You Start

Make sure you have:

- [ ] Read the overview document (`03a-phase-2-prd-overview.md`)
- [ ] Reviewed your Phase 1 research about databases and web frameworks
- [ ] Understood that AI creates articles, you store them, and others use them

---

## Task 1: Talk to Other Module Owners

**Why**: You need to understand what other modules need from your Backend so you build the right thing.

### Talk to the AI Module Owner
Ask them:

- What information will be in each news article?
- How will they send articles to you?
- What should happen if an article is missing required information?

**Write down their answers** - you'll need them for your plan.

### Talk to the Publishing Module Owner
Ask them:

- How do they want to search for articles? (by date, topic, etc.)
- How many articles do they need at once?
- What information do they need about each article?

**Write down their answers** too.

### Talk to the Frontend Module Owner
Ask them:

- How will users view articles on the website?
- What information should each article show?
- How should website addresses look?

**Save all your notes** - you'll reference them when writing your plan.

---

## Task 2: Plan Your Database

Think of your database like a filing cabinet for articles. You need to decide:

### What to Store for Each Article
Create a simple list like this:
```
Article Information:
- Unique ID (so we can find it later)
- Title (what the article is about)
- Summary (short description)
- Full content (the actual article text)
- Topics (like "technology", "business")
- Date created
- Type (breaking news, analysis, etc.)
- Web address (URL)
```

### Simple Examples
Write examples of what this information looks like:
```
Example Article:
- ID: 12345
- Title: "New Robot Helps Farmers"
- Summary: "A new robot can pick apples faster than humans"
- Content: "Scientists at Stanford University have created..."
- Topics: ["technology", "agriculture"]
- Date: "2025-09-22"
- Type: "feature"
- Web address: "/reports/2025-09-22/robot-helps-farmers"
```

**Make 2-3 examples** with different types of articles.

---

## Task 3: Design Simple Commands (APIs)

Other modules need simple ways to interact with your Backend. Think of these like menu options at a restaurant.

### Commands You Need to Support

#### 1. Save New Article
- **Who uses it**: AI module
- **What it does**: Saves a new article
- **Example**: "Save this article about robots"
- **Response**: "Saved! You can find it at /reports/2025-09-22/robot-news"

#### 2. Get List of Articles
- **Who uses it**: Publishing and Frontend modules
- **What it does**: Returns multiple articles based on filters
- **Example request**: "Give me all technology articles from today"
- **Example response**: List of 5 articles with basic information

#### 3. Get One Specific Article
- **Who uses it**: Frontend module mainly
- **What it does**: Returns all information about one article
- **Example request**: "Give me article 12345"
- **Example response**: Full article with title, content, everything

#### 4. Get Article by Web Address
- **Who uses it**: Anyone clicking links
- **What it does**: Shows article when someone visits the web address
- **Example**: Someone visits `/reports/2025-09-22/robot-news` → Gets the robot article

### Write Simple Examples
For each command, write:

- What someone sends to your Backend
- What your Backend sends back
- What happens if something goes wrong

---

## Task 4: Plan Basic Security

Keep it simple! You just need:

### Two Types of Access
1. **Public Reading**: Anyone can read published articles (no password needed)
2. **Saving Articles**: Only the AI module can save new articles (needs password/token)

### Simple Token System
- Give the AI module a special password (token)
- They include this token when saving articles
- Your Backend checks the token before saving

**Don't overcomplicate this** - just basic password protection for saving, public access for reading.

---

## Task 5: Plan Web Addresses (URLs)

Make addresses that are easy to read and remember.

### Good URL Examples
- `/reports/2025-09-22/robot-helps-farmers`
- `/reports/2025-09-22/openai-funding-news`
- `/reports/2025-09-21/climate-change-update`

### URL Rules
1. Start with `/reports/`
2. Add the date (YYYY-MM-DD)
3. Add a short description (use dashes, not spaces)
4. Keep it under 80 characters
5. Make it readable by humans

### Handle Duplicates
If two articles have similar titles on the same day, add a number:

- `/reports/2025-09-22/tech-news-1`
- `/reports/2025-09-22/tech-news-2`

---

## Task 6: Write Your Complete Plan (PRD)

Now put everything together into one document. Your plan should have these sections:

### Section 1: What This System Does (1 page)
- Explain the Backend in simple terms
- Who uses it and why
- How it fits with other modules

### Section 2: The 5 Main Features (2-3 pages)
- Feature 1: Store articles in database
- Feature 2: Let AI save new articles
- Feature 3: Let others search for articles
- Feature 4: Show individual articles
- Feature 5: Basic security and setup

For each feature, explain:

- What it does
- Who uses it
- How it works
- Example of using it

### Section 3: Database Plan (1-2 pages)
- What information you store
- How you organize it
- Examples of actual data

### Section 4: Commands/APIs (2-3 pages)
- All the commands other modules can use
- Examples of requests and responses
- What happens when things go wrong

### Section 5: Web Addresses (1 page)
- How URLs are created
- Examples of good URLs
- How to handle duplicates

### Section 6: Basic Security (1 page)
- Who can do what
- How the token system works
- What's public vs private

### Section 7: How to Test It Works (1 page)
- Simple ways to verify each feature works
- Example: "Can save an article and get it back"
- Example: "Web address shows the right article"

---

## Quality Checklist

Before submitting, make sure:

- [ ] **Clear Language**: A new developer can understand everything
- [ ] **Specific Examples**: Real examples, not vague descriptions
- [ ] **Complete Coverage**: All 5 features are fully explained
- [ ] **Simple Focus**: No complex features that aren't needed
- [ ] **Working Integration**: Other modules know exactly how to use your system
- [ ] **No Technical Jargon**: Explain things in plain English

---

## Common Mistakes to Avoid

❌ **Too Complicated**: Don't add features beyond the basic 5

❌ **Vague Descriptions**: Instead of "handle data", say "save article in database"

❌ **Missing Examples**: Always show what the actual data looks like

❌ **No Error Handling**: Explain what happens when things go wrong

❌ **Ignoring Other Modules**: Make sure you talked to all module owners

---

## Getting Help

**Stuck on database design?** Ask: "How would I organize articles in a simple filing system?"

**Confused about APIs?** Ask: "What are the simplest commands other modules need?"

**Unclear about security?** Ask: "How do I protect article creation but allow public reading?"

---

## Timeline

**Week 1**:

- Day 1-2: Talk to other module owners
- Day 3-4: Plan database and APIs
- Day 5: Plan security and URLs

**Week 2**:

- Day 1-3: Write complete PRD
- Day 4: Review and get feedback
- Day 5: Final version and submit

---

## Submission

When your PRD is complete:

1. Save it as `deliverables/PRD.md` in your module directory
2. Create a pull request with your changes
3. Ask other module owners to review the parts that affect them
4. Get approval from your team lead

Remember: **Keep it simple and working!** A basic system that works is much better than a complex system that doesn't.
