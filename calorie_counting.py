# consumed_table_sql = """CREATE TABLE IF NOT EXISTS CONSUMED (
#                         USER TEXT NOT NULL,
#                         DATE DATE NOT NULL,
#                         TOTAL_MASS REAL NOT NULL,
#                         TOTAL_PROTEINS REAL NOT NULL,
#                         TOTAL_FATS REAL NOT NULL,
#                         TOTAL_CARBOHYDRATES REAL NOT NULL,
#                         TOTAL_KCAL INTEGER NOT NULL,
#                         NORM_PROTEINS REAL NOT NULL,
#                         NORM_FATS REAL NOT NULL,
#                         NORM_CARBOHYDRATES REAL NOT NULL,
#                         NORM_KCAL INTEGER NOT NULL
#                         );"""
import csv
from datetime import date, timedelta
from tkinter import filedialog

from DB_control import DBControl

class CalorieCounting:
    def __init__(self, user):
        self.user = user
        self.activity_factor = float(user.activity_factor)
        self.goal = user.goal
        self.norm_calories = self.calculate_total_calories()
        self.norm_bjv = self.calculate_bjv()
        self.db_name = "Health_database.db"

    def change_user_attribute(self, attr_name, new_value):
        """Method to change user attribute and recalculate norms"""
        setattr(self.user, attr_name, new_value)
        self.norm_calories = self.calculate_total_calories()
        self.norm_bjv = self.calculate_bjv()

    def calculate_bmr(self):
        """Method to calculate Basal Metabolic Rate (BMR)"""
        if self.user.sex == 'M':
            bmr = 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.get_age() + 5
        else:
            bmr = 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.get_age() - 161
        return bmr

    def calculate_total_calories(self):
        """Method to calculate total daily caloric needs based on activity and goal"""
        bmr = self.calculate_bmr()
        total_calories = bmr * self.activity_factor

        if self.goal == 'L':
            total_calories -= 500
        elif self.goal == 'G':
            total_calories += 500

        return total_calories

    def calculate_bjv(self):
        """Method to calculate daily nutrient targets"""
        total_calories = self.calculate_total_calories()

        protein_ratio = 0.30
        fat_ratio = 0.30
        carb_ratio = 0.40

        protein = total_calories * protein_ratio / 4
        fat = total_calories * fat_ratio / 9
        carb = total_calories * carb_ratio / 4

        return {
            "protein": round(protein, 1),
            "fat": round(fat, 1),
            "carb": round(carb, 1)
        }

    def update_norm_if_needed(self, db_name):
        """Method to update stored norm values in DB if they have changed"""
        current_date = date.today().isoformat()
        norm_calories = int(self.calculate_total_calories())
        bjv = self.calculate_bjv()

        norm_protein = bjv['protein']
        norm_fat = bjv['fat']
        norm_carb = bjv['carb']

        result = DBControl.receive_data(
            file_name=db_name,
            table_name="CONSUMED",
            columns_name="NORM_PROTEINS, NORM_FATS, NORM_CARBOHYDRATES, NORM_KCAL",
            object_condition=f"USER = '{self.user.name}' AND DATE = '{current_date}'"
        )

        if result:
            stored_protein, stored_fat, stored_carb, stored_kcal = result[0]
            if (
                stored_protein != norm_protein or
                stored_fat != norm_fat or
                stored_carb != norm_carb or
                stored_kcal != norm_calories
            ):
                print("[INFO] Norms changed - updating record.")
                DBControl.update_data(
                    file_name=db_name,
                    table_name="CONSUMED",
                    columns_array=["NORM_PROTEINS", "NORM_FATS", "NORM_CARBOHYDRATES", "NORM_KCAL"],
                    values_array=[norm_protein, norm_fat, norm_carb, norm_calories],
                    object_condition=f"USER = '{self.user.name}' AND DATE = '{current_date}'"
                )
            else:
                print("[INFO] Norms unchanged - no update required.")
        else:
            print("[INFO] No data - creating a new record.")
            insert_query = f"""
                INSERT INTO CONSUMED 
                (USER, DATE, NORM_PROTEINS, NORM_FATS, NORM_CARBOHYDRATES, NORM_KCAL,
                 TOTAL_MASS, TOTAL_PROTEINS, TOTAL_FATS, TOTAL_CARBOHYDRATES, TOTAL_KCAL)
                VALUES 
                ('{self.user.name}', '{current_date}', {norm_protein}, {norm_fat}, {norm_carb}, {norm_calories},
                 0, 0, 0, 0, 0);
            """
            DBControl.insert_data(db_name, insert_query)

        # Output all CONSUMED rows for the user and date
        print("\nCONSUMED:")
        cons = DBControl.receive_data(
            file_name=db_name,
            table_name="CONSUMED",
            columns_name="*",
            object_condition=f"USER = '{self.user.name}' AND DATE = '{current_date}'"
        )
        for v in cons:
            print(v)

    def store_norm_to_db(self, db_name):
        """Store norms to DB (used on initial day setup)"""
        current_date = date.today().isoformat()
        norm_calories = int(self.calculate_total_calories())
        bjv = self.calculate_bjv()
        norm_protein = bjv['protein']
        norm_fat = bjv['fat']
        norm_carb = bjv['carb']

        columns = [
            "USER", "DATE",
            "TOTAL_MASS", "TOTAL_PROTEINS", "TOTAL_FATS", "TOTAL_CARBOHYDRATES", "TOTAL_KCAL",
            "NORM_PROTEINS", "NORM_FATS", "NORM_CARBOHYDRATES", "NORM_KCAL"
        ]

        values = [
            f"'{self.user.name}'", f"'{current_date}'",
            0, 0, 0, 0, 0,
            norm_protein, norm_fat, norm_carb, norm_calories
        ]

        insert_sql = f"""
            INSERT INTO CONSUMED ({', '.join(columns)})
            VALUES ({', '.join(map(str, values))});
        """
        DBControl.insert_data(db_name, insert_sql)

    def get_daily_totals(self, db_name, target_date=None):
        """Get total consumption values for a specific date """
        if target_date is None:
            target_date = date.today().isoformat()

        condition = f"USER = '{self.user.name}' AND DATE = '{target_date}'"
        columns_name = "SUM(TOTAL_PROTEINS), SUM(TOTAL_FATS), SUM(TOTAL_CARBOHYDRATES), SUM(TOTAL_KCAL)"
        results = DBControl.receive_data(db_name, "CONSUMED", columns_name, condition)

        if results and results[0] and any(results[0]):
            proteins = results[0][0] or 0
            fats = results[0][1] or 0
            carbs = results[0][2] or 0
            kcal = results[0][3] or 0
            return (proteins, fats, carbs, kcal)
        else:
            return (0, 0, 0, 0)

    def get_norm(self):
        """Get daily norm values"""
        norm_protein = self.norm_bjv['protein']
        norm_fat = self.norm_bjv['fat']
        norm_carbs = self.norm_bjv['carb']
        norm_calories = self.norm_calories
        return norm_protein, norm_fat, norm_carbs, norm_calories

    def get_consumed_nutrition(self, target_date=date.today()):
        """Get consumed values for today (or specified date)"""
        consumed_protein, consumed_fat, consumed_carbs, consumed_calories = self.get_daily_totals(db_name=self.db_name, target_date=target_date)
        return consumed_protein, consumed_fat, consumed_carbs, consumed_calories

    def get_nutrition_percentage(self):
        """Return nutrient intake as a percentage of the daily norm"""
        try:
            consumed = self.get_consumed_nutrition()
            consumed_protein, consumed_fat, consumed_carbs, consumed_calories = consumed

            calories_percent = (consumed_calories / self.norm_calories) * 100 if self.norm_calories > 0 else 0
            protein_percent = (consumed_protein / self.norm_bjv['protein']) * 100 if self.norm_bjv['protein'] > 0 else 0
            fat_percent = (consumed_fat / self.norm_bjv['fat']) * 100 if self.norm_bjv['fat'] > 0 else 0
            carbs_percent = (consumed_carbs / self.norm_bjv['carb']) * 100 if self.norm_bjv['carb'] > 0 else 0

            return {
                'calories_percent': round(calories_percent, 1),
                'protein_percent': round(protein_percent, 1),
                'fat_percent': round(fat_percent, 1),
                'carb_percent': round(carbs_percent, 1)
            }
        except Exception as e:
            print(f"[ERROR] Failed to calculate percentages: {e}")
            return {
                'calories_percent': 0,
                'protein_percent': 0,
                'fat_percent': 0,
                'carb_percent': 0
            }

    def get_nutrition_advice(self):
        """Generate advice based on nutrient intake percentages"""
        percent = self.get_nutrition_percentage()
        advice_pool = []

        diffs = {
            "calories": abs(percent['calories_percent'] - 100),
            "protein": abs(percent['protein_percent'] - 100),
            "fat": abs(percent['fat_percent'] - 100),
            "carb": abs(percent['carb_percent'] - 100),
        }

        sorted_keys = sorted(diffs, key=diffs.get, reverse=True)

        for key in sorted_keys:
            if key == "calories":
                if percent['calories_percent'] < 90:
                    advice_pool.append("Low calorie intake. Add nutrient-dense foods like nuts or whole grains.")
                elif percent['calories_percent'] > 110:
                    advice_pool.append("You've exceeded your calorie goal. Watch portion sizes and avoid snacking.")
            elif key == "protein":
                if percent['protein_percent'] < 90:
                    advice_pool.append("Low protein. Include more chicken, tofu, fish, or legumes.")
                elif percent['protein_percent'] > 110:
                    advice_pool.append("High protein intake. Consider balancing with carbs and fats.")
            elif key == "fat":
                if percent['fat_percent'] < 90:
                    advice_pool.append("Low fat. Add healthy fats like olive oil, nuts, or seeds.")
                elif percent['fat_percent'] > 110:
                    advice_pool.append("Too much fat. Reduce fried foods and excessive oil.")
            elif key == "carb":
                if percent['carb_percent'] < 90:
                    advice_pool.append("Low carbs. Add complex carbs like oats or fruit.")
                elif percent['carb_percent'] > 110:
                    advice_pool.append("High carb intake. Limit sweets and refined grains.")

        if not advice_pool:
            advice_pool = [
                "Excellent balance today. Keep up the good work!",
                "Staying consistent supports your long-term health goals."
            ]

        return advice_pool[:4]

    def get_summary_table_data(self, period="week"):
        """Create summary table data for the selected time period"""
        today = date.today()

        if period == "week":
            start_date = today - timedelta(days=6)
        elif period == "month":
            start_date = today.replace(day=1)
        elif period == "halfyear":
            month = today.month - 6
            year = today.year
            if month <= 0:
                month += 12
                year -= 1
            start_date = date(year, month, 1)
        else:
            raise ValueError("Period must be 'week', 'month' or 'halfyear'")

        table_rows = []
        _, _, _, norm_calories = self.get_norm()
        days_range = (today - start_date).days + 1

        for i in reversed(range(days_range)):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.isoformat()
            _, _, _, consumed_calories = self.get_consumed_nutrition(current_date)

            if consumed_calories == 0:
                diff_str = "No data"
            else:
                difference = consumed_calories - norm_calories
                diff_str = f"{'+' if difference >= 0 else ''}{difference}"

            table_rows.append((date_str, consumed_calories, norm_calories, diff_str))

        return table_rows

    def save_table_to_file(self, table=None):
        """Save summary table data to a file"""
        table_data = []
        for row_id in table.get_children():
            row_values = table.item(row_id)["values"]
            table_data.append(row_values)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not file_path:
            return

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Calories Consumed", "Calorie Norm", "Final Result"])
            writer.writerows(table_data)

        print(f"[INFO] Data successfully saved to file: {file_path}")