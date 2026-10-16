# Aetheris // Multi-Agent AI Research System 🌌

Autonomous multi-agent research constellation powered by **LangChain**, **Groq LLMs**, **Tavily Web Search**, and a **Three.js WebGL Quantum Constellation** interface.

---

## 🏗️ Architecture

```
                                  +------------------------------------+
                                  |         Vercel (Frontend)          |
                                  |  - index.html (Three.js WebGL UI)  |
                                  |  - config.js (API Base resolver)   |
                                  |  - vercel.json (Static edge host)  |
                                  +-----------------+------------------+
                                                    |
                                      HTTPS / SSE   |  Real-time EventStream
                                     (CORS Enabled) |  (/api/stream)
                                                    v
                                  +------------------------------------+
                                  |          Render (Backend)          |
                                  |  - server.py (aiohttp async engine)|
                                  |  - pipeline.py (multi-agent flow)  |
                                  |  - agents.py (Groq + LangChain)    |
                                  |  - tools.py (Tavily search+scrape) |
                                  +------------------------------------+
```

### The 4 Neural Agents:
1. **🔍 Search Agent** (`build_search_agent`): Performs targeted real-time web intelligence using Tavily.
2. **📖 Reader / Scraper Agent** (`build_scrape_agent`): Extracts, parses, and cleans content from primary web sources.
3. **✍️ Synthesis Writer** (`writer_chain`): Drafts a structured 4-part research report (Introduction, Key Findings, Conclusion, Sources).
4. **⚖️ Adversarial Critic** (`critic_chain`): Stress-tests assertions, grades the report out of 10, and delivers an objective verdict.

---

## 🚀 Deployment Instructions

### Step 1: Initialize Git and Push to GitHub

If you haven't already initialized git:

```bash
git init
git add .
git commit -m "feat: deployable format for Render backend and Vercel frontend"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git push -u origin main
```

*(Note: `.gitignore` protects your local `.env` and `.venv` from being pushed).*

---

### Step 2: Deploy the Backend on Render

1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Fill in the service configuration:
   - **Name**: `aetheris-backend` (or your preferred name)
   - **Region**: Choose the closest region (e.g., Oregon, Frankfurt, Singapore)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: `Free`
5. Click **Advanced** and add your **Environment Variables**:
   | Key | Value | Description |
   |---|---|---|
   | `GROQ_API_KEY` | `gsk_...` | Your Groq API key from [Groq Console](https://console.groq.com/keys) |
   | `TAVILY_API_KEY` | `tvly-...` | Your Tavily API key from [Tavily](https://tavily.com) |
   | `GROQ_MODEL` | `openai/gpt-oss-120b` | Model name (or `llama-3.3-70b-versatile`) |
   | `PYTHON_VERSION` | `3.11.9` | Recommended Python version |
6. Click **Create Web Service**.
7. Once deployed, copy your Render URL:  
   `https://aetheris-backend.onrender.com`
8. Verify it works by opening `https://aetheris-backend.onrender.com/api/health` in your browser. It should return:
   ```json
   {
     "status": "online",
     "system": "Aetheris Multi-Agent AI Research System",
     "groq_configured": true,
     "tavily_configured": true
   }
   ```

*(Alternatively: Use Render Blueprints — Render will automatically read `render.yaml` and configure everything in one click).*

---

### Step 3: Deploy the Frontend on Vercel

1. Log in to [Vercel Dashboard](https://vercel.com).
2. Click **Add New...** > **Project**.
3. Import the same GitHub repository.
4. Vercel automatically detects the static site configuration from `vercel.json` and `.vercelignore`:
   - **Framework Preset**: `Other` (Static)
   - **Root Directory**: `./`
   - **Build Command**: Leave empty / default
   - **Output Directory**: `./`
5. Click **Deploy**.
6. In a few seconds, your site is live at:  
   `https://<your-project>.vercel.app`

---

### Step 4: Connect Vercel to Render

You have **3 seamless options** to connect your Vercel frontend to the Render backend:

#### Option A: In-App UI Configuration (Easiest - No Redeployment)
1. Open your live Vercel site (`https://<your-project>.vercel.app`).
2. In the top header bar, click the **CONNECT BACKEND** pill (with the ⚙️ icon).
3. Paste your Render backend URL (e.g. `https://aetheris-backend.onrender.com`).
4. Click **TEST & SAVE**.
5. The status badge will turn green: `ONLINE: GROQ + TAVILY`. Your URL is saved in `localStorage`.

#### Option B: In `config.js` (Permanent Default)
Open `config.js` in your repository and set your Render URL:
```javascript
window.AETHERIS_BACKEND_URL = "https://aetheris-backend.onrender.com";
```
Commit and push to GitHub. Vercel will automatically re-deploy in seconds.

#### Option C: Query String (Quick Share / Debugging)
Append `?backend=` to your Vercel URL:
```
https://<your-project>.vercel.app?backend=https://aetheris-backend.onrender.com
```

---

## 💻 Local Development

To run the entire system locally on your computer:

1. Clone repository and set up environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # On Windows
   # source .venv/bin/activate # On macOS/Linux
   pip install -r requirements.txt
   ```

2. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```
   Add your `GROQ_API_KEY` and `TAVILY_API_KEY`.

3. Start the server:
   ```bash
   python server.py
   ```
4. It will automatically launch your browser at `http://localhost:8000`.

---

## 🛠️ Key Troubleshooting Tips

- **Render Cold Starts (Free Tier)**: On Render's free tier, servers sleep after 15 minutes of inactivity. When you send your first request, it may take 30–50 seconds to spin up. The frontend health-check handles this with an extended timeout and informs you if the backend is waking up.
- **CORS Handling**: `server.py` includes global CORS middleware and handles preflight `OPTIONS` requests seamlessly so your Vercel domain can interact with Render without restriction.
- **SSE Buffering**: `server.py` sends `X-Accel-Buffering: no` and `Cache-Control: no-cache, no-transform` headers to prevent reverse proxies from buffering real-time agent output.
