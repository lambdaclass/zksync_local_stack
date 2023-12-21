import json
import subprocess
import unittest

import requests


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        config_file_path = '../config.json'
        self.flask_url = "http://127.0.0.1:5000/run"

        # Open the file and load the data
        with open(config_file_path, 'r') as file:
            data = json.load(file)

        self.node_host = data["node_host"]
        self.rich_wallets = data["rich_wallets"]
        self.rich_wallet = self.rich_wallets[0]["address"]

    def test_01_can_hit_the_chain_using_cli(self):
        command = f"zksync-era-cli --host {self.node_host} --l2-port 3050 balance --account {self.rich_wallet}"

        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        self.assertIsNotNone(output)

    def test_02_can_ask_for_balance_of_zksync_stack_rich_wallet_and_it_have_funds(self):
        command = f"zksync-era-cli --host {self.node_host} --l2-port 3050 balance --account {self.rich_wallet}"

        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
        account_balance = output.split()[-1]

        self.assertTrue(int(account_balance) > 100)

    def test_03_can_hit_the_chain_using_flask(self):
        command = f"zksync-era-cli --host {self.node_host} --l2-port 3050 balance --account {self.rich_wallet}"
        response = -1

        try:
            response = requests.post(self.flask_url, json={"command": command})
            print(response)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
