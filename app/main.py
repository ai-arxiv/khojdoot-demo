from fastapi import FastAPI
from app.db.connection import init_db
from app.db.crud import get_shop, create_shop, update_shop, save_infobin, get_infobin, get_facts, update_status, get_status, save_provenance, get_provenance, save_photo, get_photos
from pydantic import BaseModel

app = FastAPI()

init_db()


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


class Status(BaseModel):
    status: str


class Provenance(BaseModel):
    source: str
    channel: str
    extraction: str
    approval: str


class Photo(BaseModel):
    filename: str


@app.get("/")
def home():
    return {"message": "Khoj Doot API is running"}


@app.get("/shop/{slug}")
def shop(slug: str):
    data = get_shop(slug)

    if data is None:
        return {"message": "Shop not found"}

    return dict(data)


@app.get("/b/{slug}")
def get_public_shop(slug: str):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

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
        return {"message": "Shop not found"}

    return get_facts(shop["id"])


@app.post("/shops")
@app.post("/smes")
def add_shop(shop: Shop):
    shop_id = create_shop(
        shop.sme_id,
        shop.slug,
        shop.name,
        shop.phone,
        shop.city,
        shop.updated_at
    )

    return {"id": shop_id, "message": "Shop created"}


@app.put("/shops/{slug}")
def edit_shop(slug: str, shop: Shop):
    if get_shop(slug) is None:
        return {"message": "Shop not found"}

    update_shop(
        slug,
        shop.name,
        shop.phone,
        shop.city,
        shop.updated_at
    )

    return {"message": "Shop updated"}


@app.post("/smes/{slug}/bins")
def add_infobin(slug: str, bin: InfoBin):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    save_infobin(shop["id"], bin.bin_type, bin.data)

    return {"message": "InfoBin saved"}


@app.get("/smes/{slug}/bins/{bin_type}")
def get_infobin_data(slug: str, bin_type: str):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    data = get_infobin(shop["id"], bin_type)

    if data is None:
        return {"message": "InfoBin not found"}

    return data


@app.get("/smes/{slug}/status")
def get_shop_status(slug: str):
    status = get_status(slug)

    if status is None:
        return {"message": "Shop not found"}

    return {"status": status}


@app.put("/smes/{slug}/status")
def change_shop_status(slug: str, status: Status):
    if get_shop(slug) is None:
        return {"message": "Shop not found"}

    update_status(slug, status.status)

    return {"message": "Status updated"}


@app.post("/smes/{slug}/provenance")
def add_provenance(slug: str, provenance: Provenance):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    save_provenance(
        shop["id"],
        provenance.source,
        provenance.channel,
        provenance.extraction,
        provenance.approval
    )

    return {"message": "Provenance saved"}


@app.get("/smes/{slug}/provenance")
def get_shop_provenance(slug: str):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    data = get_provenance(shop["id"])

    return [dict(row) for row in data]


@app.post("/smes/{slug}/photos")
def add_photo(slug: str, photo: Photo):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    save_photo(shop["id"], photo.filename)

    return {"message": "Photo saved"}


@app.get("/smes/{slug}/photos")
def get_shop_photos(slug: str):
    shop = get_shop(slug)

    if shop is None:
        return {"message": "Shop not found"}

    photos = get_photos(shop["id"])

    return [dict(photo) for photo in photos]