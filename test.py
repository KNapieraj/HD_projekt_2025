import os
import pandas as pd


folder_path = 'dane_zrodlowe'


# Iteracja po plikach w folderze
# for file_name in os.listdir(folder_path):
#     if file_name.endswith('.csv'):
#         file_path = os.path.join(folder_path, file_name)
        # df = pd.read_csv(file_path, on_bad_lines='skip')  # Pandas 1.3+

        # dataframes[file_name] = df
        # print(f"\n{file_name}")
        # print(df.head())  # Wyświetlenie pierwszych 5 wierszy

data_csv = [
    "obwody_glosowania_2015.csv",
    "obwody_glosowania_2019.csv",
    "obwody_glosowania_2023_utf8.csv",
    "rejestr_wyborcow_2015_kw_3.csv",
    "rejestr_wyborcow_2019_kw_3.csv",
    "rejestr_wyborcow_2023_kw_3.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2015.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2019.csv",
    "wyniki_gl_na_listy_po_obwodach_sejm_2023_utf8.csv"
]


# file_name = "obwody_glosowania_2015.csv"
# print(f"Path:{os.path}")
# file_path = os.path.join(folder_path, file_name)
# df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')
# # dataframes[file_name] = df
# print(f"\n{file_name}")
# print(f"\n{df.head(1)}")


# dataframes = {}
# for i in range(0,9):
#     file_name = data_csv[i]
#     file_path = os.path.join(folder_path, file_name)
#     df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')
#     dataframes[file_name] = df
#     print(f"\n{file_name}")
#     print(f"\n{df.head(1)}")
#     column_line = df.columns
#     for column in column_line:
#         print(f"{column}\n")


import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

def extract_gmina_name(full_name):
    if isinstance(full_name, str) and ' ' in full_name:
        return full_name.split(' ', 1)[1].strip()
    return full_name

def read_csv(file_name):
    return pd.read_csv(file_name, sep=';', on_bad_lines='skip', dtype=str)

def load_gminy(df_obwody):
    df_obwody['Gmina_clean'] = df_obwody['Gmina'].apply(extract_gmina_name)
    gminy = df_obwody[['KOD TERYTORIALNY', 'Gmina_clean']].drop_duplicates().reset_index(drop=True)
    gminy['id_gminy'] = gminy.index + 1
    return gminy

def map_id_gminy(df, gminy):
    df['Gmina_clean'] = df['Gmina'].apply(extract_gmina_name)
    return df.merge(gminy, on=['KOD TERYTORIALNY', 'Gmina_clean'])

def load_obwody(df_obwody, gminy):
    df = map_id_gminy(df_obwody, gminy)
    df['id_obwodu'] = df['KOD TERYTORIALNY'].astype(str) + df['Numer obwodu'].astype(str)
    df['przystosowany_dla_niepelnosprawnych'] = df['Przystosowany dla niepełnosprawnych'].map({'T': 'True', 'N': 'False'})
    return df[['id_obwodu', 'Numer obwodu', 'id_gminy', 'Pełna siedziba', 'przystosowany_dla_niepelnosprawnych', 'Typ obwodu', 'Typ obszaru', 'Opis granic']].rename(columns={
        'Numer obwodu': 'numer_obwodu',
        'Pełna siedziba': 'adres',
        'Typ obwodu': 'typ_obwodu',
        'Typ obszaru': 'typ_obszaru',
        'Opis granic': 'opis_granic'
    })

def load_statystyki(df_stat):
    df_stat['id_obwodu'] = df_stat['KOD TERYTORIALNY'].astype(str) + df_stat['Numer obwodu'].astype(str)
    df_stat['id_czasu'] = 1
    df_stat['id_statystyki'] = range(1, len(df_stat) + 1)
    return df_stat.rename(columns={
        'Liczba wyborców': 'liczba_wyborcow',
        'Wydane karty': 'karty_wydane',
        'Niewykorzystane karty': 'karty_niewykorzystane',
        'Głosy ważne': 'glosy_wazne',
        'Głosy nieważne': 'glosy_niewazne',
        'Liczba wyborców głosujących przez pełnomocnika': 'glosy_pelnomocnik',
        'Liczba wyborców głosujących na podstawie zaświadczenia o prawie do głosowania': 'glosy_zaswiadczenie'
    })[['id_statystyki', 'id_obwodu', 'id_czasu', 'liczba_wyborcow', 'karty_wydane', 'karty_niewykorzystane', 'glosy_wazne', 'glosy_niewazne', 'glosy_pelnomocnik', 'glosy_zaswiadczenie']]

def load_komitety_i_wyniki(df_wyniki):
    komitety = [col for col in df_wyniki.columns if col.startswith('KOMITET')]
    komitet_df = pd.DataFrame({
        'id_komitetu': range(1, len(komitety) + 1),
        'nazwa_komitetu': komitety,
        'skrot': None,
        'typ': None
    })

    wyniki = []
    for _, row in df_wyniki.iterrows():
        id_obwodu = str(row['KOD TERYTORIALNY']) + str(row['Numer obwodu'])
        for idx, komitet in enumerate(komitety):
            wyniki.append({
                'id_wyniku': len(wyniki) + 1,
                'id_obwodu': id_obwodu,
                'id_komitetu': idx + 1,
                'id_czasu': 1,
                'glosy_na_komitet': row[komitet]
            })
    return komitet_df, pd.DataFrame(wyniki)

def load_czas():
    return pd.DataFrame([{
        'id_czasu': 1,
        'rok': 2015,
        'miesiac': 10,
        'dzien': 25,
        'kwartal': 4
    }])

def main():
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

    df_obwody = read_csv("dane_zrodlowe/obwody_glosowania_2015.csv")
    df_stat = read_csv("dane_zrodlowe/rejestr_wyborcow_2015_kw_3.csv")
    df_wyniki = read_csv("dane_zrodlowe/wyniki_gl_na_listy_po_obwodach_sejm_2015.csv")

    gminy = load_gminy(df_obwody)
    obwody = load_obwody(df_obwody, gminy)
    statystyki = load_statystyki(df_stat)
    komitety, wyniki = load_komitety_i_wyniki(df_wyniki)
    czas = load_czas()

    gminy.to_sql('Wymiar_Gmina', engine, if_exists='append', index=False)
    obwody.to_sql('Wymiar_Obwod', engine, if_exists='append', index=False)
    statystyki.to_sql('Fakt_Statystyki_Obwodu', engine, if_exists='append', index=False)
    komitety.to_sql('Wymiar_Komitet', engine, if_exists='append', index=False)
    wyniki.to_sql('Fakt_Wyniki_Wyborcze', engine, if_exists='append', index=False)
    czas.to_sql('Wymiar_Czas', engine, if_exists='append', index=False)

if __name__ == '__main__':
    main()
