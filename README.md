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

## Attack.py explained
I decrypt blocks starting from the last one.
The first thing I did was to split the ciphertext into blocks, every block is large BLOCKSIZE. So I create my block list and I can use it to decrypt the ciphertext.

I call "Current_Block" the block I want to decrypt, so the IV is current_block-1 for every block. I start from the last one and here I have 2 cases:

1) the last block fills perfectly the dimension BLOCK_SIZE. In this case I know for sure that I will have 1 more block of padding.
2) the last block not fills the dimension and there is padding. In this case I use the get_padding function to know actually how much the pad_len is. For example, for attack at dawn I get an error on index 14, so I know that the pad_len is 2.

Now that I know the pad, I can decrypt the last block so I modify the pad bytes with the XOR to get the actual pad_len +1 and I do the same for the index I want to decrypt. When I find a guessed value [in the Range 0-255] that is ok for the is_padding_ok function, it means I can decrypt the current index and add it to the plaintext.

I always use current_block index to cicle over blocks and I decrement it when I have to switch block to analyze. So the next block I want to analyze, I will have no pad and in the function get_padding I will assign to idx_paderror the value BLOCK_SIZE, so that the pad_len is 0. Obviously in this case we will start modifying the index we want to decrypt letting the oracle think that we have pad 1, and so on.

## Authors

* **Riccardo Basso** - *Università degli studi di Genova*
