from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from utils.image_processing import detect_defects
from utils.data_converter import json_to_xml, xml_to_json

app = FastAPI()
UPLOAD_FOLDER = 'uploads/'  # 您可能需要修改的路径变量

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, file_id + os.path.splitext(file.filename)[1])
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return JSONResponse(content={"status": "success", "file_id": file_id})

@app.post("/api/detect")
async def detect_image(file_id: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    defects = detect_defects(file_path)
    return JSONResponse(content={"status": "success", "defects": defects})

@app.get("/api/results")
async def get_results(file_id: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    defects = detect_defects(file_path)
    return JSONResponse(content={"status": "success", "defects": defects})

@app.get("/api/records")
async def get_records():
    # 在实际应用中，应该从数据库或持久化存储中获取记录
    # 这里简化为返回空列表
    records = []
    return JSONResponse(content={"status": "success", "records": records})

@app.post("/api/json_to_xml")
async def convert_json_to_xml(data: dict):
    xml_data = json_to_xml(data)
    return JSONResponse(content={"status": "success", "xml": xml_data})

@app.post("/api/xml_to_json")
async def convert_xml_to_json(xml_data: str):
    json_data = xml_to_json(xml_data)
    return JSONResponse(content={"status": "success", "json": json_data})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)