from app.db.connection import get_connection
import json


def create_shop(sme_id, slug, name, phone, city, updated_at):
    conn = get_connection()

    shop = conn.execute(
        "SELECT id FROM shops WHERE slug = ? OR phone = ?",
        (slug, phone)
    ).fetchone()

    if shop:
        conn.execute(
            """UPDATE shops
            SET sme_id = ?, slug = ?, name = ?, phone = ?, city = ?, updated_at = ?
            WHERE id = ?""",
            (sme_id, slug, name, phone, city, updated_at, shop["id"])
        )
        conn.commit()
        shop_id = shop["id"]
        conn.close()
        return shop_id

    cursor = conn.execute(
        """INSERT INTO shops
        (sme_id, slug, name, phone, city, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (sme_id, slug, name, phone, city, updated_at)
    )

    conn.commit()
    shop_id = cursor.lastrowid
    conn.close()

    return shop_id


def get_shop(slug):
    conn = get_connection()

    shop = conn.execute(
        "SELECT * FROM shops WHERE slug = ?",
        (slug,)
    ).fetchone()

    conn.close()

    return shop


def update_shop(slug, name, phone, city, updated_at):
    conn = get_connection()

    conn.execute(
        """UPDATE shops
        SET name = ?, phone = ?, city = ?, updated_at = ?
        WHERE slug = ?""",
        (name, phone, city, updated_at, slug)
    )

    conn.commit()
    conn.close()


def save_infobin(shop_id, bin_type, data):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM bins WHERE shop_id = ? AND bin_type = ?",
        (shop_id, bin_type)
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE bins SET data = ? WHERE id = ?",
            (json.dumps(data), existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO bins (shop_id, bin_type, data) VALUES (?, ?, ?)",
            (shop_id, bin_type, json.dumps(data))
        )

    conn.commit()
    conn.close()


def get_infobin(shop_id, bin_type):
    conn = get_connection()

    row = conn.execute(
        "SELECT data FROM bins WHERE shop_id = ? AND bin_type = ?",
        (shop_id, bin_type)
    ).fetchone()

    conn.close()

    if row:
        return json.loads(row["data"])

    return None


def get_facts(shop_id):
    conn = get_connection()

    rows = conn.execute(
        "SELECT bin_type, data FROM bins WHERE shop_id = ?",
        (shop_id,)
    ).fetchall()

    conn.close()

    facts = {}

    for row in rows:
        facts[row["bin_type"]] = json.loads(row["data"])

    return facts


def save_provenance(shop_id, field_name, source_type, confidence, confirmed):
    conn = get_connection()

    conn.execute(
        """INSERT INTO provenance
        (shop_id, field_name, source_type, confidence, confirmed)
        VALUES (?, ?, ?, ?, ?)""",
        (shop_id, field_name, source_type, confidence, confirmed)
    )

    conn.commit()
    conn.close()


def get_provenance(shop_id):
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM provenance WHERE shop_id = ?",
        (shop_id,)
    ).fetchall()

    conn.close()

    return rows


def save_photo(shop_id, filename, source=None):
    conn = get_connection()

    conn.execute(
        "INSERT INTO photos (shop_id, filename, source) VALUES (?, ?, ?)",
        (shop_id, filename, source)
    )

    conn.commit()
    conn.close()


def get_photos(shop_id):
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM photos WHERE shop_id = ?",
        (shop_id,)
    ).fetchall()

    conn.close()

    return rows


def update_status(slug, status):
    conn = get_connection()

    conn.execute(
        "UPDATE shops SET status = ? WHERE slug = ?",
        (status, slug)
    )

    conn.commit()
    conn.close()


def get_status(slug):
    conn = get_connection()

    row = conn.execute(
        "SELECT status FROM shops WHERE slug = ?",
        (slug,)
    ).fetchone()

    conn.close()

    if row:
        return row["status"]

    return None


def save_consent(shop_id, consent_type, approved_at, payload_hash):
    conn = get_connection()

    conn.execute(
        """INSERT INTO consent_records
        (shop_id, consent_type, approved_at, payload_hash)
        VALUES (?, ?, ?, ?)""",
        (shop_id, consent_type, approved_at, payload_hash)
    )

    conn.commit()
    conn.close()


def get_consent(shop_id):
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM consent_records WHERE shop_id = ?",
        (shop_id,)
    ).fetchall()

    conn.close()

    return rows


def save_website_spec(shop_id, version, spec_data, validation_score, status):
    conn = get_connection()

    conn.execute(
        """INSERT INTO website_specs
        (shop_id, version, spec_data, validation_score, status)
        VALUES (?, ?, ?, ?, ?)""",
        (
            shop_id,
            version,
            json.dumps(spec_data),
            validation_score,
            status
        )
    )

    conn.commit()
    conn.close()


def get_website_specs(shop_id):
    conn = get_connection()

    rows = conn.execute(
        """SELECT * FROM website_specs
        WHERE shop_id = ?
        ORDER BY version""",
        (shop_id,)
    ).fetchall()

    conn.close()

    specs = []

    for row in rows:
        spec = dict(row)
        if spec["spec_data"]:
            spec["spec_data"] = json.loads(spec["spec_data"])
        specs.append(spec)

    return specs