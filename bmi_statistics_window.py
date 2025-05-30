import customtkinter as ctk
from tkinter import ttk
from calorie_counting import CalorieCounting

class StatisticsWindow(ctk.CTkToplevel, CalorieCounting):
    def __init__(self, parent, calorie_counter):
        super().__init__(parent)
        self.parent = parent
        self.calorie_counter = calorie_counter

        self.geometry("900x600")
        self.title("Statistics")
        self.configure(fg_color="white")

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"900x600+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Хедер (розтягнутий по ширині)
        self.create_header()

        # Основний фрейм для всього вмісту
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Дропдаун меню + таблиця
        self.dropdown = self.create_dropdown()
        self.table = self.create_table(self.calorie_counter, period="week")

        # Кнопки
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.back_button = self.create_back_button(self.button_frame)
        self.save_button = self.create_save_button(self.button_frame)

    def on_close(self):
        self.destroy()
        self.parent.deiconify()

    def create_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#ff4fd4",
            height=50,
            corner_radius=0
        )
        header.pack(fill="x", side="top")

        label = ctk.CTkLabel(
            header,
            text="BMI calculator",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        label.pack(pady=10)

    def create_dropdown(self):
        options = {
            "Calories per week": "week",
            "Calories per month": "month",
            "Calories per half year": "halfyear"
        }

        self.period_options = options

        dropdown = ctk.CTkOptionMenu(
            master=self.main_frame,
            values=list(options.keys()),
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
            command=self.update_table_for_selected_period
        )
        dropdown.set("Calories per week")
        dropdown.pack(pady=10)
        return dropdown

    def update_table_for_selected_period(self, selected_label):
        period = self.period_options[selected_label]
        for item in self.table.get_children():
            self.table.delete(item)
        new_data = self.calorie_counter.get_summary_table_data(period)
        for row in new_data:
            self.table.insert("", "end", values=row)

    def create_table(self, calorie_counter, period="week"):
        self.table_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Inter", 13, "bold"))
        style.configure("Custom.Treeview", font=("Inter", 12), rowheight=30)

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.table = ttk.Treeview(
            self.table_frame,
            columns=("date", "calories_consumed", "calorie_norm", "final_result"),
            show="headings",
            yscrollcommand=scrollbar.set,
            style = "Custom.Treeview"
        )
        scrollbar.config(command=self.table.yview)

        self.table.heading("date", text="Date")
        self.table.heading("calories_consumed", text="Calories consumed")
        self.table.heading("calorie_norm", text="Calorie norm")
        self.table.heading("final_result", text="Final result")

        self.table.column("date", width=160, anchor="center")
        self.table.column("calories_consumed", width=160, anchor="center")
        self.table.column("calorie_norm", width=160, anchor="center")
        self.table.column("final_result", width=160, anchor="center")

        # Вставка початкових даних
        data_rows = calorie_counter.get_summary_table_data(period)
        for row in data_rows:
            self.table.insert("", "end", values=row)

        self.table.pack(fill="both", expand=True)
        return self.table

    def create_back_button(self, parent):
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
        return button

    def create_save_button(self, parent):
        button = ctk.CTkButton(
            parent,
            text="Save data",
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
        return button
