use crate::config::AppConfig;
use anyhow::{Context, Result};
use std::fs;
use std::path::PathBuf;

const CONFIG_DIR_NAME: &str = "aion";
const CONFIG_FILE_NAME: &str = "config.toml";

pub fn config_dir() -> Result<PathBuf> {
    let base = dirs::config_dir().context("failed to locate system config directory")?;
    Ok(base.join(CONFIG_DIR_NAME))
}

pub fn config_file_path() -> Result<PathBuf> {
    Ok(config_dir()?.join(CONFIG_FILE_NAME))
}

pub fn ensure_config_dir_exists() -> Result<()> {
    let dir = config_dir()?;
    if !dir.exists() {
        fs::create_dir_all(&dir)
            .with_context(|| format!("failed to create config directory: {}", dir.display()))?;
    }
    Ok(())
}

pub fn load_config() -> Result<AppConfig> {
    let path = config_file_path()?;

    if !path.exists() {
        return Err(anyhow::anyhow!("config file does not exist"));
    }

    let content = fs::read_to_string(&path)
        .with_context(|| format!("failed to read config file: {}", path.display()))?;

    let config: AppConfig = toml::from_str(&content)
        .with_context(|| format!("failed to parse config file: {}", path.display()))?;

    config.validate().with_context(|| "config validation failed")?;
    Ok(config)
}

pub fn save_config(config: &AppConfig) -> Result<()> {
    ensure_config_dir_exists()?;

    let path = config_file_path()?;
    let toml_str = toml::to_string_pretty(config).context("failed to serialize config to TOML")?;

    fs::write(&path, toml_str)
        .with_context(|| format!("failed to write config file: {}", path.display()))?;

    Ok(())
}

pub fn load_or_create_config() -> Result<AppConfig> {
    match load_config() {
        Ok(config) => Ok(config),
        Err(_) => {
            let config = AppConfig::new_default();
            save_config(&config)?;
            Ok(config)
        }
    }
}

pub fn config_exists() -> Result<bool> {
    let path = config_file_path()?;
    Ok(path.exists())
}