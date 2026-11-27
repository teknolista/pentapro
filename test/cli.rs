use serde_json::Value;
use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, Output},
    sync::atomic::{AtomicU64, Ordering},
};
static NEXT: AtomicU64 = AtomicU64::new(0);
struct Temp(PathBuf);
impl Temp {
    fn new() -> Self {
        let p = std::env::temp_dir().join(format!(
            "pentapro-test-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&p).unwrap();
        Self(p)
    }
}
impl Drop for Temp {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn run(dir: &Path, args: &[&str]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_pentapro"))
        .current_dir(dir)
        .args(args)
        .output()
        .unwrap()
}
fn data(o: &Output) -> Value {
    serde_json::from_slice(&o.stdout).unwrap()
}
fn err(o: &Output) -> Value {
    serde_json::from_slice(&o.stderr).unwrap()
}
fn ok(dir: &Path, args: &[&str]) -> Value {
    let o = run(dir, args);
    assert!(o.status.success(), "{}", String::from_utf8_lossy(&o.stderr));
    data(&o)
}
#[test]
fn complete_journey_and_preservation() {
    let t = Temp::new();
    fs::write(t.0.join("AGENTS.md"), "sentinel").unwrap();
    fs::create_dir_all(t.0.join("pentapro/product")).unwrap();
    fs::write(t.0.join("pentapro/product/overview.md"), "existing").unwrap();
    let v = ok(&t.0, &["init", "--json"]);
    assert_eq!(v["data"]["created"].as_array().unwrap().len(), 21);
    assert_eq!(v["data"]["preserved"].as_array().unwrap().len(), 1);
    let again = ok(&t.0, &["--json", "init"]);
    assert_eq!(again["data"]["created"].as_array().unwrap().len(), 0);
    assert_eq!(
        fs::read_to_string(t.0.join("pentapro/product/overview.md")).unwrap(),
        "existing"
    );
    assert_eq!(
        fs::read_to_string(t.0.join("AGENTS.md")).unwrap(),
        "sentinel"
    );
    ok(&t.0, &["--json", "new", "zeta-work"]);
    ok(&t.0, &["new", "alpha-work", "--json"]);
    let v = ok(&t.0, &["--json", "list"]);
    assert_eq!(
        v["data"]["changes"],
        serde_json::json!(["alpha-work", "zeta-work"])
    );
    let shown = ok(&t.0, &["show", "alpha-work", "--json"]);
    assert_eq!(shown["data"]["files"].as_object().unwrap().len(), 6);
    assert!(
        ok(&t.0, &["--json", "validate"])["data"]["valid"]
            .as_bool()
            .unwrap()
    );
    let path = t.0.join("pentapro/changes/alpha-work/proof.md");
    fs::write(&path, " \n").unwrap();
    let fail = run(&t.0, &["validate", "alpha-work", "--json"]);
    assert_eq!(fail.status.code(), Some(1));
    assert_eq!(data(&fail)["data"]["diagnostics"][0]["code"], "empty-file");
    fs::write(&path, "repaired").unwrap();
    assert!(
        ok(&t.0, &["validate", "alpha-work", "--json"])["data"]["valid"]
            .as_bool()
            .unwrap()
    );
    let nested = t.0.join("pentapro/product");
    assert_eq!(
        ok(&nested, &["list", "--json"])["data"]["changes"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
    let root = t.0.to_str().unwrap();
    assert_eq!(
        ok(&nested, &["--json", "--root", root, "list"])["data"]["changes"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
    let dup = run(&t.0, &["new", "alpha-work", "--json"]);
    assert_eq!(err(&dup)["error"]["code"], "already-exists");
    assert!(dup.stdout.is_empty());
}
#[test]
fn invalid_missing_and_archive() {
    let t = Temp::new();
    let missing = run(&t.0, &["list", "--json"]);
    assert_eq!(err(&missing)["error"]["code"], "project-not-found");
    ok(&t.0, &["--json", "init"]);
    for n in ["../escape", "/tmp/escape", "bad", "A-b", "a-b-c-d"] {
        let o = run(&t.0, &["--json", "new", n]);
        assert_eq!(err(&o)["error"]["code"], "invalid-name");
    }
    fs::create_dir(t.0.join("pentapro/changes/archive/2026-11-26_old-work")).unwrap();
    assert_eq!(
        err(&run(&t.0, &["new", "old-work", "--json"]))["error"]["code"],
        "already-exists"
    );
    ok(&t.0, &["new", "good-work", "--json"]);
    fs::remove_file(t.0.join("pentapro/changes/good-work/proof.md")).unwrap();
    let v = run(&t.0, &["validate", "good-work", "--json"]);
    assert_eq!(data(&v)["data"]["diagnostics"][0]["code"], "missing-file");
    let s = run(&t.0, &["show", "good-work", "--json"]);
    assert_eq!(err(&s)["error"]["code"], "not-found");
}
#[test]
fn lock_and_malformed_entries() {
    let t = Temp::new();
    ok(&t.0, &["--json", "init"]);
    fs::write(t.0.join(".pentapro-engine.lock"), "held").unwrap();
    assert_eq!(
        err(&run(&t.0, &["new", "valid-name", "--json"]))["error"]["code"],
        "locked"
    );
    assert!(!t.0.join("pentapro/changes/valid-name").exists());
    fs::remove_file(t.0.join(".pentapro-engine.lock")).unwrap();
    fs::create_dir(t.0.join("pentapro/changes/BAD")).unwrap();
    assert_eq!(
        err(&run(&t.0, &["list", "--json"]))["error"]["code"],
        "invalid-name"
    );
}
#[cfg(unix)]
#[test]
fn symlink_and_preflight_safety() {
    use std::os::unix::fs::symlink;
    let t = Temp::new();
    let outside = Temp::new();
    fs::create_dir_all(t.0.join("pentapro")).unwrap();
    symlink(&outside.0, t.0.join("pentapro/product")).unwrap();
    let o = run(&t.0, &["init", "--json"]);
    assert_eq!(err(&o)["error"]["code"], "unsafe-path");
    assert!(!t.0.join("pentapro/project").exists());
    assert_eq!(fs::read_dir(&outside.0).unwrap().count(), 0);
    let link = t.0.join("root-link");
    symlink(&outside.0, &link).unwrap();
    let o = run(&t.0, &["--root", link.to_str().unwrap(), "init", "--json"]);
    assert_eq!(err(&o)["error"]["code"], "unsafe-path");
}
#[cfg(unix)]
#[test]
fn unsafe_change_and_non_utf8() {
    use std::os::unix::fs::symlink;
    let t = Temp::new();
    let outside = Temp::new();
    ok(&t.0, &["--json", "init"]);
    symlink(&outside.0, t.0.join("pentapro/changes/evil-link")).unwrap();
    assert_eq!(
        err(&run(&t.0, &["list", "--json"]))["error"]["code"],
        "unsafe-path"
    );
    fs::remove_file(t.0.join("pentapro/changes/evil-link")).unwrap();
    ok(&t.0, &["--json", "new", "real-change"]);
    fs::write(t.0.join("pentapro/changes/real-change/product.md"), [0xff]).unwrap();
    assert_eq!(
        err(&run(&t.0, &["show", "real-change", "--json"]))["error"]["code"],
        "invalid-content"
    );
}
#[test]
fn help_version_and_usage() {
    let t = Temp::new();
    assert!(run(&t.0, &["--help"]).status.success());
    assert!(run(&t.0, &["--version"]).status.success());
    assert_eq!(run(&t.0, &["unknown"]).status.code(), Some(2));
}
#[test]
fn concurrent_same_name_has_one_winner() {
    let t = Temp::new();
    ok(&t.0, &["--json", "init"]);
    let bin = env!("CARGO_BIN_EXE_pentapro");
    let mut a = Command::new(bin)
        .current_dir(&t.0)
        .args(["--json", "new", "race-test"])
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .spawn()
        .unwrap();
    let mut b = Command::new(bin)
        .current_dir(&t.0)
        .args(["--json", "new", "race-test"])
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .spawn()
        .unwrap();
    let a = a.wait().unwrap();
    let b = b.wait().unwrap();
    assert_eq!(usize::from(a.success()) + usize::from(b.success()), 1);
    assert_eq!(
        fs::read_dir(t.0.join("pentapro/changes/race-test"))
            .unwrap()
            .count(),
        6
    );
}
#[test]
fn regular_file_directory_collision_preflight() {
    let t = Temp::new();
    fs::create_dir(t.0.join("pentapro")).unwrap();
    fs::write(t.0.join("pentapro/proof"), "keep").unwrap();
    let o = run(&t.0, &["--json", "init"]);
    assert_eq!(err(&o)["error"]["code"], "unsafe-path");
    assert!(!t.0.join("pentapro/product").exists());
    assert_eq!(
        fs::read_to_string(t.0.join("pentapro/proof")).unwrap(),
        "keep"
    );
}

#[cfg(unix)]
#[test]
fn root_rejects_intermediate_symlinks_before_parent_resolution() {
    use std::os::unix::fs::symlink;
    let workspace = Temp::new();
    let outside = Temp::new();
    fs::create_dir(outside.0.join("child")).unwrap();
    symlink(&outside.0, workspace.0.join("alias")).unwrap();
    let absolute = workspace.0.join("alias/child");
    let with_parent = workspace.0.join("alias/../alias/child");
    for root in [
        absolute.as_path(),
        with_parent.as_path(),
        Path::new("alias/child"),
        Path::new("alias/../alias/child"),
    ] {
        let o = run(
            &workspace.0,
            &["--root", root.to_str().unwrap(), "init", "--json"],
        );
        assert_eq!(
            o.status.code(),
            Some(1),
            "unexpected success for {}",
            root.display()
        );
        assert_eq!(err(&o)["error"]["code"], "unsafe-path");
        assert!(!outside.0.join("child/pentapro").exists());
        assert!(!workspace.0.join(".pentapro-engine.lock").exists());
    }
    fs::create_dir(workspace.0.join("real")).unwrap();
    assert!(
        run(&workspace.0, &["--root", "real/../real", "init", "--json"])
            .status
            .success()
    );
}

#[test]
fn discovery_skips_ordinary_file_markers() {
    let t = Temp::new();
    ok(&t.0, &["--json", "init"]);
    fs::create_dir(t.0.join("nested")).unwrap();
    fs::write(t.0.join("nested/pentapro"), "ordinary file").unwrap();
    let o = run(&t.0.join("nested"), &["list", "--json"]);
    assert!(o.status.success(), "{}", String::from_utf8_lossy(&o.stderr));
    assert_eq!(data(&o)["data"]["changes"], serde_json::json!([]));
    let explicit = run(&t.0, &["--root", "nested", "list", "--json"]);
    assert_eq!(err(&explicit)["error"]["code"], "unsafe-path");
}

#[cfg(unix)]
#[test]
fn discovery_rejects_symlink_marker() {
    use std::os::unix::fs::symlink;
    let t = Temp::new();
    let outside = Temp::new();
    ok(&t.0, &["--json", "init"]);
    fs::create_dir(t.0.join("nested")).unwrap();
    symlink(&outside.0, t.0.join("nested/pentapro")).unwrap();
    let o = run(&t.0.join("nested"), &["list", "--json"]);
    assert_eq!(err(&o)["error"]["code"], "unsafe-path");
}

#[test]
fn compat_list_real_project_json() {
    let guard = Temp::new();
    let dir = &guard.0;
    std::fs::create_dir_all(dir.join("openspec/specs/alpha")).unwrap();
    std::fs::write(dir.join("openspec/specs/alpha/spec.md"), "# Alpha\n\n## Purpose\n\nA capability.\n\n## Requirements\n\n### Requirement: Login\n\nThe system SHALL allow access.\n").unwrap();
    let out = std::process::Command::new(env!("CARGO_BIN_EXE_pentapro"))
        .current_dir(dir)
        .env("HOME", dir)
        .env_remove("XDG_CONFIG_HOME")
        .env_remove("XDG_DATA_HOME")
        .args(["compat", "openspec", "list", "--specs", "--json"])
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    let v: serde_json::Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(v["specs"][0]["id"], "alpha");
    assert_eq!(v["specs"][0]["requirementCount"], 1);
}
