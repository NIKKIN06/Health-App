import customtkinter as ctk
from tkinter import ttk
from calorie_counting import CalorieCounting

class StatisticsWindow(ctk.CTkToplevel, CalorieCounting):
    def __init__(self, parent, calorie_counter):
        super().__init__(parent)
        self.parent = parent
        self.calorie_counter = calorie_counter

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Initial setup for the statistics window"""
        self.geometry("900x600")
        self.title("Statistics")
        self.configure(fg_color="white")

        # Center the window on screen
        self.update_idletasks()
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (screen_w - 900) // 2
        y = (screen_h - 600) // 2
        self.geometry(f"900x600+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        """Create all widgets for the window"""
        self.create_header()

        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.period_options = {
            "Calories per week": "week",
            "Calories per month": "month",
            "Calories per half year": "halfyear"
        }

        self.dropdown = self.create_dropdown()
        self.table = self.create_table(period="week")

        self.create_buttons()

    def on_close(self):
        """Close statistics window and return to main window"""
        self.destroy()
        self.parent.deiconify()

    def create_header(self):
        """Create the top header with the app title"""
        header = ctk.CTkFrame(self, fg_color="#ff4fd4", height=50, corner_radius=0)
        header.pack(fill="x", side="top")

        label = ctk.CTkLabel(
            header,
            text="BMI Calculator",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        label.pack(pady=10)

    def create_dropdown(self):
        """Create the dropdown to select data period"""
        dropdown = ctk.CTkOptionMenu(
            master=self.main_frame,
            values=list(self.period_options.keys()),
            width=550,
            height=40,
            corner_radius=7,
            fg_color="#c4c4c4",
            button_color="#AAAAAA",
            button_hover_color="#848484",
            text_color="black",
            dropdown_fg_color="#C8C8C8",
            dropdown_text_color="black",
            font=("Inter", 16),
            dropdown_font=("Inter", 14),
            command=self.update_table
        )
        dropdown.set("Calories per week")
        dropdown.pack(pady=10)
        return dropdown

    def create_table(self, period="week"):
        """Create table with calorie statistics"""
        self.table_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Inter", 13, "bold"))
        style.configure("Custom.Treeview", font=("Inter", 12), rowheight=30)

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        table = ttk.Treeview(
            self.table_frame,
            columns=("date", "calories_consumed", "calorie_norm", "final_result"),
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Custom.Treeview"
        )
        scrollbar.config(command=table.yview)

        headers = {
            "date": "Date",
            "calories_consumed": "Calories Consumed",
            "calorie_norm": "Calorie Norm",
            "final_result": "Final Result"
        }

        for col, title in headers.items():
            table.heading(col, text=title)
            table.column(col, width=160, anchor="center")

        self.fill_table(table, period)
        table.pack(fill="both", expand=True)
        return table

    def fill_table(self, table, period):
        """Fill table with data from the calorie counter"""
        rows = self.calorie_counter.get_summary_table_data(period)
        for row in rows:
            table.insert("", "end", values=row)

    def update_table(self, selected_label):
        """Clear and refill table based on selected dropdown option"""
        period = self.period_options[selected_label]
        self.table.delete(*self.table.get_children())
        self.fill_table(self.table, period)

    def create_buttons(self):
        """Create 'Back' and 'Save' buttons"""
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.create_back_button(button_frame)
        self.create_save_button(button_frame)

    def create_back_button(self, parent):
        """Create button to close statistics and return"""
        button = ctk.CTkButton(
            parent,
            text="Back",
            font=("Inter", 17, "bold"),
            width=230,
            height=50,
            fg_color="#ff4fd4",
            hover_color="#e03ebf",
            corner_radius=8,
            text_color="white",
            command=self.on_close
        )
        button.pack(side="left", padx=20)

    def create_save_button(self, parent):
        """Create button to save the current table to file"""
        button = ctk.CTkButton(
            parent,
            text="Save Data",
            font=("Inter", 17, "bold"),
            width=230,
            height=50,
            fg_color="#ff4fd4",
            hover_color="#e03ebf",
            text_color="white",
            corner_radius=8,
            command=lambda: self.calorie_counter.save_table_to_file(table=self.table)
        )
        button.pack(side="right", padx=20)