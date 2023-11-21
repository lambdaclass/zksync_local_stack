import subprocess
import random
from time import sleep

# Deploy ERC20 contract:
# Run this command in root directory, and copy the output addres into erc20_address
# zksync-era-cli --l2-port 3050 deploy --project-root contracts/ --contract contracts/ERC20.sol  --contract-name ERC20 --constructor-args 0xde03a0B5963f75f1C8485B355fF6D30f3093BDE7 --private-key 0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be --chain-id 270

erc20_address = "0x755f0f59c65de6a9afd5267dc7c0546a0c05a23b"
arc20_private_key = "0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be"

rich_wallets = [{"address": "0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be"}]

random_wallets = [{"address": "0xaEcaE5bAcBbE8be2854711243df66c3520751bE0",
                  "private_key": "3b5612631e37c5fbf7d7e6ce78827b02ec273b066010a0208daa8d898d571e82"},
                  {"address": "0xb51473Db0e8e001fA0Ccbd5B80CEc36BEF3d4306",
                  "private_key": "2fbad8907af7a46dacbbe642f368edba3581e492277d5319f5ace26d7d978466"},
                  {"address": "0xcB7946b862dd03dDe7a578BA2B610D03f6EEaE7C",
                  "private_key": "54144e4c98058d93b85e9a0d3e5530a7078e92856cd3746a19ee1f2d5b0bc3c5"},
                  {"address": "0xd49F634edCdF6465EDcE4183AB1663D062B96f4e",
                  "private_key": "9a3ee9566125508eb58f1da91d630c8c7b672f2e15c4321c71f7d073a51f3acc"},
                  {"address": "0xe6f7833Ed0549Dda68E271367285E70eB43e53dB",
                  "private_key": "ad630e498af2b1590d7a6f7e20d64c7da69bd52324b503d4498ca66459710b10"},
                  ]

def main():
    for _ in range(100):
        try:
            subprocess.run(["zksync-era-cli",
                            "--l2-port", "3050", "transfer",
                            "--amount", str(random.randrange(1,200)),
                            "--from", rich_wallets[0]['address'],
                            "--to", random_wallets[random.randrange(0,4)]['address'],
                            "--chain-id", "270"])
            subprocess.run(["zksync-era-cli",
                            "--l2-port", "3050", "send",
                            "--contract", erc20_address,
                            "--function", "transfer(address, uint256)",
                            "--args", random_wallets[random.randrange(0,4)]['address'], str(random.randrange(1,200)),
                            "--output-types", "bool",
                            "--private-key", arc20_private_key,
                            "--chain-id", "270"])
        except subprocess.CalledProcessError as e:
            print(f'Command {e.cmd} failed with error {e.returncode}')


if __name__ == "__main__":
    main()
