# Khoj Doot backend: POST /ingest + shop preview page
# Run:  pip install fastapi uvicorn python-multipart
#       uvicorn main:app --reload --port 8000
import json, re, html, uuid, time
from pathlib import Path
from typing import List
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, PlainTextResponse, Response
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

@app.get("/upload")
def upload_page():
    # serves the form from the backend, so any device can open  <address>/upload
    return FileResponse(Path(__file__).with_name("upload.html"))

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
        {"name": name, "phone": phone, "city": city, "slug": slug, "photos": saved, "created": time.time()}))
    base = str(request.base_url).rstrip("/")
    return {"slug": slug, "photos": len(saved), "preview_url": f"{base}/b/{slug}"}

STAGES = ["Received", "Photos checked", "Facts extracted", "Merchant approved", "Khoj Card built", "Published"]
SECONDS_PER_STAGE = 2   # DEMO: stages advance by time. Replace with Abhishek's real pipeline status.

def load_shop(slug):
    f = DATA / clean_slug(slug) / "shop.json"
    if not f.exists():
        raise HTTPException(404, "Shop not found")
    return json.loads(f.read_text())

@app.get("/preview/{slug}")
def old_preview(slug: str):
    return RedirectResponse(f"/b/{clean_slug(slug)}")

def all_shops():
    return sorted((json.loads(f.read_text()) for f in DATA.glob("*/shop.json")), key=lambda s: -s.get("created", 0))

def business(s, base):
    """One approved record -> Business JSON. Every other asset is built from this."""
    return {"slug": s["slug"], "name": s["name"], "city": s["city"], "phone": s["phone"],
            "photos": [f"{base}/files/{s['slug']}/{x}" for x in s["photos"]],
            "url": f"{base}/b/{s['slug']}"}

def jsonld(b):
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "name": b["name"],
            "telephone": b["phone"], "url": b["url"], "image": b["photos"],
            "address": {"@type": "PostalAddress", "addressLocality": b["city"], "addressCountry": "IN"}}

@app.get("/b/{slug}.json")
def business_json(slug: str, request: Request):
    return business(load_shop(slug), str(request.base_url).rstrip("/"))

@app.get("/merchant/{slug}")
def merchant_alias(slug: str):
    return RedirectResponse(f"/b/{clean_slug(slug)}")

@app.get("/llms.txt", response_class=PlainTextResponse)
def llms(request: Request):
    base = str(request.base_url).rstrip("/")
    lines = ["# Khoj Doot", "> Merchant onboarding and publishing. Each page below is a published merchant.", "", "## Merchants"]
    lines += [f"- [{s['name']}, {s['city']}]({base}/b/{s['slug']}): {base}/b/{s['slug']}.json" for s in all_shops()]
    return "\n".join(lines) + "\n"

@app.get("/llms-full.txt", response_class=PlainTextResponse)
def llms_full(request: Request):
    base = str(request.base_url).rstrip("/")
    out = ["# Khoj Doot - full merchant listing", ""]
    for s in all_shops():
        b = business(s, base)
        out += [f"## {b['name']}", f"- City: {b['city']}", f"- Phone: {b['phone']}", f"- Page: {b['url']}", f"- Data: {b['url']}.json", ""]
    return "\n".join(out)

@app.get("/sitemap.xml")
def sitemap(request: Request):
    base = str(request.base_url).rstrip("/")
    urls = "".join(f"<url><loc>{base}/b/{s['slug']}</loc></url>" for s in all_shops())
    return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>", media_type="application/xml")

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots(request: Request):
    return f"User-agent: *\nAllow: /\nDisallow: /labs\nDisallow: /api/\nSitemap: {str(request.base_url).rstrip('/')}/sitemap.xml\n"

@app.get("/.well-known/agent-card.json")
def agent_card(request: Request):
    # PLACEHOLDER: align with the exact Agent Card spec the team chose before the demo.
    base = str(request.base_url).rstrip("/")
    return {"name": "KhojDoot", "description": "Multilingual merchant onboarding and publishing.",
            "url": base, "version": "0.1", "skills": [{"id": "onboard-merchant", "name": "Onboard a merchant"}]}

@app.get("/b/{slug}", response_class=HTMLResponse)
def khoj_card(slug: str, request: Request):
    s = load_shop(slug); e = html.escape
    imgs = "".join(f'<img src="/files/{s["slug"]}/{x}" alt="">' for x in s["photos"][1:])
    cover = f'/files/{s["slug"]}/{s["photos"][0]}'
    tel = re.sub(r"\D", "", s["phone"])
    ld = json.dumps(jsonld(business(s, str(request.base_url).rstrip("/")))).replace("</", "<\\/")
    return CARD.replace("{LD}", ld).replace("{NAME}", e(s["name"])).replace("{CITY}", e(s["city"])).replace("{COVER}", cover)\
               .replace("{IMGS}", imgs).replace("{TEL}", tel).replace("{PHONE}", e(s["phone"]))

@app.get("/api/pipeline")
def pipeline():
    out = []
    for f in DATA.glob("*/shop.json"):
        s = json.loads(f.read_text())
        done = min(len(STAGES), int((time.time() - s.get("created", 0)) // SECONDS_PER_STAGE))
        st = ["done" if i < done else "running" if i == done else "waiting" for i in range(len(STAGES))]
        out.append({"slug": s["slug"], "name": s["name"], "created": s.get("created", 0), "stages": st})
    out.sort(key=lambda x: -x["created"])
    return {"stages": STAGES, "shops": out[:10]}

@app.get("/labs", response_class=HTMLResponse)
def labs():
    return LABS

CARD = """<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{NAME} - Khoj Card</title>
<script type="application/ld+json">{LD}</script>
<style>:root{--ink:#1f2a44;--indigo:#243b8f;--saffron:#f0a000}*{box-sizing:border-box}
body{margin:0;background:#fbf7f0;color:var(--ink);font:18px/1.5 system-ui,sans-serif}
main{max-width:560px;margin:0 auto;padding:16px}
.hero{height:min(60vw,300px);border-radius:18px;background:#e9e3d4 url({COVER}) center/cover}
.badge{display:inline-block;background:#e3f4ea;color:#1f7a4d;font-size:.8rem;font-weight:600;padding:2px 10px;border-radius:99px;margin-top:14px}
h1{margin:6px 0 0;font-size:1.8rem;line-height:1.2}.city{color:#5d6477;margin:0 0 14px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:18px}
.g img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px}
a.b{display:block;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:600;margin-top:10px}
.wa{background:#1f9d55;color:#fff}.call{background:#fff;color:var(--indigo);border:2px solid var(--indigo)}
.f{margin-top:22px;text-align:center;color:#5d6477;font-size:.85rem}</style>
<main><div class=hero></div><span class=badge>Verified by merchant</span>
<h1>{NAME}</h1><p class=city>{CITY}</p><div class=g>{IMGS}</div>
<a class="b wa" href="https://wa.me/91{TEL}">Message on WhatsApp</a>
<a class="b call" href="tel:+91{TEL}">Call {PHONE}</a>
<p class=f>Khoj Card by Khoj Doot</p></main></html>"""

LABS = """<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>KhojDoot Labs</title>
<style>*{box-sizing:border-box}body{margin:0;background:#10162b;color:#e8ecf8;font:16px/1.5 system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:18px}h1{margin:0}.sub{color:#8d97b8;margin:0 0 18px}
.shop{background:#1a2342;border-radius:14px;padding:14px;margin-bottom:12px}
.shop a{color:#ffc247;font-weight:600;text-decoration:none}
.pipe{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:10px}
.st{font-size:.7rem;text-align:center;padding:8px 2px;border-radius:8px;background:#26305a;color:#8d97b8;transition:.4s}
.st.done{background:#1f7a4d;color:#fff}.st.running{background:#f0a000;color:#10162b;font-weight:600;animation:p 1s infinite}
@keyframes p{50%{opacity:.55}}.empty{color:#8d97b8}
@media(max-width:520px){.pipe{grid-template-columns:repeat(2,1fr)}.st{font-size:.8rem}}</style>
<main><h1>KhojDoot Labs</h1><p class=sub>Live pipeline status. Updates every 2 seconds.</p><div id=list class=empty>No shops yet.</div></main>
<script>
async function tick(){try{const d=await (await fetch("/api/pipeline")).json();
if(!d.shops.length)return;
document.getElementById("list").innerHTML=d.shops.map(s=>'<div class=shop><a href="/b/'+s.slug+'">'+s.name.replace(/</g,"&lt;")+'</a><div class=pipe>'+
s.stages.map((x,i)=>'<div class="st '+x+'">'+d.stages[i]+'</div>').join("")+'</div></div>').join("");}catch(e){}}
tick();setInterval(tick,2000);
</script></html>"""
