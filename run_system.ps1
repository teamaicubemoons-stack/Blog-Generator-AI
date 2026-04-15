# Cubemoons AI Blog Agent - Execution Script

# Kill any existing processes on these ports
Write-Host "Cleaning up existing processes..." -ForegroundColor Cyan
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue

# Start Backend
Write-Host "Starting Backend API (Port 8001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\.venv\Scripts\activate; python main.py"

# Start Frontend
Write-Host "Starting Frontend UI (Port 5173)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "System is launching! Please wait a moment for the ports to become active." -ForegroundColor Yellow
Write-Host "Backend: http://localhost:8001"
Write-Host "Frontend: http://localhost:5173"
