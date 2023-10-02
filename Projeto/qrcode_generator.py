from flask import Flask, render_template, request, send_from_directory, redirect, jsonify
import os
import datetime
import qrcode
from os.path import exists

FILE_DIR = 'files/'
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("qrcodegenerator.html") 
    else:
        print(request.form)
        qrcode_text = request.form['qrcodetext']
        img = qrcode.make(qrcode_text)
        type(img)  # qrcode.image.pil.PilImage
        filename ="qrcode" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        img.save(FILE_DIR + filename)
        return send_from_directory(directory=FILE_DIR, path=filename)

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)