# Load Tests

Load testing the zksync era blockchain.

This setup uses locust to emulate hundreds of users making transactions to each other.
Locust makes http requests to a local flask server that executes zksync-era-cli commands to hit the blockchain.


## Running Loadtests

### Setup
* Install python requirements with

    `pip install -r requirements.txt`


* Run the flask server so that we can execute zksync-era-cli commands as http requests

    `make run`


* Edit the `config.json` file with the correct ip of the chain you want to loadtest and other configs.
* You may run `pipeline_tests.py` to verify the setup.
* The loadtests are in `loadtests.py

### Config file
  The config file has the following:
* _Host_: The ip of the host machine running the l2
* _fund_wallets_: Set to True if you want to fund wallets from scratch when running the tests in a recently initialized testnode
* _amount_of_wallets_: The amount of wallets making transactions.
* _rich_wallet_: the address of a rich wallet to transfer funds from.
  

