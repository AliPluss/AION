use anyhow::{Context, Result};
use serde::Deserialize;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

/// Locale metadata section
#[derive(Debug, Clone, Deserialize)]
pub struct LocaleMeta {
    pub code: String,
    pub name: String,
    pub native: String,
    pub direction: String,
    pub status: String,
}

/// Full locale structure
#[derive(Debug, Clone, Deserialize)]
pub struct LocaleFile {
    pub meta: LocaleMeta,

    #[serde(flatten)]
    pub sections: HashMap<String, toml::Value>,
}

/// Runtime locale manager
#[derive(Debug, Clone)]
pub struct LocaleManager {
    locales: HashMap<String, LocaleFile>,
    fallback: String,
}

impl LocaleManager {
    /// Load locales from disk
    pub fn load() -> Result<Self> {
        let mut manager = Self {
            locales: HashMap::new(),
            fallback: "en".to_string(),
        };

        for dir in Self::locale_search_paths()? {
            if dir.exists() {
                manager.load_from_dir(&dir)?;
            }
        }

        if !manager.locales.contains_key("en") {
            return Err(anyhow::anyhow!(
                "Fallback locale 'en' not found in locales directory"
            ));
        }

        Ok(manager)
    }

    /// Get translated string
    pub fn t(&self, locale: &str, key: &str) -> String {
        self.lookup(locale, key)
            .or_else(|| self.lookup(&self.fallback, key))
            .unwrap_or_else(|| key.to_string())
    }

    /// Get available locale codes
    pub fn available_locales(&self) -> Vec<String> {
        let mut list: Vec<String> = self.locales.keys().cloned().collect();
        list.sort();
        list
    }

    /// Get locale metadata
    pub fn meta(&self, code: &str) -> Option<&LocaleMeta> {
        self.locales.get(code).map(|l| &l.meta)
    }

    /// Internal lookup
    fn lookup(&self, locale: &str, key: &str) -> Option<String> {
        let locale_file = self.locales.get(locale)?;

        let parts: Vec<&str> = key.split('.').collect();

        let mut current: Option<&toml::Value> = None;

        for (i, part) in parts.iter().enumerate() {
            if i == 0 {
                current = locale_file.sections.get(*part);
            } else {
                current = current?.get(*part);
            }
        }

        current?.as_str().map(|s| s.to_string())
    }

    /// Load locales from a directory
    fn load_from_dir(&mut self, dir: &Path) -> Result<()> {
        for entry in fs::read_dir(dir)
            .with_context(|| format!("Failed to read locale directory {}", dir.display()))?
        {
            let entry = entry?;
            let path = entry.path();

            if path.extension().and_then(|s| s.to_str()) != Some("toml") {
                continue;
            }

            let locale = Self::load_file(&path)?;
            let code = locale.meta.code.clone();

            self.locales.insert(code, locale);
        }

        Ok(())
    }

    /// Load a single locale file
    fn load_file(path: &Path) -> Result<LocaleFile> {
        let content = fs::read_to_string(path)
            .with_context(|| format!("Failed to read locale file {}", path.display()))?;

        let locale: LocaleFile = toml::from_str(&content)
            .with_context(|| format!("Failed to parse locale file {}", path.display()))?;

        Ok(locale)
    }

    /// Determine search paths
    fn locale_search_paths() -> Result<Vec<PathBuf>> {
        let mut paths = Vec::new();

        // ./locales
        if let Ok(current) = std::env::current_dir() {
            paths.push(current.join("locales"));
        }

        // executable_dir/locales
        if let Ok(exe) = std::env::current_exe() {
            if let Some(dir) = exe.parent() {
                paths.push(dir.join("locales"));
            }
        }

        // %APPDATA%/aion/locales
        if let Some(config_dir) = dirs::config_dir() {
            paths.push(config_dir.join("aion").join("locales"));
        }

        Ok(paths)
    }
}

/// Global locale instance
static mut GLOBAL_LOCALE: Option<LocaleManager> = None;

/// Initialize locale system
pub fn init() -> Result<()> {
    let manager = LocaleManager::load()?;

    unsafe {
        GLOBAL_LOCALE = Some(manager);
    }

    Ok(())
}

/// Get translated string from global locale
pub fn t(locale: &str, key: &str) -> String {
    unsafe {
        GLOBAL_LOCALE
            .as_ref()
            .map(|m| m.t(locale, key))
            .unwrap_or_else(|| key.to_string())
    }
}

/// Get available locales
pub fn available_locales() -> Vec<String> {
    unsafe {
        GLOBAL_LOCALE
            .as_ref()
            .map(|m| m.available_locales())
            .unwrap_or_default()
    }
}