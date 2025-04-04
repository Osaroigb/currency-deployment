import os
import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter

# Load environment variables from .env file
load_dotenv()

# Constants for environment variable names
APP_PORT_VAR = "APP_PORT"
APP_HOST_VAR = "APP_HOST"
APP_NAME_VAR = "APP_NAME"
REDIS_CLOUD_URL_VAR = "REDIS_CLOUD_URL"
OPEN_XR_APP_ID_VAR = "OPEN_XR_APP_ID"
OPEN_XR_BASE_URL_VAR = "OPEN_XR_BASE_URL"
XECD_API_ID_VAR = "XECD_API_ID"
XECD_API_KEY_VAR = "XECD_API_KEY"
XECD_BASE_URL_VAR = "XECD_BASE_URL"


# Configuration class
class Config:
    APP_PORT: int = int(os.getenv(APP_PORT_VAR))
    APP_HOST: str = os.getenv(APP_HOST_VAR)
    APP_NAME: str = os.getenv(APP_NAME_VAR)
    REDIS_CLOUD_URL: str = os.getenv(REDIS_CLOUD_URL_VAR)
    OPEN_XR_APP_ID: str = os.getenv(OPEN_XR_APP_ID_VAR)
    OPEN_XR_BASE_URL: str = os.getenv(OPEN_XR_BASE_URL_VAR)
    XECD_API_ID: str = os.getenv(XECD_API_ID_VAR)
    XECD_API_KEY: str = os.getenv(XECD_API_KEY_VAR)
    XECD_BASE_URL: str = os.getenv(XECD_BASE_URL_VAR)


    @classmethod
    def validate_env(cls):
        required_vars = [
            APP_NAME_VAR,
            APP_PORT_VAR,
            APP_HOST_VAR,
            REDIS_CLOUD_URL_VAR,
            OPEN_XR_APP_ID_VAR,
            OPEN_XR_BASE_URL_VAR,
            XECD_API_ID_VAR,
            XECD_API_KEY_VAR,
            XECD_BASE_URL_VAR
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Define color format for log messages
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
    },
)

# Set up logging with color formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])