
-- Tabele faktów

CREATE TABLE Fakt_Wyniki_Wyborcze (
    id_wyniku INT PRIMARY KEY,
    id_obwodu VARCHAR(255),
    id_komitetu INT,
    id_czasu INT,
    glosy_na_komitet INT,
    FOREIGN KEY (id_obwodu) REFERENCES Wymiar_Obwod(id_obwodu),
    FOREIGN KEY (id_komitetu) REFERENCES Wymiar_Komitet(id_komitetu),
    FOREIGN KEY (id_czasu) REFERENCES Wymiar_Czas(id_czasu)
);

CREATE TABLE Fakt_Statystyki_Obwodu (
    id_statystyki INT PRIMARY KEY,
    id_obwodu VARCHAR(255),
    id_czasu INT,
    liczba_wyborcow INT,
    karty_wydane INT,
    karty_niewykorzystane INT,
    glosy_wazne INT,
    glosy_niewazne INT,
    glosy_pelnomocnik INT,
    glosy_zaswiadczenie INT,
    FOREIGN KEY (id_obwodu) REFERENCES Wymiar_Obwod(id_obwodu),
    FOREIGN KEY (id_czasu) REFERENCES Wymiar_Czas(id_czasu)
);

-- Tabele wymiarów

CREATE TABLE Wymiar_Gmina (
    id_gminy INT PRIMARY KEY,
    kod_teryt VARCHAR(255),
    nazwa_gminy VARCHAR(255),
    typ_gminy VARCHAR(255),
    powiat VARCHAR(255),
    wojewodztwo VARCHAR(255)
);

CREATE TABLE Wymiar_Obwod (
    id_obwodu VARCHAR(255) PRIMARY KEY,
    numer_obwodu INT,
    id_gminy INT,
    adres VARCHAR(255),
    przystosowany_dla_niepelnosprawnych BOOLEAN,
    typ_obwodu VARCHAR(255),
    typ_obszaru VARCHAR(255),
    FOREIGN KEY (id_gminy) REFERENCES Wymiar_Gmina(id_gminy)
);

CREATE TABLE Wymiar_Komitet (
    id_komitetu INT PRIMARY KEY,
    nazwa_komitetu VARCHAR(255),
    skrot VARCHAR(255),
    typ VARCHAR(255)
);

CREATE TABLE Wymiar_Czas (
    id_czasu INT PRIMARY KEY,
    rok INT,
    miesiac INT,
    dzien INT,
    kwartal INT
);
