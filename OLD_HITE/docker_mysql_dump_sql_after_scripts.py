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
    set_key(".env", key, value)


def open_scripts_from_broswer(db_name):
    # create chromeoptions instance
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    ##provide location where chrome stores profiles
    # options.add_argument(r"--user-data-dir=/home/bharat/.config/google-chrome")

    ##provide the profile name with which we want to open browser
    # options.add_argument(r'--profile-directory=Profile 3')

    # specify where your chrome driver present in your pc
    # driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.get("http://0.0.0.0:70")
    time.sleep(5)

    driver.find_element(By.ID, "username").send_keys("test")
    driver.find_element(By.ID, "password").send_keys("test2015xlb")
    driver.find_element(By.XPATH, "//div/div[1]/div/button").submit()
    time.sleep(10)

    driver.get("http://0.0.0.0:70/fix-index.php?link=1")
    time.sleep(8)

    driver.get("http://0.0.0.0:70/fix-index.php?link=15")
    time.sleep(8)

    driver.get("http://0.0.0.0:70/fix-index.php?link=17")
    time.sleep(8)

    driver.get("http://0.0.0.0:8080/")
    time.sleep(5)

    driver.find_element(By.ID, "serverNameInput").send_keys("mysql-56")
    driver.find_element(By.ID, "input_username").send_keys("root")
    driver.find_element(By.ID, "input_password").send_keys("secret")
    driver.find_element(By.ID, "input_go").submit()
    time.sleep(5)

    driver.get(f"http://0.0.0.0:8080/index.php?route=/database/export&db={db_name}")
    time.sleep(5)

    driver.find_element(By.ID, "buttonGo").submit()
    time.sleep(10)

    driver.close()


database_list = [
    "sls_client_abl_demo",
    "sls_client_amol6",
    "sls_client_auag2",
    "sls_client_auag",
    "sls_client_auc",
    "sls_client_bigdata",
    "sls_client_blank",
    "sls_client_calculus",
    "sls_client_chaminade",
    "sls_client_course360",
    "sls_client_dd",
    "sls_client_dtoc",
    "sls_client_flvs_live",
    "sls_client_flvs",
    "sls_client_hite2",
    "sls_client_hite4",
    "sls_client_hite_s1",
    "sls_client_hite_s2",
    "sls_client_hite_s3",
    "sls_client_hite",
    "sls_client_hult",
    "sls_client_idemo",
    "sls_client_idesigner",
    "sls_client_iuea",
    "sls_client_landmark",
    "sls_client_lms_demo2",
    "sls_client_lms_demo",
    "sls_client_lms_live2",
    "sls_client_lms_live",
    "sls_client_lmssand",
    "sls_client_lms",
    "sls_client_loadtest2",
    "sls_client_loadtest",
    "sls_client_mcl_demo",
    "sls_client_mcl",
    "sls_client_mi",
    "sls_client_modules",
    "sls_client_mooc2",
    "sls_client_mooc_dev",
    "sls_client_mooc_live",
    "sls_client_mooc",
    "sls_client_nova_live",
    "sls_client_nova",
    "sls_client_recover",
    "sls_client_sgl_demo",
    "sls_client_sgl",
    "sls_client_spb",
    "sls_client_stleo",
    "sls_client_testprep",
    "sls_client_test",
    "sls_client_tmpl_academic",
]

if __name__ == "__main__":
    for db_name in database_list:
        print("👉 Starting conversion of db:", db_name)
        print("♻ Environment variable updated")

        update_env_variable("DB_NAME", db_name)
        time.sleep(2)

        run_docker_command("docker-compose restart")
        time.sleep(10)

        print("🐋 Docker container restarted")

        open_scripts_from_broswer(db_name)
        print("✅ Conversion and Download success\n\n\n")
