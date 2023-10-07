from flask import Flask, render_template, request, send_from_directory, redirect, jsonify
import os
import datetime
import qrcode
from os.path import exists
import uuid
import glob

FILE_DIR = 'files/'

def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"qrcode_{unique_id}_{timestamp}.png"
    return filename

def cleanup_old_files():
    # Delete QR code files older than 20 seconds
    expiration_time = datetime.datetime.now() - datetime.timedelta(seconds=20)
    files_to_delete = glob.glob(os.path.join(FILE_DIR, 'qrcode_*'))
    
    for file_path in files_to_delete:
        if os.path.getmtime(file_path) < expiration_time.timestamp():
            os.remove(file_path)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("qrcodegenerator.html") 
    else:
        cleanup_old_files()
        print(request.form)
        qrcode_text = request.form['qrcodetext']
        img = qrcode.make(qrcode_text)
        type(img)  # qrcode.image.pil.PilImage
        filename = generate_unique_filename()
        img.save(FILE_DIR + filename)
        return send_from_directory(directory=FILE_DIR, path=filename)

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)