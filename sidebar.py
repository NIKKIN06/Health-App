import customtkinter as ctk
from PIL import Image

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        """Custom sidebar button with predefined styling"""
        super().__init__(
            master=master,
            width=150,
            height=32,
            font=("Inter", 15),
            fg_color="#8D8989",
            hover_color="#665E5E",
            text_color="black",
            corner_radius=0,
            anchor="w",
            **kwargs
        )

class Button_Icon(ctk.CTkImage):
    def __init__(self, image_link, **kwargs):
        """Icon for sidebar buttons, uses the same image for both light and dark themes"""
        super().__init__(
            light_image=Image.open(image_link),
            dark_image=Image.open(image_link),
            size=(35, 19),
            **kwargs
        )

    @classmethod
    def create(cls, link, **kwargs):
        """Factory method for creating an icon instance"""
        icon = cls(image_link=link, **kwargs)
        return icon

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        """Initializes the sidebar with navigation buttons. """
        super().__init__(master, fg_color="#c4c4c4", width=200, height=480, corner_radius=0)
        self.switch_callback = switch_callback
        self.place(x=0, y=0)

        # Sidebar title
        ctk.CTkLabel(
            self,
            text="Menu",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="black",
        ).place(x=25, y=10)

        # Initialize icons for the buttons
        profile_icon = Button_Icon.create("icons/profile_icon.png")
        nutrition_icon = Button_Icon.create("icons/nutrition_icon.png")
        activity_icon = Button_Icon.create("icons/activity_icon.png")
        calorie_counting_icon = Button_Icon.create("icons/calorie_icon.png")
        reg_win_icon = Button_Icon.create("icons/reg_win_icon.png")
        help_icon = Button_Icon.create("icons/help_icon.png")

        # Button list with corresponding commands and icons
        self.buttons = []
        self.buttons.append(SidebarButton(self, text="Profile", image=profile_icon, command=lambda: switch_callback("Nutrition")))
        self.buttons.append(SidebarButton(self, text="Nutrition", image=nutrition_icon, command=lambda: switch_callback("Nutrition")))
        self.buttons.append(SidebarButton(self, text="Activity", image=activity_icon, command=lambda: switch_callback("Nutrition")))
        self.buttons.append(SidebarButton(self, text="CalorieC", image=calorie_counting_icon, command=lambda: switch_callback("BMI")))
        self.buttons.append(SidebarButton(self, text="Reg_Win", image=reg_win_icon, command=lambda: switch_callback("Nutrition")))
        self.buttons.append(SidebarButton(self, text="Help", image=help_icon, command=lambda: switch_callback("Nutrition")))

        # Place the buttons vertically with spacing
        y_offset = 50
        for button in self.buttons:
            button.place(x=25, y=y_offset)
            y_offset += 41