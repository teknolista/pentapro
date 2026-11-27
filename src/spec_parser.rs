// Adapted from OpenSpec v2.2.0 f1cd852, Copyright Fission AI Inc., MIT license.
// See https://github.com/Fission-AI/OpenSpec/blob/f1cd852f4edce22b8df9548a4df889172ca8ff25/LICENSE
use serde::Serialize;
fn js_space(c: char) -> bool {
    (c.is_whitespace() && c != '\u{0085}') || c == '\u{feff}'
}
#[derive(Serialize)]
pub struct Scenario {
    pub name: String,
    #[serde(rename = "rawText")]
    pub raw_text: String,
}
#[derive(Serialize)]
pub struct Requirement {
    pub name: String,
    pub text: String,
    pub scenarios: Vec<Scenario>,
}

#[derive(Debug)]
struct Section {
    level: usize,
    title: String,
    content: String,
    parent: Option<usize>,
}
fn fences(lines: &[&str]) -> Vec<bool> {
    let mut active: Option<(char, usize)> = None;
    lines
        .iter()
        .map(|line| {
            let s = line.trim_start_matches(js_space);
            let ch = s.chars().next();
            let n = ch
                .map(|c| s.chars().take_while(|x| *x == c).count())
                .unwrap_or(0);
            match active {
                Some((c, k)) => {
                    if ch == Some(c) && n >= k && s[n..].trim_matches(js_space).is_empty() {
                        active = None;
                    }
                    true
                }
                None => {
                    if n >= 3
                        && matches!(ch, Some('`' | '~'))
                        && !(ch == Some('`')
                            && s[n..]
                                .split(['\u{2028}', '\u{2029}'])
                                .next()
                                .unwrap_or("")
                                .contains('`'))
                    {
                        active = Some((ch.unwrap(), n));
                        true
                    } else {
                        false
                    }
                }
            }
        })
        .collect()
}
fn header_level(line: &str) -> Option<usize> {
    let n = line.bytes().take_while(|b| *b == b'#').count();
    if (1..=6).contains(&n) && line[n..].chars().next().is_some_and(js_space) {
        Some(n)
    } else {
        None
    }
}
fn heading(line: &str) -> Option<(usize, &str)> {
    let n = line.bytes().take_while(|b| *b == b'#').count();
    if !(1..=6).contains(&n) || !line[n..].chars().next().is_some_and(js_space) {
        return None;
    }
    let tail = line[n..].trim_start_matches(js_space);
    if line.ends_with(['\u{2028}', '\u{2029}']) || tail.contains(['\u{2028}', '\u{2029}']) {
        return None;
    }
    if tail.is_empty() {
        // The upstream regex can leave the final whitespace as its title.
        if line[n..].chars().count() >= 2 {
            return Some((n, ""));
        }
        return None;
    }
    Some((n, tail))
}
fn close_title(s: &str) -> String {
    let x = s.trim_end_matches([' ', '\t']);
    let without = x.trim_end_matches('#');
    if without.len() < x.len() && without.ends_with([' ', '\t']) {
        without
            .trim_end_matches(js_space)
            .trim_matches(js_space)
            .to_string()
    } else {
        s.trim_matches(js_space).to_string()
    }
}
fn prefix_ci<'a>(s: &'a str, p: &str) -> &'a str {
    match s.get(..p.len()) {
        Some(x) if x.eq_ignore_ascii_case(p) => s[p.len()..].trim_start_matches(js_space),
        _ => s,
    }
}
fn body_text(title: &str, content: &str) -> String {
    let lines: Vec<_> = content.split('\n').collect();
    let mask = fences(&lines);
    let mut body = Vec::new();
    let mut meta = Vec::new();
    for (i, line) in lines.iter().enumerate() {
        if mask[i] {
            continue;
        }
        if header_level(line).is_some() {
            break;
        }
        let s = line.trim_matches(js_space);
        if s.is_empty() {
            continue;
        }
        if s.strip_prefix("**")
            .and_then(|x| x.find("**:").map(|n| &x[..n]))
            .is_some_and(|x| !x.is_empty() && !x.contains('*'))
        {
            meta.push(s)
        } else {
            body.push(s)
        }
    }
    if !body.is_empty() {
        body.join("\n")
    } else if !meta.is_empty() {
        meta.join("\n")
    } else {
        title.trim_matches(js_space).to_string()
    }
}
pub fn parse(input: &str) -> Result<(String, Vec<Requirement>), &'static str> {
    let normalized = input
        .strip_prefix('\u{feff}')
        .unwrap_or(input)
        .replace("\r\n", "\n")
        .replace('\r', "\n");
    let lines: Vec<_> = normalized.split('\n').collect();
    let mask = fences(&lines);
    let mut sections: Vec<Section> = Vec::new();
    let mut stack: Vec<usize> = Vec::new();
    for (i, line) in lines.iter().enumerate() {
        if mask[i] {
            continue;
        }
        let Some((level, title)) = heading(line) else {
            continue;
        };
        let mut end = lines.len();
        for j in i + 1..lines.len() {
            if !mask[j] && header_level(lines[j]).is_some_and(|n| n <= level) {
                end = j;
                break;
            }
        }
        while stack
            .last()
            .is_some_and(|idx| sections[*idx].level >= level)
        {
            stack.pop();
        }
        sections.push(Section {
            level,
            title: close_title(title),
            content: lines[i + 1..end]
                .join("\n")
                .trim_matches(js_space)
                .to_string(),
            parent: stack.last().copied(),
        });
        stack.push(sections.len() - 1);
    }
    let purpose = sections
        .iter()
        .find(|s| s.title.eq_ignore_ascii_case("Purpose"))
        .map(|s| s.content.as_str())
        .unwrap_or("");
    if purpose.is_empty() {
        return Err("Spec must have a Purpose section");
    }
    let Some(reqidx) = sections
        .iter()
        .position(|s| s.title.eq_ignore_ascii_case("Requirements"))
    else {
        return Err("Spec must have a Requirements section");
    };
    let reqs = sections
        .iter()
        .enumerate()
        .filter(|(_, s)| s.parent == Some(reqidx))
        .map(|(idx, s)| {
            let scenarios: Vec<_> = sections
                .iter()
                .filter(|x| x.parent == Some(idx) && !x.content.trim_matches(js_space).is_empty())
                .map(|x| Scenario {
                    name: prefix_ci(&x.title, "Scenario:")
                        .trim_matches(js_space)
                        .to_string(),
                    raw_text: x.content.clone(),
                })
                .collect();
            Requirement {
                name: close_title(prefix_ci(&s.title, "Requirement:")),
                text: body_text(&s.title, &s.content),
                scenarios,
            }
        })
        .collect();
    Ok((purpose.trim_matches(js_space).to_string(), reqs))
}
