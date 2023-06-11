from javascript import require
import os
import dotenv
from random import randint

dotenv.load_dotenv()

link = require('./createLink.js')
transfer = require('./send_sol.js')
transfer_token = require('./send_token.js')

def generate_tip():
    tip_link = link.createLink()
    new_link = tip_link.url.href
    pub_key = tip_link.keypair.publicKey.toBase58()
    return new_link, pub_key

def send_tip(pub_key, amount):
    # Fromsecretkey, publicKey, amount
    transfer.sendTokens(os.getenv("SOLANA_PRIVATE_KEY"), pub_key, amount)

def send_token_tip(pub_key, amount):
    token_acc = "AKeAUzd8rLiayS3oSCMh5mkraGDQbfk6ZTrxP2ZoZ6dG"
    transfer_token.send_token(os.getenv("SOLANA_PRIVATE_KEY"), pub_key, amount, token_acc)


def send_tip_link():
    amount = randint(1, 100)
    tiplink_stuff = generate_tip()
    send_token_tip(tiplink_stuff[1], amount)
    return tiplink_stuff[0]


if __name__ == '__main__':
    print(send_tip_link())
    