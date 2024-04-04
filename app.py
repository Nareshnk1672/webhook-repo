from flask import Flask, request, jsonify
import pymongo

app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["webhook_data"]
collection = db["webhooks"]

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get JSON data from the request
    data = request.get_json()

    # Process the incoming data and store it in MongoDB
    collection.insert_one({
        "author": data["pusher"]["name"],
        "action": data["action"],
        "from_branch": data["pull_request"]["head"]["ref"] if "pull_request" in data else None,
        "to_branch": data["pull_request"]["base"]["ref"] if "pull_request" in data else data["ref"].split("/")[-1],
        "timestamp": data["head_commit"]["timestamp"]
    })

    return "Webhook received successfully"

@app.route('/actions', methods=['GET'])
def get_actions():
    actions = list(collection.find({}, {"_id": 0}))
    return jsonify(actions)

if __name__ == '__main__':
    app.run()

