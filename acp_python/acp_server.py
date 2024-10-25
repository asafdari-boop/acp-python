from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

class ACPServer:
    def __init__(self):
        self.agents = {}  # Store registered agents

    def register_agent(self, agent_id, capabilities):
        self.agents[agent_id] = {
            "capabilities": capabilities,
            "last_seen": datetime.utcnow()
        }

    def handle_request(self, request_data):
        try:
            header = request_data.get('header', {})
            body = request_data.get('body', {})
            metadata = request_data.get('metadata', {})

            sender = header.get('sender')
            action = body.get('action')
            payload = body.get('payload')

            if not sender or not action:
                return jsonify({"error": "Invalid request format"}), 400

            # Update agent's last seen time
            if sender in self.agents:
                self.agents[sender]["last_seen"] = datetime.utcnow()

            # Process the request based on the action
            if action == "register":
                self.register_agent(sender, metadata.get('capabilities', []))
                return jsonify({"message": "Agent registered successfully"}), 200
            elif action == "REQUEST":
                # Implement task or query logic here
                return jsonify({"action": "REQUEST", "result": "Task or query initiated"}), 200
            elif action == "RESPOND":
                # Implement response handling logic here
                return jsonify({"action": "RESPOND", "result": "Response received"}), 200
            elif action == "DELEGATE":
                # Implement task delegation logic here
                return jsonify({"action": "DELEGATE", "task_id": str(uuid.uuid4())}), 200
            elif action == "NEGOTIATE":
                # Implement negotiation logic here
                return jsonify({"action": "NEGOTIATE", "result": "Negotiation successful"}), 200
            elif action == "UPDATE":
                # Implement update handling logic here
                return jsonify({"action": "UPDATE", "status": "Update received"}), 200
            elif action == "COMPLETE":
                # Implement task completion logic here
                return jsonify({"action": "COMPLETE", "result": "Task completed"}), 200
            else:
                return jsonify({"error": f"Unsupported action: {action}"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500

acp_server = ACPServer()

@app.route('/', methods=['POST'])
def agent_endpoint():
    request_data = request.json
    return acp_server.handle_request(request_data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
