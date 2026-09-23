# PixiJS v8 API reference

Use this as a quick checklist, then verify signatures in the [release API docs](https://pixijs.download/release/docs/).

## Application

```ts
const app = new Application();
await app.init({
  width: 800,
  height: 600,
  background: 0x10151f,
  resolution: Math.min(window.devicePixelRatio, 2),
  autoDensity: true,
});
document.body.appendChild(app.canvas);
```

Key properties: `stage`, `renderer`, `canvas`, `screen`, and `ticker`. `Application.init()` is asynchronous in v8. Use `resizeTo` for a responsive canvas.

## Assets and textures

```ts
await Assets.init({ basePath: '/assets' });
const texture = await Assets.load<Texture>('hero.png');
const cached = Assets.get('hero');
await Assets.unload('hero');
```

Use aliases, manifests, bundles, and `Assets.backgroundLoad`/the documented background-loader route for larger applications. Textures now wrap loaded texture sources; `BaseTexture` is not a v8 application API.

## Display objects

- `Container`: hierarchy, transforms, child management.
- `Sprite`: one texture; `anchor`, `position`, `scale`, `rotation`, `tint`, `alpha`.
- `AnimatedSprite`: frame-texture animation.
- `TilingSprite`: repeating texture.
- `NineSliceSprite`: scalable panels.
- `Graphics`: vector paths and shapes.
- `Text`, `BitmapText`, `HTMLText`: text rendering options with different browser/performance trade-offs.
- `MeshSimple`, `MeshPlane`, `MeshRope`, `Mesh`: custom geometry and UVs.
- `ParticleContainer` plus `Particle`: lightweight high-volume sprites.

## Graphics

```ts
const shape = new Graphics()
  .roundRect(0, 0, 200, 100, 12)
  .fill({ color: 0x223044, alpha: 0.95 })
  .stroke({ width: 2, color: 0x6ea8fe });
```

Use `rect`, `circle`, `ellipse`, `roundRect`, `poly`, `star`, `moveTo`, `lineTo`, `closePath`, `fill`, `stroke`, and `cut`. The v7 `beginFill`/`endFill`, `drawRect`, `lineStyle`, and `beginHole` sequence should not be copied into v8 code.

## Events

```ts
view.eventMode = 'static';
view.cursor = 'pointer';
view.hitArea = new Rectangle(0, 0, 200, 80);
view.on('pointertap', handler);
```

Use `none`, `passive`, `static`, and `dynamic` deliberately. Prefer pointer events and clean up listeners with the scene lifecycle.

## Ticker

Use `deltaTime` for frame-normalized updates and `deltaMS` for seconds-based simulation. Remove callbacks when a screen is destroyed. Do not run a competing animation loop without a clear reason.

## Extensions and custom rendering

PixiJS v8 uses the extensions system and a systems/pipes renderer architecture. Optional imports use documented `pixi.js/*` entry points. For custom GPU code, verify the current `Shader.from`, `GlProgram`, `GpuProgram`, `Filter.from`, uniform, and resource signatures in the release docs. Test WebGL and WebGPU separately.

## Migration

- `@pixi/*` imports → `pixi.js` where using the v8 single-package layout.
- `new Application(options)` → `new Application(); await app.init(options)`.
- `app.view` → `app.canvas`.
- `Loader` → `Assets`.
- `BaseTexture` → texture-source APIs.
- v7 Graphics begin/end methods → v8 shape plus `fill`/`stroke`/`cut`.

## Lifecycle

Destroy an application on route/component teardown. Remove children before destroying reusable containers. Destroy generated textures and render textures when their owner is gone, and unload cached assets only after no live view references them.
