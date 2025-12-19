  WebVOWL could be good for the main ontology view but it hasn't been updated in a while

  We might be best off with Neo4j Bloom because we're running Neo4j, but of course we have plans to not use Neo4j when
  it gets to the point where we'd have to pay and we'd have to be using an open source solution for Neo4j and its
  display system.


  Linkurious is expensive, but has some important design patterns - For example, floating panels for the different
  types of filters. So that the right hand column doesn't have to be a bunch of one big column. It could just be a
  little set of tools. And when you click on the tools it opens the controls for that tool. [Image #1]
  https://linkurious.com/decision-intelligence-platform-overview/


# force layout

  D3 seems to have way better force directed graphs than we're using it for.
  https://blocks.roadtolarissa.com/denisemauldin/cdd667cbaf7b45d600a634c8ae32fae5

  https://observablehq.com/@d3/force-directed-graph-component

  circle packing looks cool:
  https://observablehq.com/@d3/pack-rollup/2 And honestly, it makes more visual sense to me than trying to show every node. 

  So I've been looking through these and it's fairly helpful, but now what I need is a
  something that does the force directed graphs type thing where, and this is specifically for an interface where you
  have a bubble, you click on the bubble and you type something in it and then similar things appear around the
  bubble. But I want it to behave more like bubbles do, where the smaller circles are attached to the outer circle,
  sort of like with surface tension in real bubbles. And I'm wondering if there's something like that out there or
  Ideally, many options for me to look through to find something that could do that view for us. So every time you
  click on an area of the screen, you can type and that becomes a core central bubble. And then outer bubbles appear
  and you can click on them.If you click on a bubble twice, it selects it and deselects it. If you click it once, it selects it. If you select a sub-bubble, it will generate additional bubbles around that sub-bubble. So we need this sort of surface tension hierarchy thing. The behavior of the bubbles in general should feel like soap sliding on a dish where it auto centers and tries to take up the minimal space by being and still be in the center with a way to zoom in and out that crops at the canvas which would be the full width and height of the view and allows you to and automatically scales to fit all of the bubbles that you're working on so the first bubble would look really big but if you've got 10 on the screen they would all be smaller.
  
- d3's clustered bubbles might be what we need!
  https://observablehq.com/@d3/clustered-bubbles
- even better? https://observablehq.com/@d3/zoomable-circle-packing
- https://www.react-graph-gallery.com/example/circle-packing-with-d3-force


  Another design metaphor that might work would be like a infinite grid, sort of like Figma or something, where we draw relationships between things. And that can then show complex data sets like a chunk of text with a large image that represents a photo or a series of images or, you know, any type of visual representation of a non-image file. all laid out in a way where it naturally fills a space with force layout, but looks more like a organized but expanding range of ideas. This might be better for the explorer browser thing as well. Thank you. 