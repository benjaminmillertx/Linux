use std::process::Command;
use std::io::{BufRead, BufReader};

fn main() {
    // Step 1: run `gau hackerone.com | grep "=" | qsreplace hack\" -a`
    let gau = Command::new("gau")
        .arg("hackerone.com")
        .output()
        .expect("Failed to run gau");

    let gau_output = String::from_utf8_lossy(&gau.stdout);

    // Filter URLs containing "=" and apply qsreplace
    let mut replaced = Command::new("qsreplace")
        .arg("hack\"")
        .arg("-a")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to run qsreplace");

    {
        use std::io::Write;
        let stdin = replaced.stdin.as_mut().unwrap();
        for line in gau_output.lines() {
            if line.contains("=") {
                writeln!(stdin, "{}", line).unwrap();
            }
        }
    }

    let qs_output = replaced
        .wait_with_output()
        .expect("Failed to read qsreplace output");

    // Step 2: read each URL and check reflection
    let reader = BufReader::new(&qs_output.stdout[..]);

    for line in reader.lines() {
        let url = line.unwrap();

        let curl_output = Command::new("curl")
            .args(["-s", "-l", &url])
            .output()
            .expect("Failed to run curl");

        let body = String::from_utf8_lossy(&curl_output.stdout);

        let reflected = body.contains("hack\"") || body.contains("hack\\\"");

        if reflected {
            println!(
                "Target: {}  [XSS Possible] Reflection found...",
                url
            );
        } else {
            println!("Target: {}", url);
        }
    }
}
