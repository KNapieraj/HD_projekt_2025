import os
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
    return pd.read_csv(file_path, on_bad_lines='skip', sep=';')

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



def main():
    # Przetwarzanie danych obwodow
    obwody_csv_files = [
        "obwody_glosowania_2015.csv",
        "obwody_glosowania_2019.csv",
        "obwody_glosowania_2023.csv"
        ]

    engine = createEngine()

    for csv_file in obwody_csv_files:
        df_obwody = extractDataObwody(csv_file)
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


    # # Wstawienie danych do tabeli Wymiar_Obwod
    # df_obwody.to_sql('Wymiar_Obwod', con=engine, if_exists='append', index=False)
    # print("INFO --- Dane zostały zapisane do tabeli Wymiar_Obwod.")



if __name__ == '__main__':
    main()
