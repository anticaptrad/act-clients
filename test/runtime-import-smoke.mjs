import assert from "node:assert/strict";

const runtime = globalThis.Deno ? "deno" : globalThis.Bun ? "bun" : "node";
const candidates = [
  "../clients/typescript/dist/index.js",
  "../clients/typescript/dist/index.mjs",
  "../clients/typescript/lib/index.js",
  "../clients/typescript/build/index.js",
  "../clients/typescript/src/index.js",
];
let sdk;
let lastError;
for (const candidate of candidates) {
  try {
    sdk = await import(new URL(candidate, import.meta.url));
    break;
  } catch (error) {
    lastError = error;
  }
}
assert.ok(sdk, `could not import the built TypeScript client in ${runtime}: ${lastError}`);
assert.ok(Object.keys(sdk).length > 0, "client module must export a public API");
for (const globalName of ["fetch", "Headers", "Request", "Response"]) {
  assert.equal(typeof globalThis[globalName], "function", `${runtime} must expose ${globalName}`);
}
console.log(`${runtime} client import smoke passed with ${Object.keys(sdk).length} exports`);
