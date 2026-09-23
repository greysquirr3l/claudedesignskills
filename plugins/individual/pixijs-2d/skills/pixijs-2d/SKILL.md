---
name: pixijs-2d
description: "PixiJS v8 development for high-performance 2D web graphics, games, interactive canvases, data visualizations, and UI overlays. Use for PixiJS, pixi.js, Application.init, WebGL/WebGPU rendering, Assets, sprites, containers, Graphics, text, meshes, particles, events, filters, shaders, accessibility, performance, project setup, or v7-to-v8 migrations."
---

# PixiJS v8

Use this skill for current PixiJS work. Prefer the single `pixi.js` package and v8 APIs. PixiJS is a 2D scene-graph renderer with WebGL and WebGPU backends; it is not a DOM layout system or a 3D engine.

## Operating rules

1. Inspect the project’s installed `pixi.js` version before writing code. If the version is not v8, decide explicitly whether to preserve the project’s API or migrate it.
2. Consult the [official guides](https://pixijs.com/8.x/guides) and the [release API reference](https://pixijs.download/release/docs/) for APIs not covered here. PixiJS evolves quickly; do not invent option names from memory.
3. Use TypeScript types when available. Keep renderer, asset, scene, input, and application-lifecycle concerns separate.
4. Treat canvas dimensions, CSS dimensions, device-pixel resolution, and world coordinates as different concepts. Decide how resizing and high-DPI rendering work before positioning content.
5. Destroy views, textures, render textures, and applications when their owning screen or route is removed. Do not use `Assets.unload` while live sprites still reference the asset.

## Start with a minimal v8 application

PixiJS v8 constructs synchronously but initializes asynchronously. Put all renderer-dependent work after `await app.init()`.

```ts
import { Application, Assets, Sprite } from 'pixi.js';

const app = new Application();
await app.init({
  resizeTo: window,
  background: '#10151f',
  antialias: true,
  resolution: Math.min(window.devicePixelRatio, 2),
  autoDensity: true,
});
document.body.appendChild(app.canvas);

const texture = await Assets.load('/assets/hero.png');
const hero = new Sprite(texture);
hero.anchor.set(0.5);
hero.position.set(app.screen.width / 2, app.screen.height / 2);
app.stage.addChild(hero);

app.ticker.add((ticker) => {
  hero.rotation += 0.01 * ticker.deltaTime;
});
```

For a fixed-size canvas, pass `width` and `height`; for a responsive canvas, use `resizeTo` and lay out from `app.screen`. Prefer `background` in new code; `backgroundColor` remains a supported alias in the v8 guide. Choose `preference: 'webgpu'` only when the project has tested its browser and shader requirements; WebGL is the safer default.

### Project setup

- Use the project’s existing bundler and install `pixi.js` once. Do not mix v7 `@pixi/*` packages with v8 unless a documented compatibility constraint requires it.
- Use the official [create-pixi](https://pixijs.com/8.x/guides/getting-started/quick-start) scaffolder for a new project when the repository has no established app structure.
- In React, Vue, or Svelte, create and initialize PixiJS in the framework lifecycle, append `app.canvas` once, and destroy the app on unmount. Keep application state in the framework and rendering state in PixiJS.
- In SSR, do not initialize a renderer during server rendering. Dynamically import or initialize on the client, and use the documented `DOMAdapter`/environment route for workers or non-browser hosts.

## Assets and textures

Use the Promise-based, cache-aware `Assets` API. Load before creating sprites that need the texture.

```ts
import { Assets, Sprite, Texture } from 'pixi.js';

await Assets.init({ basePath: '/assets' });
const texture = await Assets.load<Texture>('hero.png');
const sprite = new Sprite(texture);
```

- Use aliases for stable application-level names: `Assets.load({ alias: 'hero', src: 'hero.png' })`, then `Assets.get('hero')`.
- Use a manifest and named bundles for screens or routes. Load the next bundle in the background and unload a bundle only after its scene is destroyed.
- Loading the same URL or alias is cached; do not add a second ad-hoc loader.
- Use `Assets.unload` for lifecycle cleanup, not as a general texture reset. Destroy generated textures and render textures explicitly when they are no longer needed.
- Use built-in loaders for images, SVG, video, spritesheets, bitmap fonts, web fonts, JSON, text, and supported compressed textures. Add a parser/resolver only for a required custom format.
- Keep URLs and aliases stable across code and manifests. Add error handling around preload boundaries and show a recoverable loading state.

## Scene graph and transforms

`app.stage` is the root `Container`. Containers group children and provide transforms; `Sprite`, `Graphics`, `Text`, `Mesh`, and `Particle` are leaves or specialized render objects.

- Build a shallow, meaningful hierarchy: world, camera/world transform, layers, UI, and debug overlays.
- Use `position`, `scale`, `rotation`, `skew`, and `pivot` consistently. Prefer `pivot` for the point around which an object rotates and `anchor` for sprite/texture-relative placement.
- Use `zIndex` with `sortableChildren = true` only where ordering is genuinely dynamic; otherwise add children in render order.
- Use `toGlobal`/`toLocal` for coordinate conversion rather than manually undoing parent transforms.
- Use `getBounds`/`getLocalBounds` for layout and hit testing only when needed; repeated bounds calculations can be expensive.
- Remove a child before destroying it when a container should remain reusable. Destroy with documented options when a subtree owns its textures.
- Use render groups or culling intentionally. They can improve large scenes but may add render passes or batching costs.

## Sprites and animation

Use `Sprite` for a single texture, `AnimatedSprite` for frame animation, `TilingSprite` for repeating backgrounds, and `NineSliceSprite` for scalable panels. For frame animation, keep frame textures in an atlas and control `animationSpeed`, `loop`, `play`, `stop`, and `gotoAndStop` from one owner. Do not recreate sprites every tick.

```ts
const atlas = await Assets.load('run.json');
const player = new AnimatedSprite(atlas.animations.run);
player.anchor.set(0.5);
player.animationSpeed = 0.15;
player.play();
```

## Graphics and generated textures

PixiJS v8’s Graphics API builds a shape first and then applies `fill`, `stroke`, or `cut`.

```ts
const card = new Graphics()
  .roundRect(0, 0, 280, 120, 16)
  .fill({ color: 0x182234, alpha: 0.96 })
  .stroke({ width: 2, color: 0x6ea8fe });
```

Use v8 names such as `rect`, `circle`, `ellipse`, `roundRect`, `poly`, and `star`. Replace v7 patterns such as `beginFill`, `endFill`, `drawRect`, `lineStyle`, and `beginHole` with `fill`, `stroke`, shape methods, and `cut`. Reuse a `GraphicsContext` when many objects share the same geometry. Generate a texture from stable graphics only when rasterization improves batching or reuse; do not regenerate it every frame.

## Text, masks, filters, and blend modes

- Use `Text` for flexible styled text, `BitmapText` for large amounts of frequently changing text, and `HTMLText` only when its browser and accessibility trade-offs are acceptable.
- Load bitmap/web fonts before measuring or laying out text. Avoid changing expensive text styles every frame.
- Use masks and filters on the smallest practical subtree. Set a tight `filterArea` when the bounds are known.
- Prefer built-in filters for common effects. For custom GPU work, use the v8 shader/filter APIs and test both WebGL and WebGPU if both are supported.
- Advanced blend modes and optional extensions may require an explicit `pixi.js/*` import. Register extensions before initialization when the documented API requires it.
- Do not assume a filter, blend mode, or text extension is included in a custom build. Verify the import path against the release docs.

## Interaction and accessibility

PixiJS v8 uses federated events. Set the minimum event mode needed and define a `hitArea` when the visual bounds are not the intended target.

```ts
button.eventMode = 'static';
button.cursor = 'pointer';
button.hitArea = new Rectangle(0, 0, 220, 64);
button.on('pointertap', onActivate);
```

- Use `eventMode: 'none'` for decorative subtrees, `'passive'` for transparent containers, `'static'` for interactive objects, and `'dynamic'` only when an object needs interaction while moving.
- Prefer pointer events so mouse, pen, and touch share a path. Capture the active pointer for drag behavior and clean up listeners.
- Do not rely on a canvas-only control for critical actions. Pair important interactions with accessible DOM controls or use PixiJS accessibility support with labels, roles, `tabIndex`, and keyboard handlers.
- Keep focus, hover, pressed, and disabled states visible without color alone. Respect reduced-motion and keyboard navigation requirements.

## Ticker and game loops

Use `ticker.deltaTime` or `ticker.deltaMS` so motion is frame-rate independent. Keep simulation time separate from render time when determinism matters.

```ts
app.ticker.add((ticker) => {
  const seconds = ticker.deltaMS / 1000;
  player.x += velocity.x * seconds;
});
```

Remove ticker callbacks when their scene is destroyed. Use a fixed-step accumulator for physics, cap large time steps after tab suspension, and avoid starting a second `requestAnimationFrame` loop that competes with the application ticker. Set `maxFPS` or `minFPS` only for a measured requirement.

## Particle systems and meshes

Use `ParticleContainer` with `Particle` for very large numbers of lightweight, similarly textured particles. It is not a drop-in replacement for `Container`: particles do not provide the full display-object feature set, events, filters, or arbitrary child hierarchy. Mark only animated fields in `dynamicProperties` and call `update()` after bulk changes to static fields.

Use `MeshSimple`, `MeshPlane`, `MeshRope`, or a custom `Mesh` when geometry or UVs—not a sprite transform—is the core problem. Keep geometry buffers stable and update only changing attributes.

## Rendering, shaders, and extensions

- Start with the default renderer and measure. Use `preference`, renderer options, and custom builds only for a demonstrated need.
- PixiJS v8 uses an extensions system. For custom application plugins, implement `init`/`destroy`, declare `ExtensionType.Application`, register with `extensions.add`, and augment `PixiMixins.ApplicationOptions` when adding typed options.
- In custom builds, import required extensions explicitly and use the documented `skipExtensionImports` option. Be careful with text, events, filters, compressed textures, and `unsafe-eval` imports.
- Use `Shader.from`, `GlProgram`/`GpuProgram`, and `Filter.from` only after checking the current API reference. Keep GLSL and WGSL source separate when portability is required; test uniform layout, coordinate origin, premultiplied alpha, and precision.
- For render-to-texture, track render-texture size, resolution, color space, and lifecycle. Reuse temporary targets through the documented pool where appropriate.

## Performance checklist

1. Profile frame time, draw calls, texture memory, upload time, and CPU scripting time before optimizing.
2. Use atlases and consistent texture sources to preserve batching. Avoid needless texture switches, filters, masks, and blend-mode changes.
3. Reuse objects and arrays in hot loops. Prefer pooling for bullets, particles, and transient effects.
4. Keep resolution bounded on high-DPI screens; a doubled resolution is roughly four times the pixel workload.
5. Cull objects outside the camera and set explicit bounds where automatic bounds are costly.
6. Use `BitmapText`, `ParticleContainer`, cached textures, render groups, or render bundles only when measurements show a benefit.
7. Tune texture garbage collection and call destroy deliberately. GPU memory is not released merely because a JavaScript reference disappeared.
8. Test WebGL and WebGPU separately. A feature working on one backend is not proof of portability.

## v7-to-v8 migration checklist

- Replace `@pixi/*` imports with `pixi.js` imports where moving to the v8 single-package layout.
- Change `new Application(options)` to `const app = new Application(); await app.init(options);`.
- Replace `app.view` with `app.canvas`.
- Replace `Loader` patterns with `Assets`.
- Replace `BaseTexture` usage with the v8 texture-source model; textures expect loaded resources.
- Replace old Graphics begin/end APIs and long shape names with v8 shape, `fill`, `stroke`, and `cut` calls.
- Recheck `ParticleContainer`, filters, events, text, mesh, and extension imports against v8 docs rather than applying mechanical renames.
- Audit third-party Pixi libraries before upgrading; an un-migrated dependency can be a reason to defer the upgrade.

## Troubleshooting

- **Blank canvas:** verify `await app.init()`, append `app.canvas`, inspect renderer/context errors, and check that the asset promise resolved.
- **Wrong scale or blurry output:** separate CSS size from renderer size, configure `resolution`/`autoDensity`, and avoid scaling the canvas twice.
- **Clicks miss:** set `eventMode`, check ancestor event modes, define `hitArea`, and verify coordinate conversion.
- **Unexpected draw cost:** inspect filters, masks, render textures, texture switches, resolution, and object count before changing the renderer.
- **WebGPU-only failure:** retry with WebGL, check browser support, shader language, optional extensions, and adapter/device errors.
- **Asset memory growth:** stop retaining scene objects, unload only after destruction, destroy generated targets, and verify aliases do not keep stale references.

## Official references

- [PixiJS getting started](https://pixijs.com/8.x/guides/getting-started/intro)
- [Application](https://pixijs.com/8.x/guides/components/application)
- [Assets](https://pixijs.com/8.x/guides/components/assets)
- [v8 migration guide](https://pixijs.com/8.x/guides/migrations/v8)
- [Official PixiJS skills](https://github.com/pixijs/pixijs-skills)
- [Release API docs](https://pixijs.download/release/docs/)

## Related skills

- **threejs-webgl** or **react-three-fiber** for 3D scenes.
- **gsap-scrolltrigger** or **motion-framer** for timeline and UI animation around a PixiJS canvas.
- **barba-js** for route transitions; destroy and recreate PixiJS applications at route boundaries.
- **web3d-integration-patterns** when combining canvas rendering with broader 3D experiences.

## Bundled resources

- `references/api_reference.md` - compact v8 API and migration checklist.
- `references/filters_effects.md` - filter and shader patterns.
- `references/performance_guide.md` - profiling and optimization notes.
- `assets/starter_pixijs/` - minimal starter project.
- `assets/examples/` - resource index; use the official examples site for live examples.
- `scripts/particle_builder.py` and `scripts/sprite_generator.py` - generators that emit v8-compatible examples.
