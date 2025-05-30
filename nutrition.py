from datetime import date
from DB_control import DBControl

# products_table_sql = """CREATE TABLE IF NOT EXISTS PRODUCTS (
#                         PRODUCT TEXT PRIMARY KEY,
#                         PROTEINS REAL NOT NULL,
#                         FATS REAL NOT NULL,
#                         CARBOHYDRATES REAL NOT NULL,
#                         KCAL INTEGER NOT NULL
#                         );"""

# product_pictures_table_sql = """CREATE TABLE IF NOT EXISTS PICTURES (
#                                     PRODUCT TEXT PRIMARY KEY,
#                                     IMAGE BLOB NOT NULL
#                                     );"""
    
# nutrition_table_sql = """CREATE TABLE IF NOT EXISTS NUTRITION (
#                         USER TEXT NOT NULL,
#                         DATE DATE NOT NULL,
#                         PRODUCT TEXT NOT NULL,
#                         CONSUMED_MASS REAL NOT NULL,
#                         CONSUMED_PROTEINS REAL NOT NULL,
#                         CONSUMED_FATS REAL NOT NULL,
#                         CONSUMED_CARBOHYDRATES REAL NOT NULL,
#                         CONSUMED_KCAL INTEGER NOT NULL
#                         );"""

class Nutrition:
    def __init__(self, user, db_name = "Health_database.db"):
        self.user_email = user.email
        self.db_name = db_name
        self.db = DBControl()
        self.products_table_name = "PRODUCTS"
        self.nutrition_table_name = "NUTRITION"
        self.consumed_table_name = "CONSUMED"
        self.nutrition_columns = ["USER", "DATE", "PRODUCT", "CONSUMED_MASS", "CONSUMED_PROTEINS", "CONSUMED_FATS", "CONSUMED_CARBOHYDRATES", "CONSUMED_KCAL"]
        self.consumed_columns = ["USER", "DATE", "TOTAL_MASS", "TOTAL_PROTEINS", "TOTAL_FATS", "TOTAL_CARBOHYDRATES", "TOTAL_KCAL", "NORM_PROTEINS", "NORM_FATS", "NORM_CARBOHYDRATES", "NORM_KCAL"]

        nutrition_table_sql = """CREATE TABLE IF NOT EXISTS NUTRITION (
                                 USER TEXT PRIMARY KEY,
                                 DATE DATE NOT NULL,
                                 PRODUCT TEXT NOT NULL,
                                 CONSUMED_MASS REAL NOT NULL,
                                 CONSUMED_PROTEINS REAL NOT NULL,
                                 CONSUMED_FATS REAL NOT NULL,
                                 CONSUMED_CARBOHYDRATES REAL NOT NULL,
                                 CONSUMED_KCAL INTEGER NOT NULL
                                 );"""

        consumed_table_sql = """CREATE TABLE IF NOT EXISTS CONSUMED (
                                 USER TEXT NOT NULL,
                                 DATE DATE NOT NULL,
                                 TOTAL_MASS REAL NOT NULL,
                                 TOTAL_PROTEINS REAL NOT NULL,
                                 TOTAL_FATS REAL NOT NULL,
                                 TOTAL_CARBOHYDRATES REAL NOT NULL,
                                 TOTAL_KCAL INTEGER NOT NULL,
                                 NORM_PROTEINS REAL NOT NULL,
                                 NORM_FATS REAL NOT NULL,
                                 NORM_CARBOHYDRATES REAL NOT NULL,
                                 NORM_KCAL INTEGER NOT NULL
                                 );"""

        # making sure that table is existed in database
        self.db.create_table(self.db_name, nutrition_table_sql)
        self.db.create_table(self.db_name, consumed_table_sql)

        # self.db.delete_data(self.db_name, self.nutrition_table_name)                    #----------------------------
        # self.db.delete_data(self.db_name, self.consumed_table_name)                     #----------------------------
    
    def add_consumed_product(self, product_name, product_mass):
        data = self.db.receive_data(self.db_name, self.products_table_name, "*", f"PRODUCT = '{product_name}'")
        for record in data:
              product, proteins, fats, carbohydrates, kcal = record
       
        values = [f"'{self.user_email}'", f"'{date.today()}'", f"'{product}'", round(float(product_mass), 2), round((proteins / 100) * float(product_mass), 2), round((fats / 100) * float(product_mass), 2), round((carbohydrates / 100) * float(product_mass), 2), round((kcal / 100) * float(product_mass), 2)]
    
        sql = f"INSERT INTO {self.nutrition_table_name} ({", ".join(self.nutrition_columns)}) VALUES({", ".join(str(v) for v in values)});"
        self.db.insert_data(self.db_name, sql)
    
        self.update_consumed_table(values.copy())

        print("\nNUTRITION:")                                                           #----------------------------
        nutr = self.db.receive_data(self.db_name, self.nutrition_table_name, "*")       #----------------------------
        for v in nutr:                                                                  #----------------------------
            print(v)                                                                    #----------------------------

        print("\nCONSUMED:")                                                            #----------------------------
        cons = self.db.receive_data(self.db_name, self.consumed_table_name, "*")        #----------------------------
        for v in cons:                                                                  #----------------------------
            print(v)                                                                    #----------------------------

        values[2] = product
        return values
            
    def update_consumed_table(self, nutrition_values):
        nutrition_last_date = self.db.receive_data(self.db_name, self.nutrition_table_name, "DATE", f"USER = '{self.user_email}' AND (DATE = (SELECT MAX(DATE) FROM {self.nutrition_table_name}))")
        is_current_date = self.db.data_exists(self.db_name, self.consumed_table_name, "*", f"USER = '{self.user_email}' AND DATE = '{nutrition_last_date[0][0]}'")

        if is_current_date:
            old_data = self.db.receive_data(self.db_name, self.consumed_table_name, "*", f"USER = '{self.user_email}' AND DATE = '{date.today()}'")
        
            for record in old_data:
                old_user, old_date, old_mass, old_proteins, old_fats, old_carbohydrates, old_kcal, old_norm_p, old_norm_f, old_norm_c, old_norm_k = record

            nutrition_values[3] += old_mass
            nutrition_values[4] += old_proteins
            nutrition_values[5] += old_fats
            nutrition_values[6] += old_carbohydrates
            nutrition_values[7] += old_kcal
        
            self.db.update_data(self.db_name, self.consumed_table_name, self.consumed_columns[2:7], nutrition_values[3:8], f"USER = '{self.user_email}' AND DATE = '{nutrition_last_date[0][0]}'")
        else:
            insert_sql = f"INSERT INTO {self.consumed_table_name} ({", ".join(self.consumed_columns)}) VALUES ({", ".join(str(v) for v in (nutrition_values[:2] + nutrition_values[3:]))}, -1, -1, -1, -1);"
            self.db.insert_data(self.db_name, insert_sql)
        
    def show_today_consumption(self):
        nutrition = self.db.receive_data(self.db_name, self.nutrition_table_name, "*")
        consumed = self.db.receive_data(self.db_name, self.consumed_table_name, "*")    #----------------------------

        print("Nutrition table:")                                                       #----------------------------
        for my_list in nutrition:                                                       #----------------------------
            print(my_list)                                                              #----------------------------

        print("\nConsumed table:")                                                      #----------------------------
        for my_list in consumed:                                                        #----------------------------
            print(my_list)                                                              #----------------------------

        today_nutrition = self.db.receive_data(self.db_name, self.nutrition_table_name, "*", f"USER = '{self.user_email}' AND DATE = '{date.today()}'")
        return today_nutrition

    def get_all_products_list(self):
        product_list = self.db.receive_data(self.db_name, self.products_table_name, "PRODUCT")
        list_values = [k[0] for k in product_list]

        return list_values

    def check_product(self, product_name):
        return self.db.data_exists(self.db_name, self.products_table_name, "PRODUCT", f"PRODUCT = '{product_name}'")

    def remove_consumed_product(self, product_name, product_mass):
        product_list = self.db.receive_data(self.db_name, self.nutrition_table_name, "ROWID, *", f"USER = '{self.user_email}' AND DATE = '{date.today()}' AND PRODUCT = '{product_name}' AND CONSUMED_MASS = {product_mass}")

        if product_list:
            rowid = product_list[0][0]
            self.db.delete_specific_data(self.db_name, self.nutrition_table_name, f"ROWID = {rowid}")

            deleted_product = list(product_list[0][4:9])
            
            consumed_values = self.db.receive_data(self.db_name, self.consumed_table_name, "TOTAL_MASS, TOTAL_PROTEINS, TOTAL_FATS, TOTAL_CARBOHYDRATES, TOTAL_KCAL", f"USER = '{self.user_email}' AND DATE = '{date.today()}'")
            for consumed_records in consumed_values:
                mass, proteins, fats, carbohydrates, kcal = consumed_records

            deleted_product[0] = mass - deleted_product[0]
            deleted_product[1] = proteins - deleted_product[1]
            deleted_product[2] = fats - deleted_product[2]
            deleted_product[3] = carbohydrates - deleted_product[3]
            deleted_product[4] = kcal - deleted_product[4]

            self.db.update_data(self.db_name, self.consumed_table_name, self.consumed_columns[2:7], deleted_product, f"USER = '{self.user_email}' AND DATE = '{date.today()}'")

        nutrition = self.db.receive_data(self.db_name, self.nutrition_table_name, "*")  #----------------------------
        consumed = self.db.receive_data(self.db_name, self.consumed_table_name, "*")    #----------------------------

        print("Nutrition table:")                                                       #----------------------------
        for my_list in nutrition:                                                       #----------------------------
            print(my_list)                                                              #----------------------------

        print("\nConsumed table:")                                                      #----------------------------
        for my_list in consumed:                                                        #----------------------------
            print(my_list)                                                              #----------------------------

    def get_product_image(self, product_name):
        result = self.db.receive_data(self.db_name, "PICTURES", "IMAGE", f"PRODUCT = '{product_name}'")

        if result:
            return result[0][0]
        return None