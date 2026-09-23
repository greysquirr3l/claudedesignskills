# PixiJS examples

This directory is a resource index, not a duplicate of the official example suite. Use the [official PixiJS v8 examples](https://pixijs.com/8.x/examples) for runnable, release-matched demos.

Useful example families to inspect:

- Application initialization, resize, and renderer preferences
- Assets, manifests, bundles, spritesheets, fonts, and video textures
- Containers, sprites, animated sprites, tiling sprites, and nine-slice UI
- Graphics paths, fills, strokes, cuts, gradients, patterns, and SVG
- Text, BitmapText, HTMLText, masks, filters, and blend modes
- Pointer events, drag interactions, hit areas, and accessibility
- Meshes, render textures, custom shaders, and WebGL/WebGPU differences
- ParticleContainer, culling, batching, and performance profiling

When adapting an example, check the project’s installed `pixi.js` version and keep the v8 lifecycle rule: construct `Application`, await `app.init(options)`, then use `app.canvas`.
