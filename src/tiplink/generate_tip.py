from javascript import require

link = require('./createLink.js')

def generate_tip():
    tip_link = link.createLink()
    new_link = tip_link.url.href
    pub_key = tip_link.keypair.publicKey.toBase58()
    return new_link, pub_key


generate_tip()