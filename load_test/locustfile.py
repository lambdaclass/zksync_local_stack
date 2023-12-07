import random

from locust import HttpUser, task, between

import setup.setup

from utils import eth_balance_command, eth_transfer_command


# If wallets are all funded, set with_transfer to False
wallets_with_money = setup.setup.create_wallets_with_money_for_zksync_stack(with_transfer=False, quantity=100)


class ZkSyncWalletUser(HttpUser):
    wait_time = between(1, 5)

    host = "http://127.0.0.1:5000" #local flask server

    failed_wallets = {}

    #@task
    def check_balance(self):
        wallet = random.choice(wallets_with_money)
        self.client.post("/run", json={"command": eth_balance_command(wallet["address"])}, name="ETH Balance")

    @task
    def transfer_eth(self):
        from_wallet, to_wallet = random.sample(wallets_with_money, 2)
        post_response = self.client.post("/run", json={"command": eth_transfer_command(from_wallet["privateKey"], to_wallet["address"])}, name="ETH Transfer")


# class ZkSyncContractUser(HttpUser):
#    wait_time = between(1, 5)
#    host = "http://127.0.0.1:5000"
#
#   @task
#    def check_erc20_token_balance(self):
#        self.client.post("/run", json={"command": erc20_contract_balance_command}, name="ERC20 Balance")
#
#    @task
#    def erc20_token_transfer(self):
#        self.client.post("/run", json={"command": erc20_contract_transfer_command}, name="ERC20 Transfer")
