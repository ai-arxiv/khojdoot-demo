from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.db.connection import init_db
from app.db.crud import (
    get_shop,
    create_shop,
    update_shop,
    save_infobin,
    get_infobin,
    get_facts,
    save_photo,
    get_photos,
)
import os
import shutil
from datetime import datetime


app = FastAPI()

init_db()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# Request Models
# -------------------------

class Shop(BaseModel):
    sme_id: str
    slug: str
    name: str
    phone: str
    city: str
    updated_at: str


class InfoBin(BaseModel):
    bin_type: str
    data: dict


# -------------------------
# Health Check
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Khoj Doot API is running"
    }


# -------------------------
# Ticket 2: Photo Ingest
# -------------------------

@app.post("/ingest")
async def ingest_photos(
    slug: str,
    photo1: UploadFile = File(...),
    photo2: UploadFile | None = File(None)
):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    photos = [photo1]

    if photo2:
        photos.append(photo2)

    saved_files = []

    for photo in photos:
        original_name = os.path.basename(photo.filename)

        filename = (
            f"{shop['id']}_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_"
            f"{original_name}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                photo.file,
                buffer
            )

        save_photo(
            shop["id"],
            filename
        )

        saved_files.append(filename)

    return {
        "message": "Photos uploaded successfully",
        "slug": slug,
        "files": saved_files
    }


# -------------------------
# Shop
# -------------------------

@app.get("/shop/{slug}")
def shop(slug: str):
    data = get_shop(slug)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    return dict(data)


# -------------------------
# Public JSON Catalog
# -------------------------

@app.get("/b/{slug}.json")
def get_public_shop_json(slug: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    facts = get_facts(shop["id"])
    photos = get_photos(shop["id"])

    return {
        "slug": shop["slug"],
        "business_name": shop["name"],
        "city": shop["city"],
        "facts": facts,
        "photos": [dict(photo) for photo in photos]
    }


# -------------------------
# Public Shop Data
# -------------------------

@app.get("/b/{slug}")
def get_public_shop(slug: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    facts = get_facts(shop["id"])
    photos = get_photos(shop["id"])

    return {
        "slug": shop["slug"],
        "business_name": shop["name"],
        "city": shop["city"],
        "facts": facts,
        "photos": [dict(photo) for photo in photos]
    }


@app.get("/b/{slug}/facts")
def get_shop_facts(slug: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    return get_facts(shop["id"])


# -------------------------
# Ticket 2: Create Shop
# -------------------------

@app.post("/smes")
@app.post("/shops")
def add_shop(shop: Shop):
    shop_id = create_shop(
        shop.sme_id,
        shop.slug,
        shop.name,
        shop.phone,
        shop.city,
        shop.updated_at
    )

    return {
        "id": shop_id,
        "message": "Shop created"
    }


# -------------------------
# Update Shop
# -------------------------

@app.put("/shops/{slug}")
def edit_shop(slug: str, shop: Shop):
    if get_shop(slug) is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    update_shop(
        slug,
        shop.name,
        shop.phone,
        shop.city,
        shop.updated_at
    )

    return {
        "message": "Shop updated"
    }


# -------------------------
# Ticket 2: Save InfoBin
# -------------------------

@app.post("/smes/{slug}/bins")
def add_infobin(slug: str, bin: InfoBin):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    save_infobin(
        shop["id"],
        bin.bin_type,
        bin.data
    )

    return {
        "message": "InfoBin saved"
    }


# -------------------------
# Get InfoBin
# -------------------------

@app.get("/smes/{slug}/bins/{bin_type}")
def get_infobin_data(slug: str, bin_type: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    data = get_infobin(
        shop["id"],
        bin_type
    )

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="InfoBin not found"
        )

    return data


# -------------------------
# Photos
# -------------------------

@app.post("/smes/{slug}/photos")
def add_photo(slug: str, filename: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    save_photo(
        shop["id"],
        filename
    )

    return {
        "message": "Photo saved"
    }


@app.get("/smes/{slug}/photos")
def get_shop_photos(slug: str):
    shop = get_shop(slug)

    if shop is None:
        raise HTTPException(
            status_code=404,
            detail="Shop not found."
        )

    photos = get_photos(shop["id"])

    return [
        dict(photo)
        for photo in photos
    ]