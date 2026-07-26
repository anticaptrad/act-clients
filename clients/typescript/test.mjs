import assert from "node:assert/strict";
import test from "node:test";

import { ActClient, ActHttpError } from "./src/index.js";

test("health and readiness use the expected paths", async () => {
  const originalFetch = globalThis.fetch;
  const seen = [];
  globalThis.fetch = async (url, init) => {
    seen.push([String(url), init]);
    return new Response(JSON.stringify({ status: "ok" }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  };
  try {
    const client = new ActClient("https://act.example/");
    await client.health();
    await client.ready();
    assert.deepEqual(seen.map(([url]) => url), [
      "https://act.example/health",
      "https://act.example/ready",
    ]);
    assert.ok(seen.every(([, init]) => init.redirect === "manual"));
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("non-success responses are typed and bounded", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => new Response("x".repeat(2000), { status: 503 });
  try {
    await assert.rejects(
      () => new ActClient("https://act.example").ready(),
      (error) =>
        error instanceof ActHttpError &&
        error.status === 503 &&
        error.body.length === 1024,
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});
