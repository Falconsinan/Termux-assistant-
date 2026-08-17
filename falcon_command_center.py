#!/usr/bin/env python3
"""
FALCON Command Center v4.0
Falcon by Sinan

Local Termux/Linux security diagnostics only.
No external host scanning, credential collection, or automatic system changes.
"""

import datetime as dt
import json
import os
import platform
import shutil
import socket
import subprocess
import time
import webbrowser
from pathlib import Path

# ==================== CONFIG ====================

VERSION = "5.0"
REPORT_DIR = Path.home() / "FALCON_reports"
INSTAGRAM_URL = "https://www.instagram.com/sinanzzyy?igsh=azZnaTg5am5sOGdp"

# ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

THEMES = {
    "CYAN": (CYAN, BLUE, MAGENTA),
    "MATRIX": (GREEN, GREEN, CYAN),
    "PURPLE": (MAGENTA, BLUE, CYAN),
    "MONO": (WHITE, WHITE, WHITE),
}

SETTINGS_FILE = Path.home() / ".falcon_settings.json"


# ==================== CORE UI ====================

def c(text, color=WHITE, bold=False, dim=False):
    prefix = color + (BOLD if bold else "") + (DIM if dim else "")
    return f"{prefix}{text}{RESET}"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    try:
        input(c("\n  Press ENTER to continue...", CYAN))
    except (EOFError, KeyboardInterrupt):
        pass


def term_width():
    try:
        return max(60, min(shutil.get_terminal_size((80, 24)).columns, 100))
    except Exception:
        return 80


def line(char="─"):
    return char * min(term_width(), 82)


def load_settings():
    defaults = {"theme": "CYAN"}
    try:
        if SETTINGS_FILE.exists():
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            if data.get("theme") in THEMES:
                defaults["theme"] = data["theme"]
    except Exception:
        pass
    return defaults


SETTINGS = load_settings()


def save_settings():
    try:
        SETTINGS_FILE.write_text(
            json.dumps(SETTINGS, indent=2), encoding="utf-8"
        )
    except OSError:
        pass


def palette():
    return THEMES.get(SETTINGS["theme"], THEMES["CYAN"])


def accent():
    return palette()[0]


def boot():
    clear()
    print()
    print(c("        ███████╗ █████╗ ██╗      ██████╗ ███╗   ██╗", CYAN, True))
    print(c("        ██╔════╝██╔══██╗██║     ██╔═══██╗████╗  ██║", BLUE, True))
    print(c("        █████╗  ███████║██║     ██║   ██║██╔██╗ ██║", MAGENTA, True))
    print(c("        ██╔══╝  ██╔══██║██║     ██║   ██║██║╚██╗██║", CYAN, True))
    print(c("        ██║     ██║  ██║███████╗╚██████╔╝██║ ╚████║", BLUE, True))
    print(c("        ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝", MAGENTA, True))
    print()
    print(c("                 FALCON COMMAND CENTER", WHITE, True))
    print(c("                       Falcon by Sinan", MAGENTA))
    print(c(f"                         v{VERSION}", CYAN))
    print()
    time.sleep(0.35)


def header(title, subtitle=""):
    clear()
    print(c("╭" + line("─")[:78] + "╮", accent()))
    print(c("│  🦅 FALCON COMMAND CENTER".ljust(79) + "│", accent(), True))
    print(c(f"│  {title}".ljust(79) + "│", WHITE, True))
    if subtitle:
        print(c(f"│  {subtitle}".ljust(79) + "│", WHITE, dim=True))
    print(c("╰" + line("─")[:78] + "╯", accent()))


def status_icon(ok):
    return c("●", GREEN if ok else YELLOW)


def bar(value, width=24):
    value = max(0, min(100, int(value)))
    filled = round(value / 100 * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


# ==================== SAFE COMMANDS ====================

def exists(command):
    return shutil.which(command) is not None


def run_cmd(args, timeout=4):
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError, ValueError):
        return ""


# ==================== DEVICE DATA ====================

def android_info():
    if exists("getprop"):
        release = run_cmd(["getprop", "ro.build.version.release"]) or "Unknown"
        manufacturer = run_cmd(["getprop", "ro.product.manufacturer"])
        model = run_cmd(["getprop", "ro.product.model"])
        patch = run_cmd(["getprop", "ro.build.version.security_patch"]) or "Unknown"
        return {
            "Android": release,
            "Device": f"{manufacturer} {model}".strip() or "Unknown",
            "Security Patch": patch,
        }

    return {
        "Android": "Not detected",
        "Device": platform.node() or "Unknown",
        "Security Patch": "N/A",
    }


def ram_stats():
    try:
        values = {}
        with open("/proc/meminfo", encoding="utf-8", errors="ignore") as f:
            for row in f:
                if row.startswith(("MemTotal:", "MemAvailable:")):
                    values[row.split(":")[0]] = int(row.split()[1])

        total = values.get("MemTotal", 0) / 1024
        available = values.get("MemAvailable", 0) / 1024
        if total > 0:
            used = max(0, total - available)
            percent = used / total * 100
            return total, available, used, percent
    except (OSError, ValueError):
        pass
    return 0, 0, 0, 0


def storage_stats():
    try:
        total, used, free = shutil.disk_usage(Path.home())
        return total, used, free, used / total * 100 if total else 0
    except OSError:
        return 0, 0, 0, 0


def local_ip():
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.connect(("1.1.1.1", 80))
        ip = sock.getsockname()[0]
        if ip and ip != "0.0.0.0":
            return ip
    except OSError:
        pass
    finally:
        if sock:
            sock.close()

    if exists("ip"):
        output = run_cmd(["ip", "-4", "addr", "show"])
        for row in output.splitlines():
            row = row.strip()
            if "inet " in row and "127.0.0.1" not in row:
                try:
                    return row.split()[1].split("/")[0]
                except (IndexError, ValueError):
                    pass
    return "Unknown"


def dns_servers():
    values = []
    if exists("getprop"):
        for n in range(1, 5):
            value = run_cmd(["getprop", f"net.dns{n}"])
            if value:
                values.append(value)

    if not values:
        try:
            with open("/etc/resolv.conf", encoding="utf-8", errors="ignore") as f:
                for row in f:
                    parts = row.split()
                    if len(parts) >= 2 and parts[0] == "nameserver":
                        values.append(parts[1])
        except OSError:
            pass

    return ", ".join(dict.fromkeys(values)) or "Unknown"


def ssh_status():
    running = bool(run_cmd(["pgrep", "-a", "sshd"]))
    installed = exists("sshd")
    if running:
        return "Running: sshd"
    if installed:
        return "Installed: OpenSSH Server"
    return "Not detected"


def package_count():
    if not exists("dpkg-query"):
        return "Unknown"
    output = run_cmd(["dpkg-query", "-W", "-f=${binary:Package}\n"])
    count = len([x for x in output.splitlines() if x.strip()])
    return str(count) if count else "Unknown"


def battery_info():
    paths = [
        Path("/sys/class/power_supply/battery/capacity"),
        Path("/sys/class/power_supply/BAT0/capacity"),
    ]
    for path in paths:
        try:
            value = path.read_text().strip()
            if value.isdigit():
                charging = ""
                status = path.parent / "status"
                if status.exists():
                    charging = status.read_text().strip()
                return f"{value}%{f' ({charging})' if charging else ''}"
        except OSError:
            pass
    return "Not available"


def cpu_info():
    try:
        load = os.getloadavg()[0]
        return f"{load:.2f} load"
    except (AttributeError, OSError):
        return "Not available"


def listening_sockets():
    if exists("ss"):
        return run_cmd(["ss", "-lntup"])
    if exists("netstat"):
        return run_cmd(["netstat", "-lntup"])
    return ""


def health_checks():
    commands = ["python", "python3", "git", "curl", "ip", "ss", "pkg", "ssh"]
    return {cmd: exists(cmd) for cmd in commands}


# ==================== SECURITY ENGINE ====================

def scan():
    device = android_info()
    total, available, used, ram_pct = ram_stats()
    st_total, st_used, st_free, storage_pct = storage_stats()
    ssh = ssh_status()
    ip = local_ip()
    dns = dns_servers()

    findings = []
    score = 100

    if ssh.startswith("Running"):
        score -= 15
        findings.append({
            "severity": "MEDIUM",
            "title": "SSH daemon is running",
            "action": "If SSH is not needed, stop the service using your normal Termux/Linux service controls.",
        })
    elif ssh.startswith("Installed"):
        findings.append({
            "severity": "LOW",
            "title": "OpenSSH server is installed",
            "action": "Keep authentication hardened if you intentionally use SSH.",
        })

    if storage_pct >= 90:
        score -= 10
        findings.append({
            "severity": "MEDIUM",
            "title": "Storage usage is very high",
            "action": "Free space before the filesystem becomes unstable.",
        })
    elif storage_pct >= 80:
        score -= 5
        findings.append({
            "severity": "LOW",
            "title": "Storage usage is high",
            "action": "Consider cleaning unused files.",
        })

    if ram_pct >= 90:
        score -= 5
        findings.append({
            "severity": "LOW",
            "title": "Memory usage is high",
            "action": "Close unused applications if the device feels slow.",
        })

    if ip == "Unknown":
        score -= 2
        findings.append({
            "severity": "LOW",
            "title": "Local IP could not be detected",
            "action": "Check the active network connection.",
        })

    if dns == "Unknown":
        score -= 2
        findings.append({
            "severity": "LOW",
            "title": "DNS servers could not be detected",
            "action": "Check network/DNS configuration if name resolution fails.",
        })

    score = max(0, min(100, score))
    rating = (
        "EXCELLENT" if score >= 95 else
        "GOOD" if score >= 85 else
        "MODERATE" if score >= 70 else
        "NEEDS ATTENTION"
    )

    return {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "falcon_version": VERSION,
        "mode": "local-diagnostics",
        "device": device,
        "ram": {
            "total_gb": round(total / 1024, 2) if total else None,
            "available_gb": round(available / 1024, 2) if available else None,
            "used_percent": round(ram_pct, 1),
        },
        "storage": {
            "total_gb": round(st_total / 1024**3, 2) if st_total else None,
            "free_gb": round(st_free / 1024**3, 2) if st_free else None,
            "used_percent": round(storage_pct, 1),
        },
        "battery": battery_info(),
        "cpu": cpu_info(),
        "local_ip": ip,
        "dns": dns,
        "ssh": ssh,
        "packages": package_count(),
        "termux_prefix": os.environ.get("PREFIX", "Not detected"),
        "health": health_checks(),
        "security_score": score,
        "rating": rating,
        "findings": findings,
    }


# ==================== HISTORY / REPORTS ====================

def report_files():
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        return sorted(
            [p for p in REPORT_DIR.glob("FALCON_security_*.json") if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return []


def save_report(result):
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = REPORT_DIR / f"FALCON_security_{stamp}.json"
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        return path
    except OSError:
        return None


def previous_report():
    files = report_files()
    if len(files) < 1:
        return None
    try:
        return json.loads(files[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def score_history(limit=8):
    history = []
    for path in report_files()[:limit]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            history.append((
                data.get("timestamp", "?"),
                data.get("security_score", 0),
            ))
        except (OSError, json.JSONDecodeError):
            pass
    return history


def compare_with_previous(result):
    old = previous_report()
    if not old:
        return None

    old_score = old.get("security_score")
    new_score = result.get("security_score")
    if not isinstance(old_score, int) or not isinstance(new_score, int):
        return None

    return new_score - old_score


def change_detector(result):
    old = previous_report()
    if not old:
        return []

    changes = []

    old_score = old.get("security_score")
    new_score = result.get("security_score")
    if isinstance(old_score, int) and isinstance(new_score, int) and old_score != new_score:
        changes.append(("Security score", f"{old_score}/100 → {new_score}/100"))

    old_ssh = old.get("ssh")
    new_ssh = result.get("ssh")
    if old_ssh != new_ssh:
        changes.append(("SSH", f"{old_ssh} → {new_ssh}"))

    old_ip = old.get("local_ip")
    new_ip = result.get("local_ip")
    if old_ip != new_ip:
        changes.append(("Local IP", f"{old_ip} → {new_ip}"))

    old_dns = old.get("dns")
    new_dns = result.get("dns")
    if old_dns != new_dns:
        changes.append(("DNS", f"{old_dns} → {new_dns}"))

    old_ram = old.get("ram", {}).get("used_percent")
    new_ram = result.get("ram", {}).get("used_percent")
    if isinstance(old_ram, (int, float)) and isinstance(new_ram, (int, float)):
        if abs(new_ram - old_ram) >= 5:
            changes.append(("RAM usage", f"{old_ram:.1f}% → {new_ram:.1f}%"))

    old_storage = old.get("storage", {}).get("used_percent")
    new_storage = result.get("storage", {}).get("used_percent")
    if isinstance(old_storage, (int, float)) and isinstance(new_storage, (int, float)):
        if abs(new_storage - old_storage) >= 5:
            changes.append(("Storage usage", f"{old_storage:.1f}% → {new_storage:.1f}%"))

    return changes


# ==================== SCREENS ====================

def dashboard():
    result = scan()
    header("LIVE DASHBOARD", "Local device status overview")

    total, available, used, ram_pct = ram_stats()
    st_total, st_used, st_free, storage_pct = storage_stats()

    print()
    print(c("  SECURITY", accent(), True))
    print(f"  Score       : {c(str(result['security_score']) + '/100', GREEN if result['security_score'] >= 85 else YELLOW, True)}")
    print(f"  Rating      : {result['rating']}")
    print()

    print(c("  SYSTEM", accent(), True))
    print(f"  Device      : {result['device'].get('Device', 'Unknown')}")
    print(f"  Android     : {result['device'].get('Android', 'Unknown')}")
    print(f"  Patch       : {result['device'].get('Security Patch', 'Unknown')}")
    print(f"  CPU         : {result['cpu']}")
    print(f"  Battery     : {result['battery']}")
    print()

    if total:
        print(f"  RAM         : {bar(ram_pct)} {ram_pct:5.1f}%")
    if st_total:
        print(f"  Storage     : {bar(storage_pct)} {storage_pct:5.1f}%")

    print()
    print(c("  NETWORK", accent(), True))
    print(f"  Local IP    : {result['local_ip']}")
    print(f"  DNS         : {result['dns']}")
    print(f"  SSH         : {result['ssh']}")

    print()
    print(c("  FALCON", accent(), True))
    print(f"  Reports     : {len(report_files())}")
    print(f"  Theme       : {SETTINGS['theme']}")
    print(f"  Instagram   : @sinanzzyy")

    pause()


def full_scan_screen():
    header("FULL SECURITY SCAN", "Checking local device configuration")
    print()
    print(c("  Running diagnostics...", CYAN))
    result = scan()
    time.sleep(0.25)

    print()
    print(c(f"  SECURITY SCORE  {result['security_score']}/100", GREEN if result["security_score"] >= 85 else YELLOW, True))
    print(c(f"  {result['rating']}", WHITE, True))
    print()

    delta = compare_with_previous(result)
    if delta is not None:
        arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        color = GREEN if delta > 0 else RED if delta < 0 else CYAN
        print(c(f"  Previous score: {result['security_score'] - delta}/100  {arrow}  {delta:+d}", color))

    if result["findings"]:
        print()
        print(c("  FINDINGS", MAGENTA, True))
        for item in result["findings"]:
            color = RED if item["severity"] == "HIGH" else YELLOW if item["severity"] == "MEDIUM" else CYAN
            print()
            print(c(f"  [{item['severity']}] {item['title']}", color, True))
            print(c(f"      → {item['action']}", WHITE))

    path = save_report(result)
    if path:
        print(c(f"\n  ✓ Report saved: {path}", GREEN))
    else:
        print(c("\n  ⚠ Could not save report.", YELLOW))

    pause()


def history_screen():
    header("SCAN HISTORY", "Recent FALCON security scores")
    history = score_history()

    if not history:
        print(c("\n  No scan history yet.", YELLOW))
        pause()
        return

    print()
    for timestamp, score in reversed(history):
        stamp = timestamp.replace("T", " ")[:19]
        print(f"  {stamp}  {bar(score, 18)}  {score:3}/100")

    if len(history) >= 2:
        newest = history[0][1]
        oldest = history[-1][1]
        diff = newest - oldest
        print()
        print(c(f"  Trend: {diff:+d} points", GREEN if diff >= 0 else RED, True))

    pause()


def reports_screen():
    header("REPORT BROWSER", "Saved local JSON reports")
    files = report_files()

    if not files:
        print(c("\n  No reports found.", YELLOW))
        pause()
        return

    print()
    for i, path in enumerate(files[:10], 1):
        print(f"  [{i}] {path.name}")

    print()
    choice = input(c("  Select report (ENTER to back): ", MAGENTA)).strip()
    if not choice:
        return

    if not choice.isdigit() or not 1 <= int(choice) <= min(10, len(files)):
        print(c("  Invalid selection.", YELLOW))
        pause()
        return

    path = files[int(choice) - 1]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        header("REPORT VIEWER", path.name)
        print()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except (OSError, json.JSONDecodeError) as error:
        print(c(f"  Could not read report: {error}", RED))

    pause()


def network_screen():
    header("NETWORK DIAGNOSTICS", "Local interfaces and listening sockets")
    print()
    print(f"  Local IP : {local_ip()}")
    print(f"  DNS      : {dns_servers()}")
    print()

    sockets = listening_sockets()
    if sockets:
        print(c("  LISTENING SOCKETS", YELLOW, True))
        print(sockets)
    else:
        print(c("  Socket information unavailable.", YELLOW))

    print(c("\n  Note: listening services are shown locally; FALCON does not scan external hosts.", CYAN))
    pause()


def health_screen():
    header("HEALTH CENTER", "Required local tools")
    print()

    checks = health_checks()
    for command, available in checks.items():
        print(f"  {status_icon(available)} {command:<10} {'Available' if available else 'Not detected'}")

    total = len(checks)
    good = sum(checks.values())
    print()
    print(c(f"  Tool availability: {good}/{total}", GREEN if good == total else YELLOW, True))
    pause()


def privacy_screen():
    header("PRIVACY CENTER", "FALCON safety boundaries")
    print()
    checks = [
        ("External host scanning", "OFF"),
        ("Password collection", "OFF"),
        ("Credential extraction", "OFF"),
        ("Automatic system changes", "OFF"),
        ("Local JSON reports", "ON"),
        ("External network requests", "Not performed by scanner"),
    ]
    for name, status in checks:
        print(f"  {status_icon(status in ('OFF', 'ON'))} {name:<30} {status}")
    print()
    print(c("  FALCON is a local diagnostics utility.", CYAN))
    pause()



def changes_screen():
    result = scan()
    header("CHANGE DETECTOR", "Current scan compared with the latest saved report")

    changes = change_detector(result)
    print()

    if not previous_report():
        print(c("  No previous report exists yet.", YELLOW))
        print(c("  Run a Full Security Scan first.", CYAN))
    elif not changes:
        print(c("  ✓ No significant changes detected.", GREEN, True))
    else:
        print(c("  CHANGES DETECTED", MAGENTA, True))
        print()
        for name, value in changes:
            print(f"  ⚠ {name:<18} {value}")

    pause()

def self_test():
    header("FALCON SELF-TEST", "Checking core modules")
    tests = []

    try:
        _ = android_info()
        tests.append(("Device detection", True))
    except Exception:
        tests.append(("Device detection", False))

    try:
        _ = ram_stats()
        tests.append(("Memory detection", True))
    except Exception:
        tests.append(("Memory detection", False))

    try:
        _ = storage_stats()
        tests.append(("Storage detection", True))
    except Exception:
        tests.append(("Storage detection", False))

    try:
        _ = dns_servers()
        tests.append(("DNS detection", True))
    except Exception:
        tests.append(("DNS detection", False))

    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        tests.append(("Report directory", True))
    except OSError:
        tests.append(("Report directory", False))

    print()
    for name, ok in tests:
        print(f"  {status_icon(ok)} {name:<24} {'PASS' if ok else 'FAIL'}")

    print()
    passed = sum(ok for _, ok in tests)
    print(c(f"  Result: {passed}/{len(tests)} tests passed", GREEN if passed == len(tests) else YELLOW, True))
    pause()


def settings_screen():
    header("FALCON SETTINGS", "Customize the command center")
    print()
    names = list(THEMES)
    for i, name in enumerate(names, 1):
        marker = "●" if SETTINGS["theme"] == name else "○"
        print(f"  [{i}] {marker} {name}")

    print()
    choice = input(c("  Theme (ENTER to back): ", MAGENTA)).strip()
    if not choice:
        return

    if choice.isdigit() and 1 <= int(choice) <= len(names):
        SETTINGS["theme"] = names[int(choice) - 1]
        save_settings()
        print(c(f"  ✓ Theme changed to {SETTINGS['theme']}", GREEN))
    else:
        print(c("  Invalid theme.", YELLOW))
    time.sleep(0.8)


def instagram_screen():
    header("FALCON SOCIAL", "Falcon by Sinan")
    print()
    print(c("  Instagram profile", MAGENTA, True))
    print("  @sinanzzyy")
    print()
    print(c("  Exact profile URL:", CYAN, True))
    print(f"  {INSTAGRAM_URL}")
    print()

    opened = False

    # Prefer Android's normal VIEW intent. This lets Android choose
    # Instagram when installed, otherwise the browser can handle it.
    if exists("am"):
        intents = [
            ["am", "start", "-a", "android.intent.action.VIEW",
             "-c", "android.intent.category.BROWSABLE", "-d", INSTAGRAM_URL],
            ["am", "start", "-a", "android.intent.action.VIEW", "-d", INSTAGRAM_URL],
        ]

        for command in intents:
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    opened = True
                    break
            except (OSError, subprocess.SubprocessError):
                pass

    # Browser fallback for desktop Linux / Termux environments.
    if not opened:
        try:
            opened = bool(webbrowser.open(INSTAGRAM_URL))
        except Exception:
            opened = False

    print()
    if opened:
        print(c("  ✓ Launch request sent.", GREEN, True))
        print(c("  Android will choose Instagram or your browser.", CYAN))
    else:
        print(c("  ⚠ Automatic launch failed.", YELLOW, True))
        print(c("  Open the exact URL above manually.", WHITE))

    pause()


# ==================== MAIN MENU ====================

def menu():
    while True:
        header("MAIN MENU", "Local security command center")

        result = scan()
        score = result["security_score"]
        score_color = GREEN if score >= 85 else YELLOW if score >= 70 else RED

        print()
        print(c(f"  SECURITY   {score:3}/100   {result['rating']}", score_color, True))
        print(c(f"  DEVICE     {result['device'].get('Device', 'Unknown')}", WHITE))
        print(c(f"  BATTERY    {result['battery']}", WHITE))
        print()

        options = [
            ("1", "Full Security Scan"),
            ("2", "Live Dashboard"),
            ("3", "Network Diagnostics"),
            ("4", "Device Information"),
            ("5", "Health Center"),
            ("6", "Scan History"),
            ("7", "Change Detector"),
            ("8", "Report Browser"),
            ("9", "Privacy Center"),
            ("10", "FALCON Self-Test"),
            ("11", "Settings / Themes"),
            ("12", "Falcon Instagram"),
            ("0", "Exit"),
        ]

        print(c("  ┌────────────────────────────────────────────┐", accent()))
        for key, name in options:
            print(c(f"  │  [{key:>2}]  {name:<37}│", WHITE))
        print(c("  └────────────────────────────────────────────┘", accent()))
        print()

        try:
            choice = input(c("  FALCON@termux > ", MAGENTA, True)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        actions = {
            "1": full_scan_screen,
            "2": dashboard,
            "3": network_screen,
            "4": device_screen,
            "5": health_screen,
            "6": history_screen,
            "7": changes_screen,
            "8": reports_screen,
            "9": privacy_screen,
            "10": self_test,
            "11": settings_screen,
            "12": instagram_screen,
        }

        if choice == "0":
            clear()
            print(c("\n  🦅 FALCON — Falcon by Sinan", CYAN, True))
            print(c("  Stay secure. Stay curious.\n", WHITE))
            return

        action = actions.get(choice)
        if action:
            action()
        else:
            print(c("  Invalid option.", YELLOW))
            time.sleep(0.7)


def device_screen():
    header("DEVICE INFORMATION", "Android and local system details")
    info = android_info()
    total, available, used, ram_pct = ram_stats()
    st_total, st_used, st_free, storage_pct = storage_stats()

    print()
    for key, value in info.items():
        print(f"  {key:<18}: {value}")

    print(f"  {'RAM':<18}: {total/1024:.1f} GB total / {available/1024:.1f} GB available" if total else "  RAM                 : Unknown")
    print(f"  {'Storage':<18}: {st_free/1024**3:.1f} GB free / {st_total/1024**3:.1f} GB total" if st_total else "  Storage             : Unknown")
    print(f"  {'Battery':<18}: {battery_info()}")
    print(f"  {'CPU':<18}: {cpu_info()}")
    print(f"  {'Local IP':<18}: {local_ip()}")
    print(f"  {'DNS':<18}: {dns_servers()}")
    print(f"  {'Packages':<18}: {package_count()}")
    print(f"  {'Termux PREFIX':<18}: {os.environ.get('PREFIX', 'Not detected')}")
    pause()


def main():
    boot()
    menu()


if __name__ == "__main__":
    main()
