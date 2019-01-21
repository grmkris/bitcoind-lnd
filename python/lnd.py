import codecs
import logging
import os

import grpc

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s', )
logger = logging.getLogger('main')

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
# os.environ["GRPC_SSL_CIPHER_SUITES"] = 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256'


LND_DOCKER = {
    'name': 'LND',
    'rpc_port': 10009,
    'tls_cert': '/Users/cherijs/.docker_volumes/.lnd/tls.cert',
    'admin_macaroon': '/Users/cherijs/.docker_volumes/.lnd/data/chain/bitcoin/regtest/admin.macaroon'
}

ALICE_DOCKER = {
    'name': 'Alice',
    'rpc_port': 10010,
    'tls_cert': '/Users/cherijs/.docker_volumes/simnet/alice/tls.cert',
    'admin_macaroon': '/Users/cherijs/.docker_volumes/simnet/alice/data/chain/bitcoin/regtest/admin.macaroon'
}

BOB_DOCKER = {
    'name': 'Bob',
    'rpc_port': 10011,
    'tls_cert': '/Users/cherijs/.docker_volumes/simnet/bob/tls.cert',
    'admin_macaroon': '/Users/cherijs/.docker_volumes/simnet/bob/data/chain/bitcoin/regtest/admin.macaroon'
}


class LndRpc(object):

    def __init__(self, config):
        cred = grpc.ssl_channel_credentials(open(config['tls_cert'], 'rb').read())
        auth_credentials = grpc.metadata_call_credentials(self.metadata_callback)
        combined_credentials = grpc.composite_channel_credentials(cred, auth_credentials)
        channel = grpc.secure_channel(f'localhost:{config["rpc_port"]}', combined_credentials)
        logger.info(f'CONNECTING TO {config["name"]}:  localhost:{config["rpc_port"]}')
        self.macaroon = codecs.encode(open(config['admin_macaroon'], 'rb').read(), 'hex')
        self.stub = lnrpc.LightningStub(channel)

    def metadata_callback(self, context, callback):
        callback([('macaroon', self.macaroon)], None)


class LndNode(object):
    def __repr__(self):
        return self.displayName

    def __init__(self, config):
        self.displayName = config['name']
        self.rpc = LndRpc(config)

    def ping(self):
        try:
            self.rpc.stub.GetInfo(ln.GetInfoRequest())
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def peers(self):
        try:
            peers = self.rpc.stub.ListPeers(ln.ListPeersRequest()).peers
            return [p.pub_key for p in peers]
        except Exception as e:
            logger.exception(e)

    def wallet_balance(self):
        try:
            response = self.rpc.stub.WalletBalance(ln.WalletBalanceRequest())
            return {
                'node': self.displayName,
                'total_balance': response.total_balance,
                'confirmed_balance': response.confirmed_balance,
                'unconfirmed_balance': response.unconfirmed_balance,
            }
        except Exception as e:
            logger.exception(e)

    def invoice_subscription(self):
        try:
            response = self.rpc.stub.SubscribeInvoices(ln.InvoiceSubscription())
            for invoice in response:
                logger.info(invoice)
            return response
        except Exception as e:
            logger.exception(e)

    def list_channels(self):
        try:
            response = self.rpc.stub.ListChannels(ln.ListChannelsRequest())
            return response
        except Exception as e:
            logger.exception(e)

    def add_invoice(self, memo='Pay me', ammount=0, expiry=3600):
        try:
            invoice_req = ln.Invoice(memo=memo, value=ammount, expiry=expiry)
            response = self.rpc.stub.AddInvoice(invoice_req)
            return response
        except Exception as e:
            logger.exception(e)

    def list_invoices(self):
        try:
            response = self.rpc.stub.ListInvoices(ln.ListInvoiceRequest())
            return response
        except Exception as e:
            logger.exception(e)

    def decode_pay_request(self, pay_req):
        try:
            pay_req = pay_req.rstrip()
            raw_invoice = ln.PayReqString(pay_req=str(pay_req))
            response = self.rpc.stub.DecodePayReq(raw_invoice)
            return response
        except Exception as e:
            logger.exception(e)

    def send_payment(self, pay_req):
        invoice_details = self.decode_pay_request(pay_req)
        try:
            request = ln.SendRequest(
                dest_string=invoice_details.destination,
                amt=invoice_details.num_satoshis,
                payment_hash_string=invoice_details.payment_hash,
                final_cltv_delta=144  # final_cltv_delta=144 is default for lnd
            );
            response = self.rpc.stub.SendPaymentSync(request)
            logger.warning(response)
        except Exception as e:
            logger.exception(e)

    def invoice_subscription(self, add_index):
        try:
            request = ln.InvoiceSubscription(
                add_index=add_index,
                # settle_index= 3,
            )
            for response in self.rpc.stub.SubscribeInvoices(request):
                print(response)
                logger.warning(response)

        except Exception as e:
            logger.exception(e)


alice_node = LndNode(ALICE_DOCKER)
bob_node = LndNode(BOB_DOCKER)

logger.debug(alice_node.wallet_balance())
logger.debug(bob_node.wallet_balance())

# logger.debug(alice_node.list_channels())

# logger.debug(node.list_invoices())
# logger.debug(node.add_invoice(ammount=100))
# logger.debug(node.invoice_subscription(3))
# logger.debug(node.decode_pay_request(
#     'lntb1u1pwyzfh2pp5aw6te06r3lrtm8fddy0yptvm70l0z8vs2cjvkzgnph0lhe4lqnzsdqqcqzysxqyz5vq39h3nw9lenhr5ly8mmtjc4faqyq46pycfv4tekxey25cm2z0ehlhxc03lurwwpfh6pyu9a7pukgudp3dnxjeyn309493lqeyksy6sqsq0lyskc'))
#
# logger.debug(node.send_payment(
#     'lntb1u1pwyzfh2pp5aw6te06r3lrtm8fddy0yptvm70l0z8vs2cjvkzgnph0lhe4lqnzsdqqcqzysxqyz5vq39h3nw9lenhr5ly8mmtjc4faqyq46pycfv4tekxey25cm2z0ehlhxc03lurwwpfh6pyu9a7pukgudp3dnxjeyn309493lqeyksy6sqsq0lyskc'))
#
