use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, Output},
    sync::atomic::{AtomicUsize, Ordering},
};
static NEXT: AtomicUsize = AtomicUsize::new(0);
struct Temp(PathBuf);
impl Temp {
    fn new() -> Self {
        let p = std::env::temp_dir().join(format!(
            "pentapro-compat-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&p).unwrap();
        fs::create_dir(p.join("home")).unwrap();
        fs::create_dir(p.join("project")).unwrap();
        Self(p)
    }
    fn project(&self) -> PathBuf {
        self.0.join("project")
    }
    fn run(&self, args: &[&str]) -> Output {
        Command::new(env!("CARGO_BIN_EXE_pentapro"))
            .current_dir(self.project())
            .env("HOME", self.0.join("home"))
            .env_remove("XDG_CONFIG_HOME")
            .env_remove("XDG_DATA_HOME")
            .args(args)
            .output()
            .unwrap()
    }
    fn spec(&self, name: &str, bytes: &[u8]) {
        let p = self.project().join("openspec/specs").join(name);
        fs::create_dir_all(&p).unwrap();
        fs::write(p.join("spec.md"), bytes).unwrap();
    }
}
impl Drop for Temp {
    fn drop(&mut self) {
        fs::remove_dir_all(&self.0).ok();
    }
}
fn v(out: &Output) -> serde_json::Value {
    serde_json::from_slice(&out.stdout).unwrap()
}
const SPEC: &str = "# Alpha\n\n## Purpose\n\nA capability.\n\n## Requirements\n\n### Requirement: Login\n\nThe system SHALL allow access.\n\n#### Scenario: Success\n\n- **WHEN** login\n- **THEN** yes\n";
#[test]
fn basic_journey_and_unsupported() {
    let t = Temp::new();
    t.spec("alpha", SPEC.as_bytes());
    let before = fs::read(t.project().join("openspec/specs/alpha/spec.md")).unwrap();
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert!(out.status.success());
    assert_eq!(v(&out)["specs"][0]["requirementCount"], 1);
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    let json = v(&out);
    assert_eq!(
        json["requirements"][0]["text"],
        "The system SHALL allow access."
    );
    assert_eq!(json["requirements"][0]["scenarios"][0]["name"], "Success");
    let out = t.run(&["compat", "openspec", "show", "alpha", "--type", "spec"]);
    assert_eq!(out.stdout, [SPEC.as_bytes(), b"\n"].concat());
    let out = t.run(&["compat", "openspec", "validate", "alpha"]);
    assert_eq!(out.status.code(), Some(2));
    assert!(out.stdout.is_empty());
    assert_eq!(
        before,
        fs::read(t.project().join("openspec/specs/alpha/spec.md")).unwrap()
    );
}
#[test]
fn parsing_bad_utf8_fences_and_errors() {
    let t = Temp::new();
    t.spec("alpha",b"\xef\xbb\xbf# X\r\n## Purpose\r\nInvalid \xff text\r\n## Requirements\r\n```\r\n### Fake\r\n```\r\n### Requirement: Real ###\r\n**ID**: A\r\nText\r\n#### Scenario: Here ###\r\nBody\r\n");
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    let x = v(&out);
    assert_eq!(x["overview"], "Invalid \u{fffd} text");
    assert_eq!(x["requirementCount"], 1);
    assert_eq!(x["requirements"][0]["name"], "Real");
    assert_eq!(x["requirements"][0]["text"], "Text");
    assert_eq!(x["requirements"][0]["scenarios"][0]["name"], "Here");
    t.spec("alpha", b"# Missing purpose\n");
    let list = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(v(&list)["specs"][0]["requirementCount"], 0);
    let show = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert_eq!(show.status.code(), Some(1));
    assert_eq!(
        v(&show)["status"][0]["message"],
        "Spec must have a Purpose section"
    );
}
#[test]
fn missing_root_and_conservative_rules() {
    let t = Temp::new();
    let list = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(list.status.code(), Some(1));
    assert_eq!(v(&list)["status"][0]["code"], "no_openspec_root");
    let show = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert_eq!(v(&show)["status"][0]["code"], "show_error");
    t.spec("alpha", SPEC.as_bytes());
    fs::write(
        t.project().join("openspec/config.yaml"),
        "schema: [broken\n",
    )
    .unwrap();
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(out.stderr, b"unsupported root selection\n");
}
#[test]
fn unsupported_ordering() {
    let t = Temp::new();
    t.spec("alpha", SPEC.as_bytes());
    t.spec("nested/second", SPEC.as_bytes());
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(out.stderr, b"unsupported spec identifier ordering\n");
}
#[cfg(unix)]
#[test]
fn symlink_discovery_containment() {
    use std::os::unix::fs::symlink;
    let t = Temp::new();
    t.spec("real", SPEC.as_bytes());
    let specs = t.project().join("openspec/specs");
    fs::create_dir(specs.join("inside")).unwrap();
    symlink("../real/spec.md", specs.join("inside/spec.md")).unwrap();
    fs::create_dir(specs.join("bad")).unwrap();
    let outside = t.0.join("outside.md");
    fs::write(&outside, "outside").unwrap();
    symlink(&outside, specs.join("bad/spec.md")).unwrap();
    let out = t.run(&[
        "compat", "openspec", "show", "real", "--type", "spec", "--json",
    ]);
    assert_eq!(out.status.code(), Some(1));
    assert!(
        v(&out)["status"][0]["message"]
            .as_str()
            .unwrap()
            .contains("outside the allowed directory")
    );
    fs::remove_file(specs.join("bad/spec.md")).unwrap();
    let out = t.run(&[
        "compat", "openspec", "show", "inside", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    fs::create_dir(specs.join("broken")).unwrap();
    symlink("missing.md", specs.join("broken/spec.md")).unwrap();
    let out = t.run(&[
        "compat", "openspec", "show", "broken", "--type", "spec", "--json",
    ]);
    assert!(
        v(&out)["status"][0]["message"]
            .as_str()
            .unwrap()
            .contains("dangling symbolic link")
    );
}
#[test]
fn nested_explicit_root_unchanged() {
    let t = Temp::new();
    t.spec("alpha", SPEC.as_bytes());
    let sub = t.project().join("nested");
    fs::create_dir(&sub).unwrap();
    let out = Command::new(env!("CARGO_BIN_EXE_pentapro"))
        .current_dir(&sub)
        .env("HOME", t.0.join("home"))
        .env_remove("XDG_CONFIG_HOME")
        .env_remove("XDG_DATA_HOME")
        .args(["compat", "openspec", "list", "--specs", "--json"])
        .output()
        .unwrap();
    assert_eq!(v(&out)["root"]["path"], t.project().to_str().unwrap());
    assert!(Path::new(&t.project()).exists());
}

#[test]
fn ecmascript_whitespace_in_spec_content() {
    let t = Temp::new();
    t.spec(
        "alpha",
        "# X\n## Purpose\n\u{feff}Hello\u{feff}\n## Requirements\n### Requirement: A\nBody\n"
            .as_bytes(),
    );
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    assert_eq!(v(&out)["overview"], "Hello");
    t.spec(
        "alpha",
        "# X\n## Purpose\n\u{0085}Hello\u{0085}\n## Requirements\n### Requirement: A\nBody\n"
            .as_bytes(),
    );
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    assert_eq!(v(&out)["overview"], "\u{0085}Hello\u{0085}");
}

#[test]
fn reject_global_config_and_store_without_mutation() {
    let t = Temp::new();
    t.spec("alpha", SPEC.as_bytes());
    let global = t.0.join("home/.config/openspec");
    fs::create_dir_all(&global).unwrap();
    fs::write(global.join("config.json"), "sentinel").unwrap();
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(out.stderr, b"unsupported root selection\n");
    assert_eq!(
        fs::read_to_string(global.join("config.json")).unwrap(),
        "sentinel"
    );
    fs::remove_dir_all(global).unwrap();
    let store = t.project().join("openspec/specs/.openspec-store");
    fs::write(&store, "sentinel").unwrap();
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(out.stderr, b"unsupported root selection\n");
    assert_eq!(fs::read_to_string(store).unwrap(), "sentinel");
}

#[cfg(unix)]
#[test]
fn explicit_directory_symlink_and_mode_zero_preflight() {
    use std::os::unix::fs::{PermissionsExt, symlink};
    let t = Temp::new();
    t.spec("real", SPEC.as_bytes());
    let specs = t.project().join("openspec/specs");
    symlink("real", specs.join("alias")).unwrap();
    let out = t.run(&[
        "compat", "openspec", "show", "alias", "--type", "spec", "--json",
    ]);
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert_eq!(v(&out)["id"], "alias");
    fs::set_permissions(&specs, fs::Permissions::from_mode(0o0)).unwrap();
    let out = t.run(&["compat", "openspec", "list", "--specs", "--json"]);
    fs::set_permissions(&specs, fs::Permissions::from_mode(0o755)).unwrap();
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(out.stderr, b"unsupported root selection\n");
}

#[test]
fn ecmascript_line_terminators_in_headings_and_fence_info() {
    let t = Temp::new();
    let prefix = "# Alpha\n\n## Purpose\n\nPurpose text\n\n## Requirements\n\n";
    for separator in ['\u{2028}', '\u{2029}'] {
        for suffix in [
            format!("### Requirement: A{separator}B\nBody\n"),
            format!("### Requirement: A{separator}\nBody\n"),
            format!("```foo{separator}`\n### Requirement: Hidden\nBody\n```\n"),
        ] {
            t.spec("alpha", format!("{prefix}{suffix}").as_bytes());
            let out = t.run(&[
                "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
            ]);
            assert!(
                out.status.success(),
                "{}",
                String::from_utf8_lossy(&out.stderr)
            );
            assert_eq!(v(&out)["requirementCount"], 0, "{suffix:?}");
        }
    }
    t.spec(
        "alpha",
        format!("{prefix}### Requirement: Normal\nBody\n").as_bytes(),
    );
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert!(out.status.success());
    assert_eq!(v(&out)["requirementCount"], 1);
}

#[cfg(unix)]
#[test]
fn external_directory_file_link_back_into_project_is_rejected() {
    use std::os::unix::fs::symlink;
    let t = Temp::new();
    let specs = t.project().join("openspec/specs");
    fs::create_dir_all(&specs).unwrap();
    let docs = t.project().join("docs");
    fs::create_dir(&docs).unwrap();
    fs::write(docs.join("spec.md"), SPEC).unwrap();
    let outside = t.0.join("outside");
    fs::create_dir(&outside).unwrap();
    symlink(docs.join("spec.md"), outside.join("spec.md")).unwrap();
    symlink(&outside, specs.join("alpha")).unwrap();
    let expected = format!(
        "Path is outside the allowed directory: {}",
        specs.join("alpha").display()
    );
    let out = t.run(&[
        "compat", "openspec", "show", "alpha", "--type", "spec", "--json",
    ]);
    assert_eq!(
        out.status.code(),
        Some(1),
        "{}",
        String::from_utf8_lossy(&out.stdout)
    );
    assert_eq!(v(&out)["status"][0]["message"], expected);
    let out = t.run(&["compat", "openspec", "show", "alpha", "--type", "spec"]);
    assert_eq!(out.status.code(), Some(1));
    assert!(String::from_utf8_lossy(&out.stderr).contains(&expected));
    assert_eq!(fs::read_to_string(docs.join("spec.md")).unwrap(), SPEC);
}
