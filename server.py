import asyncio
import json
import os
import sys
from aiohttp import web
from dotenv import load_dotenv

# Ensure local modules are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

load_dotenv()
from pipeline import run_research_pipeline_stream

# HTML UI File Path
INDEX_HTML_PATH = os.path.join(current_dir, "index.html")

@web.middleware
async def cors_middleware(request, handler):
    """Global CORS middleware supporting preflight OPTIONS and cross-origin headers."""
    if request.method == "OPTIONS":
        return web.Response(
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, *",
                "Access-Control-Max-Age": "86400",
            }
        )
    try:
        response = await handler(request)
    except web.HTTPException as ex:
        response = ex

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, *"
    return response

async def handle_options(request):
    """Fallback handler for preflight OPTIONS requests."""
    return web.Response(status=200)

async def handle_index(request):
    if not os.path.exists(INDEX_HTML_PATH):
        return web.Response(text="Aetheris Multi-Agent Research System API is running. (index.html not hosted here)", status=200)
    return web.FileResponse(INDEX_HTML_PATH)

async def handle_health(request):
    return web.json_response({
        "status": "online",
        "system": "Aetheris Multi-Agent AI Research System",
        "agents": ["search", "scrape", "writer", "critic"],
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY")),
        "groq_model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    })

async def handle_stream(request):
    topic = request.query.get("topic", "").strip()
    if not topic:
        return web.Response(text="Query parameter 'topic' is required.", status=400)

    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache, no-transform',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
            'Access-Control-Allow-Origin': '*',
        }
    )
    await response.prepare(request)

    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def run_pipeline_sync():
        try:
            for event in run_research_pipeline_stream(topic):
                loop.call_soon_threadsafe(queue.put_nowait, event)
        except Exception as e:
            loop.call_soon_threadsafe(queue.put_nowait, {
                "step": -1,
                "agent": "error",
                "status": "error",
                "message": f"Pipeline execution error: {str(e)}"
            })
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    # Run the synchronous pipeline in a worker thread
    asyncio.create_task(asyncio.to_thread(run_pipeline_sync))

    while True:
        try:
            event = await queue.get()
            if event is None:
                break
            data = f"data: {json.dumps(event)}\n\n"
            await response.write(data.encode('utf-8'))
            await response.drain()
        except (ConnectionResetError, asyncio.CancelledError):
            # Client disconnected early
            break
        except Exception:
            break

    return response

async def init_app():
    app = web.Application(middlewares=[cors_middleware])
    app.router.add_route('OPTIONS', '/{tail:.*}', handle_options)
    app.router.add_get('/', handle_index)
    app.router.add_get('/index.html', handle_index)
    app.router.add_get('/api/health', handle_health)
    app.router.add_get('/api/stream', handle_stream)
    return app

import socket
import webbrowser

def find_available_port(start_port=8000, max_attempts=10):
    for p in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', p))
                return p
            except OSError:
                continue
    return start_port

if __name__ == '__main__':
    # Render and cloud platforms supply PORT in the environment
    is_cloud_env = "PORT" in os.environ
    if is_cloud_env:
        port = int(os.environ["PORT"])
    else:
        port = find_available_port(8000)

    print("\n" + "=" * 60)
    print(" * AETHERIS MULTI-AGENT AI RESEARCH SYSTEM")
    print(" * WebGL Quantum Constellation Backend")
    print(f" * Serving on: http://0.0.0.0:{port}")
    if is_cloud_env:
        print(" * Environment: Cloud Production (Render)")
    else:
        print(" * Environment: Local Development")
    print("=" * 60 + "\n")

    if not is_cloud_env:
        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass

    web.run_app(init_app(), host='0.0.0.0', port=port)
