# rsa
This script is a simple representation of the RSA (Rivest-Shamir-Adleman) encryption algorithm

### Functions
#### 1. Generate keys
Generate key pairs:
  + __Public key__ for encrypting message
  + __Private key__ for decrypting message

#### 2. Encrypting message using public key
+ `Input`: 
	+ Public key (___int___) 
	+ Message (___str___)
+ `Output`: Encrypted number string 

#### 3. Decryting cipher string of numbers using private key
+ `Input`: 
	+ Private key (___int___) 
	+ Cipher (___str___)
+ `Output`: Plain text message

#### 4. Create a Digital Signature for a message using the private key
+ `Input`:
	+ Private key (___int___)
	+ Message to sign (___str___)
+ `Output`: A signature to verify the message integrity

#### 5. Verify a message using the signature and public key
+ `Input`:
	+ Public key (___int___)
	+ Digital Signature (___int___)
	+ Message to verified (___str___)
+ `Output`: The message integrity 
