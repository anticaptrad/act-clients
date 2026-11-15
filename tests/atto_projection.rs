//! Rust-only fail-closed checks for the AttoLang client candidate.
//! These are source/manifest boundary checks, NOT Atto compiler execution.

const SOURCE: &str = include_str!("../language-candidates/atto/status_probe.atto");
const MANIFEST: &str = include_str!("../language-candidates/atto/candidate.json");
const TYPESCRIPT: &str = include_str!("../clients/typescript/src/index.js");

fn status_bounds(source: &str, function: &str) -> Option<(i64, i64)> {
    let marker = format!("fnc {function}(int status): bool {{");
    let body = source.split_once(&marker)?.1.split_once("\n}")?.0;
    let lines: Vec<_> = body.lines().map(str::trim).filter(|s| !s.is_empty()).collect();
    if lines.len() != 4 || lines[1] != "return false;" || lines[2] != "fi" {
        return None;
    }
    let lower = lines[0].strip_prefix("if status < ")?.strip_suffix(" then")?.parse().ok()?;
    let upper = lines[3].strip_prefix("return status < ")?.strip_suffix(';')?.parse().ok()?;
    Some((lower, upper))
}

fn integer_field(json: &str, name: &str) -> Option<i64> {
    let key = format!("\"{name}\"");
    if json.matches(&key).count() != 1 {
        return None;
    }
    let (_, tail) = json.split_once(&key)?;
    let digits: String = tail.trim_start().strip_prefix(':')?.trim_start()
        .chars().take_while(|c| c.is_ascii_digit()).collect();
    digits.parse().ok()
}

fn errors(manifest: &str, source: &str, typescript: &str) -> Vec<&'static str> {
    let mut errors = Vec::new();
    let mut need = |valid: bool, label| {
        if !valid { errors.push(label); }
    };

    need(manifest.contains("\"language\": \"atto\""), "language");
    need(manifest.contains("\"status\": \"candidate\""), "candidate only");
    need(manifest.contains("\"compilerEvidence\": \"unverified\""), "missing compiler proof");
    need(manifest.contains("\"runtimeHttpClient\": false"), "not a working HTTP SDK");
    need(manifest.contains("\"zedPublishing\": false"), "not published");
    need(manifest.contains("\"source\": \"language-candidates/atto/status_probe.atto\""), "source path");
    need(manifest.contains("\"contractAuthority\": \"clients/api-surface.json\""), "authority");
    need(manifest.contains("\"/health\"") && manifest.contains("\"/ready\""), "public probes");
    let success = status_bounds(source, "is_success_status");
    let redirect = status_bounds(source, "is_redirect_status");
    need(success == Some((200, 300)), "success status shape");
    need(redirect == Some((300, 400)), "redirect status shape");
    need(integer_field(manifest, "successMinInclusive") == Some(200), "success minimum");
    need(integer_field(manifest, "successMaxExclusive") == Some(300), "success maximum");
    need(integer_field(manifest, "redirectMinInclusive") == Some(300), "redirect minimum");
    need(integer_field(manifest, "redirectMaxExclusive") == Some(400), "redirect maximum");
    need(source.contains("pub fnc main(): int {"), "entrypoint");
    need(!["bearerToken", "Authorization", "secret_key", "/admin"]
        .iter().any(|part| source.contains(part)), "credential leak");
    need(typescript.contains("return this.#get(\"/health\");"), "health mapping");
    need(typescript.contains("return this.#get(\"/ready\");"), "ready mapping");
    need(typescript.contains("redirect: \"manual\""), "redirect policy");
    need(typescript.contains("response.status >= 300 && response.status < 400"), "redirect bounds");
    need(typescript.contains("!response.ok"), "non-2xx failure");
    errors
}

#[test]
fn atto_candidate_matches_public_probe_contract() {
    assert!(errors(MANIFEST, SOURCE, TYPESCRIPT).is_empty(),
        "{:?}", errors(MANIFEST, SOURCE, TYPESCRIPT));
}

#[test]
fn negative_canaries_reject_drift_and_premature_promotion() {
    for (old, new) in [
        ("\"status\": \"candidate\"", "\"status\": \"production\""),
        ("\"runtimeHttpClient\": false", "\"runtimeHttpClient\": true"),
        ("\"successMinInclusive\": 200", "\"successMinInclusive\": 201"),
    ] {
        let invalid = MANIFEST.replace(old, new);
        assert!(!errors(&invalid, SOURCE, TYPESCRIPT).is_empty(), "{old}");
    }
    for (old, new) in [
        ("status < 300;", "status < 301;"),
        ("return status < 400;", "return status < 401;"),
    ] {
        assert!(!errors(MANIFEST, &SOURCE.replace(old, new), TYPESCRIPT).is_empty());
    }
    assert!(!errors(MANIFEST, &format!("{SOURCE}\nAuthorization secret_key"), TYPESCRIPT).is_empty());
}
