import io
import logging
from PIL import Image
from PIL.ExifTags import TAGS
from fastapi import UploadFile, HTTPException
from torchvision.transforms import Resize, ToTensor, Normalize
from torchvision.models import resnet50, ResNet50_Weights
import torch

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Starting image processing module with description...")

# Load the image classification model
try:
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print("Image classification model loaded successfully")
except Exception as e:
    logger.error(f"Error loading image classification model: {str(e)}")
    model = None

# ImageNet class labels
try:
    with open('imagenet_classes.txt') as f:
        labels = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    logger.error("imagenet_classes.txt not found. Using default labels.")
    labels = [f"class_{i}" for i in range(1000)]  # Default to 1000 generic class names

def extract_exif(image):
    exif_data = {}
    try:
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)
    except AttributeError as e:
        logger.error(f"Error extracting EXIF data: {str(e)}")
    return exif_data

def describe_image(image):
    try:
        if model is None:
            return "Image description is not available due to model loading error."
        
        # Prepare image
        transform = Resize((224, 224), ToTensor(), Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]))
        img_t = transform(image)
        batch_t = torch.unsqueeze(img_t, 0).to(device)

        # Generate prediction
        with torch.no_grad():
            out = model(batch_t)

        _, indices = torch.sort(out, descending=True)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        top_5 = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]
        
        description = f"This image most likely contains: {', '.join([f'{label} ({conf:.2f}%)' for label, conf in top_5])}"
        
        return description
    except Exception as e:
        logger.error(f"Error during image description: {str(e)}")
        return "Error during image description"

def basic_image_info(image):
    try:
        width, height = image.size
        format = image.format
        mode = image.mode
        return f"Image size: {width}x{height}, Format: {format}, Mode: {mode}"
    except Exception as e:
        logger.error(f"Error getting basic image info: {str(e)}")
        return "Error getting image info"

async def process_image(image: UploadFile):
    try:
        logger.info(f"Starting image processing for file: {image.filename}")
        contents = await image.read()
        logger.info(f"Image file read successfully, size: {len(contents)} bytes")
        
        pil_image = Image.open(io.BytesIO(contents))
        logger.info(f"PIL Image created successfully, mode: {pil_image.mode}")
        
        exif_data = extract_exif(pil_image)
        logger.info("EXIF data extracted")
        
        image_description = describe_image(pil_image)
        logger.info("Image description generated")
        
        image_info = basic_image_info(pil_image)
        logger.info("Basic image info retrieved")
        
        return {
            "exif_data": exif_data,
            "description": image_description,
            "image_info": image_info
        }
    except Exception as e:
        logger.error(f"Error in process_image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

print("Image processing module with description loaded successfully.")