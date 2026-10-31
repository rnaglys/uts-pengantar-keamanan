import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

# Pastikan path templates absolut agar tidak TemplateNotFound di serverless Vercel
base_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(base_dir, "templates")

app = Flask(__name__, template_folder=templates_dir)
app.secret_key = "keamanan-sistem-informasi-angelita-secret-key"

# In-memory dummy data storage untuk log insiden keamanan
incidents = [
    {
        "id": 1,
        "date": "2024-10-31 09:15",
        "system": "Server Database Utama",
        "threat_type": "SQL Injection Attempt",
        "severity": "High",
        "status": "Terselesaikan",
        "notes": "Upaya injeksi SQL terdeteksi oleh WAF dan otomatis di-block."
    },
    {
        "id": 2,
        "date": "2024-10-30 14:40",
        "system": "Portal Web Mahasiswa",
        "threat_type": "Brute Force Attack",
        "severity": "Medium",
        "status": "Dalam Investigasi",
        "notes": "15 kali kegagalan login berturut-turut dari IP 192.168.1.105."
    },
    {
        "id": 3,
        "date": "2024-10-29 11:20",
        "system": "Mail Gateway Office",
        "threat_type": "Phishing Email",
        "severity": "Critical",
        "status": "Terselesaikan",
        "notes": "Email palsu berkedok reset password akun banking telah di-quarantine."
    },
    {
        "id": 4,
        "date": "2024-10-28 16:05",
        "system": "Firewall Router Edge",
        "threat_type": "Port Scanning",
        "severity": "Low",
        "status": "Monitoring",
        "notes": "Aktivitas scanning port terbuka terdeteksi tanpa anomali lanjutan."
    }
]

@app.route("/")
def index():
    # Hitung ringkasan statistik
    total_logs = len(incidents)
    critical_logs = len([i for i in incidents if i["severity"] in ["Critical", "High"]])
    resolved_logs = len([i for i in incidents if i["status"] == "Terselesaikan"])

    stats = {
        "total": total_logs,
        "critical": critical_logs,
        "resolved": resolved_logs,
        "safety_score": 98.6
    }
    return render_template("index.html", incidents=incidents, stats=stats)

@app.route("/add-incident", methods=["POST"])
def add_incident():
    system = request.form.get("system", "").strip()
    threat_type = request.form.get("threat_type", "").strip()
    severity = request.form.get("severity", "Low")
    status = request.form.get("status", "Baru")
    notes = request.form.get("notes", "").strip()

    if not system or not threat_type:
        flash("Gagal menambahkan log: Nama Sistem dan Jenis Ancaman wajib diisi!", "error")
        return redirect(url_for("index"))

    new_id = (max([i["id"] for i in incidents]) + 1) if incidents else 1
    new_entry = {
        "id": new_id,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "system": system,
        "threat_type": threat_type,
        "severity": severity,
        "status": status,
        "notes": notes or "Tidak ada catatan tambahan."
    }
    # Tambahkan di baris paling atas
    incidents.insert(0, new_entry)
    flash(f"Log Insiden #{new_id} ({threat_type}) berhasil ditambahkan ke dashboard!", "success")
    return redirect(url_for("index"))

@app.route("/delete-incident/<int:item_id>", methods=["POST"])
def delete_incident(item_id):
    global incidents
    incidents = [item for item in incidents if item["id"] != item_id]
    flash(f"Log Insiden #{item_id} berhasil dihapus dari sistem.", "info")
    return redirect(url_for("index"))

# Variabel app diekspos untuk deployment serverless Vercel
app = app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

