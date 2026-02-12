import subprocess
import os
import sys
import platform
import datetime
import time
import signal
import psutil
# For memory monitoring

# ========== CONFIG ==========
LOG_DIR = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "automation_1hour.log")
INTERVAL_HOURS = 1
INTERVAL_SECONDS = 60 * 60  # 1 hour
SCRIPTS = ["login.py"]
# ============================

def log(msg):
    """Write timestamped log messages safely."""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except UnicodeEncodeError:
        safe_msg = msg.encode("ascii", "ignore").decode()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {safe_msg}\n")
    print(line)

def kill_chrome():
    """Ensure Chrome/Chromedriver processes are cleaned up."""
    try:
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=False)
            subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], check=False)
        else:
            subprocess.run(["pkill", "-f", "chrome"], check=False)
            subprocess.run(["pkill", "-f", "chromedriver"], check=False)
    except Exception as e:
        log(f"⚠️ Chrome cleanup error (ignored): {e}")

def check_memory():
    """Check memory usage to detect leaks."""
    try:
        mem = psutil.virtual_memory()
        log(f"💾 Memory usage: {mem.percent}%")
    except Exception:
        pass

def run_script(name):
    """Run a Python script using the same interpreter."""
    if not os.path.exists(name):
        log(f"❌ Script not found: {name}")
        return 1
    log(f"🚀 Running {name}...")
    result = subprocess.run([sys.executable, name])
    log(f"✅ {name} exited with code {result.returncode}")
    return result.returncode

def graceful_exit(signum, frame):
    log(f"🛑 Received signal {signum}. Shutting down gracefully.")
    sys.exit(0)

# Handle Docker stop signals
signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

def main():
    log("🚀 Automation runner started.")
    check_memory()
    kill_chrome()

    all_ok = True
    for script in SCRIPTS:
        result = run_script(script)
        if result != 0:
            log(f"❌ {script} failed. Stopping sequence.")
            all_ok = False
            break

    if all_ok:
        log("🎉 All scripts executed successfully this run.")
    else:
        log("⚠️ Run completed with some errors.")

    log(f"⏳ Sleeping for {INTERVAL_HOURS} hours before next execution...")
    time.sleep(INTERVAL_SECONDS)

    log("🔁 1 hour completed. Restarting cycle now.")
    os.execv(sys.executable, [sys.executable] + sys.argv)  # restart same script

if __name__ == "__main__":
    main()