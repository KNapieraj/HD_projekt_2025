
# Projekt Hurtowni Danych

## Fakty (tabele faktów)

### Fakt_Wyniki_Wyborcze
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_wyniku     | INT        | PK    | Unikalny identyfikator wyniku |
| id_obwodu     | INT        | FK    | Identyfikator obwodu głosowania |
| id_komitetu   | INT        | FK    | Identyfikator komitetu wyborczego |
| rok           | INT        |       | Rok wyborów (np. 2015, 2019, 2023) |
| glosy_oddane  | INT        |       | Liczba oddanych głosów |
| glosy_wazne   | INT        |       | Liczba ważnych głosów |
| glosy_na_komitet | INT     |       | Liczba głosów na komitet |

### Fakt_Rejestr_Wyborców
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_rejestru   | INT        | PK    | Unikalny identyfikator rejestru |
| id_gminy      | INT        | FK    | Identyfikator gminy |
| rok           | INT        |       | Rok |
| liczba_mieszkancow | INT   |       | Liczba mieszkańców |
| liczba_wyborcow | INT     |       | Liczba wyborców |

## Wymiary (tabele wymiarów)

### Wymiar_Gmina
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_gminy      | INT        | PK    | Unikalny identyfikator gminy |
| kod_teryt     | VARCHAR    |       | Kod TERYT gminy |
| nazwa_gminy   | VARCHAR    |       | Nazwa gminy |
| typ_gminy     | VARCHAR    |       | Typ gminy (m., gm., etc.) |
| powiat        | VARCHAR    |       | Powiat |
| wojewodztwo   | VARCHAR    |       | Województwo |

### Wymiar_Obwod
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_obwodu     | INT        | PK    | Unikalny identyfikator obwodu |
| numer_obwodu  | INT        |       | Numer obwodu |
| adres         | VARCHAR    |       | Adres obwodu |
| id_gminy      | INT        | FK    | Identyfikator gminy |

### Wymiar_Komitet
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_komitetu   | INT        | PK    | Unikalny identyfikator komitetu |
| nazwa_komitetu | VARCHAR   |       | Nazwa komitetu |
| skrot         | VARCHAR    |       | Skrót nazwy komitetu |
| typ           | VARCHAR    |       | Typ komitetu (koalicja, partia, etc.) |

### Wymiar_Czas
| Nazwa kolumny | Typ danych | Klucz | Opis |
|---------------|------------|-------|------|
| id_czasu      | INT        | PK    | Unikalny identyfikator czasu |
| rok           | INT        |       | Rok |
| miesiac       | INT        |       | Miesiąc |
| dzien         | INT        |       | Dzień |
| kwartal       | INT        |       | Kwartał |

## Relacje między tabelami
- `Fakt_Wyniki_Wyborcze.id_obwodu` -> `Wymiar_Obwod.id_obwodu`
- `Fakt_Wyniki_Wyborcze.id_komitetu` -> `Wymiar_Komitet.id_komitetu`
- `Fakt_Rejestr_Wyborców.id_gminy` -> `Wymiar_Gmina.id_gminy`
