use serde::Deserialize;

#[derive(Debug, Clone)]
pub struct ActClient {
    base_url: String,
    agent: ureq::Agent,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct HealthResponse {
    pub status: String,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct ReadyResponse {
    pub ready: bool,
    pub nats_connected: Option<bool>,
    pub database_connected: Option<bool>,
}

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("Act API returned HTTP {status}: {body}")]
    Http { status: u16, body: String },
    #[error("Act API transport error: {0}")]
    Transport(#[from] ureq::Error),
    #[error("Act API response decode error: {0}")]
    Decode(#[from] std::io::Error),
}

impl ActClient {
    pub fn new(base_url: impl Into<String>) -> Self {
        Self {
            base_url: base_url.into().trim_end_matches('/').to_owned(),
            agent: ureq::Agent::config_builder()
                .max_redirects(0)
                .build()
                .into(),
        }
    }

    pub fn health(&self) -> Result<HealthResponse, Error> {
        self.get("/health")
    }

    pub fn ready(&self) -> Result<ReadyResponse, Error> {
        self.get("/ready")
    }

    fn get<T: for<'de> Deserialize<'de>>(&self, path: &str) -> Result<T, Error> {
        match self
            .agent
            .get(format!("{}{}", self.base_url, path))
            .header("accept", "application/json")
            .call()
        {
            Ok(mut response) => Ok(response.body_mut().read_json()?),
            Err(ureq::Error::StatusCode(status)) => Err(Error::Http {
                status,
                body: String::new(),
            }),
            Err(error) => Err(Error::Transport(error)),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn trims_trailing_slashes() {
        let client = ActClient::new("https://act.example///");
        assert_eq!(client.base_url, "https://act.example");
    }
}
