---
name: understand-metastack
description: "WHAT: metastack (the pydantic-stack-core / PSC library) — how to generate structured text (markdown, docs, blogs, READMEs, prompts, reports, code) by COMPOSING small TYPED pydantic pieces into a tree that renders itself recursively, instead of hand-rolling f-strings (which is how you get garbled/duplicated output). Three parts: RenderablePiece (a typed model that render()s itself), MetaStack (a list of pieces joined by a separator; pieces nest as typed fields), FractalPattern/FractalStage (a built-in template for staged transformations like Hero's Journey / AIDA). WHEN: when you need to generate or FIX any structured-text renderer (a blog, README, doc, prompt body, report); when output is garbled/duplicated because it was built with ad-hoc string concatenation; or when the user mentions metastack, pydantic-stack-core, PSC, RenderablePiece, MetaStack, FractalPattern, or composing renderable pieces (any of)."
---

# understand-metastack — compose typed pieces, never hand-roll f-strings

**The core idea:** structured text is a TREE of typed pieces, each of which knows how to render itself. You build the tree from small reusable pieces with full pydantic type-safety + validation, then call `.render()` once and it cascades. This is the opposite of one monolithic function full of f-strings — and it's why metastack output can't garble or duplicate: each datum lives in exactly one typed piece that renders exactly once.

Canonical source (read it if you need depth): `/tmp/core_libraries_to_publish/pydantic_stack_core/` — `pydantic_stack_core/core.py` (RenderablePiece, MetaStack), `fractal.py` (FractalStage, FractalPattern), `README.md`. Installed + importable: `from pydantic_stack_core import RenderablePiece, MetaStack, generate_output_from_metastack` and `from pydantic_stack_core import FractalStage, FractalPattern`.

## The 3 layers

1. **`RenderablePiece`** — a pydantic `BaseModel` with one abstract method `render() -> str`. The atom: a typed model that renders ITSELF.
   ```python
   class Title(RenderablePiece):
       text: str
       level: int = 1
       def render(self) -> str:
           return f"{'#' * self.level} {self.text}"
   ```
2. **`MetaStack`** — a container: `pieces: List[RenderablePiece]` + a `separator`; its `render()` joins each `piece.render()`. **The real power: a RenderablePiece can hold OTHER RenderablePieces as typed fields** → a recursive document tree; one `.render()` cascades through it.
   ```python
   class Section(RenderablePiece):
       title: str
       code_examples: List[CodeExample]      # NESTED typed pieces
       def render(self) -> str:
           body = "\n\n".join(e.render() for e in self.code_examples)
           return f"## {self.title}\n\n{body}"
   ```
3. **`FractalPattern` / `FractalStage`** (`fractal.py`) — a built-in template for any STAGED TRANSFORMATION (the docstring names **Hero's Journey** and **AIDA**). `FractalStage` = emoji/name/substages/`transformation_from`→`transformation_to`. Useful when your content IS a staged arc.

## Two usage modes
- **Library-in-code** (default, no dependencies beyond PSC): import the classes, compose, `.render()`. This is what the doc-mirror framework pipeline uses.
- **MCP registry** (`mcp_server.py`): `register_metastack(name, class_path, domain/tags/defaults…)` once, then `render_metastack(name, content)` / `render_to_file` / `append_from` — agent-accessible reusable templates by name. Needs the metastack MCP connected + a HEAVEN registry. Use when you want named, reusable, agent-callable templates.

## The pattern to follow (and the anti-pattern to kill)
- **DO:** decompose the output into small typed pieces (one per logical block), give each a trivially-correct `render()`, compose them in a `MetaStack`. Each field appears in ONE piece.
- **DON'T:** write one big `render()` that string-splices everything (e.g. `accomplishment.split('now')[1]` for a hook, or printing the same field in two places). That monolith is exactly where garbled hooks and duplicated paragraphs come from. If you inherit one, rebuild it as pieces.

## Worked example in this repo
`integration/cave-discord-fork/framework_render.py` is a real metastack rebuild: a framework blog as `Title / Hook / StoryArc / KeyInsight / Demo / WhyThisMatters / UniversalApplication / Links` pieces composed in `FrameworkBlog(MetaStack)`, built by `framework_blog_from_core(core)`. It replaced a hand-rolled `BlogPost` whose f-string `render()` garbled the hook and double-rendered a field — the rebuild makes both bugs structurally impossible. `JourneyCore` (`core.py`) stays a plain pydantic DATA container that FEEDS the renderer.

## Where to reach for it
Blogs, chapters, READMEs, doc(m)/SYSTEM diagrams, prompt bodies (a prompt = `Role`/`Inputs`/`Steps`/`Constraints`/`Report` pieces), reports, generated code — anything that is structured text assembled from parts. Compose pieces; don't concatenate strings.
