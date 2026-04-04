import os
from scheduler import (
    Scheduler,
    load_config_from_file,
    CombinedConfig
    
)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import copy

from model.schedule.conflict import conflict
from model.schedule.course import course
from model.schedule.faculty import faculty
from model.schedule.lab import lab
from model.schedule.room import room



class Schedule():
    # Initialize Schedule
    # Initializes all scheduling submodules and creates an empty configuration
    # Sets up conflict, course, faculty, lab, and room handlers
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        empty_path = os.path.join(base_dir, "../../view/static/empty.json")
        self.conflict = conflict()
        self.course = course()
        self.faculty = faculty()
        self.lab = lab()
        self.room = room()
        self.config = load_config_from_file(CombinedConfig, empty_path)
        self.empty_config = copy.deepcopy(self.config)
        self.result = []

    #--------------#
    #FILE MANAGEMENT

    # Load Configuration
    # Loads a configuration file into the scheduler
    # Replaces the current configuration with the loaded file
    # Parameters: Configuration file path
    def load_config(self, file_name):
        try:
            
            if os.path.basename(file_name) == "empty.json":
                self.load_empty_prototype()
                print("Loaded from prototype.")
                return

            self.config = load_config_from_file(CombinedConfig, file_name)
            print("Config loaded successfully.")

        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        
    def load_empty_prototype(self):
    
        self.config = copy.deepcopy(self._empty_prototype)
        self.result = []
        return
    # Save Configuration
    # Saves the current configuration to a file
    def save_config(self):
        print("Enter the path of the file you would like to save to, including extension\n==> ",end="")
        file_name = input()
        try:
            with open(file_name, "w") as f:
                f.write(self.config.model_dump_json(indent=2))
                print("Config saved successfully.")
        except Exception as e:
            print("Could not save file, try again")
            print(e)
        return

    # Print Configuration
    # Prints the current configuration in a human-readable format
    def print_config(self):
        self.conflict.print_conflicts(self.config)
        self.course.print_courses(self.config)
        self.faculty.print_faculty(self.config)
        self.lab.print_labs(self.config)
        self.room.print_rooms(self.config)
        return

    #Run Scheduler
    #Executes the scheduling engine using the current configuration
    #Prompts the user for generation limits, output format, and optimization options
    #Generates schedules and writes results to a file
    def run_scheduler(self, limit: int = 10, optimize: bool = True):

        if optimize:
            self.config.optimizer_flags = [
                "faculty_course",
                "faculty_room",
                "faculty_lab",
                "same_room",
                "same_lab",
                "pack_rooms"
            ]
        else:
            self.config.optimizer_flags = []

        try:
            sched = Scheduler(self.config)
        except Exception as e:
            print("Scheduler error:", e)
            return []

        self.result = []

        for model in sched.get_models():
            self.result.append(model)

            if len(self.result) >= limit:
                break

        return self.result


    #Print Schedule
    #Displays the current schedule in a human-readable, formatted layout
    #Prints courses, faculty assignments, classes, time slots, and misc settings
    #Requires a loaded configuration   
    def print_schedule(self, count: int = 1):

        if not self.result:
            return []

        count = min(count, len(self.result))

        output = []

        for i in range(count):
            
            schedule_lines = []

            for sch in self.result[i]:
                schedule_lines.append(sch.as_csv())

            output.append(schedule_lines)

        return output

    def export_schedule_csv(self, index: int):
        if not self.result:
            return ""

        model = self.result[index]

        lines = []

        for sch in model:
            lines.append(sch.as_csv())

        return "\n".join(lines)

    def export_schedules_pdf(self):

        if not self.result:
            return None

        buffer = io.BytesIO()

        styles = getSampleStyleSheet()

        elements = []

        for i, model in enumerate(self.result):

            elements.append(Paragraph(f"Schedule {i+1}", styles["Heading2"]))
            elements.append(Spacer(1, 10))

            table_data = [["Course", "Faculty", "Room", "Lab", "Time"]]

            for sch in model:

                parts = sch.as_csv().split(",")

                if len(parts) < 5:
                    continue

                table_data.append([p.strip() for p in parts[:5]])

            table = Table(table_data)

            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
                ("GRID", (0,0), (-1,-1), 1, colors.black)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 30))

        doc = SimpleDocTemplate(buffer)

        doc.build(elements)

        buffer.seek(0)

        return buffer
