pub type Client { Client(base_url: String) }
pub fn new(base_url: String) -> Client { Client(base_url: base_url) }
pub fn health_path() -> String { "/health" }
pub fn ready_path() -> String { "/ready" }
