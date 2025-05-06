from flask import Flask
import platform
import psutil
import os
import requests
from datetime import datetime
from threading import Thread

app = Flask('')

start_time = datetime.now()
ram = psutil.virtual_memory().percent
cpu = platform.processor() or "Unknown CPU"

# Fungsi untuk mendapatkan uptime dalam format yang mudah dibaca
def get_uptime():
    now = datetime.now()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# Fungsi untuk mendapatkan informasi sistem update
def get_sistem_update():
    file_path = '/storage/emulated/0/download/Termux/database/update.env'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()  # Membaca isi file dan menghapus spasi atau baris kosong
    else:
        return "Update file tidak ditemukan."

# Fungsi untuk mendapatkan IP Address
def get_ip_address():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        return ip_data.get('ip', 'Unknown IP')
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Fungsi untuk mengukur kecepatan (dalam contoh ini, kecepatan dummy)
def hazel_speed_test():
    # Kamu bisa implementasikan pengujian kecepatan jaringan di sini
    return 100  # kecepatan dummy dalam mbps

# Fungsi untuk menampilkan informasi dalam format HTML
@app.route('/')
def about():
    kecepatan = hazel_speed_test()
    ip_address = get_ip_address()
    ram = psutil.virtual_memory().percent
    sistem_update = get_sistem_update()
    uptime = get_uptime()

    # Banner dan Informasi Server
    html_content = f"""
    <html>
        <head>
            <title>Status Server</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #333;
                    color: white;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    color: #00CFFF;
                }}
                .section {{
                    background-color: #444;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                }}
                .section h2 {{
                    margin-top: 0;
                }}
                .banner {{
                    background-color: #222;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                    border-radius: 10px;
                }}
                .banner h1 {{
                    font-size: 2em;
                    color: #F8A1C0;
                }}
            </style>
        </head>
        <body>
            <div class="banner">
                <h1>Antartica-Server</h1>
                <p>Powered by Antartica</p>
            </div>
            <div class="section">
                <h2>Informasi</h2>
                <p><strong>Update:</strong> {sistem_update}</p>
                <p><strong>Python:</strong> {platform.python_version()}</p>
                <p><strong>OS:</strong> {platform.system()}</p>
                <p><strong>Powered:</strong> Antartica-Server</p>
                <p><strong>Status Bot:</strong> 🟢 Aktif</p>
            </div>
            <div class="section">
                <h2>Developer</h2>
                <p><strong>Author:</strong> Hazelnut</p>
                <p><strong>WhatsApp:</strong> +6285183131924</p>
                <p><strong>TikTok:</strong> @stc_fay</p>
                <p><strong>Instagram:</strong> @stc_ryzzz</p>
                <p><strong>Team:</strong> Coding Jawascript</p>
            </div>
            <div class="section">
                <h2>Server</h2>
                <p><strong>IP Address:</strong> {ip_address}</p>
                <p><strong>RAM Usage:</strong> {ram}%</p>
                <p><strong>CPU Usage:</strong> {cpu}</p>
                <p><strong>Latency:</strong> {kecepatan:.2f} mbps</p>
                <p><strong>Uptime:</strong> {uptime}</p>
            </div>
        </body>
    </html>
    """
    return html_content

# Fungsi untuk menjalankan aplikasi Flask
def run():
    app.run(host='0.0.0.0', port=8080)

# Fungsi untuk menjaga server tetap hidup
def keep_alive():
    t = Thread(target=run)
    t.start()

# Mulai server
keep_alive()