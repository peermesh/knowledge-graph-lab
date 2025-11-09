Key Findings for Your Use Case
The best solution is D3.js with force simulation - it gives you exactly the "surface tension" physics you described. Here's why:

Best Live Demos to Try Right Now:
D3 Clustered Bubbles - https://observablehq.com/@d3/clustered-bubbles

Bubbles attract each other and cluster naturally

Collision detection prevents overlap

You can edit the code right in your browser!

D3 Zoomable Circle Packing - https://observablehq.com/@d3/zoomable-circle-packing

Click bubbles to zoom and expand

Smooth transitions

Auto-scales to fit viewport

Circle Packing with D3-Force - https://www.react-graph-gallery.com/example/circle-packing-with-d3-force

Uses forceCollide() for surface tension boundaries

forceManyBody() attracts bubbles together

forceY(0) aligns them horizontally like soap bubbles

Video Tutorials (Watch These!):
Making an Interactive Bubble Chart (11 min) - https://www.youtube.com/watch?v=lPr60pexvEM

Shows exactly how to make clickable bubbles

Explains force simulation step-by-step

Interactive Clustering (15 min) - https://www.youtube.com/watch?v=NTS7uXOxQeM

Shows how to reorganize bubbles on click

Demonstrates the collision forces

The "Surface Tension" Physics Code:
The key is combining multiple D3 forces:

forceCollide() - prevents overlap (like surface tension boundary)

forceManyBody() with positive strength - attracts bubbles together

forceCenter() - gentle pull toward center

forceX() and forceY() - creates alignment (like soap settling)

Why Not React Flow or Others?
I included React Flow (https://play.reactflow.dev) as an alternative because:

Much easier if you're using React

Built-in auto-zoom with .fitView()

Professional UI out of the box

But less control over the physics

The document includes:

✅ Complete code examples for both D3 and React Flow

✅ Links to working demos you can fork and edit

✅ Video tutorials explaining concepts

✅ Physics tuning guide for the "soap bubble" feel

✅ Auto-zoom implementation code

✅ Click-to-expand functionality examples

Start here: Go to https://observablehq.com/@d3/zoomable-circle-packing, click "Fork", and start modifying. It's free, runs in your browser, and you'll see results instantly!


---


you can absolutely use the D3 source code from Observable notebooks in your own projects.

Observable notebooks are built using standard JavaScript, and most D3 examples on Observable are shared under permissive open licenses. You are allowed to:

View and copy the D3 source code directly from any public Observable notebook.

Reuse, adapt, and modify the code for your own personal or commercial projects (respecting the D3 and individual notebook licenses).

Download or export the code to run locally or in your chosen platform (such as VS Code, CodeSandbox, GitHub Pages, etc).

What to watch for:

Most D3-based Observable notebooks are under the MIT license, which permits nearly any use (including commercial and derivative work).

If a specific notebook author has added a different license, check the notebook's header or footer for attribution requirements.

You do NOT need to use Observable’s platform just to use D3 code — you can simply copy and paste the relevant logic and use it in any JavaScript environment.

How to do it:

Open the notebook you like (e.g., https://observablehq.com/@d3/zoomable-circle-packing).

Click through the code cells to find the main logic.

Copy the code and paste it into your project (such as a standalone HTML file or a React/D3/Node.js app).

Make sure to include D3 as a script tag or via npm/yarn import if needed.

Summary:
Observable’s code is for learning and sharing — feel free to study and use D3 code from public Observable notebooks in your own development, without any cost or lock-in. Just respect any license or attribution notices the code author includes.

