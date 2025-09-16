import logging
import inspect
import datetime
import pytz
import os

class TehranTimeFormatter(logging.Formatter):
    tehran_tz = pytz.timezone('Asia/Tehran')

    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created, self.tehran_tz)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            t = dt.strftime("%Y-%m-%d %H:%M:%S")
            s = f"{t},{int(record.msecs):03d}"
        return s

handler = logging.FileHandler("log.log", encoding="utf-8")
formatter = TehranTimeFormatter('%(asctime)s - (%(levelname)s) - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

def log_message(message="test log"):
    frame = inspect.stack()[1]
    filepath = frame.filename
    last_folder = os.path.basename(os.path.dirname(filepath))
    filename = frame.filename

    caller_file = filename.split("/")[-1]
    line_number = frame.lineno

    for line in message.splitlines():
        logger.info(f"{last_folder}/{caller_file}:{line_number}:\n{line}\n-----------------------------------------------------------------------------------------------------")
