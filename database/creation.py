import os
import random
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

# —————————————————————————————
# 1) Konfiguration + DB‐connection
# —————————————————————————————
load_dotenv()
DB_PW = os.getenv("DB_PW")

def conn_to_db():
    return mysql.connector.connect(
        host="mac123.mysql.pythonanywhere-services.com",
        user="mac123",
        password=DB_PW,
        database="mac123$ewii_customer_data"
    )

# —————————————————————————————
# 2) Opret tabel
# —————————————————————————————
def create_ewii_table(conn):
    ddl = """
    CREATE TABLE IF NOT EXISTS ewii_customer_data (
      Kundenr                          INT       NOT NULL,
      Year                             YEAR      NOT NULL,
      Instnr                           INT,
      Forbnr                           INT,
      Segment_privat                   VARCHAR(255),
      Segment_forening                 VARCHAR(255),
      Teknologi                        VARCHAR(255),
      Antal_dage_som_Bredbånd_kunde    INT,
      Kontraktnavn                     VARCHAR(255),
      Fiberpris                        DOUBLE,
      Sikkerhedspakke                  VARCHAR(255),
      Premium_Wifi                     BOOLEAN,
      Fast_IP_adresse                  BOOLEAN,
      Router                           BOOLEAN,
      PC_Hjaelp_til_1_enhed            BOOLEAN,
      Access_Point                     BOOLEAN,
      Telefoni_Fri_Fastnet             BOOLEAN,
      Telefoni_tilvalg                 VARCHAR(255),
      Tilmeldt_betalingsmetode         VARCHAR(255),
      Samlede_betalinger               DOUBLE,
      Gns_betalinger                   DOUBLE,
      Antal_rykker_1                   INT,
      Antal_rykker_2                   INT,
      Kreditscore                      INT,
      Rykker_saldo                     DOUBLE,
      Faktisk_betalingsmetode          VARCHAR(255),
      xkommunkode                      VARCHAR(50),
      Kampagne                         VARCHAR(255),
      Digital_post                     BOOLEAN,
      Aktiv_el                         BOOLEAN,
      Antal_henvendelser               INT,
      PRIMARY KEY (Kundenr, Year)
    ) ENGINE=InnoDB;
    """
    cur = conn.cursor()
    cur.execute(ddl)
    conn.commit()

# —————————————————————————————
# 3) Generér dummy‐data og indsæt
# —————————————————————————————
def generate_and_insert(conn, excel_path, n_customers=100):
    # Læs data
    df = pd.read_excel(excel_path)

    # Omdøb kolonner fra Excel til DB-navne
    df.rename(columns={
        "Anonymiseret kundenr": "Kundenr",
        "Anonymiseret Instnr":  "Instnr"
    }, inplace=True)

    # Normaliser alle kolonnenavne: whitespace, bindestreg og punktum → underscore
    df.columns = (
        df.columns
          .str.strip()
          .str.replace(r'[\s\-.]+', '_', regex=True)
    )

    # Definér kolonnegrupper
    category_cols = [
        "Segment_privat", "Segment_forening", "Teknologi", "Kontraktnavn",
        "Sikkerhedspakke", "Telefoni_tilvalg", "Tilmeldt_betalingsmetode",
        "Faktisk_betalingsmetode", "xkommunkode", "Kampagne"
    ]
    bool_cols = [
        "Premium_Wifi", "Fast_IP_adresse", "Router",
        "PC_Hjaelp_til_1_enhed", "Access_Point", "Telefoni_Fri_Fastnet",
        "Digital_post", "Aktiv_el"
    ]
    int_cols = [
        "Instnr", "Forbnr", "Antal_dage_som_Bredbånd_kunde",
        "Antal_rykker_1", "Antal_rykker_2", "Kreditscore", "Antal_henvendelser"
    ]
    float_cols = [
        "Fiberpris", "Samlede_betalinger",
        "Gns_betalinger", "Rykker_saldo"
    ]

    # Byg sampling-lister og ranges
    cats = {col: df[col].dropna().unique().tolist() for col in category_cols}
    ranges = {
        **{col: (int(df[col].min()), int(df[col].max()))   for col in int_cols},
        **{col: (float(df[col].min()), float(df[col].max())) for col in float_cols}
    }

    # Generér data for 100 kunder over to år
    customer_ids = random.sample(range(1_000_000, 9_999_999), n_customers)
    rows = []
    for kn in customer_ids:
        for year in (2024, 2025):
            row = {"Kundenr": kn, "Year": year}

            # Numeriske felter
            for col, (mn, mx) in ranges.items():
                if col in int_cols:
                    row[col] = random.randint(mn, mx)
                else:
                    row[col] = round(random.uniform(mn, mx), 2)

            # Kategoriske felter
            for col, vals in cats.items():
                row[col] = random.choice(vals)

            # Boolske felter
            for col in bool_cols:
                row[col] = random.choice([True, False])

            # Let variation for 2025
            if year == 2025:
                row["Samlede_betalinger"] = round(row["Samlede_betalinger"] * random.uniform(0.9, 1.1), 2)
                row["Antal_rykker_1"] = max(0, row["Antal_rykker_1"] + random.randint(-1, 2))
                row["Antal_rykker_2"] = max(0, row["Antal_rykker_2"] + random.randint(-1, 2))

            rows.append(row)

    # Bulk‐insert til MySQL
    cols = list(rows[0].keys())
    placeholders = ", ".join(["%s"] * len(cols))
    colnames    = ", ".join(f"`{c}`" for c in cols)
    sql = f"INSERT INTO ewii_customer_data ({colnames}) VALUES ({placeholders})"

    cur = conn.cursor()
    cur.executemany(sql, [[r[c] for c in cols] for r in rows])
    conn.commit()
    print(f"{n_customers*2} dummy‐rækker indsat (2024 + 2025).")

# —————————————————————————————
if __name__ == "__main__":
    conn = conn_to_db()
    create_ewii_table(conn)
    generate_and_insert(
        conn,
        excel_path="../data/Active_nov_2024.xlsx",
        n_customers=100
    )
    conn.close()