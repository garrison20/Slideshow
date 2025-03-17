import os
import random
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "password"
app.config["UPLOAD_FOLDER"] = os.path.join(f"{os.path.dirname(os.path.realpath(__file__))}", "files")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "heic"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # POST request missing the file
        if "file" not in request.files:
            flash("Failed to send image to server!") 
            return redirect(request.url)
        file = request.files["file"]
        # No file selected
        if file.filename == "":
            flash('No image selected!')
            return redirect(request.url)
        # Something went wrong with the file
        if not file:
            flash("Error uploading image!")
            return redirect(request.url)
        # Filetype not allowed
        if not allowed_file(file.filename):
            flash("Filetype not allowed!")
            return redirect(request.url)
        
        filename = f"{datetime.now().strftime('%y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1]}"
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("Successfully uploaded image!")
        return redirect(url_for('upload_file'))
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)