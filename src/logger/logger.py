import logging
import sys

# Configure basic logging structure
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create and export a configurable logger instance
logger = logging.getLogger("document_rag_app")
