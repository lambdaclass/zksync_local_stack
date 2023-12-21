import random
import subprocess

from ecpy.curves import Curve
from sha3 import keccak_256

from utils import eth_transfer_command, erc20_transfer_command

random.seed(42)


def transfer_with(node_host, amount, from_pk, to_address):
    command = eth_transfer_command(node_host, from_pk, to_address, amount)
    return subprocess.Popen(command, shell=True, text=True)


def transfer_erc20(node_host, amount, from_pk, to, contract_address):
    command = erc20_transfer_command(node_host, from_pk, to, amount, contract_address)
    return subprocess.Popen(command, shell=True, text=True)


def generate_new_wallet():
    private_key = generate_private_key()
    address = get_address_from(private_key)
    return {"address": address,
            "privateKey": hex(private_key)
            }


def generate_private_key():
    pk = "".join(random.choices(["0", "1"], k=256))
    actual_int = int(pk, base=2)
    if len(hex(actual_int)) != 66:
        return generate_private_key()
    return actual_int


def get_address_from(private_key):
    cv = Curve.get_curve('secp256k1')
    pu_key = private_key * cv.generator  # just multiplying the private key by generator point (EC multiplication)

    concat_x_y = pu_key.x.to_bytes(32, byteorder='big') + pu_key.y.to_bytes(32, byteorder='big')
    eth_addr = '0x' + keccak_256(concat_x_y).digest()[-20:].hex()
    return eth_addr


def create_wallets_with_money(node_host, with_transfer, amount_of_wallets, rich_wallets):
    new_wallets = [generate_new_wallet() for _ in range(amount_of_wallets)]

    total_transferred = 0
    range_to_use = int(amount_of_wallets / len(rich_wallets))
    for _ in range(range_to_use):
        processes_to_wait = []
        for wallet in rich_wallets:
            from_pk = wallet["privateKey"]
            to = new_wallets[total_transferred]["address"]
            amount = 4536975000000000000
            if with_transfer:
                process = transfer_with(node_host, amount, from_pk, to)
                processes_to_wait.append(process)
            total_transferred = total_transferred + 1
        for p in processes_to_wait:
            p.wait()
    return new_wallets


def create_erc20_wallets_with_money(node_host, with_transfer, wallets, contract_owner_wallet, contract_address):
    total_transferred = 0

    for wallet in wallets:
        amount = 1000
        if with_transfer:
            process = transfer_erc20(node_host, amount, contract_owner_wallet["privateKey"], wallet["address"], contract_address)
            process.wait()
        total_transferred = total_transferred + 1

    return wallets


def deploy_erc20_with_rich_account(host, contract_owner_wallet):
    owner_wallet_address_ = contract_owner_wallet["address"]
    owner_private_key = contract_owner_wallet["privateKey"]
    deploy_command = f"zksync-era-cli --host {host} --l2-port 3050 deploy --project-root contracts/ --contract contracts/ERC20_loadtest.sol --contract-name ERC20 \
                      --constructor-args {owner_wallet_address_} --private-key {owner_private_key} --chain-id 270"
    result = subprocess.run(deploy_command, capture_output=True, shell=True, text=True)
    last_line = result.stderr.splitlines()[-1] #zksync-era-cli bug. it returns all stdout into stderr
    contract_address = last_line.split()[-1]
    return contract_address


def encode_address_array(wallets):
    addresses = [wallet["address"] for wallet in wallets]

    array_length = "0x0000000000000000000000000000000000000000000000000000000000000002"
    address1 = "0x00000000000000000000000036615Cf349d7F6344891B1e7CA7C72883F5dc049"
    address2 = "0x000000000000000000000000a61464658AfeAf65CccaaFD3a512b69A83B77618"
    calldata = 0x000000000000000000000000000000000000000000000000000000000000000200000000000000000000000036615Cf349d7F6344891B1e7CA7C72883F5dc049000000000000000000000000a61464658AfeAf65CccaaFD3a512b69A83B77618
