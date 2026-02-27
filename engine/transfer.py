import os
import time
import shutil
from .security import SecurityEngine

class TransferEngine:
    BUFFER_SIZE = 1024 * 1024 # 1MB chunks

    @staticmethod
    def transfer_item(src, dst, password, mode="TRANSFER", algorithm="AES-GCM", progress_callback=None):
        """
        Transfers a file or folder. 
        If src is a folder, it processes recursively.
        mode: "TRANSFER" (Encrypt & Copy) or "DECRYPT" (Decrypt & Copy).
        """
        if os.path.isdir(src):
            TransferEngine._transfer_folder(src, dst, password, mode, algorithm, progress_callback)
        else:
            TransferEngine._transfer_file(src, dst, password, mode, algorithm, progress_callback)

    @staticmethod
    def _transfer_file(src, dst, password, mode, algorithm="AES-GCM", progress_callback=None):
        """Processes a single file."""
        try:
            if mode == "TRANSFER":
                SecurityEngine.encrypt_file(src, password, dst, algorithm)
            else:
                SecurityEngine.decrypt_file(src, password, dst)
            
            if progress_callback:
                size = os.path.getsize(src)
                progress_callback(src, size, True)
        except Exception as e:
            if progress_callback:
                progress_callback(src, 0, False, str(e))
            raise e

    @staticmethod
    def _transfer_folder(src_root, dst_root, password, mode, algorithm="AES-GCM", progress_callback=None):
        """Recursively processes a folder."""
        for root, dirs, files in os.walk(src_root):
            # Create corresponding directory in destination
            rel_path = os.path.relpath(root, src_root)
            target_dir = os.path.join(dst_root, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for file in files:
                src_file = os.path.join(root, file)
                
                # Determine destination filename
                if mode == "TRANSFER":
                    dst_file = os.path.join(target_dir, file + ".fhc")
                else:
                    dst_file = os.path.join(target_dir, file.replace(".fhc", ""))
                
                TransferEngine._transfer_file(src_file, dst_file, password, mode, algorithm, progress_callback)
