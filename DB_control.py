import sqlite3

# sample code how to use each function to manage the database
#
# initialize the variable to interact with the database management functions
#       db = DBControl()
#
#       db_name = "example.db"
#       table_name = "NUTRITION"
#
# function to create a database file, for this you need to enter its name
#       db.create_db(db_name)
#
#       sql_columns = """CREATE TABLE IF NOT EXISTS NUTRITION (
#                        PRODUCT TEXT PRIMARY KEY,
#                        PROTEINS REAL NOT NULL,
#                        FATS REAL NOT NULL,
#                        CARBOHYDRATES REAL NOT NULL,
#                        KCAL INTEGER NOT NULL
#                        );"""
#
# a function to create a table of values in a database file, for this we specify the name of
# the existing database and the SQL query with the necessary information to form the table
#       db.create_table(db_name, sql_columns)
#
# this uses a construct to read lines from a text file that contain generated SQL queries,
# the values of which are entered into the database using a function
#       with open("testfordb.txt", "r") as file:
#           for line in file:
#               db.insert_data(db_name, line.strip())
#
# an example of inserted SQL queries: INSERT INTO NUTRITION (PRODUCT, PROTEINS, FATS, CARBOHYDRATES, KCAL) VALUES('Quince', 0.6, 0, 8.7, 37);
#
# a function to delete a specific row of data in a table under a certain condition
#       db.delete_specific_data(db_name, table_name, "PRODUCT = 'Apricot'")
#
# if you just need to clear all the data in the table, use this function
#       db.delete_data(db_name, table_name)
#
# a function for printing values from the database, if necessary, you can enter a condition for filtering values
#       db.print_data(db_name, "*", table_name)
#       db.print_data(db_name, "*", table_name, "FATS < 9")
#
# function to check for the presence of the required data in the table (by condition)
#       db.data_exists(db_name, "*", table_name, "PRODUCT = 'Lamb'")
#
# function to get all the data that meets the specified condition,
# as a result, we get an array of tuples with data (data rows)
#       result = db.receive_data(db_name, "*", table_name, "KCAL > 43")
#
#       for record in result:
#           product, proteins, fats, carbohydrates, kcal = record
#           print(product)
#       result = db.receive_data(db_name, table_name, "*", "KCAL > 43")
#       product_array, proteins_array, fats_array, carbohydrates_array, kcal_array = [], [], [], [], []
#
#       for record in result:
#           product, proteins, fats, carbohydrates, kcal = record
#
#           product_array.append(product)
#           proteins_array.append(proteins)
#           fats_array.append(fats)
#           carbohydrates_array.append(carbohydrates)
#           kcal_array.append(kcal)
#
# a function to update the required values in the table (you need to specify the required columns and set a condition)
#       columns = ["PRODUCT", "PROTEINS", "FATS", "CARBOHYDRATES", "KCAL"]
#       values = ["'product'", -1, -1, -1, -1]
#       db.update_data(db_name, table_name, columns, values, "PRODUCT = 'Lamborgini'")

class DBControl:
    @staticmethod
    def create_db(file_name):
        # Create database
        conn = sqlite3.connect(file_name)
        conn.close()

    @staticmethod
    def create_table(file_name, sql_columns):
        # Create table in the database
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql_columns)
            conn.commit()
            print("Table created Successfully")
        except sqlite3.Error as e:
            print(f"Error in createTable function: {e}")
        finally:
            conn.close()

    @staticmethod
    def delete_specific_data(file_name, table_name, condition):
        # Delete specific data (row of data) from the table, according to condition
        sql = f"DELETE FROM {table_name} WHERE {condition};"

        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")
            result = cursor.fetchone()

            cursor.execute(sql)
            print("Records deleted Successfully!")

            if result:
                sql_reset = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';"
                cursor.execute(sql_reset)
                print("Auto-increment reset Successfully!")
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error in deleteData function: {e}")
        finally:
            conn.close()
            
    @staticmethod
    def delete_data(file_name, table_name):
        # Delete all data from the table
        sql = f"DELETE FROM {table_name};"
    
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
        
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")
            result = cursor.fetchone()
        
            cursor.execute(sql)
            print("Records deleted Successfully!")
        
            if result:
                sql_reset = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';"
                cursor.execute(sql_reset)
                print("Auto-increment reset Successfully!")
        
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error in deleteData function: {e}")
        finally:
            conn.close()


    @staticmethod
    def insert_data(file_name, sql_value):
        # Insert data (one row of data) into table
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql_value)
            conn.commit()
            #print("Records inserted Successfully!")
        except sqlite3.Error as e:
            print(f"Error in insertData function: {e}")
        finally:
            conn.close()

    @staticmethod
    def print_data(file_name, table_name, columns_name, object_condition=""):
        # Print all data of the table, according to condition
        sql = f"SELECT {columns_name} FROM {table_name}"
        if object_condition:
            sql += f" WHERE {object_condition}"

        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            #print("Records printed Successfully!")
        except sqlite3.Error as e:
            print(f"Error in printData function: {e}")
        finally:
            conn.close()

    @staticmethod
    def data_exists(file_name, table_name, columns_name, object_condition=""):
        # Check if the data exists in the table
        sql = f"SELECT {columns_name} FROM {table_name}"
        if object_condition:
            sql += f" WHERE {object_condition}"
        
        sql += " LIMIT 1;"
        exists = False

        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            exists = cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Failed to prepare statement: {e}")
        finally:
            conn.close()

        return exists

    @staticmethod
    def receive_data(file_name, table_name, columns_name, object_condition=""):
        # Get all data from the table, according to condition
        sql = f"SELECT {columns_name} FROM {table_name}"
        if object_condition:
            sql += f" WHERE {object_condition}"

        received_tuple = []
            
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                received_tuple.append(row)
            #print("Records printed Successfully!")
        except sqlite3.Error as e:
            print(f"Error in printData function: {e}")
        finally:
            conn.close()

        return received_tuple

    @staticmethod
    def update_data(file_name, table_name, columns_array, values_array, object_condition=""):
        # Update specific data in the table by setting names of columns and their values, according to condition
        sql = f"UPDATE {table_name} SET "

        for i, column in enumerate(columns_array):
            if i != 0:
                sql += ", "

            sql += f"{column} = {values_array[i]}"

        if object_condition:
            sql += f" WHERE {object_condition}"

        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            #print("Email updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating email: {e}")
        finally:
            conn.close()