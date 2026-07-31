#!/usr/bin/env python3
"""
Generate per-slide voice-over WAV files for the HEXIS deck using ElevenLabs.

USAGE
-----
1. Install the SDK:
       pip install elevenlabs

2. Set your API key (one of):
       export ELEVENLABS_API_KEY="sk_..."
   ...or paste it into the ELEVENLABS_API_KEY constant below.

3. (Optional) Pick a voice. Default is "Rachel" — a calm female narrator.
   Browse voices at https://elevenlabs.io/app/voice-library and paste an
   ID into VOICE_ID below. Examples:
       Rachel  : 21m00Tcm4TlvDq8ikWAM   (default)
       Adam    : pNInz6obpgDQGcFmaJgB
       Antoni  : ErXwobaYiN019PkySvjV
       Bella   : EXAVITQu4vr4xnSDxMaL

4. Run:
       python tts_generate.py
   This reads `speaker-notes.json`, generates one WAV per slide, and
   writes them to `audio/01.wav` ... `audio/17.wav`.

The HTML deck (HEXIS Deck.html) auto-plays `audio/NN.wav` per slide
when you toggle the speaker icon in the bottom-right.
"""

import json
import os
import sys
from pathlib import Path

# ============================================================
# CONFIG  — edit these
# ============================================================
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")  # or paste "sk_..." here
VOICE_ID = os.environ.get("VOICE_ID", "5e3JKXK83vvgQqBcdUol")  # default narrator
MODEL_ID = "eleven_multilingual_v2"  # or "eleven_turbo_v2_5" for faster/cheaper
# Audio is grouped under audio/v-<short_id>/NN.mp3 so multiple voice sets
# can coexist. The HTML deck reads VOICE_DIR_DEFAULT and listens for a
# toggle to switch between sibling v-* folders.
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", f"audio/v-{VOICE_ID[:6]}"))
# mp3_44100_128 works on the free tier; pcm_44100 needs Pro+.
OUTPUT_FORMAT = "mp3_44100_128"
OUTPUT_EXT = "mp3"
SPEAKER_NOTES_JSON = Path("speaker-notes.json")
# ============================================================


def main():
    if not ELEVENLABS_API_KEY:
        sys.exit(
            "ERROR: ELEVENLABS_API_KEY is not set.\n"
            "Either export ELEVENLABS_API_KEY=sk_... or paste it into "
            "the constant at the top of this file."
        )

    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        sys.exit("ERROR: please run `pip install elevenlabs` first.")

    if not SPEAKER_NOTES_JSON.exists():
        sys.exit(f"ERROR: {SPEAKER_NOTES_JSON} not found.")

    notes = json.loads(SPEAKER_NOTES_JSON.read_text())
    if not isinstance(notes, list):
        sys.exit("ERROR: speaker-notes.json must be a JSON array of strings.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    is_pcm = OUTPUT_FORMAT.startswith("pcm_")

    for i, text in enumerate(notes, start=1):
        out_path = OUTPUT_DIR / f"{i:02d}.{OUTPUT_EXT}"
        if not text or not text.strip():
            print(f"[{i:02d}] (empty — skipping)")
            continue
        print(f"[{i:02d}] generating ({len(text)} chars) -> {out_path}")

        audio_stream = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            text=text,
            output_format=OUTPUT_FORMAT,
        )
        audio_bytes = b"".join(chunk for chunk in audio_stream if chunk)

        if is_pcm:
            # Wrap raw PCM in a WAV container so browsers can play it.
            import wave
            sample_rate = int(OUTPUT_FORMAT.split("_")[1])
            with wave.open(str(out_path), "wb") as wf:
                wf.setnchannels(1)         # ElevenLabs PCM is mono
                wf.setsampwidth(2)         # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_bytes)
        else:
            # mp3 (and other container formats) write straight to disk.
            out_path.write_bytes(audio_bytes)

    print(f"\nDone. {len(notes)} files written to ./{OUTPUT_DIR}/")
    print("Open HEXIS Deck.html and click the speaker icon (bottom-right) to hear them.")


if __name__ == "__main__":
    main()
