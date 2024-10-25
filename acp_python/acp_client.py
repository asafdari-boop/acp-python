import json
import uuid
import requests
import logging
from datetime import datetime

class ACPClient:
    def __init__(self, agent_id=None, capabilities=None, base_url="http://localhost:8000", log_level=logging.INFO):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.capabilities = capabilities or []
        self.session_token = None
        self.protocol_version = "1.0"  # ACP version
        self.base_url = base_url

        # Set up logging
        self.logger = logging.getLogger(f"ACPClient-{self.agent_id}")
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info(f"Initialized ACPClient with ID: {self.agent_id}")

    def send_request(self, target_agent, action, payload, priority="normal"):
        """
        Send a request to another agent.
        """
        request = {
            "header": {
                "request_id": str(uuid.uuid4()),
                "sender": self.agent_id,
                "target": target_agent,
                "timestamp": datetime.utcnow().isoformat(),
                "protocol_version": self.protocol_version
            },
            "body": {
                "action": action,
                "priority": priority,
                "payload": payload
            },
            "metadata": {
                "capabilities": self.capabilities,
                "session_token": self.session_token
            }
        }

        self.logger.info(f"Sending request to {target_agent}: action={action}, priority={priority}")
        self.logger.debug(f"Request details: {json.dumps(request, indent=2)}")

        try:
            response = requests.post(self.base_url, json=request)
            response.raise_for_status()
            self.logger.info(f"Request to {target_agent} successful")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error sending request to {target_agent}: {e}")
            return None

    def handle_response(self, response):
        """
        Process a response from another agent.
        """
        if not response:
            print("Error: No response received")
            return None

        try:
            response_data = response if isinstance(response, dict) else json.loads(response)

            # Check for errors
            if 'error' in response_data:
                print(f"Error in response: {response_data['error']}")
                return None

            # Process the response based on the action or content
            action = response_data.get('body', {}).get('action')
            if action == 'REQUEST':
                print(f"Response received: {response_data['body'].get('result')}")
            if action == 'RESPOND':
                print(f"Response received: {response_data['body'].get('result')}")
            elif action == 'DELEGATE':
                print(f"Task delegated: {response_data['body'].get('task_id')}")
            elif action == 'NEGOTIATE':
                print(f"Received negotiation offer: {response_data['body'].get('offer')}")
                # TODO: Implement negotiation logic
            elif action == 'UPDATE':
                print(f"Status update: {response_data['body'].get('status')}")
            elif action == 'COMPLETE':
                print(f"Task completed: {response_data['body'].get('result')}")
            else:
                print(f"Received response: {json.dumps(response_data, indent=2)}")
            # Update client state if necessary
            if 'session_token' in response_data.get('metadata', {}):
                self.session_token = response_data['metadata']['session_token']

            return response_data
        except json.JSONDecodeError:
            print("Error: Invalid JSON in response")
            return None
        except KeyError as e:
            print(f"Error: Missing key in response - {e}")
            return None

    def start_session(self):
        """
        Start a new session.
        """
        self.session_token = str(uuid.uuid4())
        print(f"Session started with token: {self.session_token}")

    def end_session(self):
        """
        End the current session.
        """
        self.session_token = None
        print("Session ended")

    def negotiate(self, target_agent, proposal, max_rounds=3):
        """
        Initiate a negotiation with another agent.
        """
        for round in range(max_rounds):
            print(f"Negotiation round {round + 1}")

            # Send negotiation proposal
            response = self.send_request(target_agent, "NEGOTIATE", proposal)

            if not response:
                print("No response received during negotiation")
                return None

            response_data = self.handle_response(response)

            if not response_data:
                print("Error handling negotiation response")
                return None

            action = response_data.get('body', {}).get('action')

            if action == 'NEGOTIATE':
                print("Negotiation accepted")
                return response_data['body'].get('result')
            elif action == 'negotiation_rejected':
                print("Negotiation rejected")
                return None
            elif action == 'negotiation_counter':
                counter_proposal = response_data['body'].get('counter_proposal')
                print(f"Received counter-proposal: {counter_proposal}")

                # Here you could implement logic to automatically adjust the proposal
                # For now, we'll just update our proposal with the counter-proposal
                proposal = counter_proposal
            else:
                print(f"Unexpected response during negotiation: {action}")
                return None

        print("Max negotiation rounds reached without agreement")
        return None

    def delegate_task(self, target_agent, task):
        """
        Delegate a task to another agent.
        """
        task_object = {
            "task_id": str(uuid.uuid4()),
            "description": task,
            "status": "pending"
        }

        response = self.send_request(target_agent, "DELEGATE", task_object)

        if not response:
            print("No response received during task delegation")
            return None

        response_data = self.handle_response(response)

        if not response_data:
            print("Error handling task delegation response")
            return None

        action = response_data.get('body', {}).get('action')

        if action == 'DELEGATE':
            print(f"Task accepted by {target_agent}")
            return response_data['body'].get('task_id')
        elif action == 'task_rejected':
            print(f"Task rejected by {target_agent}")
            return None
        else:
            print(f"Unexpected response during task delegation: {action}")
            return None

    def respond(self, request_id, result):
        """
        Respond to a request from another agent.
        """
        response = {
            "header": {
                "response_id": str(uuid.uuid4()),
                "request_id": request_id,
                "sender": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "protocol_version": self.protocol_version
            },
            "body": {
                "action": "RESPOND",
                "result": result
            },
            "metadata": {
                "capabilities": self.capabilities,
                "session_token": self.session_token
            }
        }

        self.logger.info(f"Sending response to request {request_id}")
        self.logger.debug(f"Response details: {json.dumps(response, indent=2)}")

        try:
            response = requests.post(self.base_url, json=response)
            response.raise_for_status()
            self.logger.info(f"Response to request {request_id} successful")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error sending response to request {request_id}: {e}")
            return None

    def complete_task(self, task_id, result):
        """
        Notify that a task is completed.
        """
        response = {
            "header": {
                "response_id": str(uuid.uuid4()),
                "task_id": task_id,
                "sender": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "protocol_version": self.protocol_version
            },
            "body": {
                "action": "COMPLETE",
                "result": result
            },
            "metadata": {
                "capabilities": self.capabilities,
                "session_token": self.session_token
            }
        }

        self.logger.info(f"Completing task {task_id}")
        self.logger.debug(f"Completion details: {json.dumps(response, indent=2)}")

        try:
            response = requests.post(self.base_url, json=response)
            response.raise_for_status()
            self.logger.info(f"Task {task_id} completion notification successful")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error completing task {task_id}: {e}")
            return None

    def update(self, update_info):
        """
        Notify other agents about state changes or new information.
        """
        update_message = {
            "header": {
                "update_id": str(uuid.uuid4()),
                "sender": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "protocol_version": self.protocol_version
            },
            "body": {
                "action": "UPDATE",
                "update_info": update_info
            },
            "metadata": {
                "capabilities": self.capabilities,
                "session_token": self.session_token
            }
        }

        self.logger.info(f"Sending update: {update_info}")
        self.logger.debug(f"Update details: {json.dumps(update_message, indent=2)}")

        try:
            response = requests.post(self.base_url, json=update_message)
            response.raise_for_status()
            self.logger.info(f"Update notification successful")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error sending update: {e}")
            return None
