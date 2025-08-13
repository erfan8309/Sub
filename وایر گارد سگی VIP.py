import random
import string
import ipaddress
import base64
import os
import tkinter as tk
from tkinter import messagebox, filedialog

# توابع تولید مقادیر رندوم
def generate_random_key():
    return base64.b64encode(os.urandom(32)).decode('utf-8')

def generate_random_ip(v4=True):
    if v4:
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}/32"
    else:
        return str(ipaddress.IPv6Address(random.getrandbits(128))) + "/128"

def generate_random_dns():
    dns_v4 = [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(2)]
    dns_v6 = [str(ipaddress.IPv6Address(random.getrandbits(128))) for _ in range(2)]
    return dns_v4 + dns_v6

def generate_random_endpoint():
    hostname = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(['vip.host', 'example.com', 'vpnserver.com'])
    port = random.randint(1000, 9999)
    return f"{hostname}.{domain}:{port}"

# تابع تولید کانفیگ
def generate_wireguard_config():
    private_key = generate_random_key()
    public_key = generate_random_key()
    address_v4 = generate_random_ip(v4=True)
    address_v6 = generate_random_ip(v4=False)
    dns_list = generate_random_dns()
    mtu = random.choice([1280, 1400, 1420, 1500])
    allowed_ips = generate_random_ip(v4=False)
    endpoint = generate_random_endpoint()

    config = f"""
[Interface]
PrivateKey = {private_key}
Address = {address_v4}, {address_v6}
DNS = {', '.join(dns_list)}
MTU = {mtu}

[Peer]
PublicKey = {public_key}
AllowedIPs = {allowed_ips}
Endpoint = {endpoint}
    """
    return config

# تابع ذخیره فایل
def save_config():
    config = text_box.get("1.0", tk.END)  # دریافت کانفیگ از جعبه متن
    file_name = filedialog.asksaveasfilename(defaultextension=".conf", filetypes=[("Config Files", "*.conf"), ("All Files", "*.*")])
    if file_name:
        with open(file_name, 'w') as file:
            file.write(config)
        messagebox.showinfo("Save", f"Config saved to {file_name}")

# تابع کپی به کلیپبورد
def copy_to_clipboard():
    config = text_box.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(config)
    messagebox.showinfo("Copy", "Config copied to clipboard")

# ایجاد رابط گرافیکی با tkinter
root = tk.Tk()
root.title("WireGuard Config Generator")

# برچسب MR.FACK
label = tk.Label(root, text="MR.FACK", font=("Arial", 24))
label.pack(pady=10)

# جعبه متن برای نمایش کانفیگ
text_box = tk.Text(root, height=15, width=60)
text_box.pack(padx=10, pady=10)

# دکمه تولید کانفیگ
def generate_config():
    config = generate_wireguard_config()
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, config)

generate_button = tk.Button(root, text="Generate Config", command=generate_config)
generate_button.pack(pady=5)

# دکمه کپی
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

# دکمه ذخیره
save_button = tk.Button(root, text="Save Config", command=save_config)
save_button.pack(pady=5)

# اجرای پنجره
root.mainloop()