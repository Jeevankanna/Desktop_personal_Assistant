import os

MEMORY_FILE = "memory.txt"

# Function to store information
def remember_this(info):
    with open(MEMORY_FILE, "a") as file:
        file.write(info + "\n")  # Append new data
    return f"Got it! I will remember that: {info}"

# Function to recall stored information
def recall_memory():
    if not os.path.exists(MEMORY_FILE) or os.stat(MEMORY_FILE).st_size == 0:
        return "I don't remember anything yet."
    
    with open(MEMORY_FILE, "r") as file:
        memories = file.readlines()
    
    return "Here’s what you asked me to remember:\n" + "".join(memories).strip()

# Function to clear memory
def forget_everything():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return "I have forgotten everything you told me."
