import logging

from constants import DEBUG_LOG_FILE, INFO_LOG_FILE

formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s')

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

debug_file_handler = logging.FileHandler(DEBUG_LOG_FILE, 'w+')
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.setFormatter(formatter)

info_file_handler = logging.FileHandler(INFO_LOG_FILE, 'w+')
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(debug_file_handler)
logger.addHandler(console_handler)
logger.addHandler(info_file_handler)


