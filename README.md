# Content Based Multimedia Retrieval Project

## Project Description

This project aims to teach us how to search for multimedia content using it's properties.
This method is much better than searching by a description written by a user as each user has his own prespective, and can descripe the content differently.

## Project Dependencies

Python 3.6 or higher - (https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

Virtual Enviroment - its recommended to have it installed when working with a python project (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

create a virutal env by running the following command:
```bash
virtualenv -p python3 env
```

activate the env using the following command in the same directory that you have setup the env in:
```bash
source env/bin/activate
```

navigate to the project directory where the requirements.txt file is located and run the following command:
```bash
pip install -r requirements.txt
```

and then install the following dependency:
```bash
sudo apt-get install ffmpeg
```

download the following file and put it in the images folder:
https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/

to run the project after installing the dependecies in the activated enviroment go to the project directory where the main.py file is located and run:
```bash
python main.py
```