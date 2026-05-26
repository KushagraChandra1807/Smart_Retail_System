import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

router = APIRouter()

endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")


@router.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    try:
        if not endpoint or not key:
            raise HTTPException(
                status_code=500,
                detail="Azure Document Intelligence credentials missing"
            )

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        file_bytes = await file.read()

        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            body=file_bytes,
            content_type=file.content_type
        )

        result = poller.result()

        extracted_fields = []

        if result.documents:
            for document in result.documents:
                for field_name, field in document.fields.items():
                    extracted_fields.append({
                        "field_name": field_name,
                        "value": str(field.content) if field.content else None,
                        "confidence": field.confidence
                    })

        return {
            "message": "Document analyzed successfully",
            "filename": file.filename,
            "model": "Azure AI Document Intelligence - Prebuilt Invoice",
            "fields": extracted_fields,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(e)}"
        )