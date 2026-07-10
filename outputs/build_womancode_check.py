#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut womancode-check.html aus astrologie-check.html.
Gleiche Engine (circular-natal-horoscope-js via jsDelivr + Open-Meteo, Placidus),
aber Womancode-Gehirn: 5 Punkte weiblicher Energie (Mond, Venus, Lilith, Mars, IC)
+ Wein/Gold-Design der Womancode-Salespage (Fonts/Logo/Hero aus womancode-reader.html)
+ Countdown auf den Start 22.07.2026 + Platz-Zaehler (noch 5 Plaetze, VIP vergeben).
Kein Platz-Zaehler (Entscheidung Patrycja 09.07.): nur Countdown als Urgency."""
import json, re, os

SRC = "astrologie-check.html"
OUT = "womancode-check.html"
READER = "womancode-reader.html"

WC_URL = "https://patrycja-nasri.de/womancode/"
WC_START_ISO = "2026-07-22T20:00:00+02:00"

with open(SRC, encoding="utf-8") as f:
    html = f.read()
orig_len = len(html)

with open(READER, encoding="utf-8") as f:
    reader = f.read()

# Gold-"Woman CODE"-Logo + Wein/Lotus-Hintergrund direkt aus dem Reader (wie build_womancode_salespage.py)
LOGO = re.search(r'class="wc-logo"\s+src="(data:image/png;base64,[^"]+)"', reader).group(1)
HERO = re.search(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', reader).group(0)

SIGNS = ["Widder","Stier","Zwillinge","Krebs","Löwe","Jungfrau",
         "Waage","Skorpion","Schütze","Steinbock","Wassermann","Fische"]

readings = {}

readings["mond"] = {
"Widder":"Dein Mond im Widder wird satt, wenn du deinem eigenen Impuls folgst. Du brauchst Bewegung, Feuer und das Gefühl, dass dein Leben dir gehört. Genährt wirst du in den Momenten, in denen du etwas beginnst, weil du es willst. Im Alltag drehst du dieses Feuer oft runter. Du wartest, bis alle versorgt sind, und verschiebst das, worauf du Lust hast, auf später. Aus der Lust wird dann Gereiztheit, und du weißt selbst nicht warum. Deine weibliche Kraft liegt in der Erlaubnis, zuerst zu fühlen, was du willst, und dann loszugehen. Du darfst lernen, deinem Impuls zu vertrauen, bevor der Verstand ihn zerredet.",
"Stier":"Dein Mond im Stier wird satt durch Ruhe, Berührung und Genuss. Du brauchst Langsamkeit, gutes Essen und einen Körper, der sich sicher fühlt. Genährt wirst du, wenn du nichts leisten musst und einfach da sein darfst. Im Alltag gönnst du dir das erst, wenn alles erledigt ist, und dieser Moment kommt nie von allein. Du isst im Stehen, du entspannst mit schlechtem Gewissen, du verschiebst deine Pause seit Wochen. Deine weibliche Kraft liegt in der Fähigkeit, tief zu genießen und dadurch aufzutanken. Du darfst lernen, dass dein Genuss keine Belohnung ist, die du dir verdienen musst.",
"Zwillinge":"Dein Mond in den Zwillingen wird satt durch Austausch, Leichtigkeit und Worte. Du brauchst Gespräche, in denen du laut denken darfst, und Menschen, die deine Gedanken halten können. Im Alltag landet dein Fühlen oft im Kopf. Du analysierst dein Gefühl, statt es zu fühlen, und beim dritten Erklären ist es weg. Abends scrollst du, um den Kopf zu füllen, während dein Körper eigentlich etwas anderes braucht. Deine weibliche Kraft liegt in der Verbindung von Kopf und Körper, wenn du aussprichst, was du fühlst, während du es fühlst. Du darfst lernen, dein Gefühl zu leben, bevor du es erklärst.",
"Krebs":"Dein Mond im Krebs wird satt durch Nähe, Geborgenheit und das Gefühl, gehalten zu sein. Du brauchst einen Ort und Menschen, bei denen du weich sein darfst. Im Alltag bist du meistens die, die hält. Du spürst, was jeder in deinem Umfeld braucht, und lieferst es, bevor jemand fragt. Deine eigene Bedürftigkeit versteckst du, weil die Starke keine Wünsche hat. Deine weibliche Kraft ist genau diese Tiefe des Fühlens, wenn sie auch dir selbst gehören darf. Du darfst lernen, dich halten zu lassen, ohne dich dafür zu schämen.",
"Löwe":"Dein Mond im Löwen wird satt durch Freude, Spiel und Momente, in denen du gesehen wirst. Du brauchst Ausdruck, Farbe und ein Leben, das sich nach dir anfühlt. Im Alltag stellst du deine Freude hinten an. Du organisierst die Feste der anderen und vergisst, wann du selbst zuletzt getanzt hast. Dein Strahlen wartet auf einen Anlass, der nie kommt, weil du ihn dir nicht gibst. Deine weibliche Kraft liegt in deiner Lebensfreude, sie steckt an, sobald du sie dir erlaubst. Du darfst lernen, dich zu zeigen, ohne dass es einen Grund braucht.",
"Jungfrau":"Dein Mond in der Jungfrau wird satt, wenn dein Alltag dich trägt, wenn Ordnung, Rhythmus und sinnvolles Tun dir Ruhe geben. Du brauchst das Gefühl, dass du nützlich bist, und genau das wird zur Falle. Du kümmerst dich um alles und alle, dein eigenes Bedürfnis steht auf keiner Liste. Du spürst dich erst, wenn alles erledigt ist, und es ist nie alles erledigt. Deine weibliche Kraft liegt in der liebevollen Sorgfalt, wenn sie sich auch auf dich selbst richtet. Du darfst lernen, dich selbst wie jemanden zu behandeln, für den du sorgst.",
"Waage":"Dein Mond in der Waage wird satt durch Schönheit, Verbindung und Frieden. Du brauchst Harmonie um dich herum, um innerlich zur Ruhe zu kommen. Im Alltag bezahlst du diesen Frieden mit dir selbst. Du spürst die Stimmung im Raum schneller als dein eigenes Gefühl, und du passt dich an, bevor du gemerkt hast, was du eigentlich willst. Bei der Frage, wo du essen willst, sagst du seit Jahren, mir egal. Deine weibliche Kraft liegt in deinem Gespür für Schönheit und Beziehung. Du darfst lernen, dein eigenes Empfinden genauso wichtig zu nehmen wie das aller anderen.",
"Skorpion":"Dein Mond im Skorpion wird satt durch Tiefe, Intensität und Nähe, die nichts zurückhält. Du brauchst Verbindungen, in denen du ganz gesehen wirst, mit allem, was in dir tobt. Im Alltag zeigst du davon nur die Oberfläche. Du fühlst alles, kontrollierst aber genau, wie viel davon nach außen darf, und selbst die Menschen, die dich lieben, kennen nur die halbe Frau. Deine weibliche Kraft ist deine Fähigkeit, dich ganz hinzugeben, ohne dich zu verlieren. Du darfst lernen, deine Tiefe zu teilen, statt sie allein zu tragen.",
"Schütze":"Dein Mond im Schützen wird satt durch Weite, Sinn und Aufbruch. Du brauchst das Gefühl, dass dein Leben größer ist als deine To-do-Liste. Im Alltag hast du deine Sehnsucht klein gefaltet und in den Kalender gepresst. Du funktionierst zwischen Terminen und merkst nur an deiner Rastlosigkeit, dass etwas fehlt. Die Reise, die du seit Jahren machen willst, hat immer noch kein Datum. Deine weibliche Kraft liegt in deinem Vertrauen ins Leben und in deiner Lust auf mehr. Du darfst lernen, deiner Sehnsucht Raum zu geben, bevor sie zur leisen Unzufriedenheit wird.",
"Steinbock":"Dein Mond im Steinbock hat früh gelernt, dass Gefühle warten müssen, bis die Arbeit getan ist. Du brauchst in Wahrheit dasselbe wie jede andere Frau, Nähe, Wärme und einen Ort, an dem du nichts leisten musst. Du erlaubst es dir nur nicht. Im Alltag funktionierst du, du trägst Verantwortung, du hältst durch, und deine Bedürfnisse behandelst du wie Störungen im Betriebsablauf. Deine weibliche Kraft liegt in deiner Verlässlichkeit, die weich werden darf, ohne zu zerbrechen. Du darfst lernen, dass du Zuwendung nicht verdienen musst und Pausen kein Versagen sind.",
"Wassermann":"Dein Mond im Wassermann wird satt durch Freiraum, Eigenständigkeit und Verbindungen, die dich nicht einengen. Du brauchst Luft zum Denken und Menschen, die dein Anderssein feiern. Im Alltag rettest du dich oft in den Kopf. Du beobachtest deine Gefühle aus der Distanz, wie eine Zuschauerin deines eigenen Lebens, und wirkst gefasst, während innen etwas ganz anderes läuft. Deine weibliche Kraft liegt in deiner Freiheit, die Nähe zulassen kann, ohne sich zu verlieren. Du darfst lernen, aus dem Kopf in den Körper zu kommen und dein Gefühl zu fühlen, bevor du es verstehst.",
"Fische":"Dein Mond in den Fischen wird satt durch Stille, Träumen und Momente ohne Anforderung. Du brauchst Rückzug, um zu verarbeiten, was du den ganzen Tag aufnimmst. Denn du spürst alles, die Stimmung deiner Kinder, die Anspannung deines Partners, den Frust deiner Kollegin, und trägst es mit dir herum, als wäre es deins. Am Ende des Tages weißt du nicht mehr, welches Gefühl dir gehört. Deine weibliche Kraft ist genau diese Durchlässigkeit, wenn sie eine Grenze bekommt. Du darfst lernen, dich zurückzuziehen, bevor du leer bist, und nicht erst danach.",
}

readings["venus"] = {
"Widder":"Deine Venus im Widder liebt das Feuer. Dich macht lebendig, was aufregend ist, der Anfang, das Knistern, die Direktheit. Du willst begehren und begehrt werden, mit klarer Ansage. Im Alltag hast du dieses Feuer auf Sparflamme gestellt. Du erledigst Beziehung wie einen Punkt auf der Liste und wunderst dich, wo deine Lust geblieben ist. Deine Sinnlichkeit braucht Bewegung, Spiel und Eroberung, nur dann bleibt sie wach. Du darfst lernen, dir zu nehmen, worauf du Lust hast, ohne auf eine Einladung zu warten.",
"Stier":"Deine Venus im Stier ist die sinnlichste Platzierung, die es gibt. Du bist gebaut für Genuss, für Berührung, für gutes Essen, für Stoff auf der Haut, für Langsamkeit. Empfangen ist deine Natur. Im Alltag hast du daraus ein Belohnungssystem gemacht. Erst die Arbeit, dann vielleicht der Genuss, und meistens fällt er hinten runter. Du kaufst schöne Dinge und trägst sie nicht, du hebst den Genuss für einen Anlass auf. Deine weibliche Kraft liegt in der vollen Erlaubnis zu genießen, ohne Gegenleistung. Du darfst lernen, deinen Körper wieder als Quelle von Lust zu behandeln, statt als Werkzeug.",
"Zwillinge":"Deine Venus in den Zwillingen liebt über Worte. Dich verführt ein kluger Satz mehr als ein Strauß Rosen, du willst reden, lachen, flirten und Gedanken austauschen, die knistern. Im Alltag ist aus dem Flirten Organisieren geworden. Ihr sprecht über Termine, Kinder und Einkäufe, und der Ton, der dich einmal lebendig gemacht hat, ist verschwunden. Auch mit dir selbst redest du nur noch sachlich. Deine weibliche Kraft liegt in deiner Leichtigkeit, in Neugier und Verspieltheit. Du darfst lernen, wieder zu flirten, mit deinem Partner, mit dem Leben, mit dir.",
"Krebs":"Deine Venus im Krebs liebt tief und zärtlich. Du willst Vertrautheit, Rituale und einen Menschen, der dein Innerstes hütet. Geben fällt dir leicht, du umsorgst, du bekochst, du merkst dir alles. Empfangen fällt dir schwer. Wenn jemand dich verwöhnen will, wirst du unruhig und gibst schnell etwas zurück. Deine Zärtlichkeit läuft in eine Richtung, von dir weg. Deine weibliche Kraft liegt in deiner Fähigkeit, eine Nähe zu schaffen, in der Menschen heilen. Du darfst lernen, diese Nähe auch anzunehmen und dich verwöhnen zu lassen, ohne sofort die Rechnung zu begleichen.",
"Löwe":"Deine Venus im Löwen liebt groß. Du willst gefeiert werden, dich schmücken, strahlen und eine Liebe, die sich nach Bühne anfühlt. Schönheit gibt dir Energie wie anderen der Schlaf. Im Alltag hast du dein Bedürfnis nach Bewunderung weggepackt, weil du dich dafür geschämt hast. Du ziehst das Bequeme an, verschiebst den Friseurtermin und nennst es vernünftig, und jedes Mal stirbt ein Stück deiner Lebendigkeit. Dein Glanz ist deine Natur. Du darfst lernen, dich wieder zu schmücken, für dich selbst, und Blicke zu genießen, ohne sie wegzulächeln.",
"Jungfrau":"Deine Venus in der Jungfrau liebt im Konkreten. Deine Zuneigung zeigt sich in Taten, im vorbereiteten Tee, im mitgedachten Detail, in der stillen Fürsorge. Deine Sinnlichkeit liegt in der Achtsamkeit, im bewussten Spüren kleiner Dinge. Im Alltag ist daraus reines Dienen geworden. Du sorgst für alle und gehst mit dir selbst um wie mit einem Projekt, das nie gut genug läuft. Deinen Körper prüfst du im Spiegel, statt ihn zu bewohnen. Deine weibliche Kraft liegt im bewussten Genuss des Konkreten. Du darfst lernen, dich selbst mit derselben Hingabe zu behandeln, mit der du für andere sorgst.",
"Waage":"Deine Venus in der Waage liebt Schönheit in allen Formen. Du brauchst Ästhetik, Stil und ein Gegenüber, mit dem sich das Leben wie ein Tanz anfühlt. Du bist gebaut für das Paarsein und für Räume, die schön sind. Im Alltag machst du dich schön für die Blicke der anderen und richtest Räume her, in denen du selbst nie ankommst. Du gefällst allen und fragst dich abends, wer eigentlich dir gefällt. Deine weibliche Kraft liegt in deinem Sinn für Schönheit, wenn er bei dir selbst beginnt. Du darfst lernen, zu empfangen, was du ständig gibst, Aufmerksamkeit, Wertschätzung und Schönheit.",
"Skorpion":"Deine Venus im Skorpion liebt ganz oder gar nicht. Du willst Verschmelzung, Tiefe und eine Sexualität, die Seelen berührt. Halbe Nähe langweilt dich, du spürst sofort, wenn jemand nicht ganz da ist. Im Alltag schützt du diese Tiefe mit Kontrolle. Du gibst dich nie ganz hin, weil Hingabe sich wie Ausgeliefertsein anfühlt, und bleibst selbst in intimen Momenten die, die beobachtet. Deine weibliche Kraft ist deine erotische Tiefe, sie verwandelt dich und den Menschen, der sie halten darf. Du darfst lernen, die Kontrolle abzugeben und zu erleben, dass du in der Hingabe stärker bist als im Schutz.",
"Schütze":"Deine Venus im Schützen liebt das Abenteuer. Du willst mit deinem Menschen wachsen, reisen, lachen und über Gott und die Welt reden. Deine Lust entzündet sich an Weite und Neuem. Im Alltag ist die Liebe sesshaft geworden und deine Lust gleich mit. Alles ist geregelt, geplant und bekannt, und du verwechselst diese Langeweile mit dem Ende deiner Sinnlichkeit. Deine weibliche Kraft liegt in deiner Begeisterung, sie macht dich anziehend, sobald du ihr folgst. Du darfst lernen, das Abenteuer wieder einzuladen, in deine Beziehung, in deinen Körper, in deinen Alltag.",
"Steinbock":"Deine Venus im Steinbock liebt ernsthaft und beständig. Du willst eine Liebe, die trägt, mit einem Menschen, der bleibt. Oberflächliches Geflirte hat dich nie interessiert. Dein Muster: Du verdienst dir Zuwendung über Zuverlässigkeit und Leistung, und du gönnst dir Sinnlichkeit erst, wenn alles andere steht. So wird aus deiner Liebe Pflichterfüllung und aus deinem Körper ein Terminkalender. Deine weibliche Kraft liegt in deiner Tiefe und Treue, die mit den Jahren immer sinnlicher werden darf. Du darfst lernen, dass dir Liebe und Lust zustehen, ohne dass du sie verdienen musst.",
"Wassermann":"Deine Venus im Wassermann liebt frei. Du brauchst eine Liebe, die dich atmen lässt, Freundschaft im Kern und Raum für dein Anderssein. Enge macht dir mehr Angst als Alleinsein. Im Alltag hältst du auch zu deiner eigenen Sinnlichkeit Distanz. Du lebst viel im Kopf, beobachtest Nähe, statt sie zu fühlen, und dein Körper läuft nebenher wie ein Mitbewohner, mit dem du wenig sprichst. Deine weibliche Kraft liegt in deiner Eigenart, sie zieht genau die Menschen an, die dich wirklich meinen. Du darfst lernen, im Körper anzukommen, ohne deine Freiheit dafür herzugeben.",
"Fische":"Deine Venus in den Fischen liebt grenzenlos. Du willst Verschmelzung, Romantik und eine Liebe, die sich nach Bestimmung anfühlt. Du gibst dich ganz hinein, wenn du liebst, und genau da liegt dein Muster. Du löst dich in den Bedürfnissen des anderen auf, spürst seine Wünsche früher als deine und nennst deine Selbstaufgabe Liebe. Irgendwann bist du in der Beziehung und trotzdem einsam. Deine weibliche Kraft ist deine Hingabe, und sie bleibt nur heilig, solange sie freiwillig ist. Du darfst lernen, bei dir zu bleiben, während du liebst, und zu empfangen, statt nur zu fließen.",
}

readings["lilith"] = {
"Widder":"Deine Lilith im Widder ist die Frau, die will, ohne zu fragen. Sie kennt ihr Begehren, sie geht zuerst los, sie wartet auf niemanden. Du hast früh gelernt, dass so viel Eigenwille bei einer Frau nicht gut ankommt, und hast sie gezähmt. Heute meldet sie sich als plötzliche Wut beim Abwasch und als Gereiztheit, wenn wieder alle etwas von dir wollen. Diese Wut ist deine Lebensenergie, die einen Ausgang sucht. Du darfst lernen, dein Wollen wieder ernst zu nehmen und ihm Raum zu geben, bevor es sich als Explosion meldet.",
"Stier":"Deine Lilith im Stier ist die Frau, die genießt, ohne sich zu schämen. Sie liebt ihren Körper, ihr Essen, ihr Geld und ihre Lust, und sie findet nichts davon zu viel. Du hast gelernt, dass eine Frau bescheiden zu sein hat, und dir das Haben und Genießen verboten. Heute isst du heimlich, kaufst mit schlechtem Gewissen und sprichst über deinen Körper wie über einen Gegner. Deine wilde Weiblichkeit will besitzen, schmecken und sich räkeln dürfen. Du darfst lernen, deinem Hunger zu vertrauen, auf Genuss, auf Fülle, auf Leben.",
"Zwillinge":"Deine Lilith in den Zwillingen ist die Frau, die sagt, was sie denkt, auch wenn der Raum danach still ist. Ihre Sprache ist direkt, frech und manchmal unbequem. Du hast gelernt, dass ein Mädchen freundlich formuliert, und hast deine Klarheit in Watte gepackt. Heute lächelst du in Gesprächen, in denen du innerlich schreist, und schreibst Nachrichten dreimal um, bis sie harmlos sind. Deine wilde Weiblichkeit sitzt auf deiner Zunge. Du darfst lernen, deine Wahrheit unverpackt auszusprechen und die Stille danach auszuhalten.",
"Krebs":"Deine Lilith im Krebs ist die Frau, die Bedürfnisse haben darf, laute, unbequeme, kindliche Bedürfnisse. Du hast gelernt, dass eine gute Frau sich kümmert und selbst nichts braucht, und hast deine Bedürftigkeit zur Sperrzone erklärt. Heute versorgst du alle und wirst innerlich wütend auf die, die sich einfach nehmen, was du dir verbietest. Genau diese Wut zeigt dir, wo deine Wildheit eingesperrt liegt. Deine wilde Weiblichkeit will auch mal fallen, weinen und gehalten werden. Du darfst lernen, zu fordern, was du brauchst, mit derselben Selbstverständlichkeit, mit der du gibst.",
"Löwe":"Deine Lilith im Löwen ist die Frau, die den Raum nimmt, wenn sie ihn betritt. Sie will glänzen, gesehen werden, im Mittelpunkt stehen, und sie genießt es ohne Entschuldigung. Du hast gelernt, dass das arrogant wirkt, und dich gedimmt. Heute trägst du gedeckte Farben, redest dich klein, wenn dich jemand lobt, und spürst einen Stich, wenn eine andere Frau sich nimmt, was du dir versagst. Deine wilde Weiblichkeit ist eine Königin. Du darfst lernen, dein Licht auszuhalten und den Neid der anderen als Kompliment zu nehmen.",
"Jungfrau":"Deine Lilith in der Jungfrau ist die Frau, die sich nicht optimieren lässt. Sie ist wild unter der aufgeräumten Oberfläche, sie will fühlen statt funktionieren. Du hast gelernt, dass eine Frau gepflegt, korrekt und nützlich zu sein hat, und deine Ungezähmtheit weggeräumt wie Unordnung. Heute putzt du, wenn du wütend bist, arbeitest, wenn du weinen müsstest, und hältst deine Fassade makellos. Deine wilde Weiblichkeit liegt unter dem Perfektionismus und wartet. Du darfst lernen, unordentlich zu fühlen, laut zu sein und dich trotzdem wertvoll zu wissen.",
"Waage":"Deine Lilith in der Waage ist die Frau, die lieber wahr ist als gefällig. Sie kann Nein sagen und im Raum bleiben, sie braucht keinen Applaus, um zu wissen, wer sie ist. Du hast gelernt, dass eine Frau angenehm zu sein hat, und dich zur Gefallenden erzogen. Heute sagst du Ja mit zusammengebissenen Zähnen, hältst Beziehungen mit deiner Anpassung am Laufen und verlierst dich darin. Deine wilde Weiblichkeit will anecken dürfen. Du darfst lernen, dass eine Verbindung, die deine Wahrheit nicht aushält, dich in Wahrheit nie gehalten hat.",
"Skorpion":"Deine Lilith im Skorpion ist die Frau mit der dunklen, magnetischen Kraft. Ihre Sexualität ist tief, ihre Wahrnehmung durchdringt jede Fassade, ihre Intensität füllt Räume. Du hast früh gespürt, dass diese Kraft anderen Angst macht, und sie in den Keller gebracht. Heute dimmst du deine Ausstrahlung, sobald es knistert, und hältst deine Tiefe zurück, damit niemand erschrickt. Dabei hungert genau dieser Teil von dir nach Leben. Deine wilde Weiblichkeit wirkt wie Magie, wenn du sie lässt. Du darfst lernen, deine Intensität zu leben, ohne dich für ihre Wirkung zu entschuldigen.",
"Schütze":"Deine Lilith im Schützen ist die Frau, die ihrer eigenen Wahrheit folgt, egal was der Pfarrer, die Mutter oder die Nachbarin sagt. Sie ist frei, laut und unterwegs. Du hast gelernt, dass eine Frau sich einordnet, und deine Freiheit gegen Zugehörigkeit getauscht. Heute lebst du eine kleinere Version deines Lebens und spürst die Sehnsucht als leises Ziehen, wenn andere von ihren Aufbrüchen erzählen. Deine wilde Weiblichkeit will Horizont. Du darfst lernen, deinem inneren Ruf zu folgen, auch wenn du dafür Erwartungen enttäuschst.",
"Steinbock":"Deine Lilith im Steinbock ist die Frau, die Macht hat und sie nimmt. Sie führt, sie entscheidet, sie baut Reiche, und sie entschuldigt sich nicht dafür. Du hast gelernt, dass Macht eine Frau hart macht, und deine Autorität versteckt. Heute arbeitest du in der zweiten Reihe, obwohl du die Erste sein könntest, und nennst es Bescheidenheit. Deine Wut auf Autoritäten zeigt dir, wo deine eigene Kraft eingesperrt liegt. Deine wilde Weiblichkeit trägt eine Krone. Du darfst lernen, Macht und Weichheit zusammen zu leben, als Frau, die führt und fühlt.",
"Wassermann":"Deine Lilith im Wassermann ist die Frau, die anders ist und es zeigt. Sie passt in keine Schublade, sie sprengt Rollenbilder, sie lebt ihr eigenes Modell von Frausein. Du hast gelernt, dass Anderssein einsam macht, und dich der Norm angepasst. Heute trägst du, denkst und lebst unauffälliger, als du bist, und fühlst dich fremd im eigenen Leben. Deine wilde Weiblichkeit ist die Rebellin, die die Regeln neu schreibt. Du darfst lernen, deine Eigenart als Geschenk zu leben und eine Zugehörigkeit gehen zu lassen, die dich verbiegen will.",
"Fische":"Deine Lilith in den Fischen ist die Frau, die mit allem verbunden ist und trotzdem sich selbst gehört. Ihre Sinnlichkeit ist fließend, ihre Intuition uralt, ihre Sehnsucht grenzenlos. Du hast gelernt, dass so viel Gefühl zu viel ist, und dich für dein Fühlen geschämt. Heute betäubst du dich mit Serien, Essen oder Arbeit, wenn die Welle kommt, und opferst dich für andere, um deine eigene Tiefe nicht zu spüren. Deine wilde Weiblichkeit ist ein Ozean. Du darfst lernen, deiner Tiefe zu vertrauen und in ihr zu schwimmen, statt vor ihr davonzulaufen.",
}

readings["mars"] = {
"Widder":"Dein Mars im Widder gibt dir einen Antrieb, der Berge versetzt. Du startest schneller, als andere denken können, und wenn du willst, dann jetzt. Dein Muster: Du bist im Dauervollgas. Du erledigst, entscheidest und rennst von morgens bis abends, und Stillstand fühlt sich wie Rückschritt an. Dein Körper kommt in deinem Tempo nicht mehr vor, er funktioniert nur noch mit. Deine Kraft bleibt dieselbe, wenn sie aus Lust statt aus Druck kommt. Du darfst lernen, vor dem Losrennen einmal zu spüren, ob du überhaupt dorthin willst.",
"Stier":"Dein Mars im Stier arbeitet beharrlicher als jeder andere. Du ziehst durch, wo andere längst aufgeben, und baust Dinge, die bleiben. Dein Muster: Du hörst nicht auf. Du schuftest über deine Grenzen, weil Aufhören sich wie Schwäche anfühlt, und behandelst deinen Körper wie ein Arbeitstier. Dein Nacken ist steif, deine Schultern sind verspannt und dein Becken hat seit Monaten nicht mehr gekreist. Genau in diesem Körper liegt deine Sinnlichkeit begraben. Du darfst lernen, deine Ausdauer auch für deinen Genuss einzusetzen, für lange Abende, langsame Berührung und tiefes Atmen.",
"Zwillinge":"Dein Mars in den Zwillingen macht dich schnell im Kopf und flink im Handeln. Du kannst fünf Dinge gleichzeitig und langweilst dich bei einem. Dein Muster: Dein Verstand kommt nie zur Ruhe. Du beantwortest Nachrichten beim Kochen, planst beim Einschlafen und nennst das Effizienz. Dein Körper wartet unten, während oben das Gewitter läuft. Weibliche Energie beginnt bei dir dort, wo das Denken aufhört. Du darfst lernen, eine Sache zu tun und dabei zu bleiben, mit den Händen, mit den Sinnen, mit dem ganzen Körper.",
"Krebs":"Dein Mars im Krebs kämpft für Menschen, die er liebt. Wenn es um deine Familie oder dein Team geht, entwickelst du Kräfte, die niemand erwartet. Dein Muster: Für dich selbst gehst du nicht los. Du setzt dich für jeden ein, dein eigenes Bedürfnis vertagst du seit Jahren. Deine Kraft kommt in Wellen, mit deinen Gefühlen, und du nennst das Unzuverlässigkeit, dabei ist es dein natürlicher Rhythmus. Du darfst lernen, mit deiner Welle zu arbeiten, statt gegen sie, und dieselbe Löwinnenkraft, die du für andere hast, einmal auf dich selbst zu richten.",
"Löwe":"Dein Mars im Löwen handelt mit Herz und Bühne. Du kannst Menschen bewegen, begeistern und mitreißen, wenn du für etwas brennst. Dein Muster: Du performst, statt zu leben. Du machst aus jedem Tag eine Vorstellung von Stärke, und niemand darf sehen, wie erschöpft die Hauptdarstellerin ist. Anerkennung wurde dein Treibstoff, und der Tank wird nie voll. Deine Kraft wird weiblich, wenn sie aus Freude handelt und keine Zuschauer mehr braucht. Du darfst lernen, Dinge nur für dich zu tun, ohne Publikum, ohne Beweis, aus purer Lust.",
"Jungfrau":"Dein Mars in der Jungfrau arbeitet präzise und unermüdlich. Du siehst jeden Fehler, jede Lücke und jedes Detail, und du ruhst nicht, bis alles stimmt. Dein Muster: Deine To-do-Liste ist dein Tagesgebet. Du optimierst deinen Alltag, deinen Körper und dein Business, und hinter der Optimierung verschwindet das Leben, das du optimierst. Perfekt ist der Feind von lebendig. Du darfst lernen, gut genug stehen zu lassen und die frei gewordene Kraft in etwas zu stecken, das sich gut anfühlt statt nur richtig.",
"Waage":"Dein Mars in der Waage kämpft elegant. Du setzt dich durch über Charme, Diplomatie und kluges Austarieren, und Menschen folgen dir gern. Dein Muster: Deine Kraft geht ins Gefallen. Du strengst dich an, damit alle zufrieden sind, wägst jede Entscheidung dreimal ab und bist abends erschöpft vom Rücksichtnehmen. Wut zeigst du kaum, sie gilt dir als hässlich, also lächelst du sie weg und dein Körper speichert sie. Du darfst lernen, dass ein klares Nein mehr Frieden schafft als hundert halbherzige Ja.",
"Skorpion":"Dein Mars im Skorpion hat eine Kraft, die durch Wände geht. Wenn du dich für etwas entscheidest, gibt es kein Zurück, du gehst durch jede Tiefe. Dein Muster: Verbissenheit. Du kämpfst mit zusammengebissenen Zähnen, kontrollierst jedes Detail und kannst nicht loslassen, selbst wenn dich etwas längst vergiftet. Alles in dir läuft auf Anspannung. Deine Kraft wird weiblich, wenn sie durch den Körper fließen darf, statt sich in ihm zu stauen. Du darfst lernen, loszulassen, was du im Griff halten willst, und deiner Tiefe zu vertrauen, dass sie dich trägt.",
"Schütze":"Dein Mars im Schützen jagt Ziele. Du willst wachsen, weiterkommen, das nächste Level, und kaum ist ein Ziel erreicht, brennt schon das übernächste. Dein Muster: Du kommst nie an. Du feierst deine Erfolge keine fünf Minuten, dann läufst du weiter, und dein Leben fühlt sich an wie eine Dauerjagd. Dein Körper sitzt dabei im Zuschauerraum. Weibliche Energie heißt für dich, den Moment zu ernten, den du dir erarbeitet hast. Du darfst lernen, nach dem Gipfel stehen zu bleiben, die Aussicht zu genießen und dich feiern zu lassen.",
"Steinbock":"Dein Mars im Steinbock ist die Definition von Disziplin. Du arbeitest härter, länger und strukturierter als alle um dich herum, und du erreichst, was du dir vornimmst. Dein Muster: Leistung wurde dein Zuhause. Du funktionierst seit Jahren im männlichen Modus, über Pläne, Ziele und Kontrolle, und dein Erfolg steht, während du dich selbst kaum noch spürst. Pause fühlt sich für dich wie Gefahr an. Genau deshalb bleibt der Umsatz irgendwann stehen, Energie lügt nicht. Du darfst lernen, dass Empfangen kein Kontrollverlust ist und dein nächstes Level nicht aus noch mehr Druck entsteht.",
"Wassermann":"Dein Mars im Wassermann arbeitet über Ideen. Du bist schnell im Denken, gehst unkonventionelle Wege und bist deiner Zeit oft voraus. Dein Muster: Du lebst vom Hals aufwärts. Deine Projekte laufen im Kopf, deine Beziehungen laufen über Distanz, und dein Körper ist das Gerät, das den Kopf durch die Gegend trägt. Gefühle bearbeitest du wie Datensätze. Weibliche Energie beginnt bei dir mit Erdung. Du darfst lernen, regelmäßig aus dem Kopf auszusteigen, barfuß, im Wald, im Wasser, und deinen Körper wieder zu bewohnen.",
"Fische":"Dein Mars in den Fischen kämpft leise und für andere. Deine Kraft fließt in Hilfe, Mitgefühl und Visionen, und sie versickert genauso leise. Dein Muster: Du verzettelst dich. Du fängst für alle mit an, opferst deine Energie für fremde Baustellen und stehst abends mit leerem Tank da, ohne zu wissen, wohin dein Tag geflossen ist. Grenzen setzen fühlt sich für dich hart an. Deine Kraft wird weiblich, wenn sie eine Richtung bekommt, deine Richtung. Du darfst lernen, deine Energie wie kostbares Wasser zu behandeln und selbst zu entscheiden, wohin sie fließt.",
}

readings["ic"] = {
"Widder":"Dein IC im Widder kommt aus einer Linie von Frauen, die kämpfen mussten. Bei euch hieß Frausein, stark sein, sich durchbeißen und niemandem zur Last fallen. Weichheit war ein Luxus, den sich keine leisten konnte. Heute trägst du das weiter, du machst alles allein, lehnst Hilfe ab und ruhst dich nicht aus, obwohl niemand mehr kämpfen muss. Deine Weiblichkeit beginnt dort, wo der alte Kampf endet. Du darfst lernen, dass du die Erste in deiner Linie sein kannst, die weich wird, ohne unterzugehen.",
"Stier":"Dein IC im Stier kommt aus einer Linie von Frauen, für die Sicherheit über allem stand. Bei euch hieß Frausein, festhalten, haushalten und aushalten. Genuss war verdächtig, Veränderung war Gefahr. Heute trägst du das weiter, du bleibst in Situationen, die dich längst nicht mehr nähren, weil Bleiben sich sicherer anfühlt als Leben. Deine Weiblichkeit will mehr als Sicherheit, sie will Fülle. Du darfst lernen, dass du genießen und trotzdem sicher sein kannst, und dass deine Linie mit dir zum ersten Mal satt werden darf.",
"Zwillinge":"Dein IC in den Zwillingen kommt aus einem Zuhause, in dem viel geredet und wenig gefühlt wurde. Bei euch wurden Gefühle besprochen, bewertet oder weggewitzelt, und die wichtigen Dinge blieben unausgesprochen. Heute trägst du das weiter, du erklärst deine Gefühle, statt sie zu fühlen, und füllst Stille sofort mit Worten. Deine Weiblichkeit liegt unterhalb der Worte, in dem Körper, der nie mitreden durfte. Du darfst lernen, still zu werden und zu spüren, was da ist, bevor du es in Sätze packst.",
"Krebs":"Dein IC im Krebs kommt aus einer Linie von Müttern, die sich aufgegeben haben. Bei euch hieß Frausein, für alle da sein, und die Frau, die zuletzt isst, war das Vorbild. Vielleicht hast du nie gesehen, wie eine Frau sich selbst an die erste Stelle setzt. Heute trägst du das weiter, du nährst alle und hungerst selbst, emotional und manchmal wörtlich. Deine Weiblichkeit will endlich auch empfangen. Du darfst lernen, dich selbst zu bemuttern, und damit brichst du ein Muster, das älter ist als du.",
"Löwe":"Dein IC im Löwen kommt aus einem Zuhause, in dem zählte, was die Leute sagen. Bei euch hieß Frausein, vorzeigbar sein, die Fassade halten und Stolz nach außen tragen. Gesehen wurdest du für Leistung und Glanz, für dein bloßes Dasein kaum. Heute trägst du das weiter, du inszenierst dein Leben und fragst dich manchmal, wer hinter der Inszenierung eigentlich wohnt. Deine Weiblichkeit braucht keine Bühne, um wertvoll zu sein. Du darfst lernen, dich auch ungeschminkt und unproduktiv liebenswert zu fühlen.",
"Jungfrau":"Dein IC in der Jungfrau kommt aus einer Linie von Frauen, die gedient haben. Bei euch hieß Frausein, fleißig sein, keine Umstände machen und sich das Dasein über Nützlichkeit verdienen. Gelobt wurde die saubere Küche, nach der Frau darin hat niemand gefragt. Heute trägst du das weiter, du erledigst dein Leben, statt es zu leben, und fühlst dich nur wohl, wenn du gebraucht wirst. Deine Weiblichkeit ist mehr wert als ihr Nutzen. Du darfst lernen, einfach da zu sein, ohne zu dienen, und dich trotzdem berechtigt zu fühlen.",
"Waage":"Dein IC in der Waage kommt aus einem Zuhause, in dem der Frieden wichtiger war als die Wahrheit. Bei euch hieß Frausein, lieb sein, vermitteln und keinen Ärger machen. Vielleicht hast du früh gelernt, die Stimmung deiner Eltern zu lesen und dich passend zu machen. Heute trägst du das weiter, du hältst überall die Harmonie und verlierst dabei deine eigene Stimme. Deine Weiblichkeit braucht Wahrheit mehr als Frieden. Du darfst lernen, Konflikte auszuhalten, und dabei erleben, dass du danach immer noch geliebt wirst.",
"Skorpion":"Dein IC im Skorpion kommt aus einer Linie mit Geheimnissen. Bei euch wurde Schweres nicht besprochen, es wurde geschluckt, und die Frauen trugen es allein, hinter verschlossenen Türen. Vielleicht spürst du bis heute Dinge in deiner Familie, über die nie jemand gesprochen hat. Heute trägst du das weiter, du zeigst niemandem, was wirklich in dir vorgeht, und hältst selbst in Nähe eine Tür verschlossen. Deine Weiblichkeit will das Schweigen beenden. Du darfst lernen, dein Innerstes einem sicheren Menschen zu zeigen, und damit endet das Schweigen deiner Linie bei dir.",
"Schütze":"Dein IC im Schützen kommt aus einem Zuhause, in dem Glaube, Moral oder Meinung vorgaben, was eine Frau darf. Bei euch gab es Regeln fürs Frausein, gesprochene und unausgesprochene, und deine Fragen dazu waren unerwünscht. Heute trägst du das weiter, du suchst nach deiner eigenen Wahrheit und fühlst dich schuldig, sobald du sie findest. Deine Weiblichkeit braucht keine Erlaubnis von oben. Du darfst lernen, deine eigene Instanz zu werden und ein Frausein zu leben, das aus dir selbst kommt und aus keiner Regel.",
"Steinbock":"Dein IC im Steinbock kommt aus einer Linie von Frauen, die durchgehalten haben. In deiner Linie steckt Trümmerfrauen-Energie, es wurde angepackt statt gejammert, und Gefühle galten als Luxus. Bei euch hieß Frausein, Pflicht erfüllen und stark bleiben, egal was es kostet. Heute trägst du das weiter, du funktionierst wie ein Uhrwerk und behandelst deine Erschöpfung als Schwäche. Dabei ist der Krieg deiner Ahninnen lange vorbei. Deine Weiblichkeit darf zum ersten Mal weich sein. Du darfst lernen, dass Durchhalten dich nicht mehr rettet und Loslassen dich nicht mehr gefährdet.",
"Wassermann":"Dein IC im Wassermann kommt aus einem Zuhause mit emotionaler Distanz. Bei euch wurde vernünftig gesprochen und wenig umarmt, und Gefühle blieben Privatsache, jede für sich. Vielleicht warst du das Kind, das anders war und damit allein blieb. Heute trägst du das weiter, du hältst Nähe auf Abstand und beobachtest dein Leben, statt darin zu wohnen. Deine Weiblichkeit braucht Berührung, im wörtlichen Sinn. Du darfst lernen, Nähe im Körper auszuhalten und zu bleiben, wenn jemand dich wirklich sehen will.",
"Fische":"Dein IC in den Fischen kommt aus einer Linie von Frauen, die sich geopfert haben. Bei euch hieß Frausein, sich hingeben, ertragen und die eigenen Träume für andere begraben. Vielleicht trägst du eine Traurigkeit in dir, die älter ist als dein eigenes Leben. Heute trägst du das weiter, du löst dich in den Bedürfnissen anderer auf und nennst es Liebe. Deine Weiblichkeit will fließen, ohne zu verschwinden. Du darfst lernen, dass Hingabe eine Wahl ist und kein Opfer, und dass deine Träume niemandem mehr weichen müssen.",
}

for k, v in readings.items():
    missing = [s for s in SIGNS if s not in v]
    assert not missing, f"{k} fehlt: {missing}"

planetIntros = {
"mond":"Dein Mond ist dein Gefühlskörper. Er zeigt, was dich wirklich nährt, wonach du dich sehnst und welches Bedürfnis untergeht, wenn du nur noch funktionierst.",
"venus":"Deine Venus ist deine Sinnlichkeit. Sie zeigt, wie du liebst, wie du genießt und wie du empfängst. Sie ist der Teil von dir, der nichts leisten muss, um begehrenswert zu sein.",
"lilith":"Lilith ist deine wilde Weiblichkeit. Der Teil von dir, der nie brav sein wollte und den du weggesperrt hast, um zu gefallen. Sie ist deine rohe Lust, deine Wut und deine Urkraft, und sie wartet darauf, dass du die Tür aufmachst.",
"mars":"Mars ist deine Macher-Energie. Er zeigt, wie du anpackst, kämpfst und durchziehst. In der männlichen Energie treibt er dich, in der weiblichen dient er dir.",
"ic":"Dein IC ist deine weibliche Wurzel. Hier liegt, was dir deine Mutter, ihre Mutter und die Frauen davor über das Frausein weitergegeben haben, meistens ohne ein einziges Wort. Dieses Erbe steuert dich, bis du es anschaust.",
}

womancodeQuestions = {
"mond":"Wann hast du heute zum ersten Mal gespürt, was DU brauchst, und was hast du damit gemacht?",
"venus":"Was hast du diese Woche nur zum Genießen getan, ohne Zweck und ohne dass es jemand gesehen hat?",
"lilith":"Welchen Teil von dir sperrst du weg, damit du für andere bequem bleibst?",
"mars":"Wie viel von deinem heutigen Tag war Machen und wie viel war Spüren?",
"ic":"Welchen unausgesprochenen Satz über das Frausein hast du von deiner Mutter übernommen und lebst ihn bis heute?",
}

wcHouse = {
1:{"name":"1. Haus","theme":"Ausstrahlung","description":"Im ersten Haus lebt diese Energie direkt in deinem Auftreten und deiner Ausstrahlung. Man sieht dir an, ob du sie lebst oder unterdrückst, dein Körper zeigt es, bevor du ein Wort gesagt hast."},
2:{"name":"2. Haus","theme":"Selbstwert und Geld","description":"Im zweiten Haus lebt diese Energie in deinem Selbstwert, deinem Körpergefühl und deinem Geld. Wenn du sie übergehst, machst du dich klein beim Preis, beim Genuss und bei allem, was du dir wert bist."},
3:{"name":"3. Haus","theme":"Worte und Denken","description":"Im dritten Haus lebt diese Energie in deinen Worten und deinem Denken. Sie will aussprechen, was du fühlst, und wenn du sie übergehst, redest du über alles außer über dich."},
4:{"name":"4. Haus","theme":"Zuhause und Innenwelt","description":"Im vierten Haus lebt diese Energie in deinem Zuhause und deiner innersten Welt. Sie entscheidet, ob du bei dir selbst ankommst oder auch in den eigenen vier Wänden weiter funktionierst."},
5:{"name":"5. Haus","theme":"Lust und Ausdruck","description":"Im fünften Haus lebt diese Energie in deiner Lust, deiner Kreativität und deinem Spiel. Sie will tanzen, erschaffen und sich zeigen, und wenn du sie übergehst, wird dein Leben korrekt und farblos."},
6:{"name":"6. Haus","theme":"Alltag und Körper","description":"Im sechsten Haus lebt diese Energie in deinem Alltag und deinem Körper. Sie entscheidet, ob deine Routinen dich nähren oder auffressen, und dein Körper führt darüber genau Buch."},
7:{"name":"7. Haus","theme":"Beziehungen","description":"Im siebten Haus lebt diese Energie in deinen Beziehungen. Sie zeigt sich in dem, was du am anderen suchst oder an ihm vermisst, und dein Gegenüber spiegelt dir, was du dir selbst nicht gibst."},
8:{"name":"8. Haus","theme":"Tiefe und Sexualität","description":"Im achten Haus lebt diese Energie in deiner Tiefe, deiner Sexualität und deiner Verwandlungskraft. Sie will Verschmelzung und Kontrollabgabe, und wenn du sie übergehst, bleibt Intimität an der Oberfläche."},
9:{"name":"9. Haus","theme":"Weite und Sinn","description":"Im neunten Haus lebt diese Energie in deiner Sehnsucht nach Weite und Sinn. Sie will wachsen und Neues erfahren, und wenn du sie übergehst, wird dein Leben eng, egal wie voll dein Kalender ist."},
10:{"name":"10. Haus","theme":"Berufung und Sichtbarkeit","description":"Im zehnten Haus lebt diese Energie in deiner Berufung und deiner Sichtbarkeit. Sie will, dass du aus ihr heraus arbeitest und führst, und wenn du sie übergehst, baust du deinen Erfolg gegen deine eigene Natur."},
11:{"name":"11. Haus","theme":"Zugehörigkeit und Vision","description":"Im elften Haus lebt diese Energie in deinen Freundschaften und deiner Vision. Sie will Frauen um dich, die dich lauter machen, und wenn du sie übergehst, passt du dich Kreisen an, die dich leiser machen."},
12:{"name":"12. Haus","theme":"Das Verborgene","description":"Im zwölften Haus lebt diese Energie im Verborgenen. Sie wirkt in deinen Träumen, deiner Intuition und deinem Rückzug, und wenn du sie übergehst, meldet sie sich als Erschöpfung, die kein Schlaf repariert."},
}

def jd(o): return json.dumps(o, ensure_ascii=False)

planets_js = (
"const planets = [\n"
'  { key: "mond",   icon: "🌙", name: "Mond" },\n'
'  { key: "venus",  icon: "♀",  name: "Venus" },\n'
'  { key: "lilith", icon: "⚸",  name: "Lilith" },\n'
'  { key: "mars",   icon: "♂",  name: "Mars" },\n'
'  { key: "ic",     icon: "⌂",  name: "IC" }\n'
"];"
)

house_js = "const houseThemes = {\n" + ",\n".join(
    f"  {n}: {jd(wcHouse[n])}" for n in range(1, 13)
) + "\n};"

readings_order = ["mond", "venus", "lilith", "mars", "ic"]
readings_js = "const readings = {\n" + ",\n".join(
    f"  {k}: {jd(readings[k])}" for k in readings_order
) + "\n};"

intros_js = "const planetIntros = " + jd(planetIntros) + ";"
questions_js = "const womancodeQuestions = " + jd(womancodeQuestions) + ";"

def sub_regex(pattern, repl, flags=0, expect=1):
    global html
    new, n = re.subn(pattern, lambda m: repl, html, flags=flags)
    assert n == expect, f"REGEX '{pattern[:40]}...' -> {n}, erwartet {expect}"
    html = new

def sub_str(old, new, expect=1):
    global html
    n = html.count(old)
    assert n == expect, f"STR '{old[:50]}...' kommt {n}x vor, erwartet {expect}"
    html = html.replace(old, new)

sub_regex(r"const planets = \[.*?\];", planets_js, re.DOTALL, 1)
sub_regex(r"const houseThemes = \{.*?\n\};", house_js, re.DOTALL, 1)
sub_regex(r"const readings = \{.*?\n\};", readings_js, re.DOTALL, 1)
sub_regex(r"const planetIntros = \{.*?\n\};", intros_js + "\n\n" + questions_js, re.DOTALL, 1)

old_chart = '''      const chart = {};
      Object.keys(PLANET_MAP).forEach(key => {
        const body = horo.CelestialBodies[PLANET_MAP[key]];
        chart[key] = { sign: SIGN_DE[body.Sign.label] || body.Sign.label, house: body.House ? body.House.id : '' };
      });
      chart.ac = { sign: SIGN_DE[horo.Ascendant.Sign.label] || horo.Ascendant.Sign.label, house: '' };

      // Vollständiges Chart für die Prompts (alle Punkte, Zeichen + Haus)
      const CB = horo.CelestialBodies, CP = horo.CelestialPoints;
      const dsign = b => b ? (SIGN_DE[b.Sign.label] || b.Sign.label) : '';
      const dhouse = b => (b && b.House && b.House.id) ? b.House.id : '';
      const OPP = { 'Widder':'Waage','Stier':'Skorpion','Zwillinge':'Schütze','Krebs':'Steinbock','Löwe':'Wassermann','Jungfrau':'Fische','Waage':'Widder','Skorpion':'Stier','Schütze':'Zwillinge','Steinbock':'Krebs','Wassermann':'Löwe','Fische':'Jungfrau' };
      const acSign = dsign(horo.Ascendant);
      const mcSign = dsign(horo.Midheaven);'''

new_chart = '''      const CB = horo.CelestialBodies, CP = horo.CelestialPoints;
      const dsign = b => b ? (SIGN_DE[b.Sign.label] || b.Sign.label) : '';
      const dhouse = b => (b && b.House && b.House.id) ? b.House.id : '';
      const OPP = { 'Widder':'Waage','Stier':'Skorpion','Zwillinge':'Schütze','Krebs':'Steinbock','Löwe':'Wassermann','Jungfrau':'Fische','Waage':'Widder','Skorpion':'Stier','Schütze':'Zwillinge','Steinbock':'Krebs','Wassermann':'Löwe','Fische':'Jungfrau' };
      const acSign = dsign(horo.Ascendant);
      const mcSign = dsign(horo.Midheaven);

      // Punkte der weiblichen Energie -> window.__chart
      const chart = {
        mond:   { sign: dsign(CB.moon),   house: dhouse(CB.moon) },
        venus:  { sign: dsign(CB.venus),  house: dhouse(CB.venus) },
        lilith: { sign: dsign(CP.lilith), house: dhouse(CP.lilith) },
        mars:   { sign: dsign(CB.mars),   house: dhouse(CB.mars) },
        ic:     { sign: OPP[mcSign] || '', house: '' }
      };'''
sub_str(old_chart, new_chart, 1)

sub_str(
'let html = `<div class="results-header"><h2>Das Horoskop von ${name}</h2><p>Gelesen aus den Mustern deiner Geburtsenergie</p></div>`;',
'let html = `<div class="results-header"><h2>Dein Womancode-Reading, ${name}</h2><p>Gelesen aus der weiblichen Energie deines Charts</p></div>`;',
1)

sub_str(
'      houseHtml = `<div class="house-addition">Im ${houseInfo.name} zeigt sich diese Energie im Bereich von ${houseInfo.theme}. ${houseInfo.description}</div>`;',
'      houseHtml = `<div class="house-addition">${houseInfo.description}</div>`;',
1)

sub_str(
'''        <p>${signReading}</p>
        ${houseHtml}
      </div>''',
'''        <p>${signReading}</p>
        ${houseHtml}
        ${womancodeQuestions[p.key] ? `<div class="wc-question"><span class="wcq-label">Deine Womancode-Frage</span>${womancodeQuestions[p.key]}</div>` : ''}
      </div>''',
1)

old_el = '''  const maxEl = Object.entries(elementCounts).sort((a,b)=>b[1]-a[1]).filter(e=>e[1]>0);
  if (maxEl.length > 0) {
    const dominantEl = maxEl[0][0];
    html += `
    <div class="summary-block">
      <h3>Dein dominantes Element: ${dominantEl}</h3>
      <p>${elementDescriptions[dominantEl]}</p>
    </div>`;
  }'''
new_el = '''  html += `
    <div class="summary-block">
      <h3>Du darfst dich erinnern</h3>
      <p>Deine tiefe, sinnliche und kraftvolle Power ist nicht weg. Du hast gerade gelesen, warum du sie nicht lebst. Genau dort beginnt der Womancode.</p>
    </div>`;'''
sub_str(old_el, new_el, 1)

old_cta = '''  html += `
  <div class="cta-block">
    <h3>Dein AstroCode. Entschlüssle deine Identität.</h3>
    <p>Du hast gerade die erste Schicht deines astrologischen Blueprint berührt. Wer bin ich? ist die tiefste aller Fragen. Dieses Reading gibt dir einen ersten Blick. Im AstroCode blickst du tiefer. Du erkennst nicht nur, wer du bist. Du wirst es. Du bewegst dich zu der Frau, die du in dir trägst. Du führst dein Business, deine Beziehungen und dein Leben aus deiner tiefsten Identität heraus.</p>
    <p style="margin-top:20px; padding-top:18px; border-top: 1px solid rgba(201,169,110,0.2);">Speicher dir am besten dein Geburtshoroskop ab. Die nächsten Tage schicke ich dir noch weitere Impulse mit den passenden Prompts. Ich möchte Astrologie mit modernen Tools so praxisnah in dein Leben bringen, wie es heute möglich ist. Bewegte Astrologie hat mein ganzes Leben verändert. Dank der Möglichkeiten der KI können wir heute so viel tiefer ins Experiment Identität eintauchen.</p>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Zum AstroCode &rarr;</a>
  </div>`;'''
new_cta = '''  html += `
  <div class="cta-block">
    <h3>Womancode. 6 Wochen zurück in deine weibliche Energie.</h3>
    <p>Es geht um den Raum, in dem du dich erfahren darfst. In dem deine Vision in weiblicher Ekstase entsteht! Es liegt in der Leichtigkeit, aus dem Sein zu kreieren! So viele wollen mit Druck etwas kreieren. Die Inspiration und die Idee entstehen aber in dir. Sie entstehen nicht aus dem Außen! Diesen Zugang darfst du wiederfinden. Dafür öffne ich Womancode!</p>
    <p style="margin-top:18px;">Am 22. Juli öffnet sich der Raum. 6 Wochen Live Experiment mit 4 Live-Calls, intensiver Telegram-Begleitung, deinem Promptguide zu deiner Weiblichkeit, einer Deep Sensual Transmission und einer Goodiebag mit sinnlichem Secret-Öl.</p>
    <a href="__WC_URL__" target="_blank" class="cta-link">Nimm dir deinen Platz &rarr;</a>
  </div>`;'''.replace("__WC_URL__", WC_URL)
sub_str(old_cta, new_cta, 1)

sub_str('<title>Astrologischer Selbst-Check</title>', '<title>Dein Womancode-Check</title>', 1)

old_head = '''    <p class="header-eyebrow">Dein kosmischer Spiegel</p>
    <h1>Dein AstroCheck</h1>
    <p class="subtitle">Entdecke, welche Energien du in dir trägst und wer du wirklich bist.</p>'''
new_head = '''    <img class="wc-logo" src="__LOGO__" alt="Womancode">
    <p class="header-eyebrow">Live Experiment &middot; Start 22. Juli</p>
    <h1>Dein Womancode-Check</h1>
    <p class="subtitle">Deine tiefste weibliche Urkraft ist die Essenz, für die du losgehst. Dieser Check zeigt dir, was dich in deiner Weiblichkeit blockiert.</p>
    <div class="wc-countdown" id="wcCountdown" aria-hidden="true"></div>'''.replace("__LOGO__", LOGO)
sub_str(old_head, new_head, 1)

sub_str('>Mein astrologisches Reading anzeigen</button>', '>Mein Womancode-Reading anzeigen</button>', 1)
sub_str("btn.textContent = 'Berechne dein Horoskop…';", "btn.textContent = 'Dein Chart wird gelesen…';", 1)
sub_str(
'<div class="error-msg" id="errorMsg">Bitte wähle mindestens ein Zeichen aus, um dein Reading zu erhalten.</div>',
'<div class="error-msg" id="errorMsg">Bitte gib deine Geburtsdaten ein, um dein Womancode-Reading zu erhalten.</div>',
1)

# ---- Womancode Wein/Gold-Design als Override-Layer (gewinnt, weil zuletzt im Head) ----
extra_css = '''<style>
:root{ --gold:#E1BE7E; --gold-light:#F6E6C2; --rose:#B4884A; --bg:#1A060C;
  --burgundy:#3A0D1A; --deep-purple:#2A0710; --mid-purple:#3A0D1A;
  --text:#F0E4D6; --text-muted:#C6A896; --accent-purple:#7A1230; }
body{ background-color:#1A060C !important; }
#binary-canvas{ display:none !important; }
body::after{ content:"" !important; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(circle at 18% 12%, rgba(92,10,40,0.55), transparent 44%),
    radial-gradient(circle at 82% 80%, rgba(58,13,26,0.7), transparent 48%),
    radial-gradient(circle at 50% 118%, rgba(225,190,126,0.10), transparent 55%); }
.moon-scene{ background:url("__HERO__") center top / cover no-repeat !important; opacity:0.92; }
header h1{ text-shadow:0 0 42px rgba(92,10,40,0.85), 0 0 90px rgba(225,190,126,0.25) !important; }
.subtitle{ color:#EFD9C2 !important; }
.results-header h2{ text-shadow:0 0 42px rgba(92,10,40,0.85), 0 0 90px rgba(225,190,126,0.2) !important; }
.results-header p{ color:#EFD9C2 !important; }
.tip-box, .form-section, .reading-block, .summary-block, .data-block, .cta-block{
  background:rgba(42,7,16,0.55) !important;
  border:1px solid rgba(225,190,126,0.22) !important;
  box-shadow:0 18px 70px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.05) !important; }
.tip-box{ border-left:3px solid var(--gold) !important; }
input[type="text"], input[type="date"], input[type="time"]{
  background:rgba(255,255,255,0.04) !important; border:1px solid rgba(225,190,126,0.22) !important; }
input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus{
  border-color:rgba(225,190,126,0.6) !important; box-shadow:0 0 28px rgba(225,190,126,0.18) !important; }
.place-results{ background:#2A0710 !important; border:1px solid rgba(225,190,126,0.3) !important; }
.place-item:hover, .place-item.active{ background:rgba(225,190,126,0.15) !important; }
select option{ background:#2A0710 !important; color:#F0E4D6 !important; }
.sign-badge{ background:rgba(92,10,40,0.55) !important; border:1px solid rgba(225,190,126,0.3) !important; color:#F6E6C2 !important; }
.house-badge{ background:rgba(225,190,126,0.14) !important; border:1px solid rgba(225,190,126,0.3) !important; color:#F6E6C2 !important; }
.submit-btn, .cta-link{
  background:linear-gradient(135deg, #E1BE7E 0%, #F6E6C2 50%, #E1BE7E 100%) !important;
  color:#2A0710 !important;
  box-shadow:0 10px 42px rgba(225,190,126,0.4), inset 0 0 0 1px rgba(255,255,255,0.12) !important; }
.submit-btn:hover, .cta-link:hover{ box-shadow:0 16px 60px rgba(225,190,126,0.6) !important; }
.wc-logo{ display:block; margin:0 auto 20px; width:min(300px, 68vw); height:auto; }
.wc-startline{ margin-top:16px; font-family:'Benzin', sans-serif; font-size:0.82rem;
  letter-spacing:0.16em; text-transform:uppercase; color:var(--gold); }
.wc-countdown{ display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin:22px auto 0; }
.wc-count-tile{ min-width:82px; padding:12px 8px 10px; border:1px solid rgba(225,190,126,0.35);
  border-radius:12px; background:rgba(42,7,16,0.6); text-align:center; }
.wc-count-num{ display:block; font-family:'Benzin', sans-serif; font-size:1.7rem; line-height:1.2; color:var(--gold); }
.wc-count-label{ display:block; margin-top:2px; font-size:0.66rem; letter-spacing:0.14em; text-transform:uppercase; color:#C6A896; }
.wc-count-live{ font-family:'Benzin', sans-serif; color:var(--gold); letter-spacing:0.08em; }
@media (max-width:600px){ .wc-count-tile{ min-width:66px; } .wc-count-num{ font-size:1.35rem; } }
.wc-question{ margin-top:18px; padding:16px 18px; border-left:3px solid var(--gold);
  background:rgba(225,190,126,0.08); border-radius:8px; font-style:italic; color:#F6E6C2; }
.wc-question .wcq-label{ display:block; font-style:normal; font-size:0.72rem; letter-spacing:0.14em;
  text-transform:uppercase; color:var(--gold); margin-bottom:6px; }
</style>
</head>'''.replace("__HERO__", HERO)
sub_str('</head>', extra_css, 1)

# ---- Countdown auf den Start ----
countdown_js = '''<script>
(function(){
  var WC_START = new Date('__WC_START__').getTime();
  function pad(n){ return n < 10 ? '0' + n : '' + n; }
  function tick(){
    var el = document.getElementById('wcCountdown');
    if (!el) return;
    var d = WC_START - Date.now();
    if (d <= 0) { el.innerHTML = '<span class="wc-count-live">Der Womancode-Raum ist offen.</span>'; return; }
    var tage = Math.floor(d / 86400000); d %= 86400000;
    var std = Math.floor(d / 3600000); d %= 3600000;
    var min = Math.floor(d / 60000);
    var sek = Math.floor((d % 60000) / 1000);
    el.innerHTML =
      '<span class="wc-count-tile"><span class="wc-count-num">' + tage + '</span><span class="wc-count-label">Tage</span></span>' +
      '<span class="wc-count-tile"><span class="wc-count-num">' + pad(std) + '</span><span class="wc-count-label">Stunden</span></span>' +
      '<span class="wc-count-tile"><span class="wc-count-num">' + pad(min) + '</span><span class="wc-count-label">Minuten</span></span>' +
      '<span class="wc-count-tile"><span class="wc-count-num">' + pad(sek) + '</span><span class="wc-count-label">Sekunden</span></span>';
  }
  tick();
  setInterval(tick, 1000);
})();
</script>
</body>'''.replace("__WC_START__", WC_START_ISO)
sub_str('</body>', countdown_js, 1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

os.makedirs("womancode-check-netlify", exist_ok=True)
with open(os.path.join("womancode-check-netlify", "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK  {SRC} ({orig_len} B) -> {OUT} ({len(html)} B)")
print("    + womancode-check-netlify/index.html")
