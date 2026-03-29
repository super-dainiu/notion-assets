# notion-assets

Image assets for Daniel's Notion workspace. Any agent (Claude Code, Codex, etc.) can upload images here and reference them in Notion pages via raw GitHub URLs.

## URL Pattern

```
https://raw.githubusercontent.com/super-dainiu/notion-assets/main/<path>
```

## Directory Structure

```
notion-assets/
├── papers/          # Figures from papers discussed in Paper Reading & Ideas
│   └── {paper-slug}/
│       └── fig1.png
├── research/        # Figures for active research projects (LogiCL, Pop-Corn, etc.)
│   └── {project-slug}/
│       └── experiment_result.png
├── ideas/           # Diagrams and sketches for idea pages
│   └── {idea-slug}/
│       └── diagram.png
└── misc/            # Anything else
```

## Naming Convention

- **Paper figures**: `papers/{first-author}{year}_{short-title}/fig{N}.png`
  - e.g. `papers/richter2026_compositional-fm/fig1.png`
- **Research figures**: `research/{project}/desc.png`
  - e.g. `research/logicl/prop3_ablation.png`
- **Idea diagrams**: `ideas/{idea-slug}/diagram.png`

## How Agents Use This

1. Upload image to the appropriate directory in this repo
2. Get raw URL: `https://raw.githubusercontent.com/Daniel-Shao/notion-assets/main/papers/richter2026_compositional-fm/fig1.png`
3. Insert into Notion page content using Notion MCP: `![Figure 1](url)`
4. Or set as page cover/icon via the Notion API

## Notion Workspace Reference

- **Memory Hub**: `331a446f8d0f814b8942dc1e8ef41a46`
- **Research**: `331a446f8d0f81f1a36fcdc73529a9a2`
- **Paper Reading & Ideas**: `331a446f8d0f81e897dbf00c8e765eff`
- **Workspace**: `331a446f8d0f81dd9969e41f52d578a8`

See the Memory Hub in Notion for the full page ID directory.
