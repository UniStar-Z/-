import os
from pathlib import Path
from dotenv import load_dotenv  # 需安装python-dotenv

# 加载环境变量（优先从.env文件读取）
load_dotenv()

# 模型文件路径（相对项目根目录）
MODEL_PATH = "app\models\steel_service_detect\main_programm\models\yolov5s.yaml"
MODEL_WEIGHTS = "app\models\steel_service_detect\runs\train\exp7\weights\best.pt"  # 权重文件

# 动态路径配置
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH",  # 环境变量优先
              BASE_DIR / "app" / "data_management" / "database.db")
)

# 报告存储目录
REPORT_DIR = "app/image_upload/reports"