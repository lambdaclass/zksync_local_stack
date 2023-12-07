contract_address = "0x8b33164f217d6d86a6fa40e7270f8cb9403e720a"

erc20_contract_balance_command = "zksync-era-cli --l2-port 3050 call --contract " + contract_address + " --function 'balanceOf(address)' --args '0xde03a0b5963f75f1c8485b355ff6d30f3093bde7' --chain-id 270"

erc20_contract_transfer_command = "zksync-era-cli --l2-port 3050 send \
--contract " + contract_address + " \
--function 'transfer(address, uint256)' \
--args 0xa61464658AfeAf65CccaaFD3a512b69A83B77618 200 \
--output-types bool \
--private-key 0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be \
--chain-id 270"


host = "http://65.21.67.134:3050" #hetzner server

def eth_balance_command(account):
    return f"zksync-era-cli --l2-port 3050 balance --account {account}"


def eth_transfer_command(from_pk, to_address):
    return f"zksync-era-cli --l2-port 3050 transfer --chain-id 270 --amount 1 --from {from_pk} --to {to_address}"