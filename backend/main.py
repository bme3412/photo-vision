from fastapi import FastAPI, UploadFile, File, HTTPException
from image_processing import process_image
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/api/process-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File is not an image")
        result = await process_image(file)
        logger.info("Image processed successfully")
        return result
    except HTTPException as e:
        logger.error(f"HTTP exception in analyze_image: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")