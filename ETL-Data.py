import os
import hashlib
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

data_csv = [
    "obwody_glosowania_2015.csv",
    "obwody_glosowania_2019.csv",
    "obwody_glosowania_2023.csv",
    "rejestr_wyborcow_2015.csv",
    "rejestr_wyborcow_2019.csv",
    "rejestr_wyborcow_2023.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2015.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2019.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2023.csv"
]

def createEngine():
    load_dotenv()
    connection_url = URL.create(
        "mssql+pyodbc",
        username="sqladminuser",
        password=os.getenv("SQL_ADMIN_PASSWORD"),
        host="hd-sql-server.database.windows.net",
        port=1433,
        database="hd-sql-database",
        query={"driver": "ODBC Driver 17 for SQL Server"}
    )
    engine = create_engine(connection_url)
    return engine

def readAndLoadDataFromCSV(csv_file):
    folder_path = 'dane_zrodlowe'
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"INFO --- Folder '{folder_path}' nie istnieje.")

    file_path = os.path.join(folder_path, csv_file)
    print(f"INFO --- {csv_file}")

    df = pd.read_csv(file_path, on_bad_lines='skip', sep=';', low_memory=False)

    # Usunięcie wierszy, gdzie druga komórka jest pusta
    df = df[df.iloc[:, 1].notna()]

    return df

def generateWymiarCzas():
    data = [
        {"id_czasu": 20151025, "rok": 2015, "miesiac": 10, "dzien": 25, "kwartal": 4},
        {"id_czasu": 20191013, "rok": 2019, "miesiac": 10, "dzien": 13, "kwartal": 4},
        {"id_czasu": 20231015, "rok": 2023, "miesiac": 10, "dzien": 15, "kwartal": 4}
    ]

2015.10.25
2019.10.13
2023.10.15

    return pd.DataFrame(data)

def loadWymiarCzas(engine):
    merge_sql = """
        MERGE INTO Wymiar_Czas AS target
        USING (SELECT * FROM (VALUES
            (20151025, 2015, 10, 25, 4),
            (20191013, 2019, 10, 13, 4),
            (20231015, 2023, 10, 15, 4)
        ) AS source (id_czasu, rok, miesiac, dzien, kwartal)) AS source
        ON target.id_czasu = source.id_czasu
        WHEN NOT MATCHED THEN
            INSERT (id_czasu, rok, miesiac, dzien, kwartal)
            VALUES (source.id_czasu, source.rok, source.miesiac, source.dzien, source.kwartal);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))

    print("INFO --- Wykonano MERGE: dodano brakujące rekordy do Wymiar_Czas.")

def extractDataObwody(csv_file):
    df = readAndLoadDataFromCSV(csv_file)

    # Wyciągnięcie roku z nazwy pliku (np. 2015 z "obwody_glosowania_2015.csv")
    rok = None
    for possible_year in ['2015', '2019', '2023']:
        if possible_year in csv_file:
            rok = int(possible_year)
            break

    if rok is None:
        raise ValueError(f"Nie udało się wyciągnąć roku z nazwy pliku: {csv_file}")

    df['ID KOMISJI'] = df.apply(lambda row: f"{row['KOD TERYTORIALNY']}{row['Numer obwodu']}", axis=1)

    df_obwody = pd.DataFrame({
        'id_obwodu': df['ID KOMISJI'],
        'numer_obwodu': df['Numer obwodu'],
        'id_gminy': None,
        'adres': df['Pełna siedziba'],
        'przystosowany_dla_niepelnosprawnych': df['Przystosowany dla niepełnosprawnych'],
        'typ_obwodu': df['Typ obwodu'],
        'typ_obszaru': df['Typ obszaru'],
        'rok': rok  # Dodajemy kolumnę rok
    })

    df_obwody['adres'] = df_obwody['adres'].astype(str).str.slice(0, 255)
    df_obwody['id_obwodu'] = df_obwody['id_obwodu'].astype(str).str.replace('.', '')

    return df_obwody

def loadDataObwody(df_obwody, engine):
    # temporary table
    df_obwody.to_sql('Wymiar_Obwod_TMP', con=engine, if_exists='replace', index=False)
    print("INFO --- Dane tymczasowe zapisane do Wymiar_Obwod_TMP.")

    # MERGE (UPSERT)
    merge_sql = """
        MERGE INTO Wymiar_Obwod AS target
        USING Wymiar_Obwod_TMP AS source
        ON target.id_obwodu = source.id_obwodu AND target.rok = source.rok
        WHEN MATCHED THEN
            UPDATE SET
                target.numer_obwodu = source.numer_obwodu,
                target.id_gminy = source.id_gminy,
                target.adres = source.adres,
                target.przystosowany_dla_niepelnosprawnych = source.przystosowany_dla_niepelnosprawnych,
                target.typ_obwodu = source.typ_obwodu,
                target.typ_obszaru = source.typ_obszaru
        WHEN NOT MATCHED THEN
            INSERT (id_obwodu, numer_obwodu, id_gminy, adres, przystosowany_dla_niepelnosprawnych, typ_obwodu, typ_obszaru, rok)
            VALUES (source.id_obwodu, source.numer_obwodu, source.id_gminy, source.adres, source.przystosowany_dla_niepelnosprawnych, source.typ_obwodu, source.typ_obszaru, source.rok);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text("DROP TABLE Wymiar_Obwod_TMP"))

    return print("INFO --- Wykonano MERGE i usunięto tabelę tymczasową.")

def extractDataGminy(csv_file):
    df = readAndLoadDataFromCSV(csv_file)

    # Dopasowanie nazw kolumn (różne w zależności od roku)
    if 'KOD TERYTORIALNY' in df.columns:
        kod_col = 'KOD TERYTORIALNY'
    elif 'Kod TERYT' in df.columns:
        kod_col = 'Kod TERYT'
    else:
        raise ValueError("Nie znaleziono kolumny z kodem TERYT w pliku.")

    if 'Nazwa jednostki' in df.columns:
        nazwa_col = 'Nazwa jednostki'
    elif 'Gmina' in df.columns:
        nazwa_col = 'Gmina'
    else:
        raise ValueError("Nie znaleziono kolumny z nazwą gminy w pliku.")

    powiat_col = 'Powiat' if 'Powiat' in df.columns else None
    woj_col = 'Województwo' if 'Województwo' in df.columns else None

    df_gminy = pd.DataFrame({
        'kod_teryt': df[kod_col],
        'nazwa_gminy': df[nazwa_col],
        'typ_gminy': df[nazwa_col].apply(lambda x: x.split()[0] if isinstance(x, str) else None),
        'powiat': df[powiat_col] if powiat_col else None,
        'wojewodztwo': df[woj_col] if woj_col else None
    })

    # Usunięcie duplikatów i nadanie ID
    df_gminy = df_gminy.drop_duplicates().reset_index(drop=True)
    df_gminy.insert(0, 'id_gminy', df_gminy.index + 1)

    return df_gminy

def loadDataGminy(df_gminy, engine):
    # Zapis do tymczasowej tabeli
    df_gminy.to_sql('Wymiar_Gmina_TMP', con=engine, if_exists='replace', index=False)
    print("INFO --- Dane tymczasowe zapisane do Wymiar_Gmina_TMP.")

    merge_sql = """
        MERGE INTO Wymiar_Gmina AS target
        USING Wymiar_Gmina_TMP AS source
        ON target.id_gminy = source.id_gminy
        WHEN MATCHED THEN
            UPDATE SET
                target.kod_teryt = source.kod_teryt,
                target.nazwa_gminy = source.nazwa_gminy,
                target.typ_gminy = source.typ_gminy,
                target.powiat = source.powiat,
                target.wojewodztwo = source.wojewodztwo
        WHEN NOT MATCHED THEN
            INSERT (id_gminy, kod_teryt, nazwa_gminy, typ_gminy, powiat, wojewodztwo)
            VALUES (source.id_gminy, source.kod_teryt, source.nazwa_gminy, source.typ_gminy, source.powiat, source.wojewodztwo);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text("DROP TABLE Wymiar_Gmina_TMP"))

    print("INFO --- Wykonano MERGE i usunięto tabelę tymczasową.")

def extractDataStatystykiObwodu(csv_file):
    df = readAndLoadDataFromCSV(csv_file)

    # Rok i id_czasu z nazwy pliku
    rok = int(csv_file.split('_')[-1].split('.')[0])
    id_czasu = {
        2015: 20151025,
        2019: 20191013,
        2023: 20231015
    }.get(rok)

    # Czyszczenie kolumn liczbowych
    numeric_columns = [
        'Liczba wyborców',
        'Wydane karty',
        'Niewykorzystane karty',
        'Głosy ważne',
        'Głosy nieważne',
        'Liczba wyborców głosujących przez pełnomocnika',
        'Liczba wyborców głosujących na podstawie zaświadczenia o prawie do głosowania'
    ]

    for col in numeric_columns:
        df[col] = df[col].astype(str).str.replace(' ', '').str.replace(',', '').replace('nan', '0')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Generowanie ID obwodu (ID KOMISJI)
    df['id_obwodu'] = df.apply(
    lambda row: f"{int(row['KOD TERYTORIALNY'])}{int(row['Numer obwodu'])}"
    if pd.notnull(row['KOD TERYTORIALNY']) and pd.notnull(row['Numer obwodu']) else None,
    axis=1
)

    # Budowa końcowego DataFrame
    df_stat = pd.DataFrame({
        'id_obwodu': df['id_obwodu'],
        'rok': rok,
        'id_czasu': id_czasu,
        'liczba_wyborcow': df['Liczba wyborców'],
        'karty_wydane': df['Wydane karty'],
        'karty_niewykorzystane': df['Niewykorzystane karty'],
        'glosy_wazne': df['Głosy ważne'],
        'glosy_niewazne': df['Głosy nieważne'],
        'glosy_pelnomocnik': df['Liczba wyborców głosujących przez pełnomocnika'],
        'glosy_zaswiadczenie': df['Liczba wyborców głosujących na podstawie zaświadczenia o prawie do głosowania']
    })

    # Usunięcie wierszy bez ID obwodu
    df_stat = df_stat.dropna(subset=['id_obwodu']).reset_index(drop=True)

    return df_stat

def loadDataStatystykiObwodu(df_stat, engine):
    df_stat.to_sql('Fakt_Statystyki_Obwodu_TMP', con=engine, if_exists='replace', index=False)
    print("INFO --- Dane tymczasowe zapisane do Fakt_Statystyki_Obwodu_TMP.")

    merge_sql = """
        MERGE INTO Fakt_Statystyki_Obwodu AS target
        USING Fakt_Statystyki_Obwodu_TMP AS source
        ON target.id_obwodu = source.id_obwodu AND target.rok = source.rok
        WHEN MATCHED THEN
            UPDATE SET
                target.id_czasu = source.id_czasu,
                target.liczba_wyborcow = source.liczba_wyborcow,
                target.karty_wydane = source.karty_wydane,
                target.karty_niewykorzystane = source.karty_niewykorzystane,
                target.glosy_wazne = source.glosy_wazne,
                target.glosy_niewazne = source.glosy_niewazne,
                target.glosy_pelnomocnik = source.glosy_pelnomocnik,
                target.glosy_zaswiadczenie = source.glosy_zaswiadczenie
        WHEN NOT MATCHED THEN
            INSERT (id_obwodu, rok, id_czasu, liczba_wyborcow, karty_wydane, karty_niewykorzystane, glosy_wazne, glosy_niewazne, glosy_pelnomocnik, glosy_zaswiadczenie)
            VALUES (source.id_obwodu, source.rok, source.id_czasu, source.liczba_wyborcow, source.karty_wydane, source.karty_niewykorzystane, source.glosy_wazne, source.glosy_niewazne, source.glosy_pelnomocnik, source.glosy_zaswiadczenie);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text("DROP TABLE Fakt_Statystyki_Obwodu_TMP"))

    print("INFO --- Wykonano MERGE i usunięto tabelę tymczasową.")

def extractDataKomitety(csv_files):
    komitety = set()

    for file in csv_files:
        df = readAndLoadDataFromCSV(file)
        for col in df.columns:
            if col.startswith("KOMITET WYBORCZY") or col.startswith("KOALICYJNY KOMITET WYBORCZY"):
                komitety.add(col.strip())

    komitety = sorted(list(komitety))
    df_komitety = pd.DataFrame({
        'id_komitetu': range(1, len(komitety) + 1),
        'nazwa_komitetu': komitety,
        'skrot': [k.split()[-1] if len(k.split()) > 1 else k for k in komitety],
        'typ': ['koalicyjny' if 'KOALICYJNY' in k else 'komitet' for k in komitety]
    })

    return df_komitety

def loadDataKomitety(df_komitety, engine):
    df_komitety.to_sql('Wymiar_Komitet_TMP', con=engine, if_exists='replace', index=False)
    print("INFO --- Dane tymczasowe zapisane do Wymiar_Komitet_TMP.")

    merge_sql = """
        MERGE INTO Wymiar_Komitet AS target
        USING Wymiar_Komitet_TMP AS source
        ON target.id_komitetu = source.id_komitetu
        WHEN MATCHED THEN
            UPDATE SET
                target.nazwa_komitetu = source.nazwa_komitetu,
                target.skrot = source.skrot,
                target.typ = source.typ
        WHEN NOT MATCHED THEN
            INSERT (id_komitetu, nazwa_komitetu, skrot, typ)
            VALUES (source.id_komitetu, source.nazwa_komitetu, source.skrot, source.typ);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text("DROP TABLE Wymiar_Komitet_TMP"))

    print("INFO --- Wykonano MERGE i usunięto tabelę tymczasową.")

def extractDataWynikiWyborcze(csv_file, df_komitety):
    df = readAndLoadDataFromCSV(csv_file)
    rok = int(csv_file.split('_')[-1].split('.')[0])
    id_czasu = {
        2015: 20151025,
        2019: 20191013,
        2023: 20231015
    }.get(rok)

    df['id_obwodu'] = df.apply(
        lambda row: f"{int(row['KOD TERYTORIALNY'])}{int(row['Numer obwodu'])}" if pd.notnull(row['KOD TERYTORIALNY']) else None,
        axis=1
    )

    records = []
    for _, row in df.iterrows():
        id_obwodu = row['id_obwodu']
        if not id_obwodu:
            continue

        for _, komitet in df_komitety.iterrows():
            nazwa = komitet['nazwa_komitetu']
            if nazwa in row and pd.notnull(row[nazwa]):
                id_komitetu = komitet['id_komitetu']
                glosy = int(str(row[nazwa]).replace(' ', '').replace(',', '') or 0)
                id_wyniku = generate_id_wyniku(id_obwodu, rok, id_komitetu)

                records.append({
                    'id_wyniku': id_wyniku,
                    'id_obwodu': id_obwodu,
                    'rok': rok,
                    'id_komitetu': id_komitetu,
                    'id_czasu': id_czasu,
                    'glosy_na_komitet': glosy
                })

    return pd.DataFrame(records)

def loadDataWynikiWyborcze(df_wyniki, engine):
    df_wyniki.to_sql('Fakt_Wyniki_Wyborcze_TMP', con=engine, if_exists='replace', index=False)
    print("INFO --- Dane tymczasowe zapisane do Fakt_Wyniki_Wyborcze_TMP.")

    merge_sql = """
        MERGE INTO Fakt_Wyniki_Wyborcze AS target
        USING Fakt_Wyniki_Wyborcze_TMP AS source
        ON target.id_wyniku = source.id_wyniku
        WHEN MATCHED THEN
            UPDATE SET
                target.id_obwodu = source.id_obwodu,
                target.rok = source.rok,
                target.id_komitetu = source.id_komitetu,
                target.id_czasu = source.id_czasu,
                target.glosy_na_komitet = source.glosy_na_komitet
        WHEN NOT MATCHED THEN
            INSERT (id_wyniku, id_obwodu, rok, id_komitetu, id_czasu, glosy_na_komitet)
            VALUES (source.id_wyniku, source.id_obwodu, source.rok, source.id_komitetu, source.id_czasu, source.glosy_na_komitet);
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text("DROP TABLE Fakt_Wyniki_Wyborcze_TMP"))

    print("INFO --- Wykonano MERGE i usunięto tabelę tymczasową.")

def generate_id_wyniku(id_obwodu, rok, id_komitetu):
    key = f"{id_obwodu}_{rok}_{id_komitetu}"
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10 ** 10)


def main():
    engine = createEngine()

    loadWymiarCzas(engine)

    # Przetwarzanie danych obwodow
    obwody_csv_files = [
        "obwody_glosowania_2015.csv",
        "obwody_glosowania_2019.csv",
        "obwody_glosowania_2023.csv"
        ]
    for csv_file in obwody_csv_files:
        df_obwody = extractDataObwody(csv_file)

        # Sprawdzenie, czy id_gminy nie jest puste
        print("Sprawdzanie id_gminy w df_obwody:")
        print(df_obwody[['id_obwodu', 'id_gminy']].drop_duplicates().head())

        loadDataObwody(df_obwody, engine)

    # Przetwarzanie danych gmin
    gmina_csv_files = [
        "rejestr_wyborcow_2015.csv",
        "rejestr_wyborcow_2019.csv",
        "rejestr_wyborcow_2023.csv"
    ]
    for csv_file in gmina_csv_files:
        df_gminy = extractDataGminy(csv_file)
        loadDataGminy(df_gminy, engine)

    # Przetwarzanie danych wyniki
    stat_files = [
        "wyniki_gl_na_listy_po_obwodach_sejm_2015.csv",
        "wyniki_gl_na_listy_po_obwodach_sejm_2019.csv",
        "wyniki_gl_na_listy_po_obwodach_sejm_2023.csv"
    ]
    for csv_file in stat_files:
        df_stat = extractDataStatystykiObwodu(csv_file)
        print(df_stat[['id_obwodu', 'rok']].drop_duplicates())
        loadDataStatystykiObwodu(df_stat, engine)

    komitet_files = [
        "wyniki_gl_na_listy_po_obwodach_sejm_2015.csv",
        "wyniki_gl_na_listy_po_obwodach_sejm_2019.csv",
        "wyniki_gl_na_listy_po_obwodach_sejm_2023_utf8.csv"
    ]

    df_komitety = extractDataKomitety(komitet_files)
    loadDataKomitety(df_komitety, engine)

    for csv_file in komitet_files:
        df_wyniki = extractDataWynikiWyborcze(csv_file, df_komitety)
        loadDataWynikiWyborcze(df_wyniki, engine)


    # # Wstawienie danych do tabeli Wymiar_Obwod
    # df_obwody.to_sql('Wymiar_Obwod', con=engine, if_exists='append', index=False)
    # print("INFO --- Dane zostały zapisane do tabeli Wymiar_Obwod.")



if __name__ == '__main__':
    main()
