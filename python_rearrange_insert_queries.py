import sqlparse
import os

# Define the desired order of tables
table_order = [
    "hite_users",
    "hite_sessions",
    "hite_ajax_chat_bans",
    "hite_ajax_chat_invitations",
    "hite_ajax_chat_messages",
    "hite_ajax_chat_online",
    "hite_courses",
    "hite_course_config",
    "hite_course_groups",
    "hite_synaptic_pathways",
    "hite_course_objectives",
    "hite_course_topics",
    "hite_course_pages",
    "hite_course_aus",
    "hite_course_layout",
    "hite_course_competencies",
    "hite_course_calendar_events",
    "hite_course_attachments",
    "hite_course_files",
    "hite_course_messages",
    "hite_course_coursegroup",
    "hite_course_resources",
    "hite_course_scorm_data",
    "hite_course_survey",
    "hite_course_assignments",
    "hite_course_assignment_grades",
    "hite_course_discussion_forums",
    "hite_course_discussion_posts",
    "hite_course_gradebook_categories",
    "hite_course_gradebook_cat_topic",
    "hite_course_gradebook_cat_topic_grades",
    "hite_course_quizzes",
    "hite_course_quiz_questions",
    "hite_course_quiz_question_sets",
    "hite_course_quiz_question_choices",
    "hite_course_quiz_sessions",
    "hite_course_quiz_results",
    "hite_course_question_results",
    "hite_course_quiz_user_passwords",
    "hite_course_attendance",
    "hite_course_attendance_gradescale",
    "hite_course_attendance_verification",
    "hite_course_usertrack_page",
    "hite_course_usertrack_media",
    "hite_user_coursegroup",
    "hite_user_action_keys",
    "hite_user_forgot_passwords",
    "hite_oauth_clients",
    "hite_oauth_tokens",
    "hite_ipn_transaction",
    "hite_ipn_cart_items",
    "hite_ipn_history",
    "store_reviews",
    "store_review_ratings",
    "hite_user_course",
    "hite_course_beacons",
]


def reorder_insert_statements(input_file, output_file, table_order):
    with open(input_file, "r") as f:
        sql_content = f.read()

    # Parse the input SQL content
    parsed = sqlparse.parse(sql_content)

    # Extract INSERT statements and sort them based on the table order
    insert_statements = []
    for statement in parsed:
        if statement.get_type() == "INSERT":
            insert_statements.append(str(statement))
    print("insert_statements finished")

    # Sort the INSERT statements, handling missing tables gracefully
    def get_table_name(statement):
        return statement.split()[2]

    sorted_statements = sorted(insert_statements, key=lambda x: table_order.index(get_table_name(x)) if get_table_name(x) in table_order else len(table_order))

    print("sorted_statements finished")

    # Write the sorted INSERT statements to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(sorted_statements))


source_dir = "insert_success"
destination_dir = "rearrange_insert_success"
if not os.path.exists(destination_dir):
    os.mkdirs(destination_dir)
count = 1
if __name__ == "__main__":
    all_files = os.listdir(source_dir)
    for file in all_files:
        print(f"\nStarting extracting from {file} ; count: {count}")
        input_file = os.path.join(source_dir,file)
        output_file = os.path.join(destination_dir,file)
        reorder_insert_statements(input_file, output_file, table_order)
        count+=1
