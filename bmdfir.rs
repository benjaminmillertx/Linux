# =========================
# Toolset: Japanese/Russian -Inspired DFIR Utilities
# License: GNU General Public License v3.0
# Author: Benjamin Hunter Miller
# =========================
# This suite of tools is released under the GNU General Public License v3.0.
# Made by Benjamin Hunter Miller as part of the GNU Project.
# You are free to run, study, share, and modify this software under the terms
# of the license. Full license details: https://www.gnu.org/licenses/gpl-3.0.html
# =========================
# Tool 1: FoxGate
# =========================
# Rust (memory_acquire.rs)
/* Save this as memory_acquire.rs and compile with: rustc memory_acquire.rs */
use std::fs::File;
use std::io::Read;
use std::fs::OpenOptions;

fn main() {
    let mut src = File::open("/dev/mem").expect("Failed to open /dev/mem");
    let mut dst = OpenOptions::new()
        .create(true)
        .write(true)
        .open("memory_dump.bin")
        .expect("Failed to create dump file");

    std::io::copy(&mut src, &mut dst).expect("Failed to copy memory");
}

# Python (foxgate.py)
import subprocess
import paramiko

print("[FoxGate] Acquiring memory dump via Rust binary...")
subprocess.run(["./memory_acquire"])

print("[FoxGate] Sending dump to remote analyst node...")
sftp_host = "10.0.0.5"
sftp_user = "analyst"
sftp_pass = "hunter2"

ssh = paramiko.Transport((sftp_host, 22))
ssh.connect(username=sftp_user, password=sftp_pass)
sftp = ssh.open_sftp()
sftp.put("memory_dump.bin", "/home/analyst/memory_dump.bin")
sftp.close()
ssh.close()

# =========================
# Tool 2: PathSage
# =========================
# Rust (logparser.rs)
/* Compile with: rustc logparser.rs */
use std::fs;
fn main() {
    let logs = fs::read_to_string("/var/log/audit/audit.log").expect("Cannot read audit log");
    fs::write("events.db", logs).expect("Cannot write event DB");
}

# Python (pathsage.py)
from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)
@app.route("/")
def index():
    with open("events.db") as f:
        events = f.read().splitlines()[:100]
    return render_template_string("""
    <h1>Event Timeline</h1><ul>
    {% for e in events %}<li>{{ e }}</li>{% endfor %}
    </ul>
    """, events=events)

if __name__ == '__main__':
    app.run(port=8080)

# =========================
# Tool 3: RootScope
# =========================
# Rust (rootscan.rs)
/* Compile with: rustc rootscan.rs */
fn main() {
    println!("Scanning syscall table...");
    // Simulated syscall table check (mock)
    println!("Syscall 0x80 points to suspicious addr");
    std::fs::write("rootscope_report.txt", "Suspicious syscall found\n").unwrap();
}

# Python (rootscope.py)
print("[RootScope] Running kernel scan...")
subprocess.run(["./rootscan"])

with open("rootscope_report.txt") as f:
    print("[RootScope Report]\n" + f.read())

# =========================
# Tool 4: ShadowNet
# =========================
# Rust (sniffer.rs)
/* Requires libpcap-dev, compile with: cargo build --release */
use pcap::{Capture, Device};
fn main() {
    let mut cap = Capture::from_device(Device::lookup().unwrap()).unwrap().open().unwrap();
    let mut file = std::fs::File::create("packets.log").unwrap();
    while let Ok(packet) = cap.next() {
        use std::io::Write;
        writeln!(file, "{:?}", packet).unwrap();
    }
}

# Python (shadownet.py)
print("[ShadowNet] Running Rust sniffer...")
subprocess.Popen(["./sniffer"])

print("[ShadowNet] Monitoring traffic in packets.log")

# =========================
# Tool 5: Baptize
# =========================
# Rust (disk_clone.rs)
/* Compile with: rustc disk_clone.rs */
use std::fs::File;
use std::io::copy;

fn main() {
    let mut src = File::open("/dev/sda").unwrap();
    let mut dst = File::create("image.dd").unwrap();
    copy(&mut src, &mut dst).unwrap();
}

# Python (baptize.py)
print("[Baptize] Imaging /dev/sda...")
subprocess.run(["./disk_clone"])

print("[Baptize] Securely wiping logs...")
subprocess.run(["shred", "-u", "~/.bash_history"])
print("Done. Ejecting.")
subprocess.run(["eject"])

# Tool 1: KageSnap ("Shadow Snapshot")
# =========================
# Python script to snapshot running processes and connections
import subprocess
import datetime

def snapshot_system():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"kagesnap_{timestamp}.txt", "w") as f:
        f.write("--- Running Processes ---\n")
        f.write(subprocess.getoutput("ps aux"))
        f.write("\n\n--- Active Network Connections ---\n")
        f.write(subprocess.getoutput("ss -tulpan"))

if __name__ == "__main__":
    print("[KageSnap] Capturing snapshot...")
    snapshot_system()
    print("[KageSnap] Snapshot saved.")

# =========================
# Tool 2: TsuruTrace ("Crane Trace")
# =========================
# Rust tool to walk process trees and dump ancestry
/* tsurutrace.rs */
use std::process::Command;
fn main() {
    let out = Command::new("pstree").arg("-p").output().unwrap();
    std::fs::write("tsuru_tree.txt", out.stdout).unwrap();
    println!("[TsuruTrace] Process tree written to tsuru_tree.txt");
}

# =========================
# Tool 3: KatanaWatch ("Sword Monitor")
# =========================
# Python service to watch for privilege escalation attempts
import time
import os
import pwd

print("[KatanaWatch] Monitoring for UID changes...")
prev_uids = {}
while True:
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            uid = os.stat(f"/proc/{pid}").st_uid
            if pid in prev_uids and uid != prev_uids[pid]:
                print(f"[KatanaWatch] UID change detected in PID {pid}")
            prev_uids[pid] = uid
        except Exception:
            continue
    time.sleep(5)

# =========================
# Tool 4: KaminariCap ("Thunder Capture")
# =========================
# Rust + Python packet logger with timestamp headers
/* kaminari.rs */
use pcap::{Capture, Device};
use std::io::Write;
fn main() {
    let mut cap = Capture::from_device(Device::lookup().unwrap()).unwrap().open().unwrap();
    let mut f = std::fs::File::create("kaminari_packets.txt").unwrap();
    while let Ok(pkt) = cap.next() {
        writeln!(f, "{} bytes: {:?}", pkt.header.len, pkt.data).unwrap();
    }
}

# =========================
# Tool 5: YureiClean ("Ghost Cleaner")
# =========================
# Python cleaner for temp, bash history, cache
import os
import shutil

print("[YureiClean] Purging system artifacts...")
shutil.rmtree("/tmp", ignore_errors=True)
os.system("rm -f ~/.bash_history")
os.system("rm -rf ~/.cache/*")
print("[YureiClean] Complete. No trace remains.")

