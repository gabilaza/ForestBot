import math
import time
import logging
import datetime
import functools
import logging.handlers


class Logger:
    # Custom Formatters
    class ColourFormatter(logging.Formatter):
        LEVEL_COLOURS = [
            (logging.DEBUG, '\x1b[40;1m'),
            (logging.INFO, '\x1b[34;1m'),
            (logging.WARNING, '\x1b[33;1m'),
            (logging.ERROR, '\x1b[31m'),
            (logging.CRITICAL, '\x1b[41m'),
        ]

        FORMATS = {
            level: logging.Formatter(
                f'\x1b[40;1m%(asctime)s\x1b[0m | \x1b[35m%(processName)s %(threadName)s\x1b[0m {colour}%(levelname)-8s\x1b[0m | %(message)s',
                '%Y-%m-%d %H:%M:%S',
            )
            for level, colour in LEVEL_COLOURS
        }

        def format(self, record):
            formatter = self.FORMATS.get(record.levelno)
            if formatter is None:
                formatter = self.FORMATS[logging.DEBUG]

            # Override the traceback to always print in red
            if record.exc_info:
                text = formatter.formatException(record.exc_info)
                record.exc_text = f'\x1b[31m{text}\x1b[0m'

            output = formatter.format(record)

            # Remove the cache layer
            record.exc_text = None
            return output

    class DefaultFormatter(logging.Formatter):
        def __init__(self):
            super().__init__(fmt='%(asctime)s | %(processName)s %(threadName)s %(levelname)-8s | %(message)s')

    # Custom Handlers
    class ConsoleHandler(logging.StreamHandler):
        def __init__(self, initialFormatter: logging.Formatter):
            super().__init__()
            self.setLevel(logging.DEBUG)
            self.setFormatter(initialFormatter)

    class FileLogHandler(logging.handlers.TimedRotatingFileHandler):
        def __init__(self, filePath: str, initialFormatter: logging.Formatter):
            super().__init__(f'{filePath}.log', when='d')
            self.setLevel(logging.INFO)
            self.setFormatter(initialFormatter)

    class FileErrorHandler(logging.FileHandler):
        def __init__(self, filePath: str, initialFormatter: logging.Formatter):
            super().__init__(f'{filePath}.err')
            self.setLevel(logging.WARNING)
            self.setFormatter(initialFormatter)

    # init the logger
    __loggerInstance = logging.getLogger('logs')
    __loggerInstance.setLevel(logging.DEBUG)

    __logger = __loggerInstance

    # formatter
    __formatter = DefaultFormatter()
    __coloredFormatter = ColourFormatter()

    # console Handler
    __consoleHandler = ConsoleHandler(__coloredFormatter)
    __loggerInstance.addHandler(__consoleHandler)

    # file handlers
    __fullLogFileHandler = __errorsLogFileHandler = None

    @staticmethod
    def logOnTheDisk(filePathPattern: str) -> None:
        logger = Logger.__loggerInstance

        # treat fullLogFileHandler
        if Logger.__fullLogFileHandler is not None:
            fileHandler = Logger.__fullLogFileHandler
            logger.removeHandler(fileHandler)
            fileHandler.close()
        fileHandler = Logger.FileLogHandler(filePathPattern, Logger.__formatter)
        logger.addHandler(fileHandler)
        Logger.__fullLogFileHandler = fileHandler

        # treat errorsLogFileHandler
        if Logger.__errorsLogFileHandler is not None:
            fileHandler = Logger.__errorsLogFileHandler
            logger.removeHandler(fileHandler)
            fileHandler.close()
        fileHandler = Logger.FileErrorHandler(filePathPattern, Logger.__formatter)
        logger.addHandler(fileHandler)
        Logger.__errorsLogFileHandler = fileHandler

    # Wrappers for using the actual value of the Logger.__logger
    @staticmethod
    def debug(msg, *args, **kwargs):
        Logger.__logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        Logger.__logger.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        Logger.__logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        Logger.__logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        Logger.__logger.exception(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        Logger.__logger.critical(msg, *args, **kwargs)


debug = Logger.debug
info = Logger.info
warning = Logger.warning
error = Logger.error
exception = Logger.exception
critical = Logger.critical
logOnTheDisk = Logger.logOnTheDisk

