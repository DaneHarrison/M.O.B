@echo off

REM Run the trainin.py file to train the Model
set rootDir=%cd%
cd %rootDir%\src\logic\trainingServer
"python" "training.py"
echo Model successfully Trained!

REM Build docker mob
cd %rootDir%\src\deployment\docker\faceDB
"docker" "build" "-t" "mob" "."
echo Successfully built docker mob 

REM run three instances of docker mob
"docker" "run" "-d" "--name" "mobA" "-p" "5432:5432" "mob"
echo mobA running
"docker" "run" "-d" "--name" "mobB" "-p" "5433:5432" "mob"
echo mobB running
"docker" "run" "-d" "--name" "mobC" "-p" "5434:5432" "mob"
echo mobC running

REM build the log docker
cd %rootDir%\src\deployment\docker\logDB
"docker" "build" "-t" "logs" "."
echo Successfully built docker logs

REM run the logs docker container
"docker" "run" "-d" "--name" "logs" "-p" "5435:5432" "logs"
echo logs db running

REM build worker docker
cd %rootDir%
"docker" "build" "-t" "worker" "-f" "src/deployment/docker/worker/Dockerfile" "."
echo Successfully built docker worker

REM run docker worker
cd %rootDir%\src\deployment\docker\worker
"docker" "run" "-d" "--name" "worker" "-p" "4000:4000" "worker"
echo Worker docker image running

REM build front docker
cd %rootDir%
"docker" "build" "-t" "front" "-f" "src/deployment/docker/front/Dockerfile" "."
echo Successfully built docker front

REM run docker front
cd %rootDir%\src\deployment\docker\front
"docker" "run" "-d" "--name" "front" "-p" "5000:5000" "front"
echo front docker running

REM Seed the db
cd %rootDir%\src\persistance\seed
"python" "seed.py"
echo db seeded!