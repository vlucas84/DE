#Original, unprocessed string from the data source
raw_user_record = " 10827 ; aLeXanDer_vLaDimiRov ; mInSk ; ACTIVE "

# Split the string into individual elements, using a semicolon (;) as a delimiter
raw_list = raw_user_record.split(';')

# Strip leading and trailing whitespace characters from each resulting element
for i in range(len(raw_list)):
    raw_list[i] = raw_list[i].strip()

# Apply the prefix "UID-" to the user identifier (the first element) 
# using string formatting.
raw_list[0] = f"UID-{raw_list[0]}"

# Transform the username (the second element) by replacing the underscore (_) 
# with a space and formatting the words to use the correct casing 
# (capitalizing the first letter of each word)
raw_list[1] = raw_list[1].replace('_', ' ').title()

# Convert the city name (the third element) to uppercase
raw_list[2] = raw_list[2].upper()

# Convert the user status (the fourth element) to lowercase
raw_list[3] = raw_list[3].lower()

# Combine the processed elements into a single string, using `|` as a delimiter, 
# and result output
cleaned_record = " | ".join(raw_list)
print(f"Normalized record: {cleaned_record}")
