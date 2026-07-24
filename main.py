#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp

import sys
import time
import platform
from datetime import datetime
from colorama import Fore, Style

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input, log_header,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, get_active_apis,
    is_maintenance, get_maintenance_message, get_trial_quota, get_total_users,
    VERSION, TOOLS_NAME, BANNER, get_user_stats
)

def get_formatted_datetime():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    day_name = days[now.weekday()]
    day = now.day
    month = months[now.month - 1]
    year = now.year
    return f"{day_name}, {day} {month} {year}"

def get_device_name():
    try:
        return platform.node()
    except:
        return "Unknown Device"

def show_user_stats():
    premium, trial = get_user_stats()
    total = premium + trial
    print(f"{Fore.CYAN}Total Pengguna  : {Fore.WHITE}{total}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}├─ Premium      : {Fore.GREEN}{premium}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└─ Trial        : {Fore.YELLOW}{trial}{Style.RESET_ALL}")

def show_buy_guide():
    clear_screen()
    log_header()
    license_price = get_license_price()
    whatsapp_admin = get_whatsapp_admin()
    telegram_username = get_telegram_username()
    total_apis = get_active_apis()
    
    print(f"{Fore.CYAN}PANDUAN PEMBELIAN LISENSI PREMIUM{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Keuntungan Premium:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Akses FULL semua API ({total_apis} API)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Unlimited penggunaan (tanpa batas kuota)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Mendapat update tools terbaru")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Mendapat API baru jika ditambahkan")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Dukungan prioritas dari admin")
    print()
    print(f"{Fore.CYAN}Harga: {Fore.GREEN}Rp. {license_price:,}{Style.RESET_ALL} (sekali bayar, akses selamanya)")
    print()
    print(f"{Fore.YELLOW}Cara Pembelian:{Style.RESET_ALL}")
    print(f"  1. Chat admin via WhatsApp atau Telegram")
    print(f"  2. Damn ini cuman kelihatan banyak ajaa")
    print(f"  3. Uuuhhmmm GTW cuma kelihatan banyak aja")
    print(f"  4. Tunggu aktivasi")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}+62 895-3070-6871{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}t.me/Adrianzz324{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID Anda:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{get_device_id()}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali ke menu utama...")

def show_menu_trial():
    print(f"{Fore.CYAN}Menu Trial{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Jalankan Single Round")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Beli Lisensi Premium")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Keluar")
    print()

def show_menu_premium():
    print(f"{Fore.CYAN}Menu Premium{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Single Round")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Keluar")
    print()

def check_update():
    clear_screen()
    log_header()
    print(f"{Fore.CYAN}CEK UPDATE & KETERSEDIAAN API{Style.RESET_ALL}")
    print()
    current_version = VERSION
    latest_version = "3.1"
    if current_version == latest_version:
        log_success(f"Tools versi {current_version} adalah versi terbaru.")
    else:
        log_warning(f"Versi terbaru: {latest_version} | Versi saat ini: {current_version}")
        log_info("Kunjungi repository untuk update.")
    print()
    total_apis = get_active_apis()
    print(f"{Fore.CYAN}Ketersediaan API:{Style.RESET_ALL}")
    print(f"  Total API   : {Fore.WHITE}{total_apis}{Style.RESET_ALL}")
    print(f"  API Aktif   : {Fore.GREEN}{total_apis}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali ke menu utama...")

def show_thread_menu():
    clear_screen()
    log_header()
    print(f"{Fore.CYAN}Pilih Jumlah Thread (default 1){Style.RESET_ALL}")
    print()
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} 1 Thread (slow)")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} 2 Thread")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} 3 Thread")
    print(f"  {Fore.GREEN}[4]{Style.RESET_ALL} 4 Thread")
    print(f"  {Fore.GREEN}[5]{Style.RESET_ALL} 5 Thread (recommended)")
    print(f"  {Fore.GREEN}[6]{Style.RESET_ALL} 6 Thread")
    print(f"  {Fore.GREEN}[7]{Style.RESET_ALL} 7 Thread")
    print(f"  {Fore.GREEN}[8]{Style.RESET_ALL} 8 Thread")
    print(f"  {Fore.GREEN}[9]{Style.RESET_ALL} 9 Thread")
    print(f"  {Fore.GREEN}[10]{Style.RESET_ALL} 10 Thread (fast)")
    print()
    return log_input("Pilih thread (1-10, enter untuk default 1): ").strip()

def main():
    status, quota, device_id = check_license()
    
    if status == "trial":
        while True:
            clear_screen()
            log_header()
            print(f"{Fore.CYAN}{get_formatted_datetime()} | {Fore.WHITE}{get_device_name()}{Style.RESET_ALL}")
            print()
            show_user_stats()
            print()
            trial_quota = get_trial_quota()
            print(f"{Fore.YELLOW}Mode Trial - Sisa Kuota: {quota}/{trial_quota}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hanya bisa menggunakan Single Round.{Style.RESET_ALL}")
            print()
            show_menu_trial()
            
            choice = log_input("Pilih menu (1/2/3): ").strip()
            
            if choice == "1":
                if quota <= 0:
                    log_warning("Kuota trial habis!")
                    log_info("Silakan beli lisensi premium untuk melanjutkan.")
                    print()
                    input("Tekan Enter untuk melihat panduan pembelian...")
                    show_buy_guide()
                    user = check_user(device_id)
                    if user:
                        quota = user.get("quota", 0)
                    continue
                
                from main_engine import run_single_round
                success = run_single_round(threads=1)
                
                if use_quota(device_id):
                    user = check_user(device_id)
                    if user:
                        quota = user.get("quota", 0)
                        log_info(f"Sisa kuota sekarang: {quota}/{trial_quota}")
                else:
                    log_error("Gagal mengurangi kuota!")
                
                if quota == 0:
                    log_info("Kuota Anda telah habis.")
                    print()
                    input("Tekan Enter untuk melihat panduan pembelian...")
                    show_buy_guide()
                    user = check_user(device_id)
                    if user:
                        quota = user.get("quota", 0)
                    continue
                
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "2":
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
            
            elif choice == "3":
                log_info("Keluar...")
                sys.exit(0)
            
            else:
                log_warning("Pilihan tidak valid. Tekan Enter untuk kembali...")
                input()
    
    elif status == "premium":
        while True:
            clear_screen()
            log_header()
            print(f"{Fore.CYAN}{get_formatted_datetime()} | {Fore.WHITE}{get_device_name()}{Style.RESET_ALL}")
            print()
            show_user_stats()
            print()
            print(f"{Fore.GREEN}Premium Active - Full Access{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Terima kasih sudah membeli lisensi premium!{Style.RESET_ALL}")
            print()
            show_menu_premium()
            
            choice = log_input("Pilih menu (1/2/3): ").strip()
            
            if choice == "1":
                thread_choice = show_thread_menu()
                try:
                    threads = int(thread_choice) if thread_choice.strip() else 1
                    if threads < 1: threads = 1
                    elif threads > 10: threads = 10
                except:
                    threads = 1
                from main_engine import run_single_round
                run_single_round(threads=threads)
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "2":
                from main_engine import run_infinite_loop
                run_infinite_loop()
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "3":
                log_info("Keluar...")
                sys.exit(0)
            
            else:
                log_warning("Pilihan tidak valid. Tekan Enter untuk kembali...")
                input()

if __name__ == "__main__":
    main()