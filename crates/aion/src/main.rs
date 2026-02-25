//! AION CLI entrypoint.
//!
//! Notes:
//! - Keep main.rs small and stable.
//! - Prefer moving UI, localization, and configuration logic into modules.
//! - Rust module system reference:
//!   https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html

use anyhow::{Context, Result};
use std::io::{self, Write};
use std::time::{SystemTime, UNIX_EPOCH};

mod config;
mod tui;

// Optional i18n module. If you currently have an i18n module with init() -> Result<()>,
// you can enable it by uncommenting the two lines below.
// mod i18n;
// use crate::i18n as _i18n;

use crate::config::io::{load_or_create_config, save_config};

fn print_banner() {
    println!();
    println!("==============================================================");
    println!("                      AION CORE INITIALIZED                    ");
    println!("==============================================================");
    println!();
}

fn print_environment_info() {
    let os: &str = std::env::consts::OS;
    let arch: &str = std::env::consts::ARCH;

    println!("System Information:");
    println!("  OS Architecture : {}", arch);
    println!("  Operating System: {}", os);
    println!();
}

fn print_timestamp() {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(d) => println!("Startup Timestamp: {}", d.as_secs()),
        Err(_) => println!("Startup Timestamp: unavailable"),
    }
    println!();
}

fn print_config_summary(cfg: &config::AppConfig) {
    println!("Config loaded successfully");
    println!("Language: {}", cfg.language);
    println!("Provider: {:?}", cfg.provider.kind);
    println!("Model: {}", cfg.provider.model);
    println!();
}

fn prompt_ready() {
    print!("AION is ready > ");
    let _ = io::stdout().flush();
}

fn has_flag(name: &str) -> bool {
    std::env::args().any(|a| a == name)
}

fn main() -> Result<()> {
    // 1) Load (or create) config
    let mut cfg: config::AppConfig = load_or_create_config().context("failed to load or create config")?;

    // 2) Initialize localization (optional)
    // If you have i18n::init() implemented, you can enable this.
    // _i18n::init().context("failed to initialize locale")?;

    // 3) Print boot info
    print_banner();
    print_environment_info();
    print_timestamp();

    println!("Core Status: OK");
    println!("Runtime Status: OK");
    println!("Initialization Complete");
    println!();

    // 4) If user requests setup wizard
    if has_flag("--setup") {
        // The wizard is expected to return an updated config.
        // This assumes you have: pub fn run(existing: &AppConfig) -> Result<AppConfig>
        let updated: config::AppConfig =
            tui::wizard::run(&cfg).context("setup wizard failed")?;

        updated.validate().context("config validation failed")?;
        save_config(&updated).context("failed to save config")?;

        cfg = updated;

        // Optional: re-init i18n after changing cfg.language
        // _i18n::init().context("failed to re-initialize locale")?;
    }

    // 5) Show current config summary + ready prompt
    print_config_summary(&cfg);
    prompt_ready();

    Ok(())
}