# Knowledge Graph Lab - Shared Module Requirements

**Complete Guide to Using the Shared Module System**

This directory contains the **definitive specifications** for how all Knowledge Graph Lab modules must work together. These requirements override individual module specifications and ensure interoperability.

## 🎯 **What This System Provides**

The shared module system ensures that:
- ✅ All 4 modules (Backend, Frontend, AI, Publishing) can work together
- ✅ Teams can implement features independently but integrate seamlessly
- ✅ Advanced features can be added later without breaking existing functionality
- ✅ Specifications can be validated automatically for compliance

## 📂 **Directory Overview**

```
shared/
├── README.md                    # This guide - how to use everything
├── standalone-modules/
│   └── README.md                # Basic interoperability (handover today)
├── peermesh-modules/
│   └── README.md                # Advanced features (Phase 2+)
└── common/                      # Detailed reference (when you need specifics)
    ├── architecture-overview.md  # Universal architecture patterns
    ├── shared-infrastructure.md # Database, messaging, authentication
    ├── integration-contracts.md # API contracts & interfaces
    ├── development-standards.md # Development environment & testing
    ├── security-compliance.md   # Security baseline & compliance
    ├── performance-scalability.md # Performance requirements
    └── implementation-guide.md  # Phase-by-phase implementation timeline
```

## 🚀 **How to Use Each Component**

### 1. 📋 **Standalone Module** - *Immediate Implementation*
**Use this for:** Getting basic interoperability working right now

**What's included:**
- Complete container architecture requirements
- Database integration standards
- API contract specifications
- Authentication integration
- Development environment setup

**How to use:**
```bash
# 1. Read the complete specification
open docs/modules/shared/standalone-modules/README.md

# 2. Implement the requirements in your module
# 3. Validate compliance
python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md
```

### 2. 🔬 **PeerMesh Module** - *Advanced Features*
**Use this for:** Adding sophisticated capabilities in Phase 2+

**What's included:**
- Parallel search across multiple backends (Neo4j, Qdrant, OpenSearch)
- Event-driven architecture with NATS JetStream
- Dual-layer authorization (SpiceDB + OPA)
- Advanced observability and monitoring

**How to use:**
```bash
# 1. Read the complete advanced specification
open docs/modules/shared/peermesh-modules/README.md

# 2. Plan Phase 2+ enhancements
# 3. Ensure backward compatibility with standalone module
```

### 3. 📚 **Common Directory** - *Detailed Reference*
**Use this when:** You need specific technical details

**What's included:**
- Architecture patterns and principles
- Infrastructure configuration details
- API contract specifications
- Development and testing standards
- Security and compliance requirements
- Performance optimization guidelines
- Implementation roadmap and timelines

**How to use:**
```bash
# Reference specific requirements as needed
open docs/modules/shared/common/architecture-overview.md
open docs/modules/shared/common/shared-infrastructure.md
# etc.
```

## 🔄 **How They Work Together**

### **Hierarchy of Authority**
1. **Standalone Module** → Basic requirements (overrides everything)
2. **PeerMesh Module** → Advanced features (extends standalone)
3. **Common Directory** → Detailed reference (supports both)

### **Implementation Flow**
```
Phase 1 (Immediate):
Standalone Module → Module Implementation → Validation → Team Handover

Phase 2+ (Advanced):
PeerMesh Module → Enhanced Features → Integration → Advanced Validation
```

### **Module Compliance**
Each module specification must:
- ✅ Reference the correct shared module paths
- ✅ Include compliance sections
- ✅ Pass validation checks
- ✅ Override authority statements

## 🛠️ **Tools & Validation**

### **Automated Compliance Checking**
```bash
# Validate any module against standalone requirements
python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md

# Generate detailed compliance report
python3 scripts/validate-standalone-compliance.py docs/modules/frontend-design/Frontend-Design-Spec.md --output report.md

# Check for broken links
python3 .dev/scripts/check_links.py docs/modules/shared/
```

### **Agent Prompt for Specification Updates**
Use the comprehensive agent prompt in this file to:
- Review specifications for compliance
- Identify missing requirements
- Generate change lists
- Implement systematic updates

## 🎯 **Quick Start Guide**

### **For Team Members (Today)**
1. **Read Standalone Module** - Complete basic requirements
2. **Implement in your module** - Follow the specification exactly
3. **Run validation** - Ensure compliance before handover
4. **Test integration** - Verify modules work together

### **For Advanced Development (Phase 2+)**
1. **Read PeerMesh Module** - Understand advanced capabilities
2. **Plan enhancements** - Design backward-compatible features
3. **Implement incrementally** - Add features without breaking existing functionality
4. **Validate thoroughly** - Ensure advanced features work with basic modules

### **For Specification Maintenance**
1. **Use the agent prompt** - Systematic review and updates
2. **Check compliance** - Regular validation of all modules
3. **Update as needed** - Maintain consistency across specifications
4. **Document changes** - Track modifications in change logs

## 📋 **Key Principles**

### **Override Authority**
The shared module requirements are **definitive** and override any conflicting requirements in individual module specifications.

### **Self-Contained Specifications**
Both standalone and PeerMesh modules are **complete and self-contained** - you can implement either without needing external references.

### **Progressive Enhancement**
Start with standalone (basic interoperability) and enhance with PeerMesh (advanced features) as needed.

### **Validation-Driven Development**
Use automated validation to ensure compliance throughout development.

## 🤝 **Contributing**

When adding new shared requirements:
1. **Determine scope** - Standalone (basic) or PeerMesh (advanced)?
2. **Place appropriately** - In correct module with clear naming
3. **Update navigation** - Ensure this README reflects changes
4. **Maintain override authority** - Ensure new requirements take precedence
5. **Add validation** - Include automated compliance checks

## 📊 **Success Metrics**

### **Standalone Module**
- ✅ All modules pass compliance validation
- ✅ Basic interoperability working across all modules
- ✅ Development teams can implement independently
- ✅ Specifications are clear and actionable

### **PeerMesh Module**
- ✅ Advanced features implemented without breaking basic functionality
- ✅ Multi-backend search operational
- ✅ Event-driven architecture functional
- ✅ Enhanced observability and security deployed

---

**Document Status:** APPROVED
**Effective Date:** 2025-10-20
**Review Cycle:** Monthly
**Next Review:** 2025-11-20
