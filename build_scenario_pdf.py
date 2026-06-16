# -*- coding: utf-8 -*-
"""Génère le PDF du scénario de tournage de la vidéo de démonstration."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
)

VIOLET = colors.HexColor(0x460269)        # beamer_color (70,2,105)
VIOLET_LIGHT = colors.HexColor(0xEBC4F5)  # backframe_color (235,196,245)
VIOLET_MID = colors.HexColor(0x8A4FB0)
CARD_BODY = colors.HexColor(0xE9DCF0)

styles = getSampleStyleSheet()

H_TITLE = ParagraphStyle("HTitle", parent=styles["Title"], textColor=VIOLET,
                         fontSize=22, leading=26, spaceAfter=2)
H_SUB = ParagraphStyle("HSub", parent=styles["Normal"], textColor=VIOLET_MID,
                       fontSize=11, leading=14, spaceAfter=10, alignment=TA_LEFT)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=VIOLET,
                    fontSize=14, leading=17, spaceBefore=12, spaceAfter=6)
BODY = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14)
SCENE = ParagraphStyle("Scene", parent=styles["Normal"], textColor=colors.white,
                       fontName="Helvetica-Bold", fontSize=11, leading=14)
LBL = ParagraphStyle("Lbl", parent=styles["Normal"], fontSize=9.5, leading=13)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, BODY), leftIndent=10) for t in items],
        bulletType="bullet", bulletColor=VIOLET, leftIndent=12, bulletFontSize=8,
    )


def scene(num, titre, duree, ecran, action, voix, montage):
    """Une scène = bandeau violet + corps avec lignes étiquetées."""
    head = Table([[Paragraph(f"Scène {num} — {titre}", SCENE),
                   Paragraph(f'<font color="#EBC4F5">{duree}</font>', SCENE)]],
                 colWidths=[125 * mm, 40 * mm])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VIOLET),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    rows = []
    for label, txt in (("Écran", ecran), ("Action", action),
                       ("Voix off", voix), ("Montage", montage)):
        if txt:
            rows.append([Paragraph(f"<b>{label}</b>", LBL), Paragraph(txt, LBL)])
    body = Table(rows, colWidths=[22 * mm, 143 * mm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BODY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TEXTCOLOR", (0, 0), (0, -1), VIOLET),
    ]))
    return [head, body, Spacer(1, 7)]


doc = SimpleDocTemplate("scenario-tournage-demo.pdf", pagesize=A4,
                        topMargin=16 * mm, bottomMargin=14 * mm,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        title="Scénario de tournage — Démo")
story = []

story.append(Paragraph("Scénario de tournage — Vidéo de démonstration", H_TITLE))
story.append(Paragraph("Plateforme intelligente d'assistance à la gestion des incidents — "
                       "du flux d'alertes au post-mortem", H_SUB))
story.append(Table([[""]], colWidths=[165 * mm], rowHeights=[2],
                   style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), VIOLET)])))
story.append(Spacer(1, 8))

# --- Checklist ---
story.append(Paragraph("1. Avant de filmer — checklist", H1))
story.append(bullets([
    "<b>Tout est up et sain</b> : <font face='Courier'>docker ps</font> (postgres, paperclip, "
    "qdrant, qdrant-mcp, centreon-mcp, dynatrace-mcp), incident-service (:8090), frontend (:3000), "
    "Paperclip (:3100). MCP : <font face='Courier'>claude mcp list</font> &rarr; qdrant ✓.",
    "<b>Base propre</b> : aucun incident résiduel, pour que l'incident de la démo soit la vedette.",
    "<b>Agents câblés et actifs</b> : les 5 (CEO + Corrélation + RCA + Solution + Postmortem).",
    "<b>Lisibilité vidéo</b> : zoom navigateur ~125–150 %, police de terminal large, thème clair.",
    "<b>Fenêtres prêtes</b> : Centreon · frontend (dashboard) · Paperclip (runs d'agents) · terminal.",
    "<b>Répéter à blanc</b> la chorégraphie (sans déclencher les agents), puis <b>une seule prise réelle</b> "
    "(un run complet ≈ ½ session Pro : on ne gaspille pas en répétitions).",
    "<b>OBS prêt</b> (résolution, micro si voix off en direct).",
    "<b>Option timing</b> : si l'extinction live + le polling sont lents, préparer un batch d'alertes prêt à poster.",
]))

# --- Montage ---
story.append(Paragraph("2. Stratégie de montage", H1))
story.append(Paragraph(
    "Filmer <b>un run réel complet</b> (~10 min) d'un seul trait, puis couper à <b>2–3 min</b> : garder le "
    "<b>déclencheur</b> + le <b>résultat</b> de chaque étape, et <b>accélérer / couper les attentes</b> "
    "(cadence CEO 60 s, runs d'agents). Mettre un <b>carton de titre</b> à chaque étape + une horloge/⏩ "
    "sur les accélérations pour signaler que le temps est comprimé.", BODY))
story.append(Spacer(1, 6))

# --- Scénario ---
story.append(Paragraph("3. Scénario, scène par scène", H1))

for s in [
    (0, "Carton d'ouverture", "~5 s",
     "Titre : « Démonstration — du flux d'alertes au post-mortem ».", "", "", ""),
    (1, "État initial", "~10 s",
     "Dashboard calme + Centreon : l'hôte <i>ubuntu-target</i> OK (vert).", "",
     "« Au départ, le système est calme ; l'hôte est supervisé, aucun incident. »", ""),
    (2, "Injection de la panne", "~10 s",
     "Console hyperviseur / commande.",
     "Éteindre volontairement la VM.",
     "« On dégrade volontairement l'hôte en l'éteignant — Centreon va perdre toutes ses sondes. »", ""),
    (3, "Détection &amp; corrélation", "~20 s",
     "Centreon lève <b>5 alertes</b> &rarr; ingestion &rarr; run de l'agent Corrélation dans Paperclip "
     "&rarr; un incident <b>DETECTED</b> apparaît sur le dashboard.", "",
     "« Cinq alertes sont levées. L'orchestrateur détecte la charge en attente et réveille l'agent de "
     "corrélation, qui les regroupe en <b>un seul incident</b>. »", "Accéléré sur l'attente."),
    (4, "Investigation (RCA)", "~25 s",
     "Le CEO dispatche l'agent RCA &rarr; incident <b>INVESTIGATING</b> &rarr; l'<b>hypothèse</b> "
     "s'affiche (page Investigation) avec preuves et confiance.", "",
     "« L'agent identifie la <b>cause racine</b> — l'hôte est totalement injoignable — et <b>classe les "
     "trois alertes SNMP comme des symptômes en cascade</b>, pas des pannes distinctes. »",
     "Moment-clé : <b>ne pas accélérer</b>, c'est ici que le système impressionne."),
    (5, "Revue humaine", "~15 s",
     "Page Investigation.",
     "En tant que SRE, <b>valider l'hypothèse</b> &rarr; WAITING_FOR_REVIEW &rarr; VALIDATED.",
     "« Le système propose, l'humain décide : je valide la cause racine. »", ""),
    (6, "Proposition de solution", "~20 s",
     "Le CEO dispatche l'agent Solution &rarr; le <b>runbook de remédiation</b> apparaît "
     "(page Solution : étapes, références).", "",
     "« La validation déclenche l'agent de solution, qui propose un plan de remédiation actionnable — "
     "purement consultatif. »", "Accéléré sur l'attente."),
    (7, "Clôture", "~15 s",
     "Page Solution / incident.",
     "<b>Clôturer</b> en saisissant la <b>résolution réelle</b> (champ obligatoire) &rarr; CLOSED.",
     "« J'applique le correctif et je clôture en consignant la résolution réelle. »", ""),
    (8, "Post-mortem &amp; capitalisation", "~20 s",
     "Le CEO dispatche l'agent Postmortem &rarr; page Report : <b>compte rendu blameless</b>, badge "
     "« indexé dans la base de connaissances », bouton <b>Export PDF</b> (cliquer pour montrer le PDF).", "",
     "« La clôture déclenche le post-mortem : un compte rendu structuré, <b>capitalisé dans la base "
     "vectorielle</b> pour les incidents futurs, et exportable en PDF. »", "Accéléré sur l'attente."),
    (9, "Boucle de capitalisation (optionnel)", "~10 s",
     "", "",
     "« Ce post-mortem enrichit la base : lors d'un incident similaire, les agents pourront s'appuyer "
     "sur ce précédent. »", ""),
    (10, "Carton de clôture", "~5 s",
     "« Cycle complet : détection &rarr; corrélation &rarr; diagnostic &rarr; solution &rarr; clôture "
     "&rarr; post-mortem. »", "", "", ""),
]:
    for fl in scene(*s):
        story.append(fl)

# --- Astuces ---
story.append(Paragraph("4. Astuces finales", H1))
story.append(bullets([
    "<b>Sous-titrer chaque transition d'état</b> (DETECTED &rarr; … &rarr; CLOSED) en surimpression : "
    "ça relie la démo à la machine à états.",
    "<b>Plan B</b> : 3–4 captures des étapes clés, au cas où la vidéo refuse de se lancer le jour J.",
    "<b>Ne pas rejouer</b> la prise pour un détail mineur (coût) — corriger au montage (coupe, carton) "
    "plutôt qu'en refaisant tourner les agents.",
    "Tester la lecture de la vidéo <b>sur la machine de la soutenance</b> avant.",
]))

doc.build(story)
print("OK: scenario-tournage-demo.pdf")
