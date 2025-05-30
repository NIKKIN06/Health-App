import customtkinter as ctk
# from tkinter import ttk
from calorie_counting import CalorieCounting
from sidebar import Sidebar
# from user import User
from bmi_statistics_window import StatisticsWindow
# from nutrition_window import Create_Window

class FuncButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            width=230,
            height=50,
            font=("Inter", 15, "bold"),
            text_color="white",
            corner_radius=7,
            **kwargs
        )

class BMICalculatorApp:
    def __init__(self, on_nav_click, user=None):
        self.user = user
        self.advice_frames = []
        self.calorie_counter = CalorieCounting(user)
        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.0)

        self.root = ctk.CTk()
        self.root.title("BMI calculation")
        self.root.geometry("800x480")
        self.root.configure(fg_color="white")

        # Центрування вікна
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 480) // 2
        self.root.geometry(f"800x480+{x}+{y}")

        self.nav_buttons = {}

        self.create_header()
        self.sidebar = Sidebar(self.root, self.user, on_nav_click)
        self.create_main_content()

        self.root.mainloop()

    def create_header(self):
        header = ctk.CTkFrame(
            self.root,
            fg_color="#ff4fd4",
            width=800,
            height=50,
            corner_radius=0
        )
        header.place(x=0, y=0)

        label = ctk.CTkLabel(
            header,
            text="BMI calculator",
            text_color="white",
            font=("Inter", 20, "bold")
        )

        # Відцентровуємо відносно видимої частини, тобто зсунемо текст на півширини після бокової панелі
        label.place(x=143 + (800 - 143) // 2, rely=0.5, anchor="center")

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", width=660, height=440)
        self.main_frame.place(x=173, y=60)

        self.create_advice_box()
        self.create_circles()
        self.create_main_buttons()

    def create_advice_box(self):
        self.advice_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            border_width=1,
            border_color="gray",
            width=600,
            height=120,
            corner_radius=15
        )
        self.advice_frame.pack(pady=10)

        self.advice_label = ctk.CTkLabel(
            self.advice_frame,
            text="Loading advice...",
            font=("Inter", 20),  # Збільшено шрифт
            text_color="black",
            justify="left",
            wraplength=580
        )
        self.advice_label.place(relx=0.5, rely=0.5, anchor="center")

        # Генеруємо список порад
        self.advice_list = self.calorie_counter.get_nutrition_advice()
        self.current_advice_index = 0

        self.update_advice_text()

    def update_advice_text(self):
        if not hasattr(self, 'advice_list') or not self.advice_list:
            return

        self.fade_out_text(0)  # Починаємо fade-out

    def fade_out_text(self, step):
        # Всього 10 кроків для 1 секунди (1000 мс / 10 = 100 мс на крок)
        if step <= 10:
            # Від чорного (0,0,0) до сірого (150,150,150)
            gray_value = int(0 + (150 - 0) * (step / 10))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            self.advice_label.configure(text_color=color)
            self.advice_label.after(100, lambda: self.fade_out_text(step + 1))
        else:
            self.show_next_advice(0)  # Починаємо fade-in

    def show_next_advice(self, step):
        if step == 0:
            current_text = self.advice_list[self.current_advice_index]
            self.advice_label.configure(text=current_text)
            self.current_advice_index = (self.current_advice_index + 1) % len(self.advice_list)

        if step <= 10:
            # Від сірого (150,150,150) до чорного (0,0,0)
            gray_value = int(150 - (150 * (step / 10)))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            self.advice_label.configure(text_color=color)
            self.advice_label.after(100, lambda: self.show_next_advice(step + 1))
        else:
            # Після появи чекаємо 8 секунд, потім знову update
            self.advice_label.after(8000, self.update_advice_text)

    def create_circles(self):
        circle_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        circle_frame.pack(pady=10, fill=None, expand=True)

        # Отримуємо фактичні значення
        consumed = self.calorie_counter.get_consumed_nutrition()  # (protein, fat, carbs, calories)
        norm_protein, norm_fat, norm_carbs, norm_calories = self.calorie_counter.get_norm()
        percentages = self.calorie_counter.get_nutrition_percentage()  # {'calories_percent': ..., ...}

        # Підготовка даних для побудови
        canvas_data = [
            (percentages['calories_percent'], "Calories", "", f"{int(consumed[3])} / {int(norm_calories)}"),
            (percentages['protein_percent'], "Protein", "", f"{int(consumed[0])} / {int(norm_protein)}"),
            (percentages['carb_percent'], "Carbs", "", f"{int(consumed[2])} / {int(norm_carbs)}"),
            (percentages['fat_percent'], "Fat", "", f"{int(consumed[1])} / {int(norm_fat)}"),
        ]

        # Визначаємо кольори на основі відсотків
        for i, (percent, label, _, value) in enumerate(canvas_data):
            if percent > 110:
                color = "red"  # Червоний - перевищення норми
            elif percent >= 90:
                color = "green"  # Зелений - майже досягнута норма
            else:
                color = "orange"  # Жовтий/помаранчевий - ще далеко до норми

            # Оновлюємо дані з визначеним кольором
            canvas_data[i] = (percent, label, color, value)

        # Створюємо круги з відповідними кольорами
        for percent, label, color, value in canvas_data:
            canvas = ctk.CTkCanvas(circle_frame, width=160, height=180, bg="white", highlightthickness=0)
            canvas.pack(side="left", padx=15, pady=10)
            self.draw_circle(canvas, percent, label, color, value)

    def draw_circle(self, canvas, percent, label_text, color, value):
        # Якщо перевищено 100%, встановлюємо extent = 360 і колір = червоний
        if percent > 100:
            extent = 359.999
            draw_color = "red"
        else:
            extent = percent * 3.6
            draw_color = color

        # Фонове коло (сіре)
        canvas.create_oval(15, 15, 145, 145, outline="gray", width=10)

        # Прогрес (смужка)
        canvas.create_arc(15, 15, 145, 145, start=90, extent=-extent, outline=draw_color, style="arc", width=10)

        # Текст значення (наприклад, 120 / 200)
        canvas.create_text(80, 80, text=value, font=("Inter", 14, "bold"))

        # Підпис (Calories, Protein, тощо)
        canvas.create_text(80, 165, text=label_text, font=("Inter", 14))

    def create_main_buttons(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        frame.pack(pady=20)

        btn1 = FuncButton(
            frame,
            text="Statistics",
            fg_color="#ff4fd4",
            hover_color="#e03ebf",
            command=lambda: self.on_main_button_click("Statistics")
        )
        btn1.pack(side="left", padx=10)

    # def on_nav_click(self, name):
    #     print(f"Натиснуто кнопку меню: {name}")
    #     for btn in self.nav_buttons.values():
    #         btn.configure(fg_color="#8D8989")
    #     self.nav_buttons[name].configure(fg_color="#665E5E")

    def on_main_button_click(self, name):
        print(f"Натиснуто кнопку: {name}")
        if name == "Statistics":
            self.root.withdraw()  # Сховати головне вікно
            StatisticsWindow(self.root, self.calorie_counter)