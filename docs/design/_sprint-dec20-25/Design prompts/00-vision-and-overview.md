# Knowledge Graph Lab - Interface Vision & Overview

## What We're Building

Knowledge Graph Lab is a consumer research automation platform. Users tell it what they want to stay informed about, and it continuously researches, organizes findings, and delivers insights through their preferred channels.

Think of it as a personalized research assistant that works in the background.

## Core User Experience

**The key insight:** Users want to "follow" topics like they follow people on social media, but get intelligent synthesis instead of noise.

The interface should feel like a living research magazine that evolves with the user's interests. Not a database. Not a dashboard full of charts. A calm, intelligent companion for staying informed.

## Three Primary Modes

The entire interface operates in three modes. Navigation adapts to show only what's relevant to the current mode.

### 1. Discover Mode
A feed of findings from the user's research streams. Cards with simple graphics and short headlines. Tappable, scannable, low cognitive load.

Periodically surfaces suggestions: "Based on your interest in X, you might also want to track Y." User taps to add, ignores to skip.

### 2. Organize Mode
Hierarchical domain management. Top-level research domains containing ideas, sub-ideas, infinitely nestable. Like a file browser for research interests.

Users can:
- Add/remove domains
- Nest ideas under domains or other ideas
- Promote sub-sections to their own domains
- Collapse/expand to manage complexity

### 3. Publish Mode
Review queue for pending publications. Simple card interface with approve/skip actions.

Publishing destinations include:
- First-party: email, phone notifications, web dashboard
- Third-party: social platforms where APIs allow

Two trust levels per stream:
- Auto-publish (goes out automatically)
- Review first (sits in pending queue)

## Navigation Structure

**Desktop:** Left rail with 3 mode icons, content area adapts to mode
**Mobile:** Bottom tab bar with 3 icons, single column layout

Minimal fixed elements. The canvas reshapes based on context.

## Design Principles

- Contextual UI that shows only what's needed for the current task
- Clean, calm aesthetic (not busy dashboards)
- Mobile-first responsive design
- Smooth transitions between modes
- Progressive disclosure of complexity

## What This Prototype Is NOT

- Not connected to real backend services
- Not implementing actual AI/LLM features
- Not handling real authentication (mock it)
- Not processing real data (use fixtures)

The goal is proving out the interaction patterns and visual design before backend development.
