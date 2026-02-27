import customtkinter as ctk
import os
import threading
import time
from tkinter import filedialog, messagebox
from engine.transfer import TransferEngine
from engine.security import SecurityEngine
from engine.vault import VaultEngine
# Removed visuals import

class CipherV2tk(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CIPHER_TRANSFER // V4_PRO")
        self.geometry("1000x750")
        self.configure(fg_color="#050505")

        # --- THEME ---
        ctk.set_appearance_mode("dark")
        self.NEON_GREEN = "#00FF41"
        self.RED = "#FF3131"
        self.DARK_GRAY = "#1A1A1A"

        # --- LAYOUT ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0A0A0A")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1) # Spacer
        
        self.logo = ctk.CTkLabel(self.sidebar, text="CIPHER\n[V4_PRO]", font=ctk.CTkFont(size=20, weight="bold", family="Courier New"), text_color=self.NEON_GREEN)
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Sidebar logo removed matrix animation

        self.btn_infil = ctk.CTkButton(self.sidebar, text="INFILTRATE", fg_color="transparent", text_color=self.NEON_GREEN, border_width=1, border_color=self.NEON_GREEN, hover_color="#003300", command=lambda: self.select_frame("infiltrate"))
        self.btn_infil.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_recover = ctk.CTkButton(self.sidebar, text="RECOVER", fg_color="transparent", text_color=self.NEON_GREEN, border_width=1, border_color=self.NEON_GREEN, hover_color="#003300", command=lambda: self.select_frame("recover"))
        self.btn_recover.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_vault = ctk.CTkButton(self.sidebar, text="VAULT", fg_color="transparent", text_color=self.NEON_GREEN, border_width=1, border_color=self.NEON_GREEN, hover_color="#003300", command=lambda: self.select_frame("vault"))
        self.btn_vault.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Visuals button removed

        # --- MAIN FRAMES ---
        self.infiltrate_frame = self.create_infiltrate_frame()
        self.recover_frame = self.create_recover_frame()
        self.vault_frame = self.create_vault_frame()

        # --- LOG TERMINAL ---
        self.terminal = ctk.CTkTextbox(self, height=150, fg_color="black", text_color=self.NEON_GREEN, font=("Courier New", 12), border_width=1, border_color="#333333")
        self.terminal.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        # Visual engines removed

        self.select_frame("infiltrate")

    def log(self, text):
        self.terminal.insert("end", f"> {text}\n")
        self.terminal.see("end")

    def select_frame(self, name):
        self.infiltrate_frame.grid_forget()
        self.recover_frame.grid_forget()
        self.vault_frame.grid_forget()
        
        if name == "infiltrate": self.infiltrate_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "recover": self.recover_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "vault": self.vault_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def create_infiltrate_frame(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(frame, text="TASK: SECURE_PAYLOAD_TRANSFER", text_color=self.NEON_GREEN, font=("Courier New", 18, "bold")).pack(pady=10)
        
        self.src_entry = self.create_input_group(frame, "PAYLOAD_PATH", self.pick_file)
        self.dst_entry = self.create_input_group(frame, "EXTRACTION_VECTOR", self.pick_folder)
        
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="ACCESS_KEY", show="*", border_color=self.NEON_GREEN, fg_color=self.DARK_GRAY)
        self.pass_entry.pack(fill="x", pady=10)

        # -- ALGORITHM SELECTION (13 TYPES) --
        algo_label = ctk.CTkLabel(frame, text="ENCRYPTION_OVERRIDE_TYPE:", text_color="#666666", font=("Courier New", 10))
        algo_label.pack(anchor="w", padx=5)
        
        self.algo_var = ctk.StringVar(value="AES-GCM")
        self.algo_menu = ctk.CTkComboBox(frame, values=SecurityEngine.ALGORITHMS, variable=self.algo_var, border_color=self.NEON_GREEN, fg_color=self.DARK_GRAY)
        self.algo_menu.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(frame, text="EXECUTE_INFILTRATION", fg_color=self.NEON_GREEN, text_color="black", hover_color="#00CC33", font=("Courier New", 14, "bold"), height=45, command=self.start_transfer).pack(fill="x", pady=20)
        
        self.prog_bar = ctk.CTkProgressBar(frame, progress_color=self.NEON_GREEN)
        self.prog_bar.set(0)
        self.prog_bar.pack(fill="x", pady=10)

        return frame

    def create_recover_frame(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(frame, text="TASK: DATA_RECOVERY", text_color=self.NEON_GREEN, font=("Courier New", 18, "bold")).pack(pady=10)
        
        self.rec_src = self.create_input_group(frame, "SECURED_PAYLOAD", self.pick_file)
        self.rec_dst = self.create_input_group(frame, "RECOVERY_PATH", self.pick_folder)
        
        ctk.CTkLabel(frame, text="ALGO_DETECTION: AUTOMATIC_ENABLED", text_color=self.NEON_GREEN, font=("Courier New", 10)).pack(anchor="w", padx=5)
        
        self.rec_pass = ctk.CTkEntry(frame, placeholder_text="ACCESS_KEY", show="*", border_color=self.NEON_GREEN, fg_color=self.DARK_GRAY)
        self.rec_pass.pack(fill="x", pady=10)

        ctk.CTkButton(frame, text="EXECUTE_RECOVERY", fg_color=self.NEON_GREEN, text_color="black", font=("Courier New", 14, "bold"), height=45, command=self.start_recovery).pack(fill="x", pady=20)
        return frame

    def create_vault_frame(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(frame, text="TASK: VAULT_LOCKER", text_color=self.NEON_GREEN, font=("Courier New", 18, "bold")).pack(pady=10)
        
        self.vault_path = self.create_input_group(frame, "LOCKER_TARGET", self.pick_any)
        self.vault_pass = ctk.CTkEntry(frame, placeholder_text="VAULT_KEY", show="*", border_color=self.NEON_GREEN, fg_color=self.DARK_GRAY)
        self.vault_pass.pack(fill="x", pady=10)

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=10)
        ctk.CTkButton(btn_row, text="LOCK_TARGET", fg_color="#770000", text_color="white", command=lambda: self.vault_action("LOCK")).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_row, text="UNLOCK_TARGET", fg_color="#007700", text_color="white", command=lambda: self.vault_action("UNLOCK")).pack(side="left", expand=True, padx=5)
        
        return frame

        # visuals_frame removed

    def create_input_group(self, parent, label, command):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=5)
        e = ctk.CTkEntry(f, placeholder_text=label, border_color=self.NEON_GREEN, fg_color=self.DARK_GRAY)
        e.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(f, text="...", width=40, border_width=1, border_color=self.NEON_GREEN, fg_color="transparent", command=lambda: command(e)).pack(side="right", padx=(5, 0))
        return e

    def pick_file(self, entry):
        path = filedialog.askopenfilename()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def pick_folder(self, entry):
        path = filedialog.askdirectory()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def pick_any(self, entry):
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def show_overlay(self, status):
        color = self.NEON_GREEN if status == "GRANTED" else self.RED
        text = f"ACCESS_{status}"
        
        popup = ctk.CTkToplevel(self)
        popup.geometry("600x300")
        popup.title("AUTH_SYSTEM")
        popup.configure(fg_color="#050505")
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup, text=text, font=("Courier New", 50, "bold"), text_color=color)
        label.pack(expand=True)
        
        self.after(1500, popup.destroy)

    def start_transfer(self):
        threading.Thread(target=self._run_transfer).start()

    def _run_transfer(self):
        src = self.src_entry.get()
        dst_dir = self.dst_entry.get()
        password = self.pass_entry.get()
        algo = self.algo_var.get()
        if not all([src, dst_dir, password]): self.log("ERR: MISSING_ARGS"); return
        
        self.log(f"INIT: {os.path.basename(src)} -> {algo}")
        try:
            filename = os.path.basename(src) + ".fhc"
            dst = os.path.join(dst_dir, filename)
            TransferEngine.transfer_item(src, dst, password, "TRANSFER", algo, self.on_prog)
            self.show_overlay("GRANTED")
            self.log("FIN: PAYLOAD_INFILTRATED")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def start_recovery(self):
        threading.Thread(target=self._run_recovery).start()

    def _run_recovery(self):
        src, dst_dir, password = self.rec_src.get(), self.rec_dst.get(), self.rec_pass.get()
        if not all([src, dst_dir, password]): self.log("ERR: MISSING_ARGS"); return
        
        self.log(f"INIT_RECOVERY: {os.path.basename(src)}")
        try:
            filename = os.path.basename(src).replace(".fhc", "")
            dst = os.path.join(dst_dir, filename)
            TransferEngine.transfer_item(src, dst, password, "DECRYPT", None, self.on_prog)
            self.show_overlay("GRANTED")
            self.log("FIN: DATA_RESTORED")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def vault_action(self, action):
        threading.Thread(target=self._run_vault, args=(action,)).start()

    def _run_vault(self, action):
        path, password = self.vault_path.get(), self.vault_pass.get()
        if not path or not password: self.log("ERR: VAULT_ARGS_MISSING"); return
        
        self.log(f"VAULT_{action}: {os.path.basename(path)}")
        try:
            if action == "LOCK": VaultEngine.lock_item(path, password)
            else: VaultEngine.unlock_item(path, password)
            self.show_overlay("GRANTED")
            self.log(f"SUCCESS: VAULT_{action}_COMPLETE")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def on_prog(self, item, size, success, err=None):
        base = os.path.basename(item)
        if success: self.log(f"OK: {base} ({size}B)")
        else: self.log(f"ERR: {base} // {err}")

if __name__ == "__main__":
    app = CipherV2tk()
    app.mainloop()

    def pick_file(self, entry):
        path = filedialog.askopenfilename()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def pick_folder(self, entry):
        path = filedialog.askdirectory()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def pick_any(self, entry):
        # Could be file or folder - ask what the user wants to pick? 
        # For simplicity, let's offer both or just ask for a generic pick
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path: entry.delete(0, "end"); entry.insert(0, path)

    def show_overlay(self, status):
        color = self.NEON_GREEN if status == "GRANTED" else self.RED
        text = f"ACCESS_{status}"
        
        popup = ctk.CTkToplevel(self)
        popup.geometry("600x300")
        popup.title("AUTH_SYSTEM")
        popup.configure(fg_color="#050505")
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup, text=text, font=("Courier New", 50, "bold"), text_color=color)
        label.pack(expand=True)
        
        self.after(1500, popup.destroy)

    def start_transfer(self):
        threading.Thread(target=self._run_transfer).start()

    def _run_transfer(self):
        src, dst_dir, password, algo = self.src_entry.get(), self.dst_entry.get(), self.pass_entry.get(), self.algo_var.get()
        if not all([src, dst_dir, password]): self.log("ERR: MISSING_ARGS"); return
        
        self.log(f"INIT: {os.path.basename(src)} -> {algo}")
        try:
            filename = os.path.basename(src) + ".fhc"
            dst = os.path.join(dst_dir, filename)
            TransferEngine.transfer_item(src, dst, password, "TRANSFER", algo, self.on_prog)
            self.show_overlay("GRANTED")
            self.log("FIN: PAYLOAD_INFILTRATED")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def start_recovery(self):
        threading.Thread(target=self._run_recovery).start()

    def _run_recovery(self):
        src, dst_dir, password = self.rec_src.get(), self.rec_dst.get(), self.rec_pass.get()
        if not all([src, dst_dir, password]): self.log("ERR: MISSING_ARGS"); return
        
        self.log(f"INIT_RECOVERY: {os.path.basename(src)}")
        try:
            filename = os.path.basename(src).replace(".fhc", "")
            dst = os.path.join(dst_dir, filename)
            TransferEngine.transfer_item(src, dst, password, "DECRYPT", None, self.on_prog)
            self.show_overlay("GRANTED")
            self.log("FIN: DATA_RESTORED")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def vault_action(self, action):
        threading.Thread(target=self._run_vault, args=(action,)).start()

    def _run_vault(self, action):
        path, password = self.vault_path.get(), self.vault_pass.get()
        if not path or not password: self.log("ERR: VAULT_ARGS_MISSING"); return
        
        self.log(f"VAULT_{action}: {os.path.basename(path)}")
        try:
            if action == "LOCK": VaultEngine.lock_item(path, password)
            else: VaultEngine.unlock_item(path, password)
            self.show_overlay("GRANTED")
            self.log(f"SUCCESS: VAULT_{action}_COMPLETE")
        except Exception as e:
            self.show_overlay("DENIED")
            self.log(f"FAIL: {str(e)}")

    def on_prog(self, item, size, success, err=None):
        base = os.path.basename(item)
        if success: self.log(f"OK: {base} ({size}B)")
        else: self.log(f"ERR: {base} // {err}")

if __name__ == "__main__":
    app = CipherV2tk()
    app.mainloop()
