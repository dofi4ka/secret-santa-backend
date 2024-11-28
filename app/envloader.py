from os import getenv
import dotenv

dotenv.load_dotenv()

REQUIRED_ENV_VARS = "DATABASE_URL", "SECRET_KEY", "BOT_TOKEN"

for var in REQUIRED_ENV_VARS:
    if getenv(var) is None:
        raise EnvironmentError(f"Required environment variable {var} is not set.")
