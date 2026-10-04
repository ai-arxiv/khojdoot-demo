CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sme_id TEXT,
    slug TEXT UNIQUE,
    name TEXT NOT NULL,
    phone TEXT,
    city TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    filename TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE IF NOT EXISTS bins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    bin_type TEXT,
    data TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);
