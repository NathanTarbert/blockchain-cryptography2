from flask import Flask, jsonify, request
from web3.auto import w3
from eth_account.messages import encode_defunct
import bitcoin, hashlib, binascii, base58
from bitcoin import *
import eth_keys, binascii
import json

app =Flask(__name__)
@app.route('/crypto2/eth_sign', methods=["POST"])
def eth_sign():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["skey", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400
    
    #private-key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a' this is the private key input but we get it dynamically
    #msg = 'exercise-cryptography'  This is our input but we get it dynamically
    
    privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(values["skey"])) #this will grab our private key from the input field   
    msg = values["msg"]
    signature = privKey.sign_msg(msg.encode('utf-8')) #this will encode the signature and match with ASCII
	
    response = {"skey": hex(signature),"msg": msg} #this will be our output. Same as res.send in JS

    return json.dumps(response), 201

@app.route('/crypto2/eth_sign_to_addr', methods=["POST"])
def eth_sign_to_addr():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["signature", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    msg = values['msg'].encode('utf-8') #utf-8 will encode the message according to ASCII
    #msgSigner = '0xa44f70834a711F0DF388ab016465f2eEb255dEd0' #this will be our output
    signature = eth_keys.keys.Signature(binascii.unhexlify(values['signature'][2:]))  #the [2:]will slice off the first 2 characters, the (0x).
    signerPubKey = signature.recover_public_key_from_msg(msg)   
    signerAddress = signerPubKey.to_checksum_address()
    # print('Signer public key (recovered):', signerPubKey)
    # print('Signer address:', signerAddress)
    # print('Signature valid?:', signerAddress == msgSigner)
    
    response = {"address": (signerAddress)}
    
    return json.dumps(response), 201

@app.route('/crypto2/eth_sign_verify', methods=["POST"])
def eth_sign_verify():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["address", "signature", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    msg = values['msg'].encode('utf-8')
    msgSigner = values['address']
    #signature1 = '0xacd0acd4eabd1bec05393b33b4018fa38b69eba8f16ac3d60eec9f4d2abc127e3c92939e680b91b094242af80fce6f217a34197a69d35edaf616cb0c3da4265b01' #this is our signature input
    signature = eth_keys.keys.Signature(binascii.unhexlify(values['signature'][2:]))
    signerPubKey = signature.recover_public_key_from_msg(msg)
    signerAddress = signerPubKey.to_checksum_address()

    response = {"valid": signerAddress == msgSigner}

    return json.dumps(response), 201

@app.route('/crypto2/btc_skey_to_addr', methods=["POST"])
def btc_skey_to_addr():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["skey"]
    if not all(k in values for k in required):
        return "Missing values", 400

    private_key = values["skey"]
    public_key = privtopub(private_key)    
    address = pubtoaddr(public_key)
	
    response = {"address": (address)}
	
    return json.dumps(response), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

