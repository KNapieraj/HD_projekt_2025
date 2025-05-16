| Skrót / Termin       | Znaczenie                                                                 |
|----------------------|---------------------------------------------------------------------------|
| **DWH**              | Data Warehouse – hurtownia danych, specjalna baza danych do analizy.     |
| **ETL**              | Extract, Transform, Load – proces pobierania, przekształcania i ładowania danych. |
| **SQL**              | Structured Query Language – język zapytań do baz danych.                  |
| **SSIS**             | SQL Server Integration Services – narzędzie Microsoft do ETL.             |
| **SSAS**             | SQL Server Analysis Services – narzędzie Microsoft do analizy danych OLAP.|
| **SSRS**             | SQL Server Reporting Services – narzędzie Microsoft do raportowania.      |
| **SCD**              | Slowly Changing Dimension – technika zarządzania zmianami w danych wymiarów. |
| **OLAP**             | Online Analytical Processing – analiza danych w wielu wymiarach.          |
| **Delta danych**     | Zmiany w danych od ostatniego załadowania (np. nowe lub zmodyfikowane rekordy). |
| **BI**               | Business Intelligence – analiza danych biznesowych i podejmowanie decyzji. |
| **Power BI**         | Narzędzie Microsoft do tworzenia interaktywnych raportów i dashboardów.   |
| **Airflow**          | Narzędzie open-source do zarządzania przepływami danych (workflow).       |
| **Pentaho**          | Platforma open-source do integracji danych i analizy biznesowej.          |
| **Oracle Data Integrator** | Narzędzie firmy Oracle do tworzenia procesów ETL.                   |
| **CSV**              | Comma-Separated Values – format plików tekstowych do danych tabelarycznych. |


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