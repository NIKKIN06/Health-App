import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# activities_table_sql = """CREATE TABLE IF NOT EXISTS activities (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER NOT NULL,
#                         activity_type TEXT NOT NULL,
#                         duration_minutes INTEGER NOT NULL,
#                         calories_burned REAL NOT NULL,
#                         date TEXT NOT NULL,
#                         FOREIGN KEY (user_id) REFERENCES users (id)
#                         );"""

class ActivityTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("My Activity")
        self.root.geometry("800x400")
        self.root.configure(bg="white")

        self.selected_button = None
        self.nav_buttons = {}
        self.user = User()  # Assuming you have a User class
        self.activity = Activity(self.user)

        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        self.on_nav_click("Activity")  # Default selected menu item

    def create_header(self):
        header = tk.Frame(self.root, bg="#58C75C", height=50)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="My Activity",
            font=("Helvetica", 16, "bold"),
            bg="#58C75C",
            fg="white"
        )
        title.pack(pady=10)

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#c4c4c4", width=150)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        menu_items = {
            "Profile": "👤",
            "Nutrition": "🍴",
            "Activity": "🏃",
            "CalorieC": "📊",
            "Reg_Win": "📝",
            "Help": "❓"
        }

        for name, icon in menu_items.items():
            btn = tk.Button(
                sidebar,
                text=f"  {icon}  {name}",
                anchor="w",
                justify="left",
                font=("Arial", 10),
                bg="#c4c4c4",
                fg="black",
                bd=0,
                padx=10,
                pady=8,
                activebackground="#a0a0a0",
                command=lambda n=name: self.on_nav_click(n)
            )
            btn.pack(fill=tk.X)
            self.nav_buttons[name] = btn

    def create_main_content(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Створюємо контейнер для форми та зображення
        top_container = tk.Frame(self.main_frame, bg="white")
        top_container.pack(fill=tk.X, pady=10)

        # Створюємо рамку для форми (ліва частина)
        workout_frame = tk.LabelFrame(top_container, text="Workout", bg="white", padx=10, pady=10)
        workout_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Activity selection
        tk.Label(workout_frame, text="Select activity:", bg="white").grid(row=0, column=0, sticky="w")
        self.activity_var = tk.StringVar()
        activities = list(self.activity.activities.keys())
        self.activity_combobox = ttk.Combobox(workout_frame, textvariable=self.activity_var, values=activities)
        self.activity_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Time entry
        tk.Label(workout_frame, text="Enter time (minutes):", bg="white").grid(row=1, column=0, sticky="w")
        self.time_entry = tk.Entry(workout_frame)
        self.time_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Add activity button
        add_btn = tk.Button(workout_frame, text="Add Activity", command=self.add_activity, bg="#58C75C", fg="white")
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Додаємо зображення (права частина)
        try:
            self.photo = tk.PhotoImage(file="running.png")
            # Масштабуємо зображення, якщо потрібно
            self.photo = self.photo.subsample(5, 5)  # Зменшуємо в 2 рази
            image_label = tk.Label(top_container, image=self.photo, bg="white")
            image_label.pack(side=tk.LEFT, padx=20)
        except:
            print("Не вдалося завантажити зображення")

        # Activity history table
        history_frame = tk.LabelFrame(self.main_frame, text="Activity History", bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Activity Type", "Duration (min)", "Calories", "Date")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_activity(self):
        activity_name = self.activity_var.get()
        time_str = self.time_entry.get()

        if not activity_name:
            messagebox.showerror("Error", "Please select an activity")
            return

        try:
            time_spent = float(time_str)
            if time_spent <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for time")
            return

        if activity_name not in self.activity.activities:
            messagebox.showerror("Error", "Invalid activity selected")
            return

        calories_burned = self.activity.activities[activity_name] * time_spent

        self.activity.today_activity.append({
            "activity": activity_name,
            "time": time_spent,
            "calories_burned": calories_burned,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        messagebox.showinfo("Success",
                            f"Activity added: {activity_name} for {time_spent} min\n"
                            f"Calories burned: {calories_burned:.2f} kcal")

        self.update_activity_table()
        self.activity_var.set("")
        self.time_entry.delete(0, tk.END)

        # Update user's burned calories
        self.user.nutrition.burn_calories(calories_burned)

    def update_activity_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add new data
        for idx, activity in enumerate(self.activity.today_activity, 1):
            self.tree.insert("", tk.END, values=(
                idx,
                activity["activity"],
                activity["time"],
                f"{activity['calories_burned']:.2f}",
                activity.get("date", "")
            ))

    def on_nav_click(self, name):
        print(f"Menu button clicked: {name}")
        for btn in self.nav_buttons.values():
            btn.configure(bg="#c4c4c4")
        self.nav_buttons[name].configure(bg="#a0a0a0")
        self.selected_button = name


class Activity:
    def __init__(self, user):
        self.user = user
        self.catalog_path = "activity_catalog.json"
        self.activities = self.load_activity_catalog()
        self.today_activity = []

    def load_activity_catalog(self):
        if not os.path.exists(self.catalog_path):
            default_activities = {
                "Running": 10,
                "Swimming": 8,
                "Cycling": 7,
                "Weight Training": 5,
                "Yoga": 3,
                "Walking": 4
            }
            with open(self.catalog_path, "w") as file:
                json.dump(default_activities, file)
            return default_activities
        with open(self.catalog_path, "r") as file:
            return json.load(file)

    def get_today_activity(self):
        return sum(activity["calories_burned"] for activity in self.today_activity)


class User:
    def __init__(self):
        self.nutrition = self.Nutrition()

    class Nutrition:
        def burn_calories(self, calories):
            print(f"Burned {calories} calories")


if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityTrackerApp(root)
    root.mainloop()