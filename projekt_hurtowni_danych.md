
# Model danych i proces ETL dla projektu hurtowni danych opartego na wynikach wyborów parlamentarnych w Polsce

## 🧱 Model danych (Data Warehouse Schema)

Proponuję klasyczny **schemat gwiazdy (star schema)**:

### 🧮 Tabela faktów: `Fakty_Glosy`
Zawiera dane liczbowe, które będziemy analizować.

| Kolumna              | Opis |
|----------------------|------|
| `id_glosowania`      | Klucz główny |
| `id_kandydat`        | Klucz obcy do wymiaru Kandydat |
| `id_komitet`         | Klucz obcy do wymiaru Komitet |
| `id_okreg`           | Klucz obcy do wymiaru Okręg |
| `id_data`            | Klucz obcy do wymiaru Data |
| `glosy`              | Liczba głosów oddanych |
| `glosy_wazne`        | Liczba ważnych głosów |
| `glosy_niewazne`     | Liczba nieważnych głosów |
| `frekwencja`         | Frekwencja w % |

### 📐 Wymiary (Dimensions)

#### 📅 `Wymiar_Data`
| Kolumna | Opis |
|---------|------|
| `id_data` | Klucz główny |
| `data` | Data wyborów |
| `rok` | Rok |
| `miesiac` | Miesiąc |
| `dzien_tygodnia` | Dzień tygodnia |

#### 🧑 `Wymiar_Kandydat`
| Kolumna | Opis |
|---------|------|
| `id_kandydat` | Klucz główny |
| `imie` | Imię |
| `nazwisko` | Nazwisko |
| `plec` | Płeć |
| `wiek` | Wiek |
| `miejsce_na_liscie` | Pozycja na liście |

#### 🏛️ `Wymiar_Komitet`
| Kolumna | Opis |
|---------|------|
| `id_komitet` | Klucz główny |
| `nazwa_komitetu` | Nazwa komitetu |
| `typ_komitetu` | Typ (partia, koalicja, niezależny) |

#### 🗺️ `Wymiar_Okreg`
| Kolumna | Opis |
|---------|------|
| `id_okreg` | Klucz główny |
| `nazwa_okregu` | Nazwa okręgu |
| `wojewodztwo` | Województwo |
| `liczba_mandatow` | Liczba mandatów w okręgu |

## 🔄 Proces ETL

### 1. Extract (Pobieranie danych)
- Pobranie plików CSV/XLSX z repozytorium PKW.
- Można zautomatyzować pobieranie lub ręcznie załadować pliki.

### 2. Transform (Przekształcanie danych)
- Czyszczenie danych (np. usunięcie pustych wierszy, konwersja typów).
- Agregacja głosów na poziomie okręgów.
- Obliczanie frekwencji.
- Mapowanie kandydatów do komitetów i okręgów.
- Obsługa delty danych (np. tylko nowe dane z kolejnych wyborów).

### 3. Load (Ładowanie danych)
- Załadowanie danych do tabel wymiarów i tabeli faktów w hurtowni danych (np. SQL Server).
- Można użyć SSIS, Python + SQLAlchemy, Airflow lub innego narzędzia ETL.
