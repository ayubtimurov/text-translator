# Copilot Instructions for text-translator

## Project Overview
A Telegram bot application for translating text between multiple languages. The bot provides an interactive interface with language selection via Telegram's inline keyboards and conversation handlers.

## Architecture & Key Components

### Main Flow (main.py)
- **Entry point**: `main()` function at bottom - initializes Application and sets up handlers
- **State management**: Uses `ConversationHandler` for multi-step flows (input_language, output_language selections)
- **Handler patterns**: Command handlers → Message handlers (text input) → Callback handlers (button clicks)
- **Language data**: `LANGUAGES` dict (lines 87-108) is the single source of truth - maps ISO codes to display names with flags

### Conversation Handlers (ConversationHandler pattern)
Two identical flows exist for input/output language selection:
1. `/set_input_language` → user types language name → search matches → callback selection
2. `/set_output_language` → identical flow with `output_` prefix functions

**Critical state constant**: `SELECTING_LANGUAGE = 1` (line 85) - used across both handlers

### UI Language Handler
- Single callback handler (`ui_language_callback`) - handles all language buttons from `/ui_language` command
- Returns localized responses based on `callback_data` pattern `lang_{code}`

## Development Workflows

### Setup
```bash
# Requires Python 3.13+ (from pyproject.toml)
python -m venv .venv && source .venv/bin/activate
pip install -e .  # or: uv sync
```

### Environment Configuration
- Copy `.env` template: `TELEGRAM_BOT_TOKEN=<your_token>`
- Uses `python-dotenv` to load from `.env` (line 5-6)

### Running
```bash
python main.py
```
Bot runs in polling mode (long-polling, not webhooks).

### Dependencies
- `python-telegram-bot>=22.5`: Telegram Bot API bindings (core framework)
- `python-dotenv>=1.2.1`: Environment variable loading

## Project Conventions & Patterns

### Naming Conventions
- **Callback patterns**: `lang_{language_code}` + `lang_cancel` (used in regex pattern `^lang_`)
- **Function prefixes**: `set_*` (command entry), `search_*` (message handlers), `*_selected` (callbacks), `*_cancel` (fallbacks)
- **States**: All-caps constants (SELECTING_LANGUAGE)

### Anti-patterns Currently Present
- **Code duplication**: `set_input_language` and `set_output_language` functions are identical (lines 104-110 vs 161-167)
- **search_input_language` and `search_output_language` are nearly identical (consider refactoring to parameterized function)
- **Missing storage**: No persistent state for selected languages (use `context.user_data` for per-user selection storage)

### Async Patterns
- All handlers are `async` functions - awaits Telegram API calls with `.reply_text()`, `.edit_message_text()`, `.answer()`
- No blocking operations present

## Integration Points

### Telegram Bot API (python-telegram-bot library)
- **Update object**: Contains message, callback_query, etc.
- **ContextTypes.DEFAULT_TYPE**: Thread-safe context object - use `context.user_data` dict for user-specific state
- **Callback data limitation**: 64-byte max - current `lang_{code}` fits, but plan accordingly if expanding

### External Configuration
- Token loaded from `.env` → `TOKEN` global (line 7)
- No API keys for translation service currently integrated

## Next Development Steps (Observable Incomplete Features)
- **Translation execution**: No actual translation logic after language selection
- **User preferences persistence**: Selected languages not stored in context.user_data
- **Translation API integration**: Need to add binding to translation service (Google Translate, etc.)
- **Error handling**: Minimal error handling for token missing or Telegram API failures

## Testing Considerations
- Inline keyboard rendering requires Telegram client (hard to unit test without mocks)
- Consider extracting language search logic to separate module for testing
- Mock `Update`, `ContextTypes`, and async patterns using pytest-asyncio
