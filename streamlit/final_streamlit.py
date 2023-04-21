# Import Libraries
from secrets import choice
import json
from web3 import Web3
from dotenv import load_dotenv
import base64
from pinata import pin_file_to_ipfs, convert_data_to_json, pin_json_to_ipfs
import io
import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_image_comparison import image_comparison
import streamlit.components.v1 as components
import os


load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set Page Configuration
st.set_page_config(layout="centered", initial_sidebar_state='collapsed')

# Header and Title Screen
image = Image.open('../Orlando_Desktop/Images/LOGO.PNG')
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st.image('../Orlando_Desktop/Images/LOGO.PNG')

with col3:
    st.write("")

# Setup for visualisations        
image_comparison(
img1="../Orlando_Desktop/Images/shoes.png",
img2="../Orlando_Desktop/Images/wallet.png",
label1="real vogue",
label2="digital assets"
)

st.markdown(
    """
    <h2 style='text-align: center'>
    ALL THE BEST BRANDS, ON THE BLOCKCHAIN
    </h2>
    """,
    unsafe_allow_html=True,
)



# Load the contract
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('../contracts/compiled/final_certificate.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = Web3.toChecksumAddress(os.getenv("SMART_CONTRACT_ADDRESS"))


    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# Account connection in UI
account_opt_dict = {
    "Gucci" : "0x576e2eE34Ad4E1A9842446f7ca12e7CFA47B6d7D",
    "Prada": "0xA3D3A0c7D7Ed93Bbd087bBB69577857aC52ca8Ec",
    "Harrod" : " 0xD9E0727CBD11023837d3d812Fc42E0154dC9FDa6 ",
    "DandG" : "0x0e67bed69550a19589E481e0AF911b9939405136",
    "Gucci" : "0x576e2eE34Ad4E1A9842446f7ca12e7CFA47B6d7D",
    "WatchSwiss" : " 0x7fa3d65D65ec94BED3eaEEf0019c9b84E0e63d9A "
    
}

if 'brand' not in st.session_state:
    st.session_state.brand = ''

st.markdown("# Choose an account to get started:")
accounts = account_opt_dict.keys()
# st.write(accounts)
choice = st.selectbox("Select Brand:", options=accounts)

vendor = account_opt_dict[choice]
brand = choice  

# Frontpage UI text

st.write(choice, "uses this wallet to pay into")
st.write(vendor)
selection = ()
img_list = []
buyer = "0x3129C700695F3408dE351dBD96d3B995909dF298"

st.write("### Exclusive selections from the ",brand, "designer range" )


url = "https://gateway.pinata.cloud/ipfs/"

# Image library
items = {
"Prada" : 
    ["../Orlando_Desktop/Images/Prada Images/Bag_Beige.png",
    "../Orlando_Desktop/Images/Prada Images/Bag_Blue.png",
    "../Orlando_Desktop/Images/Prada Images/Bag_Grey.png",
    "../Orlando_Desktop/Images/Prada Images/Glasses_Dark_Rad.png",
    "../Orlando_Desktop/Images/Prada Images/Shoe_Chelsea.png",
    "../Orlando_Desktop/Images/Prada Images/Shoe_Rad_Black.png",
    "../Orlando_Desktop/Images/Prada Images/Shoe_Shiny_Choo.png"],
"Website_Images" :
    ["../Orlando_Desktop/Images/Website_Images/Bag_Leather.png",
    "../Orlando_Desktop/Images/DWebsite_Images/Bag_Maroon.png",
    "../Orlando_Desktop/Images/Website_Images/Bag_White.png",
    "../Orlando_Desktop/Images/Website_Images/Glasses_Black_Gold.png",
    "../Orlando_Desktop/Images/Website_Images/Glasses_DG_Chain.png",
    "../Orlando_Desktop/Images/Website_Images/Glasses_Pink.png",
    "../Orlando_Desktop/Images/Website_Images/Shoe_Sneakers.png"],
"Harrods" :
    ["../Orlando_Desktop/Images/Harrod_Images/Glasses_Black_Ray.png",
    "../Orlando_Desktop/Images/Harrod_Images/Jacket_Biker.png",
    "../Orlando_Desktop/Images/Harrod_Images/Jacket_Blazer.png",
    "../Orlando_Desktop/Images/Harrod_Images/Jacket_Bomber.png",
    "../Orlando_Desktop/Images/Harrod_Images/Jacket_Cafe_Racer.png",
    "../Orlando_Desktop/Images/Harrod_Images/Jacket_Field.png"],
"Gucci" :
    ["../Orlando_Desktop/Images/Gucci_Images/Bag_Azure.png",
    "../Orlando_Desktop/Images/Gucci_Images/Bag_Pink.png",
    "../Orlando_Desktop/Images/Gucci_Images/Glasses_Pearl_Chain.png",
    "../Orlando_Desktop/Images/Gucci_Images/Glasses_Rose_Chain.png",
    "../Orlando_Desktop/Images/Gucci_Images/Shoe_CL_Red.png",
    "../Orlando_Desktop/Images/Gucci_Images/Shoe_Gucci_Sneaker.png",
    "../Orlando_Desktop/Images/Gucci_Images/Shoe_Hightop.png"],
"WatchSwiss" :
    ["../Orlando_Desktop/Images/WatchSwiss/Watches_Omega.png",
    "../Orlando_Desktop/Images/WatchSwiss/Watches_Patek_Philippe.png",
    "../Orlando_Desktop/Images/WatchSwiss/Watches_Rolex.png",
    "../Orlando_Desktop/Images/WatchSwiss/Watches_Tagheuer.png",
    "../Orlando_Desktop/Images/WatchSwiss/Watches_Vacheron_Constantin.png"]   
}
#address = w3.eth.accounts[0]
buyer = Web3.toChecksumAddress('0x3129C700695F3408dE351dBD96d3B995909dF298')
#Loop for display, transactions and NFT generation
for i in items[choice]:
    st.image(i)
    if st.button(label="Buy now", key = {i}):
        with open(i, mode='rb') as image_file:
            image = image_file.read()
        # i = Image.open(i)
        ipfs_hash = pin_file_to_ipfs(image)
        image_uri = f"ipfs://{ipfs_hash}"
        token_json = {
            "name": choice,
            "image": image_uri
        }
        json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)
        item_uri = f"ipfs://{json_ipfs_hash}"
#for transacting with Web3 accounts
        tx = contract.functions.awardCertificate(
        buyer,
        item_uri
        ).buildTransaction({'from': buyer, 'gas': 1000000, 'nonce': w3.eth.get_transaction_count(buyer)})
        signed_txn = w3.eth.account.signTransaction(tx, os.getenv("ACCOUNT_PRIV_KEY"))
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction Complete. Your product is being despatched:") 
        st.write(' <---- see  NFT Receipt Details')
        st.sidebar.write('## NFT and Transaction receipt mined')
        st.sidebar.write(dict(receipt))
        #st.sidebar.write(item_uri)
        st.sidebar.image(i)
        
    st.markdown("---")






