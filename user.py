import datetime
from nutrition import Nutrition

class User:
    def __init__(self, name, email, birth_date, weight, height, sex, goal, activity_factor):
        self.name = name
        self.email = email
        self.birth_date = birth_date  # у форматі YYYY-MM-DD
        self.weight = weight
        self.height = height
        self.sex = sex  # 'M' або 'F'
        self.goal = goal  # 'lose', 'gain', 'maintain'
        self.activity_factor = float(activity_factor) # 1.2  1.55  1.9
    def get_age(self):
        today = datetime.date.today()
        birth = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def update_profile(self):
        print("\n--- Update Profile ---")
        self.name = input(f"Name [{self.name}]: ") or self.name
        self.email = input(f"Email [{self.email}]: ") or self.email
        bd = input(f"Birth Date [{self.birth_date}] (YYYY-MM-DD): ") or self.birth_date
        self.birth_date = bd
        self.weight = int(input(f"Weight [{self.weight} kg]: ") or self.weight)
        self.height = int(input(f"Height [{self.height} cm]: ") or self.height)
        self.sex = input(f"Sex (M/F) [{self.sex}]: ") or self.sex
        self.goal = input(f"Goal (lose/gain/maintain) [{self.goal}]: ") or self.goal
        self.activity_factor = input(f"Level of Activity (1.2/1.55/1.9) [{self.activity_factor}]: ") or self.activity_factor
        print("Profile updated successfully.\n")

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "birth_date": self.birth_date,
            "weight": self.weight,
            "height": self.height,
            "sex": self.sex,
            "goal": self.goal,
            "activity_factor": self.activity_factor
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["name"], data["email"], data["birth_date"],
            data["weight"], data["height"], data["sex"], data["goal"],
            data["activity_factor"]
        )

    def display_profile(self):
        print("\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.get_age()} years")
        print(f"Weight: {self.weight} kg")
        print(f"Height: {self.height} cm")
        print(f"Sex: {self.sex}")
        print(f"Goal: {self.goal}\n")
        print(f"Activity factor: {self.activity_factor}\n")
