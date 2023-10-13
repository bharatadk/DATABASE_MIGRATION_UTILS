#!/bin/bash

# Run the scripts one by one

# Script 1
echo "Running replace_characters_apostrophe_tilde.py"
python3 replace_characters_apostrophe_tilde.py

# Script 2
echo "Running extract_insert_queries.py"
python3 extract_insert_queries.py

# Script 3
echo "Running rearrange_insert_queries.py"
python3 rearrange_insert_queries.py

# Script 4
echo "Running overwrite_insert_query.py"
python3 overwrite_insert_query.py

echo "All scripts have been executed."
