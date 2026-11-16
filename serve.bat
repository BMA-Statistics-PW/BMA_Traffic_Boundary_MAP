@echo off
REM เปิดแผนที่ในเครื่อง (index.html ต้องรันผ่าน HTTP server ไม่สามารถ double-click ได้)
cd /d %~dp0
echo ==========================================================
echo   BMA Traffic Boundary Map - Local Preview
echo   เปิดเบราว์เซอร์ไปที่  http://localhost:8000/
echo   กด Ctrl+C เพื่อหยุดเซิร์ฟเวอร์
echo ==========================================================
start "" http://localhost:8000/
python -m http.server 8000
