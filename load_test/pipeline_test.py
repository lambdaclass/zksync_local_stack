import json
import subprocess
import unittest
import os

import requests


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        config_file_path = 'config.json'
        self.flask_url = "http://127.0.0.1:5000/run"

# Open the file and load the data
        with open(config_file_path, 'r') as file:
            data = json.load(file)

        self.host = data["host"]
        self.rich_wallet = data["rich_wallet"]

    def test_01_can_hit_the_chain_using_cli(self):
        command = f"zksync-era-cli --host {self.host} --l2-port 3050 balance --account {self.rich_wallet}"

        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
        self.assertIsNotNone(output)

    def test_02_can_hit_the_chain_using_flask(self):
        command = f"zksync-era-cli --host {self.host} --l2-port 3050 balance --account {self.rich_wallet}"
        response = -1

        try:
            response = requests.post(self.flask_url, json={"command": command})
            print(response)
            # Check if the request was successful (status code 200)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

        self.assertEqual(200, response.status_code)



if __name__ == '__main__':
    unittest.main()
