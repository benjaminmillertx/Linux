use rand::Rng;

fn main() {
    // Read desired length from command-line args
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <length>", args[0]);
        return;
    }

    let length: usize = args[1].parse().expect("Length must be a number");

    // Character set (same as your Bash MATRIX on bashpasswd punisher.py)
    let matrix = "1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*";

    // Generate password
    let mut rng = rand::thread_rng();
    let mut pass = String::new();

    for _ in 0..length {
        let idx = rng.gen_range(0..matrix.len());
        pass.push(matrix.chars().nth(idx).unwrap());
    }

    println!("{}", pass);
}
