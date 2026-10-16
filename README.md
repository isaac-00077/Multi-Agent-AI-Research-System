# Aetheris // Multi-Agent AI Research System 🌌

An autonomous multi-agent research constellation powered by **LangChain**, **Groq Cloud LLMs**, **Tavily Web Search**, and an interactive **Three.js WebGL Quantum Constellation** interface.

---

## ⚡ Overview

Aetheris coordinates four specialized AI agents to execute deep, fact-checked research on any user-provided topic. The system combines real-time internet search, dynamic webpage content scraping, structured multi-section report drafting, and an adversarial critique with an automated numeric score.

---

## 🧠 System Architecture & Agent Swarm

```
                        +------------------------------------+
                        |       WebGL 3D Visualizer          |
                        |   Three.js Real-Time Particle UI   |
                        +-----------------+------------------+
                                          |
                                          | HTTP SSE Stream
                                          v
                        +------------------------------------+
                        |         server.py (aiohttp)        |
                        |     Async Event-Stream Engine      |
                        +-----------------+------------------+
                                          |
                                          | Thread Bridge
                                          v
                        +------------------------------------+
                        |        pipeline.py (Runner)        |
                        +-----------------+------------------+
                                          |
        +------------------+--------------+---------------+------------------+
        |                  |                              |                  |
        v                  v                              v                  v
+---------------+  +---------------+              +---------------+  +---------------+
| 🔍 Step 1     |  | 📖 Step 2     |              | ✍️ Step 3     |  | ⚖️ Step 4     |
| Search Agent  |  | Reader Agent  |              | Writer Agent  |  | Critic Agent  |
| (Tavily Tool) |  | (BS4 Scraper) |              | (Groq LLM)    |  | (Adversarial) |
+---------------+  +---------------+              +---------------+  +---------------+
```

### The 4 Specialized Agents:

1. **🔍 Search Agent** (`build_search_agent`):
   - Queries live internet sources via Tavily API.
   - Extracts top authoritative sources, snippets, and verified URLs.

2. **📖 Reader / Scraper Agent** (`build_scrape_agent`):
   - Analyzes search results and autonomously selects the most relevant URL.
   - Extracts, cleans, and strips HTML boilerplate (scripts, styles, navs, footers) to gather dense body text up to 3,000 characters.

3. **✍️ Synthesis Writer** (`writer_chain`):
   - Fuses search intelligence and scraped content.
   - Synthesizes a structured 4-part research dossier:
     - `## Introduction`
     - `## Key Findings` (minimum 3 well-grounded points)
     - `## Conclusion`
     - `## Sources` (traceable reference links)

4. **⚖️ Adversarial Critic** (`critic_chain`):
   - Stress-tests the drafted dossier for hallucinations, unsupported claims, and structural rigor.
   - Outputs an objective score (`Score: X/10`), explicit strengths, areas to improve, and a final verdict.

---

## 📂 Project Structure

```
.
├── agents.py           # LangChain agent definitions (Search, Scrape, Writer, Critic)
├── pipeline.py         # Multi-agent orchestrator & real-time SSE stream generator
├── server.py           # aiohttp async web server with CORS and SSE streaming
├── tools.py            # Agent tools (Tavily search & BeautifulSoup HTML scraper)
├── index.html          # Single-page Three.js WebGL UI & live telemetry dashboard
├── config.js           # Frontend runtime configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # Project documentation
```

---

## 🛠️ Local Setup & Running

### 1. Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- A [Groq API Key](https://console.groq.com/keys)
- A [Tavily API Key](https://tavily.com)

### 2. Clone and Setup Environment

```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the `.env.example` template to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
TAVILY_API_KEY=tvly-your_tavily_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
PORT=8000
```

### 4. Run the Web Application

```bash
python server.py
```

The application will start on `http://localhost:8000` and automatically open your default browser.

### 5. CLI Testing Mode (Optional)

You can also run the research pipeline directly inside your terminal without the web interface:

```bash
python pipeline.py
```

You will be prompted to enter a research topic, and each agent will stream its progress directly into your terminal.

---

## 🧰 Tech Stack

- **Orchestration**: [LangChain](https://www.langchain.com/)
- **LLM Inference**: [Groq Cloud](https://groq.com/) (`ChatGroq`)
- **Web Search**: [Tavily Search API](https://tavily.com/)
- **Web Scraping**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & [Requests](https://requests.readthedocs.io/)
- **Backend Server**: [aiohttp](https://docs.aiohttp.org/) (Async HTTP & Server-Sent Events)
- **Frontend / 3D Graphics**: [Three.js](https://threejs.org/) (WebGL), OrbitControls
- **Markdown Parsing**: [Marked.js](https://marked.js.org/)
- **Audio Engine**: Web Audio API (procedural real-time sound synthesis)
