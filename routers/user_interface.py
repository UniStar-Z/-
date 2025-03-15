from fastapi import APIRouter, HTTPException
from data_management.storage import get_detection_records  # 新增导入
from config.settings import DATABASE_PATH

router = APIRouter(prefix="/ui")

@router.get("/缺陷统计")
async def query_defect_stats():
    """获取缺陷类型统计（数据库查询）"""
    records = get_detection_records(DATABASE_PATH)  # 调用新函数
    stats = {
        "夹杂物": 0,
        "划痕": 0,
        "补丁": 0,
        "其他": 0
    }
    for record in records:
        for defect in record:  # 假设defect字段是列表格式
            if defect["type"] in stats:
                stats[defect["type"]] += 1
    return stats

