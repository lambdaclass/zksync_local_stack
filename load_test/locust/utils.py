def eth_balance_command(host, account):
    return f"zksync-era-cli --host {host} --l2-port 3050 balance --account {account}"


def eth_transfer_command(host, from_pk, to_address, amount):
    return f"zksync-era-cli --host {host} --l2-port 3050 transfer --chain-id 270 --amount {amount} --from {from_pk} --to {to_address}"


def erc20_contract_balance_command(host, account, contract_address):
    return f"zksync-era-cli --host {host} --l2-port 3050 call --contract {contract_address} --function 'balanceOf(address)' --args {account} --chain-id 270"


def erc20_transfer_command(host, from_pk, to_address, amount, contract_address):
    return f"zksync-era-cli --host {host} --l2-port 3050 send --contract {contract_address} --function 'transfer(address, uint256)' --args {to_address} {amount} --private-key {from_pk} --chain-id 270"