import os
import sqlparse


def extract_insert_statements(input_file, output_file):
    with open(input_file, encoding="utf8", errors="ignore") as f:
        sql_content = f.read()
    print("reading sql_content finished")

    # Parse the input SQL content
    parsed = sqlparse.parse(sql_content)
    print("parsing sql_content finished")

    # Find INSERT statements and write them to the output file
    with open(output_file, "w") as f:
        num_inserts = 0
        for statement in parsed:
            if statement.get_type() == "INSERT":
                f.write(str(statement))
                num_inserts += 1


source_dir = "apostrophesavedsuccess"
destination_dir = "insert_success"
count = 1

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

if __name__ == "__main__":
    all_files = [file for file in os.listdir(source_dir) if file.endswith(".sql")]
    for file in all_files:
        print(f"\nStarting extracting from {file} ; count: {count}")
        input_file = os.path.join(source_dir, file)
        output_file = os.path.join(destination_dir, file)
        extract_insert_statements(input_file, output_file)
        count += 1
