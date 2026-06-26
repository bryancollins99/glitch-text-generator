// Faithful glitch export — captures the rendered #output-text effect (CSS shadows,
// RGB-split, transform) to PNG / SVG / animated GIF. Replaces the old flat-canvas
// text redraw that ignored the actual effect. Client-side only (html-to-image + gif.js).

(function () {
  // --- helpers -------------------------------------------------------------
  function getOutputNode() {
    // Preserve the original per-page element selection.
    if (window.location.pathname.includes('halloween')) {
      return document.getElementById('halloween-output');
    }
    return document.getElementById('output-text');
  }

  function bgColor(node) {
    const c = getComputedStyle(node).backgroundColor;
    return (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') ? c : '#0a0a0a';
  }

  function fileBase() {
    const p = window.location.pathname.split('/').pop().split('.')[0];
    return (p && p.length) ? p : 'glitch';
  }

  function download(href, ext, revoke) {
    const a = document.createElement('a');
    a.download = `${fileBase()}-glitchtexteffect.${ext}`;
    a.href = href;
    document.body.appendChild(a);
    a.click();
    a.remove();
    if (revoke) setTimeout(() => URL.revokeObjectURL(href), 4000);
  }

  function libsReady(needGif) {
    if (typeof htmlToImage === 'undefined') {
      console.error('html-to-image not loaded');
      return false;
    }
    if (needGif && typeof GIF === 'undefined') {
      console.error('gif.js not loaded');
      return false;
    }
    return true;
  }

  // Build an offscreen "stage": a padded, background-filled clone of the output
  // node plus a correct-domain watermark. Everything is captured from the stage
  // so PNG / SVG / GIF share identical framing + watermark.
  function buildStage(node) {
    const stage = document.createElement('div');
    stage.style.cssText =
      `position:fixed;left:-99999px;top:0;padding:32px 40px;` +
      `background:${bgColor(node)};display:inline-block;box-sizing:border-box;`;

    const clone = node.cloneNode(true);
    clone.style.animation = 'none';            // we bake each frame explicitly
    clone.style.margin = '0';
    clone.style.left = '';
    clone.style.position = 'static';
    stage.appendChild(clone);

    const wm = document.createElement('div');
    wm.textContent = 'glitchtexteffect.com';
    wm.style.cssText =
      'text-align:right;font:12px monospace;color:rgba(255,255,255,0.35);' +
      'margin-top:14px;letter-spacing:1px;';
    stage.appendChild(wm);

    document.body.appendChild(stage);
    return { stage, clone };
  }

  // The actual glitch-animation keyframes (static/css/style.css) — translate +
  // RGB-split text-shadow. Baking these guarantees visibly distinct GIF frames
  // regardless of animation runtime / html-to-image clone base-state behaviour.
  const FRAMES = [
    { tf: 'translate(0, 0)',
      ts: '-2px -2px 0 var(--primary-color), 2px 2px 0 var(--secondary-color)' },
    { tf: 'translate(-2px, 2px)',
      ts: '2px -2px 0 var(--secondary-color), -2px 2px 0 var(--primary-color)' },
    { tf: 'translate(2px, -2px)',
      ts: '-2px 2px 0 var(--primary-color), 2px -2px 0 var(--secondary-color)' },
    { tf: 'translate(-2px, -2px)',
      ts: '2px 2px 0 var(--secondary-color), -2px -2px 0 var(--primary-color)' },
  ];

  function setBusy(on) {
    document.querySelectorAll('[data-dl]').forEach((b) => {
      b.disabled = on;
      b.style.opacity = on ? '0.6' : '';
    });
  }

  // --- exporters -----------------------------------------------------------
  async function exportPng(node) {
    const { stage, clone } = buildStage(node);
    // Freeze the frame the user currently sees.
    const live = getComputedStyle(node);
    if (live.transform && live.transform !== 'none') clone.style.transform = live.transform;
    if (live.textShadow && live.textShadow !== 'none') clone.style.textShadow = live.textShadow;
    try {
      const url = await htmlToImage.toPng(stage, { pixelRatio: 2, backgroundColor: bgColor(node), skipFonts: true });
      download(url, 'png');
    } finally {
      stage.remove();
    }
  }

  async function exportSvg(node) {
    const { stage } = buildStage(node);
    try {
      const url = await htmlToImage.toSvg(stage, { backgroundColor: bgColor(node), skipFonts: true });
      download(url, 'svg');
    } finally {
      stage.remove();
    }
  }

  async function exportGif(node) {
    const { stage, clone } = buildStage(node);
    const gif = new GIF({
      workers: 2,
      quality: 10,
      workerScript: '/static/js/vendor/gif.worker.js',
      background: bgColor(node),
    });
    try {
      for (let i = 0; i < FRAMES.length; i++) {
        clone.style.transform = FRAMES[i].tf;
        clone.style.textShadow = FRAMES[i].ts;
        void clone.offsetWidth; // force reflow so getComputedStyle resolves the frame
        const canvas = await htmlToImage.toCanvas(stage, {
          pixelRatio: 1,
          backgroundColor: bgColor(node),
          skipFonts: true,
        });
        gif.addFrame(canvas, { delay: 120, copy: true });
      }
      await new Promise((resolve, reject) => {
        // Settle on success, failure, OR timeout — otherwise a failed render
        // would leave the Promise pending and the buttons permanently disabled.
        const timer = setTimeout(() => reject(new Error('GIF render timed out')), 20000);
        gif.on('finished', (blob) => {
          clearTimeout(timer);
          if (blob && blob.size) { download(URL.createObjectURL(blob), 'gif', true); resolve(); }
          else reject(new Error('GIF render produced empty output'));
        });
        gif.on('abort', () => { clearTimeout(timer); reject(new Error('GIF render aborted')); });
        gif.render();
      });
    } finally {
      stage.remove();
    }
  }

  // --- public entry --------------------------------------------------------
  async function downloadGlitch(format) {
    const node = getOutputNode();
    if (!node || !node.textContent.trim()) {
      console.error('Nothing to export — generate some glitch text first.');
      return;
    }
    const needGif = format === 'gif';
    if (!libsReady(needGif)) return;
    setBusy(true);
    try {
      if (format === 'svg') await exportSvg(node);
      else if (format === 'gif') await exportGif(node);
      else await exportPng(node);
    } catch (err) {
      console.error('Export failed:', err);
    } finally {
      setBusy(false);
    }
  }

  // Expose + keep backwards-compatible alias for pages still calling the old name.
  window.downloadGlitch = downloadGlitch;
  window.downloadAsImage = () => downloadGlitch('png');
})();
