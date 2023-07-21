import sqlparse


def extract_insert_statements(input_file, output_file):
    with open(input_file, "r") as f:
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
                print(num_inserts, end="")

    return num_inserts


if __name__ == "__main__":
    input_sql_file = (
        "sls_client_tmpl_academic.sql"  # Replace with the path to your SQL file
    )
    output_sql_file = "test.sql"  # Replace with the desired path for the new SQL file

    num_inserts_found = extract_insert_statements(input_sql_file, output_sql_file)
    print(f"Number of INSERT statements found: {num_inserts_found}")
