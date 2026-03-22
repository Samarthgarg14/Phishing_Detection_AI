import logging
import sys

# Disabled persistent file logging to stop generating unnecessary logs/ directories.
logging.basicConfig(
    stream=sys.stdout,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
