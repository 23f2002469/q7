Run a local LLM (e.g. **Ollama**) that exposes an **OpenAI-compatible** chat completions endpoint, expose it via a public tunnel, and submit the endpoint URL plus the model name. The grader sends two fresh prompts every check — an echo test and an arithmetic test.

**Required setup:**

-   Start Ollama (or any compatible server) so that `POST /v1/chat/completions` is accessible at your tunnel URL.
-   Request format: `{"model": "…", "messages": [{"role": "user", "content": "…"}], "stream": false}`
-   Response format: standard OpenAI structure — content is read from `choices[0].message.content` (or `choices[0].text` / top-level `response` as fallback).
-   Enable CORS on your tunnel so this page can reach it directly (e.g. `OLLAMA_ORIGINS=*` for Ollama).

**What the grader checks:**

1.  **Echo test:** asks the model to repeat a random token (format `TK<6-hex>`). The token must appear somewhere in the response (case-insensitive).
2.  **Arithmetic test:** asks "What is A + B?" with random integers (10-89). The correct sum must appear as digits in the response.

**Submit as JSON:**

{"url": "https://my-llm.trycloudflare.com/v1/chat/completions", "model": "llama3.2"}

-   `url` — the full path to `/v1/chat/completions` at your tunnel.
-   `model` — the exact model name your server is running.

**Your endpoint + model as JSON**
