For educational, lawful ethical hacking or dfir only.
Script by Benjamin Hunter Miller

import hashlib
import os
from pathlib import Path

# Function to perform password cracking using a provided hash and wordlist
def crack_password(hash_type, password_hash, wordlist):
    # Validate the hash_type provided is a valid hashlib function
    if hash_type not in hashlib.algorithms_guaranteed:
        print(f"Error: '{hash_type}' is not a valid hash type. Supported types: {', '.join(hashlib.algorithms_guaranteed)}")
        return

    # Convert the wordlist path to a Path object (better for handling files across platforms)
    wordlist_path = Path(wordlist)
    
    # Check if wordlist file exists
    if not wordlist_path.is_file():
        print(f"Error: The file '{wordlist}' does not exist. Please check the file path.")
        return

    print(f"Cracking password using {hash_type.upper()} hash type...")

    # Open and process the wordlist file line by line
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            total_lines = sum(1 for _ in file)  # Count the total lines in the wordlist
            file.seek(0)  # Reset the file pointer to the beginning

            # Loop through each word in the wordlist
            for line_number, line in enumerate(file, start=1):
                word = line.strip()  # Remove any extra whitespace or newline characters

                # Hash the current word using the specified hash algorithm
                hashed_word = getattr(hashlib, hash_type)(word.encode()).hexdigest()

                # Compare the hash of the current word with the given password hash
                if hashed_word == password_hash:
                    print(f"Password cracked! The password is: '{word}' (found on line {line_number})")
                    return  # Exit after finding the password

                # Show progress every 1000 words
                if line_number % 1000 == 0:
                    print(f"Processed {line_number}/{total_lines} words...")

        # If the loop finishes without a match
        print("Password not found in the wordlist.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example with md5 hash (feel free to replace with other hash types)
crack_password("md5", "e10adc3949ba59abbe56e057f20f883e", "wordlist.txt")

