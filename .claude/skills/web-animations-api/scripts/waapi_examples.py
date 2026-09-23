#!/usr/bin/env python3
"""Web Animations API example generator.

Generates 18 stand-alone HTML + CSS + JS examples for the Web
Animations API, CSS scroll-driven animations, and the View
Transitions API. Most generate a minimal demo page that runs in
any modern browser.

Usage:
    ./waapi_examples.py                          # interactive picker
    ./waapi_examples.py --pattern basic-reveal   # print one to stdout
    ./waapi_examples.py --all                    # dump all to ./out/
    ./waapi_examples.py --list                   # list names
    ./waapi_examples.py --animate-with css       # show only CSS patterns
                                                 # (script animates CSS-driven)

Patterns: basic-reveal, stagger, spring-ish, scrubable, dialog-open,
hover-lift, accordion, swipe-dismiss, morph-vt, scroll-driven-reveal,
reading-progress, headline-shrink, parallax-bg, vt-same-doc, vt-cross-doc,
vt-image-grid, reduced-motion, rAF-leaderboard.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

DOC_TPL = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{style}</style>
</head>
<body>
{body}
<script>
{script}
</script>
</body>
</html>
"""


def _emit(title: str, style: str, body: str, script: str) -> str:
    return DOC_TPL.format(title=title, style=style, body=body, script=script)


# ----------------- WAAPI patterns -------------------------------------------


def basic_reveal() -> str:
    body = """
<article class="card">
  <h1>Hello, motion.</h1>
  <p>Element.animate() is alive.</p>
  <button id="replay">Replay</button>
</article>
"""
    style = """
:root { color-scheme: light dark; font: 16px/1.55 system-ui; padding: 2rem; }
body { background: #fafafa; color: #1a1a1a; max-width: 540px; margin: 0 auto; }
.card { padding: 2rem; border: 1px solid #eee; border-radius: .75rem; background: #fff; }
button { padding: .5rem 1rem; border: 1px solid #ddd; background: #f5f5f5;
         border-radius: .375rem; cursor: pointer; margin-top: 1rem; }
"""
    script = """
const card = document.querySelector('.card')

function play() {
  card.animate(
    [
      { opacity: 0, transform: 'translateY(24px) scale(.985)' },
      { opacity: 1, transform: 'none' }
    ],
    { duration: 480, easing: 'cubic-bezier(.2, .8, .2, 1)', fill: 'both' }
  )
}

play()
document.getElementById('replay').addEventListener('click', play)
"""
    return _emit("basic-reveal", style, body, script)


def stagger() -> str:
    body = """
<ul class="list">
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
  <li>Date</li>
  <li>Elderberry</li>
</ul>
<button id="replay">Replay stagger</button>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; }
.list { list-style: none; padding: 0; }
.list li { padding: .75rem 1rem; border: 1px solid #eee; border-radius: .5rem;
           margin-bottom: .5rem; background: #f9f9f9; opacity: 0; }
button { margin-top: 1rem; padding: .5rem 1rem; cursor: pointer; }
"""
    script = """
function play() {
  document.querySelectorAll('.list li').forEach((el, i) => {
    el.animate(
      [{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'none' }],
      { duration: 360, delay: i * 80, easing: 'cubic-bezier(.2, .8, .2, 1)', fill: 'backwards' }
    )
  })
}
play()
document.getElementById('replay').addEventListener('click', play)
"""
    return _emit("stagger", style, body, script)


def spring_ish() -> str:
    body = """
<div class="dot" id="dot"></div>
<p>Click to bounce (low-stiffness spring).</p>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; text-align: center; padding-top: 4rem; }
.dot { width: 80px; height: 80px; border-radius: 50%; margin: 0 auto;
       background: linear-gradient(135deg, #06b6d4, #8b5cf6); }
"""
    script = """
const dot = document.getElementById('dot')
// Spring-like easing (Bezier approximation; not a true spring but close).
const SPRING = 'cubic-bezier(.34, 1.56, .64, 1)'

dot.addEventListener('click', () => {
  const r = dot.getBoundingClientRect()
  const dx = (Math.random() - .5) * 240
  const dy = (Math.random() - .5) * 240
  dot.animate(
    [{ transform: 'translate(0,0)' }, { transform: `translate(${dx}px, ${dy}px)` }],
    { duration: 520, easing: SPRING, fill: 'backwards' }
  )
  // Bounce back
  setTimeout(() => {
    dot.animate(
      [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'translate(0,0)' }],
      { duration: 640, easing: SPRING, fill: 'forwards' }
    )
  }, 540)
})

@media (prefers-reduced-motion: reduce) {
  .dot { transition: none; }
}
"""
    return _emit("spring-ish", style, body, script)


def scrubable() -> str:
    body = """
<p class="note">Drag the slider to scrub the box's rotation.</p>
<input id="slider" type="range" min="0" max="1000" value="0" style="width:100%">
<div id="box" class="box"></div>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
.box { width: 80px; height: 80px; background: linear-gradient(135deg, #06b6d4, #8b5cf6);
       margin: 2rem auto; border-radius: .5rem; }
.note { opacity: .6; }
"""
    script = """
const box = document.getElementById('box')
const anim = box.animate(
  [{ transform: 'rotate(0)' }, { transform: 'rotate(360deg)' }],
  { duration: 1000, fill: 'forwards' }
)
anim.pause()

document.getElementById('slider').addEventListener('input', (e) => {
  anim.currentTime = Number(e.target.value)
})
"""
    return _emit("scrubable", style, body, script)


def dialog_open() -> str:
    body = """
<button id="open">Open settings</button>
<dialog id="settings">
  <h2>Settings</h2>
  <p>Animation-driven open/close.</p>
  <form method="dialog">
    <button>Close</button>
  </form>
</dialog>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
button { padding: .5rem 1rem; cursor: pointer; }
dialog { border: 1px solid #ddd; border-radius: .75rem; padding: 1.5rem; min-width: 320px;
         background: #fff; color: #1a1a1a; }
dialog::backdrop { background: transparent; }
"""
    script = """
const dlg = document.getElementById('settings')

dlg.addEventListener('open', () => {
  dlg.animate(
    [{ opacity: 0, transform: 'translateY(40px) scale(.96)' },
     { opacity: 1, transform: 'none' }],
    { duration: 240, easing: 'cubic-bezier(.2, .8, .2, 1)', fill: 'backwards' }
  )
  dlg.backdrop.animate(
    [{ opacity: 0 }, { opacity: 1 }],
    { duration: 240, fill: 'backwards' }
  )
})
dlg.addEventListener('close', () => {
  dlg.animate(
    [{ transform: 'none' }, { transform: 'translateY(20px) scale(.96)', opacity: 0 }],
    { duration: 200, fill: 'forwards' }
  )
})

document.getElementById('open').addEventListener('click', () => dlg.showModal())
"""
    return _emit("dialog-open", style, body, script)


def hover_lift() -> str:
    body = """
<div class="grid">
  <div class="card">Hover me</div>
  <div class="card">And me</div>
  <div class="card">And me</div>
</div>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 720px; margin: 0 auto; padding-top: 4rem; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.card { aspect-ratio: 1; border-radius: .75rem; background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: white; display: grid; place-items: center; cursor: pointer;
        will-change: transform; }
"""
    script = """
document.querySelectorAll('.card').forEach((el) => {
  el.addEventListener('pointerenter', () => {
    el.animate(
      [{ transform: 'translateY(0) scale(1)' },
       { transform: 'translateY(-8px) scale(1.02)' }],
      { duration: 220, easing: 'cubic-bezier(.2, .8, .2, 1)', fill: 'forwards' }
    )
  })
  el.addEventListener('pointerleave', () => {
    el.animate(
      [{ transform: 'translateY(-8px) scale(1.02)' },
       { transform: 'translateY(0) scale(1)' }],
      { duration: 220, easing: 'cubic-bezier(.2, .8, .2, 1)', fill: 'forwards' }
    )
  })
})
"""
    return _emit("hover-lift", style, body, script)


def accordion() -> str:
    body = """
<details>
  <summary>What is WAAPI?</summary>
  <p>Element.animate() — the browser's built-in animation runtime.</p>
</details>
<details>
  <summary>What about scrolling?</summary>
  <p>Use CSS animation-timeline: scroll() — pure CSS scroll-driven motion.</p>
</details>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
details { border: 1px solid #eee; border-radius: .5rem; padding: 1rem; margin-bottom: .5rem; overflow: hidden; }
summary { cursor: pointer; font-weight: 600; }
details > p { max-height: 0; opacity: 0; transform: translateY(-12px); }
details[open] > p { max-height: 320px; opacity: 1; transform: none; transition: all 320ms cubic-bezier(.2,.8,.2,1); }
"""
    script = "// CSS-only smooth accordion. (Try scroll-driven view() for an even slicker effect.)"
    return _emit("accordion", style, body, script)


def swipe_dismiss() -> str:
    body = """
<div class="card" id="card">
  <span>Swipe me away</span>
</div>
<button id="reset">Reset</button>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
.card { padding: 2rem; background: #06b6d4; color: white; border-radius: .75rem;
        cursor: grab; user-select: none; touch-action: none;
        will-change: transform, opacity; }
button { margin-top: 1rem; padding: .5rem 1rem; cursor: pointer; }
"""
    script = """
const card = document.getElementById('card')
let startX = 0, currentX = 0, dragging = false

card.addEventListener('pointerdown', (e) => {
  dragging = true; startX = e.clientX
  card.setPointerCapture(e.pointerId)
})
card.addEventListener('pointermove', (e) => {
  if (!dragging) return
  currentX = e.clientX - startX
  card.style.transform = `translateX(${currentX}px) rotate(${currentX / 12}deg)`
  card.style.opacity = String(Math.max(0, 1 - Math.abs(currentX) / 400))
})
card.addEventListener('pointerup', () => {
  dragging = false
  if (Math.abs(currentX) > 200) {
    card.animate(
      [{ transform: `translateX(${currentX}px) rotate(${currentX / 12}deg)`, opacity: card.style.opacity },
       { transform: `translateX(${currentX * 2}px) rotate(${currentX / 6}deg)`, opacity: 0 }],
      { duration: 220, easing: 'cubic-bezier(.4, 0, .6, 1)', fill: 'forwards' }
    ).finished.then(() => card.style.display = 'none')
  } else {
    card.animate(
      [{ transform: `translateX(${currentX}px)`, opacity: card.style.opacity },
       { transform: 'translateX(0)', opacity: 1 }],
      { duration: 220, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'forwards' }
    ).finished.then(() => {
      card.style.transform = ''; card.style.opacity = ''
    })
  }
  currentX = 0
})

document.getElementById('reset').addEventListener('click', () => {
  card.style.display = ''; card.style.transform = ''; card.style.opacity = ''
})
"""
    return _emit("swipe-dismiss", style, body, script)


def morph_vt() -> str:
    body = """
<button id="trigger" popovertarget="modal" popovertargetaction="show"
        style="view-transition-name: morph-target">Open modal</button>

<div id="modal" popover="manual"
     style="view-transition-name: morph-target;
            padding:1.5rem;border:1px solid #ddd;border-radius:.5rem;background:#fff;max-width:320px;
            box-shadow:0 8px 24px rgba(0,0,0,.1)">
  <h3>Morphed in!</h3>
  <p>Same view-transition-name on trigger and modal — the browser animates between them.</p>
  <button popovertarget="modal" popovertargetaction="hide">Close</button>
</div>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 4rem 2rem; max-width: 540px; margin: 0 auto; }
button { padding: .5rem 1rem; cursor: pointer; }

::view-transition-old(morph-target), ::view-transition-new(morph-target) {
  animation-duration: 320ms;
  animation-timing-function: cubic-bezier(.2, .8, .2, 1);
}
"""
    script = "// The view-transition-name CSS keyframes handle the morph automatically."
    return _emit("morph-vt", style, body, script)


# ----------------- CSS scroll-driven patterns --------------------------------


def scroll_driven_reveal() -> str:
    body = """
<main>
  <section class="vh"></section>
  <section class="vh reveal"></section>
  <section class="vh reveal"></section>
  <section class="vh reveal"></section>
</main>
"""
    style = """
body { margin: 0; }
.vh { min-height: 80vh; display: grid; place-items: center; font: 16px/1.55 system-ui; }
.reveal {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -.02em;
  animation: rise linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
@keyframes rise {
  from { opacity: 0; transform: translateY(80px); }
  to   { opacity: 1; transform: none; }
}

@supports not (animation-timeline: view()) {
  .reveal { animation: none; opacity: 1; }
}

@media (prefers-reduced-motion: reduce) { .reveal { animation: none } }
"""
    script = "// Pure CSS scroll-driven. No JavaScript required."
    return _emit("scroll-driven-reveal", style, body, script)


def reading_progress() -> str:
    body = """
<progress id="read"></progress>
<article>
  <h1>Long-form reading</h1>
  <p>Scroll the page — the bar at the top fills.</p>
  <p>…article body…</p>
  <p>…article body…</p>
  <p>…article body…</p>
  <p>…article body…</p>
  <p>…article body…</p>
</article>
"""
    style = """
body { margin: 0; font: 16px/1.55 system-ui; }
progress#read {
  position: fixed; top: 0; left: 0; right: 0; height: 4px;
  border: 0; background: transparent;
  animation: fill linear both;
  animation-timeline: scroll(root);
}
@keyframes fill {
  from { width: 0; }
  to   { width: 100vw; }
}
article { max-width: 640px; margin: 4rem auto; padding: 0 2rem; }
article p { margin: 1.5rem 0; }
@supports not (animation-timeline: scroll()) {
  progress#read { animation: none; display: none; }
}
"""
    script = "// Bar is pure CSS. Reads scroll(root) progress 0% → 100%."
    return _emit("reading-progress", style, body, script)


def headline_shrink() -> str:
    body = """
<header class="hero">
  <h1>Pin me</h1>
</header>
<main>
  <section class="content"><p>…scroll the page…</p></section>
  <section class="content"><p>…keep going…</p></section>
  <section class="content"><p>…notice the title shrink…</p></section>
</main>
"""
    style = """
body { margin: 0; font: 16px/1.55 system-ui; }
.hero {
  height: 80vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  color: white;
}
.hero h1 {
  font-size: clamp(3rem, 12vw, 8rem);
  letter-spacing: -.04em;
  font-weight: 800;
  animation: shrink linear both;
  animation-timeline: scroll(root);
  animation-range: 0 50vh;
}
@keyframes shrink {
  to {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    letter-spacing: -.02em;
  }
}
.content { padding: 4rem 2rem; max-width: 640px; margin: 0 auto; }

@supports not (animation-timeline: scroll()) {
  .hero h1 { animation: none; }
}
@media (prefers-reduced-motion: reduce) { .hero h1 { animation: none } }
"""
    script = "// Pure CSS scroll-bound animation."
    return _emit("headline-shrink", style, body, script)


def parallax_bg() -> str:
    body = """
<section class="bg"></section>
<section class="text">
  <h1>Scroll</h1>
  <p>The background translates 30px as you scroll — that's the whole trick.</p>
</section>
<section class="bg tall"></section>
<section class="text">
  <p>…and continues to translate.</p>
</section>
"""
    style = """
body { margin: 0; font: 16px/1.55 system-ui; }
.bg {
  height: 60vh;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6) center/cover no-repeat;
  will-change: transform;
  animation: shift linear both;
  animation-timeline: scroll(root);
  animation-range: 0 80vh;
}
.bg.tall { height: 100vh; }
@keyframes shift {
  from { transform: translateY(-20%); }
  to   { transform: translateY(20%); }
}
.text { max-width: 540px; margin: 0 auto; padding: 4rem 2rem; }

@supports not (animation-timeline: scroll()) {
  .bg { animation: none; }
}
@media (prefers-reduced-motion: reduce) { .bg { animation: none } }
"""
    script = "// No JS parallax — pure CSS scroll-driven animation."
    return _emit("parallax-bg", style, body, script)


def vt_same_doc() -> str:
    body = """
<main id="main">
  <h1 style="view-transition-name: title">Index</h1>
  <button id="go">Go to detail</button>
</main>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 4rem 2rem; max-width: 540px; margin: 0 auto; }
h1 { font-size: 4rem; letter-spacing: -.04em; font-weight: 800; }
button { padding: .5rem 1rem; cursor: pointer; }

::view-transition-old(title), ::view-transition-new(title) {
  animation-duration: 320ms;
  animation-timing-function: cubic-bezier(.2, .8, .2, 1);
}
"""
    script = """
const main = document.getElementById('main')

document.getElementById('go').addEventListener('click', async () => {
  if (!document.startViewTransition) {
    main.innerHTML = '<h1 style=\"view-transition-name: title\">Detail</h1>'
    return
  }
  document.startViewTransition(() => {
    main.innerHTML = '<h1 style=\"view-transition-name: title\">Detail</h1>'
  })
})
"""
    return _emit("vt-same-doc", style, body, script)


def vt_cross_doc() -> str:
    body = """
<main>
  <h1 style="view-transition-name: page-title">Index</h1>
  <p><a href="?page=detail">Go to detail</a></p>
</main>
"""
    style = """
@view-transition { navigation: auto; }
body { font: 16px/1.55 system-ui; padding: 4rem 2rem; max-width: 540px; margin: 0 auto; }
h1 { font-size: 4rem; letter-spacing: -.04em; font-weight: 800;
     view-transition-name: page-title; }
::view-transition-old(page-title),
::view-transition-new(page-title) {
  animation-duration: 320ms;
  animation-timing-function: cubic-bezier(.2,.8,.2,1);
}
"""
    script = "// Cross-document VT — supported in Chrome/Edge 126+; feature-detect."
    return _emit("vt-cross-doc", style, body, script)


def vt_image_grid() -> str:
    body = """
<h1>Image grid</h1>
<p>Click an image — it morphs into a full-width detail.</p>
<ul class="grid">
  <li style="view-transition-name: pic-1"><img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%2306b6d4'/></svg>" width="100%" alt=""></li>
  <li style="view-transition-name: pic-2"><img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%238b5cf6'/></svg>" width="100%" alt=""></li>
  <li style="view-transition-name: pic-3"><img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23f59e0b'/></svg>" width="100%" alt=""></li>
</ul>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 720px; margin: 0 auto; }
.grid { list-style: none; padding: 0; display: grid;
        grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.grid li { aspect-ratio: 1; border-radius: .5rem; overflow: hidden;
           cursor: pointer; transition: transform 220ms; }
.grid li:hover { transform: scale(1.02); }

::view-transition-group(*) {
  animation-duration: 320ms;
  animation-timing-function: cubic-bezier(.2,.8,.2,1);
}
"""
    script = """
// Adds a click handler — opens the image in a full-screen modal
// by giving it the new view-transition-name and starting a transition.
document.querySelectorAll('.grid li').forEach(li => {
  li.addEventListener('click', () => {
    if (!document.startViewTransition) return
    document.startViewTransition(() => {
      li.style.gridColumn = '1 / -1'
      li.style.aspectRatio = '16/9'
    })
  })
})
"""
    return _emit("vt-image-grid", style, body, script)


def reduced_motion() -> str:
    body = """
<p id="status">prefers-reduced-motion: <strong>?</strong></p>
<button id="bounce">Bounce</button>
<div id="dot" class="dot"></div>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
.dot { width: 50px; height: 50px; border-radius: 50%; background: #8b5cf6; margin-top: 1rem; }
button { padding: .5rem 1rem; cursor: pointer; }

@media (prefers-reduced-motion: reduce) { .dot { animation: none !important; } }
"""
    script = """
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
document.getElementById('status').innerHTML =
  `prefers-reduced-motion: <strong>${reduced}</strong>`

document.getElementById('bounce').addEventListener('click', () => {
  const dot = document.getElementById('dot')
  if (reduced) {
    dot.animate([{ opacity: 1 }, { opacity: 0.5 }, { opacity: 1 }],
                { duration: 200, iterations: 2 })
    return
  }
  dot.animate(
    [{ transform: 'translateY(0)' }, { transform: 'translateY(-200px)' },
     { transform: 'translateY(0)' }],
    { duration: 600, easing: 'cubic-bezier(.34, 1.56, .64, 1)' }
  )
})
"""
    return _emit("reduced-motion", style, body, script)


def raf_leaderboard() -> str:
    body = """
<ul class="board">
  <li><span class="name">Ada</span><span class="pts" data-to="247" data-from="120">0</span></li>
  <li><span class="name">Linus</span><span class="pts" data-to="198" data-from="142">0</span></li>
  <li><span class="name">Grace</span><span class="pts" data-to="312" data-from="190">0</span></li>
</ul>
<button id="play">Run</button>
"""
    style = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; padding-top: 4rem; }
.board { list-style: none; padding: 0; display: grid; gap: .5rem; }
.board li { display: grid; grid-template-columns: 1fr auto; padding: .75rem 1rem;
            border: 1px solid #eee; border-radius: .5rem; background: #f9f9f9;
            counter-increment: rank; }
.board li::before { content: counter(rank); font-weight: 800; padding-right: 1rem;
                     color: #888; }
.board { counter-reset: rank; counter-increment: rank 0; }
.board li:nth-child(1) { counter-increment: rank; }
.board li:nth-child(2) { counter-increment: rank; }
.board li:nth-child(3) { counter-increment: rank; }
.pts { font-variant-numeric: tabular-nums; font-weight: 600; }
button { margin-top: 1rem; padding: .5rem 1rem; cursor: pointer; }
"""
    script = """
// Animated counter via WAAPI on a CSS custom property.
document.getElementById('play').addEventListener('click', () => {
  document.querySelectorAll('.pts').forEach((el) => {
    const from = Number(el.dataset.from)
    const to   = Number(el.dataset.to)
    el.animate(
      [{ '--n': from }, { '--n': to }],
      {
        duration: 1200,
        easing: 'cubic-bezier(.2, .8, .2, 1)',
        fill: 'forwards'
      }
    )
    // Use rAF to render the current value to text (avoids
    // animating innerHTML, which is flaky).
    const start = performance.now()
    function tick(now) {
      const t = Math.min(1, (now - start) / 1200)
      const eased = 1 - Math.pow(1 - t, 3)
      el.textContent = Math.round(from + (to - from) * eased).toLocaleString()
      if (t < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  })
})
"""
    return _emit("raf-leaderboard", style, body, script)


PATTERNS: dict[str, callable] = {
    "basic-reveal": basic_reveal,
    "stagger": stagger,
    "spring-ish": spring_ish,
    "scrubable": scrubable,
    "dialog-open": dialog_open,
    "hover-lift": hover_lift,
    "accordion": accordion,
    "swipe-dismiss": swipe_dismiss,
    "morph-vt": morph_vt,
    "scroll-driven-reveal": scroll_driven_reveal,
    "reading-progress": reading_progress,
    "headline-shrink": headline_shrink,
    "parallax-bg": parallax_bg,
    "vt-same-doc": vt_same_doc,
    "vt-cross-doc": vt_cross_doc,
    "vt-image-grid": vt_image_grid,
    "reduced-motion": reduced_motion,
    "raf-leaderboard": raf_leaderboard,
}


def list_patterns() -> str:
    return "\n".join(f"- {name}" for name in sorted(PATTERNS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pattern", choices=sorted(PATTERNS), help="Print one pattern to stdout"
    )
    parser.add_argument("--all", action="store_true", help="Dump all to ./out/")
    parser.add_argument("--list", action="store_true", help="List patterns")
    parser.add_argument("--out", default="./out", help="Output dir (default: ./out)")
    args = parser.parse_args()

    if args.list:
        print(list_patterns())
        return 0
    if args.pattern:
        print(PATTERNS[args.pattern]())
        return 0
    if args.all:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in PATTERNS.items():
            (out / f"{name}.html").write_text(fn(), encoding="utf-8")
        print(f"Wrote {len(PATTERNS)} patterns to {out.resolve()}")
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
