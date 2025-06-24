## How to run the app locally
uvicorn main:app --host 0.0.0.0 --port 5000 --reload


# API Documentation 

## Overview

This document provides a detailed guide on how backend engineers can consume the APIs developed for transcription processing, summarization, and question-answering functionalities. These APIs are built with FastAPI and leverage Hugging Face transformers for NLP tasks.

---

## **1. Transcription Upload Endpoint**

### **Endpoint:**

```
POST /transcription/
```

### **Description:**

Accepts a video file and processes its transcription.

### **Request Format:**

- **Headers:**
  ```json
  {
    "Content-Type": "multipart/form-data"
  }
  ```
- **Body:**
  | Parameter | Type | Description                  |
  | --------- | ---- | ---------------------------- |
  | file      | File | Video file for transcription |

### **Response:**

A transcription file (`transcription.txt`) is returned as a downloadable file.

```json
{
    "transcription": "transcription text....",
    "file": "transcription.txt"
}
```

---

## **2. Real-Time Transcription Endpoint**

### **Endpoint:**

```
POST /real-time-transcribe/
```

### **Description:**

Transcribes live Telepractice sessions in real-time.

### **Request Format:**

- **Headers:**
  ```json
  {
    "Content-Type": "multipart/form-data"
  }
  ```
- **Body:**
  | Parameter | Type | Description |
  | --------- | ---- | ----------- |
  | audio_stream | Stream | Live audio stream |

### **Response:**

Returns a transcription file same to the `/transcription/` endpoint.

```json
{
    "file": "transcription.txt"
}
```

---

## **3. Summarization Endpoint**

### **Endpoint:**

```
POST /summarize/
```

### **Description:**

Summarizes the given transcription text file.

### **Request Format:**

- **Headers:**
  ```json
  {
    "Content-Type": "multipart/form-data"
  }
  ```
- **Body:**
  | Parameter | Type | Description           |
  | --------- | ---- | --------------------- |
  | file      | File | Transcribed text file |

### **Response:**

```json
{
    "summary": "Summarized version of the transcription."
}
```

---

## **4. Question-Answering Endpoint**

### **Endpoint:**

```
POST /qna_summary/
```

### **Description:**

Extracts specific medical information from the transcription text file.

### **Request Format:**

- **Headers:**
  ```json
  {
    "Content-Type": "multipart/form-data"
  }
  ```
- **Body:**
  | Parameter | Type | Description           |
  | --------- | ---- | --------------------- |
  | file      | File | Transcribed text file |

### **Response:**

```json
{
    "primary_reason_for_visit": "Description of the main reason for the visit",
    "history_of_present_illness": "Details about symptoms onset, progression, etc.",
    "past_medical_history": "Relevant past illnesses and medical events",
    "medication_history": "Current medications, dosages, and changes",
    "allergies": "List of allergies (medications, food, environment)",
    "subjective": "Patient's expressed concerns",
    "objective": "Observations about the patient",
    "assessment": "Doctor's assessment based on gathered information",
    "plan": "Treatment plan, referrals, follow-ups",
    "diagnosis": "Lab reports, imaging studies, etc.",
    "procedures": "Details of procedures performed",
    "intervention": "Actions taken during the session",
    "evaluation": "Effectiveness of interventions"
}
```

---

## **Multi-Tenancy Considerations**

To support multi-tenancy, backend engineers should:

1. **Include Tenant Identification**: Each request should contain a tenant-specific identifier in the headers or request body.
2. **Store Transcriptions Separately**: Use separate storage buckets or database tables per tenant.
3. **Access Control**: Implement authentication and authorization mechanisms to ensure tenants can only access their own data.
4. **Rate Limiting**: Apply rate limits per tenant to prevent abuse.

### **Example Request with Multi-Tenancy Headers:**

```json
{
    "tenant_id": "hospital_123",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}
```
---
### **Cross-Origin Resource Sharing (CORS) Configuration**

To enable secure access to the API across different frontend applications, CORS middleware is implemented as follows:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Usage Considerations:

Development: Currently allows all origins (*) for testing purposes.

Production: Update allow_origins with the actual frontend URLs to restrict unauthorized access.

Security: Ensure only necessary methods and headers are allowed to prevent vulnerabilities.

---

## **Conclusion**

This documentation provides a clear guide on how backend engineers can consume the API endpoints efficiently. Ensure that multi-tenancy considerations are properly handled for secure and scalable deployment.




