from fastapi import APIRouter, UploadFile, File, HTTPException
from transformers import pipeline

router = APIRouter()
summary_pipeline = pipeline("summarization", model="facebook/bart-large-cnn") #revision="a4f8f3e")

@router.post("/summarize/")
async def summarize_text(file: UploadFile = File(...)):
    try:
        # Read the content of the file
        content = await file.read()
        text = content.decode("utf-8")
        
        # Ensure text is not too short
        if len(text) < 100:
            raise HTTPException(status_code=400, detail="Text is too short for summarization")
        
        # Generate summary
        summary = summary_pipeline(text, max_length=450, min_length=50, do_sample=False)
        
        return {"summary": summary[0]['summary_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
