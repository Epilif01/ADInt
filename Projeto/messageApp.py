from flask import (
    Flask,
    request,
    jsonify,
)
import message_DB as db

app = Flask(__name__)

@app.route("/api/sendmessage/<user_id>", methods=["POST"])
def api_send_message(user_id):
    try:
        print("entrei aqui")
        print(request)
        message = request.json["message"]
        destination = request.json["destination"]
        print(message)
        print(destination)
        db.new_message(user_id, message, destination)
        return jsonify({"message": "Message sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/messagesreceived/<user_id>", methods=["GET"])
def api_messages_received(user_id):
    messages = []
    for row in db.messages_received(user_id):
        messages.append((row.sender,row.message))
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, debug=True)
