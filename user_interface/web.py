#web入口
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from config.settings import DATABASE_PATH, MODEL_PATH
from routers.user_interface import router as ui_router

# 初始化FastAPI应用
web = FastAPI(title="缺陷检测系统")

# 挂载静态文件（前端资源）
web.mount("/static", StaticFiles(directory="static"), name="static")

# 包含用户界面路由
web.include_router(ui_router, prefix="/api")

def init_web():
    """Web界面初始化操作"""
    # 创建静态文件目录
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # 数据库连接验证
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"数据库文件缺失: {DATABASE_PATH}")

@web.get("/", response_class=HTMLResponse)
async def serve_ui():
    """返回前端主页面"""
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

if __name__ == "__main__":
    import uvicorn
    init_web()
    uvicorn.run(web, host="0.0.0.0", port=8000)