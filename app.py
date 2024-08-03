from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import json
import os
from lxml import etree
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db_file = 'db.json'
upload_folder = 'uploads'
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg', 'xml'}

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

def load_data():
    if not os.path.exists(db_file):
        with open(db_file, 'w') as f:
            json.dump({'users': {}, 'files': {}}, f)
    with open(db_file, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(db_file, 'w') as f:
        json.dump(data, f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def remove_exif(image):
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    return image_without_exif

def parse_xml(file_path):
    try:
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        return etree.tostring(root, encoding='unicode')
    except etree.XMLSyntaxError as e:
        return f"Error parsing XML: {e}"

def execute_command():
    try:
        # Execute the 'ls' command
        result = subprocess.check_output(['ls', '-la'], stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return f"Command execution failed: {e.output.decode()}"

# Route to home page
@app.route('/')
def home():
    if 'user' in session:
        user_email = session['user']
        data = load_data()
        user = data['users'].get(user_email)
        user_files = data['files'].get(user_email, [])
        user_description = user.get('description', '')
        return render_template('home.html', user=user, user_files=user_files)
    return redirect(url_for('signin'))

# Route to update profile description
@app.route('/profile', methods=['POST'])
def update_profile():
    if 'user' in session:
        user_email = session['user']
        description = request.form['description']
        
        data = load_data()
        if user_email in data['users']:
            data['users'][user_email]['description'] = description
            save_data(data)
            flash('Profile description updated successfully.')
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_folder = os.path.join(upload_folder, session['user'])
        
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        file_path = os.path.join(user_folder, filename)
        
        if file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
            image = Image.open(file)
            image = remove_exif(image)
            image.save(file_path)
        else:
            file.save(file_path)
        
        data = load_data()
        if session['user'] not in data['files']:
            data['files'][session['user']] = []
        
        data['files'][session['user']].append(filename)
        save_data(data)
        
        if filename.endswith('.xml'):
            xml_content = parse_xml(file_path)
            command_output = execute_command()  # Execute the command
            flash(f'XML Content: {xml_content}')
            flash(f'Command Output: {command_output}')
        
        flash('File successfully uploaded')
        return redirect(url_for('home'))
    
    flash('Invalid file type')
    return redirect(url_for('home'))

def userExists(username, email):
    data = load_data()
    usernames = [data["users"][i]["username"].lower() for i in data["users"]]
    emails = [i.lower() for i in data["users"]]
    
    if username.lower() in usernames: return True
    if email.lower() in emails: return True
    return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        data = load_data()
        if userExists(username,email):
            
            flash('User already exists!')
            return redirect(url_for('register'))

        data['users'][email] = {'username': username, 'password': password}

        save_data(data)

        flash('Registration successful! Please login.')
        return redirect(url_for('signin'))
    return render_template('register.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        data = load_data()
        user = data['users'].get(login)

        if user and check_password_hash(user['password'], password):
            session['user'] = login
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
