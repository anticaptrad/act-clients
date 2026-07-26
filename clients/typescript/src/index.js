export class ActHttpError extends Error {
  constructor(status, body) {
    super(`Act API returned HTTP ${status}`);
    this.name = "ActHttpError";
    this.status = status;
    this.body = body;
  }
}

export class ActClient {
  constructor(baseUrl) {
    this.baseUrl = String(baseUrl).replace(/\/+$/, "");
  }

  health() {
    return this.#get("/health");
  }

  ready() {
    return this.#get("/ready");
  }

  async #get(path) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      headers: { accept: "application/json" },
      redirect: "manual",
    });
    if (response.status >= 300 && response.status < 400) {
      throw new ActHttpError(response.status, "redirect refused");
    }
    if (!response.ok) {
      throw new ActHttpError(response.status, (await response.text()).slice(0, 1024));
    }
    return response.json();
  }
}
