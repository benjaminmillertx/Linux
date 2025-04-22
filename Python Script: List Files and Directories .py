import os
import platform

def list_files():
    """
    Lists files and directories in the current working directory.
    Uses the correct system command depending on the operating system.

    - On Linux/Mac: uses 'ls'
    - On Windows: uses 'dir'
    """

    # Detect the operating system
    current_os = platform.system()
    print(f"Operating System Detected: {current_os}")

    # Choose appropriate command based on OS
    if current_os == "Windows":
        command = "dir"
    else:
        command = "ls -la"  # shows hidden files and more detail

    print(f"\nListing files using command: {command}\n")

    # Execute the command and show the output
    os.system(command)

# Run the function
if __name__ == "__main__":
    list_files()
