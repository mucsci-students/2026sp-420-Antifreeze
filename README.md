# Scheduler Web Application
## CMSC420-f26

## **Contributors**
- Abdilselam Ali
- An Nguyen
- Athan Klidonas
- Dhruv Bhanot
- Hailey Cassidy
- Manuel De la Cruz
- Zane Weaver

## **Overview**
Course-scheduling program with a graphical interface. The graphical interface allows users too load/save Json files adding faculty, course, rooms, and labs to the scheduler using a visual interface. The ability to generate and view different schedules is available. Functionality to load in made schedules using CSV format and reading them in app is also availble.  
## **Features**
- **Faculty Management**: Add, delete, and modify faculty with availability, preferences, and credit limits
- **Course Management**: Add, delete, and modify courses with credits, faculty, rooms, labs, and conflict resolution
- **Room Management**:Add, delete, and modify rooms
- **Lab Management**: Add, delete, and modify labs
- **Schedule Generation**: Generate, display, and save optimized schedules
- **CSV Display**: Able to load CSV files and desplay them in application.
- **Configuration Management**: Load, modify, display, and save configuration files

## **Prerequisites**
1. Make sure to have Python 3.13 or higher installed. To check your version, run:
```python --version```. If it is not installed, download it from: https://www.python.org/downloads/
2. Git is needed to clone the project. To check your version, run: 
```git --version```. If it is not installed, download it from: https://git-scm.com/install/
3. Make sure to have uv installed:
https://docs.astral.sh/uv/getting-started/installation/. To check your version, run:
```uv --version```

## **Getting Started**
1. Clone the repository:
```git clone https://github.com/mucsci-students/2026sp-420-Antifreeze```
2. Navigate to the repository:
```cd 2026sp-420-Antifreeze```
3. Create the python virtual environment:
```uv sync```
4. Activate the python virtual environment:
    - Linux/macOS:
    ```source .venv/bin/activate```
    - Windows:
    ```.venv\Scripts\activate```
5. Run the GUI:
    ```uv run ./2026sp-420-Antifreeze/src/main.py```
6.Access web app
    ```In the command line a link should pop up where you can than access the enviornment```

# Design Patterns
1. Model-View-Controller (MVC):
   we  used the MVC method of design to seperate our front end code from our backend code, allowing for more readable structure.
    
    
