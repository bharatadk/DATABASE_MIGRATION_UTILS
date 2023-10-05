"""
Export original mysql file from server.
Edit the sql file:
Replace /var/www/websites with /mnt/gigenet_volume/websites
Replace http://rmedia.4dlspace.com static files with https://rmedia.sfo3.digitaloceanspaces.com/public_html
Replace https://rmedia.intelladapt.com static files with https://rmedia.sfo3.digitaloceanspaces.com/public_html

"""

import os
import cchardet


def replace_unwanted_characters(input_file_path, output_file_path):
    with open(input_file_path, "rb") as input_file:
        # Use cchardet to detect the encoding of the file
        detector = cchardet.UniversalDetector()
        for line in input_file:
            detector.feed(line)
            if detector.done:
                break
        input_file.seek(0)  # Reset file pointer to the beginning
        encoding = detector.result["encoding"]

        # Use 'utf-8' as a fallback encoding if detection fails
        if not encoding:
            encoding = "utf-8"

        # Read the content of the file as binary data
        file_content = input_file.read()

    # Decode the binary data using the detected or fallback encoding
    file_content = file_content.decode(encoding, errors="replace")

    replacements = [
        ("/var/www/websites", "/mnt/gigenet_volume/websites"),
        (
            "http://rmedia.4dlspace.com",
            "https://rmedia.sfo3.digitaloceanspaces.com/public_html",
        ),
        (
            "https://rmedia.intelladapt.com",
            "https://rmedia.sfo3.digitaloceanspaces.com/public_html",
        ),
    ]

    for original, replacement in replacements:
        file_content = file_content.replace(original, replacement)

    with open(output_file_path, "w", encoding=encoding) as output_file:
        output_file.write(file_content)


def create_output_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


current_directory = os.path.join(os.getcwd())
input_directory = '/Users/bansaj/Downloads/apostrophesavedsuccess/mysql1'
ouput_directory = '/Users/bansaj/Downloads/apostrophesavedsuccess/mysql2'
file_list = [file for file in os.listdir(
    input_directory) if file.endswith(".sql")]
count = 0

for file_name in file_list:
    count += 1
    print(f"♻ Processing file {file_name}")
    input_file_path = os.path.join(input_directory, file_name)
    output_file_path = os.path.join(ouput_directory, file_name)
    replace_unwanted_characters(input_file_path, output_file_path)
    print(f"✅ Processing file {file_name} : {count}")
