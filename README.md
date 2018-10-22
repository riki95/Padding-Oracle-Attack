# Padding Oracle Attack
The idea is to implement the Padding Oracle Attack against the Oracle implemented in the file oracle.py.
So, we must implement an "attack" function that, given an encrypted message (as a byte-string), recovers the original cleartext message.

## Getting Started

To download my repo:

```
git clone https://github.com/riki95/Padding-Oracle-Attack
```
Now you just run the attack.py with the text you want (you can modify it in the test_the_attack() function) and see that is working.
If you want you can erase the attack() function and implement it by yourself. This is what I've done and the main goal of this short script: learn how this attack works and implement it.

## Oracle.py explained
Most important functions (imported into the attack file):

1) the function encrypt, which takes a byte-string and returns its encryption (using a random key and IV)
2) the function is_padding_ok, which takes a byte-string an returns whether the decrypted message has a correct padding
3) the constant BLOCK_SIZE, which corresponds to the block-size of the underlying encryption algorithm (AES128, in our case).

## Authors

* **Riccardo Basso** - *Università degli studi di Genova*
