CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sme_id TEXT,
    slug TEXT UNIQUE,
    name TEXT NOT NULL,
    phone TEXT,
    city TEXT,
    status TEXT DEFAULT 'DRAFT',
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    filename TEXT,
    source TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE IF NOT EXISTS bins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    bin_type TEXT,
    data TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE IF NOT EXISTS provenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    field_name TEXT,
    source_type TEXT,
    confidence REAL,
    confirmed INTEGER DEFAULT 0,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE IF NOT EXISTS consent_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    consent_type TEXT,
    approved_at TEXT,
    payload_hash TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE IF NOT EXISTS website_specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    version INTEGER,
    spec_data TEXT,
    validation_score REAL,
    status TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);