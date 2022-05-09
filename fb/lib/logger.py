import logging
from logging.handlers import SysLogHandler
import os
import sys


class FlaskBoneLogger:
    def __init__(self):
        if sys.platform == "win32":
            return
        pc = os.environ["COMPUTERNAME"]
        formatter = logging.Formatter(
            fmt=f"%(asctime)s {pc} CEF:0|Akhfaern|FlaskBone|1.0|%(name)s| [FlaskBone] %(message)s|%(levelname)s|",
            datefmt='%b %d %H:%M:%S')
        logger = logging.getLogger("FlaskBone")
        for h in logger.handlers:
            logger.removeHandler(h)
        handler = SysLogHandler(facility=SysLogHandler.LOG_LOCAL0, address='/dev/log')
        handler.setFormatter(formatter)
        logger.setLevel(logging.CRITICAL)
        logger.addHandler(handler)

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
