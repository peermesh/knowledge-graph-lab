While Mermaid is excellent for 2D diagrams, there are several approaches for creating 3D diagrams, flowcharts, and schematics directly in your web browser. Here's what's available:

## 3D Force-Directed Graph Libraries

The most mature solution for 3D graph visualization is **3d-force-graph** by Vasco Asturiano. This powerful JavaScript library creates interactive 3D network diagrams using Three.js/WebGL for rendering and d3-force-3d for physics-based layouts. You can create nodes, links, and complex graph structures with features like:[vasturiano.github+1](https://vasturiano.github.io/3d-force-graph/)

-   Directional arrows and moving particles along edges[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    
-   Custom node geometries (spheres, cubes, text, images, or HTML)[github+1](https://github.com/vasturiano/3d-force-graph)
    
-   Interactive controls (orbit, zoom, pan, click to focus)[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    
-   Dynamic data updates and force-directed layouts[github](https://github.com/vasturiano/3d-force-graph)
    
-   DAG (directed acyclic graph) mode for hierarchical structures[github](https://github.com/vasturiano/3d-force-graph)
    

It also has React bindings (react-force-graph-3d) and versions for VR and AR. The library is well-documented with extensive examples and can handle graphs with thousands of nodes.[vasturiano.github+4](https://vasturiano.github.io/react-force-graph/)

## General 3D Design and Modeling Tools

**Spline** (spline.design) is a browser-based 3D design tool that's gaining popularity for creating interactive 3D content. While not specifically a diagramming tool, Spline offers:[spline+2](https://spline.design/)

-   Real-time collaboration in the browser[spline](https://spline.design/)
    
-   3D modeling, animation, and interactive experiences[spline](https://spline.design/)
    
-   Export to web-friendly formats[spline](https://spline.design/)
    
-   Component-based systems for reusable objects[designcode](https://designcode.io/spline-ui-shapes-and-materials/)
    
-   Path animation and interaction capabilities[designcode](https://designcode.io/spline-ui-shapes-and-materials/)
    

Spline is more focused on visual design and UI elements rather than technical diagrams, but you could create custom 3D flowcharts and schematics with it.[spline+1](https://spline.design/examples)

## Three.js-Based Solutions

Since you mentioned wanting something web-based, **Three.js** itself is the underlying technology for most 3D web graphics. Several developers have created diagram-specific tools on top of Three.js:[threejs](https://threejs.org/)

-   **3D-force-graph** (mentioned above) - the most complete solution for network diagrams[vasturiano.github+1](https://vasturiano.github.io/3d-force-graph/)
    
-   Custom implementations using Three.js with D3.js for data visualization[tomsawyer+1](https://blog.tomsawyer.com/advanced-techniques-in-threejs-graph-visualization)
    
-   **Firefly** - a browser-based tool for visualizing 3D particle data (though focused on scientific data)[arxiv](https://arxiv.org/pdf/2207.13706.pdf)
    

Three.js can be combined with diagramming logic, but you'd need to build more of the diagramming interface yourself compared to using a dedicated library like 3d-force-graph.[modeling-languages+1](https://modeling-languages.com/javascript-drawing-libraries-diagrams/)

## Web-Based 3D Modeling Platforms

Several browser-based 3D modeling tools could be adapted for technical diagrams:

-   **Clara.io** - full-featured cloud-based 3D modeling and rendering[clara](https://clara.io/)
    
-   **Figuro** - free online 3D modeling focused on simplicity[figuro](https://www.figuro.io/)
    
-   **SketchUp Free** - web-based version of the popular 3D design tool[sketchup.trimble](https://sketchup.trimble.com/en/plans-and-pricing/sketchup-free)
    
-   **Tinkercad** - beginner-friendly web-based 3D design[tinkercad](https://www.tinkercad.com/)
    

These are primarily 3D modeling tools rather than diagramming-specific solutions, so they may require more manual work to create flowcharts and technical diagrams.

## Specialized Diagram Tools with Limited 3D

Traditional diagramming tools are mostly 2D-focused, though some offer limited 3D visualization:

-   **Draw.io/diagrams.net** supports 3D network diagrams with isometric shapes[diagrams+1](https://app.diagrams.net/)
    
-   Standard flowchart tools (Lucidchart, SmartDraw, Miro) primarily work in 2D[smartdraw+2](https://www.smartdraw.com/flowchart/flowchart-maker.htm)
    

## Recommendation

For web-based 3D diagrams similar to Mermaid's text-to-diagram approach, **3d-force-graph** is your best option. It's:[github+1](https://github.com/vasturiano/3d-force-graph)

-   Mature and well-maintained with extensive documentation
    
-   Specifically designed for graph/network visualization in 3D
    
-   Works entirely in the browser using WebGL
    
-   Highly interactive and performant
    
-   Has both vanilla JavaScript and React versions
    
-   Supports various data formats and customization
    

If you want more artistic/design-oriented 3D diagrams with smooth animations, **Spline** offers an excellent browser-based experience, though it requires more manual design work rather than programmatic generation.[spline](https://spline.design/)

For a middle ground, you could combine **Three.js** with existing 2D diagram libraries to build your own 3D diagramming solution, though this requires more development effort than using an existing library like 3d-force-graph.[threejs](https://threejs.org/)

## Interactive 3D Diagramming with Labels, Hover States, and Step-Through Features

Based on your requirements for labels, text, hover states, and timeline/step-by-step walkthrough capabilities, here are the best solutions for creating interactive 3D infographics on the web:

## **3d-force-graph: Comprehensive Interactive Features**

The **3d-force-graph** library is exceptionally well-suited for your needs with robust built-in support for all your requirements:[github+1](https://github.com/vasturiano/3d-force-graph)

**Labels and Text**

-   `nodeLabel` and `linkLabel` methods support plain text, HTML strings, or HTML elements for both nodes and links[vasturiano.github+1](https://vasturiano.github.io/3d-force-graph/)
    
-   Labels appear as tooltips on hover by default[github+1](https://github.com/vasturiano/3d-force-graph/issues/34)
    
-   You can create always-visible labels by using custom node geometries with `nodeThreeObject()` that include text sprites[github](https://github.com/vasturiano/3d-force-graph/issues/34)
    
-   HTML content can be embedded directly in nodes for rich text display[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    

**Hover States and Interactions**

-   `onNodeHover()` and `onLinkHover()` callbacks detect when users hover over elements[github+1](https://github.com/vasturiano/3d-force-graph)
    
-   `enablePointerInteraction` activates mouse tracking for hover/click functionality and tooltip labels[github](https://github.com/vasturiano/3d-force-graph)
    
-   `linkHoverPrecision` controls how closely users need to look at links to trigger hover states[github](https://github.com/vasturiano/3d-force-graph)
    
-   Customizable cursor changes with `showPointerCursor`[github](https://github.com/vasturiano/3d-force-graph)
    
-   Full click support with `onNodeClick()`, `onLinkClick()`, and right-click handlers[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    

**Camera Control for Step-by-Step Walkthroughs**

-   `cameraPosition()` method allows animated camera movements to specific coordinates with configurable duration[vasturiano.github+1](https://vasturiano.github.io/3d-force-graph/)
    
-   Second parameter defines what the camera should look at, perfect for focusing attention on specific nodes[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    
-   `zoomToFit()` automatically frames specific nodes or the entire graph[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    
-   Multiple examples show "click to focus on node" functionality[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    

**Animation and Timeline Features**

-   Directional particles can move along links to show flow and direction[github+1](https://github.com/vasturiano/3d-force-graph)
    
-   `emitParticle()` triggers particles on-demand for specific events[github+1](https://github.com/vasturiano/3d-force-graph)
    
-   Dynamic data changes allow you to update the graph in real-time as you progress through steps[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    
-   Callback functions like `onEngineTick()` let you orchestrate timed sequences[vasturiano.github](https://vasturiano.github.io/3d-force-graph/)
    

## **Spline: Visual Design with State-Based Interactions**

**Spline** offers a more design-oriented approach with powerful state-based animation:[spline+2](https://spline.design/)

**State System for Steps**

-   Multiple states can be created for objects, allowing you to define different configurations[spline](https://docs.spline.design/doc/how-state-based-animation-works/docFYKxPEbGa)youtube
    
-   Switch between states to show different stages of your infographic[spline](https://docs.spline.design/doc/how-state-based-animation-works/docFYKxPEbGa)
    
-   Each state can have different positions, colors, scales, rotations, and visibility settings[spline](https://docs.spline.design/doc/how-state-based-animation-works/docFYKxPEbGa)
    

**Events and Interactivity**

-   Comprehensive event system including Start, Mouse Hover, Mouse Down/Up, Click, and more[spline](https://docs.spline.design/interaction-states-events-and-actions/events-interactivity)youtube
    
-   Events trigger transitions between states, perfect for step-by-step walkthroughsyoutube[spline](https://docs.spline.design/interaction-states-events-and-actions/events-interactivity)
    
-   Loop animations with ping-pong effects for continuous motionyoutube
    
-   Custom transition curves and timing controls[spline](https://docs.spline.design/interaction-states-events-and-actions/events-interactivity)
    

**Text and Annotations**

-   Full text support within the 3D environment[spline](https://spline.design/)
    
-   Web browser events allow interactive text overlays[spline](https://spline.design/)
    
-   Component-based system for reusable elements[spline](https://spline.design/)
    

**Limitations**: Spline is more manual/design-focused rather than data-driven like 3d-force-graph, so it works better for crafted presentations than dynamic diagrams.[designcode+1](https://designcode.io/spline-ui-shapes-and-materials/)

## **Vectary: Advanced Configurator Features**

**Vectary** specializes in interactive 3D product presentations with excellent annotation capabilities:[vectary+2](https://www.vectary.com/)

**Hotspots System**

-   2D interface elements anchored to 3D objects that remain camera-facing[vectary+1](https://help.vectary.com/documentation/3d-configurator/hotspots)
    
-   Can trigger animations, floating UI, annotations, and interactions[vectary+1](https://www.vectary.com/3d-modeling-blog/5-tips-for-hotspots-alternatives/)
    
-   Supports static images, GIFs, MP4s, and Lottie animationsyoutube[vectary](https://help.vectary.com/documentation/3d-configurator/hotspots)
    
-   Customizable fade behavior when occluded by geometry[vectary](https://help.vectary.com/documentation/3d-configurator/hotspots)
    

**Floating UI**

-   User interfaces that exist within 3D space or can be docked[vectary](https://help.vectary.com/documentation/3d-configurator)
    
-   Perfect for information panels and control interfacesyoutube
    
-   Can appear relative to hotspots with autohide functionalityyoutube
    
-   Support for text, images, videos, and audio contentyoutube
    

**Interactions Mode**

-   Define complex interactive behaviors through user-triggered actions[vectary](https://help.vectary.com/documentation/3d-configurator)
    
-   Visibility actions control what appears at each stepyoutube
    
-   Click triggers can reveal information progressivelyyoutube
    

**Variants and Animations**

-   Switch between different object states for step-by-step reveals[vectary](https://help.vectary.com/documentation/3d-configurator)
    
-   Keyframe-based animations for highlighting features[vectary](https://help.vectary.com/documentation/3d-configurator)
    
-   Variables and expressions for advanced logic[vectary](https://help.vectary.com/documentation/3d-configurator)
    

## **Tiki-Toki: 3D Timeline Specialist**

For timeline-specific visualizations, **Tiki-Toki** offers unique 3D timeline capabilities:[tiki-toki+2](https://www.tiki-toki.com/)

**3D Timeline View**

-   First-person 3D perspective for walking through timelines[tiki-toki+1](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    
-   Easy toggle between 2D and 3D views[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    
-   Multiple navigation methods (scroll, drag, keyboard, click)[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    

**Interactive Content Panels**

-   Expandable panels for detailed information about each event[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    
-   Support for text, images, videos (YouTube, Vimeo), and audio[tiki-toki+1](https://www.tiki-toki.com/faqs/)
    
-   Automatic image galleries with smooth animations[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    

**Timeline Controls**

-   Category filters to show/hide different event types[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    
-   Search functionality for finding specific events[tiki-toki](https://www.tiki-toki.com/blog/entry/interactive-timelines/)
    
-   Multiple view modes including Category Band and Duration views[tiki-toki+1](https://www.tiki-toki.com/faqs/)
    
-   Zoom controls for managing dense timelines[tiki-toki+1](https://www.tiki-toki.com/faqs/)
    

**Limitations**: Focused specifically on timeline presentations rather than general-purpose 3D diagrams.[ecml+1](https://www.ecml.at/en/Resources/ICT/InventoryID/201)

## **Recommendation for Your Use Case**

For **interactive 3D infographics with step-by-step walkthroughs**, I recommend:

1.  **3d-force-graph** if you need:[github+1](https://github.com/vasturiano/3d-force-graph)
    
    -   Data-driven node/link diagrams
        
    -   Programmatic control over camera movements
        
    -   Complex hover interactions and tooltips
        
    -   Ability to build walkthrough sequences via code
        
2.  **Vectary** if you need:[vectary+1](https://www.vectary.com/)
    
    -   Product visualization or technical schematics
        
    -   Rich annotation system with hotspots
        
    -   Click-through interactive guides
        
    -   No-code approach with visual editor
        
3.  **Spline** if you need:[spline+1](https://docs.spline.design/interaction-states-events-and-actions/events-interactivity)
    
    -   Highly designed, artistic 3D presentations
        
    -   State-based animations between steps
        
    -   Custom 3D models and environments
        
    -   Real-time collaboration features
        

All three support labels, hover states, and step-through interactions, but they approach the problem differently: 3d-force-graph is code-first and data-driven, Vectary is configurator-focused with excellent UI tools, and Spline is design-first with powerful state systems.

Based on your clarification that you need a **programmable, free web-based solution** that runs directly on web pages with high-quality rendering, here are your best options:

## **Three.js with Photorealistic Rendering (Best Overall Solution)**

**Three.js** is completely free, open-source (MIT license), and provides excellent photorealistic rendering capabilities through:[discoverthreejs+2](https://discoverthreejs.com/book/first-steps/physically-based-rendering/)

**Physically Based Rendering (PBR)**

-   `MeshStandardMaterial` and `MeshPhysicalMaterial` for realistic surfaces[css-tricks+2](https://css-tricks.com/creating-photorealistic-3d-graphics-web/)
    
-   Support for metalness, roughness, bump maps, normal maps, and environment maps[discoverthreejs+1](https://discoverthreejs.com/book/first-steps/physically-based-rendering/)
    
-   HDR environment lighting with IBL (Image-Based Lighting)youtube[css-tricks](https://css-tricks.com/creating-photorealistic-3d-graphics-web/)
    
-   Real-time reflections and refractions using environment maps[discourse.threejs](https://discourse.threejs.org/t/photorealistic-render-comparison-why-does-three-js-look-so-bad/25617)youtube
    

**Interactive Labels and Text**

-   **troika-three-text** - High-quality SDF text rendering that integrates directly with Three.js materials[protectwise.github+2](https://protectwise.github.io/troika/troika-three-text/)
    
    -   Parses font files (.ttf, .otf, .woff) on-the-fly[threejsresources+1](https://threejsresources.com/tool/troika-three-text)
        
    -   Supports lighting, shadows, fog on text[discourse.threejs+1](https://discourse.threejs.org/t/troika-3d-text-library-for-sdf-text-rendering/15111)
        
    -   Runs font processing in web workers for performance[protectwise.github+1](https://protectwise.github.io/troika/troika-three-text/)
        
    -   Completely free and open-source[protectwise.github](https://protectwise.github.io/troika/troika-three-text/)
        

**Camera Animation for Step-Through**

-   **GSAP (GreenSock)** - Industry-standard animation library[waelyasmina+2](https://waelyasmina.net/articles/animating-camera-transitions-in-three-js-using-gsap/)
    
    -   `gsap.timeline()` for creating sequential step-by-step animations[typeee+1](https://www.typeee.com/post/668a969eeee2c1191d51068a)
        
    -   Smooth camera position and rotation transitions[vaisakhnp.hashnode+1](https://vaisakhnp.hashnode.dev/camera-animation-using-react-three-fiber-and-gsap)
        
    -   `onUpdate` callbacks to keep camera focused during movement[waelyasmina](https://waelyasmina.net/articles/animating-camera-transitions-in-three-js-using-gsap/)
        
    -   Free for most uses (commercial license available)[waelyasmina](https://waelyasmina.net/articles/animating-camera-transitions-in-three-js-using-gsap/)
        

**Hover States and Interactivity**

-   Built-in raycasting for detecting mouse hover and clicks[css-tricks+1](https://css-tricks.com/creating-photorealistic-3d-graphics-web/)
    
-   Event listeners for pointer events on 3D objects[discourse.threejs+1](https://discourse.threejs.org/t/techniques-to-render-photo-realistic-three-js/17530)
    
-   Full control over interactive behaviors via JavaScript[discoverthreejs+1](https://discoverthreejs.com/book/first-steps/physically-based-rendering/)
    

**Example Implementation Pattern:**

## **Babylon.js (Feature-Rich Alternative)**

**Babylon.js** is another excellent free option (Apache 2.0 license):[babylonjs+2](https://www.babylonjs.com/)

**Advantages:**

-   Completely free and open-source forever[babylonjs+1](https://forum.babylonjs.com/t/what-is-the-bjs-future-about-opensource-license-and-is-that-wanna-be-changed/2137)
    
-   Built-in PBR materials with excellent photorealistic rendering[sitepoint+1](https://www.sitepoint.com/using-babylon-js-build-3d-games-web/)
    
-   **GUI3DManager** for native 3D UI elements with tooltips[doc.babylonjs+2](https://doc.babylonjs.com/features/featuresDeepDive/gui/gui3D)
    
    -   Built-in tooltip system for hover states[babylonjs+1](https://forum.babylonjs.com/t/made-some-cool-tooltips/38516)
        
    -   3D buttons, panels, and interactive elementsyoutube[doc.babylonjs](https://doc.babylonjs.com/features/featuresDeepDive/gui/gui3D)
        
    -   HTML integration for annotations[babylonjs+1](https://forum.babylonjs.com/t/simple-text-label-in-3d-world/16613)
        
-   Extensive free asset library[doc.babylonjs+1](https://doc.babylonjs.com/toolsAndResources/assetLibrarian)
    
-   Very well-documented with many tutorials[thisdot+1](https://www.thisdot.co/blog/introduction-to-babylon-js)
    

**Interactive Features:**

-   Native action system for hover/click events[sitepoint](https://www.sitepoint.com/using-babylon-js-build-3d-games-web/)youtube
    
-   Built-in animation timeline system[github+1](https://github.com/playcanvas/engine)
    
-   VR/AR support built-in[thisdot](https://www.thisdot.co/blog/introduction-to-babylon-js)
    
-   Physics engine integration[thisdot](https://www.thisdot.co/blog/introduction-to-babylon-js)
    

**Text Rendering:**

-   Dynamic texture system for 3D text labels[babylonjs+1](https://forum.babylonjs.com/t/optimizing-scene-with-lots-thousands-of-2d-text-labels-in-3d-space/25666)
    
-   Support for thousands of labels with optimization techniques[babylonjs](https://forum.babylonjs.com/t/optimizing-scene-with-lots-thousands-of-2d-text-labels-in-3d-space/25666)
    
-   GUI components specifically designed for annotations[reactylon+1](https://reactylon.com/docs/gui/3d)
    

## **React Three Fiber (If Using React)**

If you're building with React, **React Three Fiber** provides:[abhijitrao+2](https://www.abhijitrao.info/blog/threejs/annotations)

-   Declarative Three.js using React components[reddit+1](https://www.reddit.com/r/threejs/comments/104iisk/how_to_make_annotation_shortcuts_on_an_animation/)
    
-   **@react-three/drei** library with `<Html>` component for annotations[sbcode+2](https://sbcode.net/react-three-fiber/annotations/)
    
    -   Real HTML elements positioned in 3D space[abhijitrao+1](https://www.abhijitrao.info/blog/threejs/annotations)
        
    -   Perfect for rich tooltips and interactive overlays[discourse.threejs+1](https://discourse.threejs.org/t/how-can-i-add-annotations-to-different-mesh-parts-or-textures-and-shift-the-camera-focus-to-them-when-clicked/82114)
        
-   GSAP integration for camera animations[gsap+1](https://gsap.com/community/forums/topic/44834-how-to-use-gsap-scrolltrigger-or-timeline-with-floating-threejs-models/)
    
-   Same photorealistic PBR capabilities as Three.js[reddit+1](https://www.reddit.com/r/reactjs/comments/t1nif9/3d_models_in_react_with_reactthreefiber/)
    
-   Completely free and open-source[r3f.pmnd+1](https://r3f.docs.pmnd.rs/getting-started/examples)
    

## **PlayCanvas (Web-First Game Engine)**

**PlayCanvas** offers:[developer.mozilla+2](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas)

-   Free tier with unlimited public projects[developer.mozilla+1](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas)
    
-   Open-source engine (MIT license)youtube[github](https://github.com/playcanvas/engine)
    
-   Can be used programmatically without the editor[playcanvas+2](https://forum.playcanvas.com/t/using-playcanvas-for-website-development/12709)
    
-   Built-in PBR rendering[github](https://github.com/playcanvas/engine)
    
-   Physics, audio, and animation systemsyoutube[github](https://github.com/playcanvas/engine)
    
-   Can be embedded in existing web pages via iframe[playcanvas+1](https://blog.playcanvas.com/declarative-3d-with-playcanvas-react/)
    

**Limitations:** Best results come from using their editor, though the engine itself is fully programmable.[developer.mozilla+1](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas)

## **Recommendation for Your Use Case**

For **programmable, free, photorealistic 3D diagrams with labels, hover states, and step-through timelines**, I recommend:

**Three.js + troika-three-text + GSAP** because:

1.  **Completely free** - All MIT/permissive licenses[threejs+1](https://threejs.org/)
    
2.  **Photorealistic rendering** - Industry-standard PBR with HDR environmentsyoutube[css-tricks+1](https://css-tricks.com/creating-photorealistic-3d-graphics-web/)
    
3.  **Professional text** - troika-three-text provides crisp, styled labels that work with lighting[threejsresources+2](https://threejsresources.com/tool/troika-three-text)
    
4.  **Timeline control** - GSAP provides powerful step-by-step animation sequencing[typeee+1](https://www.typeee.com/post/668a969eeee2c1191d51068a)
    
5.  **Full programmatic control** - Pure JavaScript/TypeScript, runs anywhere[threejs+1](https://threejs.org/)
    
6.  **Massive ecosystem** - Largest community, most examples, best documentation[pixelfreestudio+2](https://blog.pixelfreestudio.com/top-webgl-libraries-for-building-3d-interactive-websites/)
    
7.  **No vendor lock-in** - Run it on any web page you control[css-tricks+1](https://css-tricks.com/creating-photorealistic-3d-graphics-web/)
    

**Alternative:** **Babylon.js** if you prefer a more integrated, batteries-included approach with built-in GUI systems and excellent official documentation. It's equally free and powerful, just with a slightly different API philosophy (more object-oriented vs. Three.js's functional approach).[doc.babylonjs+5](https://doc.babylonjs.com/journey/theFirstStep)

Both are production-ready, completely free, and capable of the photorealistic quality you're looking for.[discourse.threejs+3](https://discourse.threejs.org/t/photorealistic-render-comparison-why-does-three-js-look-so-bad/25617)