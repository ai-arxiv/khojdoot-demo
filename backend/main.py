from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from datetime import datetime
import re
import os
import shutil

from database import init_db, get_db



app = FastAPI(
    title="Khoj Doot API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Khoj Doot API is running"
    }


# -------------------------
# SHOP REQUEST MODEL
# -------------------------

class ShopCreate(BaseModel):
    name: str
    phone: str | None = None
    city: str


# -------------------------
# SLUG GENERATOR
# -------------------------

def create_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")

    return slug


# -------------------------
# CREATE SHOP
# -------------------------

@app.post("/smes")
def create_shop(shop: ShopCreate):

    slug = create_slug(shop.name)

    conn = get_db()

    # Check whether slug already exists
    existing = conn.execute(
        "SELECT id FROM shops WHERE slug = ?",
        (slug,)
    ).fetchone()

    if existing:
        conn.close()

        raise HTTPException(
            status_code=409,
            detail="A shop with this name already exists."
        )

    updated_at = datetime.now().isoformat()

    cursor = conn.execute(
        """
        INSERT INTO shops
        (name, phone, city, slug, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            shop.name,
            shop.phone,
            shop.city,
            slug,
            updated_at
        )
    )

    conn.commit()

    shop_id = cursor.lastrowid

    conn.close()

    return {
        "id": shop_id,
        "slug": slug
    }
# -------------------------
# INGEST / PHOTO UPLOAD
# -------------------------

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/ingest")
async def ingest_photos(
    slug: str = Form(...),
    photos: list[UploadFile] = File(...)
):
    conn = get_db()

    # Check that shop exists
    shop = conn.execute(
        "SELECT id FROM shops WHERE slug = ?",
        (slug,)
    ).fetchone()

    if not shop:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    shop_id = shop["id"]

    saved_files = []

    for photo in photos:

        # Basic filename cleanup
        original_name = os.path.basename(photo.filename)

        # Create unique filename
        filename = f"{shop_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{original_name}"

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Save filename in database
        conn.execute(
            """
            INSERT INTO photos (shop_id, filename)
            VALUES (?, ?)
            """,
            (shop_id, filename)
        )

        saved_files.append(filename)

    # Update shop timestamp
    conn.execute(
        """
        UPDATE shops
        SET updated_at = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            shop_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Photos uploaded successfully",
        "slug": slug,
        "files": saved_files
    }

# -------------------------
# SAVE BINS
# -------------------------

@app.post("/smes/{slug}/bins")
def save_bins(slug: str, data: dict):

    conn = get_db()

    # Check that shop exists
    shop = conn.execute(
        "SELECT id FROM shops WHERE slug = ?",
        (slug,)
    ).fetchone()

    if not shop:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    shop_id = shop["id"]

    # Convert JSON object to string for SQLite
    import json

    bins_json = json.dumps(data)

    # Check if bins already exist for this shop
    existing = conn.execute(
        "SELECT id FROM bins WHERE shop_id = ?",
        (shop_id,)
    ).fetchone()

    if existing:
        # Update existing bins
        conn.execute(
            """
            UPDATE bins
            SET data = ?
            WHERE shop_id = ?
            """,
            (bins_json, shop_id)
        )
    else:
        # Insert new bins
        conn.execute(
            """
            INSERT INTO bins (shop_id, data)
            VALUES (?, ?)
            """,
            (shop_id, bins_json)
        )

    # Update shop timestamp
    conn.execute(
        """
        UPDATE shops
        SET updated_at = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            shop_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Bins saved successfully",
        "slug": slug
    }

# -------------------------
# GET SHOP CATALOG JSON
# -------------------------

@app.get("/b/{slug}.json")
def get_shop_catalog(slug: str):

    conn = get_db()

    # Get shop
    shop = conn.execute(
        """
        SELECT id, name, phone, city, slug, updated_at
        FROM shops
        WHERE slug = ?
        """,
        (slug,)
    ).fetchone()

    if not shop:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    shop_id = shop["id"]

    # Get photos
    photos = conn.execute(
        """
        SELECT filename
        FROM photos
        WHERE shop_id = ?
        """,
        (shop_id,)
    ).fetchall()

    photo_list = [
        photo["filename"]
        for photo in photos
    ]

    # Get bins
    bins = conn.execute(
        """
        SELECT data
        FROM bins
        WHERE shop_id = ?
        """,
        (shop_id,)
    ).fetchone()

    import json

    bins_data = {}

    if bins:
        bins_data = json.loads(bins["data"])

    conn.close()

    return {
        "sme_id": shop["id"],
        "name": shop["name"],
        "phone": shop["phone"],
        "city": shop["city"],
        "slug": shop["slug"],
        "photos": photo_list,
        "bins": bins_data,
        "updated_at": shop["updated_at"],
        "source": "merchant upload"
    }