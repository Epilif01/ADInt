from flask import Flask, request, send_from_directory, jsonify
import os
import datetime
import qrcode
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
    expiration_time = datetime.datetime.now() - datetime.timedelta(seconds=120)
    files_to_delete = glob.glob(os.path.join(FILE_DIR, 'qrcode_*'))
    
    for file_path in files_to_delete:
        if os.path.getmtime(file_path) < expiration_time.timestamp():
            os.remove(file_path)

def create_qrcode(data):
    cleanup_old_files()
    img = qrcode.make(data)
    type(img)  # qrcode.image.pil.PilImage
    filename = generate_unique_filename()
    img.save(FILE_DIR + filename)
    return filename

app = Flask(__name__)
    
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(directory=FILE_DIR, path=filename)

@app.route('/api', methods=['POST'])
def post_resource():
    data = request.get_json()
    filename = create_qrcode(data['link'])
    return jsonify({"filename":"%s" % filename})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)