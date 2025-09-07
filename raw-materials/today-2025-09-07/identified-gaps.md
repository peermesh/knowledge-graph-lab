# Key Gaps Identified

## Missing Pieces for Intern Project

### 1. **Module Independence Strategy**
**Gap**: Current materials focus heavily on AI/KG in isolation
**Need**: Clear plan for how each module demos independently
- Systems module: What can it show without other pieces?
- Publishing module: How does it work without full KG?
- Frontend module: What does it display with stub data?

### 2. **Realistic Technical Stack**
**Gap**: Materials assume expert-level semantic web knowledge
**Need**: Technology choices appropriate for interns
- Replace: OWL/RDF/SHACL/Fuseki → JSON/TypeScript/Postgres
- Replace: SPARQL queries → REST endpoints
- Replace: JSON-LD deltas → CSV/JSON imports

### 3. **Integration Touch Points**
**Gap**: No clear interfaces between the 4 modules
**Need**: Define how modules connect
- What APIs does Systems provide?
- What data does AI/KG expose?
- How does Publishing consume creator data?
- What does Frontend need to display?

### 4. **Scaled-Down Scope Definition**
**Gap**: 80-hour single-person project vs 40-hour (4×10h) team project
**Need**: Simplified requirements that fit the time budget
- MVP definitions for each module
- Clear "good enough" acceptance criteria
- Parking lot for future enhancements

### 5. **Demo Day Vision**
**Gap**: No concrete end-to-end scenario defined
**Need**: One clear story that shows all pieces working
- Example: "Submit research about new creator platform → see it in knowledge graph → generate weekly email → view on website"

### 6. **Week 1 Research Focus**
**Gap**: Research briefs are not defined for the simplified scope
**Need**: Focused research questions for each intern
- Systems: How to set up simple multi-service environment?
- AI/KG: What's the simplest useful creator schema?
- Publishing: How to template emails and social posts?
- Frontend: What are the essential user workflows?

### 7. **Risk Mitigation Strategy**
**Gap**: No plan for what happens if someone falls behind
**Need**: Independence ensures project survives individual failures
- Module A delayed → others still demo
- Integration nice-to-have, not requirement
- Clear fallback positions

### 8. **Handoff Documentation**
**Gap**: How does this project continue after 10 weeks?
**Need**: Plan for knowledge transfer and future development
- What gets merged into main KGL project?
- How do findings influence full system design?
- What would be the next 10-week cycle priorities?

## Priority Order for Filling Gaps
1. **Module boundaries** (enables parallel work)
2. **Simple technical stack** (enables Week 1 research)
3. **Demo day scenario** (aligns everyone on the goal)
4. **Integration interfaces** (prevents integration hell in Week 10)
5. **Risk mitigation** (insurance policy for project success)