# CS AI Agent - Supermarket Shopping Assistant

A voice AI shopping assistant for supermarkets built with [LiveKit Agents](https://github.com/livekit/agents) and [Google Gemini Realtime API](https://cloud.livekit.io/).

## Overview

**Siza** is your personal supermarket shopping assistant. She helps customers:

- **Browse Products** - Browse the full product catalog by category
- **Search Items** - Find specific products you're looking for
- **Create Shopping Lists** - Add items to your cart/shopping list
- **Place Orders** - Complete purchases directly through voice
- **Schedule Pickup** - Arrange to pick up your groceries after work
- **Delivery Options** - Request home delivery if preferred

Perfect for busy professionals who want to do their grocery shopping hands-free while commuting or multitasking.

## Features

- **Voice-First Interface** - Natural conversation with AI
- **Real-time Product Search** - Instant access to product catalog
- **Smart Cart Management** - Add, remove, and modify items
- **Flexible Fulfillment** - Pickup or delivery options
- **No Downloads Required** - Uses Gemini Realtime API (no local VAD/model downloads)

## Tech Stack

- [LiveKit Agents](https://github.com/livekit/agents) - Voice AI framework
- [Google Gemini Realtime API](https://docs.livekit.io/agents/models/realtime/plugins/gemini/) - LLM + STT + TTS in one model
- [LiveKit Cloud](https://cloud.livekit.io/) - WebRTC infrastructure
- Python 3.10+

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- LiveKit Cloud account
- Google AI Studio API key (for Gemini Realtime)

### Installation

```console
cd cs-ai-agent
uv sync
```

### Environment Setup

Copy `.env.example` to `.env.local` and fill in your credentials:

```bash
# LiveKit Cloud credentials
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Google Gemini API key
GOOGLE_API_KEY=your_google_api_key
```

### Run the Agent

**Console mode (speak directly in terminal):**
```console
uv run python src/agent.py console
```

**Development mode (connect via frontend/telephony):**
```console
uv run python src/agent.py dev
```

**Production mode:**
```console
uv run python src/agent.py start
```

## Usage Examples

> **User:** "Hi Siza, I need to do my grocery shopping"

> **Siza:** "Hello! I'd be happy to help you with your grocery shopping today. What would you like to get?"

> **User:** "I'm making pasta tonight. Can you add some ground beef, tomatoes, and spaghetti?"

> **Siza:** "Of course! I've added 1 lb ground beef, 2 cans of tomatoes, and 1 box of spaghetti to your cart. Would you like anything else?"

> **User:** "Yes, add some garlic bread and parmesan cheese"

> **Siza:** "Got it - garlic bread and parmesan cheese added. Your total is looking good so far. Would you like to complete your order?"

> **User:** "Yes, I'll pick it up after work"

> **Siza:** "Perfect! Your order will be ready for pickup at 5 PM today. Just mention your name at the checkout counter. Is there anything else you need?"

## Project Structure

```
cs-ai-agent/
├── src/
│   ├── agent.py          # Main agent code
│   └── ...
├── livekit.toml          # LiveKit configuration
├── pyproject.toml        # Python dependencies
├── Dockerfile            # Production container
└── README.md
```

## Deployment

This project is production-ready. Deploy to LiveKit Cloud:

```bash
uv run python src/agent.py start
```

Or use the included Dockerfile for custom deployment.

## License

MIT License - see [LICENSE](LICENSE) file for details.
