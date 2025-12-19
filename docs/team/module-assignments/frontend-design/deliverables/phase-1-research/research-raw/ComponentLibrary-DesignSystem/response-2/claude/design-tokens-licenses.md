# Design Tokens License Analysis Table

## Open-Source Licenses

| Tool/Framework | SPDX ID | Use Rights | Redistribution | Cloud/SaaS | Asset Embedding | Key Restrictions | Copyleft Risk |
|----------------|---------|------------|----------------|------------|-----------------|------------------|---------------|
| **Style Dictionary** | Apache-2.0 | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | Must preserve notices | ❌ None |
| **Penpot** | MPL-2.0 | ✅ Commercial use permitted | ✅ Must share modifications to MPL files | ✅ SaaS allowed | ✅ Permitted | File-level copyleft | ⚠️ Weak (file-level) |
| **Theo (Salesforce)** | BSD-3-Clause | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | Cannot use trademark | ❌ None |
| **Material Design 3** | Apache-2.0 | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | Attribution required | ❌ None |
| **Adobe Spectrum** | Apache-2.0 | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | Apache NOTICE file | ❌ None |
| **Shopify Polaris** | MIT | ✅ Commercial use permitted | ✅ No restrictions | ✅ No restrictions | ✅ Permitted | Include copyright | ❌ None |
| **Lightning Design** | BSD-3-Clause | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | No endorsement claims | ❌ None |
| **Universal Design Tokens** | MIT | ✅ Commercial use permitted | ✅ No restrictions | ✅ No restrictions | ✅ Permitted | Include license | ❌ None |
| **Lona (Airbnb)** | MIT | ✅ Commercial use permitted | ✅ No restrictions | ✅ No restrictions | ✅ Permitted | Include copyright | ❌ None |
| **Design Token Transformer** | MIT | ✅ Commercial use permitted | ✅ No restrictions | ✅ No restrictions | ✅ Permitted | Include license | ❌ None |
| **Diez** | Apache-2.0 | ✅ Commercial use permitted | ✅ Source & binary | ✅ No restrictions | ✅ Permitted | Attribution required | ❌ None |

## Proprietary/Commercial Licenses

| Tool/Framework | License Type | Use Rights | Redistribution | Cloud/SaaS | Asset Embedding | Key Restrictions | Commercial Add-ons |
|----------------|-------------|------------|----------------|------------|-----------------|------------------|-------------------|
| **Tokens Studio** | Hybrid (Plugin: Proprietary, Core: Open) | ✅ Plugin free tier available | ❌ No redistribution of plugin | ⚠️ Platform features paid | ✅ Token outputs permitted | Platform features require subscription | Studio Platform (Enterprise) |
| **Specify** | Commercial SaaS | ⚠️ Subscription required | ❌ Not applicable | ✅ Cloud-based service | ✅ Export permitted | Per-seat pricing, API limits | Enterprise tier |
| **Supernova** | Commercial SaaS | ⚠️ Subscription required | ❌ Not applicable | ✅ Cloud-based service | ✅ Export permitted | Seat-based licensing | Enterprise features |
| **Backlight** | Commercial SaaS | ⚠️ Free tier + paid | ❌ Not applicable | ✅ Cloud service | ✅ Export permitted | Team size limits | Team/Enterprise plans |
| **Knapsack** | Commercial SaaS | ⚠️ Enterprise pricing | ❌ Not applicable | ✅ Cloud service | ✅ Export permitted | Enterprise only | Custom pricing |
| **Zeroheight** | Commercial SaaS | ⚠️ Subscription required | ❌ Not applicable | ✅ Cloud service | ✅ Documentation export | Viewer limits | Team plans |
| **Chromatic** | Commercial SaaS | ⚠️ Free tier + paid | ❌ Not applicable | ✅ Cloud service | ✅ Storybook integration | Snapshot limits | Premium features |
| **Interplay** | Commercial SaaS | ⚠️ Subscription required | ❌ Not applicable | ✅ Cloud service | ✅ Export permitted | Per-project pricing | Enterprise tier |

## Integrated/Platform Licenses

| Tool/Framework | License Context | Use Rights | Redistribution | Key Restrictions | Platform Lock-in |
|----------------|----------------|------------|----------------|------------------|------------------|
| **Atlassian Design Tokens** | Product Integration | ✅ Within Atlassian products | ❌ Platform-specific | Forge platform requirements | ⚠️ High (Atlassian ecosystem) |
| **Open edX Tokens** | AGPL-3.0 (Platform) | ✅ Open platform | ✅ Must share modifications | Strong copyleft | ❌ None (open platform) |
| **Android OEM Tokens** | Apache-2.0 (AOSP) | ✅ Android development | ✅ Within Android | Android compatibility | ⚠️ Medium (Android specific) |
| **Figma Variables** | Platform Feature | ⚠️ Figma subscription | ❌ Within Figma only | Figma account required | ⚠️ High (Figma only) |

## Dual-License Considerations

| Tool | Primary License | Alternative License | Choosing Factors | Risks |
|------|----------------|-------------------|------------------|-------|
| **Tokens Studio** | Proprietary (Plugin) | Open components available | Free for basic use, paid for platform features | Feature limitations in free tier |
| **Style Dictionary** | Apache-2.0 | N/A (single license) | Fully open-source | None |
| **Penpot** | MPL-2.0 | N/A (single license) | Fully open-source | File-level copyleft only |

## Asset Embedding & Output Rights

| License Type | Generated CSS/JS | Design Files | Documentation | API Outputs | Important Notes |
|-------------|------------------|--------------|--------------|-------------|-----------------|
| **MIT/Apache/BSD** | ✅ Unrestricted | ✅ Unrestricted | ✅ Unrestricted | ✅ Unrestricted | No attribution required in outputs |
| **MPL-2.0** | ✅ Unrestricted | ✅ Unrestricted | ✅ Unrestricted | ✅ Unrestricted | Only source modifications need sharing |
| **Commercial SaaS** | ✅ You own outputs | ✅ You own exports | ✅ You own content | ✅ You own data | Check ToS for specific rights |
| **Platform-integrated** | ⚠️ Platform-dependent | ⚠️ Platform-dependent | ⚠️ Platform-dependent | ⚠️ Platform-dependent | Review platform license agreements |

## Critical Licensing Insights

### ✅ Safe for Commercial Use (No restrictions):
- **Apache-2.0**: Style Dictionary, Material Design, Adobe Spectrum
- **MIT**: Shopify Polaris, UDT
- **BSD-3**: Theo, Lightning Design

### ⚠️ Requires Careful Review:
- **MPL-2.0**: Penpot (file-level copyleft, but outputs unrestricted)
- **Hybrid models**: Tokens Studio (check feature availability)
- **SaaS platforms**: Review Terms of Service for data ownership

### ❌ Avoid for Certain Use Cases:
- **AGPL-3.0**: If used in backend (Open edX) - strong copyleft
- **Platform-locked**: If vendor independence is required
- **Seat-limited licenses**: For large distributed teams

### Key Legal Considerations:
1. **Output Ownership**: All tools reviewed grant users ownership of generated tokens/code
2. **Attribution**: Open-source tools require attribution in source, not in generated outputs
3. **SaaS Data Portability**: Verify export capabilities before commitment
4. **Copyleft Boundaries**: MPL-2.0 is file-level only, doesn't affect token outputs
5. **Trademark Usage**: BSD-3 and others prohibit using project names for endorsement