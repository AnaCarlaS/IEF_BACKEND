import logging.config
import math
import structlog

from datetime import datetime
from pathlib import Path

DEFAULT_LEVEL = 'INFO'

BASE_DIR = Path(__file__).resolve().parent.parent
folder = Path(BASE_DIR) / 'logs'
folder.mkdir(parents=True, exist_ok=True)
file_name = str(math.trunc(datetime.now().timestamp()))[0:9]
file = folder / f'{file_name}.log'

timestamper = structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S', utc=False)
pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.ExtraAdder(),
    timestamper,
]

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'plain': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processors': [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            'foreign_pre_chain': pre_chain,
        },
        'colored': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processors': [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            'foreign_pre_chain': pre_chain,
        },
    },
    'handlers': {
        'default': {
            'level': DEFAULT_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': DEFAULT_LEVEL,
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': file,
            'formatter': 'plain',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': DEFAULT_LEVEL,
            'propagate': True,
        },
    }
})
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# logger = structlog.stdlib.get_logger()
"""Instância de logger para todo o script"""
