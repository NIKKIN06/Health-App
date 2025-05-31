import customtkinter as ctk
from sidebar import Sidebar
from bmi_calculator import BMICalculator
from nutrition_window import NutritionWindow
from user import User
from calorie_counting import CalorieCounting

class CalorieApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calorie Tracker")
        self.geometry("1000x600")
        self.resizable(True, True)

        self.sidebar = Sidebar(self, self.switch_window)
        self.sidebar.pack(side="left", fill="y")

        user = User(
            name="TestUser",
            email="TestUser",
            birth_date="2006-05-12",
            weight=70,
            height=175,
            sex='M',
            goal='M',
            activity_factor=1.2
        )

        self.calorie_counter = CalorieCounting(user)

        self.windows = {
            "BMI": BMICalculator(self, user),
            "Nutrition": NutritionWindow(self, user)
        }

        for window in self.windows.values():
            window.place(x=200, y=0, relwidth=1, relheight=1)
            window.hide()

        self.current_window = None
        self.switch_window("Nutrition")

    def switch_window(self, name):
        if self.current_window:
            self.windows[self.current_window].hide()

        # Updating norm in db
        if name == "BMI":
            self.calorie_counter.update_norm_if_needed("Health_database.db")

        self.current_window = name
        self.windows[name].show()