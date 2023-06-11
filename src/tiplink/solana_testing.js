import {
    Connection,
    Keypair,
    PublicKey,
    SystemProgram,
    LAMPORTS_PER_SOL,
    Transaction,
    sendAndConfirmTransaction,
  } from "@solana/web3.js";

//   Function to create a keypair from a secret key
    const secretKey = bs58.decode("4KWWN59DQXGkG3zNvHPagaunkGUK7WAqjqK3DweTjtBrLuz9FoZsQ3W22uKzKQXw6cnwvWfWhtk1vPq1o15Cw1eY");
    const keypair = Keypair.fromSecretKey(secretKey);

    // Key pair to send to is this: 9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc
    const publicKey = new PublicKey("9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc");


  (async () => {
    const fromKeypair = keypair
    const toKeypair = publicKey;
  
    const connection = new Connection(
      "https://api.mainnet.solana.com",
      "confirmed"
    );
  
    const airdropSignature = await connection.requestAirdrop(
      fromKeypair.publicKey,
      LAMPORTS_PER_SOL
    );
  
    await connection.confirmTransaction(airdropSignature);
  
    const lamportsToSend = 1_000_000;
  
    const transferTransaction = new Transaction().add(
      SystemProgram.transfer({
        fromPubkey: fromKeypair.publicKey,
        toPubkey: toKeypair,
        lamports: lamportsToSend,
      })
    );
  
    await sendAndConfirmTransaction(connection, transferTransaction, [
      fromKeypair,
    ]);
  })();
  