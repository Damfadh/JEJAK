// Minimal QR scanning using browser camera and jsQR via CDN
(function(){
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  const result = document.getElementById('result');
  const startBtn = document.getElementById('start');
  const stopBtn = document.getElementById('stop');

  let stream = null;
  let raf = null;

  async function start(){
    try{
      stream = await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'}});
      video.srcObject = stream;
      await video.play();
      tick();
    }catch(e){ result.textContent = 'Camera error: '+e.message }
  }

  function stop(){
    if(stream){ stream.getTracks().forEach(t=>t.stop()); stream=null }
    if(raf) cancelAnimationFrame(raf);
  }

  function tick(){
    if(video.readyState === video.HAVE_ENOUGH_DATA){
      canvas.width = video.videoWidth; canvas.height = video.videoHeight;
      ctx.drawImage(video,0,0,canvas.width,canvas.height);
      try{
        // use jsQR from CDN
        const imageData = ctx.getImageData(0,0,canvas.width,canvas.height);
        if(window.jsQR){
          const code = window.jsQR(imageData.data, imageData.width, imageData.height);
          if(code){
            stop();
            result.textContent = 'QR: ' + code.data;
            // try parse JSON payload or call backend verify
            handlePayload(code.data);
            return;
          }
        }
      }catch(e){ /* ignore */ }
    }
    raf = requestAnimationFrame(tick);
  }

  async function handlePayload(data){
    try{
      const parsed = JSON.parse(data);
      // call backend verify
      result.textContent = 'Verifying...';
      const r = await fetch((window.__JEJAK_API_BASE||'/api') + '/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({signed_payload:parsed})});
      const j = await r.json();
      result.textContent = j.valid ? 'Verified: OK' : 'Not valid';
    }catch(e){
      result.textContent = 'Scanned data (not JSON): '+data;
    }
  }

  startBtn.addEventListener('click', start);
  stopBtn.addEventListener('click', stop);

  // load jsQR
  const s = document.createElement('script');
  s.src = 'https://unpkg.com/jsqr/dist/jsQR.js';
  s.onload = ()=> console.log('jsQR loaded');
  document.head.appendChild(s);
})();
