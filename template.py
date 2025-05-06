import os 
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name = "clustering-insured-population"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",    
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trial.ipynb",
    "template/index.html",
    "test.py",
    "README.md",
]
print(list_of_files)

# Create the project structure
for file_path in list_of_files:
    file_path = Path(file_path) 
    filedir , filename = os.path.split(file_path)
    print(f"Creating file: {filedir}")
    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")
        
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
            with open(file_path, 'w') as f:
                  pass 
                  logging.info(f"Creating empty file: {file_path}")
    else:
            logging.info(f"File already exists: {file_path}")
            
            
             