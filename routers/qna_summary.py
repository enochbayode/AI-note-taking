from fastapi import APIRouter, UploadFile, File
from transformers import pipeline
import json

router = APIRouter()
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", revision="564e9b5")

questions = {
    "primary_reason": "What is the primary reason for the visit?",
    "history_of_present_illness": "What is the history of present illness?",
    "past_medical_history": "What is the past medical history?",
    "medication_history": "What are the current medications and their dosages?",
    "allergies": "What are the known allergies?",
    "subjective": "What concerns did the patient express?",
    "objective": "What was observed about the client?",
    "assessment": "What is the assessment based on gathered information?",
    "plan": "What is the treatment plan, referrals, or medications prescribed?",
    "diagnosis": "What are the diagnosis details, including lab reports?",
    "procedures": "What procedures were performed during the visit?",
    "intervention": "What actions were taken during the session?",
    "evaluation": "What are the outcomes and effectiveness of interventions?"
}

@router.post("/qna_summary/")
async def medical_qna(file: UploadFile = File(...)):
    try:
        content = await file.read()
        transcript_text = content.decode("utf-8")
        
        responses = {}
        for key, question in questions.items():
            try:
                answer = qa_pipeline(question=question, context=transcript_text)
                responses[key] = answer["answer"] if answer["score"] > 0.5 else None
            except:
                responses[key] = None
        
        return {"responses": responses}
    except Exception as e:
        return {"error": str(e)}
