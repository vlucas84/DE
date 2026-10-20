# Configuration dictionary obtained from the initialization service
db_config = {
    "connection": {
        "host": "production-db.internal",
        "port": 5432,
        "user": "postgres"
        }
    }

# Safely extract the 'connection' dict (handles missing key or None value)
connection = db_config.get("connection") or {}

# Extract the 'host' value ​​from the nested 'connection' dictionary
# and output 
db_host = connection.get("host")
print(f"Verifying the extracted host value: {db_host}\n")

# Extract the 'port' value ​​from the nested 'connection' dictionary
# and output 
db_port = connection.get("port")
print(f"Verifying the extracted port value: {db_port}\n")

# Safely check for the 'ssl_settings' key. 
# If this key or its 'ssl_mode' parameter is missing, 
# the variable defaults to 'verify-full'.
ssl_settings = connection.get("ssl_settings")
if isinstance(ssl_settings, dict):
    db_ssl_mode = ssl_settings.get("ssl_mode", "verify-full")
else:
    db_ssl_mode = "verify-full"

# Ensure the nested 'connection' dict exists and is not None before modification
if not isinstance(db_config.get("connection"), dict):
    db_config["connection"] = {}
conn_dict = db_config["connection"]

# Change the 'user' value in the nested dict to 'admin'
conn_dict["user"] = "admin"

# Add a new parameter 'max_connections'=100 to the nested dict
conn_dict["max_connections"] = 100

# Output the updated content of the 'connection' configuration 
# by iterating over key-value pairs
print(f"SSL Mode: {db_ssl_mode}")
print("Connection parameters:")
for key, value in (db_config.get("connection") or {}).items():
    print(f"* {key} : {value}")
