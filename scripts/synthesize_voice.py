import asyncio
import edge_tts
import os
import sys
import json
import subprocess
import argparse
import numpy as np
import wave

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

VOICE = "vi-VN-NamMinhNeural"
SAMPLE_RATE = 44100

def generate_procedural_bgm(duration, out_path, bgm_type="tech"):
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    if bgm_type == "tech":
        # Tech thriller pulse
        bass = 0.28 * np.sin(2 * np.pi * 46.25 * t) + 0.18 * np.sin(2 * np.pi * 92.5 * t)
        beat_pulse = np.exp(-((t % 0.5) / 0.08)**2)
        beat_sound = 0.35 * beat_pulse * np.sin(2 * np.pi * 55 * t)
        tick = 0.08 * np.sin(2 * np.pi * 1200 * t) * np.exp(-((t % 0.25) / 0.02)**2)
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
        pad = 0.12 * lfo * (np.sin(2 * np.pi * 185.0 * t) + np.sin(2 * np.pi * 220.0 * t))
        mixed = bass + beat_sound + tick + pad
    else:
        # Lo-fi chill pulse
        bass = 0.3 * np.sin(2 * np.pi * 65.4 * t)
        beat_pulse = np.exp(-((t % 0.66) / 0.12)**2)
        beat_sound = 0.3 * beat_pulse * np.sin(2 * np.pi * 50 * t)
        pad = 0.15 * (np.sin(2 * np.pi * 261.6 * t) + np.sin(2 * np.pi * 329.6 * t))
        mixed = bass + beat_sound + pad

    fade_in_len = int(1.5 * SAMPLE_RATE)
    fade_out_len = int(2.5 * SAMPLE_RATE)
    mixed[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    mixed[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    mixed = mixed / np.max(np.abs(mixed)) * 0.3

    pcm = (mixed * 32767).astype(np.int16)
    with wave.open(out_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())

async def generate_chunk(text, out_file):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(out_file)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                return out_file
        except Exception as e:
            print(f"  [Attempt {attempt+1}] Warning: {e}")
            await asyncio.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"Failed to generate: {text}")

async def process_script(chunks, output_prefix, output_dir, tempo=1.16, bgm_type="tech"):
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, f"temp_{output_prefix}")
    os.makedirs(temp_dir, exist_ok=True)

    chunk_files = []
    print(f"Generating {len(chunks)} voice chunks...")
    for idx, text in enumerate(chunks):
        out_file = os.path.join(temp_dir, f"chunk_{idx:03d}.mp3")
        f = await generate_chunk(text, out_file)
        chunk_files.append(f)
        print(f"[{idx+1}/{len(chunks)}] Done ({len(text)} chars)")
        await asyncio.sleep(1.5)

    concat_txt = os.path.join(temp_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            abs_p = os.path.abspath(cf).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")

    raw_voice = os.path.join(temp_dir, "raw_voice.mp3")
    tempo_voice = os.path.join(temp_dir, "tempo_voice.mp3")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-c", "copy", raw_voice
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_voice, "-filter:a", f"atempo={tempo}", tempo_voice
    ], check=True)

    dur_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", tempo_voice
    ]
    res = subprocess.run(dur_cmd, capture_output=True, text=True, check=True)
    total_dur = float(res.stdout.strip())

    # Generate BGM
    bgm_path = os.path.join(temp_dir, "bgm.wav")
    generate_procedural_bgm(total_dur, bgm_path, bgm_type)

    final_m4a = os.path.join(output_dir, f"final_audio_{output_prefix}.m4a")

    cmd_mix = [
        "ffmpeg", "-y",
        "-i", tempo_voice,
        "-i", bgm_path,
        "-filter_complex",
        "[0:a]volume=1.0,pan=stereo|c0=c0|c1=c0[v];"
        "[1:a]volume=0.25,pan=stereo|c0=c0|c1=c0[b];"
        "[v][b]amix=inputs=2:duration=first:dropout_transition=2[mixed]",
        "-map", "[mixed]",
        "-c:a", "aac",
        "-b:a", "192k",
        final_m4a
    ]
    subprocess.run(cmd_mix, check=True)
    print(f"\nFinal audio ready: {final_m4a}")
    print(f"Total duration: {total_dur:.2f}s ({total_dur/60:.2f}m)")
    return final_m4a, total_dur

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Path to JSON file containing array of text chunks")
    parser.add_argument("--name", required=True, help="Output project name")
    parser.add_argument("--outdir", default="03_Audio_Tracks", help="Output directory")
    parser.add_argument("--tempo", type=float, default=1.16, help="Tempo speedup factor")
    parser.add_argument("--bgm", default="tech", choices=["tech", "lofi"], help="BGM mood")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    asyncio.run(process_script(chunks, args.name, args.outdir, args.tempo, args.bgm))
