import os
import json
from werkzeug.security import generate_password_hash

# User data with plaintext passwords
user_data = {
    "users": {
        "admin@ctf.de": {
            "username": "Admin",
            "password": "8zsdamje2",
            "description":"Update your description.s"
        },
        "Raj@waterfall.eu": {
            "username": "Raj",
            "password": "90t$0$3cure",
            "description":"Update your description."
        },
        "Alex@waterfall.eu": {
            "username": "Alex",
            "password": "8^&sd09.",
            "description":"Update your description."
        },
        "Bob@waterfall.eu": {
            "username": "Bob",
            "password": "B$$?sdj",
            "description":"Update your description."
        },
        "Cindy@waterfall.eu": {
            "username": "Cindy",
            "password": "!143a0t",
            "description":"Update your description."
        },
        "john.doe@example.com": {
            "username": "John Doe",
            "password": "jD@5r#0s3l",
            "description":"Update your description."
        },
        "jane.smith@example.com": {
            "username": "Jane Smith",
            "password": "sM!th7@3kq",
            "description":"Update your description."
        },
        "michael.brown@example.com": {
            "username": "Michael Brown",
            "password": "M!c#b0wn_2024",
            "description":"Update your description."
        },
        "emily.jones@example.com": {
            "username": "Emily Jones",
            "password": "Em!lyJ@ne9",
            "description":"Update your description."
        }
    },
    "files": {}
}

# Define file contents
files_content = {
    "secret_msg.txt": "SECRET",
    "share1.txt": "1 11",
    "share2.txt": "2 11",
    "share3.txt": "3 11",
    "share4.txt": "4 11",
    "john_file1.txt": "John Doe's data",
    "jane_file1.txt": "Jane Smith's data",
    "michael_file1.txt": "Michael Brown's data",
    "emily_file1.txt": "Emily Jones's data"
}

# Define users and their files
users_files = {
    "Admin": ["secret_msg.txt"],
    "Raj": ["share1.txt"],
    "Alex": ["share2.txt"],
    "Bob": ["share3.txt"],
    "Cindy": ["share4.txt"],
    "John Doe": ["john_file1.txt"],
    "Jane Smith": ["jane_file1.txt"],
    "Michael Brown": ["michael_file1.txt"],
    "Emily Jones": ["emily_file1.txt"]
}

# Create user directories and files
base_path = 'uploads'
if not os.path.exists(base_path):
    os.makedirs(base_path)

for user, files in users_files.items():
    user_folder = os.path.join(base_path, user)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    user_files = []
    for file_name in files:
        file_path = os.path.join(user_folder, file_name)
        user_files.append(file_path)
        with open(file_path, 'w') as file:
            file.write(files_content[file_name])
    # Add files to user data
    email = next(email for email, details in user_data["users"].items() if details["username"] == user)
    user_data["files"][email] = user_files

# Update the user data with hashed passwords
for email, details in user_data["users"].items():
    details["password"] = generate_password_hash(details["password"])


# Write the updated data to db.json
with open('db.json', 'w') as file:
    json.dump(user_data, file, indent=4)

print("User data with hashed passwords and files has been written to db.json.")
