import sys
import os
import unittest

# Add parenth path to sys.path to import engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.security import SecurityEngine

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.password = "HackerPassword123"
        self.test_file = "test_data.txt"
        self.encrypted_file = "test_data.txt.fhc"
        self.decrypted_file = "test_data_decrypted.txt"
        
        with open(self.test_file, "w") as f:
            f.write("This is a secret message for the hacker elite.")

    def tearDown(self):
        for f in [self.test_file, self.encrypted_file, self.decrypted_file, "skeleton.key"]:
            if os.path.exists(f):
                os.remove(f)

    def test_encryption_decryption(self):
        # Encrypt
        SecurityEngine.encrypt_file(self.test_file, self.password, self.encrypted_file)
        self.assertTrue(os.path.exists(self.encrypted_file))
        
        # Original should be different from encrypted (highly likely)
        with open(self.test_file, "rb") as f:
            original = f.read()
        with open(self.encrypted_file, "rb") as f:
            encrypted = f.read()
        self.assertNotEqual(original, encrypted)

        # Decrypt
        SecurityEngine.decrypt_file(self.encrypted_file, self.password, self.decrypted_file)
        self.assertTrue(os.path.exists(self.decrypted_file))

        with open(self.decrypted_file, "rb") as f:
            decrypted = f.read()
        
        self.assertEqual(original, decrypted)

    def test_invalid_password(self):
        SecurityEngine.encrypt_file(self.test_file, self.password, self.encrypted_file)
        with self.assertRaises(ValueError):
            SecurityEngine.decrypt_file(self.encrypted_file, "WrongPassword", self.decrypted_file)

    def test_skeleton_key(self):
        path = SecurityEngine.generate_skeleton_key(self.password, "skeleton.key")
        self.assertTrue(os.path.exists(path))
        with open(path, "rb") as f:
            content = f.read()
            self.assertEqual(len(content), 16 + 44) # 16 salt + 44 base64 Fernet key

if __name__ == "__main__":
    unittest.main()
