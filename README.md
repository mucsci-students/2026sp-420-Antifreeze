# Scheduler CLI Application
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
Course-scheduling program with a command-line interface. The CLI allows users to manage faculty, courses, rooms, and labs, as well as generate, display, and save optimized class schedules.

## **Features**
- **Faculty Management**: Add, delete, and modify faculty with availability, preferences, and credit limits
- **Course Management**: Add, delete, and modify courses with credits, faculty, rooms, labs, and conflict resolution
- **Room Management**:Add, delete, and modify rooms
- **Lab Management**: Add, delete, and modify labs
- **Schedule Generation**: Generate, display, and save optimized schedules
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
5. Run the CLI:
    ```uv run ./2026sp-420-Antifreeze/src/Main.py```
    
