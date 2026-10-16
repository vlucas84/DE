# Configuration dictionary obtained from the initialization service
db_config = {
"connection": {
"host": "production-db.internal",
"port": 5432,
"user": "postgres"
}
}

# Extract the 'host' value ​​from the nested 'connection' dictionary
# and output 
db_host = db_config.get("connection").get("host")
print(f"Verifying the extracted host value: {db_host}\n")

# Extract the 'port' value ​​from the nested 'connection' dictionary
# and output 
db_port = db_config.get("connection").get("port")
print(f"Verifying the extracted port value: {db_port}\n")

# Safely check for the 'ssl_settings' key. 
# If this key or its 'ssl_mode' parameter is missing, 
# the variable defaults to 'verify-full'.
# Also output result
db_ssl_settings = db_config.get("connection", {}).get("ssl_settings", "verify-full")

# Change the 'user' value in the nested dict to 'admin'
db_config["connection"]["user"] = "admin"

# Add a new parameter 'max_connections'=100 to the nested dict
db_config["connection"]["max_connections"] = 100

# Output the updated content of the 'connection' configuration 
# by iterating over key-value pairs
print(f"SSL Mode: {db_ssl_settings}")
print("Connection parameters:")
for key, value in db_config["connection"].items():
    print(f"* {key} : {value}")
