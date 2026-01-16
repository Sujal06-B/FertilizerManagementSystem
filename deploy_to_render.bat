@echo off
set /p msg="Enter commit message: "
echo Adding files...
git add .
echo Committing...
git commit -m "%msg%"
echo Push to GitHub...
git push origin main
echo.
echo Deployment triggered! Visit your Render dashboard to see progress.
pause
