"""
The Caesar cipher is one of the oldest and simplest encryption techniques.
It works by shifting each letter in a message by a fixed number of positions
in the alphabet.
"""

class Codec:
    def __init__(self,shift=3):
        self.shift = shift
    
    def caesar_encrypt(self, text):
        res = ''
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                res += chr((ord(c) - base + self.shift) % 26 + base)
            else:
                # Non-letter
                res+=c
        return res

    def caesar_decrypt(self, text):
        res = ''
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                res += chr((ord(c) - base - self.shift) % 26 + base)
            else:
                res+=c
        return res
    
    def encode(self, ls):
        encoded = [ f"{len(s)}#{self.caesar_encrypt(s)}" for s in ls ]
        return ''.join(encoded)

    def decode(self, encoded):
        decoded = []
        i = 0
        while i < len(encoded):
            j = encoded.find('#', i)
            length = int(encoded[i:j])
            encrypted = encoded[j+1:j+1+length]
            decrypted = self.caesar_decrypt(encrypted)
            decoded.append(decrypted)
            i = j + 1 + length
        return decoded


codec = Codec(shift=3)

commands = ["Push", "Box, box", "Overtake", "", "Check temperatures"]
encoded = codec.encode(commands)
decoded = codec.decode(encoded)

print("Original:", commands)
print("Encoded:", encoded)
print("Decoded:", decoded)