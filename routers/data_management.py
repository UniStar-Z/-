from fastapi import APIRouter, HTTPException
from data_management.storage import (
    init_db,
    save_record,
    get_detection_records,  # 新增导入
    export_to_csv  # 假设已存在
)
from config.settings import DATABASE_PATH, REPORT_DIR

router = APIRouter(prefix="/data")

@router.post("/initialize")
async def initialize_database():
    """初始化数据库（仅第一次调用）"""
    try:
        init_db(DATABASE_PATH)
        return {"message": "Database initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export缺陷数据")
async def export缺陷数据():
    """导出检测数据到CSV"""
    try:
        records = get_detection_records(DATABASE_PATH)  # 使用新函数
        export_to_csv(DATABASE_PATH, f"{REPORT_DIR}/defects.csv")
        return {"path": f"{REPORT_DIR}/defects.csv"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))