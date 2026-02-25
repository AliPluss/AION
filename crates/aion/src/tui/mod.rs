pub mod wizard;

use crate::config::AppConfig;
use anyhow::Result;

pub fn run_wizard(existing: &AppConfig) -> Result<AppConfig> {
    wizard::run(existing)
}