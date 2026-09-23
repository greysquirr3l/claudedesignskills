# Claude Design Skillstack

**Professional design agency skillstack for 3D/WebGL, animation, and modern web development**

Claude Code plugin marketplace providing comprehensive coverage of modern web technologies including Three.js, GSAP, React Three Fiber, Motion, Babylon.js, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plugins: 31](https://img.shields.io/badge/Plugins-31-blue.svg)](#available-plugins)
[![Skills: 25](https://img.shields.io/badge/Skills-25-green.svg)](#available-skills)
[![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen.svg)](#status)

## 🚀 Quick Start (Plugin Marketplace)

**New**: Install skills as plugins directly from this marketplace!

```bash
# Add marketplace to Claude Code
/plugin marketplace add greysquirr3l/claudedesignskills

# Install individual plugins
/plugin install threejs-webgl
/plugin install gsap-scrolltrigger
/plugin install react-three-fiber

# Or install complete bundles
/plugin install core-3d-animation        # 5 skills: Three.js, GSAP, R3F, Motion, Babylon
/plugin install extended-3d-scroll       # 6 skills: A-Frame, Vanta, PlayCanvas, PixiJS, Locomotive, Barba
/plugin install animation-components     # 5 skills: React Spring, Magic UI, AOS, Anime.js, Lottie
/plugin install authoring-motion         # 4 skills: Blender, Spline, Rive, Substance 3D
/plugin install meta-skills             # 2 skills: Integration patterns, Modern design
```

**Each plugin includes**:
- ✅ Complete skill content with SKILL.md
- ✅ 1-3 slash commands for quick actions
- ✅ 1-2 specialized agents for domain expertise
- ✅ Scripts, references, and asset templates

📚 **[View complete marketplace documentation →](MARKETPLACE.md)**

## Overview

**31 plugins (25 individual + 6 bundles)** extending Claude Code with specialized knowledge for cutting-edge web technologies.

**Key Features**:
- 🏪 Plugin marketplace with 31 ready-to-install plugins
- ✅ 25 individual skills + 6 category bundles
- 🔧 60+ slash commands for instant boilerplate generation
- 🤖 27+ specialized agents for domain expertise
- 📚 Comprehensive patterns, examples, and integration guides
- 🚀 Auto-activates when Claude detects relevant tasks

## What are Claude Skills?

Modular packages that teach Claude specific technologies. Each contains:
- **SKILL.md** - Instructions and patterns
- **references/** - API docs and guides
- **scripts/** - Automation utilities
- **assets/** - Templates and examples

Progressive disclosure: Claude loads only what's needed per task.

## Available Plugins

### Individual Plugins (25)

All plugins include slash commands and specialized agents. [Full details →](MARKETPLACE.md)

### Category Bundles (6)

- **core-3d-animation** - Three.js, GSAP, R3F, Motion, Babylon.js (5 skills, 9 commands, 6 agents)
- **extended-3d-scroll** - A-Frame, Vanta, PlayCanvas, PixiJS, Locomotive, Barba (6 skills, 12 commands, 7 agents)
- **animation-components** - React Spring, Magic UI, AOS, Anime.js, Lottie (5 skills, 10 commands, 6 agents)
- **authoring-motion** - Blender, Spline, Rive, Substance 3D (4 skills, 10 commands, 5 agents)
- **meta-skills** - Integration patterns, Modern design (2 skills, 4 commands, 3 agents)
- **native-html5-stack** - HTMX, Web Animations API, HTML5 Native Design (3 skills, 4 commands, 3 agents)

## Available Skills

### Core 3D & Animation (5)
**threejs-webgl** • **gsap-scrolltrigger** • **react-three-fiber** • **motion-framer** • **babylonjs-engine**

### Extended 3D & Scroll (6)
**aframe-webxr** • **lightweight-3d-effects** • **playcanvas-engine** • **pixijs-2d** • **locomotive-scroll** • **barba-js**

### Animation & Components (5)
**react-spring-physics** • **animated-component-libraries** • **scroll-reveal-libraries** • **animejs** • **lottie-animations**

### 3D Authoring & Motion (4)
**blender-web-pipeline** • **spline-interactive** • **rive-interactive** • **substance-3d-texturing**

### Meta-Skills (2)
**web3d-integration-patterns** • **modern-web-design**

### Native HTML5 & Motion (3)
**htmx** • **web-animations-api** • **html5-native-design** — The no-framework stack for beautiful sites. HTMX 2.x for server-driven interactivity, the Web Animations API (WAAPI + CSS scroll-driven animations + View Transitions) for native motion, and modern HTML5 elements (Popover, `<dialog>`, container queries, `:has()`, Web Components) for the UI primitives.

## Documented Library Versions

Each skill is maintained against the version listed below (audit date
**2026-09-23**). v3 patterns are retained in migration sections where
they exist; the **current** API is what the main examples use.

| Skill | Library | Version |
|---|---|---|
| `threejs-webgl` | three | 0.186.0 / r186 |
| `gsap-scrolltrigger` | gsap | 3.15.0 |
| `react-three-fiber` | @react-three/fiber | 9.8.0 (React 19) |
| `motion-framer` | motion / motion/react | 13.4.1 |
| `babylonjs-engine` | @babylonjs/core | 9.27.1 |
| `aframe-webxr` | a-frame / aframe-extras | 1.8.0 / 7.7.0 |
| `lightweight-3d-effects` | zdog / vanta / vanilla-tilt | 1.1.1 / 0.5.24 / 1.8.1 |
| `playcanvas-engine` | playcanvas | 2.22.4 |
| `locomotive-scroll` | locomotive-scroll (Lenis) | 5.0.1 |
| `barba-js` | @barba/core | 2.10.3 |
| `react-spring-physics` | react-spring | 10.1.2 |
| `animated-component-libraries` | motion + Magic UI + React Bits | 13.4.1 |
| `scroll-reveal-libraries` | aos | 2.3.4 |
| `animejs` | animejs | 4.5.0 |
| `lottie-animations` | lottie-web / dotlottie-web | 5.13.0 / 0.80.0 |
| `blender-web-pipeline` | Blender | 5.2 LTS |
| `spline-interactive` | @splinetool/runtime / react-spline | 2.0.56 / 4.1.0 |
| `rive-interactive` | @rive-app/webgl2 | 2.43.0 |
| `htmx` | htmx.org | 2.0.x |
| `web-animations-api` | browser-native (WAAPI / CSS scroll-driven / View Transitions) | — |
| `html5-native-design` | browser-native (Popover / `<dialog>` / container queries / Web Components) | — |
| `web3d-integration-patterns` | meta-skill (matrix of all the above) | — |
| `modern-web-design` | meta-skill | — |

The full audit plan lives in [`FRAMEWORK_SKILL_UPDATE_PLAN.txt`](FRAMEWORK_SKILL_UPDATE_PLAN.txt). The new native-HTML5 stack ships with copies of the user's [`greysquirr3l/pattern_lab`](https://github.com/greysquirr3l/pattern_lab) reference examples in each skill's `assets/groundtruth/`.

## Installation

**Prerequisites**: Claude Code CLI or [claude.com/code](https://claude.com/code)

### Option 1: Plugin Marketplace (Recommended - New!)

Install directly from the marketplace:

```bash
# Add marketplace
/plugin marketplace add greysquirr3l/claudedesignskills

# Browse and install plugins
/plugin install threejs-webgl
/plugin install core-3d-animation  # Bundle: 5 skills + commands + agents
```

**Benefits**:
- ✅ One-command installation
- ✅ Includes slash commands for quick actions
- ✅ Specialized agents for domain expertise
- ✅ Automatic updates when repo updates
- ✅ Individual plugins or category bundles

### Option 2: Upload to claude.ai

Upload individual skills directly to [claude.ai](https://claude.ai):

1. Go to **Settings > Features > Skills**
2. Click **Upload skill**
3. Select any `.zip` file from `.claude/skills/`
4. Skill activates automatically when Claude detects relevant tasks

**All skills are properly packaged** with:
- ✅ SKILL.md at root level with valid YAML frontmatter
- ✅ No nested zip files
- ✅ Correct directory structure for claude.ai

### Option 3: Clone Repository (Development)

Clone for skill development or local customization:

```bash
git clone https://github.com/greysquirr3l/claudedesignskills.git
cd claudedesignskills
```

Skills auto-activate when triggered. Example prompts:
- "Create a Three.js scene with PBR materials" → `threejs-webgl`
- "Add GSAP scroll animations" → `gsap-scrolltrigger`
- "Build React Three Fiber component with physics" → `react-three-fiber`

### Option 4: Individual Skills (Local Projects)

Copy individual skills to your project:

```bash
# Extract skill contents (not the zip itself)
unzip .claude/skills/threejs-webgl.zip -d your-project/.claude/skills/threejs-webgl/
```

## Creating Skills

```bash
# Initialize new skill
.claude/skills/skill-creator/scripts/init_skill.py my-skill --path .claude/skills

# Validate
.claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/my-skill

# Package (auto-validates)
.claude/skills/skill-creator/scripts/package_skill.py .claude/skills/my-skill
```

### Packaging Requirements

All skills in this repository meet claude.ai upload requirements:

**Required ZIP Structure**:
```
skill-name.zip
├── SKILL.md              ← Must be at root level!
├── references/
│   └── api_reference.md
├── scripts/
│   └── helper_script.py
└── assets/
    └── templates/
```

**Automatic Validation**:
- `package_skill.py` ensures correct structure
- Skips `.zip` files to prevent nesting
- Places SKILL.md at root level (not in subdirectory)
- Validates YAML frontmatter before packaging

**Common Errors** (all fixed in this repo):
- ❌ SKILL.md inside subdirectory (e.g., `skill-name/SKILL.md`)
- ❌ Nested .zip files inside archive
- ❌ Missing or invalid YAML frontmatter

## Generator Scripts

Each skill includes automation utilities. Examples:

- **threejs-webgl**: `setup_scene.py` - Three.js boilerplate
- **react-three-fiber**: `component_generator.py` - 12 R3F component types
- **motion-framer**: `animation_generator.py` - 11 animation types
- **babylonjs-engine**: `scene_generator.py` - 8 scene types, `mesh_builder.py` - 13 shapes
- **gsap-scrolltrigger**: `generate_animation.py`, `timeline_builder.py`

50+ generators total across all skills.

## Repository Verification

```bash
# Count skills (should be 23)
ls -d .claude/skills/*/ | wc -l

# Count packages (should be 22)
find .claude/skills -name "*.zip" -type f | wc -l

# Validate all
for skill in .claude/skills/*/; do
  .claude/skills/skill-creator/scripts/quick_validate.py "$skill"
done
```

## Skill Relationships

**Foundation**: `threejs-webgl` (used by R3F, A-Frame, Vanta) • `gsap-scrolltrigger` (integrates with most) • `motion-framer` (used by component libs)

**Alternatives**: 3D (`threejs-webgl` vs `babylonjs-engine` vs `playcanvas-engine`) • Animation (`gsap` vs `motion` vs `react-spring`) • Scroll (`locomotive` vs `AOS`)

**Common Integrations**: Three.js + GSAP • R3F + Motion • Vanta + GSAP

## Contributing

1. Fork repo
2. Create/improve skill using `init_skill.py`
3. Follow [Claude Skills standards](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
4. Validate with `quick_validate.py`
5. Submit PR with packaged skill

**Guidelines**: Imperative form in SKILL.md • Runnable examples • Executable scripts (`chmod +x`) • Python 3 stdlib only • Proper YAML frontmatter

## Documentation

- **CLAUDE.md** - Repository guidance for Claude Code
- **Official Docs** - [Claude Skills guidelines](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- **Individual Skills** - Each SKILL.md contains detailed instructions

## License

MIT License - see [LICENSE](LICENSE) file

## Status

✅ **Production Ready** - All 25 skills complete, validated, and packaged
🏪 **Plugin Marketplace** - 31 plugins (25 individual + 6 bundles) ready to install
📦 **25 Skills** - 3D graphics, animation, scroll effects, interactive web, native HTML5
🔧 **60+ Commands** - Slash commands for instant boilerplate
🤖 **30+ Agents** - Specialized domain experts
📚 **Fully Documented** - Guides, patterns, examples
🚀 **Upload Ready** - All skills meet claude.ai packaging requirements

### Recent Updates

**2026-09-23**: Native HTML5 Stack & Pattern Lab Integration
- ✅ Added 3 new skills: **htmx** (HTMX 2.x hypermedia), **web-animations-api**
  (WAAPI + CSS scroll-driven + View Transitions), **html5-native-design**
  (Popover, `<dialog>`, container queries, `:has()`, Web Components).
- ✅ Added new bundle `native-html5-stack` (3 skills, 4 commands, 3 agents).
- ✅ Marketplace count: 25 individual plugins + 6 bundles (31 total).
- ✅ Integrated ground-truth examples from the user's
  `greysquirr3l/pattern_lab`: scroll-timeline lab, HTML5 APIs lab,
  2026 pattern lab, periodic table, nth-letter lab. Each new skill
  ships with the relevant subset under `assets/groundtruth/` and a
  `references/groundtruth.md` index with re-pull instructions.
- ✅ The **nth-letter lab** is highlighted in `modern-web-design` —
  12 pure-CSS typography effects (spectral hue via `oklch()`,
  kinetic wave, Solari flip, chromatic glitch, dust accumulation,
  …) that fake the still-unshipped `::nth-letter` pseudo-element
  with per-glyph wrappers + custom properties. Zero JS.

**2026-09-23**: Framework Skill Refresh (Priority 1–3)
- ✅ Audited all 21 framework skills against current package versions and
  official documentation; pixijs-2d already current, substance-3d-texturing
  unchanged
- ✅ **Priority 1 — major API migrations** (5 skills): animejs v4.5.0
  (`animate`, `createTimeline`, `stagger`, `createSpring`); locomotive-scroll
  v5.0.1/Lenis (`lenisOptions`, `resize`, official ScrollTrigger integration);
  threejs-webgl 0.186.0 (async WebGPURenderer, WebGL2 fallback, PCFShadowMap);
  playcanvas-engine 2.22.4 (`render` + `entity.render`, `anim` + state graphs,
  ESM `Script` subclasses, Ammo `WasmModule`); react-three-fiber 9.8.0 on
  React 19 (Canvas color-management props, named Zustand, experimental WebGPU)
- ✅ **Priority 2 — current API corrections** (11 skills): A-Frame 1.8.0 +
  aframe-extras 7.7.0, Babylon 9.27.1, Barba 2.10.3, GSAP 3.15.0
  (`gsap.matchMedia` replaces deprecated `ScrollTrigger.matchMedia`),
  Motion 13.4.1, react-spring 10.1.2, Rive 2.43.0, AOS 2.3.4 (replaces invalid
  `data-aos="fade-in"`), Spline runtime 2.0.56 / react 4.1.0, lottie-web 5.13.0
  + dotLottie split, animated-component-libraries (BlurText/CountUp fixes)
- ✅ **Priority 3 — meta and tooling** (4 skills): Blender 5.2 LTS, lightweight
  3D effects (Zdog 1.1.1 beta, Vanta 0.5.24, Vanilla-Tilt 1.8.1, Three 0.186.0),
  modern-web-design (FID → INP, March 2024 Core Web Vital), web3d-integration
  patterns (dated dependency matrix, framer-motion-3d quarantined with
  @react-spring/three replacement, real Three.js cleanup function)
- ✅ Quarantined deprecated APIs: `framer-motion-3d`, `data-aos="fade-in"`,
  `@next` install tags, `ScrollTrigger.matchMedia` as the primary example,
  `model`/`animation` PlayCanvas components, `anime({...})` /
  `anime.timeline()` / `anime.stagger()` defaults, v4 `data-scroll-container`
  markup as the default example, `FID` as an active metric
- ✅ All 22 skills pass `quick_validate.py`; all skill scripts pass
  `python3 -m py_compile`; `scripts/marketplace/validate_marketplace.py`
  passes; individual skill copies and bundle copies synchronised
- ✅ Detailed plan in `FRAMEWORK_SKILL_UPDATE_PLAN.txt`; commit `77ad005`

**2025-11-13**: Launched Plugin Marketplace
- ✅ Created 27 plugins (22 individual + 5 category bundles)
- ✅ Added 50+ slash commands for quick actions
- ✅ Created 27+ specialized agents for domain expertise
- ✅ Published marketplace.json for easy installation
- ✅ Full marketplace documentation in MARKETPLACE.md

**2025-10-25**: Fixed packaging script for claude.ai compatibility
- ✅ Corrected ZIP structure (SKILL.md at root level)
- ✅ Removed nested .zip files
- ✅ All 22 skills re-packaged with correct structure
- ✅ Verified upload compatibility with claude.ai

Built following [Anthropic's Claude Skills guidelines](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview).

**Ready to use**: Upload any skill to [claude.ai](https://claude.ai) or clone the repository!

---

**Star this repository** to stay updated with new skills and features!
