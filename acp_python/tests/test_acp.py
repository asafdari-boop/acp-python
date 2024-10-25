import unittest
from unittest.mock import patch, MagicMock
import json
from acp_python.acp_client import ACPClient

class TestACPClient(unittest.TestCase):

    def setUp(self):
        self.client = ACPClient(agent_id="test_agent", capabilities=["test"])

    def test_initialization(self):
        self.assertEqual(self.client.agent_id, "test_agent")
        self.assertEqual(self.client.capabilities, ["test"])
        self.assertIsNone(self.client.session_token)
        self.assertEqual(self.client.protocol_version, "1.0")

    @patch('requests.post')
    def test_send_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        response = self.client.send_request("target_agent", "test_action", {"key": "value"})

        self.assertEqual(response, {"status": "success"})
        mock_post.assert_called_once()

    def test_handle_response(self):
        test_response = {
            "body": {
                "action": "task_completed",
                "result": "Task done"
            },
            "metadata": {
                "session_token": "new_token"
            }
        }
        result = self.client.handle_response(test_response)
        self.assertEqual(result, test_response)
        self.assertEqual(self.client.session_token, "new_token")

    @patch('acp_python.acp_client.ACPClient.send_request')
    def test_negotiate(self, mock_send_request):
        mock_send_request.side_effect = [
            {"body": {"action": "negotiation_counter", "counter_proposal": "counter"}},
            {"body": {"action": "negotiation_accepted", "result": "success"}}
        ]

        result = self.client.negotiate("target_agent", "initial_proposal")

        self.assertEqual(result, "success")
        self.assertEqual(mock_send_request.call_count, 2)

    @patch('acp_python.acp_client.ACPClient.send_request')
    def test_delegate_task(self, mock_send_request):
        mock_send_request.return_value = {
            "body": {
                "action": "task_accepted",
                "task_id": "test_task_id"
            }
        }

        result = self.client.delegate_task("target_agent", "test_task")

        self.assertEqual(result, "test_task_id")
        mock_send_request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
