from algosdk.v2client import algod, indexer
from algosdk import mnemonic, transaction
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

##### GLOBAL CONSTANTS ##########
ALGOD_ENDPOINT = os.getenv("ALGOD_ENDPOINT")
INDEXER_ENPOINT = os.getenv("INDEXER_ENPOINT")
API_KEY = os.getenv("API_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
MNEMONIC = os.getenv("MNEMONIC")
TOKEN = os.getenv("TOKEN")
HEADERS = {
    "X-Algo-API-Token": API_KEY,
}
PUBLIC_ADDRESS_2 = os.getenv("PUBLIC_ADDRESS_2")
MNEMONIC_2 = os.getenv("MNEMONIC_2")
#################################

# Initialize the indexer client
indexer_client = indexer.IndexerClient(TOKEN, INDEXER_ENPOINT, HEADERS)

def create_token(asset_name, unit_name, total, decimals):
    """
    Create a new token (asset) on the Algorand blockchain.
    """
    total = total * (10 ** decimals)

    # Initialize the algod client
    algod_client = algod.AlgodClient(TOKEN, ALGOD_ENDPOINT, HEADERS)
    
    # Create the asset creation transaction
    nft_mint = transaction.AssetCreateTxn(PUBLIC_ADDRESS, algod_client.suggested_params(), total, decimals, False, unit_name=unit_name, asset_name=asset_name)
    
    # Sign the transaction
    signed_nft_mint = nft_mint.sign(mnemonic.to_private_key(MNEMONIC))
    
    # Send the transaction
    tx_id = algod_client.send_transaction(signed_nft_mint)
    
    # Wait for confirmation
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)

    created_asset = results["asset-index"]

    print("Created Asset With id : {}".format(str(created_asset)))

    return created_asset

def optin_token(asset_id):
    """
    Opt-in to receive a specific asset.
    """
    # Initialize the algod client
    algod_client = algod.AlgodClient(TOKEN, ALGOD_ENDPOINT, HEADERS)
    
    # Create the opt-in transaction
    opt_in = transaction.AssetOptInTxn(PUBLIC_ADDRESS_2, algod_client.suggested_params(), asset_id)
    
    # Sign the transaction
    signed_opt_in = opt_in.sign(mnemonic.to_private_key(MNEMONIC_2))
    
    # Send the transaction
    tx_id = algod_client.send_transaction(signed_opt_in)
    
    # Wait for confirmation
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Opt IN Completed\n Transaction id {} confirmed in {}".format(tx_id, results['confirmed-round']))

def send_token(asset_id, amt):
    """
    Send a specific amount of the asset to another address.
    """
    # Get asset information
    asset_info = indexer_client.asset_info(asset_id)
    decimals = asset_info['asset']['params']['decimals']
    amt = amt * (10 ** decimals)
    
    # Initialize the algod client
    algod_client = algod.AlgodClient(TOKEN, ALGOD_ENDPOINT, HEADERS)
    
    # Create the asset transfer transaction
    send_txn = transaction.AssetTransferTxn(PUBLIC_ADDRESS, algod_client.suggested_params(), PUBLIC_ADDRESS_2, amt, asset_id)
    
    # Sign the transaction
    signed_send_txn = send_txn.sign(mnemonic.to_private_key(MNEMONIC))
    
    # Send the transaction
    tx_id = algod_client.send_transaction(signed_send_txn)
    
    # Wait for confirmation
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Transfer Completed\n Transaction id {} confirmed in {}".format(tx_id, results['confirmed-round']))

# Create a new token, opt-in to receive it, and send some amount of it
asset_id = create_token("RUPEE", "RBI", 1000, 2)
optin_token(asset_id)
send_token(asset_id, 2)
