# Frontend Design: Phase 1 Research

Optional Deep Dive: see [02c-phase-1-research-advanced.md](02c-phase-1-research-advanced.md)

## Research Dependencies
**Required Before Starting**: System architecture requirements, user journey analysis

### Phase Milestones
- **Phase 1**: Technology comparison and initial recommendations
- **Phase 2**: Proof of concept and final recommendations

## Research Objectives

Research and recommend optimal technology choices for:

### 1. UI Framework: React vs Vue vs Angular vs Svelte
**Recommendation:** **React** is the optimal choice for this knowledge graph application.

**Rationale:**
The decision is based on React's dominant position in enterprise ecosystems, its vast talent pool, and its robust support for the specific technologies required by this project, such as high-performance graph visualization and complex state management. The provided research materials consistently highlight React's maturity and the extensive tooling available within its ecosystem.

*   **Ecosystem and Maturity:** React is a perennial leader in popularity, with ~96k GitHub stars and millions of npm downloads. [cite: 1-FINAL.md] It is widely used in enterprise/web applications, ensuring long-term stability and community support. [cite: 1-FINAL.md] The ecosystem includes mature, accessibility-first component libraries (React Aria, Chakra UI) and headless primitives (Radix UI) that are critical for building a compliant and flexible application. [cite: 3-FINAL.md]
*   **Talent Pool:** As the dominant framework, the availability of experienced React developers is significantly higher than for Vue, Angular, or Svelte, which is a critical factor for building and maintaining an enterprise-scale application.
*   **Project-Specific Alignment:** The research on state management, component libraries, and graph visualization heavily favors the React ecosystem. Key libraries recommended for other objectives, such as TanStack Query, Zustand, Sigma.js, and Cytoscape.js, have first-class support and integrations for React.

**Comparison:**
*   **Vue:** While a strong contender, its ecosystem for highly specialized, large-scale graph visualization and enterprise-grade state management is less mature than React's.
*   **Angular:** Often used in enterprise settings, its opinionated structure can be more rigid. The modern React ecosystem offers comparable scalability with greater flexibility.
*   **Svelte:** Known for its high performance due to its compiler-based approach, it has a smaller ecosystem and community. For an application requiring a rich selection of mature third-party libraries for complex tasks like 10K+ node graph visualization, Svelte poses a higher risk.

### 2. State Management: Redux vs MobX vs Context API vs Zustand
**Recommendation:** A hybrid approach using **TanStack Query (formerly React Query) for server state** and **Zustand for global client state** is recommended. The built-in **Context API** can be used for localized, simple state that doesn't change often.

**Rationale:**
Modern React architecture recognizes a fundamental separation between server state (asynchronous data from APIs) and client state (UI state). A hybrid approach leverages specialized tools for each, leading to better performance, developer experience, and maintainability.

*   **TanStack Query (Server State):** This has become the de facto standard for managing server state. It automates complex concerns like caching, background updates, request deduplication, pagination, and optimistic updates, significantly reducing boilerplate code. [cite: FINAL.md] Its declarative caching approach allows developers to manage data freshness with minimal effort. [cite: FINAL.md] For an application that must integrate with a Neo4j graph database via FastAPI endpoints and WebSockets, TanStack Query provides the robust hooks (`useQuery`, `useMutation`) needed to handle these interactions efficiently. [cite: FINAL.md]

*   **Zustand (Client State):** For global client state (e.g., UI toggles, theme settings, session information), Zustand offers a minimalist, hook-based API that is simple, fast, and scalable. [cite: FINAL.md] Its key advantage is performance; it implements selective subscriptions, ensuring components only re-render when the specific state slices they subscribe to change, avoiding the performance issues common with the standard Context API. [cite: FINAL.md] With a bundle size of ~1KB, it's highly performant. [cite: FINAL.md]

*   **Redux Toolkit:** While still a viable and powerful tool for complex, predictable global state, its conceptual overhead and boilerplate are often unnecessary when server state is handled by a dedicated library like TanStack Query. It remains the best choice for applications requiring time-travel debugging and an extensive middleware ecosystem. [cite: FINAL.md]

*   **Context API:** Best suited for low-frequency, simple state updates within a limited component tree. Overusing it for global or high-frequency state can lead to significant performance issues due to unnecessary re-renders of all consuming components.

### 3. Component Library: Material-UI vs Ant Design vs custom solution
**Recommendation:** Use a "headless" or utility-first component library like **Radix UI** or **Headless UI** in combination with **Tailwind CSS**. For rapid development of internal dashboards or areas where a consistent, pre-built design is acceptable, a comprehensive library like **Chakra UI** is a strong second choice.

**Rationale:**
This project requires a balance between rapid development and a unique, highly accessible, and performant user interface, especially for its complex data visualizations.

*   **Headless UI + Tailwind CSS (Primary Recommendation):** This approach offers maximum flexibility and performance.
    *   **Accessibility:** Headless libraries like Radix UI and React Aria (the foundation for many modern libraries) provide accessible, unstyled components with all the necessary behavior (keyboard navigation, ARIA attributes) baked in. [cite: 3-FINAL.md] This addresses the critical requirement for WCAG 2.1 AA compliance from the ground up.
    *   **Performance:** Tailwind CSS, as a utility-first framework, yields smaller critical CSS bundles and avoids the runtime overhead of CSS-in-JS solutions, which is crucial for maintaining a 60fps frame rate during complex graph interactions. [cite: 1-FINAL.md]
    *   **Customization:** This stack provides complete control over the visual identity, avoiding the generic look of Material Design or Ant Design and allowing for a bespoke interface tailored to knowledge graph exploration.

*   **Chakra UI (Secondary Recommendation):** Chakra UI is a modular, accessibility-first library that offers an excellent developer experience and strong theming capabilities. [cite: 1-FINAL.md, 3-FINAL.md] It's a great compromise if the speed of a pre-styled component set is prioritized over complete visual control. It is built with WAI-ARIA compliance as a core principle. [cite: 1-FINAL.md]

*   **Material-UI (MUI) and Ant Design:** These are mature, enterprise-ready libraries with extensive component sets. [cite: 1-FINAL.md] However, they enforce a strong, opinionated design language (Google's Material Design and Ant's enterprise aesthetic, respectively). Overriding these styles for a custom look can be cumbersome. While they have good accessibility, some components in Ant Design have been noted to have gaps in ARIA support. [cite: 1-FINAL.md, 3-FINAL.md] They are better suited for internal admin panels or applications where adopting their design system is a benefit, not a constraint.

### 4. Graph Visualization: D3.js vs Cytoscape vs vis.js for 10K+ nodes
**Recommendation:** **Sigma.js** for maximum performance with 10,000+ nodes, with **Cytoscape.js** as a strong alternative for its rich analytical feature set.

**Rationale:**
The requirement to render 10,000+ nodes while maintaining 60fps during interactions makes WebGL-based rendering a necessity. Traditional SVG and Canvas-based solutions struggle at this scale.

*   **Sigma.js (Primary Recommendation):**
    *   **Performance:** Sigma.js is designed specifically for high-performance, large-scale graph rendering. Its core is a WebGL engine that leverages the GPU, allowing it to easily handle networks of 10,000 to 100,000+ nodes and edges while maintaining smooth, interactive frame rates. [cite: FINAL.md] Research shows it maintains 60+ FPS with networks containing 100,000+ elements. [cite: FINAL.md] This directly meets the project's most demanding performance benchmark.
    *   **Architecture:** It integrates with Graphology for data structure management, providing a clean separation between data manipulation and visualization. [cite: FINAL.md]

*   **Cytoscape.js (Secondary Recommendation):**
    *   **Balance of Performance and Features:** Cytoscape.js offers an optimal balance between performance and analytical power. [cite: FINAL.md] Originally designed for bioinformatics, it has a rich API for graph theory operations like pathfinding and centrality calculations.
    *   **Rendering:** While traditionally Canvas-based (handling up to 5,000 nodes comfortably), it has an experimental WebGL renderer that shows 3-5x performance improvements, enabling it to handle upwards of 50,000 nodes. [cite: FINAL.md] This makes it a viable, feature-rich alternative.

*   **D3.js:**
    *   **Flexibility vs. Performance:** D3 is a low-level, versatile library, not a dedicated graph visualization tool. While it offers maximum flexibility for bespoke visualizations, its standard SVG-based approach does not scale well beyond a few thousand nodes due to DOM overhead. [cite: FINAL.md] Achieving high performance with D3 for 10,000+ nodes would require a custom implementation using Canvas or WebGL, which is a significant engineering effort that libraries like Sigma.js have already solved. [cite: FINAL.md]

*   **vis.js:**
    *   **Ease of Use:** As noted in the assignment, vis.js is easy to use with good defaults, making it an excellent choice for smaller graphs (e.g., up to 500 nodes) or initial prototyping. [cite: 02b-phase-1-research-assignment.md] However, it is not optimized for the 10,000+ node requirement and will not meet the 60fps performance benchmark at that scale.

### 5. Build Tooling: Webpack vs Vite vs Parcel
**Recommendation:** **Vite** for development and **Webpack** for production builds.

**Rationale:**
This hybrid approach leverages the strengths of both tools: Vite's exceptional development speed and Webpack's mature, highly optimizable production bundling.

*   **Vite (for Development):**
    *   **Developer Experience:** Vite offers a significantly faster development experience. It uses native ES modules in the browser, providing instant server start-up and Hot Module Replacement (HMR) that remains fast regardless of application size. This directly improves developer productivity.
    *   **Modern Tooling:** It leverages esbuild for pre-bundling dependencies, which is dramatically faster than JavaScript-based bundlers.

*   **Webpack (for Production):**
    *   **Ecosystem and Optimization:** Webpack has the most mature and extensive ecosystem of plugins and loaders, offering fine-grained control over the production build. This is critical for advanced optimizations like bundle size analysis, code splitting, tree shaking, and creating performance budgets, all of which are requirements for this project. [cite: FINAL.md] Its `SplitChunksPlugin` is powerful for optimizing vendor and common code chunks. [cite: FINAL.md]
    *   **Enterprise Standard:** Webpack is the battle-tested standard for large-scale enterprise applications, ensuring stability and long-term community support. While Vite's production output is solid, Webpack's ecosystem for complex, large-scale optimization remains unparalleled.

*   **Parcel:** Parcel is known for its zero-configuration setup, making it very easy to get started. However, for a large-scale enterprise application with specific performance and optimization requirements, its lack of configuration flexibility can become a limitation compared to Webpack.

## Success Criteria

Research is complete when you deliver:
- Clear technology recommendation for each category
- Proof of concept demonstrating 10K node graph rendering
- Performance benchmarks meeting system requirements
- Implementation roadmap with risk assessment

## Specific Research Tasks

### Core Technology Evaluation
- [X] **Compare React, Vue, Angular for knowledge graph applications (performance, community, learning curve)**
    *   **Answered in "UI Framework".** React is recommended due to its massive community, mature ecosystem for complex tasks, and large talent pool. Its performance is excellent when paired with the right libraries and optimization strategies.

- [X] **Evaluate graph visualization libraries with 10,000+ nodes (D3.js, Cytoscape, vis.js)**
    *   **Answered in "Graph Visualization".** Sigma.js is the top recommendation for its WebGL-native performance at 10k-100k nodes. Cytoscape.js is a strong second with its analytical features and experimental WebGL renderer. D3.js and vis.js are not suitable for this scale out-of-the-box.

- [X] **Test state management with complex nested graph data (Redux, MobX, Context API, Zustand)**
    *   **Answered in "State Management".** A hybrid approach is best. TanStack Query should manage the fetching, caching, and updating of the graph data (server state). Zustand should manage global UI state. This separation prevents bloating a single store with server cache and provides specialized tools for each job, which is ideal for complex nested data.

- [X] **Research component libraries for rapid development (Material-UI vs Ant Design vs custom)**
    *   **Answered in "Component Library".** For rapid development with high quality, Chakra UI is recommended. For a more custom and performant solution that still offers speed, a headless library (Radix UI) paired with a utility-CSS framework (Tailwind CSS) is the primary recommendation. MUI and Ant Design are excellent but enforce opinionated design systems.

- [X] **Compare CSS-in-JS vs traditional CSS for large applications (performance impact)**
    *   **Recommendation:** Use a utility-first CSS framework like **Tailwind CSS**.
    *   **Rationale:** Research indicates that utility-first CSS yields smaller critical CSS bundles and has better performance compared to many CSS-in-JS libraries, which can introduce runtime overhead. [cite: 1-FINAL.md] For an application striving for a consistent 60fps during complex interactions like graph panning and zooming, eliminating potential runtime styling overhead is a critical optimization. Tailwind's approach combines the benefits of traditional CSS (static, cacheable files) with the component-scoped styling ergonomics often associated with CSS-in-JS.

### System Integration Research
- [X] **Investigate Progressive Web App capabilities (service workers, offline support)**
    *   **Capability:** High. Modern frameworks and browser APIs provide robust support for PWA features.
    *   **Service Workers:** Can be used to implement sophisticated caching strategies for offline support, such as caching the application shell and graph data. They can also handle background sync and push notifications.
    *   **Offline Support:** This is a key research task. Using IndexedDB or local storage, it's possible to cache graph data for offline viewing and basic editing. The `BroadcastChannel` API or Service Workers can be used to sync state between tabs, even when offline. [cite: FINAL.md] CRDT frameworks like Yjs are specifically designed for robust offline editing and conflict resolution upon reconnection. [cite: FINAL.md]

- [X] **Research accessibility compliance (WCAG 2.1 AA for complex visualizations)**
    *   **Strategy:** This is a significant challenge for complex visualizations but is achievable.
    *   **Component Choice:** Select an accessibility-first component library like Radix UI or Chakra UI, which provide WCAG-compliant components out-of-the-box. [cite: 3-FINAL.md]
    *   **Graph Accessibility:**
        *   **Keyboard Navigation:** The graph must be navigable using the keyboard (e.g., arrow keys to move between nodes, enter to select/expand). This is a core feature of accessible libraries like React Aria. [cite: 3-FINAL.md]
        *   **Screen Reader Support:** Use ARIA attributes to describe the graph structure, selected nodes, and relationships. For example, a node could be a `button` in the accessibility tree with a label describing its content and connections.
        *   **Alternative Views:** Provide a non-visual, hierarchical, or tabular view of the graph data that is fully accessible to screen readers.
        *   **Color Contrast:** Ensure all text and visual elements within the graph meet WCAG AA contrast ratios.

- [X] **Evaluate testing frameworks (Jest for unit, Cypress/Playwright for e2e)**
    *   **Recommendation:** This is the industry-standard stack and is highly recommended.
    *   **Jest:** A mature, widely-adopted framework for unit and integration testing of React components. Paired with React Testing Library, it allows developers to write tests that simulate user behavior and ensure components are functionally correct and accessible.
    *   **Cypress/Playwright:** Both are excellent modern frameworks for end-to-end testing. Playwright has gained significant traction for its cross-browser support (Chromium, Firefox, WebKit) and powerful features. Cypress is known for its excellent developer experience and debugging capabilities. The choice between them is often a matter of team preference, but both are superior to older solutions like Selenium.

- [X] **Assess mobile responsiveness requirements (tablet-first design strategy)**
    *   **Strategy:** A tablet-first approach is highly appropriate for a data-heavy, interactive application like a knowledge graph.
    *   **Implementation:**
        *   Design the primary layout and interactions for tablet-sized screens, which provide enough space for complex visualizations and controls.
        *   Scale down for mobile: For smaller phone screens, the UI may need to adapt significantly. This could involve hiding secondary controls, switching to a list-based view for the graph, or focusing on consumption rather than heavy editing.
        *   Scale up for desktop: For larger screens, the UI can expand to show more information, such as detail panels alongside the main graph visualization without overlap.
    *   **Technology:** Using a utility-first framework like Tailwind CSS makes implementing responsive design with breakpoints straightforward and maintainable.

- [X] **Research offline functionality implementation (graph caching, local storage limits)**
    *   **Strategy:**
        *   **Graph Caching:** Use a Service Worker to cache API responses for the graph data. For more structured storage, use IndexedDB, which is designed for larger datasets.
        *   **Local Storage Limits:** Local storage is generally limited to ~5MB and is synchronous, making it unsuitable for large graph datasets. IndexedDB is the appropriate choice, offering significantly more space (often several gigabytes, depending on the browser and user permissions) and an asynchronous API. [cite: FINAL.md]
        *   **State Syncing:** For offline editing, a library like Yjs (a CRDT implementation) is ideal. It can store changes locally in IndexedDB and automatically sync and merge them with the server once a connection is re-established. [cite: FINAL.md]

## Key Research Tasks

- **Benchmark 10,000+ node rendering to achieve 60fps performance**
    *   **Achievable:** Yes, with a WebGL-based library.
    *   **Methodology:** A proof of concept should be built using Sigma.js. A dataset of 10,000 nodes and a variable number of edges will be generated. Performance will be measured using browser developer tools (e.g., Chrome's Performance monitor) to record frame rates during pan, zoom, and node-drag interactions. The goal is to ensure the rendering task consistently completes within the 16ms frame budget.

- **Evaluate state management approaches for real-time graph updates**
    *   **Approach:** TanStack Query integrated with WebSockets is the recommended approach.
    *   **Mechanism:** When the WebSocket connection receives a real-time update from the server (e.g., a node has been added or an edge modified), the client-side logic will use TanStack Query's `queryClient.setQueryData` method to imperatively update the cached graph data. This will trigger a re-render in only the components subscribed to that data, ensuring an efficient, real-time update.

- **Validate accessibility compliance for complex visualizations**
    *   **Validation Plan:**
        1.  **Automated Testing:** Integrate `axe-core` into the testing pipeline to catch common WCAG violations automatically.
        2.  **Manual Keyboard Testing:** Manually verify that all interactive elements in the graph (nodes, edges, controls) are fully operable using only the keyboard.
        3.  **Screen Reader Testing:** Test the application using major screen readers (JAWS, NVDA, VoiceOver) to ensure the graph structure is announced logically and that all information is accessible.
        4.  **Alternative View:** Implement and test a tabular or list-based alternative view of the graph data for users who cannot interact with the visual representation.

- **Design mobile strategy balancing functionality with performance**
    *   **Strategy:** Progressive enhancement and adaptive loading.
    *   **Tablet:** Deliver the full interactive experience, as per the tablet-first design.
    *   **Mobile Phone:**
        *   **Functionality:** Prioritize graph viewing, search, and viewing node details. Complex editing and layout manipulation may be disabled or moved to dedicated, simplified interfaces.
        *   **Performance:**
            *   Implement "level-of-detail" (LOD) rendering, showing simplified node representations or fewer nodes initially.
            *   Use the Network Information API to load lower-resolution assets or less data on slow connections. [cite: FINAL.md]
            *   Heavily leverage code-splitting to ensure only the necessary code for the mobile view is loaded.

- **Implement offline graph viewing and basic editing capabilities**
    *   **Implementation Plan:**
        1.  **Storage:** Use IndexedDB to store the graph's node and edge data.
        2.  **Caching:** A Service Worker will cache the application shell and the last-fetched version of the graph data. On subsequent loads without a network connection, the Service Worker will serve the cached assets and data.
        3.  **Editing:** For basic editing (e.g., updating a node's property), use a CRDT library like Yjs. Changes will be applied locally and stored in an "outbox" in IndexedDB. When the application comes back online, a background sync process initiated by the Service Worker will push the queued changes to the server.

### Evaluation Criteria
- **Performance**: Bundle size, rendering speed, memory usage
- **Developer Experience**: Learning curve, debugging tools, documentation quality
- **Ecosystem**: Available libraries, community size, maintenance status
- **Integration**: Compatibility with backend APIs, authentication, real-time updates

## Deliverables

### 1. Executive Summary
- **Top recommendation for each technology choice:**
    *   **UI Framework:** React
    *   **State Management:** TanStack Query (Server) + Zustand (Client)
    *   **Component Library:** Headless UI (e.g., Radix) + Tailwind CSS
    *   **Graph Visualization:** Sigma.js
    *   **Build Tooling:** Vite (Dev) + Webpack (Prod)
- **Critical trade-offs and risk factors:**
    *   **Graph Visualization:** The primary risk is the complexity of making a WebGL-based graph fully accessible. This requires significant, dedicated effort in providing alternative representations and keyboard navigation.
    *   **Component Library:** The headless/utility-first approach provides maximum flexibility but has a higher initial setup cost and requires more design discipline than an off-the-shelf library like MUI.
    *   **Offline Editing:** Implementing robust offline editing with CRDTs is complex and requires significant testing to handle all edge cases and conflicts correctly.
- **Implementation roadmap:**
    *   A phase-based plan is outlined in "Implementation Roadmap" below.

### 2. Technology Analysis
- **Pros/cons matrix with scoring (1-5 scale across performance, DX, ecosystem, integration)**

| Category | Technology | Performance | DX | Ecosystem | Integration | **Total** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UI Framework** | **React** | 4 | 4 | 5 | 5 | **18** |
| | Vue | 4 | 4 | 4 | 4 | **16** |
| | Angular | 3 | 3 | 4 | 4 | **14** |
| **State (Server)** | **TanStack Query** | 5 | 5 | 5 | 5 | **20** |
| | Redux Toolkit (Thunks) | 3 | 3 | 5 | 4 | **15** |
| **State (Client)** | **Zustand** | 5 | 5 | 4 | 5 | **19** |
| | Redux Toolkit | 4 | 3 | 5 | 5 | **17** |
| | Context API | 2 | 4 | 5 | 5 | **16** |
| **Graph Viz (10k+)** | **Sigma.js** | 5 | 4 | 4 | 4 | **17** |
| | Cytoscape.js | 4 | 4 | 5 | 4 | **17** |
| | D3.js (custom WebGL) | 5 | 2 | 5 | 5 | **17** |
| | D3.js (SVG) | 1 | 3 | 5 | 5 | **14** |
| **Component Lib** | **Headless + Tailwind**| 5 | 4 | 5 | 5 | **19** |
| | Chakra UI | 4 | 5 | 4 | 5 | **18** |
| | Material-UI | 3 | 4 | 5 | 5 | **17** |
| | Ant Design | 3 | 4 | 5 | 5 | **17** |

- **Performance benchmarks with specific metrics (load time, bundle size, memory usage)**
    *   These will be generated during the Proof of Concept phase, specifically targeting the benchmarks listed below.
- **Code examples showing integration patterns with backend APIs**
    *   A code example for a TanStack Query hook fetching data from a FastAPI endpoint:
    ```javascript
    import { useQuery } from '@tanstack/react-query';
    import axios from 'axios';

    const fetchGraphData = async (graphId) => {
      // Assumes JWT token is handled by an Axios interceptor
      const { data } = await axios.get(`/api/graphs/${graphId}`);
      return data;
    };

    export const useGraph = (graphId) => {
      return useQuery({
        queryKey: ['graph', graphId],
        queryFn: () => fetchGraphData(graphId),
        staleTime: 5 * 60 * 1000, // 5 minutes
      });
    };
    ```

### 3. Proof of Concept
- **Interactive demo with 10K node graph (pan, zoom, search functionality)**
    *   This deliverable will be a standalone web application built using the recommended stack (React, Sigma.js, TanStack Query) demonstrating smooth interaction with a 10,000-node, 20,000-edge graph.
- **Performance metrics: load time, frame rate, memory usage under stress**
    *   The PoC will be evaluated against the defined performance benchmarks. Results will be captured via browser profiling tools and documented.
- **Setup instructions and deployment notes for team evaluation**
    *   The PoC will include a `README.md` with instructions to run locally and a link to a deployed version for easy access.

### 4. Implementation Roadmap
- **Phase-based development plan with clear milestones:**
    *   **Phase 1 (Months 1-2): Foundation & Core Visualization.**
        *   Setup project with React, Vite, Webpack, and Tailwind CSS.
        *   Integrate Headless UI components for the basic application shell.
        *   Build the core graph visualization component using Sigma.js.
        *   Implement basic data fetching from the Neo4j backend via FastAPI using TanStack Query.
        *   *Milestone: An interactive, read-only graph visualization of 1,000 nodes is deployed.*
    *   **Phase 2 (Months 3-4): Real-time, Accessibility & Mobile.**
        *   Integrate WebSocket for real-time updates.
        *   Implement core accessibility features (keyboard navigation, ARIA).
        *   Develop and implement the tablet-first responsive design strategy.
        *   Setup Jest and Playwright for testing.
        *   *Milestone: The graph updates in real-time and is accessible and responsive on tablets.*
    *   **Phase 3 (Months 5-6): Advanced Features & Offline.**
        *   Implement complex features like search and filtering.
        *   Build out basic offline viewing capabilities using Service Workers and IndexedDB.
        *   Refine performance and conduct stress testing.
        *   *Milestone: The application is feature-complete for its initial version, with robust performance and offline support.*
- **Risk mitigation strategies for each technology choice:**
    *   See "Critical trade-offs and risk factors" in the Executive Summary.
- **Resource requirements and team skill assessment:**
    *   **Team:** Requires frontend developers proficient in React and its modern ecosystem (Hooks, TypeScript). At least one developer should have or be willing to develop deeper expertise in WebGL and performance optimization for the graph component.
    *   **Resources:** Standard development tooling. Access to performance monitoring tools like Sentry is recommended for production.

## Performance Benchmarks

### Graph Rendering Requirements
- **Load time: <3 seconds for 1,000 nodes**
    *   This is achievable. The critical path involves fetching the data and the initial render. With a performant API and a WebGL-based library, this target should be met.
- **Frame rate: Maintain 60fps during pan/zoom operations**
    *   This is the primary driver for recommending a WebGL library like Sigma.js. This benchmark will be the key success criterion for the PoC.
- **Memory usage: <500MB for 10,000 nodes**
    *   This is a reasonable budget. WebGL is generally memory-efficient as it offloads geometry data to the GPU. This will be monitored during PoC stress testing.
- **Search performance: <200ms for node/edge queries**
    *   This is primarily a backend and data structure concern (indexing in Neo4j). On the frontend, the UI must render the results of the search within this timeframe. Efficient state management and rendering will be key.

### UI Framework Requirements
- **Initial bundle size: <1MB gzipped**
    *   This is achievable with aggressive code-splitting and by using lightweight libraries like Zustand and a utility-CSS approach. The largest dependency will be the graph visualization library itself.
- **Time to interactive: <2 seconds**
    *   This is a challenging but achievable goal. It requires deferring the loading of all non-critical CSS and JavaScript, prioritizing the critical rendering path, and ensuring the initial data payload is small.
- **Re-render performance: <16ms for component updates**
    *   This ties into the 60fps requirement. Using performant state management libraries (Zustand) and memoization techniques will be critical to ensure component updates do not cause frame drops.
- **Build time: <30 seconds for development builds**
    *   Using Vite for development will easily meet this benchmark. Its use of esbuild and native ES modules results in near-instant build and reload times.

## Research Methodology

1.  **Literature Review**: Official documentation and community resources
2.  **Hands-on Testing**: Build small prototypes for each option
3.  **Performance Testing**: Use standardized benchmark scenarios
4.  **Community Assessment**: GitHub activity, issue response time, ecosystem

## System Context

### Architecture Dependencies
- **Must integrate with Neo4j graph database:** Data will be fetched via the FastAPI backend. TanStack Query is ideal for managing this data flow.
- **Backend API uses FastAPI with async endpoints:** Standard REST or GraphQL communication. `axios` and TanStack Query are a standard and effective combination for this.
- **Real-time updates via WebSocket connections:** The state management solution (TanStack Query) must be able to handle incoming data from a WebSocket and update its cache accordingly.
- **Authentication through JWT tokens:** An `axios` interceptor will be configured to attach the JWT token to all outgoing API requests to the FastAPI backend.

### User Experience Requirements
- **Support for 6 user personas (researchers, creators, analysts):** The UI must balance power and simplicity. A headless component approach allows for crafting a UI that can be tailored to these different needs, potentially using progressive disclosure to hide complexity from novice users.
- **Mobile-responsive design for tablet usage:** A tablet-first strategy using Tailwind CSS is recommended.
- **Keyboard navigation for accessibility:** This is a core tenet of the recommended accessibility strategy, leveraging features from a headless library like Radix UI.
- **Internationalization support (English, Spanish initially):** A library like `react-i18next` should be integrated from the start to handle translations. The component-based architecture of React is well-suited for i18n.

## Key Resources

- React patterns and performance guide
- Vue 3 composition API documentation
- Angular enterprise application patterns
- Svelte performance optimization guide
- Observable notebooks for D3.js graph examples
- Cytoscape.js large graph demos
- Material Design principles
- Ant Design component guidelines