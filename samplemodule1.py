import singleton
print(f"1. {singleton.shared_variable}")
singleton.shared_variable+='(modified by samplemodule1)'
print(f"2. {singleton.shared_variable}")