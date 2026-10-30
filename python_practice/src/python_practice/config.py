import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read database configuration keys
# Provide default host and port to prevent connection failures if missing in .env,
# while keeping credentials (user, password, db name) strictly environment-driven for security
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# The following data was added for verification purposes only (output result)
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"