# Scheduler GUI Application
## CMSC420-f26

---

## Contributors
- Abdilselam Ali
- An Nguyen
- Athan Klidonas
- Dhruv Bhanot
- Hailey Cassidy
- Manuel De la Cruz
- Zane Weaver

---

## Overview

A Flask-based web application for generating course schedules. The system is driven by loading in a JSON or CSV file that allows users to manage faculty, courses, rooms, and labs, as well as generate, display, and save optimized class schedules.

---

## Project Structure

```bash
.
├── LICENSE
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   ├── controller/
│   │   ├── flask/
│   │   │   └── ...
│   │   ├── modifyConfig/
│   │   │   ├── configCli.py
│   │   │   ├── modConflict.py
│   │   │   └── ...
│   │   ├── navigation_controller.js
│   │   ├── navigation_model.js
│   │   └── navigation_view.js
│   ├── main.py
│   ├── model/
│   │   ├── AI/
│   │   │   ├── agent.py
│   │   │   └── executor.py
│   │   └── schedule/
│   │       ├── conflict.py
│   │       ├── course.py
│   │       └── ...
│   └── view/
│       ├── static/
│       │   ├── css/
│       │   │   └── ...
│       │   └── images/
│       │       └── ...
│       └── templates/
│           └── index.html
└── test/
    ├── test_conflict.py
    ├── test_course.py
    └── ...
```

---

## Features

- **Faculty Management:** Add, delete, and modify faculty with availability, preferences, and credit limits
- **Course Management:** Add, delete, and modify courses with credits, faculty, rooms, labs, and conflict resolution
- **Room Management:** Add, delete, and modify rooms
- **Lab Management:** Add, delete, and modify labs
- **Time Slot Management:** Add, delete, and modify time slots with days, times, and spacing
- **Schedule Generation:** Generate, display, and save optimized schedules\
- **Configuration Management:** Import and export configuration files; default at startup is an empty JSON
- **Schedule Viewer:** View schedules by room, lab, faculty, and day in tabular format
- **AI Assistant:** Interactive assistant that can answer questions, modify fields, and generate schedules

---

## Prerequisites

1. **Python 3.13+** 
    - Check with `python --version`
    - Download from https://www.python.org/downloads/
2. **Git** 
    - Check with `git --version` 
    - Download from https://git-scm.com/install/
3. **uv** 
    - Check with `uv --version` 
    - Download from https://docs.astral.sh/uv/getting-started/installation/

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/mucsci-students/2026sp-420-Antifreeze
   ```

2. Navigate to the repository:
   ```bash
   cd 2026sp-420-Antifreeze
   ```

3. Create the virtual environment and install dependencies:
   ```bash
   uv sync
   ```

4. Activate the virtual environment:
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `source .venv/Scripts/activate`

5. Set up your OpenAI API key:
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```
   - Retrieve a key from https://platform.openai.com/api-keys
   - Never commit your `.env` file — it poses a major security risk!

6. Run the GUI:
   ```bash
   uv run src/main.py
   ```
   - Open the address shown in your terminal (e.g. `http://127.0.0.1:5000`)
   - Press `CTRL+C` to stop the server

7. To deactivate the virtual environment:
   ```bash
   deactivate
   ```

---

## Navigating the GUI

#### Loading and Saving
- Click **Load** to import a JSON or CSV configuration file — the status bar at the bottom confirms file name and load time
- Click **Save** to export the current configuration as a JSON file
- An empty configuration is loaded automatically on startup

#### Field Tabs
- The colored **Fields** buttons (Faculty, Courses, Labs, Rooms, Time Slots, and Schedule) populate the display with the respective field's entries

#### Adding, Modifying, and Deleting Entries
- Select a field tab, then use the **Add**, **Modify**, or **Delete** toolbar buttons
- **Add** and **Modify** open a popup form for that field; use the **+** and **−** buttons to manage multi-value fields
- For **Modify** and **Delete**, click an item in the list to select it first, then click the toolbar button
- Click **Save** inside the popup to confirm changes, or **X** to cancel them

#### Navigation History
- The **Back** and **Forward** toolbar buttons navigate between previously visited field tabs

#### Viewing and Printing Schedules
- Select the **Schedule** tab, choose a count and optimization setting, then generate
- Click **View** to open the schedule viewer — browse by faculty, room, lab, or day
- Click **Print** to export the schedules as a PDF

#### AI Assistant (Clippy)
- Click **Chat** in the top-right toolbar to open the assistant panel
- Type a command and click **Send** — Clippy can add, modify, and delete entries, and generate schedules
- See [Prompting the AI Assistant](#prompting-the-ai-assistant) for tips

---

## Prompting the AI Assistant

When prompting the AI, be direct. State what you want it to do (add/modify/delete/generate) then the name of what should be altered.

```
Delete lab 'WindowsOS'.
```

For more complex elements, like adding a faculty member, ensure that you specify all required elements needed for the Faculty member within the prompt.

```
Add a faculty member 'Killian' that has 12 min credits, 12 max credits, 3 unique course limit and 3 max days.
Ensure that Killian has time slots of MON 12:00-13:00, TUE 12:00-13:00, A course preference for CMSC 476,
CMSC 380, a Room preference for Roddy 147, A lab preference for Mac, Linux, and mandatory days 'MON' and 'TUE.'
```

**Generating schedules**

For generating schedules, specify whether you want the schedule to be optimized or unoptimized, and how many schedules you would like to generate. 

**Note**

The AI assistant has no chat history. If it does not confirm the task was completed, alter your prompt and try again.

---

## Running Tests

Run all tests:
```bash
uv run pytest
```

Run a specific test file:
```bash
uv run pytest test/test_conflict.py
```

Available test files:
    `test_conflict.py`
    `test_course.py`
    `test_faculty.py`
    `test_lab.py`
    `test_room.py`
    `test_time_slot_config.py`

---

## Design Patterns

#### Model-View-Controller (MVC)
- **Pattern:** Divides an application into three components to separate data logic from UI
- **Implementation:** The application is split into three distinct layers:
    - Model handles data, application state, AI logic, and API calls
    - View handles DOM elements, layout, and rendering
    - Controller facilitates user interaction and coordinates between Model and View
- **Files:** `src/model/`, `src/view/`, `src/controller/`, `src/controller/navigation_model.js`, `src/controller/navigation_view.js`, `src/controller/navigation_controller.js`

#### Memento
- **Pattern:** Captures and restores an object's internal state
- **Implementation:** When navigating between views, the current view's state is saved before moving to a new one. The Back and Forward buttons restore those saved states, giving the application browser-like navigation history without the controller needing to know the details of what was saved
- **File:** `src/controller/navigation_controller.js`

#### Prototype
- **Pattern:** A fully initialized instance to be copied or cloned
- **Implementation:** On startup, the empty configuration is loaded once and stored. When a new configuration file is loaded, the program clones the empty configuration prototype and populates it with the new data
- **File:** `src/model/schedule/schedule.py`

#### Factory
- **Pattern:** Creates instances of several derived classes from a single point
- **Implementation:** `build_tools()` constructs and returns a list of `StructuredTool` objects for every scheduler operation. `get_agent()` calls `build_tools()` and passes the result into `create_agent()` to assemble the final AI agent. The rest of the application calls `run_agent()` without needing to know how the tools or agent were built
- **File:** `src/model/AI/agent.py`

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

Copyright © 2026 Antifreeze
