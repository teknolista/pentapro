#[path = "manifest.rs"]
mod manifest;
use crate::Command;
use serde::Serialize;
use serde_json::{Value, json};
use std::{
    collections::BTreeMap,
    fs,
    io::{self, Write},
    path::{Component, Path, PathBuf},
};

const FILES: [&str; 6] = [
    "change.md",
    "process.md",
    "product.md",
    "production.md",
    "project.md",
    "proof.md",
];
const PILLARS: [&str; 5] = ["product", "project", "production", "proof", "process"];
const LOCK: &str = ".pentapro-engine.lock";

#[derive(Debug)]
pub struct Error {
    pub code: &'static str,
    pub message: String,
}
type Result<T> = std::result::Result<T, Error>;
fn error(code: &'static str, message: impl Into<String>) -> Error {
    Error {
        code,
        message: message.into(),
    }
}
fn io_error(path: &Path, e: io::Error) -> Error {
    error("io-error", format!("{}: {e}", path.display()))
}
fn metadata(path: &Path) -> Result<Option<fs::Metadata>> {
    match fs::symlink_metadata(path) {
        Ok(m) => Ok(Some(m)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(io_error(path, e)),
    }
}
fn safe_dir(path: &Path) -> Result<bool> {
    match metadata(path)? {
        None => Ok(false),
        Some(m) if m.file_type().is_symlink() || !m.is_dir() => Err(error(
            "unsafe-path",
            format!("Expected a real directory: {}", path.display()),
        )),
        Some(_) => Ok(true),
    }
}
fn safe_file(path: &Path) -> Result<bool> {
    match metadata(path)? {
        None => Ok(false),
        Some(m) if m.file_type().is_symlink() || !m.is_file() => Err(error(
            "unsafe-path",
            format!("Expected a regular file: {}", path.display()),
        )),
        Some(_) => Ok(true),
    }
}
fn validate_name(name: &str) -> Result<()> {
    let parts: Vec<_> = name.split('-').collect();
    if !(2..=3).contains(&parts.len())
        || parts
            .iter()
            .any(|p| p.is_empty() || !p.bytes().all(|b| b.is_ascii_lowercase()))
    {
        return Err(error(
            "invalid-name",
            "Change names must contain two or three lowercase words separated by hyphens",
        ));
    }
    Ok(())
}
fn root(requested: Option<&Path>, init: bool) -> Result<PathBuf> {
    let path = match requested {
        Some(p) => p.to_path_buf(),
        None => std::env::current_dir().map_err(|e| error("io-error", e.to_string()))?,
    };
    // Check components in operating-system traversal order before canonicalization.
    // In particular, `link/..` must check `link` before moving to its parent.
    #[cfg(windows)]
    if !path.is_absolute() && matches!(path.components().next(), Some(Component::Prefix(_))) {
        return Err(error(
            "unsafe-path",
            "Drive-relative roots are unsupported; supply an absolute root",
        ));
    }
    let mut checked = if path.is_absolute() {
        PathBuf::new()
    } else {
        std::env::current_dir().map_err(|e| error("io-error", e.to_string()))?
    };
    for component in path.components() {
        checked.push(component.as_os_str());
        // On Windows a standalone drive prefix does not yet name a directory.
        if matches!(component, Component::Prefix(_) | Component::CurDir) {
            continue;
        }
        if !safe_dir(&checked)? {
            return Err(error(
                "project-not-found",
                format!("Root does not exist: {}", path.display()),
            ));
        }
    }
    let abs = fs::canonicalize(&path).map_err(|e| io_error(&path, e))?;
    if init || requested.is_some() {
        if !init && !safe_dir(&abs.join("pentapro"))? {
            return Err(error(
                "project-not-found",
                "No pentapro directory; run init first",
            ));
        }
        return Ok(abs);
    }
    for dir in abs.ancestors() {
        let candidate = dir.join("pentapro");
        match metadata(&candidate)? {
            Some(m) if m.file_type().is_symlink() => {
                return Err(error(
                    "unsafe-path",
                    format!("Symlinked specification marker: {}", candidate.display()),
                ));
            }
            Some(m) if m.is_dir() => return Ok(dir.to_path_buf()),
            _ => {} // A regular file is not a specification directory marker.
        }
    }
    Err(error(
        "project-not-found",
        "No pentapro directory found; run init or provide --root",
    ))
}
struct Lock {
    path: PathBuf,
}
impl Lock {
    fn acquire(root: &Path) -> Result<Self> {
        let path = root.join(LOCK);
        let mut f = fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)
            .map_err(|e| {
                if e.kind() == io::ErrorKind::AlreadyExists {
                    error(
                        "locked",
                        format!(
                            "Operation lock exists: {} (inspect before recovery)",
                            path.display()
                        ),
                    )
                } else {
                    io_error(&path, e)
                }
            })?;
        writeln!(f, "pid={}", std::process::id()).map_err(|e| io_error(&path, e))?;
        Ok(Self { path })
    }
}
impl Drop for Lock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.path);
    }
}
fn ensure_dirs(root: &Path, rels: &[&str]) -> Result<()> {
    for rel in rels {
        safe_dir(&root.join(rel))?;
    }
    for rel in rels {
        let p = root.join(rel);
        if !p.exists() {
            fs::create_dir(&p).map_err(|e| io_error(&p, e))?;
        }
    }
    Ok(())
}
fn title(s: &str) -> String {
    s.split('-')
        .map(|w| {
            let mut c = w.chars();
            c.next()
                .map(|f| f.to_uppercase().collect::<String>() + c.as_str())
                .unwrap_or_default()
        })
        .collect::<Vec<_>>()
        .join(" ")
}
fn init(root: &Path) -> Result<Value> {
    let dirs = [
        "pentapro",
        "pentapro/product",
        "pentapro/project",
        "pentapro/production",
        "pentapro/proof",
        "pentapro/process",
        "pentapro/assets",
        "pentapro/changes",
        "pentapro/changes/archive",
    ];
    let mut items: Vec<(String,String)> = manifest::TOPICS.iter().map(|(p,purpose)| { let (pillar,file)=p.split_once('/').expect("manifest"); let stem=file.strip_suffix(".md").expect("manifest"); (format!("pentapro/{p}"),format!("# {} · {}\n\nPurpose: {purpose}\n\nStatus: Pending project-specific specification.\n",pillar.to_uppercase(),title(stem))) }).collect();
    items.extend([
      ("pentapro/README.md".into(), "# PentaPRO specification\n\nRead [PROCESS](process/index.md) for scope, and [changes](changes/) for active work.\n".into()),
      ("pentapro/assets/README.md".into(), "# Specification assets\n\nRecord supporting asset sources and rights. See the [specification](../README.md).\n".into()),
      ("pentapro/changes/README.md".into(), "# Active changes\n\nRecord active changes here; completed changes belong in [archive](archive/).\n".into()),
      ("pentapro/changes/archive/README.md".into(), "# Archived changes\n\nKeep completed or cancelled changes with their date. See [active changes](../).\n".into())]);
    items.sort_by(|a, b| a.0.cmp(&b.0));
    for d in dirs {
        safe_dir(&root.join(d))?;
    }
    for (p, _) in &items {
        safe_file(&root.join(p))?;
    }
    ensure_dirs(root, &dirs)?;
    let (mut created, mut preserved) = (Vec::new(), Vec::new());
    for (p, content) in items {
        let full = root.join(&p);
        match fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&full)
        {
            Ok(mut f) => {
                f.write_all(content.as_bytes())
                    .map_err(|e| io_error(&full, e))?;
                created.push(p);
            }
            Err(e) if e.kind() == io::ErrorKind::AlreadyExists => {
                safe_file(&full)?;
                preserved.push(p);
            }
            Err(e) => return Err(io_error(&full, e)),
        }
    }
    Ok(json!({"created":created,"preserved":preserved}))
}
fn changes_path(root: &Path) -> Result<PathBuf> {
    let p = root.join("pentapro/changes");
    if !safe_dir(&p)? {
        return Err(error(
            "project-not-found",
            "Missing pentapro/changes; run init first",
        ));
    }
    Ok(p)
}
fn entries(path: &Path) -> Result<Vec<String>> {
    let mut v = Vec::new();
    for entry in fs::read_dir(path).map_err(|e| io_error(path, e))? {
        let e = entry.map_err(|e| io_error(path, e))?;
        let name = e
            .file_name()
            .into_string()
            .map_err(|_| error("invalid-content", "Non-UTF-8 entry in changes"))?;
        if name == "archive" || name == "README.md" || name.starts_with('.') {
            continue;
        }
        let m = fs::symlink_metadata(e.path()).map_err(|x| io_error(&e.path(), x))?;
        if m.file_type().is_symlink() {
            return Err(error(
                "unsafe-path",
                format!("Symlinked change: {}", e.path().display()),
            ));
        }
        if m.is_dir() {
            validate_name(&name)?;
            v.push(name);
        }
    }
    v.sort();
    Ok(v)
}
fn new_change(root: &Path, name: &str) -> Result<Value> {
    validate_name(name)?;
    let changes = changes_path(root)?;
    let archive = changes.join("archive");
    if !safe_dir(&archive)? {
        return Err(error(
            "project-not-found",
            "Missing archive directory; run init first",
        ));
    }
    let dest = changes.join(name);
    if metadata(&dest)?.is_some() {
        return Err(error(
            "already-exists",
            format!("Change already exists: {name}"),
        ));
    }
    for e in fs::read_dir(&archive).map_err(|e| io_error(&archive, e))? {
        let e = e.map_err(|e| io_error(&archive, e))?;
        let filename = e.file_name();
        let n = filename.to_string_lossy();
        if n.split_once('_').is_some_and(|(_, id)| id == name) {
            return Err(error(
                "already-exists",
                format!("Archived change identity already exists: {name}"),
            ));
        }
    }
    let stage = changes.join(format!(".pentapro-stage-{}", std::process::id()));
    fs::create_dir(&stage).map_err(|e| {
        if e.kind() == io::ErrorKind::AlreadyExists {
            error(
                "locked",
                format!("Staging path exists: {}", stage.display()),
            )
        } else {
            io_error(&stage, e)
        }
    })?;
    for f in FILES {
        let p = stage.join(f);
        let body = if f == "change.md" {
            format!(
                "# Change: {name}\n\nStatus: Draft\n\nRecord project-specific change details here.\n"
            )
        } else {
            format!(
                "# {} · Change\n\nStatus: Pending\n\nRecord project-specific details here.\n",
                f.trim_end_matches(".md").to_uppercase()
            )
        };
        fs::write(&p, body).map_err(|e| io_error(&p, e))?;
    }
    if metadata(&dest)?.is_some() {
        return Err(error(
            "already-exists",
            format!("Change already exists: {name}"),
        ));
    }
    fs::rename(&stage, &dest).map_err(|e| io_error(&dest, e))?;
    Ok(json!({"name":name,"path":format!("pentapro/changes/{name}"),"files":FILES}))
}
fn show(root: &Path, name: &str) -> Result<Value> {
    validate_name(name)?;
    let p = changes_path(root)?.join(name);
    if !safe_dir(&p)? {
        return Err(error("not-found", format!("Change not found: {name}")));
    }
    let mut files = BTreeMap::new();
    for f in FILES {
        let file = p.join(f);
        if !safe_file(&file)? {
            return Err(error(
                "not-found",
                format!("Required file missing: {}", file.display()),
            ));
        }
        let content = fs::read_to_string(&file).map_err(|e| {
            if e.kind() == io::ErrorKind::InvalidData {
                error(
                    "invalid-content",
                    format!("Invalid UTF-8: {}", file.display()),
                )
            } else {
                io_error(&file, e)
            }
        })?;
        files.insert(f, content);
    }
    Ok(json!({"name":name,"files":files}))
}
#[derive(Serialize)]
struct Diagnostic {
    code: &'static str,
    path: String,
    message: String,
}
fn diagnostic(out: &mut Vec<Diagnostic>, code: &'static str, path: String, message: &str) {
    out.push(Diagnostic {
        code,
        path,
        message: message.into(),
    });
}
fn inspect_dir(root: &Path, rel: &str, out: &mut Vec<Diagnostic>) -> bool {
    match safe_dir(&root.join(rel)) {
        Ok(true) => true,
        Ok(false) => {
            diagnostic(
                out,
                "missing-directory",
                rel.into(),
                "Required directory is missing",
            );
            false
        }
        Err(e) => {
            diagnostic(out, e.code, rel.into(), &e.message);
            false
        }
    }
}
fn inspect_change(root: &Path, name: &str, out: &mut Vec<Diagnostic>) {
    let base = format!("pentapro/changes/{name}");
    if !inspect_dir(root, &base, out) {
        return;
    }
    for f in FILES {
        let rel = format!("{base}/{f}");
        let p = root.join(&rel);
        match safe_file(&p) {
            Ok(false) => diagnostic(out, "missing-file", rel, "Required file is missing"),
            Err(e) => diagnostic(out, e.code, rel, &e.message),
            Ok(true) => match fs::read_to_string(&p) {
                Ok(s) if s.trim().is_empty() => {
                    diagnostic(out, "empty-file", rel, "Required file is empty")
                }
                Ok(_) => (),
                Err(e) if e.kind() == io::ErrorKind::InvalidData => {
                    diagnostic(out, "invalid-content", rel, "File is not UTF-8")
                }
                Err(e) => diagnostic(out, "io-error", rel, &e.to_string()),
            },
        }
    }
}
fn validate(root: &Path, name: Option<&str>) -> Result<(Value, bool)> {
    let mut d = Vec::new();
    if let Some(n) = name {
        validate_name(n)?;
        let changes = changes_path(root)?;
        if !safe_dir(&changes.join(n))? {
            return Err(error("not-found", format!("Change not found: {n}")));
        }
        inspect_change(root, n, &mut d);
    } else {
        for p in PILLARS {
            inspect_dir(root, &format!("pentapro/{p}"), &mut d);
        }
        if inspect_dir(root, "pentapro/changes", &mut d) {
            inspect_dir(root, "pentapro/changes/archive", &mut d);
            let p = root.join("pentapro/changes");
            match entries(&p) {
                Ok(names) => {
                    for n in names {
                        inspect_change(root, &n, &mut d)
                    }
                }
                Err(e) => diagnostic(&mut d, e.code, "pentapro/changes".into(), &e.message),
            }
        }
    }
    d.sort_by(|a, b| a.path.cmp(&b.path).then(a.code.cmp(b.code)));
    let valid = d.is_empty();
    Ok((json!({"valid":valid,"diagnostics":d}), valid))
}
pub fn run(requested: Option<&Path>, cmd: Command) -> Result<(Value, bool)> {
    let is_init = matches!(cmd, Command::Init);
    let root = root(requested, is_init)?;
    match cmd {
        Command::Init => {
            let _lock = Lock::acquire(&root)?;
            Ok((init(&root)?, true))
        }
        Command::New { name } => {
            let _lock = Lock::acquire(&root)?;
            Ok((new_change(&root, &name)?, true))
        }
        Command::List => Ok((json!({"changes":entries(&changes_path(&root)?)?}), true)),
        Command::Show { name } => Ok((show(&root, &name)?, true)),
        Command::Validate { name } => validate(&root, name.as_deref()),
    }
}
pub fn print_human(command: &str, data: &Value) {
    match command {
        "init" => println!(
            "Initialized specification: {} created, {} preserved",
            data["created"].as_array().map_or(0, Vec::len),
            data["preserved"].as_array().map_or(0, Vec::len)
        ),
        "new" => println!("Created {}", data["path"].as_str().unwrap_or("change")),
        "list" => {
            println!("Active changes:");
            if let Some(a) = data["changes"].as_array() {
                for n in a {
                    println!("  {}", n.as_str().unwrap_or("?"));
                }
            }
        }
        "show" => {
            println!("Change: {}", data["name"].as_str().unwrap_or("?"));
            if let Some(files) = data["files"].as_object() {
                for (name, content) in files {
                    println!("\n--- {name} ---\n{}", content.as_str().unwrap_or(""));
                }
            }
        }
        "validate" => {
            println!(
                "Structural validation: {}",
                if data["valid"] == true {
                    "passed (semantic review still required)"
                } else {
                    "failed"
                }
            );
            if let Some(d) = data["diagnostics"].as_array() {
                for x in d {
                    println!(
                        "  {}: {} ({})",
                        x["path"].as_str().unwrap_or("?"),
                        x["message"].as_str().unwrap_or("?"),
                        x["code"].as_str().unwrap_or("?")
                    );
                }
            }
        }
        _ => (),
    }
}
