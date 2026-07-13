#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Chartruler-Reader aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine (Placidus), nur das Reading-Gehirn wird getauscht:
Der Reader liest den Aszendenten, bestimmt daraus den Chartruler (Horoskopherrscher),
zeigt eine ausführliche Erklärung, ein automatisches Minireading (Planet + Zeichen +
Haus + goldene Chartruler-Frage) und baut einen fertigen KI-Prompt zum Kopieren.

Quelle:  astro-business-reader.html
Ziel:    astro-chartruler-reader.html (+ astro-chartruler-reader-netlify/index.html)
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.
"""
import re, os, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-chartruler-reader.html")
NETLIFY_DIR = os.path.join(HERE, "astro-chartruler-reader-netlify")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

SIGNS = ["Widder","Stier","Zwillinge","Krebs","Löwe","Jungfrau",
         "Waage","Skorpion","Schütze","Steinbock","Wassermann","Fische"]
PLANETS = ["Sonne","Mond","Merkur","Venus","Mars","Jupiter","Saturn","Uranus","Neptun","Pluto"]

# ============================================================================
# TEXTE (alle Anti-KI-geprüft: keine Gedankenstriche, kein "nicht... sondern",
# kein Kontrast-Muster, keine leeren Verstärker, konkret, Du-Form)
# ============================================================================

EXPLAIN = [
    "Dein Aszendent ist das Tierkreiszeichen, das im Moment deiner Geburt am östlichen Horizont aufgestiegen ist. Er ist die Tür in deine Chart: dein Auftreten, deine Ausstrahlung, die Art, wie du in jede Situation hineingehst.",
    "Jedes Tierkreiszeichen hat einen Planeten, der es regiert. Der Planet, der dein Aszendenten-Zeichen regiert, ist dein Chartruler, auf Deutsch: dein Horoskopherrscher. Steigt zum Beispiel die Waage auf, führt Venus deine Chart. Steigt der Widder auf, führt Mars.",
    "Damit wird dieser eine Planet zum wichtigsten Planeten deiner gesamten Chart. Er ist der Kapitän. Sein Zeichen zeigt, in welchem Stil und in welchem Tempo du dein Leben führst. Sein Haus zeigt, in welchem Lebensbereich sich dein Leben immer wieder entscheidet. Seine Aspekte zeigen, welche inneren Kräfte bei jeder deiner Entscheidungen mit am Tisch sitzen.",
    "Deshalb reicht es nicht, deinen Aszendenten zu kennen. Zwei Frauen mit Waage-Aszendent leben zwei verschiedene Leben, wenn die Venus der einen im 10. Haus im Steinbock steht und die Venus der anderen im 4. Haus im Krebs. Dein Chartruler macht deine Chart persönlich.",
]

AC_INTRO = {
    "Widder": "Bei deiner Geburt stieg der Widder am Horizont auf. Du gehst direkt und ohne Umweg in jede Situation, und der Planet, der diese Tür steuert, ist Mars.",
    "Stier": "Bei deiner Geburt stieg der Stier am Horizont auf. Du wirkst ruhig, verlässlich und sinnlich, und die Kraft hinter dieser Tür ist Venus.",
    "Zwillinge": "Bei deiner Geburt stiegen die Zwillinge am Horizont auf. Du öffnest Räume über Worte und Neugier, und der Planet hinter dieser Tür ist Merkur.",
    "Krebs": "Bei deiner Geburt stieg der Krebs am Horizont auf. Menschen fühlen sich in deiner Nähe schnell sicher, und die Kraft hinter dieser Tür ist der Mond.",
    "Löwe": "Bei deiner Geburt stieg der Löwe am Horizont auf. Du betrittst Räume mit Wärme und Präsenz, und die Kraft hinter dieser Tür ist die Sonne.",
    "Jungfrau": "Bei deiner Geburt stieg die Jungfrau am Horizont auf. Du wirkst klar, aufmerksam und präzise, und der Planet hinter dieser Tür ist Merkur.",
    "Waage": "Bei deiner Geburt stieg die Waage am Horizont auf. Du gewinnst Menschen über Charme und Ausgleich, und die Kraft hinter dieser Tür ist Venus.",
    "Skorpion": "Bei deiner Geburt stieg der Skorpion am Horizont auf. Deine Präsenz hat Tiefe, Menschen spüren dich, bevor du sprichst. Die Kraft hinter dieser Tür ist Pluto. In der klassischen Astrologie regiert zusätzlich Mars mit, schau dir beide an, der Fokus liegt auf Pluto.",
    "Schütze": "Bei deiner Geburt stieg der Schütze am Horizont auf. Du bringst Weite und Zuversicht in jeden Raum, und die Kraft hinter dieser Tür ist Jupiter.",
    "Steinbock": "Bei deiner Geburt stieg der Steinbock am Horizont auf. Du wirkst gesammelt und verlässlich, Menschen nehmen dich ernst. Die Kraft hinter dieser Tür ist Saturn.",
    "Wassermann": "Bei deiner Geburt stieg der Wassermann am Horizont auf. Du fällst auf, weil du anders denkst und anders lebst. Die Kraft hinter dieser Tür ist Uranus. In der klassischen Astrologie regiert zusätzlich Saturn mit, schau dir beide an, der Fokus liegt auf Uranus.",
    "Fische": "Bei deiner Geburt stiegen die Fische am Horizont auf. Du wirkst weich, offen und nahbar, Menschen erzählen dir Dinge, die sie sonst niemandem erzählen. Die Kraft hinter dieser Tür ist Neptun. In der klassischen Astrologie regiert zusätzlich Jupiter mit, schau dir beide an, der Fokus liegt auf Neptun.",
}

PLANET_TXT = {
    "Sonne": "Deine Chart wird von der Sonne geführt. Damit ist dein Lebensauftrag Sichtbarkeit: du bist gebaut, um zu strahlen, zu gestalten und aus deinem eigenen Zentrum heraus zu leben. Du kannst dich nicht lange hinter anderen verstecken, dein System ruft nach Ausdruck. Entscheidungen gelingen dir, wenn sie aus deinem Kern kommen, und sie scheitern, wenn du sie triffst, um zu gefallen. Deine Aufgabe ist Selbstführung: du bist die Quelle deines Lebens. Wo deine Sonne steht, dort will dein Leben hin.",
    "Mond": "Deine Chart wird vom Mond geführt. Dein Leben steuert über dein Gefühl: dein Körper weiß vor deinem Kopf, was stimmt. Du brauchst Nähe, Rhythmus und Orte, an denen du dich sicher fühlst, sonst trägt dich nichts, was du aufbaust. Deine Stimmungen zeigen dir die Richtung an, lange bevor dein Kopf sie begründen kann. Du lebst in Zyklen: es gibt Tage zum Säen und Tage zum Zurückziehen, und du führst am klarsten, wenn du beide ernst nimmst. Wo dein Mond steht, dort füllt sich dein Leben oder es leert sich.",
    "Merkur": "Deine Chart wird von Merkur geführt. Dein Leben läuft über Sprache, Denken und Verbindung: du verarbeitest die Welt, indem du sie benennst. Gespräche, Schreiben, Lernen und Austausch sind für dich Lebensenergie, du merkst sofort, wenn dein Kopf nichts zu kauen hat. Deine Wirkung entsteht über deine Worte, du öffnest Menschen mit einer Frage schneller als andere mit einer Stunde Smalltalk. Deine Aufgabe ist es, deinem Denken eine Richtung zu geben, sonst zerstreut es sich in tausend offene Tabs. Wo dein Merkur steht, dort will dein Verstand arbeiten und dein Wort wirken.",
    "Venus": "Deine Chart wird von Venus geführt. Dein Leben steuert über Anziehung: du erreichst mit Ausstrahlung, Geschmack und Beziehung, wofür andere kämpfen. Schönheit, Genuss und Verbindung sind bei dir Lebensgrundlage, du spürst sofort, wenn ein Raum, ein Mensch oder ein Angebot nicht stimmig ist. Du bist gebaut, um zu empfangen und Werte aufzubauen: Geld, Beziehungen und Selbstwert hängen in deiner Chart an einem Faden. Deine Aufgabe ist es, dich selbst als den ersten Wert zu behandeln, den du pflegst. Wo deine Venus steht, dort entscheidet sich, was und wen du in dein Leben ziehst.",
    "Mars": "Deine Chart wird von Mars geführt. Dein Leben steuert über Handlung: du bist gebaut, um zu beginnen, zu entscheiden und dir zu nehmen, was du willst. Warten macht dich krank, du brauchst Bewegung, Richtung und ein Ziel, auf das du zugehen kannst. Deine Energie will kämpfen dürfen, im guten Sinn: für eine Sache, für Menschen, für dich. Unterdrückst du diesen Antrieb, wird er zu Gereiztheit und richtet sich nach innen. Wo dein Mars steht, dort will dein Feuer arbeiten.",
    "Jupiter": "Deine Chart wird von Jupiter geführt. Dein Leben steuert über Wachstum und Sinn: du brauchst einen Horizont, der größer ist als dein Alltag. Du bist gebaut, um zu expandieren, zu lehren, zu inspirieren und Räume zu öffnen, in denen andere größer denken. Enge, Kleinlichkeit und Routinen ohne Bedeutung machen dich müde. Dein Vertrauen ins Leben ist dein Kapital, es zieht Gelegenheiten an, an die andere gar nicht erst glauben. Deine Aufgabe ist es, deiner Fülle eine Form zu geben, sonst bleibt sie ein schönes Versprechen. Wo dein Jupiter steht, dort wächst dein Leben.",
    "Saturn": "Deine Chart wird von Saturn geführt. Dein Leben steuert über Verantwortung: du bist gebaut, um etwas aufzubauen, das trägt und bleibt. Du nimmst das Leben ernst, oft schon als Kind, und du spürst früh, dass dir nichts geschenkt wird. Das macht dich am Anfang langsamer als andere und auf der langen Strecke stärker als die meisten. Deine Reife ist deine Autorität: Menschen vertrauen dir, weil du hältst, was du sagst. Deine Aufgabe ist es, Strenge in Struktur zu verwandeln und dich selbst freundlicher zu behandeln, als dein innerer Richter es vorschlägt. Wo dein Saturn steht, dort wartet deine Meisterschaft.",
    "Uranus": "Deine Chart wird von Uranus geführt. Dein Leben steuert über Freiheit: du bist gebaut, um auszubrechen, neu zu denken und Systeme zu hinterfragen, in denen alle anderen funktionieren. Du spürst früher als andere, wenn etwas vorbei ist, und dein Leben verläuft in Sprüngen statt in geraden Linien. Anpassung kostet dich Lebensenergie, du zahlst an jedem Tag, an dem du dich kleiner machst, um dazuzugehören. Deine Andersartigkeit hat eine Funktion: du bist da, um zu erneuern. Wo dein Uranus steht, dort bricht dein Leben auf.",
    "Neptun": "Deine Chart wird von Neptun geführt. Dein Leben steuert über Feinfühligkeit: du nimmst Stimmungen, Bilder und Zwischentöne auf, die an anderen vorbeiziehen. Du brauchst einen Zugang zu etwas Größerem, ob über Kreativität, Spiritualität oder Heilung, sonst fühlt sich dein Alltag an wie ein zu enger Schuh. Deine Durchlässigkeit hat zwei Seiten: sie macht dich zur Künstlerin und Heilerin, und sie macht dich anfällig für Flucht, Nebel und Selbstaufgabe. Deine Aufgabe ist Erdung: je klarer deine Grenzen, desto kraftvoller dein Kanal. Wo dein Neptun steht, dort sucht dein Leben nach Hingabe.",
    "Pluto": "Deine Chart wird von Pluto geführt. Dein Leben steuert über Tiefe und Wandlung: du lebst in Zyklen von Stirb und Werde, und du weißt das seit deiner Kindheit. Halbe Sachen, oberflächliche Gespräche und Kontrolle von außen sind für dich unerträglich. Du hast eine Kraft in dir, die Menschen entweder magnetisch anzieht oder ihnen Angst macht, oft beides gleichzeitig. Aus jeder Krise baust du dich größer wieder auf, Wandlung ist dein Rohstoff. Deine Aufgabe ist es, deine Intensität bewusst zu führen, damit sie erschafft und heilt. Wo dein Pluto steht, dort verwandelt sich dein Leben.",
}

SIGN_TXT = {
    "Widder": "Die Kraft, die dein Leben führt, arbeitet schnell, direkt und aus dem Impuls. Du entscheidest im Moment und korrigierst unterwegs, langes Abwägen erstickt deine Energie. Dein Lebensmotor springt an, wenn du beginnen darfst.",
    "Stier": "Die Kraft, die dein Leben führt, arbeitet langsam, sinnlich und beständig. Du baust in deinem eigenen Tempo auf und lässt dich von niemandem hetzen, dafür bleibt, was du erschaffst. Dein Lebensmotor läuft über Sicherheit, Genuss und Dinge, die du anfassen kannst.",
    "Zwillinge": "Die Kraft, die dein Leben führt, arbeitet neugierig, wendig und über Verbindung. Du brauchst Austausch, neue Eindrücke und mehrere Projekte gleichzeitig, Eintönigkeit legt dein System lahm. Dein Lebensmotor läuft über Worte und Begegnungen.",
    "Krebs": "Die Kraft, die dein Leben führt, arbeitet über Gefühl, Nähe und Zugehörigkeit. Du entscheidest aus dem Bauch und brauchst emotionale Sicherheit, bevor du dich zeigst. Dein Lebensmotor läuft über Verbundenheit: Menschen, Orte und Räume, in denen du zu Hause bist.",
    "Löwe": "Die Kraft, die dein Leben führt, arbeitet warm, kraftvoll und mit dem Wunsch zu strahlen. Du willst gestalten, gesehen werden und deinem Leben deine Handschrift geben. Dein Lebensmotor läuft über Ausdruck und Herz.",
    "Jungfrau": "Die Kraft, die dein Leben führt, arbeitet genau, aufmerksam und im Dienst einer Sache. Du siehst Details, die andere übersehen, und verbesserst, wo du hinkommst. Dein Lebensmotor läuft über sinnvolle Arbeit und einen klaren Alltag.",
    "Waage": "Die Kraft, die dein Leben führt, arbeitet über Beziehung, Ausgleich und Ästhetik. Du wägst ab, verbindest Menschen und erschaffst Harmonie, wo vorher Reibung war. Dein Lebensmotor läuft über Begegnung auf Augenhöhe.",
    "Skorpion": "Die Kraft, die dein Leben führt, arbeitet tief, leidenschaftlich und unter der Oberfläche. Du gehst dorthin, wo andere wegsehen, und verwandelst, was du berührst. Dein Lebensmotor läuft über Intensität und Wahrheit.",
    "Schütze": "Die Kraft, die dein Leben führt, arbeitet weit, optimistisch und auf ein Ziel am Horizont gerichtet. Du brauchst Sinn, Bewegung und die Freiheit, über den eigenen Tellerrand zu gehen. Dein Lebensmotor läuft über Vision und Vertrauen.",
    "Steinbock": "Die Kraft, die dein Leben führt, arbeitet diszipliniert, geduldig und auf ein Lebenswerk hin. Du denkst in Jahren und baust Stufe für Stufe auf, was am Ende trägt. Dein Lebensmotor läuft über Verantwortung und Ergebnisse.",
    "Wassermann": "Die Kraft, die dein Leben führt, arbeitet frei, eigenständig und dem eigenen Kopf folgend. Du gehst Wege, die es noch nicht gibt, und brauchst Raum für deine Ideen. Dein Lebensmotor läuft über Unabhängigkeit und Zukunft.",
    "Fische": "Die Kraft, die dein Leben führt, arbeitet fein, intuitiv und mit offenen Kanälen. Du spürst Strömungen, bevor sie sichtbar werden, und dein Weg entsteht oft erst im Gehen. Dein Lebensmotor läuft über Hingabe, Fantasie und Verbundenheit mit etwas Größerem.",
}

HOUSE_TXT = {
    "1": "Dein Chartruler steht im 1. Haus, direkt an der Tür deiner Chart. Dein Leben entscheidet sich über dich selbst: dein Auftreten, deinen Körper, deinen Mut, sichtbar du zu sein. Dein Platz ist vorn, dein Thema ist Selbstbehauptung. Alles beginnt damit, dass du dich zeigst.",
    "2": "Dein Chartruler steht im 2. Haus. Dein Leben entscheidet sich über Werte: Geld, Besitz, Sicherheit und die Frage, was du dir selbst wert bist. Du bist hier, um dein eigenes Fundament zu bauen und von dem zu leben, was du kannst. Dein Selbstwert und dein Kontostand erzählen dieselbe Geschichte.",
    "3": "Dein Chartruler steht im 3. Haus. Dein Leben entscheidet sich über Kommunikation: Worte, Wissen, Austausch und dein direktes Umfeld. Du bist hier, um zu sprechen, zu schreiben, zu lernen und Menschen zu verbinden. Deine Stimme ist dein Werkzeug.",
    "4": "Dein Chartruler steht im 4. Haus. Dein Leben entscheidet sich über deine Wurzeln: Familie, Zuhause, Herkunft und deinen inneren Boden. Du bist hier, um Heimat zu schaffen, zuerst in dir, dann um dich herum. Deine Kraft wächst aus der Tiefe, aus der du kommst.",
    "5": "Dein Chartruler steht im 5. Haus. Dein Leben entscheidet sich über Ausdruck: Kreativität, Sichtbarkeit, Freude, Herzensprojekte, auch Kinder. Du bist hier, um zu erschaffen, was es ohne dich nicht gäbe. Dein Leben will gespielt werden, mit vollem Einsatz.",
    "6": "Dein Chartruler steht im 6. Haus. Dein Leben entscheidet sich über den Alltag: Arbeit, Routinen, Gesundheit und deinen Körper. Du bist hier, um Dienst und Selbstfürsorge in eine Ordnung zu bringen, die dich trägt. Wie dein Dienstag aussieht, entscheidet, wie dein Leben aussieht.",
    "7": "Dein Chartruler steht im 7. Haus. Dein Leben entscheidet sich über Begegnung: Partnerschaft, enge Verbindungen, dein Gegenüber. Menschen sind deine Spiegel, an ihnen erkennst du dich. Du bist hier, um Beziehung auf Augenhöhe zu lernen, ohne dich selbst darin zu verlieren.",
    "8": "Dein Chartruler steht im 8. Haus. Dein Leben entscheidet sich in der Tiefe: Wandlung, Intimität, Macht, geteilte Ressourcen und die großen Übergänge. Du bist hier, um durch Krisen hindurch zu wachsen und andere durch ihre zu führen. Oberflächlich wird dein Leben nie sein.",
    "9": "Dein Chartruler steht im 9. Haus. Dein Leben entscheidet sich über den Horizont: Reisen, Weisheit, Lehren und deine eigene Wahrheit. Du bist hier, um Erfahrungen zu sammeln, die dein Weltbild sprengen, und daraus deine eigene Philosophie zu bauen. Dein Leben braucht ein Wohin.",
    "10": "Dein Chartruler steht im 10. Haus, am höchsten Punkt deiner Chart. Dein Leben entscheidet sich über Berufung: deinen Platz in der Welt, deine Aufgabe, deinen Ruf. Du bist hier, um öffentlich Verantwortung zu tragen und mit deinem Werk gesehen zu werden. Dein Weg führt nach oben, ob du willst oder nicht.",
    "11": "Dein Chartruler steht im 11. Haus. Dein Leben entscheidet sich über Gemeinschaft: Netzwerke, Freundschaften und Visionen, die größer sind als du allein. Du bist hier, um Menschen um eine Idee zu versammeln und an einer Zukunft zu bauen, die es noch nicht gibt. Deine Wirkung entsteht im Wir.",
    "12": "Dein Chartruler steht im 12. Haus. Dein Leben entscheidet sich im Verborgenen: Rückzug, Spiritualität, das Unbewusste und die Räume hinter den Kulissen. Du bist hier, um loszulassen, zu heilen und aus der Stille Kraft zu ziehen. Vieles in deinem Leben wirkt, ohne dass es eine Bühne braucht.",
}

QUESTION_TXT = {
    "1": "Wo wartest du auf Erlaubnis, obwohl du längst dran bist, dich zu zeigen?",
    "2": "Was würdest du verlangen, wenn du deinen Wert nie wieder verhandeln müsstest?",
    "3": "Welchen Satz trägst du seit Wochen in dir, den dein Umfeld längst hören müsste?",
    "4": "An welchem Ort und mit welchen Menschen hörst du auf zu funktionieren und fängst an zu leben?",
    "5": "Welches Herzensprojekt schiebst du auf, weil du dich mit ihm zeigen müsstest?",
    "6": "Welche Routine in deinem Alltag kostet dich jeden Tag Energie, und warum hältst du an ihr fest?",
    "7": "Was zeigt dir der Mensch, an dem du dich gerade reibst, über dich selbst?",
    "8": "Welche Wandlung schiebst du auf, weil du weißt, dass danach nichts mehr ist wie vorher?",
    "9": "Für welche Wahrheit würdest du losgehen, wenn du keine Angst hättest anzuecken?",
    "10": "Welchen Platz nimmst du nicht ein, obwohl er längst für dich reserviert ist?",
    "11": "Welche Vision sprichst du nicht aus, weil dein Umfeld sie noch nicht versteht?",
    "12": "Was lebt in dir, das noch nie jemand gesehen hat, und wie lange soll es dort noch warten?",
}

OWN_SIGN_TXT = "{P} steht in seinem eigenen Zeichen, im Zeichen {S}. Dein Chartruler arbeitet damit in voller Kraft: die Energie, die dein Leben führt, muss sich nicht verbiegen, sie wirkt so, wie sie gemeint ist."

# --- Vollständigkeit prüfen, bevor irgendwas gebaut wird -------------------
for sign in SIGNS:
    assert sign in AC_INTRO, "AC_INTRO fehlt: " + sign
    assert sign in SIGN_TXT, "SIGN_TXT fehlt: " + sign
for p in PLANETS:
    assert p in PLANET_TXT, "PLANET_TXT fehlt: " + p
for h in range(1, 13):
    assert str(h) in HOUSE_TXT, "HOUSE_TXT fehlt: " + str(h)
    assert str(h) in QUESTION_TXT, "QUESTION_TXT fehlt: " + str(h)

TEXTS_JSON = json.dumps({
    "explain": EXPLAIN,
    "acIntro": AC_INTRO,
    "planet": PLANET_TXT,
    "sign": SIGN_TXT,
    "house": HOUSE_TXT,
    "question": QUESTION_TXT,
    "ownSign": OWN_SIGN_TXT,
}, ensure_ascii=False)

# ============================================================================
# 1. Branding / sichtbare Texte
# ============================================================================
repl("<title>Dein Business-Code</title>",
     "<title>Dein Chartruler · Der Herrscher deiner Chart</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<p class="header-eyebrow">Der Herrscher deiner Chart</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>", "<h1>Dein Chartruler</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Ein einziger Planet führt deine gesamte Chart. Finde heraus, wer dein Chartruler ist und was das für dein Leben bedeutet.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Chartruler aufdecken</button>', "submit-btn")

# ============================================================================
# 2. E-Mail komplett entfernen (kein Opt-in, wie Chiron-Reader)
# ============================================================================
repl('''    <div class="name-group">
      <label class="field-label" for="userEmail">Deine E-Mail</label>
      <input type="email" id="userEmail" placeholder="Wohin schicken wir deinen Business-Code?" autocomplete="email" inputmode="email">
    </div>

''', '', "email-field-remove")

repl("    const email = ($('userEmail').value || '').trim();", "    const email = '';", "email-var")

repl('''    const emailOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
    if(!emailOk){ return fail('Bitte gib eine gültige E-Mail-Adresse ein. Dorthin kommt dein Business-Code.'); }
''', '', "email-validation")

repl("      subscribeLead(name, email);\n", "", "subscribe-call")

repl('''  // Trägt die Lead über die Netlify-Funktion in die GetResponse-Liste ein.
  // Bewusst nicht-blockierend: scheitert der Eintrag (Netzwerk/Server), bekommt
  // die Nutzerin trotzdem ihr Reading. Doppelte Einträge fängt GetResponse selbst ab.
  function subscribeLead(name, email){
    try{
      fetch('/.netlify/functions/subscribe', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ name: name || '', email: email || '' })
      }).catch(function(){});
    }catch(e){}
  }
''', '', "subscribe-fn-remove")

# ============================================================================
# 3. Ergebnis-Kopf + Zurück-Button
# ============================================================================
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Chartruler${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Der Herrscher deiner Chart'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# Mehr Luft zwischen den Karten (gleiches Spacing wie Chiron-Reader)
# + Header-Typografie: Eyebrow, Titel und Untertitel sauber getrennt,
#   Untertitel kleiner und mit Zeilenluft (Feedback 12.07.: nichts klebt)
SPACING_CSS = """<style>
  .data-block, .cta-block, .summary-block, .results-header{ margin-top:40px !important; margin-bottom:40px !important; }
  .cta-block .cta-kicker{ margin-bottom:16px !important; }
  .cta-block h3{ margin:14px 0 16px !important; line-height:1.3 !important; }
  .cta-block .cta-text{ margin:0 0 24px !important; }
  .header-eyebrow{ margin-bottom:18px !important; letter-spacing:0.26em !important; }
  header h1{ margin:0 0 22px !important; line-height:1.15 !important; }
  .subtitle{
    font-size:clamp(1rem, 2vw, 1.18rem) !important;
    line-height:1.75 !important;
    max-width:480px !important;
    margin:0 auto !important;
    opacity:0.95;
  }
</style>"""
repl("</body>", SPACING_CSS + "\n</body>", "spacing-css")

# ============================================================================
# 4. Chartruler-Berechnung in runCheck einhängen
#    (Anker NACH window.__chart, damit window.__aspects bereits gesetzt ist)
# ============================================================================
calc_anchor = "      window.__chart = chart;\n      generateReading();"
ruler_calc = """      window.__chart = chart;

      // Chartruler: Herrscher des Aszendenten + Position + Verdrahtung
      (function(){
        const FULL = window.__fullChart || [];
        function find(label){ return FULL.find(function(e){ return e.label === label; }) || null; }
        const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Loewe':'Sonne','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schuetze':'Jupiter','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
        const CORULER = { 'Skorpion':'Mars','Wassermann':'Saturn','Fische':'Jupiter' };
        const HOME = { 'Sonne':['Löwe'],'Mond':['Krebs'],'Merkur':['Zwillinge','Jungfrau'],'Venus':['Stier','Waage'],'Mars':['Widder','Skorpion'],'Jupiter':['Schütze','Fische'],'Saturn':['Steinbock','Wassermann'],'Uranus':['Wassermann'],'Neptun':['Fische'],'Pluto':['Skorpion'] };
        const acEntry = find('Aszendent') || {};
        const acSign = acEntry.sign || '';
        const rulerName = RULER[acSign] || '';
        const rulerEntry = rulerName ? (find(rulerName) || {}) : {};
        const coName = CORULER[acSign] || '';
        const coEntry = coName ? (find(coName) || {}) : {};
        const rulerSign = rulerEntry.sign || '';
        const inOwnSign = rulerName ? ((HOME[rulerName] || []).indexOf(rulerSign) !== -1) : false;
        const dispCandidate = RULER[rulerSign] || '';
        const dispName = (dispCandidate && dispCandidate !== rulerName) ? dispCandidate : '';
        const dispEntry = dispName ? (find(dispName) || {}) : {};
        const ASP = window.__aspects || [];
        const rulerAspects = rulerName ? ASP.filter(function(a){ return a.p1 === rulerName || a.p2 === rulerName; }) : [];
        window.__ruler = {
          acSign: acSign,
          name: rulerName,
          sign: rulerSign,
          house: rulerEntry.house || '',
          co: { name: coName, sign: coEntry.sign || '', house: coEntry.house || '' },
          dispositor: { name: dispName, sign: dispEntry.sign || '', house: dispEntry.house || '' },
          aspects: rulerAspects,
          inOwnSign: inOwnSign
        };
      })();

      generateReading();"""
repl(calc_anchor, ruler_calc, "ruler-calc-injection")

# ============================================================================
# 5. Sichtbare Blöcke: Erklärung + Dein Chartruler + Minireading
#    (direkt nach dem Ergebnis-Kopf, vor den Platzierungen)
# ============================================================================
element_anchor = "  // Dominantes Element aus den Hauptpunkten zählen"
ruler_blocks = """  // ===== Chartruler: Erklärung + Minireading =====
  const R = window.__ruler || {};
  const RT = window.CHARTRULER_TEXTS || {};
  html += `
  <div class="data-block">
    <h3>Was ist ein Chartruler?</h3>
    ${(RT.explain || []).map(function(p){ return '<p style="margin:0 0 14px">' + p + '</p>'; }).join('')}
  </div>`;
  if (R.name) {
    html += `
    <div class="data-block">
      <h3>Dein Chartruler: ${R.name}</h3>
      <div class="data-grid">
        <div class="data-row"><span class="data-planet">Dein Aszendent</span><span class="data-values"><span class="badge sign-badge">${R.acSign}</span></span></div>
        <div class="data-row"><span class="data-planet">Dein Chartruler</span><span class="data-values"><span class="badge sign-badge">${R.name}</span></span></div>
        <div class="data-row"><span class="data-planet">${R.name} steht in</span><span class="data-values"><span class="badge sign-badge">${R.sign}</span>${R.house ? `<span class="badge house-badge">${R.house}. Haus</span>` : ''}</span></div>
        ${(R.co && R.co.name && R.co.sign) ? `<div class="data-row"><span class="data-planet">Klassischer Mitherrscher: ${R.co.name}</span><span class="data-values"><span class="badge sign-badge">${R.co.sign}</span>${R.co.house ? `<span class="badge house-badge">${R.co.house}. Haus</span>` : ''}</span></div>` : ''}
      </div>
      ${(RT.acIntro && RT.acIntro[R.acSign]) ? `<p style="margin-top:16px">${RT.acIntro[R.acSign]}</p>` : ''}
    </div>`;
    let mini = '';
    if (RT.planet && RT.planet[R.name]) mini += `<p style="margin:0 0 14px">${RT.planet[R.name]}</p>`;
    if (RT.sign && RT.sign[R.sign]) mini += `<p style="margin:0 0 14px"><strong>${R.name} im Zeichen ${R.sign}:</strong> ${RT.sign[R.sign]}</p>`;
    if (R.inOwnSign && RT.ownSign) mini += `<p style="margin:0 0 14px">${RT.ownSign.split('{P}').join(R.name).split('{S}').join(R.sign)}</p>`;
    if (R.house && RT.house && RT.house[R.house]) mini += `<p style="margin:0 0 14px"><strong>${R.name} im ${R.house}. Haus:</strong> ${RT.house[R.house]}</p>`;
    if (R.house && RT.question && RT.question[R.house]) mini += `<p style="margin-top:18px;color:var(--gold);font-weight:600">Deine Chartruler-Frage: ${RT.question[R.house]}</p>`;
    if (mini) html += `
    <div class="data-block">
      <h3>Dein Minireading</h3>
      ${mini}
    </div>`;
  }

  // Dominantes Element aus den Hauptpunkten zählen"""
repl(element_anchor, ruler_blocks, "ruler-blocks-injection")

# ============================================================================
# 5b. Platzierungen, Aspekte-Liste und Element-Block von der Seite nehmen
#     (Feedback 12.07.: nur Minireading + Prompt sichtbar; im kopierten
#     Prompt bleiben volles Chart und alle Aspekte drin)
# ============================================================================
repl('''  const FULL = window.__fullChart || [];
  if (FULL.length) {
    const rows = FULL.map(e => `<div class="data-row"><span class="data-planet">${e.label}</span><span class="data-values"><span class="badge sign-badge">${e.sign}</span>${e.house ? `<span class="badge house-badge">${e.house}. Haus</span>` : ''}</span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine Platzierungen</h3>
      <div class="data-grid">${rows}</div>
      <button class="copy-btn" id="copyBtn" onclick="copyChartData()">Alle Daten kopieren</button>
    </div>`;
  }

  const ASP = window.__aspects || [];
  if (ASP.length) {
    const arows = ASP.map(a => `<div class="data-row"><span class="data-planet">${a.p1}${a.s1 ? ` <span class="asp-sign">${a.s1}</span>` : ''} <span class="asp-sym">·</span> ${a.p2}${a.s2 ? ` <span class="asp-sign">${a.s2}</span>` : ''}</span><span class="data-values"><span class="badge sign-badge">${a.type}</span></span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine wichtigsten Aspekte</h3>
      <div class="data-grid aspect-grid">${arows}</div>
      <button class="copy-btn" id="copyAspBtn" onclick="copyAspects()">Aspekte kopieren</button>
    </div>`;
  }

  const maxEl = Object.entries(elementCounts).sort((a,b)=>b[1]-a[1]).filter(e=>e[1]>0);
  if (maxEl.length > 0) {
    const dominantEl = maxEl[0][0];
    html += `
    <div class="summary-block">
      <h3>Dein dominantes Element: ${dominantEl}</h3>
      <p>${elementDescriptions[dominantEl]}</p>
    </div>`;
  }
''', '', "platzierungen-aspekte-element-remove")

# ============================================================================
# 6. CTA-Blöcke: Prompt-Button + Womancode statt Business/AstroCode
# ============================================================================
repl('''  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;''',
'''  html += `
  <div class="cta-block">
    <h3>Dein Chartruler-Reading mit KI</h3>
    <p>Das Minireading oben ist der Anfang. Kopiere jetzt den Prompt und füg ihn in ChatGPT oder Claude ein. Dein tiefes Reading zeigt dir, wie dein Chartruler dein Leben führt, in welchem Lebensbereich sich alles entscheidet, welche Kräfte bei jeder Entscheidung mitreden und wie du deinen Kapitän bewusst lebst.</p>
    <button class="copy-btn" id="copyRulerBtn" onclick="copyChartrulerReading()">Chartruler-Prompt + Daten kopieren</button>
  </div>`;''',
"prompt-cta-block")

repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Hast du es satt, deine Weiblichkeit zu zügeln?</p>
    <h3>Lebe dein Womancode im Live-Experiment und werde erfolgreich, glücklich und lebendig.</h3>
    <p class="cta-text">Womancode steht für eine gelebte, lebendige Weiblichkeit. Eine Frau, die weiß, wer sie ist und aus ihrem tiefsten Inneren kreiert.</p>
    <a href="https://patrycja-nasri.de/womancode/" target="_blank" class="cta-link">Hier geht's zu Womancode &rarr;</a>
  </div>`;''',
"womancode-cta")

# ============================================================================
# 7. Prompt-Gehirn + Copy-Funktion austauschen
# ============================================================================
new_region = r"""  window.CHARTRULER_TEXTS = __TEXTS_JSON__;

  const CHARTRULER_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin. Du liest ein Geburtshoroskop über seinen Herrscher: den Chartruler. Du schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Worum es geht: Mein Chartruler ist der Planet, der mein Aszendenten-Zeichen regiert. Er ist der wichtigste Planet meiner Chart, der Kapitän meines Lebens. Sein Zeichen zeigt, wie ich mein Leben führe. Sein Haus zeigt, in welchem Lebensbereich sich mein Leben immer wieder entscheidet. Seine Aspekte zeigen, welche inneren Kräfte bei jeder meiner Entscheidungen mitreden. Die Häuser sind nach Placidus berechnet.

Unten bekommst du meine Daten:
- mein Aszendent und mein Chartruler
- Zeichen und Haus meines Chartrulers
- falls vorhanden: der klassische Mitherrscher meines Aszendenten-Zeichens mit seiner Position
- die Aspekte meines Chartrulers
- der Dispositor: der Herrscher des Zeichens, in dem mein Chartruler steht (dorthin fließt die Energie weiter)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Mein Kapitän. Ein kraftvoller Absatz: welcher Planet mein Leben führt und was das über die Grundenergie meines Lebens sagt. Sprich mich direkt mit "du" an.

2. Meine Tür und die Kraft dahinter. Verbinde meinen Aszendenten mit meinem Chartruler: wie ich auftrete und welche Kraft dieses Auftreten von innen steuert. Zeig mir, wo beide zusammenspielen und wo sie sich widersprechen.

3. Wie ich führe. Lies das Zeichen meines Chartrulers: in welchem Stil, in welchem Tempo und mit welcher Motivation die Kraft arbeitet, die mein Leben lenkt.

4. Wo mein Leben spielt. Nimm das Haus meines Chartrulers und mach konkret, in welchem Lebensbereich sich mein Leben immer wieder entscheidet, zum Beispiel Business, Geld, Beziehungen, Sichtbarkeit, Zuhause, Gesundheit, Berufung oder Rückzug. Gib mir eine Alltagsszene, an der ich das erkenne.

5. Wer mitredet. Geh die Aspekte meines Chartrulers einzeln durch, den engsten zuerst. Sag mir bei jedem, welche innere Kraft mitsteuert, ob sie Rückenwind gibt oder Reibung erzeugt und wie ich sie nutze.

6. Wohin die Energie weiterfließt. Lies den Dispositor, also den Herrscher des Zeichens, in dem mein Chartruler steht. Was will mein Leben über diese Kette noch von mir? Steht mein Chartruler im eigenen Zeichen, dann geh stattdessen darauf ein, was diese Eigenständigkeit bedeutet.

7. Schatten und Geschenk. Wie lebt sich mein Chartruler, wenn ich unbewusst bin: welche Muster, welche Ausreden, welche Sackgassen. Und was geht auf, wenn ich ihn bewusst führe.

8. Meine Chartruler-Frage. Eine einzige, konfrontierende Frage, die mich nicht mehr loslässt.

Falls ein klassischer Mitherrscher angegeben ist, nimm ihn in Schritt 2 und 6 kurz dazu, der Fokus bleibt auf dem Hauptherrscher.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyChartrulerReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const R = window.__ruler || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN CHARTRULER:');
    if(R.acSign) data.push('Mein Aszendent: ' + R.acSign + '.');
    if(R.name) data.push('Mein Chartruler: ' + R.name + ' (Herrscher des Zeichens ' + R.acSign + ').');
    if(R.sign) data.push('Mein Chartruler steht in ' + R.sign + (R.house ? (', ' + R.house + '. Haus') : '') + '.');
    if(R.inOwnSign) data.push('Mein Chartruler steht im eigenen Zeichen und arbeitet in voller Kraft.');
    if(R.co && R.co.name && R.co.sign) data.push('Klassischer Mitherrscher meines Aszendenten-Zeichens: ' + R.co.name + ' in ' + R.co.sign + (R.co.house ? (', ' + R.co.house + '. Haus') : '') + '.');
    if(R.dispositor && R.dispositor.name && R.dispositor.sign) data.push('Dispositor (Herrscher des Zeichens, in dem mein Chartruler steht): ' + R.dispositor.name + ' in ' + R.dispositor.sign + (R.dispositor.house ? (', ' + R.dispositor.house + '. Haus') : '') + '.');
    const ra = R.aspects || [];
    if(ra.length){
      data.push('Aspekte meines Chartrulers:');
      ra.forEach(function(a){ const other = (a.p1 === R.name) ? a.p2 : a.p1; const os = (a.p1 === R.name) ? a.s2 : a.s1; data.push('- ' + R.name + ' ' + a.type + ' ' + other + (os ? (' in ' + os) : '')); });
    } else if(R.name) {
      data.push('Mein Chartruler hat keine engen Aspekte (Orb bis 5 Grad). Er arbeitet als freistehende Kraft.');
    }
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = CHARTRULER_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyRulerBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

new_region = new_region.replace("__TEXTS_JSON__", TEXTS_JSON)

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# Sicherheitscheck: keine Business-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY_DIR, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY_DIR, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY_DIR, "index.html"))
print("Groesse:", len(s), "Zeichen")
