@echo off
REM This script automates the process of training a model, building and running Docker containers, seeding the database, and launching the application components.

set "rootDir=%cd%"
set "trainingDir=%rootDir%\src\logic\training"
set "faceDBDir=%rootDir%\deployment\docker\faceDB"
set "logDBDir=%rootDir%\deployment\docker\logDB"
set "seedDir=%rootDir%\src\persistance\seed"
set "presentationDir=%rootDir%\src\presentation"
set "apiDir=%rootDir%\src\api"

REM Run the training.py file to train the Model
cd "%trainingDir%"
python training.py
if errorlevel 1 (
    echo Error: Training failed!
    pause
    exit /b 1
)
echo Model successfully Trained!

REM Build docker mob
cd "%faceDBDir%"
docker build -t mob .
if errorlevel 1 (
    echo Error: Docker build failed!
    pause
    exit /b 1
)
echo Successfully built Docker mob 

REM Run three instances of docker mob
docker run -d --name mobA -p 5432:5432 mob
docker run -d --name mobB -p 5433:5432 mob
docker run -d --name mobC -p 5434:5432 mob
echo mobA, mobB, and mobC running

REM Build the log docker
cd "%logDBDir%"
docker build -t logs .
if errorlevel 1 (
    echo Error: Docker build failed!
    pause
    exit /b 1
)
echo Successfully built Docker logs

REM Run the logs docker container
docker run -d --name logs -p 5435:5432 logs
echo logs db running

REM Seed the database
cd "%seedDir%"
python seed.py
if errorlevel 1 (
    echo Error: Database seeding failed!
    pause
    exit /b 1
)
echo Database seeded successfully!

REM Build React app
cd "%presentationDir%"
call npm install
call npm run build
echo React app built successfully!

REM Launch front-end
cd "%apiDir%"
start cmd /k "python front.py"

REM Launch worker
cd "%rootDir%\src"
start cmd /k "python api\worker.py"

exit