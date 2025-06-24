from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.transcription import router as transcription_router
from routers.live_transcription import router as live_transcription_router
from routers.summarization import router as summarization_router
from routers.qna_summary import router as qna_summary_router


app = FastAPI()

#CORS middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include different routers for modularity
app.include_router(transcription_router)
app.include_router(live_transcription_router)
app.include_router(summarization_router)
app.include_router(qna_summary_router)



@app.get("/")
async def home():
    return {"message": "Telepractice real-time transcription and sumarization built on FAST API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True) 