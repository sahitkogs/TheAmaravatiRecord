# Chatbot: "Ask The Record"

Every page includes an AI chatbot widget powered by [chatbot-in-html](https://github.com/sahitkogs/chatbot-in-html).

| Feature | Detail |
|---------|--------|
| **Model** | Qwen3-0.6B via WebLLM (runs in browser, no API key) |
| **Theme** | Cream/ink palette, serif fonts, dark-red accent, dark-mode aware |
| **Mobile** | Full-width chat window, bubble stays visible when open |
| **Persistence** | Conversation carries across all pages (shared localStorage) |
| **Suggestions** | Page-specific chips re-appear after every response |
| **Backend toggle** | Users can switch between Local (WebLLM) and Cloud |

## WebLLM Loading Strategy

Loading is handled differently on desktop and mobile to avoid slowing down page loads on phones:

| | Desktop | Mobile (first visit) | Mobile (repeat visits) |
|-|---------|---------------------|----------------------|
| **On page load** | Preload engine in background | Download model to cache in background | Do nothing |
| **On chatbot open** | Instant (already loaded) | Engine initializes from cache | Engine initializes from cache |
| **GPU memory** | Allocated on page load | Freed after caching, re-allocated on chat open | Allocated only on chat open |

Mobile is detected via `matchMedia('(max-width: 600px)')`. First-visit status is tracked in localStorage. After the first visit downloads and caches the model weights, the engine is torn down to free GPU memory. On subsequent visits, nothing happens until the user taps the chat bubble.
