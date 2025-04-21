Key Features:

    Disk Image Analysis: Extract file metadata and recover deleted files.

    Keyword Search: Search for specific terms within the disk image.

    Timeline Analysis: Analyze file creation, modification, and access times for timeline creation.

    Report Generation: Automate report generation for findings.

Step 1: Set up your environment

Ensure you have Kali Linux installed with Sleuth Kit and pytsk3 libraries. If you're missing any packages, you can install them using:

sudo apt-get install sleuthkit python3-pip
pip install pytsk3

Step 2: Python Script for Disk Image Analysis and File Metadata Extraction

import pytsk3
import os
from datetime import datetime

# Function to analyze a disk image and extract file metadata
def analyze_disk_image(image_path):
    img_info = pytsk3.Img_Info(image_path)
    fs_info = pytsk3.FS_Info(img_info)

    # Iterate through all files and directories in the root directory
    for directory in fs_info.open_dir(path="/"):
        print("[+] Directory:", directory.info.name.name.decode('utf-8'))
        
        for f in directory:
            if f.info.name.name.decode('utf-8') == "$OrphanFiles":
                continue

            file_path = "{}/{}".format(directory.info.name.name.decode('utf-8'), f.info.name.name.decode('utf-8'))
            print(f"[+] File: {file_path}")
            print(f"    [+] Size: {f.info.meta.size} bytes")

            # Metadata extraction
            metadata = f.info.meta
            print(f"    [+] Created: {format_time(metadata.crtime)}")
            print(f"    [+] Modified: {format_time(metadata.mtime)}")
            print(f"    [+] Accessed: {format_time(metadata.atime)}")
            print(f"    [+] Permissions: {oct(metadata.mode)}")
            
            # Recovering deleted files (files with an empty name or deleted)
            if f.info.meta.flags == pytsk3.TSK_FS_META_FLAG_UNALLOC:
                print("    [+] Deleted File")
            
            print("\n")

# Function to format timestamps into a readable format
def format_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/disk/image.dd"  # Change this to your disk image path
    analyze_disk_image(image_path)

Explanation:

    Metadata Extraction: This script extracts file metadata such as creation time (crtime), modification time (mtime), access time (atime), and file permissions.

    Deleted File Detection: If a file has been deleted but still exists in the disk image (unallocated), it will be flagged as a deleted file.

    Formatted Timestamps: The format_time() function converts timestamps into a human-readable format (YYYY-MM-DD HH:MM:SS).

Step 3: Python Script for Keyword Search in Disk Image

You can use keyword searching to look for sensitive information such as passwords, email addresses, or other strings within a disk image.

import pytsk3
import re

# Function to perform keyword search in disk image
def search_keyword_in_disk(image_path, keyword):
    img_info = pytsk3.Img_Info(image_path)
    fs_info = pytsk3.FS_Info(img_info)
    
    print(f"[+] Searching for keyword '{keyword}' in the disk image...\n")
    
    # Iterate through files and search for the keyword
    for directory in fs_info.open_dir(path="/"):
        for f in directory:
            if f.info.name.name.decode('utf-8') == "$OrphanFiles":
                continue

            file_path = "{}/{}".format(directory.info.name.name.decode('utf-8'), f.info.name.name.decode('utf-8'))
            print(f"Checking file: {file_path}")

            try:
                file_data = f.read_random(0, f.info.meta.size)
                if re.search(keyword.encode(), file_data):
                    print(f"[+] Keyword '{keyword}' found in: {file_path}")
            except Exception as e:
                print(f"[-] Could not read file {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/disk/image.dd"  # Change this to your disk image path
    keyword = "password"  # Change this to your search keyword
    search_keyword_in_disk(image_path, keyword)

Explanation:

    Keyword Search: This script searches for a specified keyword in all files of the disk image. It reads each file in chunks and performs a regular expression search.

    Error Handling: If a file cannot be read (due to permissions or corruption), the script catches and prints the error without crashing.

Step 4: Python Script for Timeline Analysis (File Activity Over Time)

For forensic investigations, it's often helpful to visualize when files were created, modified, or accessed. This script generates a timeline of file activity.

import pytsk3
from datetime import datetime

# Function to create a timeline of file activity
def generate_timeline(image_path):
    img_info = pytsk3.Img_Info(image_path)
    fs_info = pytsk3.FS_Info(img_info)

    timeline = []

    for directory in fs_info.open_dir(path="/"):
        for f in directory:
            if f.info.name.name.decode('utf-8') == "$OrphanFiles":
                continue

            file_path = "{}/{}".format(directory.info.name.name.decode('utf-8'), f.info.name.name.decode('utf-8'))
            metadata = f.info.meta

            created_time = format_time(metadata.crtime)
            modified_time = format_time(metadata.mtime)
            accessed_time = format_time(metadata.atime)

            timeline.append({
                "file": file_path,
                "created": created_time,
                "modified": modified_time,
                "accessed": accessed_time
            })

    # Sorting files by modification time
    timeline_sorted = sorted(timeline, key=lambda x: x['modified'])
    
    print("[+] File Activity Timeline:")
    for entry in timeline_sorted:
        print(f"{entry['modified']} - {entry['file']}")

# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/disk/image.dd"  # Change this to your disk image path
    generate_timeline(image_path)

Explanation:

    Timeline Generation: This script creates a timeline of file activity based on the modification time of each file.

    Sorting: It sorts the timeline by file modification time, so you can see a chronological list of file changes and activities.

Step 5: Report Generation

Now that you have collected evidence, you may want to generate a simple report of the findings. Here’s an example of automated report generation:

def generate_report(data, filename="forensic_report.txt"):
    with open(filename, 'w') as file:
        for entry in data:
            file.write(f"File: {entry['file']}\n")
            file.write(f"  Created: {entry['created']}\n")
            file.write(f"  Modified: {entry['modified']}\n")
            file.write(f"  Accessed: {entry['accessed']}\n\n")
    print(f"[+] Report generated: {filename}")

# Example usage
if __name__ == "__main__":
    timeline_data = [
        {"file": "file1.txt", "created": "2025-01-01 12:00:00", "modified": "2025-01-02 15:00:00", "accessed": "2025-01-02 14:30:00"},
        {"file": "file2.doc", "created": "2025-01-03 13:00:00", "modified": "2025-01-03 18:00:00", "accessed": "2025-01-03 17:30:00"},
    ]
    generate_report(timeline_data)

Final Thoughts:

    Forensic Analysis: These scripts provide a framework to analyze disk images, recover deleted files, perform keyword searches, and create file activity timelines.

    Report Generation: They also allow you to automate the process of generating forensic reports, which is essential for documenting findings during investigations.

Make sure to adapt these scripts based on your investigation’s needs. They can be expanded with more advanced features such as file carving, hash analysis, and network traffic analysis.
