'use strict';
const express = require('express');
const bodyParser = require('body-parser');
const EthCrypto = require('eth-crypto');
const bitcoinjs = require('bitcoinjs-lib');
var http_port = 5000;

function containsAll(body, requiredKeys) {
    return requiredKeys.every(elem => body.indexOf(elem) > -1) &&
           body.length == requiredKeys.length;
}

var initHttpServer = () => {
    var app = express();
    app.use(bodyParser.json());

    app.post('/crypto2/eth_sign', (req, res) => {
        var values = req.body;
        if (Object.keys(values).length === 0) {
            return res.status(400).send('Missing Body');
        }

        var required = [{
            "skey": "97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a",
            "msg": "exercise-cryptography"
        }];
        
        if (!containsAll(Object.keys(values), required)) {
            return res.status(400).send('Missing values');
        }
		
        const identity = EthCrypto.createIdentity();
        /* >{
            address: '0x3f243FdacE01Cfd9719f7359c94BA11361f32471',
            privateKey: '0x107be946709e41b7895eea9f2dacf998a0a9124acbb786f0fd1a826101581a07',
            publicKey: 'bf1cc3154424dc22191941d9f4f50b063a2b663a2337e5548abea633c1d06ece...'
            } */        

        res.send({ signature: `${identity}`, msg: `exercise cryptography`});
    });

    app.post('/crypto2/eth_sign_to_addr', (req, res) => {
        var values = req.body;
        if (Object.keys(values).length === 0) {
            return res.status(400).send('Missing Body');
        }

        var required = ["signature", "msg"];
        if (!containsAll(Object.keys(values), required)) {
            return res.status(400).send('Missing values');
        }

		// TODO: Not Implemented Yet

        res.send({address: "TODO"});
    });

    app.post('/crypto2/eth_sign_verify', (req, res) => {
        var values = req.body;
        if (Object.keys(values).length === 0) {
            return res.status(400).send('Missing Body');
        }

        var required = ["address", "msg", "signature"];
        if (!containsAll(Object.keys(values), required)) {
            return res.status(400).send('Missing values');
        }

        // TODO: Not Implemented Yet

        res.send({valid: "TODO"});
    });

    app.post('/crypto2/btc_skey_to_addr', (req, res) => {
        var values = req.body;
        if (Object.keys(values).length === 0) {
            return res.status(400).send('Missing Body');
        }

        var required = ["skey"];
        if (!containsAll(Object.keys(values), required)) {
            return res.status(400).send('Missing values');
        }

        // TODO: Not Implemented Yet

        res.send({address: "TODO"});
    });

    app.listen(http_port, () => console.log(`Listening http port: ${http_port}`));
};

initHttpServer();
