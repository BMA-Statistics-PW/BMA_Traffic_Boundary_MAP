@echo off
REM ==== อัปเดตโปรเจกต์ขึ้น GitHub (double-click เพื่อรัน) ====
cd /d %~dp0
echo ============================================================
echo   BMA Traffic Boundary Map  -  Push to GitHub
echo ============================================================

REM ตรวจว่าตั้ง remote origin แล้วหรือยัง
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  echo.
  echo [ยังไม่ได้ตั้ง remote origin]
  set /p REPO="วาง URL ของ GitHub repo (เช่น https://github.com/USER/BMA_traffic_boundary_map.git): "
  git init
  git branch -M main
  git remote add origin %REPO%
)

echo.
echo กำลังเพิ่มไฟล์และ commit...
git add .
git commit -m "Update BMA traffic boundary map - %date% %time%"

echo.
echo กำลัง push ขึ้น GitHub...
git push -u origin main

echo.
echo ============================================================
echo เสร็จแล้ว! หากตั้ง GitHub Pages ไว้ แผนที่จะอัปเดตใน 1-2 นาที
echo   https://USER.github.io/BMA_traffic_boundary_map/
echo ============================================================
pause
