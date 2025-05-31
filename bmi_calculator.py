import customtkinter as ctk
from calorie_counting import CalorieCounting
from bmi_statistics_window import StatisticsWindow

class BMICalculator(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self.calorie_counter = CalorieCounting(user)
        self.advice_list = self.calorie_counter.get_nutrition_advice()
        self.current_advice_index = 0

        self.content_wrapper = ctk.CTkFrame(self, fg_color="white")
        self.content_wrapper.place(relx=0.5, rely=0.5, anchor="center")

        self.configure(fg_color="white", corner_radius = 0)

        self.create_header()
        self.create_advice_box()
        self.create_circles()
        self.create_main_buttons()

    def update_circles(self):
        for widget in self.circle_frame.winfo_children():
            widget.destroy()

        consumed = self.calorie_counter.get_consumed_nutrition()
        norm_protein, norm_fat, norm_carbs, norm_calories = self.calorie_counter.get_norm()
        percentages = self.calorie_counter.get_nutrition_percentage()

        canvas_data = [
            (percentages['calories_percent'], "Calories", "", f"{int(consumed[3])} / {int(norm_calories)}"),
            (percentages['protein_percent'], "Protein", "", f"{int(consumed[0])} / {int(norm_protein)}"),
            (percentages['carb_percent'], "Carbs", "", f"{int(consumed[2])} / {int(norm_carbs)}"),
            (percentages['fat_percent'], "Fat", "", f"{int(consumed[1])} / {int(norm_fat)}"),
        ]

        for i, (percent, label, _, value) in enumerate(canvas_data):
            if percent > 110:
                color = "red"
            elif percent >= 90:
                color = "green"
            else:
                color = "orange"
            canvas_data[i] = (percent, label, color, value)

        for percent, label, color, value in canvas_data:
            canvas = ctk.CTkCanvas(self.circle_frame, width=160, height=180, bg="white", highlightthickness=0)
            canvas.pack(side="left", padx=15, pady=10)
            self.draw_circle(canvas, percent, label, color, value)

    def show(self):
        self.update_circles()
        self.lift()
        self.pack(expand=True, fill="both")

    def hide(self):
        self.pack_forget()

    def create_header(self):
        """Create the top header bar with title"""
        header = ctk.CTkFrame(
            self,
            fg_color="#ff4fd4",
            height=50,
            corner_radius=0
        )
        header.pack(fill="x")

        label = ctk.CTkLabel(
            header,
            text="BMI calculator",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        label.place(x=143 + (700 - 143) // 2, rely=0.5, anchor="center")

    def create_advice_box(self):
        """Create the advice box that cycles through nutrition tips"""
        self.advice_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            border_width=1,
            border_color="gray",
            width=600,
            height=120,
            corner_radius=15
        )
        self.advice_frame.pack(pady=20)

        self.advice_label = ctk.CTkLabel(
            self.advice_frame,
            text="Loading advice...",
            font=("Inter", 20),
            text_color="black",
            justify="left",
            wraplength=580
        )
        self.advice_label.place(relx=0.5, rely=0.5, anchor="center")

        self.update_advice_text()

    def update_advice_text(self):
        """Start the fade-out/fade-in animation for cycling tips"""
        if not self.advice_list:
            return
        self.fade_out_text(0)

    def fade_out_text(self, step):
        """Fade out current text before replacing it"""
        if step <= 10:
            gray_value = int(0 + (150 - 0) * (step / 10))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            self.advice_label.configure(text_color=color)
            self.advice_label.after(100, lambda: self.fade_out_text(step + 1))
        else:
            self.show_next_advice(0)

    def show_next_advice(self, step):
        """Fade in the next piece of advice"""
        if step == 0:
            current_text = self.advice_list[self.current_advice_index]
            self.advice_label.configure(text=current_text)
            self.current_advice_index = (self.current_advice_index + 1) % len(self.advice_list)

        if step <= 10:
            gray_value = int(150 - (150 * (step / 10)))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            self.advice_label.configure(text_color=color)
            self.advice_label.after(100, lambda: self.show_next_advice(step + 1))
        else:
            self.advice_label.after(8000, self.update_advice_text)

    def create_circles(self):
        """Draw circular progress charts for calories, proteins, carbs, and fats"""
        self.circle_frame = ctk.CTkFrame(self, fg_color="white")
        self.circle_frame.pack(pady=10)
        self.update_circles()

    def draw_circle(self, canvas, percent, label_text, color, value):
        """Draw a single circular progress bar"""
        if percent > 100:
            extent = 359.999
            draw_color = "red"
        else:
            extent = percent * 3.6
            draw_color = color

        canvas.create_oval(15, 15, 145, 145, outline="gray", width=10)
        canvas.create_arc(15, 15, 145, 145, start=90, extent=-extent, outline=draw_color, style="arc", width=10)
        canvas.create_text(80, 80, text=value, font=("Inter", 14, "bold"))
        canvas.create_text(80, 165, text=label_text, font=("Inter", 14))

    def open_statistics_window(self):
        stat_win = StatisticsWindow(self.master, self.calorie_counter)
        stat_win.grab_set()

    def create_main_buttons(self):
        """Create main action buttons (for statistics)"""
        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=20)

        btn1 = ctk.CTkButton(
            button_frame,
            text="Statistics",
            width=230,
            height=50,
            font=("Inter", 15, "bold"),
            text_color="white",
            corner_radius=7,
            fg_color="#ff4fd4",
            hover_color="#e03ebf",
            command=self.open_statistics_window
        )
        btn1.pack(side="left", padx=10)