# PixiJS v8 filters and effects

Use effects on the smallest practical subtree and measure the extra render passes. Verify filter constructor options in the [release API docs](https://pixijs.download/release/docs/).

## Built-in filters

Common filters include `BlurFilter`, `ColorMatrixFilter`, `DisplacementFilter`, `AlphaFilter`, `NoiseFilter`, and `FXAAFilter`. Import them from `pixi.js` in the default build or from a documented optional entry point in a custom build.

```ts
const blur = new BlurFilter({ strength: 4 });
sprite.filters = [blur];
sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);
```

Avoid filters on a full-screen container when a smaller target is sufficient. Clear `filters` when an effect is no longer needed.

## Displacement

Use a loaded texture sprite as the displacement source and keep its dimensions and lifecycle explicit. Do not mutate a v7 `texture.baseTexture` property; configure the source/options documented for the installed v8 release.

## Custom filters

Prefer `Filter.from` or the current `GlProgram`/`GpuProgram` APIs rather than copying old shader constructors. Keep GLSL and WGSL variants separate when WebGPU support matters. Test premultiplied alpha, coordinate origin, precision, uniform names, and device loss.

## Alternatives

For a repeated static effect, generate a texture once. For animation, update uniforms or a stable displacement source rather than rebuilding display objects. Use `Graphics` for simple vector geometry and DOM/CSS for effects that do not need canvas composition.
