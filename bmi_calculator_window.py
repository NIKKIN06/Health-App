import customtkinter as ctk
from calorie_counting import CalorieCounting
from bmi_statistics_window import StatisticsWindow

# Global Styles
FONT_HEADER = ("Inter", 20, "bold")
FONT_BODY = ("Inter", 14)
FONT_BOLD = ("Inter", 14, "bold")
FONT_BUTTON = ("Inter", 15, "bold")


class ActionButton(ctk.CTkButton):
    """Reusable styled button for consistent UI"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            width=230,
            height=50,
            font=FONT_BUTTON,
            text_color="white",
            corner_radius=7,
            **kwargs
        )

class BMICalculatorApp:
    def __init__(self, user=None):
        self.user = user
        self.advice_frames = []
        self.calorie_counter = CalorieCounting(user)

        # Configure the main app window
        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.0)

        self.root = ctk.CTk()
        self.root.title("BMI Calculation")
        self.root.geometry("800x480")
        self.root.configure(fg_color="white")
        self.center_window()

        self.create_header()
        self.create_main_content()
        self.root.mainloop()

    def center_window(self):
        """Center the application window on the screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 480) // 2
        self.root.geometry(f"800x480+{x}+{y}")

    def create_header(self):
        """Create the top header bar with title"""
        header = ctk.CTkFrame(self.root, fg_color="#ff4fd4", width=800, height=50, corner_radius=0)
        header.place(x=0, y=0)

        label = ctk.CTkLabel(
            header,
            text="BMI Calculator",
            text_color="white",
            font=FONT_HEADER
        )
        label.place(x=143 + (800 - 143) // 2, rely=0.5, anchor="center")

    def create_main_content(self):
        """Initialize the main layout content below the header"""
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", width=660, height=440)
        self.main_frame.place(x=173, y=60)

        self.create_advice_box()
        self.create_circles()
        self.create_main_buttons()

    def create_advice_box(self):
        """Create the advice box that cycles through nutrition tips"""
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
            font=FONT_HEADER,
            text_color="black",
            justify="left",
            wraplength=580
        )
        self.advice_label.place(relx=0.5, rely=0.5, anchor="center")

        self.advice_list = self.calorie_counter.get_nutrition_advice() or ["No advice available."]
        self.current_advice_index = 0
        self.update_advice_text()

    def update_advice_text(self):
        """Start the fade-out/fade-in animation for cycling tips"""
        if not self.advice_list:
            return
        self.fade_out_text(0)

    def fade_out_text(self, step):
        """Fade out current text before replacing it"""
        if step <= 10:
            gray_value = int(0 + (150 * (step / 10)))
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
        circle_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        circle_frame.pack(pady=10)

        consumed = self.calorie_counter.get_consumed_nutrition()
        norm_protein, norm_fat, norm_carbs, norm_calories = self.calorie_counter.get_norm()
        percentages = self.calorie_counter.get_nutrition_percentage()

        canvas_data = [
            (percentages['calories_percent'], "Calories", f"{int(consumed[3])} / {int(norm_calories)}"),
            (percentages['protein_percent'], "Protein", f"{int(consumed[0])} / {int(norm_protein)}"),
            (percentages['carb_percent'], "Carbs", f"{int(consumed[2])} / {int(norm_carbs)}"),
            (percentages['fat_percent'], "Fat", f"{int(consumed[1])} / {int(norm_fat)}"),
        ]

        for percent, label, value in canvas_data:
            color = self.get_color_by_percent(percent)
            canvas = ctk.CTkCanvas(circle_frame, width=160, height=180, bg="white", highlightthickness=0)
            canvas.pack(side="left", padx=15, pady=10)
            self.draw_circle(canvas, percent, label, color, value)

    def get_color_by_percent(self, percent):
        """Determine circle color based on how close value is to target"""
        if percent > 110:
            return "red"
        elif percent >= 90:
            return "green"
        else:
            return "orange"

    def draw_circle(self, canvas, percent, label_text, color, value):
        """Draw a single circular progress bar"""
        extent = 359.999 if percent > 100 else percent * 3.6
        canvas.create_oval(15, 15, 145, 145, outline="gray", width=10)
        canvas.create_arc(15, 15, 145, 145, start=90, extent=-extent, outline=color, style="arc", width=10)
        canvas.create_text(80, 80, text=value, font=FONT_BOLD)
        canvas.create_text(80, 165, text=label_text, font=FONT_BODY)

    def create_main_buttons(self):
        """Create main action buttons (for statistics)"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        frame.pack(pady=20)

        btn_stats = ActionButton(
            frame,
            text="Statistics",
            fg_color="#ff4fd4",
            hover_color="#e03ebf",
            command=lambda: self.on_main_button_click("Statistics")
        )
        btn_stats.pack(side="left", padx=10)

    def on_main_button_click(self, name):
        """Handle main button actions"""
        print(f"[INFO] Button clicked: {name}")
        if name == "Statistics":
            self.root.withdraw()
            StatisticsWindow(self.root, self.calorie_counter)