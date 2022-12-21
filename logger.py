import logging

from constants import LOG_FILE

formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s')

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, 'w+')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


