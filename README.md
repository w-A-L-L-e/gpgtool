# gpgtool
Gnupg python script to make managing keys, encrypting and decrypting files with GPG easier
Just run python gpgtool.py after installing gnupg and it saves a lot of time/hastle to encrypt and decrypt files.
I spent less than an hour making this with the help of chat gpt. 

It was more an exercise for myself if I could use
AI more for creating little side projects. And it does indeed save time for this type of thing. However there we're some bugs
that it could not solve on its own and it just started spawning new versions with different errors over and over so a little
manual work was still required. However it is indeed scary to see how far we've come already

## Examples
Share a public key with a person:

```
$ python gpgtool.py

Menu:
=====

1. List GPG keys
2. Create a new GPG key
3. Show the public key block for a GPG key
4. Delete a GPG key
5. Encrypt a file
6. Decrypt a file
q. Exit
Enter your choice (0-6): 3

Available GPG keys:
1. Key ID: 707DC79E85353D7D
   Name: Walter Schreppers
   Email: schreppers@gmail.com
   Comment: Manier om encrypted files te sharen met Meemoo

2. Key ID: A52CAB489EF8B1D3
   Name: Kubernetes <walter@sitweb.eu> Used for files on openshift
   Email: walter@sitweb.eu> Used for files on openshift
   Comment: Kubernetes

Enter the index number of the key to show the public key: 2
Public Key Block:

-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEZFyXkxYJKwYBBAHaRw8BAQdA+Qzx8MkKzpH7B0RCIa19JK+dTTcB7/WRGixn
lU4aThS0OUt1YmVybmV0ZXMgPHdhbHRlckBzaXR3ZWIuZXU+IFVzZWQgZm9yIGZp
bGVzIG9uIG9wZW5zaGlmdIiZBBMWCgBBFiEEwL+6H40ZNHKcW47hpSyrSJ74sdMF
AmRcl5MCGwMFCQPCZwAFCwkIBwICIgIGFQoJCAsCBBYCAwECHgcCF4AACgkQpSyr
QORsjVzanBWBDV3+nLXxzEPFNJOzB8+b3IAlFvP9/BInAwEIB4h4BBgWCgAgFiEE
wL+6H40ZNHKcW47hpSyrSJ74sdMFAmRcl5MCGwwACgkQpSyrSJ74sdOrCQD9HCGG
BU0xvKX1wBrQ20/e+IcjY2HR9rrEXZ3YLGyStzABAPzbpeSGW2gd56x/Cdm0Zlx3
f/ixRWHwCNKasZEBjSsF
=Xhcj
-----END PGP PUBLIC KEY BLOCK-----
```

So we just need to enter the index here. Not copy/paste the correct id from our keylist.

To decrypt a file it's also pretty straightforward. A little curses file selection menu was also added here :
```
$ python gpgtool.py

Menu:
=====

1. List GPG keys
2. Create a new GPG key
3. Show the public key block for a GPG key
4. Delete a GPG key
5. Encrypt a file
6. Decrypt a file
q. Exit
Enter your choice (0-6): 5

Available GPG keys:
1. Key ID: 707DC79E85353D7D
   Name: Walter Schreppers
   Email: schreppers@gmail.com
   Comment: Manier om encrypted files te sharen met Meemoo

2. Key ID: A52CAB489EF8B1D3
   Name: Kubernetes <walter@sitweb.eu> Used for files on openshift
   Email: walter@sitweb.eu> Used for files on openshift
   Comment: Kubernetes


Enter the index number of the key to use for encryption: 2

Select a file to encrypt:
/Users/wschrep/pythonWork/gpgtool
 > helloworld.txt <
   Makefile
   README.md
   gpgtool.py
   .git   

Enter the path to save the encrypted file: hello_encrypted.gpg
File encrypted successfully.
```

By no means is this fully replacing the gnupg cli entirely.
Decryption is just as easy and straightforward. 
If anything breaks or explodes don't blame me, blame chat gpt ;).

