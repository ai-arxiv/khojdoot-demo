# Khoj Doot backend: POST /ingest + shop preview page
# Run:  pip install fastapi uvicorn python-multipart
#       uvicorn main:app --reload --port 8000
import json, re, html, uuid
from pathlib import Path
from typing import List
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

DATA = Path("shops"); DATA.mkdir(exist_ok=True)
app = FastAPI(title="Khoj Doot")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/files", StaticFiles(directory=DATA), name="files")

def clean_slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "shop-" + uuid.uuid4().hex[:6]

@app.get("/")
def health():
    return {"ok": True, "service": "khoj-doot"}

@app.post("/ingest")
async def ingest(request: Request,
                 name: str = Form(...), phone: str = Form(...), city: str = Form(...),
                 slug: str = Form(""), photos: List[UploadFile] = File(...)):
    slug = clean_slug(slug or f"{name} {city}")
    folder = DATA / slug
    folder.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, p in enumerate(photos[:8]):
        if not (p.content_type or "").startswith("image/"):
            continue
        ext = Path(p.filename or "").suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            ext = ".jpg"
        fname = f"{i+1}{ext}"
        (folder / fname).write_bytes(await p.read())
        saved.append(fname)
    if not saved:
        raise HTTPException(400, "No valid photos")
    (folder / "shop.json").write_text(json.dumps(
        {"name": name, "phone": phone, "city": city, "slug": slug, "photos": saved}))
    base = str(request.base_url).rstrip("/")
    return {"slug": slug, "photos": len(saved), "preview_url": f"{base}/preview/{slug}"}

@app.get("/preview/{slug}", response_class=HTMLResponse)
def preview(slug: str):
    f = DATA / clean_slug(slug) / "shop.json"
    if not f.exists():
        raise HTTPException(404, "Shop not found")
    s = json.loads(f.read_text())
    imgs = "".join(f'<img src="/files/{s["slug"]}/{x}" alt="">' for x in s["photos"])
    e = html.escape
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{e(s['name'])} – Khoj Doot</title>
<style>body{{margin:0;font:18px system-ui;background:#fbf7f0;color:#1f2a44}}main{{max-width:640px;margin:auto;padding:20px}}
h1{{margin:0}}p{{color:#5d6477}}.g{{display:grid;gap:10px;margin:16px 0}}.g img{{width:100%;border-radius:12px}}
a.b{{display:block;text-align:center;background:#1f9d55;color:#fff;padding:14px;border-radius:12px;text-decoration:none;font-weight:600}}</style>
<main><h1>{e(s['name'])}</h1><p>{e(s['city'])}</p><div class=g>{imgs}</div>
<a class=b href="https://wa.me/91{re.sub(r'\\D','',s['phone'])}">Message on WhatsApp</a></main>"""
