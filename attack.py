from oracle import encrypt, is_padding_ok, BLOCK_SIZE


def test_the_attack():
    messages = (b'Attack at dawn', b'', b'Giovanni',
                b"In symmetric cryptography, the padding oracle attack can be applied to the CBC mode of operation," +
                b"where the \"oracle\" (usually a server) leaks data about whether the padding of an encrypted " +
                b"message is correct or not. Such data can allow attackers to decrypt (and sometimes encrypt) " +
                b"messages through the oracle using the oracle's key, without knowing the encryption key")
    for msg in messages:
        print('Testing:', msg)
        cracked_ct = attack(encrypt(msg))
        assert cracked_ct == msg


def attack(ciphertext):
    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    current_block = len(blocks)-1
    plaintext = ""

    # Cycle over blocks starting from last one and last one -1.
    while current_block > 0:
        pad_len = get_padding(blocks, current_block)
        idx_paderror = BLOCK_SIZE - pad_len
        iv_copy = bytearray(blocks[current_block-1])  # Need another copy of the IV to send it to the oracle for decrypt so that I do not modify blocks
        
        while idx_paderror > 0:
            idx_reverse = BLOCK_SIZE - 1

            while idx_reverse >= idx_paderror:  # Here I modify the bytes of padding increasing them with XOR
                iv_copy[idx_reverse] = iv_copy[idx_reverse] ^ pad_len ^ (pad_len + 1)
                idx_reverse -= 1
    
            for guessedValue in range(0, 256):  # Here I find the guessed value and decrypt the current index
                iv_copy[idx_reverse] = guessedValue
                if is_padding_ok(bytes(iv_copy) + blocks[current_block]):
                    plaintext += chr((pad_len + 1) ^ guessedValue ^ blocks[current_block - 1][idx_reverse])
                    break
                
            pad_len += 1
            idx_paderror -= 1
        # }END WHILE that Cycle over bytes.
        current_block -= 1
    # }END WHILE that Cycle over blocks.
    return str.encode(plaintext[::-1])


def get_padding(blocks, current_block):
    idx_paderror = 0
    if current_block < len(blocks) - 1:  # If I am not visiting the last block, I have no padding.
        idx_paderror = BLOCK_SIZE
    else:  # Else I find the Pad Length.
        iv_fake = bytearray(blocks[current_block - 1])
        for byte in iv_fake:
            # Check if it is == 255 because if I do byte+1 I could get a value out of range
            iv_fake[idx_paderror] = byte - 1 if iv_fake[idx_paderror] == 255 else byte + 1

            if not is_padding_ok(bytes(iv_fake) + blocks[current_block]):
                break
            idx_paderror += 1
    return BLOCK_SIZE - idx_paderror


if __name__ == '__main__':
    test_the_attack()
