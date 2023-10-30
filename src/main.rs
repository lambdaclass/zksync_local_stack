use std::str::FromStr;
use zksync_web3_rs::providers::{Middleware, Provider};
use zksync_web3_rs::signers::{LocalWallet, Signer};
use zksync_web3_rs::ZKSWallet;
use zksync_web3_rs::zks_provider::ZKSProvider;
use ethers::{types::Address, abi::Abi};
use zksync_web3_rs::zks_wallet::DeployRequest;
use zksync_web3_rs::zks_wallet::CallRequest;

// This is the default url for a local `era-test-node` instance.
static ERA_PROVIDER_URL: &str = "http://localhost:3050";

// This is the private key for one of the rich wallets that come bundled with the era-test-node.
//static PRIVATE_KEY: &str = "0xe667e57a9b8aaa6709e51ff7d093f1c5b73b63f9987e4ab4aa9a5c699e024ee8";
static PRIVATE_KEY: &str = "0x27593fea79697e947890ecbecce7901b0008345e5d7259710d0dd5e500d040be";
// static PRIVATE_KEY: &str = "0x9600ccac13e12ea8b75cbe73221ef6c0f5bc3530c5a1e8d5d5cd596fd6072ff1";


static CONTRACT_BIN: &[u8] = include_bytes!("../build/ERC20.sol:ERC20.zbin");
static CONTRACT_ABI: &str = include_str!("../build/ERC20.abi");

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let zk_wallet = {
        let era_provider = Provider::try_from(ERA_PROVIDER_URL).unwrap();

        let chain_id = era_provider.get_chainid().await.unwrap();
        let l2_wallet = LocalWallet::from_str(PRIVATE_KEY)
            .unwrap()
            .with_chain_id(chain_id.as_u64());
        ZKSWallet::new(l2_wallet, None, Some(era_provider.clone()), None).unwrap()
    };

    // Deploy contract:
    let contract_address = {
        // Read both files from disk:
        let abi = Abi::load(CONTRACT_ABI.as_bytes()).unwrap();
        let contract_bin = CONTRACT_BIN; //hex::decode(CONTRACT_BIN).unwrap().to_vec();

        // DeployRequest sets the parameters for the constructor call and the deployment transaction.
        let request = DeployRequest::with(abi, contract_bin.to_vec(), vec!["0x639dE71cB7C7022594cCe2BBF6873746b117E5CF".to_owned()])
            .from(zk_wallet.l2_address());

        // Send the deployment transaction and wait until we receive the contract address.
        let address = zk_wallet.deploy(&request).await.unwrap();

        println!("Contract address: {:#?}", address);

        address
    };

    // Call the greet view method:
    let era_provider = zk_wallet.get_era_provider().unwrap();
    //let contract_address = "0x8a544924916dcf0f73564750cbc68bbc65fe1e0b".parse::<Address>().unwrap();
    let get_name = CallRequest::new(contract_address, "name()(string)".to_owned());
    let token_name = ZKSProvider::call(era_provider.as_ref(), &get_name)
        .await
        .unwrap();

    println!("token name: {}", token_name[0]);

    let get_balance = CallRequest::new(contract_address, "balanceOf(address)(uint256)".to_owned())
        .function_parameters(vec!["0x639dE71cB7C7022594cCe2BBF6873746b117E5CF".to_owned()]);
    let initial_balance = ZKSProvider::call(era_provider.as_ref(), &get_balance)
        .await
        .unwrap();

    println!("Initial balance: {}", initial_balance[0]);
}
