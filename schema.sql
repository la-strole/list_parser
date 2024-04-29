CREATE TABLE advertisement (
        id INTEGER PRIMARY KEY,
        image_href VARCHAR(255) NOT NULL,
        title TEXT NOT NULL,
        price_value INTEGER NOT NULL,
        currancy CHARACTER(3) NOT NULL,
        price_amd INTEGER NOT NULL,
        description TEXT NOT NULL,
        date_posted TEXT NOT NULL,
        date_updated TEXT DEFAULT NULL,
        location VARCHAR(255) NOT NULL,
        agent_status BOOLEAN NOT NULL,
        user_link VARCHAR(255) NOT NULL,   
        appliances TEXT DEFAULT NULL,
        garage BOOLEAN DEFAULT NULL,
        rooms_count INTEGER DEFAULT NULL,
        toilet_count INTEGER DEFAULT 1,
        utility_bills_included BOOLEAN DEFAULT NULL,
        furniture TEXT DEFAULT NULL,
        children_allowed BOOLEAN DEFAULT NULL,
        animals_allowed BOOLEAN DEFAULT NULL,
        total_area INTEGER DEFAULT NULL,
        land_area INTEGER DEFAULT NULL,
        prepayment TEXT DEFAULT NULL,
        appartment_state TEXT DEFAULT NULL,
        type VARCHAR(50) DEFAULT NULL,
        building_type VARCHAR(50) DEFAULT NULL,
        facilities TEXT DEFAULT NULL,
        floors_count INTEGER DEFAULT 1,
        district VARCHAR(50) DEFAULT NULL
);

CREATE TABLE telegram_user_filtres (
        user_id INTEGER PRIMARY KEY,
        send_duplicates BOOLEAN DEFAULT 1,
        price_value_amd INTEGER DEFAULT NULL,
        agent_status BOOLEAN DEFAULT NULL,
        garage BOOLEAN DEFAULT NULL,
        rooms_count INTEGER DEFAULT NULL,
        toilet_count INTEGER DEFAULT NULL,
        furniture TEXT DEFAULT NULL,
        children_allowed BOOLEAN DEFAULT NULL,
        animals_allowed BOOLEAN DEFAULT NULL,
        total_area INTEGER DEFAULT NULL,
        land_area INTEGER DEFAULT NULL,
        floors_count INTEGER DEFAULT NULL,
        district VARCHAR(50) DEFAULT NULL
)

CREATE TABLE sent_adv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        adv_id INTEGER NOT NULL,
        tlg_user_id TEXT NOT NULL,
        FOREIGN KEY(adv_id) REFERENCES advertisement(id),
        FOREIGN KEY(tlg_user_id) REFERENCES telegram_user(user_id)

)