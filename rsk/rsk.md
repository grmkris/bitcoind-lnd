mkdir $HOME/Downloads
wget https://github.com/rsksmart/rskj/releases/download/IRIS-3.0.1/rskj-core-3.0.1-IRIS-all.jar -P $HOME/Downloads
`
java -cp $HOME/Downloads/rskj-core-3.0.1-IRIS-all.jar -Drpc.providers.web.cors=0.0.0.0 -Drpc.providers.web.ws.enabled=true -Drpc.providers.web.http.bind_address=0.0.0.0 -Drpc.providers.web.http.hosts={0.0.0.0} co.rsk.Start --regtest
`


rpc.providers.web.http.hosts
 ## More info:
 - https://developers.rsk.co/quick-start/step1-install-rsk-local-node/
 - https://developers.rsk.co/rsk/node/configure/reference/#rpc

 curl http://localhost:4444/ \
    -X POST -H "Content-Type: application/json" \
    --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'


curl http://185.217.125.196:4444/ \
  -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

  curl --insecure --header "Grpc-Metadata-macaroon: 0201046c6f6f700277030a10f735013853cf95b117af83a4d88798c61201301a0c0a04617574681204726561641a0f0a046c6f6f701202696e12036f75741a1a0a0b73756767657374696f6e73120472656164120577726974651a150a04737761701207657865637574651204726561641a0d0a057465726d731204726561640000062084ed6d6be6c1cc29b90a59d1e20ec33bcaee085800739a032e9819fe38b608d2" https://185.217.125.196:8081/v1/loop/swaps