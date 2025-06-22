# LLM Calculator

A simple GUI calculator app that uses Claude API to perform mathematical calculations. Instead of evaluating expressions locally, all calculations are sent to Claude for processing.

## Features

- **GUI Interface**: Clean tkinter-based calculator with digit buttons (0-9), operators (+, -, *, /, =), decimal point, Clear, and Close buttons
- **Expression Display**: Shows the current mathematical expression being built
- **Result Display**: Shows the calculated result from Claude API
- **LLM-Powered**: All calculations are performed by Claude API, not local evaluation
- **Clear Function**: Reset the calculator display
- **Close Function**: Immediately exits the application

## Requirements

- Python 3.6 or higher
- tkinter (included with Python)
- anthropic library (for real Claude API integration)

## Quick Start

1. **Run the calculator directly:**
   ```bash
   python3 calculator.py
   ```

2. **Or use the setup script:**
   ```bash
   python3 run.py
   ```

## Usage

1. Click digit buttons (0-9) and operator buttons (+, -, *, /) to build your mathematical expression
2. The expression will be displayed in the "Expression" field
3. Click "=" to send the expression to Claude for calculation
4. The result will appear in the "Result" field
5. Click "Clear" to reset both fields
6. Click "Close" to exit the application

## API Integration

The calculator can work in two modes:

### 1. Simulation Mode (Default)
- Works out of the box without API keys
- Uses local evaluation for demonstration
- Perfect for testing the UI and functionality

### 2. Real Claude API Mode
- Uses actual Claude API for calculations
- Requires Anthropic API key

**To enable real Claude API:**

1. Install the anthropic library:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your actual Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-actual-api-key-here
   ```

4. The calculator will automatically detect the API key and use real Claude API

**Environment Variables:**
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required for real API)
- `CLAUDE_MODEL` - Claude model to use (default: claude-3-sonnet-20240229)
- `CLAUDE_MAX_TOKENS` - Maximum tokens for response (default: 100)
- `CLAUDE_TIMEOUT` - API timeout in seconds (default: 30)

## Example

- Enter: `12 + 7.5 / 3`
- The app sends to Claude: "What is the result of this calculation: 12 + 7.5 / 3?"
- Claude responds with the calculated result
- Result displayed: `14.5`

## Architecture

- **GUI**: tkinter for cross-platform GUI
- **Event Handling**: Button clicks build expression string
- **API Communication**: HTTP requests to Claude API
- **Result Parsing**: Extracts numerical result from Claude's text response

## Files

- `calculator.py` - Main calculator application
- `run.py` - Setup and run script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys, configuration)
- `.env.example` - Example environment file template
- `.gitignore` - Git ignore file (keeps secrets safe)
- `README.md` - This documentation

## Security

- Your `.env` file containing API keys is automatically ignored by git
- Never commit API keys to version control
- Use the provided `.env.example` as a template
