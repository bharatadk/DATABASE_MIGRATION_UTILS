"""
In the old project (branch: old_hite).
Update .env file with db_name.
Run the old project in docker with mysql.
http://0.0.0.0:70
Log in.
Run the script from the browser:
http://0.0.0.0:70/fix-index.php?link=1
http://0.0.0.0:70/fix-index.php?link=15
http://0.0.0.0:70/fix-index.php?link=17
If successful, “Done 21” will be displayed on screen.
This script will fix and convert the date, varbinary, blob, etc data
Export this database in sql format from phpmyadmin
(export from terminal not recommended as the field names are missing from insert query)
http://0.0.0.0:8080/

"""

import os
import time
import subprocess
from dotenv import load_dotenv, set_key
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import shutil

def move_file(file_name):
    # Source and destination directory paths
    source_directory = os.path.expanduser("~/Downloads")
    destination_directory = "../sqlfiles/need_to_remove_apostrophe"

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Construct the source and destination file paths
    source_file_path = os.path.join(source_directory, f'{file_name}.sql')
    destination_file_path = os.path.join(destination_directory, f'{file_name}.sql')

    # Move the file
    try:
        shutil.move(source_file_path, destination_file_path)
        print(f"File '{file_name}' moved successfully from '{source_directory}' to '{destination_directory}'.")
    except Exception as e:
        print(f"Error: {e}")

def run_docker_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing the command: {e}")
        return None


def update_env_variable(key, value):
    load_dotenv()  # Load the .env file
    # Modify the environment variable in memory
    os.environ[key] = value
    # Save the modified environment variable to the .env file
    set_key("../../.env", key, value)


def open_scripts_from_broswer(db_name):
    # create chromeoptions instance
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # provide location where chrome stores profiles
    # options.add_argument(r"--user-data-dir=/home/bharat/.config/google-chrome")

    # provide the profile name with which we want to open browser
    # options.add_argument(r'--profile-directory=Profile 3')

    # specify where your chrome driver present in your pc
    # driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.get("http://0.0.0.0:70")
    time.sleep(5)

    driver.find_element(By.ID, "username").send_keys("test")
    driver.find_element(By.ID, "password").send_keys("test2015xlb")
    driver.find_element(By.XPATH, "//div/div[1]/div/button").submit()
    time.sleep(5)

    driver.get("http://0.0.0.0:70/fix-index.php?link=1")
    time.sleep(5)

    driver.get("http://0.0.0.0:70/fix-index.php?link=15")
    time.sleep(5)

    driver.get("http://0.0.0.0:70/fix-index.php?link=17")
    time.sleep(5)

    driver.get("http://0.0.0.0:8080/")
    time.sleep(1)

    driver.find_element(By.ID, "serverNameInput").send_keys("mysql-56")
    driver.find_element(By.ID, "input_username").send_keys("root")
    driver.find_element(By.ID, "input_password").send_keys("secret")
    driver.find_element(By.ID, "input_go").submit()
    time.sleep(1)

    driver.get(
        f"http://0.0.0.0:8080/index.php?route=/database/export&db={db_name}")
    time.sleep(1)

    driver.find_element(By.ID, "buttonGo").submit()
    time.sleep(10) # This is required

    driver.close()

database_list = []
FILES_DIR = os.path.join(os.path.dirname(os.getcwd()), 'sqlfiles')
input_folder = os.path.join(FILES_DIR,"mysql2")
sql_files = [file for file in os.listdir(
    input_folder) if file.endswith(".sql")]

for file in sql_files:
    sql_file_name = file.rsplit(".", 1)[0]
    database_list.append(sql_file_name)

print("DAtabase list",database_list)

if __name__ == "__main__":
    for db_name in database_list:
        print("👉 Starting conversion of db:", db_name)
        print("♻ Environment variable updated")

        update_env_variable("DB_NAME", db_name)
        time.sleep(1)

        run_docker_command(
            "docker-compose -f /Users/danphe/Desktop/server-migration/HITE2021-old/docker-compose.yml down")

        run_docker_command(
            "docker-compose -f /Users/danphe/Desktop/server-migration/HITE2021-old/docker-compose.yml up -d")

        print("🐋 Docker container restarted")

        open_scripts_from_broswer(db_name)
        print("✅ Conversion and Download success\n\n\n")
        print("Moving file ... ")
        move_file(db_name)
        print ("File moved")
