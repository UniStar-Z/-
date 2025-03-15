from fastapi import APIRouter
from data_management.storage import get_detection_records  # 引用存储模块
from utils.format_converter import json_to_xml  # 格式转换工具
from config.settings import REPORT_DIR          # 报告目录路径
from config.settings import DATABASE_PATH

router = APIRouter(prefix="/data",tags=['数据采集'])

@router.get("/get_all_data")
async def get_all_defect_data():
    """获取所有检测记录（数据库路径注释）"""
    records = get_detection_records(DATABASE_PATH)
    return {"data": records}

@router.post("/convert_format")
async def convert_data_format(request):
    """JSON转XML格式转换"""
    data = await request.json()
    return json_to_xml(data)  # 工具函数调用
