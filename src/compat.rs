use crate::spec_parser;
use serde::Serialize;
use std::{
    env, fs, io,
    path::{Path, PathBuf},
};
#[derive(Serialize)]
struct Root<'a> {
    path: &'a Path,
    source: &'static str,
}
#[derive(Serialize)]
struct Item {
    id: String,
    #[serde(rename = "requirementCount")]
    requirement_count: usize,
}
#[derive(Serialize)]
struct Listing<'a> {
    specs: Vec<Item>,
    root: Root<'a>,
}
#[derive(Serialize)]
struct Show<'a> {
    id: &'a str,
    title: &'a str,
    overview: String,
    #[serde(rename = "requirementCount")]
    requirement_count: usize,
    requirements: Vec<spec_parser::Requirement>,
    metadata: Meta,
    root: Root<'a>,
}
#[derive(Serialize)]
struct Meta {
    version: &'static str,
    format: &'static str,
}
#[derive(Serialize)]
struct Status<'a> {
    severity: &'static str,
    code: &'a str,
    message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    fix: Option<&'a str>,
}
#[derive(Serialize)]
struct ErrorOut<'a> {
    status: Vec<Status<'a>>,
}
#[derive(Serialize)]
struct ListError<'a> {
    specs: Vec<Item>,
    root: Option<Root<'a>>,
    status: Vec<Status<'a>>,
}
fn refuse(s: &str) -> i32 {
    eprintln!("{s}");
    2
}
fn meta(p: &Path) -> io::Result<Option<fs::Metadata>> {
    match fs::symlink_metadata(p) {
        Ok(m) => Ok(Some(m)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}
fn base(k: &str, fallback: &str) -> Result<PathBuf, ()> {
    let v = match env::var_os(k) {
        Some(x) => x,
        None => env::var_os("HOME").ok_or(())?,
    };
    let p = PathBuf::from(&v);
    if !p.is_absolute() || p.to_str().is_none() {
        return Err(());
    }
    let base = if env::var_os(k).is_some() {
        p
    } else {
        p.join(fallback)
    };
    let openspec = base.join("openspec");
    if meta(&openspec).map_err(|_| ())?.is_some() {
        return Err(());
    }
    Ok(base)
}
fn dir(p: &Path) -> Result<bool, ()> {
    match meta(p).map_err(|_| ())? {
        None => Ok(false),
        Some(m) if m.is_dir() && !m.is_symlink() => Ok(true),
        _ => Err(()),
    }
}
fn root() -> Result<Option<PathBuf>, ()> {
    if !cfg!(target_os = "linux") {
        return Err(());
    }
    base("XDG_CONFIG_HOME", ".config")?;
    base("XDG_DATA_HOME", ".local/share")?;
    let cwd = env::current_dir().map_err(|_| ())?;
    if cwd.to_str().is_none() {
        return Err(());
    }
    for a in cwd.ancestors() {
        let o = a.join("openspec");
        if !dir(&o)? {
            continue;
        }
        let y = o.join("config.yaml");
        let yy = o.join("config.yml");
        if meta(&yy).map_err(|_| ())?.is_some() {
            return Err(());
        }
        let y_exists = match meta(&y).map_err(|_| ())? {
            None => false,
            Some(m) if m.is_file() && !m.is_symlink() => {
                if fs::read(&y).map_err(|_| ())? != b"schema: spec-driven\n" {
                    return Err(());
                }
                true
            }
            _ => return Err(()),
        };
        let mut qualified = y_exists;
        for x in ["specs", "changes"] {
            let p = o.join(x);
            if dir(&p)? {
                qualified = true;
                if meta(&p.join(".openspec-store")).map_err(|_| ())?.is_some() {
                    return Err(());
                }
            }
        }
        if !qualified && meta(&o.join("project.md")).map_err(|_| ())?.is_some() {
            return Err(());
        }
        if qualified {
            return Ok(Some(a.to_path_buf()));
        }
    }
    Ok(None)
}
fn err(cmd: &str, json: bool, msg: String, fix: Option<&'static str>) -> i32 {
    let status = Status {
        severity: "error",
        code: if cmd == "list" {
            "list_error"
        } else {
            "show_error"
        },
        message: msg.clone(),
        fix,
    };
    if json {
        if cmd == "list" {
            println!(
                "{}",
                serde_json::to_string_pretty(&ListError {
                    specs: vec![],
                    root: None,
                    status: vec![status]
                })
                .unwrap()
            )
        } else {
            println!(
                "{}",
                serde_json::to_string_pretty(&ErrorOut {
                    status: vec![status]
                })
                .unwrap()
            )
        }
    } else {
        eprintln!("✖ Error: {msg}");
        if let Some(f) = fix {
            eprintln!("Fix: {f}")
        }
    }
    1
}
fn walk(dir: &Path, root: &Path, ids: &mut Vec<(String, PathBuf)>) -> Result<(), String> {
    let entries = match fs::read_dir(dir) {
        Ok(x) => x,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(()),
        Err(e) if e.kind() == io::ErrorKind::PermissionDenied => {
            return Err(format!(
                "EACCES: permission denied, scandir '{}'",
                dir.display()
            ));
        }
        Err(_) => return Err("unsupported filesystem error".into()),
    };
    for e in entries {
        let e = e.map_err(|_| "unsupported filesystem error")?;
        let n = e.file_name();
        if n.to_string_lossy().starts_with('.') {
            continue;
        }
        let p = e.path();
        let t = e.file_type().map_err(|_| "unsupported filesystem error")?;
        if t.is_dir() {
            walk(&p, root, ids)?
        } else if n == "spec.md" && dir != root && (t.is_file() || t.is_symlink()) {
            if !p.exists() {
                continue;
            }
            if !fs::metadata(&p)
                .map_err(|_| "unsupported filesystem error")?
                .is_file()
            {
                continue;
            }
            let real = fs::canonicalize(&p).map_err(|_| "unsupported filesystem error")?;
            let project = root
                .parent()
                .and_then(Path::parent)
                .ok_or("unsupported filesystem error")?;
            if !real.starts_with(project) {
                return Err(format!(
                    "Path is outside the allowed directory: {}",
                    p.display()
                ));
            }
            let id = dir
                .strip_prefix(root)
                .map_err(|_| "unsupported filesystem error")?
                .to_str()
                .ok_or("unsupported spec identifier ordering")?
                .to_string();
            ids.push((id, p));
        }
    }
    Ok(())
}
fn safe_ids(ids: &[(String, PathBuf)]) -> bool {
    let valid = ids.iter().all(|(s, _)| {
        s.split('/')
            .all(|x| !x.is_empty() && x.bytes().all(|b| b.is_ascii_lowercase()))
    });
    valid && (ids.len() <= 1 || ids.iter().all(|(s, _)| !s.contains('/')))
}
fn read(p: &Path) -> io::Result<String> {
    Ok(String::from_utf8_lossy(&fs::read(p)?).into_owned())
}
pub fn run(cmd: &str, id: Option<&str>, json: bool) -> i32 {
    let root = match root() {
        Ok(x) => x,
        Err(_) => return refuse("unsupported root selection"),
    };
    let cwd = env::current_dir().unwrap();
    if root.is_none() && cmd == "list" {
        let m = "No OpenSpec root found from the current directory.";
        let f = "Run openspec init to create a root here.";
        if json {
            #[derive(Serialize)]
            struct NoRootStatus {
                severity: &'static str,
                code: &'static str,
                message: &'static str,
                target: &'static str,
                fix: &'static str,
            }
            #[derive(Serialize)]
            struct O {
                specs: Vec<Item>,
                root: Option<Root<'static>>,
                status: Vec<NoRootStatus>,
            }
            println!(
                "{}",
                serde_json::to_string_pretty(&O {
                    specs: vec![],
                    root: None,
                    status: vec![NoRootStatus {
                        severity: "error",
                        code: "no_openspec_root",
                        message: m,
                        target: "openspec.root",
                        fix: f
                    }]
                })
                .unwrap()
            )
        } else {
            eprintln!("✖ Error: {m}\nFix: {f}")
        }
        return 1;
    }
    let project = root.as_ref().unwrap_or(&cwd);
    let specs = project.join("openspec/specs");
    let mut ids = Vec::new();
    if let Err(e) = walk(&specs, &specs, &mut ids) {
        if e == "unsupported filesystem error" {
            return refuse(&e);
        }
        return err(cmd, json, e, None);
    }
    ids.sort_by(|a, b| a.0.cmp(&b.0));
    if cmd == "list" && !safe_ids(&ids) {
        return refuse("unsupported spec identifier ordering");
    }
    if cmd == "list" {
        let mut entries = Vec::new();
        for (id, p) in ids {
            let n = read(&p)
                .ok()
                .and_then(|s| spec_parser::parse(&s).ok())
                .map(|x| x.1.len())
                .unwrap_or(0);
            entries.push(Item {
                id,
                requirement_count: n,
            })
        }
        if json {
            println!(
                "{}",
                serde_json::to_string_pretty(&Listing {
                    specs: entries,
                    root: Root {
                        path: project,
                        source: "nearest"
                    }
                })
                .unwrap()
            )
        } else if entries.is_empty() {
            println!("No specs found.")
        } else {
            println!("Specs:");
            let width = entries.iter().map(|e| e.id.len()).max().unwrap_or(0);
            for e in entries {
                println!("  {:width$}     requirements {}", e.id, e.requirement_count)
            }
        }
        return 0;
    }
    let id = id.unwrap();
    if id.starts_with("../") || id == ".." || id.starts_with('/') {
        let mut path = specs.clone();
        for part in id.split('/') {
            if part == ".." {
                path.pop();
            } else if !part.is_empty() && part != "." {
                path.push(part);
            }
        }
        path.push("spec.md");
        return err(
            cmd,
            json,
            format!("Path is outside the allowed directory: {}", path.display()),
            None,
        );
    }
    if id
        .split('/')
        .any(|s| s.is_empty() || !s.bytes().all(|b| b.is_ascii_lowercase()))
    {
        return refuse("unsupported spec identifier");
    }
    let path = specs.join(id).join("spec.md");
    if fs::symlink_metadata(&path).is_ok_and(|m| m.file_type().is_symlink()) && !path.exists() {
        return err(
            cmd,
            json,
            format!("Cannot verify dangling symbolic link: {}", path.display()),
            None,
        );
    }
    if path.exists() {
        if !fs::metadata(&path).is_ok_and(|m| m.is_file()) {
            return refuse("unsupported filesystem error");
        }
        let file_real = match fs::canonicalize(&path) {
            Ok(x) => x,
            Err(_) => return refuse("unsupported filesystem error"),
        };
        let parent_real = match fs::canonicalize(path.parent().unwrap()) {
            Ok(x) => x,
            Err(_) => return refuse("unsupported filesystem error"),
        };
        let specs_real = match fs::canonicalize(&specs) {
            Ok(x) => x,
            Err(_) => return refuse("unsupported filesystem error"),
        };
        // Upstream accepts a selected capability directory as its own trust root.
        // The project-wide fallback applies only to a final file symlink whose
        // parent itself resolves within the canonical specs root.
        if !file_real.starts_with(&specs_real) && !file_real.starts_with(&parent_real) {
            let is_file_link =
                fs::symlink_metadata(&path).is_ok_and(|m| m.file_type().is_symlink());
            let denied = if is_file_link && !parent_real.starts_with(&specs_real) {
                Some(path.parent().unwrap())
            } else if !is_file_link || !file_real.starts_with(project) {
                Some(path.as_path())
            } else {
                None
            };
            if let Some(denied) = denied {
                return err(
                    cmd,
                    json,
                    format!(
                        "Path is outside the allowed directory: {}",
                        denied.display()
                    ),
                    None,
                );
            }
        }
    }
    if !path.exists() {
        return err(
            cmd,
            json,
            format!("Spec '{id}' not found at {}", path.display()),
            None,
        );
    }
    let content = match read(&path) {
        Ok(x) => x,
        Err(_) => return refuse("unsupported filesystem error"),
    };
    if !json {
        println!("{content}");
        return 0;
    }
    match spec_parser::parse(&content) {
        Ok((overview, requirements)) => {
            println!(
                "{}",
                serde_json::to_string_pretty(&Show {
                    id,
                    title: id,
                    overview,
                    requirement_count: requirements.len(),
                    requirements,
                    metadata: Meta {
                        version: "1.0.0",
                        format: "openspec"
                    },
                    root: Root {
                        path: project,
                        source: "nearest"
                    }
                })
                .unwrap()
            );
            0
        }
        Err(e) => err(cmd, json, e.into(), None),
    }
}
