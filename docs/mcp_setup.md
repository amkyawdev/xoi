# MCP Setup Guide

Guide for setting up Model Context Protocol (MCP) integrations.

## Overview

Amkyaw AI Agent supports MCP for extended capabilities:

- **Browser Automation** - Control headless browsers via Browserless
- **Web Search** - Search the web via RapidAPI
- **Telegram** - Send messages via Telegram Bot

## Browserless Setup

### 1. Create Account

1. Sign up at [browserless.io](https://browserless.io)
2. Choose a plan (Free tier available)
3. Copy your API key

### 2. Configure

Add to your `.env` file:

```env
BROWSERLESS_API_KEY=your-api-key
```

### 3. Usage

The browser automation tool can:
- Navigate to URLs
- Take screenshots
- Execute JavaScript
- Extract page content

## RapidAPI Setup

### 1. Create Account

1. Sign up at [rapidapi.com](https://rapidapi.com)
2. Subscribe to a web search API (e.g., Google Search API)
3. Copy your API key

### 2. Configure

Add to your `.env` file:

```env
RAPIDAPI_KEY=your-api-key
```

### 3. Usage

Web search enables the agent to:
- Research topics
- Find current information
- Answer questions about recent events

## Telegram Setup

### 1. Create Bot

1. Open Telegram and search for @BotFather
2. Send `/newbot`
3. Follow the prompts
4. Copy your bot token

### 2. Configure

Add to your `.env` file:

```env
TELEGRAM_BOT_TOKEN=your-bot-token
```

### 3. Usage

Telegram integration allows:
- Sending messages to users
- Receiving updates
- Building custom bots

## OpenAI Setup

### 1. Get API Key

1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Go to API Keys
3. Create a new secret key
4. Copy the key

### 2. Configure

Add to your `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key
AI_MODEL=gpt-4o
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=4096
```

### 3. Models

Available models:
- `gpt-4o` - Most capable
- `gpt-4-turbo` - Faster, cheaper
- `gpt-3.5-turbo` - Fastest, most affordable

## Environment Variables Summary

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `AI_MODEL` | No | Model to use (default: gpt-4o) |
| `AI_TEMPERATURE` | No | Response creativity (0-1, default: 0.7) |
| `AI_MAX_TOKENS` | No | Max response length (default: 4096) |
| `BROWSERLESS_API_KEY` | No | Browser automation |
| `RAPIDAPI_KEY` | No | Web search |
| `TELEGRAM_BOT_TOKEN` | No | Telegram integration |
| `DATABASE_URL` | No | PostgreSQL database |
| `SECRET_KEY` | Yes | JWT signing key |
