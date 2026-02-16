#!/bin/bash

# 1. 检查并创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 2. 激活环境
source .venv/bin/activate

# 3. 安装依赖 (如果依赖文件有更新)
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# 4. 启动后端服务
echo "Starting Backend Server..."
nohup uvicorn web_app.backend.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!

# 5. 启动前端服务 (简单的 HTTP Server)
echo "Starting Frontend Server..."
cd web_app/frontend
nohup python3 -m http.server 8080 > ../../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ../..

echo "=================================================="
echo "✅ Project Started!"
echo "👉 Frontend: http://localhost:8080"
echo "👉 Backend API: http://localhost:8000/docs"
echo "=================================================="
echo "Press Ctrl+C to stop servers."

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
