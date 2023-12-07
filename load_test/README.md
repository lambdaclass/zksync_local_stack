# Load Tests

Load testing the zksync era blockchain.

This setup uses locust to emulate hundreds of users making transactions to each other.
Locust makes http requests to a local flask server that executes zksync-era-cli commands to hit the blockchain.



Execute 
