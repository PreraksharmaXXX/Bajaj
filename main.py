import os
import io
import json
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pyngrok import ngrok
import nest_asyncio



app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Save temporarily
    temp_path = "/content/temp_uploaded_image.png"
    image.save(temp_path)

    # Apply your existing processing
    img = preprocess_image(temp_path)
    text = extract_text_from_image(img)
    lab_tests = parse_lab_report_text(text)

    result = {
        "is_success": True,
        "data": lab_tests
    }
    return JSONResponse(content=result)

nest_asyncio.apply()

public_url = ngrok.connect(8001)
print(f"🔗 Public URL: {public_url}/docs")

import uvicorn
from threading import Thread

def run():
    uvicorn.run(app, host="0.0.0.0", port=8001)

Thread(target=run).start()
