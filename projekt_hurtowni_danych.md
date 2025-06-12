
# 🧱 Tabele faktów

## `Fakt_Wyniki_Wyborcze`

| Kolumna               | Typ danych | Klucz | Opis |
|------------------------|------------|-------|------|
| `id_wyniku`            | INT        | PK    | Unikalny identyfikator |
| `id_obwodu`            | VARCHAR    | FK    | Klucz do `Wymiar_Obwod` (np. `KOD TERYTORIALNY` + `Numer obwodu`) |
| `id_komitetu`          | INT        | FK    | Klucz do `Wymiar_Komitet` |
| `id_czasu`             | INT        | FK    | Klucz do `Wymiar_Czas` |
| `glosy_na_komitet`     | INT        |       | Liczba głosów oddanych na komitet |

## `Fakt_Statystyki_Obwodu`

| Kolumna               | Typ danych | Klucz | Opis |
|------------------------|------------|-------|------|
| `id_statystyki`        | INT        | PK    | Unikalny identyfikator |
| `id_obwodu`            | VARCHAR    | FK    | Klucz do `Wymiar_Obwod` |
| `id_czasu`             | INT        | FK    | Klucz do `Wymiar_Czas` |
| `liczba_wyborcow`      | INT        |       | Liczba wyborców w obwodzie |
| `karty_wydane`         | INT        |       | Liczba wydanych kart |
| `karty_niewykorzystane`| INT        |       | Liczba niewykorzystanych kart |
| `glosy_wazne`          | INT        |       | Liczba głosów ważnych |
| `glosy_niewazne`       | INT        |       | Liczba głosów nieważnych |
| `glosy_pelnomocnik`    | INT        |       | Głosy oddane przez pełnomocnika |
| `glosy_zaswiadczenie`  | INT        |       | Głosy oddane na podstawie zaświadczenia |

# 🧩 Tabele wymiarów

## `Wymiar_Gmina`

| Kolumna       | Typ danych | Klucz | Opis |
|----------------|------------|-------|------|
| `id_gminy`      | INT        | PK    | Unikalny identyfikator |
| `kod_teryt`     | VARCHAR    |       | Kod TERYT |
| `nazwa_gminy`   | VARCHAR    |       | Nazwa gminy |
| `typ_gminy`     | VARCHAR    |       | Typ gminy (m., gm., etc.) |
| `powiat`        | VARCHAR    |       | Powiat |
| `wojewodztwo`   | VARCHAR    |       | Województwo |

## `Wymiar_Obwod`

| Kolumna                         | Typ danych | Klucz | Opis |
|----------------------------------|------------|-------|------|
| `id_obwodu`                      | VARCHAR    | PK    | Unikalny identyfikator (`KOD TERYTORIALNY` + `Numer obwodu`) |
| `numer_obwodu`                  | INT        |       | Numer obwodu |
| `id_gminy`                      | INT        | FK    | Klucz do `Wymiar_Gmina` |
| `adres`                         | VARCHAR    |       | Pełna siedziba obwodu |
| `przystosowany_dla_niepelnosprawnych` | BOOLEAN |       | Czy przystosowany dla niepełnosprawnych |
| `typ_obwodu`                    | VARCHAR    |       | Typ obwodu (powszechny, odrębny) |
| `typ_obszaru`                   | VARCHAR    |       | Typ obszaru (miejski, wiejski) |
| `opis_granic`                   | TEXT       |       | Opis granic obwodu |

## `Wymiar_Komitet`

| Kolumna         | Typ danych | Klucz | Opis |
|------------------|------------|-------|------|
| `id_komitetu`     | INT        | PK    | Unikalny identyfikator komitetu |
| `nazwa_komitetu`  | VARCHAR    |       | Pełna nazwa komitetu |
| `skrot`           | VARCHAR    |       | Skrót (opcjonalnie) |
| `typ`             | VARCHAR    |       | Typ komitetu (partia, koalicja, inne) |

## `Wymiar_Czas`

| Kolumna   | Typ danych | Klucz | Opis |
|------------|------------|-------|------|
| `id_czasu`  | INT        | PK    | Unikalny identyfikator (np. `20231015`) |
| `rok`       | INT        |       | Rok |
| `miesiac`   | INT        |       | Miesiąc |
| `dzien`     | INT        |       | Dzień |
| `kwartal`   | INT        |       | Kwartał |
