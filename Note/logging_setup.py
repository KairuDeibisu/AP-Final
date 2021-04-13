
from Note import __version__ as note_version
from Note.utils.strings import StringBuilder

import logging
import os
import sys


def setup(logging_level, log_file=None, filemode="a"):

    logging.basicConfig(
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        filename=log_file,
        filemode=filemode,
        format="%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        level=logging_level,
    )

    logger = logging.getLogger(__name__)
    logger.info(StringBuilder("Starting Logging:", logging_level))
    logger.info(StringBuilder("Note Version:", note_version))

    logger.debug(StringBuilder("Python", sys.version))
    logger.debug(StringBuilder("Platform", sys.platform))


setup(logging.DEBUG, "main.log", "w")
