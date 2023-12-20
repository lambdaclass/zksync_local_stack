import json
import random

from locust import HttpUser, task, between

from utils import eth_balance_command, eth_transfer_command, erc20_contract_balance_command, erc20_transfer_command
from setup import create_wallets_with_money, deploy_erc20_with_wallets_with_money

# Setup wallets from config
config_file_path = 'config.json'
with open(config_file_path, 'r') as file:
    data = json.load(file)
should_fund_wallets = data["fund_wallets"] == "True"
amount_of_wallets = int(data["amount_of_wallets"])
rich_wallets = data["rich_wallets"]
node_host = data["node_host"]

wallets_with_money = create_wallets_with_money(node_host=node_host, with_transfer=should_fund_wallets,
                                               amount_of_wallets=amount_of_wallets, rich_wallets=rich_wallets)
erc20_contract_address = deploy_erc20_with_wallets_with_money(wallets_with_money)

class ZkSyncWalletUser(HttpUser):
    wait_time = between(1, 5)

    host = "http://127.0.0.1:5000"  # local flask server

    @task
    def check_balance(self):
        wallet = random.choice(wallets_with_money)
        self.client.post("/run", json={"command": eth_balance_command(data["node_host"], wallet["address"])},
                         name="ETH Balance")

    @task
    def transfer_eth(self):
        from_wallet, to_wallet = random.sample(wallets_with_money, 2)
        self.client.post("/run", json={
            "command": eth_transfer_command(data["node_host"], from_wallet["privateKey"], to_wallet["address"], 1)},
                         name="ETH Transfer")

    @task
    def check_erc20_token_balance(self):
        wallet = random.choice(wallets_with_money)
        self.client.post("/run", json={
            "command": erc20_contract_balance_command(data["node_host"], wallet["address"], erc20_contract_address)},
                         name="ERC20 Balance")

    @task
    def transfer_eth(self):
        from_wallet, to_wallet = random.sample(wallets_with_money, 2)
        self.client.post("/run", json={
            "command": erc20_transfer_command(data["node_host"], from_wallet["privateKey"], to_wallet["address"], 1)},
                         name="ERC20 Transfer")
