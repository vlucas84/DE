# List of roles provided in the authorization request (contains duplicates)
requested_roles = ["guest", "developer", "guest", "admin", "developer", "guest"]

# A set of mandatory roles for performing administrative functions
required_admin_roles = {"admin", "security_officer", "audit_manager"}

# Convert the list of requested roles into a set to instantly remove duplicates
unique_roles = set(requested_roles)

# Identify the roles that are present in both the list of unique requested roles 
# and the list of mandatory administrative roles (the intersection of the sets)
general_roles = required_admin_roles & unique_roles

# Identify the missing administrative roles that were not requested by the user (set difference)
missing_roles = required_admin_roles - unique_roles

# Check for the presence of the 'security_officer' role 
# within the deduplicated set of requested roles, 
# using a high-performance membership operator that executes in O(1) time
if "security_officer" in unique_roles:
    role_presence = True
else:
    role_presence = False

# Result output
print(f"Unique requested roles: {unique_roles}")
print(f"General administrative roles: {general_roles}")
print(f"Missing administrative roles: {missing_roles}")
print(f"Presence of the 'security_officer' role in the request: {role_presence}")
