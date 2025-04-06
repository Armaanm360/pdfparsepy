from fastapi import FastAPI, File, UploadFile
import fitz
import pdfplumber
import pytesseract
from PIL import Image
import io
import shutil

app = FastAPI()

@app.post("/api/v1/pdf")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = {"pymupdf": [], "pdfplumber": [], "ocr": []}

    doc = fitz.open(temp_path)
    for page in doc:
        text = page.get_text()
        result["pymupdf"].append(text)

    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            result["pdfplumber"].append(text)

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        result["ocr"].append(text)

    return result

