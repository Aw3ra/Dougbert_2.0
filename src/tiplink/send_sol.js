const { Connection, 
        Keypair, 
        PublicKey, 
        SystemProgram, 
        LAMPORTS_PER_SOL, 
        Transaction, 
        sendAndConfirmTransaction 
    } 
    = require("@solana/web3.js");

    
const bs58 = require("bs58");
  
  async function sendLamports(fromSecretKeyStr, toPublicKeyStr, lamportsToSend) {
    // Convert the base58 secret key string to a byte array
    const secretKey = bs58.decode(fromSecretKeyStr);
    
    // Create a keypair from the secret key
    const fromKeypair = Keypair.fromSecretKey(secretKey);
    
    // Create a PublicKey from the base58 public key string
    const toPublicKey = new PublicKey(toPublicKeyStr);
    
    // Create a connection to the Solana mainnet
    const connection = new Connection("https://api.mainnet-beta.solana.com", "confirmed");
    
    // Create a transfer transaction
    const transferTransaction = new Transaction().add(
      SystemProgram.transfer({
        fromPubkey: fromKeypair.publicKey,
        toPubkey: toPublicKey,
        lamports: lamportsToSend,
      })
    );
    
    // Send and confirm the transfer transaction
    await sendAndConfirmTransaction(connection, transferTransaction, [fromKeypair]);
  }
  
  module.exports = { sendLamports };
  