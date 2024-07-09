#!/bin/bash
# interpreter path. change this to your own python interpreter path
PYTHON_INTERPRETER="C:/Users/MONSTER/AppData/Local/Programs/Python/Python39/python.exe"

# hyper parameters
QUERY_TIME_OFFSET="1d"
RAW_DATA="raw_data.csv"
PROCESSED_DATA="prepared_data.csv"

"$PYTHON_INTERPRETER" extract_raw_data.py "$QUERY_TIME_OFFSET" "$RAW_DATA"
"$PYTHON_INTERPRETER" preprocess_raw_data.py "$RAW_DATA" "$PROCESSED_DATA"
