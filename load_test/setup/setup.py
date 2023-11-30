# we are running setup everytime we run locust.
# on setup, we redistribute our 10 rich wallets eths to have 100 rich wallets
# therefore, there will be a time that rich wallets become poor
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
    return int(pk, base=2)

def get_address_from(private_key):
    cv = Curve.get_curve('secp256k1')
    pu_key = private_key * cv.generator  # just multiplying the private key by generator point (EC multiplication)

    concat_x_y = pu_key.x.to_bytes(32, byteorder='big') + pu_key.y.to_bytes(32, byteorder='big')
    eth_addr = '0x' + keccak_256(concat_x_y).digest()[-20:].hex()

    print('private key: ', hex(private_key))
    print('eth_address: ', eth_addr)
    return eth_addr


def create_wallets_with_money():
    with open("setup/rich-wallets.json") as f:
        original_rich_wallet = json.load(f)  # tengo un json

    # DUDA: Tiene sentido modelar la wallet con su Private key y su address? Por ahora son una lista de dict con keys

    new_wallets = [generate_new_wallet() for _ in range(100)]  # genero 100 private keys y las keccakeo

    total_transfered = 0
    for wallet in original_rich_wallet:
        for _ in range(10):
            from_pk = wallet["privateKey"]
            to = new_wallets[total_transfered]["address"]
            amount = 4536975000000000000
            transfer_with(amount, from_pk, to)
            total_transfered = total_transfered + 1

    return new_wallets
