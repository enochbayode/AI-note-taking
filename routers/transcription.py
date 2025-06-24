from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
import subprocess
from models.whisper_model import model

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded video file temporarily
        temp_video_path = Path(f"temp_{file.filename}")
        with temp_video_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Compress video file before processing
        #compressed_video_path = temp_video_path.with_suffix("_compressed.mp4")
        compressed_video_path = temp_video_path.parent / f"{temp_video_path.stem}_compressed.mp4"

        ffmpeg_compress_command = [
            "ffmpeg", "-i", str(temp_video_path), "-b:v", "500k", "-bufsize", "1000k", str(compressed_video_path)
        ]
        subprocess.run(ffmpeg_compress_command, check=True)

        # Extract audio using FFmpeg
        temp_audio_path = compressed_video_path.with_suffix(".wav")
        ffmpeg_command = [
            "ffmpeg", "-i", str(compressed_video_path),
            "-ac", "1", "-ar", "16000", "-vn",  # Convert to mono, 16kHz, remove video
            str(temp_audio_path)
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Break audio into segments for efficient processing
        segments = []
        segment_duration = 30  # 30 seconds per segment
        ffmpeg_segment_command = [
            "ffmpeg", "-i", str(temp_audio_path), "-f", "segment", "-segment_time", str(segment_duration),
            "-c", "copy", "segment_%03d.wav"
        ]
        subprocess.run(ffmpeg_segment_command, check=True)

        # Transcribe each segment using fast-whisper
        transcription_text = ""
        for segment in Path(".").glob("segment_*.wav"):
            segments_result, _ = model.transcribe(str(segment))
            for segment_text in segments_result:
                transcription_text += segment_text.text + " "
            segment.unlink()

        # Save transcription to a text file
        transcription_file = temp_audio_path.with_suffix(".txt")
        with transcription_file.open("w") as txt_file:
            txt_file.write(transcription_text.strip())

        # Clean up temporary files
        temp_video_path.unlink()
        compressed_video_path.unlink()
        temp_audio_path.unlink()

        return {"transcription": transcription_text.strip(), "file": str(transcription_file)}

    except subprocess.CalledProcessError as ffmpeg_error:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(ffmpeg_error)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
