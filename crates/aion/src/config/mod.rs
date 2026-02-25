pub mod io;
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ProviderKind {
    OpenAI,
    Claude,
    OpenRouter,
    Ollama,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum UiMode {
    Tui,
    Cli,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProviderConfig {
    pub kind: ProviderKind,
    pub model: String,
    pub base_url: Option<String>,
    pub api_key_env: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Features {
    pub system_scan: bool,
    pub web_in_terminal: bool,
    pub command_suggestions: bool,
    pub safe_execute: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capabilities {
    pub read_files: bool,
    pub write_files: bool,
    pub network: bool,
    pub run_commands: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub version: u32,
    pub language: String,
    pub ui_mode: UiMode,
    pub provider: ProviderConfig,
    pub features: Features,
    pub caps: Capabilities,
}

#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("config version is not supported: {0}")]
    UnsupportedVersion(u32),

    #[error("language is invalid: {0}")]
    InvalidLanguage(String),

    #[error("provider model is empty")]
    EmptyModel,

    #[error("base_url is required for this provider")]
    MissingBaseUrl,

    #[error("api_key_env is required for this provider")]
    MissingApiKeyEnv,
}

impl ProviderKind {
    pub fn requires_api_key(&self) -> bool {
        matches!(self, ProviderKind::OpenAI | ProviderKind::Claude | ProviderKind::OpenRouter)
    }

    pub fn default_api_key_env(&self) -> Option<&'static str> {
        match self {
            ProviderKind::OpenAI => Some("OPENAI_API_KEY"),
            ProviderKind::Claude => Some("ANTHROPIC_API_KEY"),
            ProviderKind::OpenRouter => Some("OPENROUTER_API_KEY"),
            ProviderKind::Ollama => None,
        }
    }

    pub fn default_base_url(&self) -> Option<&'static str> {
        match self {
            ProviderKind::OpenRouter => Some("https://openrouter.ai/api/v1"),
            ProviderKind::Ollama => Some("http://localhost:11434"),
            _ => None,
        }
    }

    pub fn default_model(&self) -> &'static str {
        match self {
            ProviderKind::OpenAI => "gpt-4.1-mini",
            ProviderKind::Claude => "claude-3-5-sonnet-latest",
            ProviderKind::OpenRouter => "openai/gpt-4o-mini",
            ProviderKind::Ollama => "mistral",
        }
    }
}

impl AppConfig {
    pub const CURRENT_VERSION: u32 = 1;

    pub fn new_default() -> Self {
        let kind = ProviderKind::Ollama;
        Self {
            version: Self::CURRENT_VERSION,
            language: "en".to_string(),
            ui_mode: UiMode::Tui,
            provider: ProviderConfig {
                kind: kind.clone(),
                model: kind.default_model().to_string(),
                base_url: kind.default_base_url().map(|s| s.to_string()),
                api_key_env: kind.default_api_key_env().map(|s| s.to_string()),
            },
            features: Features {
                system_scan: true,
                web_in_terminal: true,
                command_suggestions: true,
                safe_execute: true,
            },
            caps: Capabilities {
                read_files: true,
                write_files: false,
                network: true,
                run_commands: false,
            },
        }
    }

    pub fn validate(&self) -> Result<(), ConfigError> {
        if self.version != Self::CURRENT_VERSION {
            return Err(ConfigError::UnsupportedVersion(self.version));
        }

        let allowed = allowed_languages();
        if !allowed.contains(self.language.as_str()) {
            return Err(ConfigError::InvalidLanguage(self.language.clone()));
        }

        if self.provider.model.trim().is_empty() {
            return Err(ConfigError::EmptyModel);
        }

        match self.provider.kind {
            ProviderKind::OpenRouter => {
                if self.provider.base_url.as_deref().unwrap_or("").trim().is_empty() {
                    return Err(ConfigError::MissingBaseUrl);
                }
                if self.provider.api_key_env.as_deref().unwrap_or("").trim().is_empty() {
                    return Err(ConfigError::MissingApiKeyEnv);
                }
            }
            ProviderKind::Ollama => {
                if self.provider.base_url.as_deref().unwrap_or("").trim().is_empty() {
                    return Err(ConfigError::MissingBaseUrl);
                }
            }
            ProviderKind::OpenAI | ProviderKind::Claude => {
                if self.provider.api_key_env.as_deref().unwrap_or("").trim().is_empty() {
                    return Err(ConfigError::MissingApiKeyEnv);
                }
            }
        }

        Ok(())
    }

    pub fn set_provider_kind(&mut self, kind: ProviderKind) {
        self.provider.kind = kind.clone();
        self.provider.model = kind.default_model().to_string();
        self.provider.base_url = kind.default_base_url().map(|s| s.to_string());
        self.provider.api_key_env = kind.default_api_key_env().map(|s| s.to_string());
    }
}

pub fn allowed_languages() -> BTreeSet<&'static str> {
    BTreeSet::from(["en", "ar"])
}