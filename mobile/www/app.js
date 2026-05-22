// Mobile scanner with camera mode + image upload fallback.
(function () {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const result = document.getElementById('result');
  const startBtn = document.getElementById('start');
  const stopBtn = document.getElementById('stop');
  const scanImageBtn = document.getElementById('scanImage');
  const fileInput = document.getElementById('fileInput');
  const apiBaseInput = document.getElementById('apiBase');
  const apiKeyInput = document.getElementById('apiKey');
  const saveCfgBtn = document.getElementById('saveCfg');

  let stream = null;
  let raf = null;
  let lastDecoded = '';
  let verifying = false;

  const CFG_KEY = 'jejak_mobile_cfg';

  function getConfig() {
    try {
      const parsed = JSON.parse(localStorage.getItem(CFG_KEY) || '{}');
      return {
        apiBase: parsed.apiBase || 'http://127.0.0.1:8000',
        apiKey: parsed.apiKey || '',
      };
    } catch (_e) {
      return { apiBase: 'http://127.0.0.1:8000', apiKey: '' };
    }
  }

  function setStatus(text) {
    result.textContent = text;
  }

  function saveConfig() {
    const cfg = {
      apiBase: (apiBaseInput.value || '').trim().replace(/\/$/, ''),
      apiKey: (apiKeyInput.value || '').trim(),
    };
    localStorage.setItem(CFG_KEY, JSON.stringify(cfg));
    setStatus('Config saved.');
  }

  async function start() {
    try {
      stop();
      stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: 'environment' },
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });
      video.srcObject = stream;
      await video.play();
      setStatus('Camera ready. Point to QR...');
      tick();
    } catch (e) {
      setStatus('Camera error: ' + e.message);
    }
  }

  function stop() {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
    }
    if (raf) {
      cancelAnimationFrame(raf);
      raf = null;
    }
  }

  function tryDecodeFromCanvas() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    if (!window.jsQR) {
      setStatus('Scanner library not loaded yet.');
      return null;
    }
    return window.jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: 'attemptBoth',
    });
  }

  function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA && !verifying) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      try {
        const code = tryDecodeFromCanvas();
        if (code && code.data && code.data !== lastDecoded) {
          lastDecoded = code.data;
          stop();
          setStatus('QR detected. Verifying...');
          handlePayload(code.data);
          return;
        }
      } catch (_e) {
        // Keep scanning frames.
      }
    }
    raf = requestAnimationFrame(tick);
  }

  async function verifyPayload(parsed) {
    const cfg = getConfig();
    const headers = { 'Content-Type': 'application/json' };
    if (cfg.apiKey) {
      headers['x-api-key'] = cfg.apiKey;
    }

    const res = await fetch(cfg.apiBase + '/verify', {
      method: 'POST',
      headers,
      body: JSON.stringify({ signed_payload: parsed }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(body.detail || ('HTTP ' + res.status));
    }
    return body;
  }

  async function handlePayload(data) {
    verifying = true;
    try {
      const parsed = JSON.parse(data);
      const out = await verifyPayload(parsed);
      setStatus(out.valid ? 'Verified: OK' : 'Verification failed');
    } catch (e) {
      setStatus('Scan result invalid/non-JSON or backend error: ' + e.message);
    } finally {
      verifying = false;
    }
  }

  async function handleImageFile(file) {
    if (!file) return;
    const bitmap = await createImageBitmap(file);
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    ctx.drawImage(bitmap, 0, 0);

    const code = tryDecodeFromCanvas();
    if (!code || !code.data) {
      setStatus('No QR detected from selected image.');
      return;
    }
    setStatus('QR from image detected. Verifying...');
    await handlePayload(code.data);
  }

  function initConfigUi() {
    const cfg = getConfig();
    apiBaseInput.value = cfg.apiBase;
    apiKeyInput.value = cfg.apiKey;
  }

  startBtn.addEventListener('click', start);
  stopBtn.addEventListener('click', stop);
  scanImageBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', (ev) => {
    const file = ev.target.files && ev.target.files[0];
    handleImageFile(file);
    ev.target.value = '';
  });
  saveCfgBtn.addEventListener('click', saveConfig);

  initConfigUi();
})();
