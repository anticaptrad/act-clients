import gleam/option.{type Option, None}

pub type Client {
  Client(base_url: String, token: Option(String))
}

pub type Request {
  Request(method: String, url: String, token: Option(String), body: Option(String))
}

pub fn new(base_url: String) -> Client {
  Client(base_url: base_url, token: None)
}

pub fn request(client: Client, method: String, path: String, body: Option(String)) -> Request {
  Request(method: method, url: client.base_url <> path, token: client.token, body: body)
}

pub fn health(client: Client) -> Request {
  request(client, "GET", "/health", None)
}
