#!/usr/bin/env python3
import random
import math
import hashlib
import base64
import sys

class PrimeGenerate:
    def __init__ (self,start,end):
        """Declare range for the prime number"""
        self.start=start
        self.end=end

    def is_prime(self,num):
        """Test if a number is prime or not"""
        if num == 0 or num == 1:
            return False
        for i in range(2,int(math.sqrt(num)+1)):
            if num % i==0:
                return False
        else:
            return True
    
    def generate(self):
        """Generate prime number within a given range"""
        my_num=random.randint(self.start,self.end)
        #Re-generate the number until it is a prime number
        while not self.is_prime(my_num):
            my_num=random.randint(self.start,self.end)
        return my_num


class DigitalSignature:
    def __init__(self,message,n):
        """Calculate and return an integer representation of the message's sha256 hash digest"""
        self.n=n

        #Get the hash digest of the encoded message
        h_mess=hashlib.sha256()
        h_mess.update(message.encode())
        d_mess=h_mess.digest()

        #Convert the bytes digest to int
        #Since the int is bigger than n -> Calculate the moduler of int % n
        self.i_mess=int.from_bytes(d_mess,"big")%self.n
  
    def sign_mess(self,d):
        """Sign the message using private key"""
        #Use RSA decryption algorithm to sign the message
        sign=self.i_mess**d%self.n

        #Convert the signature to bytes, here I use 4 bytes  
        b_sign=sign.to_bytes(3,"big")
        #Return the signature as 64 bit encoded string
        return base64.b64encode(b_sign).decode() 


    def verify_mess(self,sign,e):
        """Verify the integrity of the message using public key"""
        #Decode the base64 signature
        b64_sign=base64.b64decode(sign)

        #Convert the bytes to integer signature
        i_sign=int.from_bytes(b64_sign,"big")

        #Calculate the expected hash digest from the signature using RSA encryption algorithm
        cal_sign=i_sign**e%self.n
        if cal_sign==self.i_mess:
            return True
        else:
            return False

def lcm(a,b):
    """Calculate least common multiplier as an integer"""
    return a*b//math.gcd(a,b)

def find_e(lambda_n):
    """Find e based on lambda_n"""
    for e in range(2,lambda_n):
        #Return e if the greatest common divisor of e and lambda_n return 1
        if math.gcd(e,lambda_n) == 1:
            return e

def find_d(e,lambda_n):
    """Find d based on lambda_n and e"""
    for d in range(2,lambda_n):
        if d*e%lambda_n == 1:
            return d
    return False

def key_to_base64(n,e_d):
    """Convert the private key or public key to base64 encoded characters"""
    #Convert the integers to bytes
    bytes_n=n.to_bytes(3,"big")
    bytes_e_d=e_d.to_bytes(3,"big")
    
    #Convert the bytes to base64 encoded character string
    base64_n=base64.b64encode(bytes_n).decode()
    base64_e_d=base64.b64encode(bytes_e_d).decode()

    #Choose a random place to append the string
    place=random.randint(0,len(base64_n))
    return base64_n[:place]+"SIsTBdc"+base64_n[place:]+"EM2AhSkBCPxjErL0"+base64_e_d[:place]+"gmYMD5"+base64_e_d[place:]

def base64_to_key(base64_key):
    """Convert the key back to integer to get n and e/d"""
    #Retrieve base64 of n and e/d
    my_base64=base64_key.split("EM2AhSkBCPxjErL0")
    
    #Get base64 encoded of n and e/d
    base64_n=my_base64[0].replace("SIsTBdc","")
    base64_e_d=my_base64[1].replace("gmYMD5","")

    #Retrieve the bytes of n and e/d 
    bytes_n=base64.b64decode(base64_n)
    bytes_e_d=base64.b64decode(base64_e_d)

    #Convert the bytes back to integer
    n=int.from_bytes(bytes_n,"big")
    e_d=int.from_bytes(bytes_e_d,"big")

    return n, e_d


def key_gen():
    """Generate key pairs:
    + Public key: (n, e) for encryption
    + Secret key: (n, d) for decryption"""
    #Generate 2 distinct primes p and q
    #Here I use the range 100 to 1000 just to demonstrate
    prime=PrimeGenerate(100,1000)
    p=prime.generate()
    q=prime.generate()

    #Regenerate p if p==q
    if p==q:
        p=prime.generate()

    #Calculate n = pq
    n=p*q

    #Calculate lambda_n which is the least common multiplier of p-1 and q-1
    lambda_n=lcm(p-1,q-1)

    #Calcualte e and d
    e=find_e(lambda_n)
    d=find_d(e,lambda_n)

    base64_public=key_to_base64(n,e)
    base64_private=key_to_base64(n,d)
    print("Public key: {}".format(base64_public))
    print("Private key: {}".format(base64_private))

def encrypt(message,n,e):
    """Encrypt a message using public key and return a string of encrypted number"""
    cipher=""
    for char in message:
        cipher+= "{} ".format(ord(char)**e%n)

    return cipher.strip()

def decrypt(cipher,n,d):
    """Decrypt a cipher text using the secret key"""
    message=""
    for num in cipher.split(" "):
        message+=(chr(int(num)**d%n))
    return message


def main():
    print("################################################")
    print("##############Welcome to basic RSA##############")
    print("################################################")
    print("1. Generate key pairs")
    print("2. Encrypt a message using the public key")
    print("3. Decrypt a cipher number string using the private key")
    print("4. Sign a message using your private key")
    print("5. Verify a message using your public key")
    error_key="[-] Error! Invalid key format!"
    choice = input("Enter your choice: ")
    if choice == "1":
        key_gen()
    
    elif choice == "2":
        message=input("Enter your message: ")
        public_key=input("Enter your public key: ")
        #Capture error key
        try:
            n,e=base64_to_key(public_key)
        except:
            print(error_key)
            sys.exit(1)
        cipher=encrypt(message,n,e)
        print("[+] Encrypted message: {}".format(cipher))
    
    elif choice == "3":
        cipher=input("Enter your cipher number string: ")
        private_key=input("Enter your private key: ")
        #Capture error key
        try:
            n,d=base64_to_key(private_key)
        except:
            print(error_key)
            sys.exit(1)
        print("[+] Decrypting message...")
        message=decrypt(cipher,n,d)
        print(message)
    
    elif choice == "4":
        message=input("Enter the message you want to sign: ")
        private_key=input("Enter your private key: ")
        #Capture error key
        try:
            n,d=base64_to_key(private_key)
        except:
            print(error_key)
            sys.exit(1)
        digitalSign=DigitalSignature(message,n)
        signature=digitalSign.sign_mess(d)
        print("[+] Your signature: {}".format(signature))

    elif choice == "5":
        message=input("Enter the message you want to verify: ")
        public_key=input("Enter your public key: ")
        sign=input("Enter the Digital Signature you received: ")
        #Capture error key
        try:
            n,e=base64_to_key(public_key)
        except:
            print(error_key)
            sys.exit(1)
        digitalSign=DigitalSignature(message,n)
        verified=digitalSign.verify_mess(sign,e)
        if verified:
            print("[+] Verified successfully!")
        else:
            print("[-] Error! Message has been changed")

    else:
        print("[-] Error! Invalid option!")

if __name__ == "__main__":
    main()

