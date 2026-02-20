# CEO Source of Truth: Knowledge Graph Lab Alpha

**Date:** 2026-02-19
**Status:** Living Document

## 1. The Core Duality: The Factory vs. The Product
The biggest point of confusion in KGL Alpha is conflating **The Product** with **The Factory** used to build it. They are strictly separate.

### A. The Product (Developer Streams)
This is what the end-user will actually use.
*   **Knowledge Graph Lab (KGL) Module:** The actual web application (React frontend, search infrastructure, node graph visualization, AI querying module).
*   **The Backend Pipeline:** The actual backend APIs, databases, authentication, and security patches (e.g., Auth Bypass fixes). 
*   *If you are writing code for the product, you are in the Developer Stream.*

### B. The AI Factory (Architect Kits / Kit Pipeline)
This is the automated "Meta-Layer" used to research, design, and specify the Product. The goal is to feed a vague concept into the front and get a pixel-perfect, implementation-ready PRD and Design Spec out the back.
*   **Discovery Kit:** Analyzes a concept and outputs architectural patterns and research.
*   **Requirements Kit:** Takes Discovery output and turns it into hard functional/non-functional requirements.
*   **Spec Kit:** Takes Requirements and builds technical PRDs and data schemas.
*   **Design Kit:** Takes Specs and generates UX/UI mockups, layouts, and component definitions.
*   *If you are fixing how these kits talk to each other, you are in the Architect Stream.*

---

## 2. The Modular Design Generator ("The Recipe System")
A massive breakthrough in the Design Kit was the **Reverse Generation Engine** (`generate-valid-designs.py`).

Instead of having AI hallucinate a design from scratch, the system uses a **Modular Combinatorial Approach (Design Recipes)**:
1.  **Atoms & Dimensions:** It breaks UX down into vectors: Layout (Grid, Split, Single), Navigation (Tabs, Modal, Wizard), Density, Emphasis, and Interaction.
2.  **Combinations:** It systematically generates thousands of possible distinct "recipes" for a screen.
3.  **Constraints:** It runs them through 28 hard constraints (e.g., "Grid Layout + Mobile = Fail", "Compact + Touch Targets = Fail") and 14 soft constraints.
4.  **Pareto Optimality:** It spits out 10 to 15 completely unique, mathematically valid, structurally sound design recipes that agents or human designers can immediately implement. 
*This means the AI is doing generative mix-and-match structural design based on rules, not just guessing pixels.*

---

## 3. The Grand Goal: The Seamless Pipeline
Right now, the individual machines in The Factory work perfectly in isolation, but the conveyer belts connecting them are broken. 

**The Pipeline Reality:**
*   **Discovery Kit** works in 30 seconds... but outputs a Markdown text file.
*   **Requirements Kit** works in 2 minutes... but expects a structured JSON file as input. 
*   Because of this, a human has to sit between the bots and manually translate Markdown into JSON for 45 minutes every time we want to run the pipeline.

**The Urgent Execution Path:**
We are stopping all feature work on the Product (Developer Streams) until The Factory (Architect Streams) is fully automated. 
1.  **Fix Discovery Validation:** Force the Discovery kit to output strictly structured JSON.
2.  **Fix Requirements Integration:** Auto-feed the Discovery JSON into the Requirements Kit.
3.  **Run the Complete System:** Push a concept through Discovery -> Requirements -> Spec -> Modular Design Generator *with zero human intervention*.
