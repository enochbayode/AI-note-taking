from faster_whisper import WhisperModel

# Load the optimized Whisper model
model = WhisperModel("base", compute_type="int8")  # Use "float16" for GPU acceleration

# Different form of model are avialable based on size
# -tiny
# -base
# -medium
# -large