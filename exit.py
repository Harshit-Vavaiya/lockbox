import os

# Path to the db.json file
db_path = 'db.json'
uploads_path = 'uploads'

def clear_db():
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"{db_path} has been cleared.")
    else:
        print(f"{db_path} does not exist.")

    # Clear the uploads directory
    if os.path.exists(uploads_path):
        for root, dirs, files in os.walk(uploads_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        print(f"{uploads_path} directory has been cleared.")
    else:
        print(f"{uploads_path} directory does not exist.")

clear_db()
