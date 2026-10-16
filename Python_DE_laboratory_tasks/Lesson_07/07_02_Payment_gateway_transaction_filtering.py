# List of transactions received from the payment gateway
raw_transactions = ["SUCCESS:100", "FAILED:50", "SUCCESS:-10", "SUCCESS:0", "SUCCESS:250", "ERROR:200"]

# Implementing filtering in a single line using List Comprehension
cleaned_transactions = [int(item[item.find(":")+1:len(item)]) 
                        for item in raw_transactions 
                        if item.startswith("SUCCESS:") and int(item[item.find(":")+1:len(item)]) > 0]

# Result output
print(f"Cleaned Transactions: {cleaned_transactions}")

