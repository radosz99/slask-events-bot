import logging

from constants import LOG_FILE

logging.basicConfig(filename=LOG_FILE,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger("root")


