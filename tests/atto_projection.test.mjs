import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import test from "node:test";

const read = (path) => readFileSync(new URL("../" + path, import.meta.url), "utf8");
const manifest = JSON.parse(read("language-candidates/atto/candidate.json"));
const source = read("language-candidates/atto/status_probe.atto");
const ts = read("clients/typescript/src/index.js");

// Parse only the deliberately restricted fixture shape. Any syntax drift
// fails closed until an Atto compiler-backed verifier replaces this guard.
function statusBounds(code, fnName) {
  const escaped = fnName.replace(/[.*+?^$\{\}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(
    "fnc " + escaped +
    "\\(int status\\): bool \\{\\s*" +
    "if status < (\\d+) then\\s*return false;\\s*fi\\s*" +
    "return status < (\\d+);\\s*\\}",
  );
  const found = code.match(regex);
  return found && [Number(found[1]), Number(found[2])];
}

function candidateErrors(candidate, attoSource) {
  const errors = [];
  const want = (ok, message) => { if (!ok) errors.push(message); };
  want(candidate.schemaVersion === 1, "schema version");
  want(candidate.language === "atto" && candidate.status === "candidate", "admission must remain candidate");
  want(candidate.compilerEvidence === "unverified", "no unproved compiler evidence");
  want(candidate.runtimeHttpClient === false && candidate.zedPublishing === false, "do not publish an incomplete SDK");
  want(candidate.contractAuthority === "clients/api-surface.json", "canonical authority");
  want(candidate.source === "language-candidates/atto/status_probe.atto", "candidate source path");
  want(JSON.stringify(candidate.endpoints) === JSON.stringify(["/health", "/ready"]), "public endpoints only");
  const success = statusBounds(attoSource, "is_success_status");
  const redirect = statusBounds(attoSource, "is_redirect_status");
  want(success !== null && success !== undefined, "success classifier syntax");
  want(redirect !== null && redirect !== undefined, "redirect classifier syntax");
  if (success) {
    want(success[0] === candidate.statusPolicy?.successMinInclusive, "success lower bound");
    want(success[1] === candidate.statusPolicy?.successMaxExclusive, "success upper bound");
    want(success[0] === 200 && success[1] === 300, "TypeScript fetch success semantics");
  }
  if (redirect) {
    want(redirect[0] === candidate.statusPolicy?.redirectMinInclusive, "redirect lower bound");
    want(redirect[1] === candidate.statusPolicy?.redirectMaxExclusive, "redirect upper bound");
    want(redirect[0] === 300 && redirect[1] === 400, "redirect boundary");
  }
  want(attoSource.includes("pub fnc main(): int {"), "executable entry signature");
  want(!/bearerToken|Authorization|\/admin|secret[_-]?key/i.test(attoSource), "no credentials or admin interface");
  return errors;
}

test("AttoLang candidate is fail-closed and matches public HTTP probe rules", () => {
  assert.deepEqual(candidateErrors(manifest, source), []);
  assert.ok(ts.includes("health() {") && ts.includes('return this.#get("/health");'));
  assert.ok(ts.includes("ready() {") && ts.includes('return this.#get("/ready");'));
  assert.match(ts, /redirect: "manual"/);
  assert.ok(ts.includes("response.status >= 300 && response.status < 400"));
  assert.ok(ts.includes("!response.ok"));
});

test("AttoLang contract mismatch and unauthorized promotion are rejected", () => {
  assert.ok(candidateErrors({...manifest, status:"production"}, source).length > 0);
  assert.ok(candidateErrors({...manifest, runtimeHttpClient:true}, source).length > 0);
  assert.ok(candidateErrors({...manifest, statusPolicy:{...manifest.statusPolicy, successMinInclusive:201}}, source).length > 0);
  assert.ok(candidateErrors(manifest, source.replace("status < 300;", "status < 301;")).length > 0);
  assert.ok(candidateErrors(manifest, source.replace("return status < 400;", "return status < 401;")).length > 0);
  assert.ok(candidateErrors(manifest, source + "\\nAuthorization: secret_key").length > 0);
});
