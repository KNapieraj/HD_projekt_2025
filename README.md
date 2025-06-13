
# Hurtownie Danych
## 🗳️ Analiza Wyników Wyborczych: Polska 2015–2023

**Projekt analizy danych wyborczych** z lat 2015, 2019 i 2023 oparty o relacyjną bazę danych w Azure SQL Database. Projekt ma charakter edukacyjno-analityczny – umożliwia porównanie wyników głosowań w różnych latach, agregację danych na poziomie komisji i gmin oraz analizę trendów partyjnych.

---

## Struktura bazy danych

Baza została zaprojektowana w formie klasycznego modelu hurtownianego (star schema) z **faktami i wymiarami**.

### Wymiary czasu i organizacyjne
- `Wymiar_Czas` – szczegółowa data z dodatkowymi metadanymi (dzień, miesiąc, rok, liczba komisji itd.).
- `Wymiar_Gmina_YYYY` – dane demograficzne i organizacyjne dla gmin w latach wyborczych.
- `Wymiar_Obwody_YYYY` – pełna lista komisji wyborczych z danymi lokalizacyjnymi i technicznymi.

### Fakty szczegółowe (na poziomie komisji)
- `Fakt_Wyniki_2015`, `Fakt_Wyniki_2019`, `Fakt_Wyniki_2023` – szczegółowe wyniki z komisji (liczba głosów, kart, błędów).

### Fakty agregowane
- `Fakt_Agregowane_Wyniki_YYYY` – sumy wyników w skali kraju z podziałem na lata.
- `Fakt_Agregowane_Gmina_YYYY` – wyniki skonsolidowane na poziomie gminy.

---

### SQL Schema Diagram:
https://gh.atlasgo.cloud/explore/00b6259a

---

## ⚙️ Technologie i narzędzia
- **Azure SQL Database** – przechowywanie i przetwarzanie danych.
- **Azure Data Factory** – przepływy danych, import, porównania między tabelami.
- **SQL** – transformacja, czyszczenie i analiza danych.
- **Power BI** – wizualizacja wyników.

---

## 👨‍💻 Autor
**Jakub Adamczyk**<br>
**Wojciech Broniewicz**<br>
**Kamil Napieraj**<br>
**Arkadiusz Sanecki**<br>

---

## linki do danych:
- 2015 - https://parlament2015.pkw.gov.pl/
- 2019 - https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/
- 2023 - https://sejmsenat2023.pkw.gov.pl/sejmsenat2023/pl