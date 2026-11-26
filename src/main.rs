mod native;
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
