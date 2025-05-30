import json
import os
from user import User

class RegistrationWindow:
    def __init__(self, db_path="users.json"):
        self.db_path = db_path
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                data = json.load(file)
                return [User.from_dict(u) for u in data]
        return []

    def save_users(self):
        with open(self.db_path, 'w') as file:
            json.dump([u.to_dict() for u in self.users], file, indent=4)

    def register_new_user(self):
        print("\n--- Register New User ---")
        name = input("Name: ")
        email = input("Email: ")
        birth_date = input("Birth date (YYYY-MM-DD): ")
        weight = int(input("Weight (kg): "))
        height = int(input("Height (cm): "))
        sex = input("Sex (M/F): ")
        goal = input("Goal (lose/gain/maintain): ")
        activity_factor = input("Level of Activity (1.2/1.55/1.9): ")
        new_user = User(name, email, birth_date, weight, height, sex, goal, activity_factor)
        self.users.append(new_user)
        self.save_users()
        print("User registered successfully.\n")
        return new_user

    def login_user(self):
        print("\n--- Login ---")
        email = input("Enter your email: ")
        for user in self.users:
            if user.email == email:
                print("Login successful.\n")
                return user
        print("User not found. Try registering.\n")
        return None
