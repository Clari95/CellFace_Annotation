# backend

### Project setup (if locally, otherwise run docker-compose of root)

#### Windows
* Consider using WSL or a Virtual Machine if you want to run the frontend also
* Using python 3.7 with [Anaconda](https://www.anaconda.com/)
```
conda env create -n <env_name> -f environment.yml
conda activate <env_name>
```
Alternatively you can use the Windows Subsystem for Linux (WSL) 
https://docs.microsoft.com/de-de/windows/wsl/install-win10 then you can follow
the Linux commands below

#### Linux
* Make sure the python library for virtual environments is installed.
```
sudo apt-get install python3-venv
```
* Create a new virtual environment called cfback
```
python3 -m venv cfback
```
* Activate the virutal environment (this step is nescesary every time you close the terminal)
```
source cfback/bin/activate
```
* Make sure pip is up to date and install the required python packages
```
pip install --update pip setuptools
pip install -r requriements.txt
```

#### General

* Copy .env.example file and rename it to .env
* Add the following settings in the .env file:
    * Visit https://djecrety.ir generate a key and paste it to the file
    * Set Debug to 1
    * Specify a MEDIA_ROOT folder. This is where the file explorer will start for preview
    * Specify a FILE_UPLOAD_TEMP_DIR folder. This is where fils will be stored during upload.

### Run server
* Activate the environment (if needed)
    * Windows
    ```
    conda activate <env_name> (if needed)
    ```
    * Linux
    ```
    source cfback/bin/activate
    ```
* Start the Django Server
```
python manage.py runserver 0.0.0.0:3000
```

* If you cannot reach http://localhost:3000 in your browser try to run the following command
    ```
    python manage.py runserver localhost:3000
    ```
    or 
    ```
    python manage.py runserver 127.0.0.1:3000
    ```

### General Structure

* Explorer: everything that explores the *media* folder, soon to be a volume mounted somewhere. 
* Preview: previewing files, specially *.raw* files.
    * contains the translation from *.bin* to *.png* 
* Upload: uploading the BIN files and creating associated *.raw* file.