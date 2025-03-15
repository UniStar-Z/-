from fastapi import BackgroundTasks
from fastapi import APIRouter, File, UploadFile, HTTPException
from models.steel_service_detect.main_programm import detect
from data_management.storage import save_detection
from config.settings import MODEL_PATH, DATABASE_PATH, REPORT_DIR
from tasks import process_imageAsync  # 异步任务模块

router = APIRouter(prefix="/upload")

@router.post("/缺陷检测")
async def defect_detection(
    background_tasks: BackgroundTasks,  # 非默认参数在前
    file: UploadFile = File(...)        # 默认参数在后
):
    """核心检测接口（模型路径注释）"""
    try:
        # 1. 保存文件
        image_path = f"{REPORT_DIR}/{file.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 2. 启动异步检测（路径注释）
        background_tasks.add_task(
            process_imageAsync,
            image_path,
            model_path=MODEL_PATH,
            db_path=DATABASE_PATH
        )
        
        return {"status": "Detection started"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))