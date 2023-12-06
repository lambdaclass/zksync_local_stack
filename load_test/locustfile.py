import random

from locust import HttpUser, task, between

import setup.setup

contract_address = "0x8b33164f217d6d86a6fa40e7270f8cb9403e720a"

erc20_contract_balance_command = "zksync-era-cli --l2-port 3050 call --contract " + contract_address + " --function 'balanceOf(address)' --args '0xde03a0b5963f75f1c8485b355ff6d30f3093bde7' --chain-id 270"

erc20_contract_transfer_command = "zksync-era-cli --l2-port 3050 send \
--contract " + contract_address + " \
--function 'transfer(address, uint256)' \
--args 0xa61464658AfeAf65CccaaFD3a512b69A83B77618 200 \
--output-types bool \
--private-key 0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be \
--chain-id 270"



def eth_balance_command(account):
    return f"zksync-era-cli --l2-port 3050 balance --account {account}"


def eth_transfer_command(from_pk, to_address):
    return f"zksync-era-cli --l2-port 3050 transfer --chain-id 270 --amount 1 --from {from_pk} --to {to_address}"


# If wallets are all funded, set with_transfer to False
wallets_with_money = setup.setup.create_wallets_with_money(with_transfer=False, quantity=200)


class ZkSyncWalletUser(HttpUser):
    wait_time = between(1, 5)

    #host = "http://127.0.0.1:5000"
    host = "http://65.21.67.134:3050"
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
