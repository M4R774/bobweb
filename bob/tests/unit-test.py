import unittest
import message_handler
import telepot
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    # TODO: Fixture: crete new database/table
    def test_test(self):
        self.assertEqual(True, True)

    def test_huutista(self):
        # Create message object
        # Call the function with the message object
        # Check if the response was correct???

        with patch('message_handler.telepot.sendMessage') as mock_send_message:
            pass
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
