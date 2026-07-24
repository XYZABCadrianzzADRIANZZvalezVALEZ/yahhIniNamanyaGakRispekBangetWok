# license.py - Wrapper untuk meng-import kode terenkripsi (DENGAN __file__ FIX)

import sys
import os
import base64
import zlib
import re

# ==========================================
# SET __file__ BIAR GAK ERROR
# ==========================================
if '__file__' not in globals():
    globals()['__file__'] = os.path.abspath(__file__)

def load_encrypted_module():
    """Baca dan dekripsi file license_enc.py, lalu return sebagai module"""
    
    # Baca file hasil enkripsi
    with open("license_enc.py", "r", encoding="utf-8") as f:
        encrypted_content = f.read()
    
    # Ekstrak data encrypted dari file (ambil bagian setelah ENCRYPTED = """...""")
    match = re.search(r'ENCRYPTED = """(.*?)"""', encrypted_content, re.DOTALL)
    if not match:
        raise Exception("Gagal menemukan data encrypted!")
    
    encrypted_data = match.group(1)
    
    # ==========================================
    # PROSES DEKRIPSI
    # ==========================================
    
    # Layer 4: Base64 decode
    step1 = base64.b64decode(encrypted_data)
    
    # Layer 3: XOR (ambil kunci dari awal)
    xor_key = step1[:32]
    ciphertext = step1[32:]
    step2 = bytes([ciphertext[i] ^ xor_key[i % len(xor_key)] for i in range(len(ciphertext))])
    
    # Layer 2: Zlib decompress
    step3 = zlib.decompress(step2)
    
    # Layer 1: Base64 decode
    step4 = base64.b64decode(step3)
    
    # Decode ke string
    decoded = step4.decode('utf-8')
    
    # Buat module dari string, dengan __file__ yang sudah diset
    module = {
        '__file__': os.path.abspath(__file__),
        '__name__': '__main__',
        '__package__': None,
    }
    exec(decoded, module)
    return module

# ==========================================
# AUTO-LOAD SEMUA FUNGSI & VARIABEL
# ==========================================

try:
    _encrypted_module = load_encrypted_module()
    
    # Ambil SEMUA nama yang ada di module terenkripsi
    _allowed_names = list(_encrypted_module.keys())
    
    for name in _allowed_names:
        # Kecualikan nama bawaan Python (yang mulai dengan __)
        if name.startswith('__') and name not in ['__file__', '__name__']:
            continue
        globals()[name] = _encrypted_module[name]
    
    # Pastikan __file__ tetap sesuai
    globals()['__file__'] = os.path.abspath(__file__)
    
    print("✅ License module loaded from encrypted file (ALL functions & variables).")
    
except Exception as e:
    print(f"❌ Gagal load license module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)