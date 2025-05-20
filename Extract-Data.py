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

dataframes = {}
for i in range(0,9):
    file_name = data_csv[i]
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')
    dataframes[file_name] = df
    print(f"\n{file_name}")
    print(f"\n{df.head(1)}")
    column_line = df.columns
    for column in column_line:
        print(f"{column}\n")


def readAndLoadDataFromCSV(csv_file):
    # Ścieżka do folderu z plikami CSV
    folder_path = 'dane_zrodlowe'
    # Sprawdzenie, czy folder istnieje
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"INFO --- Folder '{folder_path}' nie istnieje.")
    file_path = os.path.join(folder_path, csv_file)
    print(f"INFO --- {csv_file}")
    return pd.read_csv(file_path, on_bad_lines='skip', sep=';')
    # dataframes[file_name] = df

def extractDataObwody(csv_file):
    # Lista do przechowywania DataFrame'ów
    dataframes = {}
    df = readAndLoadDataFromCSV(csv_file)
    dataframes[csv_file] = df

    # Zamiana wszystkich wierszy na listę słowników
    list_of_dicts = df.to_dict(orient='records')

    # Dodanie pola "ID KOMISJI" do każdego słownika
    for row in list_of_dicts:
        row["ID KOMISJI"] = f"{row['KOD TERYTORIALNY']}{row['Numer obwodu']}"
    return list_of_dicts

def main():
    csv_file = "obwody_glosowania_2015.csv"
    tests = extractDataObwody(csv_file)

if __name__ == '__main__':
    # main()
    print("done")

