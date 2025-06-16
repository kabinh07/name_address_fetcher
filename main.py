from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO

from utils.ocr import OCR
from utils.agent import Fetcher

app = FastAPI()
ocr_instance = OCR()
fetcher_instance = Fetcher()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/fetch_info")
def fetch_info(image: UploadFile = File(...)):
    contents = image.file.read()
    image = Image.open(BytesIO(contents))
    ocr_results = ocr_instance.fetch_ocr(image)
    if not ocr_results:
        return JSONResponse(status_code=400, content={"error": "No text detected in the image."})
    document_type = fetcher_instance.get_document_type(ocr_results)
    result = fetcher_instance.extract_text(ocr_results, document_type)
    if not result:
        return JSONResponse(status_code=500, content={"error": "Failed to extract information."})
    return JSONResponse(content={"result": result, "document_type": document_type})