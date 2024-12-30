@echo off
REM Set the image ID
set IMAGE_ID=sha256:ad81f177a262b7ccb761322ffd1c5461bdb2813ad46c667c5752bd11ff97630d

REM Run instance 1
echo Starting instance 1 on port 1910...
docker run -d ^
    -e PORT=1910 ^
    -e DB_PATH=/app/data/db1.db ^
    -p 1910:1910 ^
    %IMAGE_ID%

REM Run instance 2
echo Starting instance 2 on port 2222...
docker run -d ^
    -e PORT=2222 ^
    -e DB_PATH=/app/data/db2.db ^
    -p 2222:2222 ^
    %IMAGE_ID%

echo All instances started.
pause
