import os

def replace_backticks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("`", "")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_sql_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print("👉 Reading file :",file)
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                replace_backticks(file_path)
                print(f"Processed: {file_path}")

if __name__ == "__main__":
    folder_path = "savedsuccess"
    process_sql_files(folder_path)
