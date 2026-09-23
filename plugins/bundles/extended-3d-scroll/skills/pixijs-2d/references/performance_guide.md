# PixiJS v8 performance guide

Profile before changing architecture. Measure frame time, draw calls, texture memory, upload time, and CPU scripting time on target devices.

## Rendering cost

- Keep texture sources and blend modes consistent to preserve batching.
- Use atlases for related sprites and avoid needless texture switches.
- Bound high-DPI `resolution`; doubling resolution is roughly four times the pixel workload.
- Minimize filters, masks, render-to-texture passes, and large filter areas.
- Cull off-screen content and provide explicit bounds where automatic bounds are expensive.
- Test WebGL and WebGPU independently.

## Object strategy

Reuse sprites, arrays, graphics contexts, and render textures in hot paths. Pool bullets, particles, and transient effects instead of allocating them every tick. Use `ParticleContainer` only for lightweight, similarly textured particles; it does not support the complete display-object feature set.

Mark only animated fields in `ParticleContainer.dynamicProperties`. After bulk changes to static particle fields, call the documented `update()` path. Use `BitmapText` for large, frequently changing text when its font workflow fits the product.

## Memory and lifecycle

Destroy applications, scene subtrees, generated textures, and render textures at their ownership boundary. `Assets.unload` removes a cached asset; it does not make live sprites safe. Do not copy v7 `baseTexture` destruction or mutation patterns into v8 code.

## Profiling checklist

1. Reproduce on a representative device and renderer.
2. Record baseline FPS/frame time and GPU/CPU breakdown.
3. Change one variable: resolution, filter area, culling, batching, or object count.
4. Re-measure startup, steady state, resize, tab resume, and scene teardown.
5. Keep the simpler design unless the measured improvement is meaningful.
