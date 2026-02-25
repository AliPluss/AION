use crate::config::{allowed_languages, AppConfig, ProviderKind};
use anyhow::{anyhow, Result};
use crossterm::{
    event::{self, Event, KeyCode, KeyEventKind},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{Block, Borders, List, ListItem, ListState, Paragraph, Wrap},
    Frame, Terminal,
};
use std::io::{self, Stdout};
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Step {
    Language,
    Provider,
    Model,
    Summary,
}

impl Step {
    fn title(self) -> &'static str {
        match self {
            Step::Language => "Step 1/4: Language",
            Step::Provider => "Step 2/4: Provider",
            Step::Model => "Step 3/4: Model",
            Step::Summary => "Step 4/4: Summary",
        }
    }

    fn prev(self) -> Option<Self> {
        match self {
            Step::Language => None,
            Step::Provider => Some(Step::Language),
            Step::Model => Some(Step::Provider),
            Step::Summary => Some(Step::Model),
        }
    }

    fn next(self) -> Option<Self> {
        match self {
            Step::Language => Some(Step::Provider),
            Step::Provider => Some(Step::Model),
            Step::Model => Some(Step::Summary),
            Step::Summary => None,
        }
    }
}

struct TerminalGuard;

impl TerminalGuard {
    fn enter() -> Result<Self> {
        enable_raw_mode()?;
        execute!(io::stdout(), EnterAlternateScreen)?;
        Ok(Self)
    }
}

impl Drop for TerminalGuard {
    fn drop(&mut self) {
        let _ = disable_raw_mode();
        let _ = execute!(io::stdout(), LeaveAlternateScreen);
    }
}

#[derive(Debug, Clone)]
struct LangOption {
    code: &'static str,
    name: &'static str,
    supported: bool,
}

#[derive(Debug, Clone)]
struct UiState {
    step: Step,
    status: String,

    lang_state: ListState,
    provider_state: ListState,

    model_input: String,

    use_colors: bool,
    use_animation: bool,

    tick: u64,
    last_tick: Instant,
}

impl UiState {
    fn new(existing: &AppConfig) -> Self {
        let langs = language_options();
        let providers = provider_options();

        let mut lang_state = ListState::default();
        let lang_idx = langs
            .iter()
            .position(|x| x.code == existing.language.as_str())
            .unwrap_or(0);
        lang_state.select(Some(lang_idx));

        let mut provider_state = ListState::default();
        let provider_idx = providers
            .iter()
            .position(|p| *p == existing.provider.kind)
            .unwrap_or(0);
        provider_state.select(Some(provider_idx));

        Self {
            step: Step::Language,
            status:
                "↑↓ Navigate | Enter Next | Esc/Backspace/← Back | q Quit | C Colors | A Animation"
                    .to_string(),
            lang_state,
            provider_state,
            model_input: existing.provider.model.clone(),
            use_colors: true,
            use_animation: true,
            tick: 0,
            last_tick: Instant::now(),
        }
    }
}

/* ---------------------------
   Customization points
   - Add languages in language_options()
   - Add providers in provider_options()
   - Adjust UI strings in help_text()
---------------------------- */

fn language_options() -> Vec<LangOption> {
    let supported = allowed_languages();

    // Add more languages here. Only supported languages will be selectable until config allows them.
    // When you expand config/mod.rs allowed_languages(), these will automatically become selectable.
    let all = vec![
        ("en", "English"),
        ("ar", "العربية"),
        ("no", "Norsk"),
        ("zh", "中文"),
        ("es", "Español"),
        ("fr", "Français"),
        ("de", "Deutsch"),
        ("tr", "Türkçe"),
        ("ru", "Русский"),
        ("ja", "日本語"),
        ("ko", "한국어"),
    ];

    all.into_iter()
        .map(|(code, name)| LangOption {
            code,
            name,
            supported: supported.contains(code),
        })
        .collect()
}

fn provider_options() -> Vec<ProviderKind> {
    // Add more providers here.
    vec![
        ProviderKind::Ollama,
        ProviderKind::OpenAI,
        ProviderKind::Claude,
        ProviderKind::OpenRouter,
    ]
}

fn provider_name(p: &ProviderKind) -> &'static str {
    match p {
        ProviderKind::Ollama => "Ollama",
        ProviderKind::OpenAI => "OpenAI",
        ProviderKind::Claude => "Claude",
        ProviderKind::OpenRouter => "OpenRouter",
    }
}

fn help_text(step: Step) -> Text<'static> {
    let lines: Vec<Line> = match step {
        Step::Language => vec![
            Line::from("Choose the UI language for AION."),
            Line::from(""),
            Line::from("Keys: ↑↓ move, Enter next"),
            Line::from("Back: Esc / Backspace / ← / b"),
            Line::from("Quit: q (without saving)"),
            Line::from("Toggle: C colors, A animation"),
            Line::from(""),
            Line::from("Note: Non-supported languages are shown but not selectable yet."),
        ],
        Step::Provider => vec![
            Line::from("Choose your AI provider."),
            Line::from(""),
            Line::from("Keys: ↑↓ move, Enter next"),
            Line::from("Back: Esc / Backspace / ← / b"),
            Line::from("Quit: q (without saving)"),
        ],
        Step::Model => vec![
            Line::from("Type the model name."),
            Line::from(""),
            Line::from("Examples:"),
            Line::from(" - Ollama: mistral, llama3, qwen2.5"),
            Line::from(" - OpenAI: gpt-4o-mini, gpt-4.1"),
            Line::from(" - Claude: claude-3.5-sonnet"),
            Line::from(" - OpenRouter: meta-llama/llama-3.1-70b-instruct"),
            Line::from(""),
            Line::from("Keys: type, Backspace delete, Enter next"),
            Line::from("Back: Esc / Backspace / ← / b"),
            Line::from("Quit: q (without saving)"),
        ],
        Step::Summary => vec![
            Line::from("Review settings."),
            Line::from("Enter = Save & exit"),
            Line::from("Back: Esc / Backspace / ← / b"),
            Line::from("Quit: q (without saving)"),
            Line::from(""),
            Line::from("Cargo tip: pass args after --"),
            Line::from("Example: cargo run -p aion -- --setup"),
        ],
    };
    Text::from(lines)
}

/* ---------------------------
   Animation (pip-like)
---------------------------- */

fn spinner_frame(tick: u64) -> char {
    let frames = ['|', '/', '-', '\\'];
    frames[(tick as usize) % frames.len()]
}

fn dots_frame(tick: u64) -> &'static str {
    let frames = ["", ".", "..", "...", "..", "."];
    frames[(tick as usize) % frames.len()]
}

/* ---------------------------
   Styles and indicators
---------------------------- */

fn s_title(ui: &UiState) -> Style {
    if ui.use_colors {
        Style::default()
            .fg(Color::Cyan)
            .add_modifier(Modifier::BOLD)
    } else {
        Style::default().add_modifier(Modifier::BOLD)
    }
}

fn s_help_title(ui: &UiState) -> Style {
    if ui.use_colors {
        Style::default().fg(Color::Cyan)
    } else {
        Style::default()
    }
}

fn s_active(ui: &UiState) -> Style {
    if ui.use_colors {
        Style::default().fg(Color::Green)
    } else {
        Style::default()
    }
}

fn s_cursor(ui: &UiState) -> Style {
    if ui.use_colors {
        Style::default()
            .fg(Color::Cyan)
            .add_modifier(Modifier::BOLD)
    } else {
        Style::default().add_modifier(Modifier::BOLD)
    }
}

fn s_inactive(ui: &UiState) -> Style {
    if ui.use_colors {
        Style::default().fg(Color::Red)
    } else {
        Style::default()
    }
}

fn dot_span(ui: &UiState, is_cursor: bool, is_active: bool, is_valid: bool) -> Span<'static> {
    let symbol = "● ";
    if !ui.use_colors {
        return Span::raw(symbol);
    }

    // Priority: cursor (cyan) > active (green) > invalid/inactive (red)
    if is_cursor {
        Span::styled(symbol, s_cursor(ui))
    } else if is_active && is_valid {
        Span::styled(symbol, s_active(ui).add_modifier(Modifier::BOLD))
    } else {
        Span::styled(symbol, s_inactive(ui).add_modifier(Modifier::BOLD))
    }
}

fn step_dots(ui: &UiState, draft: &AppConfig) -> Line<'static> {
    let langs = language_options();
    let lang_done = langs
        .iter()
        .any(|l| l.code == draft.language.as_str() && l.supported);

    let provider_done = true; // provider is always set to some value
    let model_done = !draft.provider.model.trim().is_empty();

    let dot = |active: bool, done: bool| -> Span<'static> {
        if !ui.use_colors {
            return Span::raw("●");
        }
        let color = if active {
            Color::Cyan
        } else if done {
            Color::Green
        } else {
            Color::Red
        };
        Span::styled("●", Style::default().fg(color))
    };

    let d1 = dot(ui.step == Step::Language, lang_done);
    let d2 = dot(ui.step == Step::Provider, provider_done);
    let d3 = dot(ui.step == Step::Model, model_done);
    let d4 = dot(ui.step == Step::Summary, lang_done && provider_done && model_done);

    Line::from(vec![
        Span::raw(" "),
        d1,
        Span::raw(" "),
        d2,
        Span::raw(" "),
        d3,
        Span::raw(" "),
        d4,
    ])
}

fn block_with_steps(title: &str, ui: &UiState, draft: &AppConfig) -> Block<'static> {
    if ui.use_colors {
        let mut spans = vec![
            Span::styled(
                title.to_string(),
                Style::default()
                    .fg(Color::Cyan)
                    .add_modifier(Modifier::BOLD),
            ),
            Span::raw("  "),
        ];
        spans.extend(step_dots(ui, draft).spans);
        Block::default()
            .borders(Borders::ALL)
            .title(Line::from(spans))
    } else {
        Block::default()
            .borders(Borders::ALL)
            .title(Line::from(format!("{title}  [1][2][3][4]")))
    }
}

/* ---------------------------
   Public entry
---------------------------- */

pub fn run(existing: &AppConfig) -> Result<AppConfig> {
    let _guard = TerminalGuard::enter().map_err(|e| {
        anyhow!(
            "Failed to initialize terminal UI. Try Windows Terminal or VS Code terminal. Error: {}",
            e
        )
    })?;

    let stdout: Stdout = io::stdout();
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;
    terminal.clear()?;

    let mut ui = UiState::new(existing);
    let mut draft = existing.clone();

    let tick_rate = Duration::from_millis(90);

    loop {
        // Animation tick
        if ui.use_animation && ui.last_tick.elapsed() >= tick_rate {
            ui.tick = ui.tick.wrapping_add(1);
            ui.last_tick = Instant::now();
        }

        terminal.draw(|f| draw_ui(f, &ui, &draft))?;

        if event::poll(Duration::from_millis(60))? {
            let ev = event::read()?;
            if let Event::Key(key) = ev {
                if key.kind != KeyEventKind::Press {
                    continue;
                }

                // Global toggles
                match key.code {
                    KeyCode::Char('c') | KeyCode::Char('C') => {
                        ui.use_colors = !ui.use_colors;
                        ui.status = format!(
                            "Colors: {} | Animation: {}",
                            if ui.use_colors { "ON" } else { "OFF" },
                            if ui.use_animation { "ON" } else { "OFF" }
                        );
                        continue;
                    }
                    KeyCode::Char('a') | KeyCode::Char('A') => {
                        ui.use_animation = !ui.use_animation;
                        ui.status = format!(
                            "Colors: {} | Animation: {}",
                            if ui.use_colors { "ON" } else { "OFF" },
                            if ui.use_animation { "ON" } else { "OFF" }
                        );
                        continue;
                    }
                    KeyCode::Char('q') => return Err(anyhow!("Wizard cancelled by user")),
                    _ => {}
                }

                // Back navigation
                if matches!(
                    key.code,
                    KeyCode::Esc | KeyCode::Backspace | KeyCode::Left | KeyCode::Char('b')
                ) {
                    if let Some(prev) = ui.step.prev() {
                        ui.step = prev;
                        ui.status = "Back to previous step".to_string();
                    } else {
                        // If already at the first step, treat as cancel
                        return Err(anyhow!("Wizard cancelled by user"));
                    }
                    continue;
                }

                // Step handlers
                match ui.step {
                    Step::Language => handle_language_step(&mut ui, &mut draft, key.code),
                    Step::Provider => handle_provider_step(&mut ui, &mut draft, key.code),
                    Step::Model => handle_model_step(&mut ui, &mut draft, key.code),
                    Step::Summary => {
                        if key.code == KeyCode::Enter {
                            draft.validate()?;
                            return Ok(draft);
                        }
                    }
                }
            }
        }
    }
}

/* ---------------------------
   Step handlers
---------------------------- */

fn handle_language_step(ui: &mut UiState, draft: &mut AppConfig, code: KeyCode) {
    let langs = language_options();
    let max = langs.len().saturating_sub(1);

    match code {
        KeyCode::Up => {
            let cur = ui.lang_state.selected().unwrap_or(0);
            ui.lang_state.select(Some(cur.saturating_sub(1)));
        }
        KeyCode::Down => {
            let cur = ui.lang_state.selected().unwrap_or(0);
            ui.lang_state.select(Some((cur + 1).min(max)));
        }
        KeyCode::Enter => {
            let idx = ui.lang_state.selected().unwrap_or(0);
            if let Some(sel) = langs.get(idx) {
                if !sel.supported {
                    ui.status = "This language is not supported yet".to_string();
                    return;
                }
                draft.language = sel.code.to_string();
                if let Some(next) = ui.step.next() {
                    ui.step = next;
                }
                ui.status = "Language selected".to_string();
            }
        }
        _ => {}
    }
}

fn handle_provider_step(ui: &mut UiState, draft: &mut AppConfig, code: KeyCode) {
    let providers = provider_options();
    let max = providers.len().saturating_sub(1);

    match code {
        KeyCode::Up => {
            let cur = ui.provider_state.selected().unwrap_or(0);
            ui.provider_state.select(Some(cur.saturating_sub(1)));
        }
        KeyCode::Down => {
            let cur = ui.provider_state.selected().unwrap_or(0);
            ui.provider_state.select(Some((cur + 1).min(max)));
        }
        KeyCode::Enter => {
            let idx = ui.provider_state.selected().unwrap_or(0);
            if let Some(kind) = providers.get(idx).cloned() {
                draft.provider.kind = kind;
                if let Some(next) = ui.step.next() {
                    ui.step = next;
                }
                ui.status = "Provider selected".to_string();
            }
        }
        _ => {}
    }
}

fn handle_model_step(ui: &mut UiState, draft: &mut AppConfig, code: KeyCode) {
    match code {
        KeyCode::Backspace => {
            ui.model_input.pop();
            draft.provider.model = ui.model_input.clone();
        }
        KeyCode::Enter => {
            let trimmed = ui.model_input.trim();
            if trimmed.is_empty() {
                ui.status = "Model cannot be empty".to_string();
            } else {
                draft.provider.model = trimmed.to_string();
                if let Some(next) = ui.step.next() {
                    ui.step = next;
                }
                ui.status = "Model selected".to_string();
            }
        }
        KeyCode::Char(c) => {
            if !c.is_control() {
                ui.model_input.push(c);
                draft.provider.model = ui.model_input.clone();
            }
        }
        _ => {}
    }
}

/* ---------------------------
   Rendering
---------------------------- */

fn draw_ui(f: &mut Frame, ui: &UiState, draft: &AppConfig) {
    let size = f.size();

    let outer = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Length(3), Constraint::Min(10), Constraint::Length(3)])
        .split(size);

    // Header
    let header_text = if ui.use_animation {
        format!("{}  {}{}", ui.step.title(), spinner_frame(ui.tick), dots_frame(ui.tick))
    } else {
        ui.step.title().to_string()
    };

    let header = Paragraph::new(header_text)
        .style(s_title(ui))
        .block(Block::default().borders(Borders::ALL).title("AION Setup Wizard"))
        .wrap(Wrap { trim: true });
    f.render_widget(header, outer[0]);

    let mid = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Percentage(50), Constraint::Percentage(50)])
        .split(outer[1]);

    // Help panel
    let help = Paragraph::new(help_text(ui.step))
        .block(
            Block::default()
                .borders(Borders::ALL)
                .title(Span::styled("Help", s_help_title(ui))),
        )
        .wrap(Wrap { trim: true });
    f.render_widget(help, mid[1]);

    // Footer
    let footer_text = if ui.use_animation {
        format!("{} {}", spinner_frame(ui.tick), ui.status)
    } else {
        ui.status.clone()
    };
    let footer = Paragraph::new(footer_text)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .title(Span::styled("Status", s_help_title(ui))),
        )
        .wrap(Wrap { trim: true });
    f.render_widget(footer, outer[2]);

    // Left content
    match ui.step {
        Step::Language => render_language(f, ui, draft, mid[0]),
        Step::Provider => render_provider(f, ui, draft, mid[0]),
        Step::Model => render_model(f, ui, draft, mid[0]),
        Step::Summary => render_summary(f, ui, draft, mid[0]),
    }
}

fn render_language(f: &mut Frame, ui: &UiState, draft: &AppConfig, area: Rect) {
    let langs = language_options();
    let cursor = ui.lang_state.selected().unwrap_or(0);

    let items: Vec<ListItem> = langs
        .iter()
        .enumerate()
        .map(|(i, l)| {
            let is_cursor = i == cursor;
            let is_active = l.code == draft.language.as_str();
            let is_valid = l.supported;
            let dot = dot_span(ui, is_cursor, is_active, is_valid);

            let label = if l.supported {
                format!("{} ({})", l.name, l.code)
            } else {
                format!("{} ({}) - Not supported yet", l.name, l.code)
            };

            let label_style = if is_cursor {
                s_cursor(ui)
            } else if is_active && is_valid {
                s_active(ui)
            } else if !is_valid {
                s_inactive(ui)
            } else {
                Style::default()
            };

            ListItem::new(Line::from(vec![dot, Span::styled(label, label_style)]))
        })
        .collect();

    let list = List::new(items)
        .block(block_with_steps("Language", ui, draft))
        .highlight_symbol("");

    let mut state = ui.lang_state.clone();
    f.render_stateful_widget(list, area, &mut state);
}

fn render_provider(f: &mut Frame, ui: &UiState, draft: &AppConfig, area: Rect) {
    let providers = provider_options();
    let cursor = ui.provider_state.selected().unwrap_or(0);

    let items: Vec<ListItem> = providers
        .iter()
        .enumerate()
        .map(|(i, p)| {
            let is_cursor = i == cursor;
            let is_active = *p == draft.provider.kind;
            let dot = dot_span(ui, is_cursor, is_active, true);

            let label_style = if is_cursor {
                s_cursor(ui)
            } else if is_active {
                s_active(ui)
            } else {
                Style::default()
            };

            ListItem::new(Line::from(vec![
                dot,
                Span::styled(provider_name(p).to_string(), label_style),
            ]))
        })
        .collect();

    let list = List::new(items)
        .block(block_with_steps("Provider", ui, draft))
        .highlight_symbol("");

    let mut state = ui.provider_state.clone();
    f.render_stateful_widget(list, area, &mut state);
}

fn render_model(f: &mut Frame, ui: &UiState, draft: &AppConfig, area: Rect) {
    let parts = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Min(7), Constraint::Length(3)])
        .split(area);

    let is_valid = !ui.model_input.trim().is_empty();
    let dot = dot_span(ui, false, is_valid, is_valid);

    let title = format!("Model ({})", provider_name(&draft.provider.kind));
    let content = Line::from(vec![
        dot,
        Span::styled(
            ui.model_input.clone(),
            if ui.use_colors {
                Style::default()
                    .fg(Color::Yellow)
                    .add_modifier(Modifier::BOLD)
            } else {
                Style::default().add_modifier(Modifier::BOLD)
            },
        ),
    ]);

    let input = Paragraph::new(Text::from(vec![
        Line::from("Type model name then press Enter:"),
        Line::from(""),
        content,
    ]))
    .block(block_with_steps(&title, ui, draft))
    .wrap(Wrap { trim: false });

    f.render_widget(input, parts[0]);

    let keys = Paragraph::new("Enter Next | Esc/Backspace/←/b Back | q Quit")
        .block(Block::default().borders(Borders::ALL).title("Keys"))
        .wrap(Wrap { trim: true });

    f.render_widget(keys, parts[1]);
}

fn render_summary(f: &mut Frame, ui: &UiState, draft: &AppConfig, area: Rect) {
    let lines = vec![
        Line::from(vec![
            Span::styled("● ", if ui.use_colors { Style::default().fg(Color::Green) } else { Style::default() }),
            Span::raw(format!("Language: {}", draft.language)),
        ]),
        Line::from(vec![
            Span::styled("● ", if ui.use_colors { Style::default().fg(Color::Green) } else { Style::default() }),
            Span::raw(format!("Provider: {}", provider_name(&draft.provider.kind))),
        ]),
        Line::from(vec![
            Span::styled("● ", if ui.use_colors { Style::default().fg(Color::Green) } else { Style::default() }),
            Span::raw(format!("Model: {}", draft.provider.model)),
        ]),
        Line::from(""),
        Line::from("Enter = Save & exit"),
        Line::from("Esc/Backspace/←/b = Back"),
        Line::from("q = Quit without saving"),
    ];

    let p = Paragraph::new(Text::from(lines))
        .block(block_with_steps("Summary", ui, draft))
        .wrap(Wrap { trim: true });

    f.render_widget(p, area);
}