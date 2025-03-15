from fastapi import APIRouter, File, UploadFile
from models.steel_service_detect.main_programm import detect  # 模型检测函数
from data_management.storage import save_record  # 数据库保存
from config.settings import MODEL_PATH, DATABASE_PATH, REPORT_DIR

router = APIRouter(prefix="/upload",tags=['图像上传与检测(unsure)'])

@router.post("/report")
async def upload_image(file: UploadFile = File(...)):
    """图像上传与检测（模型路径注释）"""
    image_path = f"{REPORT_DIR}/{file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 模型推理（参数注释）
    results = detect(
        image_path,
        model_path=MODEL_PATH,
        confidence_threshold=0.85  # 自定义置信度阈值
    )
    
    # 保存检测记录（数据库路径）
    save_record(DATABASE_PATH, image_path, results)
    
    return {"result": results}