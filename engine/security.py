import os
import base64
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

class SecurityEngine:
    ITERATIONS = 100000
    SALT_SIZE = 16
    ALGORITHMS = [
        "AES-GCM", "ChaCha20", "Fernet", "AES-CTR", "CAST5", 
        "SEED", "Camellia", "Triple-DES", "SPECTRE-XOR", 
        "BIT-SHIFTER", "CYPHER-SHUFFLE", "Vigenere-Plus", "MULTI-LAYER"
    ]

    ALGO_MAP = {
        1: "AES-GCM", 2: "ChaCha20", 3: "Fernet", 4: "AES-CTR", 
        5: "CAST5", 6: "SEED", 7: "Camellia", 8: "Triple-DES", 
        9: "SPECTRE-XOR", 10: "BIT-SHIFTER", 11: "CYPHER-SHUFFLE", 
        12: "Vigenere-Plus", 13: "MULTI-LAYER"
    }

    @staticmethod
    def derive_key(password: str, salt: bytes = None, length: int = 32) -> tuple[bytes, bytes]:
        if salt is None:
            salt = os.urandom(SecurityEngine.SALT_SIZE)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=SecurityEngine.ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password.encode()), salt

    @staticmethod
    def _apply_custom(data: bytes, key: bytes, mode: str) -> bytes:
        """Helper for custom obfuscation layers."""
        res = bytearray(data)
        if mode == "XOR":
            for i in range(len(res)):
                res[i] ^= key[i % len(key)]
        elif mode == "SHIFT":
            for i in range(len(res)):
                res[i] = (res[i] + key[i % len(key)]) % 256
        elif mode == "UNSHIFT":
            for i in range(len(res)):
                res[i] = (res[i] - key[i % len(key)]) % 256
        return bytes(res)

    @staticmethod
    def encrypt_data(data: bytes, password: str, algorithm: str = "AES-GCM") -> bytes:
        key, salt = SecurityEngine.derive_key(password)
        algo_id = {v: k for k, v in SecurityEngine.ALGO_MAP.items()}.get(algorithm, 1)
        header = bytes([algo_id]) + salt

        if algorithm == "AES-GCM":
            nonce = os.urandom(12)
            return header + nonce + AESGCM(key).encrypt(nonce, data, None)
        elif algorithm == "ChaCha20":
            nonce = os.urandom(12)
            return header + nonce + ChaCha20Poly1305(key).encrypt(nonce, data, None)
        elif algorithm == "Fernet":
            return header + Fernet(base64.urlsafe_b64encode(key)).encrypt(data)
        elif algorithm in ["AES-CTR", "CAST5", "SEED", "Camellia", "Triple-DES"]:
            iv = os.urandom(16 if algorithm != "Triple-DES" else 8)
            algo_cls = {
                "AES-CTR": algorithms.AES(key),
                "CAST5": algorithms.CAST5(key[:16]),
                "SEED": algorithms.SEED(key[:16]),
                "Camellia": algorithms.Camellia(key),
                "Triple-DES": algorithms.TripleDES(key[:24])
            }[algorithm]
            cipher = Cipher(algo_cls, modes.CTR(iv) if algorithm == "AES-CTR" else modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            # Padding for CBC
            if algorithm != "AES-CTR":
                padder = padding.PKCS7(algo_cls.block_size).padder()
                data = padder.update(data) + padder.finalize()
            return header + iv + encryptor.update(data) + encryptor.finalize()
        elif algorithm == "SPECTRE-XOR":
            return header + SecurityEngine._apply_custom(data, key, "XOR")
        elif algorithm == "BIT-SHIFTER":
            return header + SecurityEngine._apply_custom(data, key, "SHIFT")
        elif algorithm == "MULTI-LAYER":
            # AES then Custom XOR
            enc = SecurityEngine.encrypt_data(data, password, "AES-GCM")[17:] # Strip header
            return header + SecurityEngine._apply_custom(enc, key, "XOR")
        else:
            # Default to XOR for custom/placeholder
            return header + SecurityEngine._apply_custom(data, key, "XOR")

    @staticmethod
    def decrypt_data(blob: bytes, password: str) -> bytes:
        algo_id = blob[0]
        salt = blob[1:17]
        payload = blob[17:]
        key, _ = SecurityEngine.derive_key(password, salt)
        algorithm = SecurityEngine.ALGO_MAP.get(algo_id)

        try:
            if algorithm == "AES-GCM":
                return AESGCM(key).decrypt(payload[:12], payload[12:], None)
            elif algorithm == "ChaCha20":
                return ChaCha20Poly1305(key).decrypt(payload[:12], payload[12:], None)
            elif algorithm == "Fernet":
                return Fernet(base64.urlsafe_b64encode(key)).decrypt(payload)
            elif algorithm in ["AES-CTR", "CAST5", "SEED", "Camellia", "Triple-DES"]:
                iv_size = 16 if algorithm != "Triple-DES" else 8
                iv, ciphertext = payload[:iv_size], payload[iv_size:]
                algo_cls = {
                    "AES-CTR": algorithms.AES(key),
                    "CAST5": algorithms.CAST5(key[:16]),
                    "SEED": algorithms.SEED(key[:16]),
                    "Camellia": algorithms.Camellia(key),
                    "Triple-DES": algorithms.TripleDES(key[:24])
                }[algorithm]
                cipher = Cipher(algo_cls, modes.CTR(iv) if algorithm == "AES-CTR" else modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                dec = decryptor.update(ciphertext) + decryptor.finalize()
                if algorithm != "AES-CTR":
                    unpadder = padding.PKCS7(algo_cls.block_size).unpadder()
                    dec = unpadder.update(dec) + unpadder.finalize()
                return dec
            elif algorithm == "SPECTRE-XOR":
                return SecurityEngine._apply_custom(payload, key, "XOR")
            elif algorithm == "BIT-SHIFTER":
                return SecurityEngine._apply_custom(payload, key, "UNSHIFT")
            elif algorithm == "MULTI-LAYER":
                raw = SecurityEngine._apply_custom(payload, key, "XOR")
                # Need a mock blob to recurse decrypt_data or just manual
                fake_blob = bytes([1]) + salt + raw
                return SecurityEngine.decrypt_data(fake_blob, password)
            else:
                return SecurityEngine._apply_custom(payload, key, "XOR")
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    @staticmethod
    def encrypt_file(file_path: str, password: str, output_path: str, algorithm: str = "AES-GCM"):
        with open(file_path, 'rb') as f:
            data = f.read()
        with open(output_path, 'wb') as f:
            f.write(SecurityEngine.encrypt_data(data, password, algorithm))

    @staticmethod
    def decrypt_file(file_path: str, password: str, output_path: str):
        with open(file_path, 'rb') as f:
            blob = f.read()
        with open(output_path, 'wb') as f:
            f.write(SecurityEngine.decrypt_data(blob, password))
