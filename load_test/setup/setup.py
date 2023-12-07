import json
import random
import subprocess

from ecpy.curves import Curve
from sha3 import keccak_256

random.seed(42)


def transfer_with(amount, from_pk, to_address):
    command = f"zksync-era-cli --l2-port 3050 transfer --chain-id 270 --amount {amount} --from {from_pk} --to {to_address}"
    return subprocess.check_output(command, shell=True, text=True)


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

    print('private key: ', hex(private_key))
    print('eth_address: ', eth_addr)
    return eth_addr


def create_wallets_with_money(with_transfer, quantity):
    with open("setup/rich-wallets.json") as f:
        original_rich_wallet = json.load(f)

    new_wallets = [generate_new_wallet() for _ in range(quantity)]

    total_transferred = 0
    range_to_use = int(quantity / len(original_rich_wallet))
    for wallet in original_rich_wallet:
        for _ in range(range_to_use):
            from_pk = wallet["privateKey"]
            to = new_wallets[total_transferred]["address"]
            amount = 4536975000000000000
            if with_transfer:
                transfer_with(amount, from_pk, to)
            total_transferred = total_transferred + 1

    return new_wallets


def create_wallets_with_money_for_zksync_stack(with_transfer, quantity):
    rich_wallet_private_key = "0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be"
    rich_wallet_address = "0xde03a0b5963f75f1c8485b355ff6d30f3093bde7"

    new_wallets = [generate_new_wallet() for _ in range(quantity)]

    total_transferred = 0
    for _ in range(quantity):
        from_pk = rich_wallet_private_key
        to = new_wallets[total_transferred]["address"]
        amount = int(157426552000000000/100)
        if with_transfer:
            transfer_with(amount, from_pk, to)
        total_transferred = total_transferred + 1

    return new_wallets
