#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wissenschaftliches Poster Generator - DIN A0 Format
Thema: Automatisiertes Scheinwerfer-Nachführsystem mit UWB-Technologie
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patches as mpatches

# ==================== KONFIGURATION ====================

# Farbschema (zwingend einzuhalten)
COLORS = {
    'background': '#F2F1E4',
    'header_blue': '#4495D1',
    'accent_green': '#8DC63F',
    'accent_orange': '#F8971D',
    'accent_red': '#F15A36',
    'text_darkgray': '#58595B'
}

# Format DIN A0 mit Anschnitt: 845 mm x 1193 mm
# Umrechnung: 1 inch = 25.4 mm
WIDTH_MM = 845
HEIGHT_MM = 1193
WIDTH_INCH = WIDTH_MM / 25.4
HEIGHT_INCH = HEIGHT_MM / 25.4

# Schriftarten
FONT_FAMILY = 'Arial'  # Fallback für Gotham
FONT_SIZES = {
    'title': 56,
    'subtitle': 36,
    'author': 32,
    'section_header': 44,
    'subsection': 32,
    'body': 24,
    'caption': 20
}

# ==================== INHALTE (als Variablen) ====================

# Header Informationen
TITLE = "Konzeption, Aufbau und Erprobung eines automatisierten\nScheinwerfer-Nachführsystems"
SUBTITLE = "Entwicklung eines mechatronischen Kleinsystems mit Arduino/ESP32"
AUTHOR = "Sebastian Pfleiderer"
SCHOOL = "Staatliche Fachoberschule München-West"

# Spalte 1: Problem & Konzeption
TEXT_EINLEITUNG = """Manuelle Verfolgerspots in Theatern und bei Veranstaltungen 
sind personalintensiv und erfordern geschulte Operatoren. 
Professionelle automatisierte Trackingsysteme wie ZacTrack 
kosten mehr als 20.000 € und sind für Schulen, Kirchen oder 
kleinere Veranstaltungsorte nicht erschwinglich."""

TEXT_PROBLEM_TITLE = "Problem & Ausgangssituation"

TEXT_ZIEL = """Entwicklung eines kostengünstigen, automatisierten 
Scheinwerfer-Trackingsystems für Schulen und kleine 
Veranstaltungsorte mit einem Budgetrahmen unter 500 €."""

TEXT_LOESUNGSANSATZ_TITLE = "Lösungsansatz"
TEXT_LOESUNGSANSATZ = """• UWB (Ultra-Wideband) Technologie zur präzisen 
  Positionsbestimmung im 3D-Raum
• DMX512-Protokoll zur Ansteuerung von Moving Head 
  Scheinwerfern
• ESP32 Mikrocontroller als zentrale Recheneinheit
• Multilateration mit 4 Anchors zur Positionsberechnung
• Inverse Kinematik zur Berechnung der Pan/Tilt-Winkel"""

# Spalte 2: Technische Umsetzung
TEXT_HARDWARE_TITLE = "Hardware-Komponenten"
TEXT_HARDWARE = """• ESP32 Mikrocontroller (Dual-Core, WiFi/BLE)
• Makerfabs UWB Module (4× Anchor, 1× Tag)
  - Basierend auf DW1000 Chip
  - Frequenz: 3.5 - 6.5 GHz
  - Reichweite: bis 50m (Line-of-Sight)
• MAX485 TTL-zu-RS485 Konverter für DMX-Ausgabe
• Moving Head Scheinwerfer (DMX-kompatibel)"""

TEXT_ORTUNG_TITLE = "Funktionsweise der Ortung"
TEXT_ORTUNG = """Time-of-Flight (ToF) Messung:
Jeder der 4 fest installierten Anchors sendet ein Signal an 
das mobile Tag (am Akteur befestigt). Aus den Laufzeiten 
werden die Distanzen berechnet.

Multilateration (3D-Trilateration):
Mit mindestens 4 bekannten Distanzen zu fest positionierten 
Anchors können die X-, Y- und Z-Koordinaten des Tags im 
Raum eindeutig bestimmt werden (Schnittpunkt von Kugeln)."""

TEXT_KINEMATIK_TITLE = "Inverse Kinematik"
TEXT_KINEMATIK = """Aus der berechneten 3D-Position (X, Y, Z) des Tags relativ 
zum Scheinwerfer werden die benötigten DMX-Werte für die 
Pan- und Tilt-Achse des Moving Heads berechnet:

Pan-Winkel  = arctan2(X, Y)
Tilt-Winkel = arctan2(Z, √(X² + Y²))

Die Winkel werden auf den DMX-Wertebereich (0-255 oder 
0-65535 bei 16-Bit) skaliert und an den Scheinwerfer gesendet."""

# Spalte 3: Ergebnisse & Fazit
TEXT_ERPROBUNG_TITLE = "Erprobung & Messungen"
TEXT_ERPROBUNG = """Testumgebung:
Turnhalle im Kloster Schäftlarn
Raumabmessungen: ca. 20m × 15m × 8m Höhe
4 Anchors in den Ecken an der Decke montiert

Messmethode:
Vergleich der gemessenen Tag-Positionen mit bekannten 
Referenzpositionen und manuelle Validierung der DMX-Werte 
durch Abgleich mit professionellem Lichtpult."""

TEXT_ERGEBNISSE_TITLE = "Ergebnisse"
TEXT_ERGEBNISSE = """Positionsgenauigkeit:
• X/Y-Achse (lateral):  < 10 cm Abweichung ✓
• Z-Achse (Höhe):       Größerer Jitter (15-25 cm)

DMX-Werte:
• Sehr hohe Übereinstimmung mit manueller Referenz
• Latenz: ca. 100-150 ms (akzeptabel für langsame 
  Bewegungen wie Vorträge, zu hoch für Sport)

Materialkosten: ca. 270 €
(vs. 20.000 € für professionelle Industrielösung)"""

TEXT_FAZIT_TITLE = "Fazit & Ausblick"
TEXT_FAZIT = """Das entwickelte System demonstriert erfolgreich die 
Machbarkeit eines Low-Cost Trackingsystems für Moving Head 
Scheinwerfer auf Basis von UWB-Technologie.

Vorteile:
✓ Drastische Kostenreduktion (> 98%)
✓ Ausreichende Genauigkeit für typische Anwendungsfälle
✓ Einfache Installation und Bedienung

Einschränkungen:
⚠ Z-Achsen-Ungenauigkeit (bekanntes UWB-Problem)
⚠ Latenz für hochdynamische Anwendungen zu hoch

Verbesserungspotenzial:
• Kalman-Filter zur Rauschunterdrückung
• Multi-Tag Support für mehrere Akteure
• Integration mit Bühnenbilddaten (Collision Avoidance)"""

# ==================== FUNKTIONEN ====================

def create_text_box(ax, x, y, width, height, title, content, title_color, 
                     title_fontsize=None, content_fontsize=None, alpha=0.95):
    """
    Erstellt eine Text-Box mit farbigem Header
    """
    if title_fontsize is None:
        title_fontsize = FONT_SIZES['section_header']
    if content_fontsize is None:
        content_fontsize = FONT_SIZES['body']
    
    # Hintergrund-Box für den gesamten Bereich
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.01",
        edgecolor=COLORS['text_darkgray'],
        facecolor='white',
        alpha=alpha,
        linewidth=2,
        transform=ax.transAxes
    )
    ax.add_patch(box)
    
    # Titel-Bereich (farbiger Header)
    header_height = 0.08
    title_box = FancyBboxPatch(
        (x, y + height - header_height), width, header_height,
        boxstyle="round,pad=0.005",
        edgecolor=title_color,
        facecolor=title_color,
        alpha=1.0,
        linewidth=0,
        transform=ax.transAxes
    )
    ax.add_patch(title_box)
    
    # Titel-Text (weiß auf farbigem Grund)
    ax.text(
        x + width/2, y + height - header_height/2,
        title,
        ha='center', va='center',
        fontsize=title_fontsize,
        fontfamily=FONT_FAMILY,
        fontweight='bold',
        color='white',
        transform=ax.transAxes
    )
    
    # Inhalt-Text
    ax.text(
        x + 0.02, y + height - header_height - 0.03,
        content,
        ha='left', va='top',
        fontsize=content_fontsize,
        fontfamily=FONT_FAMILY,
        color=COLORS['text_darkgray'],
        transform=ax.transAxes,
        wrap=True
    )

def create_image_placeholder(ax, x, y, width, height, label, alpha=0.9):
    """
    Erstellt einen Platzhalter für ein Bild/Diagramm
    """
    placeholder = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.005",
        edgecolor=COLORS['accent_orange'],
        facecolor='#EEEEEE',
        alpha=alpha,
        linewidth=3,
        linestyle='--',
        transform=ax.transAxes
    )
    ax.add_patch(placeholder)
    
    # Label-Text
    ax.text(
        x + width/2, y + height/2,
        f"[Bild: {label}]",
        ha='center', va='center',
        fontsize=FONT_SIZES['caption'],
        fontfamily=FONT_FAMILY,
        color=COLORS['text_darkgray'],
        style='italic',
        transform=ax.transAxes
    )

def create_poster():
    """
    Erstellt das komplette Poster
    """
    # Figure mit DIN A0 Größe erstellen
    fig = plt.figure(figsize=(WIDTH_INCH, HEIGHT_INCH), dpi=150)
    fig.patch.set_facecolor(COLORS['background'])
    
    # GridSpec für Layout (Header + 3 Spalten)
    gs = gridspec.GridSpec(
        2, 3,  # 2 Zeilen, 3 Spalten
        figure=fig,
        height_ratios=[0.15, 0.85],  # Header 15%, Content 85%
        width_ratios=[1, 1, 1],
        hspace=0.02,
        wspace=0.02,
        left=0.02, right=0.98,
        top=0.98, bottom=0.02
    )
    
    # ==================== HEADER ====================
    ax_header = fig.add_subplot(gs[0, :])
    ax_header.axis('off')
    
    # Hintergrund für Header
    header_bg = Rectangle(
        (0, 0), 1, 1,
        facecolor=COLORS['header_blue'],
        edgecolor='none',
        transform=ax_header.transAxes
    )
    ax_header.add_patch(header_bg)
    
    # Logo-Platzhalter (oben links)
    logo_placeholder = Rectangle(
        (0.02, 0.15), 0.12, 0.7,
        facecolor='white',
        edgecolor=COLORS['text_darkgray'],
        linewidth=2,
        transform=ax_header.transAxes
    )
    ax_header.add_patch(logo_placeholder)
    ax_header.text(
        0.08, 0.5, '[LOGO\nSchule]',
        ha='center', va='center',
        fontsize=FONT_SIZES['caption'],
        fontfamily=FONT_FAMILY,
        color=COLORS['text_darkgray'],
        transform=ax_header.transAxes
    )
    
    # Titel
    ax_header.text(
        0.50, 0.68, TITLE,
        ha='center', va='top',
        fontsize=FONT_SIZES['title'],
        fontfamily=FONT_FAMILY,
        fontweight='bold',
        color='white',
        transform=ax_header.transAxes
    )
    
    # Untertitel
    ax_header.text(
        0.50, 0.35, SUBTITLE,
        ha='center', va='top',
        fontsize=FONT_SIZES['subtitle'],
        fontfamily=FONT_FAMILY,
        color='white',
        style='italic',
        transform=ax_header.transAxes
    )
    
    # Autor
    ax_header.text(
        0.50, 0.12, AUTHOR,
        ha='center', va='top',
        fontsize=FONT_SIZES['author'],
        fontfamily=FONT_FAMILY,
        fontweight='bold',
        color='white',
        transform=ax_header.transAxes
    )
    
    # Schule
    ax_header.text(
        0.50, 0.02, SCHOOL,
        ha='center', va='bottom',
        fontsize=FONT_SIZES['body'],
        fontfamily=FONT_FAMILY,
        color='white',
        transform=ax_header.transAxes
    )
    
    # ==================== SPALTE 1: Problem & Konzeption ====================
    ax_col1 = fig.add_subplot(gs[1, 0])
    ax_col1.axis('off')
    ax_col1.set_xlim(0, 1)
    ax_col1.set_ylim(0, 1)
    
    # Problem Box
    create_text_box(
        ax_col1, 0.02, 0.68, 0.96, 0.30,
        TEXT_PROBLEM_TITLE, TEXT_EINLEITUNG + "\n\n" + TEXT_ZIEL,
        COLORS['accent_red'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Lösungsansatz Box
    create_text_box(
        ax_col1, 0.02, 0.35, 0.96, 0.30,
        TEXT_LOESUNGSANSATZ_TITLE, TEXT_LOESUNGSANSATZ,
        COLORS['accent_green'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Bild-Platzhalter 1: Systemübersicht
    create_image_placeholder(
        ax_col1, 0.02, 0.02, 0.96, 0.30,
        "Systemübersicht / Flowchart\n(Sensorik → Berechnung → Aktorik)"
    )
    
    # ==================== SPALTE 2: Technische Umsetzung ====================
    ax_col2 = fig.add_subplot(gs[1, 1])
    ax_col2.axis('off')
    ax_col2.set_xlim(0, 1)
    ax_col2.set_ylim(0, 1)
    
    # Hardware Box
    create_text_box(
        ax_col2, 0.02, 0.78, 0.96, 0.20,
        TEXT_HARDWARE_TITLE, TEXT_HARDWARE,
        COLORS['header_blue'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Bild-Platzhalter 2: Hardware-Blockschaltbild
    create_image_placeholder(
        ax_col2, 0.02, 0.62, 0.96, 0.14,
        "Hardware-Blockschaltbild\n(ESP32 / DMX)"
    )
    
    # Ortung Box
    create_text_box(
        ax_col2, 0.02, 0.38, 0.96, 0.22,
        TEXT_ORTUNG_TITLE, TEXT_ORTUNG,
        COLORS['accent_green'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Bild-Platzhalter 3: Trilateration
    create_image_placeholder(
        ax_col2, 0.02, 0.24, 0.96, 0.12,
        "Trilateration\n(Kugelschnittpunkte)"
    )
    
    # Kinematik Box
    create_text_box(
        ax_col2, 0.02, 0.02, 0.96, 0.20,
        TEXT_KINEMATIK_TITLE, TEXT_KINEMATIK,
        COLORS['accent_orange'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # ==================== SPALTE 3: Ergebnisse & Fazit ====================
    ax_col3 = fig.add_subplot(gs[1, 2])
    ax_col3.axis('off')
    ax_col3.set_xlim(0, 1)
    ax_col3.set_ylim(0, 1)
    
    # Erprobung Box
    create_text_box(
        ax_col3, 0.02, 0.73, 0.96, 0.25,
        TEXT_ERPROBUNG_TITLE, TEXT_ERPROBUNG,
        COLORS['header_blue'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Bild-Platzhalter 4: Messabweichungen
    create_image_placeholder(
        ax_col3, 0.02, 0.58, 0.96, 0.13,
        "Messabweichungen\n(Scatterplot Soll vs. Ist)"
    )
    
    # Ergebnisse Box
    create_text_box(
        ax_col3, 0.02, 0.37, 0.96, 0.19,
        TEXT_ERGEBNISSE_TITLE, TEXT_ERGEBNISSE,
        COLORS['accent_green'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    # Fazit Box
    create_text_box(
        ax_col3, 0.02, 0.02, 0.96, 0.33,
        TEXT_FAZIT_TITLE, TEXT_FAZIT,
        COLORS['accent_orange'],
        title_fontsize=FONT_SIZES['section_header'],
        content_fontsize=FONT_SIZES['body']
    )
    
    return fig

# ==================== MAIN ====================

if __name__ == "__main__":
    print("Erstelle wissenschaftliches Poster (DIN A0)...")
    print(f"Format: {WIDTH_MM} mm × {HEIGHT_MM} mm")
    print(f"        ({WIDTH_INCH:.2f} inch × {HEIGHT_INCH:.2f} inch)")
    
    # Poster erstellen
    fig = create_poster()
    
    # Speichern
    output_filename = "poster_final.png"
    print(f"\nSpeichere Poster als '{output_filename}'...")
    fig.savefig(
        output_filename,
        dpi=150,
        bbox_inches='tight',
        facecolor=COLORS['background'],
        edgecolor='none'
    )
    print("✓ Poster erfolgreich erstellt!")
    print(f"  Datei: {output_filename}")
    
    # Optional: Auch als PDF speichern
    output_pdf = "poster_final.pdf"
    print(f"\nSpeichere zusätzlich als PDF: '{output_pdf}'...")
    fig.savefig(
        output_pdf,
        dpi=150,
        bbox_inches='tight',
        facecolor=COLORS['background'],
        edgecolor='none'
    )
    print("✓ PDF erfolgreich erstellt!")
    
    plt.close(fig)
    print("\nFertig!")