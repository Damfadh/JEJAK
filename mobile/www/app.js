// Mobile scanner with camera mode + image upload fallback.
(function () {
  const consentModal = document.getElementById('consentModal');
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
  const acceptConsentBtn = document.getElementById('acceptConsent');
  const declineConsentBtn = document.getElementById('declineConsent');

  let stream = null;
  let raf = null;
  let lastDecoded = '';
  let verifying = false;
  let consentAccepted = false;

  const CFG_KEY = 'jejak_mobile_cfg';
  const CONSENT_KEY = 'jejak_mobile_consent';

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

  function setAppLocked(locked) {
    const controls = [startBtn, stopBtn, scanImageBtn, fileInput, saveCfgBtn, apiBaseInput, apiKeyInput];
    controls.forEach((el) => {
      if (el) el.disabled = locked;
    });
    if (consentModal) {
      consentModal.style.display = locked ? 'block' : 'none';
    }
  }

  function getConsent() {
    return localStorage.getItem(CONSENT_KEY) === 'accepted';
  }

  function acceptConsent() {
    localStorage.setItem(CONSENT_KEY, 'accepted');
    consentAccepted = true;
    setAppLocked(false);
    setStatus('Consent accepted. You can start scanning.');
  }

  function declineConsent() {
    localStorage.removeItem(CONSENT_KEY);
    consentAccepted = false;
    setAppLocked(true);
    setStatus('Consent is required to use this app.');
    stop();
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
    if (!consentAccepted) {
      setStatus('You must accept the consent first.');
      return;
    }
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
    if (!window.jsQR) {
      setStatus('Scanner library not loaded yet.');
      return null;
    }
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const attempts = [
      imageData,
      preprocessForScan(imageData, 170),
      preprocessForScan(imageData, 200),
      preprocessForScan(imageData, 225),
    ];

    for (const attempt of attempts) {
      const code = window.jsQR(attempt.data, attempt.width, attempt.height, {
        inversionAttempts: 'attemptBoth',
      });
      if (code) {
        return code;
      }
    }
    return null;
  }

  function preprocessForScan(sourceImageData, threshold) {
    const { width, height, data } = sourceImageData;
    const output = new Uint8ClampedArray(data.length);
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      const a = data[i + 3];
      const luminance = Math.round((r * 299 + g * 587 + b * 114) / 1000);
      const effective = a === 0 ? 255 : Math.round((luminance * a + 255 * (255 - a)) / 255);
      const value = effective < threshold ? 0 : 255;
      output[i] = value;
      output[i + 1] = value;
      output[i + 2] = value;
      output[i + 3] = 255;
    }
    return new ImageData(output, width, height);
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

  function initConsentUi() {
    consentAccepted = getConsent();
    setAppLocked(!consentAccepted);
    if (consentAccepted) {
      setStatus('Consent already accepted. Ready to scan.');
    } else {
      setStatus('Please accept the consent to start using the app.');
    }
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
  acceptConsentBtn.addEventListener('click', acceptConsent);
  declineConsentBtn.addEventListener('click', declineConsent);

  initConfigUi();
  initConsentUi();
})();
