Khoj Doot - merchant upload form + backend

Files
- main.py      backend (POST /ingest, shop preview page, serves the form)
- upload.html  merchant upload form

Run (one time install)
1. pip install fastapi uvicorn python-multipart

Start
2. python -m uvicorn main:app --port 8001 --proxy-headers --forwarded-allow-ips="*"
3. Open http://localhost:8001/upload in the browser
   (use port 8000 instead if it is free)

Try the screens without the backend: add ?demo=1 to the page address.

Live demo on another PC
- Run the backend on your laptop, then: ngrok http 8001
- On the other PC open  <ngrok link>/upload

Note: the preview link opens only on the machine running the backend.
For the live demo we'll use ngrok.
If WhatsApp fails on stage, we use this form.
