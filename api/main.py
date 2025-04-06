
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from routers import (
    data_collection_router,
    user_interface_router,
    data_management_router,
    image_upload_router
)
from config.settings import DATABASE_PATH, MODEL_PATH, MODEL_WEIGHTS
from data_management.storage import init_db
from models.yolo_custom import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时操作
    print("⚡ 系统启动中...")
    
    # 初始化数据库并挂载到 app.state
    db_connection = init_db(DATABASE_PATH)  # 假设 init_db 返回数据库连接
    app.state.db_connection = db_connection
    
    # 加载模型并挂载到 app.state
    model = load_model(
        yaml_path=MODEL_PATH,
        weights_path=MODEL_WEIGHTS
    )
    app.state.model = model  # ✅ 将模型保存到应用状态
    
    yield
    
    # 关闭时操作
    print("🛑 系统关闭中...")
    # 关闭数据库连接（如果有需要）
    await db_connection.close()

app = FastAPI(lifespan=lifespan)

# 包含路由
app.include_router(data_collection_router)
app.include_router(user_interface_router)
app.include_router(data_management_router)
app.include_router(image_upload_router)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app='api.main:app', host='0.0.0.0', port=8080, reload=True)