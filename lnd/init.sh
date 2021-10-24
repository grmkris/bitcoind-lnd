#!/bin/sh


#mkdir ~/loop
#cd ~/loop
#wget https://github.com/lightninglabs/loop/releases/download/v0.15.0-beta/loop-linux-amd64-v0.15.0-beta.tar.gz
#tar -xf loop-linux-amd64-v0.15.0-beta.tar.gz
#cd loop-linux-amd64-v0.15.0-beta
#

./loopd --network=testnet --lnd.macaroonpath=/var/lib/docker/volumes/bitcoind-lnd_bitcoin/_data/data/chain/bitcoin/testnet/admin.macaroon  --lnd.tlspath=/var/lib/docker/volumes/bitcoind-lnd_bitcoin/_data/tls.cert


/var/lib/docker/volumes/bitcoind-lnd_bitcoin/_data/data/chain/bitcoin/testnet/