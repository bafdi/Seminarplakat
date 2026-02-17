# Wissenschaftliches Poster Generator

Dieses Python-Skript erstellt automatisch ein wissenschaftliches Poster im DIN A0 Format zum Thema "Automatisiertes Scheinwerfer-Nachführsystem mit UWB-Technologie".

## Voraussetzungen

- Python 3.x
- matplotlib

## Installation

```bash
pip install matplotlib
```

## Verwendung

Führen Sie das Skript aus:

```bash
python3 poster.py
```

Das Skript erstellt zwei Dateien:
- `poster_final.png` - Hochauflösendes PNG-Bild (150 DPI)
- `poster_final.pdf` - PDF-Version des Posters

## Anpassung

Alle Texte sind als Variablen am Anfang des Skripts definiert und können einfach geändert werden:

- `TITLE` - Haupttitel des Posters
- `SUBTITLE` - Untertitel
- `AUTHOR` - Name des Autors
- `SCHOOL` - Name der Schule
- `TEXT_*` - Verschiedene Inhaltstexte für die Spalten

## Spezifikationen

- **Format**: DIN A0 (845 mm × 1193 mm)
- **Layout**: 3 Spalten mit Header
- **Farbschema**:
  - Hintergrund: #F2F1E4
  - Header-Blau: #4495D1
  - Akzent-Grün: #8DC63F
  - Akzent-Orange: #F8971D
  - Akzent-Rot: #F15A36
  - Text-Dunkelgrau: #58595B

## Inhalt

Das Poster umfasst:

1. **Spalte 1**: Problem & Konzeption
   - Problemstellung
   - Lösungsansatz
   - Systemübersicht (Platzhalter)

2. **Spalte 2**: Technische Umsetzung
   - Hardware-Komponenten
   - Ortungsfunktionsweise (Multilateration)
   - Inverse Kinematik
   - Platzhalter für Hardware-Diagramme

3. **Spalte 3**: Ergebnisse & Fazit
   - Erprobung & Messungen
   - Ergebnisse
   - Fazit & Ausblick
   - Platzhalter für Messdiagramme

## Lizenz

Dieses Projekt ist für akademische Zwecke erstellt.
