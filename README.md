# 🦅 FALCON Command Center

**FALCON Command Center** is a lightweight terminal-based security and system diagnostics utility for **Termux and Linux**.

It focuses on **local-device visibility**: system information, memory/storage health, local network information, listening sockets, SSH status, security scoring, scan history, JSON reports, change detection, self-tests, themes, and a small Falcon social launcher.

> **Safety first:** FALCON is designed for local diagnostics. It does not perform external host scanning, credential collection, credential extraction, or automatic system changes.

## ✨ Features

- 🛡️ **Security Score** — simple 0–100 local security assessment
- 📊 **Live Dashboard** — device, battery, RAM, storage, network and SSH status
- 🔍 **Full Security Scan** — generates findings and saves a JSON report
- 🌐 **Network Diagnostics** — local IP, DNS and listening sockets
- 📱 **Device Information** — Android/Termux or Linux system details
- ❤️ **Health Center** — checks common local command availability
- 📈 **Scan History** — keeps previous security scores
- 🔄 **Change Detector** — compares the current scan with the latest saved report
- 📁 **Report Browser** — view saved JSON reports
- 🔐 **Privacy Center** — shows FALCON's safety boundaries
- 🧪 **Self-Test** — checks core diagnostic components
- 🎨 **Themes** — CYAN, MATRIX, PURPLE and MONO
- 📸 **Instagram launcher** — opens the configured Falcon profile using Android intent/browser fallback

## 🖥️ Supported environments

Designed primarily for:

- Termux on Android
- Linux
- Debian/Ubuntu-based systems
- Kali Linux

Some information depends on the commands and files available on the host system. Missing tools are handled gracefully where possible.

## 🚀 Installation

### Termux

```bash
pkg update
pkg install python git
git clone https://github.com/YOUR-USERNAME/FALCON-Command-Center.git
cd FALCON-Command-Center
python3 falcon_command_center.py
```

### Linux / Kali

```bash
git clone https://github.com/YOUR-USERNAME/FALCON-Command-Center.git
cd FALCON-Command-Center
python3 falcon_command_center.py
```

No third-party Python packages are required; the project uses Python's standard library.

## ▶️ Run

```bash
python3 falcon_command_center.py
```

Optional executable launcher:

```bash
chmod +x run.sh
./run.sh
```

## 📂 Reports and settings

FALCON stores local data outside the Git repository:

- Reports: `~/FALCON_reports/`
- Theme settings: `~/.falcon_settings.json`

Reports are JSON files named like:

```text
FALCON_security_YYYYMMDD_HHMMSS.json
```

These files contain local system information, so **do not commit personal scan reports to a public repository**.

## 🔒 Security & privacy

FALCON intentionally avoids:

- External host scanning
- Password collection
- Credential extraction
- Automatic system changes
- Scanner-generated external network requests

The network diagnostics screen only displays information available locally on the device.

## 🧰 Requirements

- Python 3
- A terminal
- Optional system utilities such as `ip`, `ss`, `netstat`, `getprop`, `dpkg-query`, `pgrep`, `ssh` and Android `am`

The program can still run when some optional utilities are unavailable.

## 🗺️ Menu

| Option | Feature |
|---:|---|
| 1 | Full Security Scan |
| 2 | Live Dashboard |
| 3 | Network Diagnostics |
| 4 | Device Information |
| 5 | Health Center |
| 6 | Scan History |
| 7 | Change Detector |
| 8 | Report Browser |
| 9 | Privacy Center |
| 10 | FALCON Self-Test |
| 11 | Settings / Themes |
| 12 | Falcon Instagram |
| 0 | Exit |

## 📸 Screenshots

Add screenshots here after uploading the project to GitHub:

```text
docs/
├── dashboard.png
├── security-scan.png
└── settings.png
```

Then reference them in this README with:

```markdown
![FALCON Dashboard](docs/dashboard.png)
```

## 🤝 Contributing

Pull requests and improvements are welcome.

Before submitting a change:

1. Keep the tool focused on local diagnostics.
2. Avoid adding credential collection or unauthorized scanning features.
3. Keep dependencies minimal.
4. Test the program with Python 3.
5. Update the README when adding major features.

## ⚠️ Disclaimer

FALCON Command Center is intended for **defensive, educational and authorized local diagnostics**.

Only use security tools and diagnostics on systems and networks you own or have explicit permission to assess. The author is not responsible for misuse.

## 👤 Author

**Falcon by Sinan**

Instagram: `@sinanzzyy`

---

🦅 **FALCON — Stay secure. Stay curious.**
