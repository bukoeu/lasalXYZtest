# Drei-Achsen-Projekt (Prototyp)

[![Test](https://github.com/bukoeu/lasalXYZtest/actions/workflows/test.yml/badge.svg)](https://github.com/bukoeu/lasalXYZtest/actions/workflows/test.yml)

Dieses Projekt beschreibt eine PLC-basierte Drei-Achsen-Steuerung mit TCP-Kommunikation, Bewegungslogik, Antriebsanbindung und Safety-/Hardwareueberwachung.

## Ziel

Das Ziel ist eine einfache Struktur fuer eine Maschine mit:

- X-Achse
- Y-Achse
- Z-Achse
- TCP-Kommandos von einem externen System
- Bewegungssteuerung ueber einen Motion Controller
- Drive- und Encoder-Anbindung
- Safety- und Hardwarestatus

## Grundidee

Ein externes System sendet ASCII-Kommandos ueber TCP. Die Steuerung nimmt diese Kommandos entgegen, dekodiert sie und leitet sie an die Bewegungslogik weiter. Die Bewegungslogik steuert die Achsen und ueberwacht Rueckmeldungen, Hardwarestatus und Safety-Zustaende.

```mermaid
flowchart LR
    PC["PC / HMI / TCP Client"] --> TCP["TCP Server"]
    TCP --> Router["Command Router"]
    Router --> Motion["Motion Controller"]
    Motion --> X["X-Achse"]
    Motion --> Y["Y-Achse"]
    Motion --> Z["Z-Achse"]
    X --> Drives["Drives / Motoren"]
    Y --> Drives
    Z --> Drives
    Drives --> HW["Hardware / I-O"]
    HW --> Safety["Safety / Status"]
    Safety --> Motion
```

## Hauptmodule

### TCP Server

Nimmt Kommandos von einem externen System entgegen.

Aufgaben:

- TCP-Verbindung bereitstellen
- empfangene Daten puffern
- Daten an den Command Router weitergeben
- Statusantworten senden

### Command Router

Interpretiert empfangene ASCII-Kommandos.

Aufgaben:

- Befehl erkennen
- Parameter auslesen
- Werte in Zahlen umwandeln
- passende Motion-Funktion aufrufen

### Motion Controller

Steuert den Bewegungsablauf der Achsen.

Aufgaben:

- Power on/off
- Homing
- absolute Bewegungen
- Zustandsmaschine
- Rueckmeldung an TCP Server

### Achsen

Das Projekt ist als Drei-Achsen-System gedacht:

- X-Achse: lineare Hauptachse
- Y-Achse: lineare Nebenachse
- Z-Achse: Hub-/Pick-Achse

### Drive- und Hardwaremodule

Aufgaben:

- Antriebsparameter verwalten
- Drive-Status lesen
- Positionen ausgeben
- Hardwarefehler melden
- I/O und Bus-Kommunikation bereitstellen

### Safety

Aufgaben:

- Not-Aus / Emergency ueberwachen
- Hardwarefehler auswerten
- Achslimits pruefen
- sichere Zustaende ermoeglichen

## TCP-Kommandos

Der TCP-Command-Port ist:

```text
1985
```

Unterstuetzte Kommandos:

```text
CPOWERON
CPOWEROF
CMOVEABS;XXXXXXXX;YYYYYYYY;PPPPPPPP
```

### CPOWERON

Schaltet die Achssteuerung ein.

```text
CPOWERON
```

### CPOWEROF

Schaltet die Achssteuerung aus.

```text
CPOWEROF
```

### CMOVEABS

Fuehrt eine absolute Bewegung aus.

Format:

```text
CMOVEABS;XXXXXXXX;YYYYYYYY;PPPPPPPP
```

Beispiel:

```text
CMOVEABS;00001000;00002000;00000000
```

Felder:

- `CMOVEABS`: Bewegungsbefehl
- `XXXXXXXX`: X-Position
- `YYYYYYYY`: Y-Position
- `PPPPPPPP`: Zusatzwert / Winkelwert

Die Werte sind als feste ASCII-Zahlenfelder ausgelegt.

## Beispiel: Kommando senden

Power einschalten:

```powershell
$client = [System.Net.Sockets.TcpClient]::new("10.101.10.150",1985)
$stream = $client.GetStream()
$msg = [Text.Encoding]::ASCII.GetBytes("CPOWERON")
$stream.Write($msg,0,$msg.Length)
$client.Close()
```

Absolute Bewegung senden:

```powershell
$client = [System.Net.Sockets.TcpClient]::new("10.101.10.150",1985)
$stream = $client.GetStream()
$msg = [Text.Encoding]::ASCII.GetBytes("CMOVEABS;00001000;00002000;00000000")
$stream.Write($msg,0,$msg.Length)
$client.Close()
```

## Projektstruktur

```text
LASAL.lcp
├─ HeaderFiles
├─ ClassFiles
├─ NetworkFiles
├─ DriveFiles
└─ DocuFiles
```

Wichtige Netzwerke:

```text
TcpServer
HW_Network
XAxis
EncoderSimulation
PickPlace
```

Wichtige Klassen:

```text
CommandServer
CommandRouter
MoveController
NCController
DrivePosControl
Encoders
SafetyManager
HwControl
```

## Projektmodule

```mermaid
flowchart TD
    A["Projekt"] --> B["TcpServer"]
    A --> C["HW_Network"]
    A --> D["XAxis"]
    A --> E["PickPlace"]
    A --> F["EncoderSimulation"]

    B --> B1["CommandServer"]
    B --> B2["CommandRouter"]

    C --> C1["DriveAxis 1..4"]
    C --> C2["Drive Manager"]
    C --> C3["Hardware Control"]
    C --> C4["Safety Manager"]

    D --> D1["X-Achse"]
    D --> D2["Y-Achse"]
    D --> D3["MoveController"]
    D --> D4["NCController"]

    E --> E1["Z-Achse"]
    E --> E2["DrivePosControl Z"]

    F --> F1["Encoder"]
```

## Teststrategie

Empfohlene Reihenfolge:

1. Projekt offline oeffnen.
2. Build/Check ausfuehren.
3. Fehlende Libraries oder Systemdateien klaeren.
4. TCP Server isoliert testen.
5. `CPOWERON` ohne Bewegung testen.
6. Kleine `CMOVEABS`-Werte senden.
7. Rueckmeldung und ACK pruefen.
8. Erst danach reale Achsbewegungen freigeben.

## Sicherheit

Dieses Projekt kann reale Motoren und Achsen bewegen.

Vor jedem Test:

- Maschine mechanisch sichern
- Not-Aus pruefen
- Safety aktivieren
- kleine Bewegungswerte verwenden
- Achsraum freihalten
- nur mit fachlicher Aufsicht testen

Kommandos wie:

```text
CPOWERON
CMOVEABS;...
```

koennen echte Bewegungen ausloesen.

## Hinweise

- Die Projektdatei ist fuer LASAL CLASS / CLASS 2 gedacht.
- Ohne passende Entwicklungsumgebung ist nur Quellcodeanalyse moeglich.
- Fuer echte Tests werden passende PLC-Hardware, passende Drives und korrekte Safety-Konfiguration benoetigt.
- Einige Dateien koennen ISO-8859-1 oder Windows-1252 codiert sein.

## Begleitdateien

Zusaetzlich koennen folgende Dateien fuer die Analyse genutzt werden:

```text
pc_console.html
docs/pc_console_snapshot.png
project_modules.html
lasal_blocks.html
lasal_viewer.html
LASAL_POC_Dokumentation_DE.pdf
```

## PC Textconsole / Steuerkonsole

Die Datei `pc_console.html` stellt eine PC Textconsole mit grafischer Bedienoberflaeche bereit.
Sie kann ohne Installation lokal in Chrome geoeffnet werden und arbeitet standardmaessig im
Simulationsmodus. Dadurch koennen Kommandos getestet werden, ohne sofort echte Achsen oder
Motoren anzusteuern.

![PC Textconsole Snapshot](docs/pc_console_snapshot.png)

Funktionen:

- Verbindungskonfiguration fuer PLC-IP und TCP-Port `1985`
- Safety-Freigabe und Power-On/Power-Off Bedienung
- X-/Y-/P-Positionen mit Jog-Schritten
- Vorschau des TCP-Kommandos `CMOVEABS;XXXXXXXX;YYYYYYYY;PPPPPPPP`
- Textconsole / Terminal-Log fuer simulierte TX/RX Meldungen
- PowerShell-Ausgabe fuer echte TCP-Tests ausserhalb des Browsers

Lokal starten:

```powershell
Start-Process chrome .\pc_console.html
```

Nutzung:

1. `pc_console.html` in Chrome oeffnen.
2. PLC-IP und TCP-Port pruefen. Standard ist `10.101.10.150:1985`.
3. `Simulationsmodus` aktiviert lassen, wenn nur die Textconsole getestet werden soll.
4. `Safety Freigabe` aktivieren, bevor Power- oder Bewegungsbefehle simuliert werden.
5. Mit `Power On` das Kommando `CPOWERON` vorbereiten und im Terminal-Log pruefen.
6. X-, Y- und P-Werte eintragen oder mit den Jog-Tasten veraendern.
7. Mit `Move Abs` das Kommando `CMOVEABS;XXXXXXXX;YYYYYYYY;PPPPPPPP` erzeugen.
8. Fuer echte TCP-Tests die PowerShell-Ausgabe kopieren und auf einem gesicherten PC ausfuehren.

GitHub-Test:

```powershell
node tools/test_pc_console.js
```

Auf GitHub prueft `.github/workflows/test.yml` dieselbe Kommandoformatierung automatisch.
Das Test-Badge oben in dieser README zeigt, ob dieser Test aktuell erfolgreich ist.
Wenn GitHub Pages im Repository aktiviert ist, veroeffentlicht `.github/workflows/pages.yml`
die statische Konsole als `pc_console.html`.

## Status

Dies ist ein POC-/Analyseprojekt fuer eine Drei-Achsen-Steuerung mit TCP-Anbindung.
