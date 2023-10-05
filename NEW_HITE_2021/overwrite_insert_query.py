import os
import re

# Path to the folder containing SQL files
input_folder = "/Users/bansaj/Downloads/apostrophesavedsuccess/rearrange_insert_success"
# Path to the folder to save modified SQL files
output_folder = "/Users/bansaj/Downloads/apostrophesavedsuccess/final_sql"

# Define a regular expression pattern to match INSERT statements
insert_pattern = r"INSERT\s+INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)\s*;"


def replace_insert(match):
    table_name = match.group(1)
    columns = match.group(2)
    values = match.group(3)
    overridden_query = f"INSERT INTO {table_name} ({columns}) OVERRIDING SYSTEM VALUE VALUES ({values});"
    return overridden_query


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".sql"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)

        with open(input_file_path, "r") as input_file:
            sql_queries = input_file.read()

        modified_sql_queries = re.sub(
            insert_pattern, replace_insert, sql_queries, flags=re.DOTALL)

        with open(output_file_path, "w") as output_file:
            output_file.write(modified_sql_queries)

        print("Modified SQL queries saved to", output_file_path)
