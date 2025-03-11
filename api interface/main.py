from fastapi import FastAPI
import uvicorn
from data_collection.collection import collect
from data_manage.get_all_data import get_all
from data_manage.storage import user
from data_report.report import reports

app=FastAPI()

app.include_router(collect,prefix="/collect",tags=["数据采集接口"])
app.include_router(get_all,prefix="/get_all",tags=["获取全部数据接口"])
app.include_router("user",prefix="/user",tags=["数据存储接口"])
app.include_router("reports",prefix="/reports",tags=["导出报告接口"])

#注意：与UI界面对接

if __name__=='__main__':
    uvicorn.run("main:app",port=8000,reload=True)

