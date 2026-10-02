CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sme_id TEXT,
    slug TEXT UNIQUE,
    name TEXT NOT NULL,
    phone TEXT,
    city TEXT,
    updated_at TEXT
);

CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    filename TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE TABLE bins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    bin_type TEXT,
    data TEXT,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);