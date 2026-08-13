use chrono::Local;
use std::process::Command;

fn main() {
    // Create timestamped filename like Backup-13-08-26-06:48:00
    let timestamp = Local::now().format("%d-%m-%y-%H:%M:%S").to_string();
    let file_name = format!("Backup-{}", timestamp);

    // Paths (replace with your actual paths)
    let source_dir = "/home/vkp/Desktop/bash/";
    let archive_path = format!("{}/{}", source_dir, file_name);
    let remote = "vkp@192.168.43.64:/home/vkp/backups";

    // Create tar archive
    let tar_status = Command::new("tar")
        .args(["-cvf", &archive_path, source_dir])
        .status()
        .expect("Failed to run tar");

    if !tar_status.success() {
        eprintln!("Tar command failed");
        return;
    }

    // Copy archive to remote server
    let scp_status = Command::new("scp")
        .args([&archive_path, remote])
        .status()
        .expect("Failed to run scp");

    if !scp_status.success() {
        eprintln!("SCP command failed");
        return;
    }

    println!("Backup completed: {}", file_name);
}
