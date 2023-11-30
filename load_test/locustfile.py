from locust import HttpUser, task, between

contract_address = "0x8b33164f217d6d86a6fa40e7270f8cb9403e720a"

erc20_contract_balance_command = "zksync-era-cli --l2-port 3050 call --contract " + contract_address + " --function 'balanceOf(address)' --args '0xde03a0b5963f75f1c8485b355ff6d30f3093bde7' --chain-id 270"

erc20_contract_transfer_command = "zksync-era-cli --l2-port 3050 send \
--contract " + contract_address + " \
--function 'transfer(address, uint256)' \
--args 0xa61464658AfeAf65CccaaFD3a512b69A83B77618 200 \
--output-types bool \
--private-key 0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be \
--chain-id 270"

eth_balance_command = "zksync-era-cli --l2-port 3050 balance --account 0x36615Cf349d7F6344891B1e7CA7C72883F5dc049"

eth_transfer_command = "zksync-era-cli --l2-port 3050 transfer --chain-id 270 --amount 100 --from 0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110 --to 0xa61464658AfeAf65CccaaFD3a512b69A83B77618"


class ZkSyncWalletUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:5000"

    @task
    def check_balance(self):
        self.client.post("/run", json={"command": eth_balance_command}, name="ETH Balance")

    @task
    def transfer_eth(self):
        self.client.post("/run", json={"command": eth_transfer_command}, name="ETH Transfer")


class ZkSyncContractUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:5000"

    @task
    def check_erc20_token_balance(self):
        self.client.post("/run", json={"command": erc20_contract_balance_command}, name="ERC20 Balance")

    @task
    def erc20_token_transfer(self):
        self.client.post("/run", json={"command": erc20_contract_transfer_command}, name="ERC20 Transfer")
