import os


LOG_FILENAME = "quote_parser.log"
LOG_BACKUP_COUNT: int = 50
LOG_LEVEL = "DEBUG"

BASE_URL = "https://quotes.toscrape.com"  # don't put the last slash

RESULT_FILE_NAME = 'result.json'

cur_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
target_path = os.sep.join(cur_path.split(os.sep)[:-2])
log_path = os.path.join(target_path, "log") + os.sep
result_file = target_path + os.sep + RESULT_FILE_NAME
