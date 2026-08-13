use std::fs;
use std::process::Command;

fn main() {
    // Threshold
    let trigger: f32 = 1.00;

    // Read /proc/loadavg
    let loadavg = fs::read_to_string("/proc/loadavg")
        .expect("Failed to read /proc/loadavg");

    // First field = 1‑minute load average
    let load_str = loadavg.split_whitespace().next().unwrap();
    let load: f32 = load_str.parse().expect("Failed to parse load average");

    // Compare
    if load > trigger {
        // Run sar -q
        let sar_output = Command::new("sar")
            .arg("-q")
            .output()
            .expect("Failed to run sar");

        // Pipe into mail
        let mut mail = Command::new("mail")
            .args([
                "-s",
                &format!("High server load - [ {} ]", load),
                "parrotngrok143@gmail.com",
            ])
            .stdin(std::process::Stdio::piped())
            .spawn()
            .expect("Failed to start mail command");

        if let Some(stdin) = mail.stdin.as_mut() {
            use std::io::Write;
            stdin.write_all(&sar_output.stdout).unwrap();
        }

        mail.wait().expect("Failed to send mail");

        println!("Alert sent: load = {}", load);
    } else {
        println!("Load normal: {}", load);
    }
}
