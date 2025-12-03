# AI Development - Phase 2 Overview

## What You're Building

You're building the **smart writer** for the Knowledge Graph Lab. Think of it like a robot journalist that reads information and writes complete news articles about it.

## How It Works (Simple Version)

1. **You give the AI information** → Articles, documents, data feeds
2. **AI reads and understands it** → Finds important facts and events
3. **AI writes complete news articles** → Full articles with titles, summaries, and content
4. **AI sends articles to Backend** → Backend saves them with web addresses

Your job is to build the "smart writer" that creates complete, standalone news articles.

---

## Important: What You Create

**You create COMPLETE NEWS ARTICLES, not emails!**

- ✅ **What you make**: Full news articles (like newspaper articles)
- ❌ **What you DON'T make**: Email newsletters or email content

The Publishing module will take your articles and put them into emails later. You just focus on making great news articles.

---

## What You'll Create in Phase 2

By the end of Phase 2, you'll have written a complete plan that explains:

### 1. Article Writing System
- How AI reads input information
- How it decides what's important
- How it writes complete articles

### 2. Article Format
- What information goes in each article
- How articles are structured (title, summary, content)
- Examples of what finished articles look like

### 3. Quality Control
- How to make sure articles are good quality
- What to do if the AI writes something wrong
- How to check articles before sending them

### 4. Connection to Backend
- How to send finished articles to the storage system
- What happens if sending fails
- How to avoid creating duplicate articles

### 5. Article Types
- Different kinds of articles (breaking news, analysis, features)
- How to decide which type to write
- Examples of each type

---

## Your 6 Main Features

These are the only things you need to build for Phase 2:

### Feature 1: Read and Understand Information
- Take in text documents, articles, or data feeds
- Find the most important facts and events
- Understand what's worth writing about

### Feature 2: Create Complete News Articles
- Write a clear headline that grabs attention
- Write a short summary (2-3 sentences)
- Write the full article content (several paragraphs)

### Feature 3: Add Important Information
- Tag articles with topics (technology, business, etc.)
- Mark article type (breaking news, analysis, feature)
- Add relevant people, companies, or places mentioned

### Feature 4: Quality Checking
- Make sure articles have all required parts
- Check that content makes sense
- Verify important facts when possible

### Feature 5: Send to Backend Storage
- Format articles correctly for the Backend
- Send articles with all required information
- Handle errors if sending fails

### Feature 6: Simple Admin Tools
- Basic interface to test article creation
- View articles before they're sent
- Simple controls to adjust writing style

---

## How Your Module Connects to Others

### Input Sources → Your AI
- **What you receive**: Text documents, articles, data feeds
- **What you do**: Read and understand the important information
- **Example**: You get a press release about new technology → You understand the key facts

### Your AI → Backend Module
- **What you send**: Complete news articles
- **What they do**: Save your articles and give them web addresses
- **Example**: You send "New Robot Helps Farmers" article → Backend saves it at `/reports/2025-09-22/robot-helps-farmers`

### Your AI → Publishing Module (Indirect)
- **How it works**: Publishing gets your articles from Backend, not directly from you
- **What they do**: Take your articles and put them into email newsletters
- **Example**: Publishing takes 5 of your articles and creates a daily email newsletter

---

## What Makes This Simple (MVP Focus)

**You DON'T need to worry about:**

- Advanced machine learning models
- Complex natural language processing
- Real-time article generation
- Email formatting or sending
- Advanced analytics or feedback loops

**You DO need to focus on:**

- Creating complete, readable articles
- Consistent article format and quality
- Reliable connection to Backend storage
- Simple, clear article writing process

---

## Technology You'll Use

Based on your Phase 1 research:
- **AI Service**: OpenAI API or similar (for writing articles)
- **Programming**: Python with simple libraries
- **Storage**: Send articles to Backend (PostgreSQL)
- **Containers**: Docker (makes it easy to run anywhere)

---

## Article Examples

### Example: Breaking News Article
```
Title: "OpenAI Announces Major Funding Round"
Summary: "OpenAI raises $10 billion in new funding led by Microsoft and other investors to expand AI research and development."
Content: "OpenAI, the artificial intelligence research company, announced today that it has secured $10 billion in new funding... [several more paragraphs]"
Topics: ["technology", "business", "artificial-intelligence"]
Type: "breaking_news"
```

### Example: Feature Article
```
Title: "How AI is Changing Modern Farming"
Summary: "New artificial intelligence tools are helping farmers increase crop yields and reduce waste through precise monitoring and predictions."
Content: "In the rolling hills of Iowa, farmer John Smith is using artificial intelligence to revolutionize how he grows corn... [several more paragraphs]"
Topics: ["technology", "agriculture", "innovation"]
Type: "feature"
```

---

## Success Checklist

Your Phase 2 is successful when:

- [ ] You can explain your AI system in simple terms
- [ ] All 6 features are clearly documented
- [ ] You have examples of different article types
- [ ] Backend module owner understands how to receive your articles
- [ ] Your plan shows how to build a working system in 1-2 weeks

---

## Next Steps

1. Read your assignment document (`03b-phase-2-prd-assignment.md`)
2. Talk to the Backend module owner about article format
3. Look at real news articles for examples
4. Start planning your article writing process

Remember: Focus on creating complete, standalone news articles that are easy to read and understand!
