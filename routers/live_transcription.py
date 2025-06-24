from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.whisper_model import model
import asyncio
import io
import numpy as np
import soundfile as sf
import soxr  # Fast resampler

router = APIRouter()


async def resample_audio(audio_data, sample_rate):
    return await asyncio.to_thread(soxr.resample, audio_data, in_rate=int(sample_rate), out_rate=16000, quality=soxr.VHQ)

async def process_audio_chunk(audio_chunk: io.BytesIO):
    """Transcribes a small chunk of audio in real-time with optimized speed."""
    try:
        audio_chunk.seek(0)  # Reset to beginning
        audio_data, sample_rate = sf.read(audio_chunk, dtype="float32")  # remember to turn to float32
        
        # Convert bytes to numpy
        audio_data = np.array(audio_data, dtype=np.float32)

        # Ensure Whisper processes only expected sample rates (16kHz is ideal) hence, resample to 16KHz if needed
        if sample_rate != 16000:
            # raise ValueError(f"Incorrect sample rate: {sample_rate}. Expected 16kHz.")
            print(f"Resampling from {sample_rate}Hz to 16kHz...")
            audio_data = await resample_audio(audio_data, sample_rate)

        # Perform transcription with segmentation
        segments, _ = model.transcribe(audio_data, word_timestamps=True)
        
        # Return transcribed text while keeping real-time speed
        #return " ".join(segment.text for segment in segments)
    
         # Join transcribed text
        transcription = " ".join(segment.text for segment in segments)

        # Append the transcription to a file
        with open("session_transcription.txt", "a", encoding="utf-8") as f:
            f.write(transcription + "\n")

        return transcription

    except Exception as e:
        return f"Error: {str(e)}"

@router.websocket("/real-time-transcribe/")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time audio transcription (optimized for speed)."""
    await websocket.accept()
    print("Client connected.")

    try:
        while True:
            data = await websocket.receive_bytes()  # Receive raw audio bytes in chunks
            print(f"Received {len(data)} bytes of audio data.")

            transcription = await process_audio_chunk(io.BytesIO(data))  # Process efficiently

            await websocket.send_text(transcription)  # Send transcription immediately

    except WebSocketDisconnect:
        print("Client disconnected.")

    except Exception as e:
        print(f"Unexpected error: {e}")
