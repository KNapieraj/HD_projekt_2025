## Hurtownie danych - projekt zaliczeniowy - laboratoria
### Cel projektu
Praktyczne poznanie:
- Architektury hurtowni danych
- Tworzenie procesu ETL
- Raportowanie przy pomocy SQL i narzędzi Microsoft

---

### Timeline
Składowe zaliczenia projektu:
- Obowiązkowa prezentacja projektu 2025-06-15, podczas laboratoriów stacjonarnych,
- Zamieszczenie projektu na Moodle do 2024-06-13 23:59, każda osoba z zespołu (1 ocena na zespół wg poniższej tabeli),

---

#### Prezentacja projektu
- Do 10 min na zespół
  - Krótka prezentacja:
    - cel biznesowy,
    - opis źródeł danych,
    - opis realizacji projektu,
    - przykładowy kod, printscreeny odpowiadające elementom składowych, uzyskane wyniki
  - testowe uruchominie ETL (proszę mieć pewność, że narzędzia zadziałają na uczelnianym maszynie wirutalnej lub urządzeniu prywatnym (polecam drugie podejście)),
- Do 5 min - dyskusja/pytania,
- Zespoły najelpej 4 osobowe,

---

#### Do zamieszczenia na Moodle
- Katalog .zip projektu (kod sql, skrypty, pliki ssis), w przypadku dużych zbiorów nie zamieszczamy samych danych, ale wymagany jest ich opis i wskazanie w dokumentacji,
- Plik z dokumnentacją (.pdf/.md) - Opis projektu analogiczny do tego z części prezentacji + krótka instrukacja uruchominia i wnioski,
- Projekt na Moodle powinna zamieścić każda osoba z zespołu,

---

### Ocena składowych

| Składowa projektu                                                                                                                                                                                                                                                                                   |  max %   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| (Obowiązkowo) Model hurtowni (min. 1 tabela faktów, 3 wymiary (w tym wymiar dat)), z zachowaniem logiki specyficznych dla DWH; Opracowanie procesu ETL - udany przebieg testowy, uzupełnienie tabel danymi (konieczna agregacja i pewne transforamacji, zestaw danych inny niż na przykładach z laboratoriów). Podstawowa obsługa delty danych. 3 przykaładowe raporty. |  |
| (Obowiązkowo) Dokumentacja i opis projektu |    |
| Zaawansowana obsługa delty danych, dobrych praktyk, walidacje, logowanie                                                                                                                                                                                                                                 | +/++    |
| Projekt z uwzględnieniem różnych SCD w tabelach wymiarów                                                                                                                                                                                                                     | +/++    |
| Integracja z innymi źródałmi danych / dane live                                                                                                                                                                                                                                                         | n * +|
| Opracowanie procesu ETL przy pomocy SSIS (lub inne dedykowane narzędzie, np AirFlow, Pentaho, Oracle Data Integrator itp.)                                                                                                                                                                                                                                       | ++   |
| Wykorzystanie SSAS (lub inne OLAP)                                                                                                                                                                                                                                                                                  | +    |
| Wykorzystanie SSRS (lub inne narzędzie raportowe BI (np Power BI, Dash, Bokeh itp.))                                                                                                                                                                                                                                                                                | +/++    |
| Dodanie przykładowych raportów jako zapytania zaawansowanego SQL/wizualizacji, ale wymaga wykorzystania użycia zapytań o różnym stopniu komplikacji technik                            | + |


 `+` - orientacyjna składowa przy prawidłowej implementacji dodająca ok 3-5% w zależności od problemu/technologii;  
 `++` - orientacyjna składowa przy prawidłowej implementacji dodająca ok 5-20% w zależności od problemu/technologii;