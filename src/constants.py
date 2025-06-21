import os

from config import ROOT_DIR

USER_SETTINGS_JSON = os.path.join(ROOT_DIR, "user_settings.json")

PATH_TO_DATA = os.path.join(ROOT_DIR, "data/")
PATH_TO_OPERATIONS_XLSX = os.path.join(ROOT_DIR, "data", "operations.xlsx")
PATH_TO_OPERATIONS_JSON = os.path.join(ROOT_DIR, "data", "operations.json")

PATH_TO_LOGS = os.path.join(ROOT_DIR, "logs/")
LOGS_DEFAULT = os.path.join(ROOT_DIR, "logs", "general.log")

TINY_DF_FOR_TESTS = os.path.join(ROOT_DIR, "tests", "test_data", "test_operations_2.xlsx")
DF_FOR_TESTS = os.path.join(ROOT_DIR, "tests", "test_data", "test_operations_1.xlsx")
FILTERED_DF_FOR_TESTS = os.path.join(ROOT_DIR, "tests", "test_data", "test_filtered_data.xlsx")
