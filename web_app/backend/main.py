from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import models, auth
from .models import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 允许跨域 (方便前端开发)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Smart-ID-Photo-Pro API is running"}

@app.post("/api/upload")
async def upload_photo(file: UploadFile = File(...)):
    contents = await file.read()
    # TODO: 调用 core.py 进行 AI 处理
    return {"filename": file.filename, "status": "Uploaded (AI processing to be connected)"}

# 挂载静态文件 (前端打包后放这里)
# app.mount("/", StaticFiles(directory="web_app/frontend/dist", html=True), name="static")
