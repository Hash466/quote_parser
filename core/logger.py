import logging
import os
import queue
from logging.handlers import (QueueHandler, QueueListener,
                              TimedRotatingFileHandler)
from core.config import (LOG_FILENAME, LOG_LEVEL, LOG_BACKUP_COUNT, log_path)


if not os.path.exists(log_path):
    os.mkdir(log_path)

_log_queue = queue.Queue()

_queue_handler = QueueHandler(_log_queue)

_rot_handler = TimedRotatingFileHandler(
    log_path + LOG_FILENAME,
    when="h",
    interval=1,
    backupCount=LOG_BACKUP_COUNT,
    encoding="utf-8"
)

log_queue_listener = QueueListener(_log_queue, _rot_handler).start()


def get_logger(name: str = None) -> logging:
    logging.basicConfig(
        handlers=[
            _queue_handler,
        ],
        format=(
            "%(asctime)s -=[%(levelname)s]=-\t%(message)s\t\t~~> %(filename)s "
            "-> %(funcName)s -> line: %(lineno)s"
        )
    )

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    return logger
