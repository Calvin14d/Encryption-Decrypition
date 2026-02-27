import os
import shutil
from .security import SecurityEngine

class VaultEngine:
    """Handles in-place locking/unlocking of files and folders."""
    
    LOCK_EXTENSION = ".LOCKED"

    @staticmethod
    def lock_item(path: str, password: str, algorithm: str = "AES-GCM"):
        """Encrypts a file or all files in a folder in-place and renames them."""
        if os.path.isdir(path):
            VaultEngine._process_folder(path, password, algorithm, encrypt=True)
        else:
            VaultEngine._process_file(path, password, algorithm, encrypt=True)

    @staticmethod
    def unlock_item(path: str, password: str):
        """Decrypts a file or all files in a folder in-place and restores names."""
        if os.path.isdir(path):
            VaultEngine._process_folder(path, password, None, encrypt=False)
        else:
            VaultEngine._process_file(path, password, None, encrypt=False)

    @staticmethod
    def _process_file(file_path: str, password: str, algorithm: str, encrypt: bool):
        if encrypt:
            if file_path.endswith(VaultEngine.LOCK_EXTENSION):
                return # Already locked
            
            temp_path = file_path + ".tmp"
            SecurityEngine.encrypt_file(file_path, password, temp_path, algorithm)
            os.remove(file_path)
            os.rename(temp_path, file_path + VaultEngine.LOCK_EXTENSION)
        else:
            if not file_path.endswith(VaultEngine.LOCK_EXTENSION):
                return # Not locked
            
            temp_path = file_path.replace(VaultEngine.LOCK_EXTENSION, ".tmp")
            SecurityEngine.decrypt_file(file_path, password, temp_path)
            os.remove(file_path)
            os.rename(temp_path, file_path.replace(VaultEngine.LOCK_EXTENSION, ""))

    @staticmethod
    def _process_folder(folder_path: str, password: str, algorithm: str, encrypt: bool):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                VaultEngine._process_file(file_path, password, algorithm, encrypt)
