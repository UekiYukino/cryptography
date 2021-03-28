#!/usr/bin/env python3
import random
import math
import hashlib

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
        return self.i_mess**d%self.n

    def verify_mess(self,sign,e):
        """Verify the integrity of the message using public key"""
        #Calculate the expected hash digest from the signature using RSA encryption algorithm
        cal_sign=sign**e%self.n
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
    
    print("Public key: n={}, e={}".format(n,e))
    print("Private key: d={}".format(d))

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
    choice = input("Enter your choice: ")
    if choice == "1":
        key_gen()
    
    elif choice == "2":
        message=input("Enter your message: ")
        n=int(input("Enter your n: "))
        e=int(input("Enter your public e key: "))
        cipher=encrypt(message,n,e)
        print("[+] Encrypted message: {}".format(cipher))
    
    elif choice == "3":
        cipher=input("Enter your cipher number string: ")
        n=int(input("Enter your n: "))
        d=int(input("Enter your private key d: "))
        print("[+] Decrypting message...")
        message=decrypt(cipher,n,d)
        print(message)
    
    elif choice == "4":
        message=input("Enter the message you want to sign: ")
        n=int(input("Enter your n: "))
        d=int(input("Enter your private key d: "))
        digitalSign=DigitalSignature(message,n)
        signature=digitalSign.sign_mess(d)
        print("[+] Your signature: {}".format(signature))

    elif choice == "5":
        message=input("Enter the message you want to verify: ")
        n=int(input("Enter your n: "))
        e=int(input("Enter your public key e: "))
        sign=int(input("Enter the Digital Signature you received: "))
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

