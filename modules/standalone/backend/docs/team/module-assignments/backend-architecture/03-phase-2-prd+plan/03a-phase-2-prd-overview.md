# Backend - Phase 2 Overview

## What You're Building

You're building the **storage system** for the Knowledge Graph Lab. Think of it like a smart filing cabinet that stores news articles and lets other parts of the system find and read them.

## How It Works (Simple Version)

1. **AI creates news articles** → Sends them to your Backend
2. **Your Backend saves them** → Stores in database with a web address
3. **Other modules ask for articles** → Your Backend finds and sends them back

Your job is to build the "middle person" that safely stores and shares the news articles.

---

## What You'll Create in Phase 2

By the end of Phase 2, you'll have written a complete plan (called a PRD) that explains:

### 1. Database Plan
- How to store news articles in a database
- What information to save (title, content, date, etc.)
- Simple ways to find articles later

### 2. Website Addresses (URLs)
- Give each article its own web address
- Make addresses that are easy to read
- Example: `/reports/2025-09-22/openai-funding-news`

### 3. Ways for Others to Get Data
- Simple commands other modules can use
- "Get all articles from today"
- "Get this specific article"
- "Save this new article"

### 4. Security
- Make sure only the right modules can save articles
- Anyone can read published articles
- Keep the system safe from bad requests

### 5. Basic Performance
- Make sure the system responds quickly
- Handle multiple requests at the same time

---

## Your 5 Main Features

These are the only things you need to build for Phase 2:

### Feature 1: Store News Articles
- Save articles with all their information
- Give each one a unique ID and web address
- Store: title, summary, full content, topics, date created

### Feature 2: Let Others Save Articles
- The AI module sends you new articles
- Check that articles have required information
- Save them and return the web address

### Feature 3: Let Others Find Articles
- Other modules ask for lists of articles
- Filter by date, topic, or type
- Return articles in a useful format

### Feature 4: Show Individual Articles
- When someone wants one specific article
- Find it by ID or web address
- Return all the article information

### Feature 5: Basic Security & Setup
- Simple password system for saving articles
- Public reading of published articles
- Works in Docker (runs anywhere)

---

## How Your Module Connects to Others

### AI Module → Your Backend
- **What they send you**: New news articles
- **What you do**: Save the article, give back a web address
- **Example**: AI says "Save this article about robots" → You save it and say "Done! It's at /reports/2025-09-22/robot-news"

### Your Backend → Publishing Module
- **What they ask for**: Lists of articles to put in emails
- **What you do**: Find articles matching their request
- **Example**: Publishing says "Give me today's tech articles" → You send back 5 tech articles from today

### Your Backend → Frontend Module
- **What they ask for**: Articles to show on the website
- **What you do**: Send article information for web pages
- **Example**: Frontend says "Show article 123" → You send back the full article

---

## What Makes This Simple (MVP Focus)

**You DON'T need to worry about:**
- Advanced search features
- Complex analytics
- Multiple servers
- Advanced security features
- Real-time updates

**You DO need to focus on:**
- Storing and finding articles reliably
- Simple web commands that work
- Basic security (passwords)
- Clear documentation other developers can follow

---

## Technology You'll Use

Based on your Phase 1 research:
- **Database**: PostgreSQL (stores the articles)
- **Programming**: Python with FastAPI (handles requests)
- **Containers**: Docker (makes it easy to run anywhere)
- **Security**: Simple token-based authentication

---

## Success Checklist

Your Phase 2 is successful when:

- [ ] You can explain your module in simple terms
- [ ] All 5 features are clearly documented
- [ ] Other module owners understand how to use your system
- [ ] Your plan has specific examples (not vague descriptions)
- [ ] Everything can be built in 1-2 weeks

---

## Next Steps

1. Read your assignment document (`03b-phase-2-prd-assignment.md`)
2. Talk to other module owners about what they need
3. Start writing your detailed plan
4. Get feedback from your team

Remember: Keep it simple! A working basic system is better than a complex system that doesn't work.