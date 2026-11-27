mod compat;
mod native;
mod spec_parser;
use clap::{Parser, Subcommand};
use serde_json::json;
use std::path::PathBuf;

#[derive(Parser)]
#[command(
    name = "pentapro",
    version,
    about = "Local PentaPRO specification tools"
)]
struct Cli {
    #[arg(long, global = true)]
    root: Option<PathBuf>,
    #[arg(long, global = true)]
    json: bool,
    #[command(subcommand)]
    command: Command,
}
#[derive(Subcommand)]
enum Command {
    Init,
    New { name: String },
    List,
    Show { name: String },
    Validate { name: Option<String> },
}
fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.first().is_some_and(|x| x == "compat") {
        std::process::exit(compat_cli(&args));
    }
    if args.iter().any(|x| x == "compat") {
        eprintln!("unsupported compatibility syntax");
        std::process::exit(2);
    }
    let cli = Cli::parse();
    let command = match &cli.command {
        Command::Init => "init",
        Command::New { .. } => "new",
        Command::List => "list",
        Command::Show { .. } => "show",
        Command::Validate { .. } => "validate",
    };
    let result = native::run(cli.root.as_deref(), cli.command);
    match result {
        Ok((data, valid)) => {
            if cli.json {
                println!(
                    "{}",
                    json!({"schema_version": 1, "command": command, "data": data})
                );
            } else {
                native::print_human(command, &data);
            }
            if !valid {
                std::process::exit(1);
            }
        }
        Err(e) => {
            if cli.json {
                eprintln!(
                    "{}",
                    json!({"schema_version": 1, "command": command, "error": {"code": e.code, "message": e.message}})
                );
            } else {
                eprintln!("{}: {}", e.code, e.message);
            }
            std::process::exit(1);
        }
    }
}

fn compat_cli(args: &[String]) -> i32 {
    if args == ["compat", "--help"] || args == ["compat", "openspec", "--help"] {
        println!("Usage: pentapro compat openspec <list --specs|show ID --type spec> [--json]");
        return 0;
    }
    if args.len() < 3 || args[1] != "openspec" {
        eprintln!("unsupported compatibility syntax");
        return 2;
    }
    let cmd = &args[2];
    let mut json = false;
    let mut specs = false;
    let mut typ = false;
    let mut id = None;
    let mut i = 3;
    while i < args.len() {
        match args[i].as_str() {
            "--json" if !json => json = true,
            "--specs" if !specs => specs = true,
            "--type" if !typ && i + 1 < args.len() && args[i + 1] == "spec" => {
                typ = true;
                i += 1
            }
            x if cmd == "show" && id.is_none() && !x.starts_with('-') => id = Some(x),
            _ => {
                eprintln!("unsupported compatibility syntax");
                return 2;
            }
        }
        i += 1;
    }
    match cmd.as_str() {
        "list" if specs && !typ && id.is_none() => compat::run("list", None, json),
        "show" if typ && !specs && id.is_some() => compat::run("show", id, json),
        _ => {
            eprintln!("unsupported compatibility command or syntax");
            2
        }
    }
}
