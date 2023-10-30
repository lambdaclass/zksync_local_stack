# zkSync full stack deployment walkthrough
This tutorial will cover how to start a zksync node, compile and deploy a contract and, finally, see it in the explorer.
This was tested on mac and linux (ubuntu), and the instructions ahead should work for both platforms.

## Dependencies
- solidity 0.8.19
    - https://github.com/ethereum/solidity/releases/tag/v0.8.19
    - scroll down to the assets section
    - download the binary matching your platform or build from source. This tutorial assumes the former.
    - `chmod a+x solc-(macos | linux)`
    - on macos: `xattr -d com.apple.quarantine solc-(macos | linux)`
- node >= 18.18.0
- npm >= 9.0.0
- yarn 1.22.19
- axel
- docker
- clang
    - linux: build-essential pkg-config cmake clang lldb lld
    - macos: Xcode
- openSSL
    - linux: libssl-dev
- postgres
    - linux: postgresql
- rust
    - recommended: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
    - `cargo install sqlx-cli`
- python
- tmux (optional)

## Installation
Now, to install the zksync node, compiler and explorer:
### zksync-era (geth and zksync nodes)
- clone the repo https://github.com/matter-labs/zksync-era
- export the ZKSYNC_HOME environmental variable on your `.zshrc` or `.bashrc` file
    - `export ZKSYNC_HOME=/path/to/repo`
    - `export PATH="$ZKSYNC_HOME:$PATH"`
- zk (enabled after the previous step)
- zk init
- zk up
- zk server (locks the terminal, tmux recommended)

### zksync explorer
- clone the repo https://github.com/matter-labs/block-explorer
- cd into block-explorer
- npm install
- npm run hyperchain:configure
- npm run db:create
- npm run dev (tmux recommended)

### zksolc compiler
After cloning the repo https://github.com/matter-labs/zksolc-bin.git and going into it's directory `cd zksloc-bin`, you will find a few folders for different operative systems and CPU architectures. Choose the one that matches your system, inside of it you will find multiple versions of the `zksolc` compiler. For convenience, you should copy the latest one into a more accessible path and change the name to something like `zksolc`.

## Setup
Create a new cargo project `cargo init zksync_full_stack`
Edit the `Cargo.toml` file to add `zksync-web3-rs` and `tokio` as dependencies
```toml
[dependencies]
zksync-web3-rs = "0.1.1"
tokio = { version = "1", features = ["macros", "process"] }
``` 

Create your contract(s). For this example we'll be using an `ERC20` implementation in solidity.

Generate the abi for the contract 
Compile contract `./zksolc --solc ./<path_to_solc> <path_to_contract> --bin -o <build_directory>`

Now we need to interact with the contract. We can refer to https://era.zksync.io/docs/api/rust/contract-deployment-and-interaction.html and pretty much copy and paste the code there, modifying a few names to match your contract. Also, you will need to have enough gas to deploy it.
