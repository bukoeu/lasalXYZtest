from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\tmp\LSLCL2\LASAL")
OUT = Path(r"C:\tmp\LSLCL2\LASAL_POC_Dokumentation_DE.pdf")


class BlockDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 175 * mm
        self.height = 132 * mm

    def draw_box(self, canvas, x, y, w, h, title, subtitle, fill):
        canvas.setFillColor(fill)
        canvas.setStrokeColor(colors.HexColor("#8fa1b5"))
        canvas.roundRect(x, y, w, h, 5, stroke=1, fill=1)
        canvas.setFillColor(colors.HexColor("#17202a"))
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawCentredString(x + w / 2, y + h - 12, title)
        canvas.setFillColor(colors.HexColor("#536476"))
        canvas.setFont("Helvetica", 7)
        for index, line in enumerate(subtitle.split("|")):
            canvas.drawCentredString(x + w / 2, y + h - 24 - index * 8, line)

    def arrow(self, canvas, x1, y1, x2, y2):
        canvas.setStrokeColor(colors.HexColor("#728197"))
        canvas.setLineWidth(1.4)
        canvas.line(x1, y1, x2, y2)
        dx = 4 if x2 >= x1 else -4
        canvas.line(x2, y2, x2 - dx, y2 + 3)
        canvas.line(x2, y2, x2 - dx, y2 - 3)

    def draw(self):
        c = self.canv
        blue = colors.HexColor("#dcecff")
        green = colors.HexColor("#ddf7ea")
        yellow = colors.HexColor("#fff2c7")
        red = colors.HexColor("#ffe1e1")
        violet = colors.HexColor("#eee6ff")
        cyan = colors.HexColor("#dff7fb")

        box_w = 34 * mm
        box_h = 20 * mm
        y_top = 100 * mm
        xs = [0, 45 * mm, 90 * mm, 135 * mm]

        self.draw_box(c, xs[0], y_top, box_w, box_h, "Externes System", "PC / HMI|TCP Client", blue)
        self.draw_box(c, xs[1], y_top, box_w, box_h, "TCP Server", "Port 1985|ASCII Daten", blue)
        self.draw_box(c, xs[2], y_top, box_w, box_h, "CommandRouter", "CPOWERON|CMOVEABS", blue)
        self.draw_box(c, xs[3], y_top, box_w, box_h, "MoveController", "State Machine|Motion", green)

        for i in range(3):
            self.arrow(c, xs[i] + box_w, y_top + box_h / 2, xs[i + 1], y_top + box_h / 2)

        y_mid = 58 * mm
        self.draw_box(c, xs[1], y_mid, box_w, box_h, "Encoder", "Rueckmeldung|Istposition", cyan)
        self.draw_box(c, xs[2], y_mid, box_w, box_h, "Achsen X/Y/Z", "Homing|MoveAbsolute", green)
        self.draw_box(c, xs[3], y_mid, box_w, box_h, "SafetyManager", "Limits|Not-Aus", yellow)

        self.arrow(c, xs[3] + box_w / 2, y_top, xs[2] + box_w / 2, y_mid + box_h)
        self.arrow(c, xs[2], y_mid + box_h / 2, xs[1] + box_w, y_mid + box_h / 2)
        self.arrow(c, xs[1] + box_w, y_mid + 4, xs[2], y_mid + 4)
        self.arrow(c, xs[2] + box_w, y_mid + box_h / 2, xs[3], y_mid + box_h / 2)

        y_bot = 18 * mm
        self.draw_box(c, xs[1], y_bot, box_w, box_h, "DrivePosControl", "Positionsregler", green)
        self.draw_box(c, xs[2], y_bot, box_w, box_h, "Drive Axis", "Antriebsobjekt", red)
        self.draw_box(c, xs[3], y_bot, box_w, box_h, "VARAN / SDIAS", "SIGMATEK Bus|I/O / Drives", violet)

        self.arrow(c, xs[2] + box_w / 2, y_mid, xs[1] + box_w / 2, y_bot + box_h)
        self.arrow(c, xs[1] + box_w, y_bot + box_h / 2, xs[2], y_bot + box_h / 2)
        self.arrow(c, xs[2] + box_w, y_bot + box_h / 2, xs[3], y_bot + box_h / 2)


class ProjectStructureDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 175 * mm
        self.height = 160 * mm

    def draw_box(self, canvas, x, y, w, h, title, subtitle, fill):
        canvas.setFillColor(fill)
        canvas.setStrokeColor(colors.HexColor("#8fa1b5"))
        canvas.roundRect(x, y, w, h, 5, stroke=1, fill=1)
        canvas.setFillColor(colors.HexColor("#17202a"))
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawCentredString(x + w / 2, y + h - 11, title)
        canvas.setFillColor(colors.HexColor("#536476"))
        canvas.setFont("Helvetica", 6.6)
        for index, line in enumerate(subtitle.split("|")):
            canvas.drawCentredString(x + w / 2, y + h - 21 - index * 7.4, line)

    def arrow(self, canvas, x1, y1, x2, y2):
        canvas.setStrokeColor(colors.HexColor("#728197"))
        canvas.setLineWidth(1.1)
        canvas.line(x1, y1, x2, y2)
        dx = 3.5 if x2 >= x1 else -3.5
        canvas.line(x2, y2, x2 - dx, y2 + 2.5)
        canvas.line(x2, y2, x2 - dx, y2 - 2.5)

    def draw(self):
        c = self.canv
        root = colors.HexColor("#dcecff")
        headers = colors.HexColor("#eef2f7")
        classes = colors.HexColor("#e3f7e9")
        net = colors.HexColor("#fff2c7")
        drive = colors.HexColor("#ffe3e3")
        obj = colors.HexColor("#eee6ff")
        doc = colors.HexColor("#e0f7fb")
        white = colors.white

        c.setFillColor(colors.HexColor("#536476"))
        c.setFont("Helvetica-Bold", 7.4)
        c.drawString(0, 151 * mm, "Hauptprojekt")
        c.drawString(47 * mm, 151 * mm, "LCP-Bereiche")
        c.drawString(93 * mm, 151 * mm, "NetworkFiles")
        c.drawString(136 * mm, 151 * mm, "Objekte")

        self.draw_box(c, 0, 128 * mm, 36 * mm, 18 * mm, "LASAL.lcp", "Project Version 13|CompilerVersion 56", root)

        section_x = 47 * mm
        sections = [
            ("HeaderFiles", "80 Eintraege|Include / Interfaces", headers, 128),
            ("ClassFiles", "112 Eintraege|ST / C++ Klassen", classes, 106),
            ("NetworkFiles", "5 Netzwerke|Objekt-Instanzen", net, 84),
            ("ObjectFiles", "Loader.lob|downloadable=false", obj, 62),
            ("DriveFiles", "5 Drive-Dateien|_DriveAxis1..4", drive, 40),
            ("DocuFiles", "2 VOV-Dateien|ST151 / _LMCAxis", doc, 18),
        ]
        for title, subtitle, fill, y_mm in sections:
            self.draw_box(c, section_x, y_mm * mm, 36 * mm, 16 * mm, title, subtitle, fill)
            self.arrow(c, 36 * mm, 137 * mm, section_x, (y_mm + 8) * mm)

        network_x = 93 * mm
        networks = [
            ("TcpServer", "commandServer|commandRouter", 126),
            ("HW_Network", "Drives / I-O|Safety / VARAN", 101),
            ("XAxis", "X/Y Achsen|MoveController", 76),
            ("EncoderSimulation", "Encoders1|Rueckmeldung", 51),
            ("PickPlace", "Z-Achse|DrivePosControl3", 26),
        ]
        for title, subtitle, y_mm in networks:
            self.draw_box(c, network_x, y_mm * mm, 38 * mm, 17 * mm, title, subtitle, net)
            self.arrow(c, section_x + 36 * mm, 92 * mm, network_x, (y_mm + 8.5) * mm)

        obj_x = 136 * mm
        objects = [
            ("Command", "CommandServer|CommandRouter", 126, colors.HexColor("#e5f0ff")),
            ("Hardware", "_DriveAxis1..4|HwControl / Safety", 101, obj),
            ("Motion X/Y", "_LMCAxis X/Y|NCController", 76, classes),
            ("Encoder", "Encoders1", 51, white),
            ("Motion Z", "_ZAxis|RefSwitchCurrent3", 26, classes),
        ]
        for title, subtitle, y_mm, fill in objects:
            self.draw_box(c, obj_x, y_mm * mm, 38 * mm, 17 * mm, title, subtitle, fill)
            self.arrow(c, network_x + 38 * mm, (y_mm + 8.5) * mm, obj_x, (y_mm + 8.5) * mm)


def p(text, style):
    return Paragraph(text, style)


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="LASAL POC Dokumentation",
        author="Codex",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=20, leading=24))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10, textColor=colors.HexColor("#536476")))
    styles.add(ParagraphStyle(name="CodeBlock", parent=styles["Code"], fontSize=8, leading=10, backColor=colors.HexColor("#f1f4f8")))

    story = []
    story.append(p("LASAL-Projekt POC Dokumentation", styles["TitleCenter"]))
    story.append(Spacer(1, 5 * mm))
    story.append(p("Projekt: C:\\tmp\\LSLCL2\\LASAL", styles["Small"]))
    story.append(p("Stand: 17.07.2026", styles["Small"]))
    story.append(Spacer(1, 8 * mm))

    story.append(p("1. Kurzfazit", styles["Heading1"]))
    story.append(p(
        "Das Projekt ist ein SIGMATEK LASAL CLASS/CLASS 2 PLC-Projekt fuer eine "
        "Bewegungs- bzw. Pick-and-Place-Maschine. Die Software nimmt ASCII-Kommandos "
        "ueber TCP entgegen, routet diese an eine Bewegungssteuerung und steuert "
        "Achsen, Antriebe, Encoder-Rueckmeldung, Safety und VARAN/SDIAS-Hardware.",
        styles["BodyText"],
    ))
    story.append(Spacer(1, 5 * mm))

    data = [
        ["Eigenschaft", "Wert"],
        ["Projektdatei", "LASAL.lcp"],
        ["Projektformat", "Project Version 13, CompilerVersion 56"],
        ["TCP Command-Port", "1985"],
        ["LASAL Online-Verbindung", "10.101.10.150:1954"],
        ["Command-Netzwerk", "Network\\TcpServer\\TcpServer.lcn"],
        ["Aktiver Command-Pfad", "CommandServer -> CommandRouter -> MoveController"],
    ]
    table = Table(data, colWidths=[50 * mm, 110 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dcecff")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c5d5")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    story.append(PageBreak())
    story.append(p("2. Projektmodul-Struktur", styles["Heading1"]))
    story.append(p(
        "Diese Sicht entspricht der Hauptstruktur aus `LASAL.lcp`: zuerst die "
        "Projektbereiche, dann die fuenf echten NetworkFiles und rechts die wichtigsten "
        "Objektinstanzen aus den `.lcn`-Netzwerken.",
        styles["BodyText"],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(ProjectStructureDiagram())
    story.append(Spacer(1, 4 * mm))
    story.append(p(
        "Wichtig: Dies ist die Projektstruktur wie in LASAL CLASS 2, nicht nur ein "
        "Funktionsablauf der Maschine.",
        styles["Small"],
    ))

    story.append(PageBreak())
    story.append(p("3. Grafische Funktionsarchitektur", styles["Heading1"]))
    story.append(BlockDiagram())
    story.append(Spacer(1, 4 * mm))
    story.append(p(
        "Die Darstellung ist eine POC-Sicht aus dem Quellcode. Sie ersetzt keine "
        "validierte Maschinen- oder Safety-Dokumentation.",
        styles["Small"],
    ))

    story.append(PageBreak())
    story.append(p("4. TCP-Kommandos", styles["Heading1"]))
    story.append(p(
        "Der CommandServer ist als TCP-Server konfiguriert. Empfangen werden einfache "
        "ASCII-Zeichenketten. Der Code ruft bei Empfang CommandRouter.SetData() auf.",
        styles["BodyText"],
    ))
    cmd_data = [
        ["Befehl", "Bedeutung", "Status"],
        ["CPOWERON", "Achsantriebe einschalten / Power on", "im Code erkannt"],
        ["CPOWEROF", "Achsantriebe ausschalten / Power off", "im Code erkannt"],
        ["CMOVEABS;XXXXXXXX;YYYYYYYY;PPPPPPPP", "Absolute X/Y-Bewegung; Phi wird gelesen, aber im MoveAxis-Aufruf nicht genutzt", "im Code erkannt"],
    ]
    cmd_table = Table(cmd_data, colWidths=[54 * mm, 82 * mm, 28 * mm])
    cmd_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ddf7ea")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c5d5")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(cmd_table)
    story.append(Spacer(1, 4 * mm))
    story.append(p("Beispiel-Kommandos:", styles["Heading2"]))
    story.append(p("CPOWERON", styles["CodeBlock"]))
    story.append(p("CMOVEABS;00001000;00002000;00000000", styles["CodeBlock"]))
    story.append(p("CPOWEROF", styles["CodeBlock"]))
    story.append(Spacer(1, 3 * mm))
    story.append(p(
        "Antwort: Der Code sendet ACK ueber CommandServer.SendStatus(), wenn ein "
        "Status fertig/ok gemeldet wird.",
        styles["BodyText"],
    ))

    story.append(PageBreak())
    story.append(p("5. POC-Test mit PowerShell", styles["Heading1"]))
    story.append(p(
        "Nur verwenden, wenn eine sichere Testumgebung vorhanden ist und die reale "
        "Maschine freigegeben wurde. Bewegungswerte koennen Achsen ausloesen.",
        styles["BodyText"],
    ))
    story.append(p(
        "$client = [System.Net.Sockets.TcpClient]::new(\"10.101.10.150\",1985)<br/>"
        "$stream = $client.GetStream()<br/>"
        "$msg = [Text.Encoding]::ASCII.GetBytes(\"CPOWERON\")<br/>"
        "$stream.Write($msg,0,$msg.Length)<br/>"
        "$client.Close()",
        styles["CodeBlock"],
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(p("6. Risiken / offene Punkte", styles["Heading1"]))
    risks = [
        "Ohne LASAL CLASS 2 kann das Projekt nicht kompiliert oder auf einer PLC simuliert werden.",
        "Fehlende System-/Loader-Dateien koennen aus der LASAL-Installation kommen.",
        "Die Werte fuer X/Y/Phi sind feste 8-Zeichen-Felder; reale Einheiten muessen an der Maschine geprueft werden.",
        "Z wird im aktiven CMOVEABS-Pfad nicht direkt aus dem TCP-Kommando gesetzt.",
        "Safety- und Motion-Funktionen duerfen nur durch Fachpersonal getestet werden.",
    ]
    for item in risks:
        story.append(p("- " + item, styles["BodyText"]))

    story.append(Spacer(1, 5 * mm))
    story.append(p("7. Wichtige Dateien", styles["Heading1"]))
    files = [
        "LASAL.lcp",
        "Network\\TcpServer\\TcpServer.lcn",
        "Class\\CommandServer\\CommandServer.st",
        "Class\\CommandRouter\\CommandRouter.st",
        "Class\\MoveController\\MoveController.st",
        "Class\\_TCPIP_SERVER\\_TCPIP_SERVER.st",
        "Network\\PickPlace\\PickPlace.lcn",
        "Network\\XAxis\\XAxis.lcn",
    ]
    for file in files:
        story.append(p("- " + file, styles["BodyText"]))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(str(OUT))
