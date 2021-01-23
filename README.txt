How to setup project:
1. 	clone git rep
2. 	sudo apt install python3.7
	sudo apt install python3.7-dev
	sudo apt install python3.7-venv
3. creat virtual environment (in backend folder)
	python3.7 -m venv <name>
	source <name>/bin/activate
	pip install -r requirements.txt   (maybe before: python -m pip install --upgrade pip; pip install scikit-build)
4. create new env file for frontend and backend
	cp .env.example .env
    open it and change (backend):
	Secret-key (google django create secret key and copy it into file)
	DEBUG=1
	MEDIA_ROOT
	FILE_UPLOAD_TEMP_DIR (this project is cirrently not using these files)
	FRONTEND_URL=http://localhost:8081 e.g.
   opent it and change to right ip-adresse (frontend)  e.g. http://localhost:3000

5. check ports in docker-compose.yml anpassen 8081:8081 und 3000:8000 
6. copy dataset to cellphaser/backdend/labeling_pw/code/RAW
7. create empty folder cellphaser/backdend/labeling_pw/code/label_maks_temp
8. start project
	backend:
	python manage.py makemigartions
	python manage.py migrate
	python manage.py runserver (id adresse e.g. 127.0.0.1:3000)
	frontend:
	yarn serve

 	OR: docker build
	docker-compose up
		[to see which container are runninh: docker ps; there you get ids for docker container logs <id>


	

	
