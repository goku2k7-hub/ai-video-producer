const puppeteer = require('puppeteer-core');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = {};
  for (let i = 2; i < process.argv.length; i += 2) {
    const key = process.argv[i].replace(/^--/, '');
    const val = process.argv[i + 1];
    args[key] = val;
  }
  return args;
}

async function render() {
  const args = parseArgs();
  const templatePath = path.resolve(args.template);
  const audioFile = path.resolve(args.audio);
  const outputFile = path.resolve(args.output);
  const width = parseInt(args.width || '1080', 10);
  const height = parseInt(args.height || '1920', 10);
  const fps = parseInt(args.fps || '30', 10);
  const duration = parseFloat(args.duration);

  if (!duration || isNaN(duration)) {
    console.error('Error: --duration <seconds> is required.');
    process.exit(1);
  }

  const totalFrames = Math.ceil(duration * fps);
  console.log(`=== STARTING ZERO-DISK PIPE RENDERING ===`);
  console.log(`Template: ${templatePath}`);
  console.log(`Audio: ${audioFile}`);
  console.log(`Output: ${outputFile}`);
  console.log(`Dimensions: ${width}x${height} | FPS: ${fps} | Frames: ${totalFrames} (${duration}s)`);

  const ffmpegArgs = [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'mjpeg',
    '-r', String(fps),
    '-i', '-',
    '-i', audioFile,
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '19',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    outputFile
  ];

  const ffmpeg = spawn('ffmpeg', ffmpegArgs);
  ffmpeg.stderr.on('data', (d) => {
    const s = d.toString();
    if (s.includes('Error') || s.includes('fatal')) console.error('[FFmpeg]', s);
  });

  const ffmpegPromise = new Promise((resolve, reject) => {
    ffmpeg.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}`));
    });
  });

  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--allow-file-access-from-files']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  const fileUrl = 'file:///' + templatePath.replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'load' });

  const startTime = Date.now();
  for (let f = 0; f < totalFrames; f++) {
    await page.evaluate((frame, frameFps) => {
      if (window.seekToFrame) window.seekToFrame(frame, frameFps);
    }, f, fps);

    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    const canContinue = ffmpeg.stdin.write(buf);
    if (!canContinue) {
      await new Promise((res) => ffmpeg.stdin.once('drain', res));
    }

    if ((f + 1) % 150 === 0 || f === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const percent = Math.floor(((f + 1) / totalFrames) * 100);
      const fpsRender = ((f + 1) / elapsed).toFixed(1);
      const remainingSec = Math.max(0, Math.floor((totalFrames - f - 1) / fpsRender));
      console.log(`[Frame ${f + 1}/${totalFrames}] ${percent}% | Speed: ${fpsRender} fps | ETA: ${remainingSec}s`);
    }
  }

  ffmpeg.stdin.end();
  await ffmpegPromise;
  await browser.close();

  const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n🎉 RENDERING FINISHED in ${totalTime}s`);
  console.log(`Saved: ${outputFile}`);
}

render().catch(err => {
  console.error('Render error:', err);
  process.exit(1);
});
