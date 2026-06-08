#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut schatten-check.html aus astrologie-check.html.
Gleiche Engine + Design, aber Schattenarbeit-Gehirn (Emotioncode Woche 3).
Readings in Patrycjas Tiefe: Wurzel UND wie sich der Schatten HEUTE zeigt."""
import json, re, os

SRC = "astrologie-check.html"
OUT = "schatten-check.html"

with open(SRC, encoding="utf-8") as f:
    html = f.read()
orig_len = len(html)

SIGNS = ["Widder","Stier","Zwillinge","Krebs","Löwe","Jungfrau",
         "Waage","Skorpion","Schütze","Steinbock","Wassermann","Fische"]

readings = {}

readings["lilith"] = {
"Widder":"Deine Lilith im Widder ist die Frau in dir, die zuerst da ist. Die, die will, die nimmt, die losgeht, ohne zu fragen. Du hast früh gespürt, dass dieses Feuer andere nervös macht, und du hast es kleiner gedreht, um nicht anzuecken. Heute zeigt sich dieser Schatten genau dann, wenn du eigentlich vorangehen willst und stattdessen wartest, bis dich jemand lässt. Du schluckst deine Wut, bis sie als Gereiztheit oder als plötzliche Explosion rauskommt. In deinem Business heißt das, du hältst dich zurück, wo du längst führen könntest. Deine verbannte Kraft ist die Frau, die für sich einsteht, ohne sich zu entschuldigen. Du darfst lernen, deinen Raum zu nehmen, bevor jemand ihn dir gibt, und stehen zu bleiben, auch wenn die ersten Trigger kommen.",
"Stier":"Deine Lilith im Stier ist die Frau, die ohne Schuld genießt und weiß, was sie wert ist. Früh hast du gelernt, dein Begehren und deine Lust zu kontrollieren, um nicht zu viel zu wollen und nicht gierig zu wirken. Heute zeigt sich dieser Schatten, wenn es ums Haben geht. Du machst dich klein beim Geld, beim Preis, beim Fordern dessen, was dir zusteht. Du gibst lieber, als zu nehmen, und nennst es Bescheidenheit. Deine verbannte Kraft ist die Frau, die ihren Körper, ihre Lust und ihren Wohlstand für sich beansprucht. Du darfst lernen, dir zu erlauben, zu haben, was du willst, ohne dich dafür zu rechtfertigen.",
"Zwillinge":"Deine Lilith in den Zwillingen ist die Stimme, die ausspricht, was andere nur denken. Früh hast du gelernt, deine Wahrheit zu glätten, damit sie niemandem wehtut, und dich lieber im Ton anzupassen. Heute zeigt sich dieser Schatten, wenn du etwas Klares sagen willst und im letzten Moment weichspülst. Du verpackst, du relativierst, du fügst ein Lächeln an, damit es bloß nicht zu direkt wird. In Posts, in Calls, in Gesprächen hältst du deine schärfste Wahrheit zurück. Deine verbannte Kraft ist die Frau, die sagt, was ist, und die Reaktion aushält. Du darfst lernen, deine Worte nicht mehr abzurunden, nur damit alle bei dir bleiben.",
"Krebs":"Deine Lilith im Krebs ist das Bedürfnis, das du dir selbst verbietest. Früh hast du gelernt, die Starke zu sein, die für alle sorgt, und deine eigene Bedürftigkeit zu verstecken. Heute zeigt sich dieser Schatten, wenn du am Limit bist und trotzdem nicht um Hilfe bittest. Du hältst alles zusammen, du bist für alle da, und tief drin wartest du darauf, dass endlich jemand fragt, wie es dir geht. Deine verbannte Kraft ist die Frau, die fordern darf, gehalten zu werden, ohne sich dafür zu schämen. Du darfst lernen, deine Sehnsucht zu zeigen, statt sie unter Fürsorge zu begraben.",
"Löwe":"Deine Lilith im Löwen ist die Größe, die du klein gemacht hast. Früh hast du gespürt, dass dein Strahlen andere klein wirken lässt, und du hast dich gedimmt, um keinen Neid zu wecken. Heute zeigt sich dieser Schatten, wenn es ums Sichtbarwerden geht. Du zeigst dich erst, wenn alles perfekt ist, du machst dich zur Nummer zwei, du gönnst anderen die Bühne und nimmst sie dir selbst nicht. In deinem Business bleibst du unter deinem Potenzial, weil oben sein sich gefährlich anfühlt. Deine verbannte Kraft ist die Frau, die strahlt, ohne sich zu rechtfertigen. Du darfst lernen, deinen Platz im Licht einzunehmen und zu bleiben, auch wenn nicht alle es halten können.",
"Jungfrau":"Deine Lilith in der Jungfrau ist die Wildheit, die du in Ordnung und Korrektheit gepresst hast. Früh hast du gelernt, dass du gut bist, wenn du fehlerlos funktionierst, und du hast deine unberechenbare, lebendige Seite weggeräumt. Heute zeigt sich dieser Schatten, wenn du dich hinter Perfektion versteckst. Du machst erst, wenn es makellos ist, du kontrollierst, du verbesserst, und nichts geht jemals raus. Dein rohes, lebendiges Selbst wartet hinter der sauberen Fassade. Deine verbannte Kraft ist die Frau, die fühlt statt funktioniert. Du darfst lernen, dich zu zeigen, bevor du fertig bist, und dich nicht mehr über deine Makellosigkeit zu definieren.",
"Waage":"Deine Lilith in der Waage ist die Wahrheit, die du für den Frieden geopfert hast. Früh hast du gelernt, dich anzupassen, gemocht zu werden, dazuzugehören, und dafür deine eigene Stimme abgegeben. Heute zeigt sich dieser Schatten überall dort, wo du Ja sagst und Nein meinst. Du vermeidest den Konflikt, du glättest, du machst es allen recht, und innen staut sich, was du nie aussprichst. In Beziehungen und im Business verbiegst du dich, bis du dich selbst nicht mehr spürst. Deine verbannte Kraft ist die Frau, die nein sagt und die Beziehung trotzdem hält. Du darfst lernen, deine Position zu halten und stehen zu bleiben, auch wenn die ersten Menschen diese Energie im Moment nicht halten können.",
"Skorpion":"Deine Lilith im Skorpion ist die Intensität, die andere früh überfordert hat. Du hast gespürt, dass deine Tiefe, deine Wahrnehmung und deine Macht zu viel sind, und du hast sie verborgen, um niemanden zu erschrecken. Heute zeigt sich dieser Schatten, wenn du dich abdimmst, sobald du merkst, dass du jemandem zu nah, zu viel, zu durchdringend wirst. Du hältst deine Kraft im Zaum, du zeigst nur die Hälfte, du lässt niemanden ganz an dich heran. Deine verbannte Kraft ist die Frau, die ihre dunkle, magnetische Seite lebt, statt sie zu verstecken. Du darfst lernen, deine Wirkung nicht mehr herunterzuregeln, nur damit andere sich wohler fühlen.",
"Schütze":"Deine Lilith im Schützen ist die Freiheit, die du dir nie ganz erlaubt hast. Früh hast du gelernt, dich anzupassen, statt deinen eigenen, unbequemen Weg zu gehen. Heute zeigt sich dieser Schatten, wenn du deine Wahrheit kennst und sie trotzdem zurückhältst, weil sie zu eckig, zu radikal, zu unbequem wäre. Du lebst eine kleinere Version deines Lebens, als du eigentlich willst. Deine verbannte Kraft ist die Frau, die laut sagt, woran sie glaubt, und danach lebt. Du darfst lernen, dein Leben nach deiner eigenen Überzeugung zu führen, auch wenn es andere irritiert.",
"Steinbock":"Deine Lilith im Steinbock ist die Autorität, die du dir nicht zugestanden hast. Früh hast du gelernt, dich unterzuordnen, brav zu sein, dich nicht über andere zu stellen. Heute zeigt sich dieser Schatten, wenn du führen könntest und es nicht tust. Du wartest auf Erlaubnis, du machst dich zur Zuarbeiterin, du gibst die Macht an andere ab, aus Angst, hart oder kalt zu wirken. In deinem Business bleibst du in der zweiten Reihe, obwohl du längst die Erste sein dürftest. Deine verbannte Kraft ist die Frau, die Verantwortung und Macht übernimmt, ohne sich dafür zu entschuldigen. Du darfst lernen, deine Führung anzunehmen und zu tragen.",
"Wassermann":"Deine Lilith im Wassermann ist das Anderssein, das du versteckt hast. Früh hast du gelernt, dich einzufügen, um dazuzugehören, und deine eigenwillige, unangepasste Seite weggesteckt. Heute zeigt sich dieser Schatten, wenn du dich anpasst, obwohl du es längst anders siehst. Du hältst deine Meinung zurück, du machst mit, du wirst Teil der Masse, um nicht ausgeschlossen zu werden. Deine verbannte Kraft ist die Frau, die ihre Eigenart offen lebt und genau dafür gebraucht wird. Du darfst lernen, dich nicht mehr zu verbiegen für eine Zugehörigkeit, die dich kostet.",
"Fische":"Deine Lilith in den Fischen ist die Frau, die mitfühlt und trotzdem ihre Grenze hält. Früh hast du gelernt, dich für andere aufzulösen, dich zu opfern, immer verständnisvoll zu sein. Heute zeigt sich dieser Schatten, wenn du gibst, bis du leer bist, und dich schuldig fühlst, sobald du etwas für dich nimmst. Du spürst die Bedürfnisse aller, nur deine eigenen nicht. Deine verbannte Kraft ist die Frau, die Nein sagt, ohne ihr Herz zu verlieren. Du darfst lernen, deine Grenze zu setzen, ohne dich dafür zu rechtfertigen oder klein zu fühlen.",
}

readings["saturn"] = {
"Widder":"Dein Saturn im Widder trägt die Angst, nur dann zu zählen, wenn du stark bist und vorangehst. Du treibst dich an, immer die Erste zu sein, und bestrafst dich innerlich für jedes Zögern. Heute zeigt sich dieser Schatten, wenn du dir keine Pause erlaubst, weil Stillstand sich wie Versagen anfühlt. Du machst und machst, du beweist und beweist, und tief drin glaubst du, deinen Platz ständig verdienen zu müssen. Genau hier liegt aber auch deine Reife, denn du kannst eine Kraft werden, die nicht überrollt, sondern führt. Du darfst lernen, dass du auch im Innehalten genug bist und nichts beweisen musst, um zu reichen.",
"Stier":"Dein Saturn im Stier trägt die Angst, nie genug zu haben. Du hältst fest, du sparst, du kontrollierst, weil Mangel sich für dich wie eine reale Bedrohung anfühlt. Heute zeigt sich dieser Schatten beim Geld und beim Selbstwert. Du traust dich nicht, höhere Preise zu nehmen, du klammerst dich an Sicherheit, du machst dich abhängig von dem, was du besitzt. Tief glaubst du, dein Wert hänge an deinem Konto. Deine Reife liegt darin, Sicherheit in dir selbst zu verankern, nicht im Außen. Du darfst lernen, dass dein Wert nicht verhandelbar ist und nicht an Zahlen hängt.",
"Zwillinge":"Dein Saturn in den Zwillingen trägt die Angst, nicht klug oder gebildet genug zu sein. Du wägst jedes Wort ab, aus Furcht, dich zu blamieren oder nicht ernst genommen zu werden. Heute zeigt sich dieser Schatten, wenn du schweigst, obwohl du etwas zu sagen hast. Du wartest, bis du dich für hundertprozentig kompetent hältst, und dieser Moment kommt nie. Du hältst dein Wissen zurück, weil du glaubst, es reicht noch nicht. Deine Reife liegt darin, deine Stimme zu nutzen, bevor du dich bereit fühlst. Du darfst lernen, dass deine Worte Gewicht haben, genau jetzt.",
"Krebs":"Dein Saturn im Krebs trägt die Angst, emotional nicht sicher zu sein. Früh hast du gespürt, dass Nähe unzuverlässig ist, und du hast Mauern um dein Herz gebaut. Heute zeigt sich dieser Schatten, wenn du alles allein trägst, weil du niemandem zutraust, dich aufzufangen. Du gibst Halt, nimmst aber keinen an. Du bist die Starke, die selbst nie zusammenbricht, und das erschöpft dich. Deine Reife liegt darin, dir selbst ein sicheres inneres Zuhause zu bauen und dich gleichzeitig anlehnen zu lassen. Du darfst lernen, dass du dich zeigen darfst, ohne deinen Halt zu verlieren.",
"Löwe":"Dein Saturn im Löwen trägt die Angst, nicht liebenswert zu sein, wenn du nicht lieferst. Früh hast du gelernt, dass Anerkennung an Leistung hängt, und du hast deinen Wert an den Applaus gekoppelt. Heute zeigt sich dieser Schatten, wenn du dich erst zeigst, sobald alles perfekt ist, aus Angst vor Ablehnung. Du strahlst kontrolliert, du hältst dich zurück, du brauchst die Bestätigung und schämst dich gleichzeitig dafür. Deine Reife liegt darin, aus innerer Autorität zu leuchten, nicht aus dem Bedürfnis nach Beifall. Du darfst lernen, dich zu zeigen, bevor du dich sicher fühlst, und zu bleiben, ob Applaus kommt oder nicht.",
"Jungfrau":"Dein Saturn in der Jungfrau trägt die Angst, nie fehlerfrei genug zu sein. Früh hast du gelernt, dass nur das Makellose zählt, und du hast einen inneren Kritiker großgezogen, der nie schweigt. Heute zeigt sich dieser Schatten, wenn du Dinge nicht rausgibst, weil sie noch nicht perfekt sind. Du überarbeitest, du kontrollierst, du verschiebst, und am Ende bleibt das Beste in der Schublade. In deinem Business bremst dich dieser Perfektionismus mehr als jede äußere Hürde. Deine Reife liegt darin, zu liefern, obwohl es unfertig ist. Du darfst lernen, dass ein Fehler dich nicht wertlos macht und dass fertig stärker ist als perfekt.",
"Waage":"Dein Saturn in der Waage trägt die Angst, allein zu sein, wenn du nicht gefällst. Früh hast du gelernt, dass Liebe an Anpassung hängt, und du hast deine Bedürfnisse hinter denen anderer versteckt. Heute zeigt sich dieser Schatten, wenn du Konflikte vermeidest und Ja sagst, obwohl du Nein meinst. Du machst dich zur Diplomatin, du hältst den Frieden, und innen wächst der Groll über das, was du nie ausgesprochen hast. Deine Reife liegt darin, deine Position zu halten und trotzdem in Verbindung zu bleiben. Du darfst lernen, dass eine Beziehung, die deine Wahrheit nicht aushält, dich ohnehin nicht trägt.",
"Skorpion":"Dein Saturn im Skorpion trägt die Angst, ausgeliefert zu sein. Früh hast du gespürt, dass Vertrauen gefährlich ist, und du hast gelernt, alles zu kontrollieren, was du fühlst und zeigst. Heute zeigt sich dieser Schatten, wenn du dich verschließt, sobald es wirklich nah oder tief wird. Du gibst nie ganz die Kontrolle ab, du testest, du beobachtest, du schützt dich, bevor jemand dich überhaupt verletzen könnte. Deine Reife liegt darin, Macht und Tiefe zu tragen, ohne dich zu verpanzern. Du darfst lernen, dich Stück für Stück zu öffnen und zu merken, dass du es überlebst.",
"Schütze":"Dein Saturn im Schützen trägt die Angst, nicht genug Sinn oder Wissen zu haben. Du suchst die große Wahrheit und bleibst dabei in Bewegung, um dich nie festlegen zu müssen. Heute zeigt sich dieser Schatten, wenn du von Vision zu Vision springst und nichts wirklich zu Ende bringst. Du fängst Großes an, und sobald die Struktur kommt, zieht es dich weiter zur nächsten Idee. Du wartest darauf, erst alles zu verstehen, bevor du beginnst. Deine Reife liegt im Bleiben und im Vollenden. Du darfst lernen, heute anzufangen mit dem, was du schon hast, statt auf den perfekten Moment zu warten.",
"Steinbock":"Dein Saturn im Steinbock ist zu Hause und trägt die härteste Form von nicht genug. Früh hast du gespürt, dass du dein Existenzrecht verdienen musst, und du hast Verantwortung getragen, als hinge alles an dir. Heute zeigt sich dieser Schatten, wenn du arbeitest und arbeitest und dir Ruhe nicht erlaubst, weil sie sich wie Faulheit anfühlt. Du bist hart zu dir, du gönnst dir nichts, du beweist ständig. Deine Reife liegt genau hier, denn niemand kann so etwas Bleibendes bauen wie du. Du darfst lernen, dass du nichts beweisen musst, um zu reichen, und dass Pause kein Verrat ist.",
"Wassermann":"Dein Saturn im Wassermann trägt die Angst, nicht dazuzugehören. Früh hast du dich anders gefühlt, und du hast Distanz gehalten, bevor jemand dich ausschließen konnte. Heute zeigt sich dieser Schatten, wenn du dich am Rand hältst, obwohl du dich nach echter Verbindung sehnst. Du beobachtest von außen, du gibst dich kühl, du lässt niemanden ganz rein, um nicht enttäuscht zu werden. Deine Reife liegt darin, dich zu zeigen und zu merken, dass genau deine Eigenart andere anzieht. Du darfst lernen, dass du nicht trotz deines Andersseins dazugehörst, sondern wegen ihm gebraucht wirst.",
"Fische":"Dein Saturn in den Fischen trägt die Angst vor der eigenen Auflösung. Du fühlst so viel, dass du dich an Struktur klammerst, um nicht im Diffusen unterzugehen. Heute zeigt sich dieser Schatten, wenn du entweder hart kontrollierst oder dich verlierst, ohne Mitte dazwischen. Du machst dich starr, weil du Angst hast, sonst zu zerfließen, oder du flüchtest in Tagträume und Aufschub. Deine Reife liegt darin, deinem Gefühl eine klare Form zu geben, statt es zu bekämpfen oder ihm ausgeliefert zu sein. Du darfst lernen, geerdet und durchlässig zugleich zu sein.",
}

readings["pluto"] = {
"Widder":"Dein Pluto im Widder verwandelt deinen Umgang mit Wut, Wille und Durchsetzung. In dir liegt eine Kraft, die etwas niederreißen oder erschaffen kann, und du hast früh gelernt, sie zu fürchten. Heute zeigt sich dieser Schatten, wenn du deine Wucht unterdrückst, bis sie unkontrolliert herausbricht, oder sie ganz abschneidest und passiv wirst. Du ringst um Kontrolle über deinen eigenen Antrieb. Deine Macht zeigt sich, wenn du handelst, ohne um Erlaubnis zu fragen, und deine Kraft bewusst lenkst. Du darfst lernen, deine Wut als Energie zu nutzen, statt sie zu fürchten.",
"Stier":"Dein Pluto im Stier verwandelt deinen Umgang mit Wert, Geld und Besitz. In dir sitzt eine tiefe Angst vor Verlust, die dich festhalten und kontrollieren lässt. Heute zeigt sich dieser Schatten, wenn du dich über das definierst, was du hast, und Mangel wie Vernichtung erlebst. Du klammerst dich an Sicherheit, du lässt nicht los, du machst deinen Wert von Zahlen abhängig. Deine Macht zeigt sich, wenn du erkennst, dass dein Wert nicht zerstörbar ist. Du darfst lernen, loszulassen und zu vertrauen, dass du immer wieder aufbauen kannst.",
"Zwillinge":"Dein Pluto in den Zwillingen verwandelt die Macht deiner Worte und Gedanken. In dir liegt die Fähigkeit, mit Sprache zu durchdringen, zu bewegen oder zu verletzen. Heute zeigt sich dieser Schatten, wenn du deine Gedanken als Kontrolle einsetzt oder deine wahren Worte aus Angst zurückhältst. Du analysierst, du argumentierst, du behältst die Deutungshoheit. Deine Macht zeigt sich, wenn du Wahrheiten aussprichst, die wirklich etwas verändern. Du darfst lernen, deine Stimme als Kraft zu nutzen, statt als Schutzwall.",
"Krebs":"Dein Pluto im Krebs verwandelt deine emotionalen Bindungen. In dir lebt eine alte Angst, verlassen zu werden, die dich klammern oder heimlich kontrollieren lässt. Heute zeigt sich dieser Schatten, wenn du Nähe durch Fürsorge oder Schuld sicherst, statt frei zu lieben. Du gibst, damit niemand geht, du hältst fest, du bindest. Deine Macht zeigt sich, wenn du dich emotional ganz zeigst, ohne den anderen zu binden. Du darfst lernen, dass echte Nähe keine Kontrolle braucht.",
"Löwe":"Dein Pluto im Löwen verwandelt deinen Umgang mit Sichtbarkeit, Ego und Wirkung. In dir lebt ein starker Drang, etwas zu hinterlassen, und die tiefe Angst, übersehen zu werden. Heute zeigt sich dieser Schatten, wenn du Anerkennung brauchst, um dich lebendig zu fühlen, oder dich versteckst, um keine Macht zu zeigen. Du schwankst zwischen Bühne und Rückzug. Deine Macht zeigt sich, wenn du strahlst, ohne Bestätigung zu brauchen. Du darfst lernen, dein Licht nicht mehr vom Applaus abhängig zu machen.",
"Jungfrau":"Dein Pluto in der Jungfrau verwandelt deinen Umgang mit Kontrolle und Perfektion. In dir sitzt der Zwang, jedes Detail zu beherrschen, weil Chaos sich wie Gefahr anfühlt. Heute zeigt sich dieser Schatten, wenn du dich und andere kontrollierst, bis nichts mehr fließt. Du optimierst, du korrigierst, du hältst alles fest. Deine Macht zeigt sich, wenn du dich der Tiefe zuwendest statt der Korrektheit. Du darfst lernen, Kontrolle gegen Vertrauen zu tauschen und zu merken, dass nicht alles zusammenbricht, wenn du loslässt.",
"Waage":"Dein Pluto in der Waage verwandelt deine Beziehungen. In dir tobt ein Machtkampf zwischen Anpassung und Selbstbehauptung. Heute zeigt sich dieser Schatten, wenn du dich in Beziehungen verlierst oder unbewusst durch Harmonie kontrollierst. Du gibst nach, um die Bindung zu halten, und sammelst gleichzeitig Macht über Schuld und Erwartung. Deine Macht zeigt sich, wenn du in Verbindung bleibst, ohne dich aufzugeben. Du darfst lernen, Harmonie nicht mehr über deine Wahrheit zu stellen.",
"Skorpion":"Dein Pluto im Skorpion steht in seiner vollen Kraft. In dir liegt deine tiefste Angst vor Kontrollverlust und gleichzeitig deine größte Macht, dich und andere zu verwandeln. Heute zeigt sich dieser Schatten, wenn du dich der Tiefe verweigerst, alles kontrollierst oder dich verschließt, um nie wieder verletzt zu werden. Du spürst alles, zeigst aber nur die Oberfläche. Deine Macht zeigt sich, wenn du dich genau dorthin stellst, wo andere fliehen. Du darfst lernen, dem Stirb-und-werde zu vertrauen, statt es zu bekämpfen, denn jeder Tod in dir war bisher ein Anfang.",
"Schütze":"Dein Pluto im Schützen verwandelt deinen Glauben und deine Wahrheit. In dir liegt die Macht, alte Überzeugungen zu sprengen und neue zu bauen. Heute zeigt sich dieser Schatten, wenn du dich an Glaubenssätze klammerst, die dich klein halten, oder anderen deine Wahrheit aufdrängst. Du suchst Sinn und verteidigst ihn manchmal wie ein Dogma. Deine Macht zeigt sich, wenn du deine eigene Wahrheit lebst, statt fremde zu übernehmen. Du darfst lernen, jeden Glaubenssatz loszulassen, der dich begrenzt.",
"Steinbock":"Dein Pluto im Steinbock verwandelt deinen Umgang mit Autorität, Struktur und Verantwortung. In dir liegt die Macht, etwas Bleibendes zu bauen, und die Angst, zu versagen oder die Kontrolle zu verlieren. Heute zeigt sich dieser Schatten, wenn du dich verhärtest, alles allein stemmst und Erfolg über deinen Wert stellst. Du baust und baust, ohne dir je genug zu sein. Deine Macht zeigt sich, wenn du Verantwortung trägst, ohne dich zu verpanzern. Du darfst lernen, alte Strukturen einzureißen, die dich nicht mehr tragen.",
"Wassermann":"Dein Pluto im Wassermann verwandelt deinen Umgang mit Zugehörigkeit und Freiheit. In dir liegt die Macht, Systeme zu hinterfragen und neu zu denken. Heute zeigt sich dieser Schatten, wenn du dich anpasst, um dazuzugehören, oder dich radikal abgrenzt, um dich zu schützen. Du schwankst zwischen Mitlaufen und Rebellion. Deine Macht zeigt sich, wenn du anders bist, ohne dich zu verstecken oder zu kämpfen. Du darfst lernen, Zugehörigkeit nicht mehr über Anpassung zu erkaufen.",
"Fische":"Dein Pluto in den Fischen verwandelt deinen Umgang mit Hingabe, Gefühl und Auflösung. In dir liegt die Macht, tiefe, alte Wunden zu heilen, und die Angst, dich darin zu verlieren. Heute zeigt sich dieser Schatten, wenn du vor Schmerz flüchtest, dich betäubst oder dich in den Gefühlen anderer auflöst. Du spürst das Leid der Welt und ertrinkst manchmal darin. Deine Macht zeigt sich, wenn du tief fühlst und trotzdem geerdet bleibst. Du darfst lernen, Schmerz zu verwandeln, statt vor ihm wegzulaufen.",
}

readings["chiron"] = {
"Widder":"Dein Chiron im Widder trägt die Wunde, nicht sein zu dürfen, wer du bist. Früh hast du gespürt, dass deine Eigeninitiative störte, und du hast gelernt, dich zurückzunehmen. Heute zeigt sich diese Wunde, wenn du übergangen wirst und es schluckst, oder wenn du dich gar nicht erst meldest, um nicht abgewiesen zu werden. Du zögerst, deinen Raum zu nehmen, und fühlst dich danach übersehen. Genau hier liegt deine Gabe, denn du kannst andere ermutigen, für sich einzustehen, weil du den Schmerz des Verstummens kennst. Du darfst lernen, dass deine Initiative erwünscht ist, angefangen bei dir selbst.",
"Stier":"Dein Chiron im Stier trägt die Wunde, nicht wertvoll genug zu sein. Früh hast du gespürt, dass dein Wert an Bedingungen hing, und du hast angefangen, ihn dir verdienen zu wollen. Heute zeigt sich diese Wunde beim Geld, beim Selbstwert, beim Fordern dessen, was dir zusteht. Du machst dich klein, du nimmst zu wenig, du zweifelst, ob du es wert bist. Deine Gabe ist, anderen zu helfen, ihren eigenen Wert zu fühlen, weil du den Mangel kennst. Du darfst lernen, dass dein Wert nicht verdient werden muss, er ist schon da.",
"Zwillinge":"Dein Chiron in den Zwillingen trägt die Wunde, nicht gehört zu werden. Früh hast du gespürt, dass deine Worte nicht zählten, und du hast angefangen, an deiner Stimme zu zweifeln. Heute zeigt sich diese Wunde, wenn du dich nicht traust zu sprechen, oder dich übermäßig erklärst, damit man dich endlich versteht. Du hältst dich für nicht klug genug. Deine Gabe ist, anderen zu helfen, ihre Wahrheit auszusprechen, weil du das Schweigen kennst. Du darfst lernen, dass deine Stimme zählt, genau wie sie ist.",
"Krebs":"Dein Chiron im Krebs trägt die Wunde fehlender Geborgenheit. Früh hast du gespürt, dass du emotional nicht sicher gehalten wurdest, und du hast gelernt, dich selbst zu halten. Heute zeigt sich diese Wunde, wenn du dich nicht anlehnen kannst und alles allein trägst, obwohl du dich nach Halt sehnst. Du sorgst für alle und fühlst dich selbst nie ganz zu Hause. Deine Gabe ist, anderen ein Zuhause zu geben, das du selbst vermisst hast. Du darfst lernen, dir diese Geborgenheit auch selbst zu schenken.",
"Löwe":"Dein Chiron im Löwen trägt die Wunde, nicht gesehen zu werden. Früh hast du gespürt, dass dein Strahlen nicht erwünscht war, und du hast es weggesteckt. Heute zeigt sich diese Wunde, wenn du zwischen Verstecken und übertriebenem Zeigen schwankst, immer auf der Suche nach dem Blick, der dich endlich sieht. Sichtbarkeit fühlt sich gefährlich und ersehnt zugleich an. Deine Gabe ist, anderen zu erlauben, sichtbar zu sein, weil du das Übersehenwerden kennst. Du darfst lernen, dass du gesehen werden darfst, einfach weil du da bist.",
"Jungfrau":"Dein Chiron in der Jungfrau trägt die Wunde, nie gut genug zu sein. Früh hast du gespürt, dass nur Fehlerlosigkeit zählte, und dein schärfster Kritiker zog bei dir ein. Heute zeigt sich diese Wunde, wenn du dich für jeden Fehler verurteilst und nichts dir je reicht. Du arbeitest gegen dich, statt für dich. Deine Gabe ist, anderen zu helfen, sich anzunehmen, wie sie sind, weil du den inneren Richter kennst. Du darfst lernen, dass du genügst, lange bevor du perfekt bist.",
"Waage":"Dein Chiron in der Waage trägt die Wunde, nur in Beziehung wertvoll zu sein. Früh hast du gespürt, dass du dich anpassen musst, um geliebt zu werden, und du hast dich abhängig gemacht von der Zustimmung anderer. Heute zeigt sich diese Wunde, wenn du dich im anderen verlierst und ohne Gegenüber kaum weißt, wer du bist. Du gibst dich auf für die Harmonie. Deine Gabe ist, anderen zu zeigen, wie Verbindung ohne Selbstaufgabe geht, weil du das Verlorengehen kennst. Du darfst lernen, dass du auch allein vollständig bist.",
"Skorpion":"Dein Chiron im Skorpion trägt die Wunde von Verrat oder Verlust. Früh hast du gespürt, dass Vertrauen gefährlich ist, und du hast dich durch Kontrolle und Distanz geschützt. Heute zeigt sich diese Wunde, wenn du niemanden ganz reinlässt, weil ein Teil von dir immer auf den nächsten Verrat wartet. Du gehst auf Abstand, bevor jemand dich verletzen kann. Deine Gabe ist, andere durch ihre dunkelsten Stunden zu begleiten, weil du die Tiefe kennst. Du darfst lernen, dass nicht jede Nähe in Schmerz endet.",
"Schütze":"Dein Chiron im Schützen trägt die Wunde fehlenden Sinns. Früh hast du gespürt, dass dein Glaube oder deine Wahrheit nicht zählte, und du hast angefangen, an deinem Weg zu zweifeln. Heute zeigt sich diese Wunde, wenn du rastlos nach Bedeutung suchst und nie ankommst, immer mit dem Gefühl, der größere Sinn fehlt. Du läufst weiter, statt zu vertrauen. Deine Gabe ist, anderen Orientierung und Hoffnung zu geben, weil du die Sinnsuche kennst. Du darfst lernen, dass dein Weg Sinn hat, auch ohne fertige Antwort.",
"Steinbock":"Dein Chiron im Steinbock trägt die Wunde, nur über Leistung wert zu sein. Früh hast du gespürt, dass Liebe verdient werden muss, und du hast angefangen, dich über Erfolg zu definieren. Heute zeigt sich diese Wunde, wenn du dich antreibst und nie ruhst, weil Pause sich nach Wertlosigkeit anfühlt. Du arbeitest für eine Anerkennung, die innen nie ankommt. Deine Gabe ist, anderen zu zeigen, dass sie ohne Leistung genug sind, weil du den Druck kennst. Du darfst lernen, dass du geliebt wirst, auch wenn du nichts leistest.",
"Wassermann":"Dein Chiron im Wassermann trägt die Wunde des Ausgeschlossenseins. Früh hast du gespürt, dass du nicht dazugehörst, und du hast dich an den Rand gestellt, um dich zu schützen. Heute zeigt sich diese Wunde, wenn du dich fremd fühlst, selbst mitten unter Menschen, und dich zurückziehst, bevor man dich ausschließt. Du gehörst nirgends ganz dazu. Deine Gabe ist, anderen einen Platz zu geben, die sich auch fremd fühlen, weil du das Außenstehen kennst. Du darfst lernen, dass du dazugehörst, ohne dich zu verbiegen.",
"Fische":"Dein Chiron in den Fischen trägt die Wunde grenzenloser Empfindsamkeit. Früh hast du gespürt, dass deine Tiefe zu viel war, und du hast dich für dein Fühlen geschämt. Heute zeigt sich diese Wunde, wenn du den Schmerz aller in dich aufnimmst und dabei deine eigene Mitte verlierst. Du spürst alles und schützt dich nicht. Deine Gabe ist, anderen beim Heilen zu helfen, weil du das tiefe Fühlen kennst. Du darfst lernen, mitzufühlen, ohne dich selbst zu verlieren.",
}

readings["mond"] = {
"Widder":"Dein Mond im Widder verbirgt das Bedürfnis nach Autonomie hinter Ungeduld und Gereiztheit. Wird es dir zu eng, reagierst du schnell, statt zu sagen, dass du Raum brauchst. Heute zeigt sich dieser Schatten, wenn deine Wut schneller da ist als das Gefühl darunter. Du fährst hoch, du knallst zu, und erst danach merkst du, was wirklich los war. Unter der Reaktion liegt oft eine Verletzlichkeit, die du nicht zeigen willst. Du darfst lernen, kurz innezuhalten, bevor du reagierst, und dem Gefühl unter der Wut Raum zu geben.",
"Stier":"Dein Mond im Stier verbirgt die Angst vor Veränderung hinter Sturheit und Festhalten. Fühlst du dich unsicher, klammerst du dich an das Vertraute, auch wenn es dich längst nicht mehr nährt. Heute zeigt sich dieser Schatten, wenn du an Menschen, Gewohnheiten oder Situationen hältst, die vorbei sind, weil Loslassen sich wie Boden verlieren anfühlt. Du wählst Sicherheit vor Lebendigkeit. Du darfst lernen, Sicherheit in dir selbst zu verankern, damit Veränderung dich nicht mehr bedroht.",
"Zwillinge":"Dein Mond in den Zwillingen verbirgt Gefühle hinter Worten und Analyse. Wird es ernst, redest oder denkst du, statt zu fühlen. Heute zeigt sich dieser Schatten, wenn du jedes Gefühl sofort erklärst, statt es zu spüren, und dich aus der Tiefe herausredest. Du verstehst alles über dich und kommst trotzdem nicht an dein Fühlen heran. Du darfst lernen, der Stille Raum zu geben, in der ein Gefühl ankommen darf, ohne dass du es sofort in Worte übersetzt.",
"Krebs":"Dein Mond im Krebs verbirgt die eigene Bedürftigkeit hinter Fürsorge. Du kümmerst dich um alle und vergisst dabei, was du selbst brauchst. Heute zeigt sich dieser Schatten, wenn du gibst und gibst und innerlich einen stillen Groll trägst, weil so wenig zurückkommt. Du wartest darauf, dass jemand merkt, wie es dir geht, und sagst es nie. Du darfst lernen, dir selbst die Heimat zu geben, die du allen anderen schenkst, und deine Bedürfnisse auszusprechen, bevor sie zu Groll werden.",
"Löwe":"Dein Mond im Löwen verbirgt die Angst, nicht geliebt zu werden, hinter dem Bedürfnis nach Aufmerksamkeit. Bleibt die Anerkennung aus, fühlst du dich übersehen und ungeliebt. Heute zeigt sich dieser Schatten, wenn du mehr gibst, lauter wirst oder ein Drama brauchst, um dir Nähe zu sichern. Du koppelst deinen Wert an den Blick der anderen. Du darfst lernen, dass du auch ohne Bühne geliebt bist, und dir selbst die Anerkennung zu geben, auf die du wartest.",
"Jungfrau":"Dein Mond in der Jungfrau verbirgt Gefühle hinter Funktionieren und Machen. Geht es dir schlecht, wirst du nützlich, statt zu fühlen. Heute zeigt sich dieser Schatten, wenn dein innerer Kritiker jedes Gefühl bewertet und du dir nicht erlaubst, einfach durcheinander zu sein. Du sortierst dich, statt dich zu spüren. Du darfst lernen, zu fühlen, ohne es zu verstehen oder zu bewerten, und dir selbst die Sanftheit zu geben, die du anderen so leicht gibst.",
"Waage":"Dein Mond in der Waage verbirgt eigene Bedürfnisse hinter Harmonie. Du schluckst, was dich verletzt, um den Frieden nicht zu stören. Heute zeigt sich dieser Schatten, wenn du Ja sagst und Nein meinst und die Wut so lange sammelst, bis sie überläuft. Du spürst die Stimmung im Raum genauer als deine eigene. Du darfst lernen, deine Bedürfnisse auszusprechen, bevor sie sich stauen, und zu sehen, dass echte Harmonie auch deine Wahrheit einschließt.",
"Skorpion":"Dein Mond im Skorpion verbirgt Verletzlichkeit hinter Kontrolle und Tiefe. Du fühlst alles intensiv, zeigst es aber selten, aus Angst vor Verrat. Heute zeigt sich dieser Schatten, wenn dein Misstrauen andere auf Abstand hält und du testest, statt dich zu öffnen. Du trägst Gefühle lange mit dir, manchmal zu lange. Du darfst lernen, dich zu zeigen, obwohl du verletzt werden könntest, denn deine Tiefe ist eine Kraft, keine Gefahr.",
"Schütze":"Dein Mond im Schützen verbirgt Schwere hinter Humor und Bewegung. Wird es eng, lenkst du ab, machst einen Witz oder gehst. Heute zeigt sich dieser Schatten, wenn du vor dem flüchtest, was tief gefühlt werden will, und dich in die nächste Aktivität stürzt. Du hältst es leicht, damit es dich nicht erwischt. Du darfst lernen, zu bleiben und durchzufühlen, statt davonzulaufen, denn ein durchgefühltes Gefühl nimmt dir keine Freiheit, es gibt sie dir.",
"Steinbock":"Dein Mond im Steinbock verbirgt das Bedürfnis nach Halt hinter Stärke und Haltung. Du hältst die Form, auch wenn innen alles bebt. Heute zeigt sich dieser Schatten, wenn du hart zu dir bist und dir kein Gefühl zugestehst, weil Schwäche sich gefährlich anfühlt. Du funktionierst, du trägst, du brichst nie zusammen. Du darfst lernen, dir zu erlauben, weich und bedürftig zu sein, ohne dich dafür zu verurteilen.",
"Wassermann":"Dein Mond im Wassermann verbirgt Gefühle hinter Distanz und Beobachtung. Wird es nah, gehst du in den Kopf, statt zu fühlen. Heute zeigt sich dieser Schatten, wenn du dich von deinen eigenen Emotionen abkoppelst und sie analysierst, als wären sie ein fremdes Phänomen. Unnahbarkeit schützt dich vor Verletzung. Du darfst lernen, Wärme zuzulassen, ohne deine Freiheit zu verlieren, und nah zu sein und trotzdem du selbst zu bleiben.",
"Fische":"Dein Mond in den Fischen verbirgt die eigene Mitte im Strom fremder Gefühle. Du nimmst alles auf und weißt oft nicht, was davon deins ist. Heute zeigt sich dieser Schatten, wenn du in den Bedürfnissen anderer verschwindest und deine eigenen aus dem Blick verlierst. Du fühlst die ganze Welt und dich selbst am wenigsten. Du darfst lernen, klare Grenzen zu ziehen und dich zu erden, damit deine Empathie kein Verschwinden mehr ist, sondern eine Gabe.",
}

readings["mars"] = {
"Widder":"Dein Mars im Widder will direkt, sofort, ohne Umweg. Hast du gelernt, deine Wut zu unterdrücken, kommt sie als plötzliche Explosion zurück, oder du schneidest sie ganz ab und wirst seltsam passiv. Heute zeigt sich dieser Schatten, wenn du entweder überrollst oder dich gar nicht mehr durchsetzt. Dein Antrieb sucht ein Ventil. Deine Kraft liegt darin, klar zu handeln, ohne den anderen zu überfahren. Du darfst lernen, deine Wut als gerichtete Energie zu nutzen, statt sie zu fürchten oder zu verschlucken.",
"Stier":"Dein Mars im Stier will langsam, beständig, unaufhaltsam. Unterdrückst du deinen Ärger, staut er sich, bis du explodierst oder ganz erstarrst. Heute zeigt sich dieser Schatten, wenn deine Sturheit jede Bewegung blockiert und du dich eingräbst, statt dich zu zeigen. Du hältst aus, wo du längst handeln solltest. Deine Kraft liegt darin, deinen Willen ruhig durchzuhalten. Du darfst lernen, deine Wut früh und klar auszudrücken, bevor sie zu Beton wird.",
"Zwillinge":"Dein Mars in den Zwillingen will durch Worte kämpfen. Unterdrückst du deine Wut, wird sie zu Sarkasmus, Ironie oder spitzen Bemerkungen. Heute zeigt sich dieser Schatten, wenn du verdeckt stichelst, statt offen zu sagen, was dich stört. Deine Aggression läuft durch die Hintertür. Deine Kraft liegt darin, mit klaren Worten für dich einzustehen. Du darfst lernen, direkt zu sagen, was dich ärgert, statt es in einem cleveren Satz zu verstecken.",
"Krebs":"Dein Mars im Krebs will schützen, traut sich aber selten direkt. Unterdrückst du deine Wut, wird sie zu Schmollen, Rückzug oder leisen Vorwürfen. Heute zeigt sich dieser Schatten, wenn du beleidigt schweigst, statt zu sagen, was du brauchst, und darauf wartest, dass der andere es errät. Deine Aggression brodelt unter der Oberfläche. Deine Kraft liegt darin, deine Bedürfnisse offen zu vertreten. Du darfst lernen, direkt zu fordern, statt indirekt zu strafen.",
"Löwe":"Dein Mars im Löwen will mit Stolz, Geste und Präsenz. Unterdrückst du deine Wut, wird sie zu gekränktem Ego oder großem Drama. Heute zeigt sich dieser Schatten, wenn du im Konflikt um Anerkennung kämpfst, statt um die Sache. Deine Durchsetzung dreht sich dann um dich, nicht um das Ziel. Deine Kraft liegt darin, dich zu zeigen, ohne dich beweisen zu müssen. Du darfst lernen, deine Wut für etwas einzusetzen, das größer ist als dein Stolz.",
"Jungfrau":"Dein Mars in der Jungfrau will präzise, durchdacht, kontrolliert. Unterdrückst du deine Wut, wird sie zu Kritik, an anderen und vor allem an dir. Heute zeigt sich dieser Schatten, wenn du gereizt nörgelst, statt klar anzusprechen, was dich wirklich stört. Deine Aggression zerpflückt im Detail, statt offen zu sein. Deine Kraft liegt darin, ein Problem direkt zu benennen. Du darfst lernen, deine Wut auszusprechen, statt sie in Korrektur und Kritik zu verstecken.",
"Waage":"Dein Mars in der Waage will keinen Streit, will Frieden, will Ausgleich. Unterdrückst du deine Wut, wird sie zu passiver Aggression oder zu stiller Erschöpfung. Heute zeigt sich dieser Schatten, wenn du Konflikte vermeidest und sie damit nur aufschiebst, bis sie größer werden. Du bist nett, bis du leer bist. Deine Kraft liegt darin, deine Position zu halten, auch wenn es ungemütlich wird. Du darfst lernen, dass ein klarer Konflikt eine Beziehung eher rettet als zerstört.",
"Skorpion":"Dein Mars im Skorpion will tief, kompromisslos, ganz. Unterdrückst du deine Wut, wird sie zu Groll, der lange nachhallt, oder zu kühler Rache, die im Stillen plant. Heute zeigt sich dieser Schatten, wenn du nicht vergibst und nicht vergisst und deine Kraft im Verborgenen einsetzt. Deine Intensität sucht ein Ventil. Deine Kraft liegt darin, deine Wucht offen und gerichtet einzusetzen. Du darfst lernen, deine Macht zu zeigen, statt sie unter der Oberfläche zu halten.",
"Schütze":"Dein Mars im Schützen will frei, überzeugt, in Bewegung. Unterdrückst du deine Wut, wird sie zu Selbstgerechtigkeit oder zur Flucht in die nächste Sache. Heute zeigt sich dieser Schatten, wenn du belehrst, statt zu streiten, oder einfach gehst, statt zu bleiben. Du weichst dem echten Konflikt aus. Deine Kraft liegt darin, für deine Wahrheit einzustehen, ohne zu predigen. Du darfst lernen, im Konflikt zu bleiben, statt dich auf den höheren Standpunkt zu retten.",
"Steinbock":"Dein Mars im Steinbock will kontrolliert, strategisch, beherrscht. Unterdrückst du deine Wut, wird sie zu Kälte, Härte oder verbissenem Durchziehen. Heute zeigt sich dieser Schatten, wenn du dich verpanzerst und alles allein durchkämpfst, statt deine Wut überhaupt zu fühlen. Deine Kraft wird zu Druck, der nie nachlässt. Deine Kraft liegt darin, deine Stärke zu zeigen, ohne dich zu verhärten. Du darfst lernen, deine Wut zuzulassen, statt sie in Disziplin zu begraben.",
"Wassermann":"Dein Mars im Wassermann will distanziert, prinzipiell, frei. Unterdrückst du deine Wut, wird sie zu kühlem Abstand oder stillem Trotz. Heute zeigt sich dieser Schatten, wenn du dich zurückziehst oder rebellierst, statt klar zu sagen, was du willst. Deine Durchsetzung grenzt nur ab, statt zu fordern. Deine Kraft liegt darin, dein Anliegen offen zu vertreten. Du darfst lernen, präsent zu bleiben und deine Wut zu zeigen, statt cool auf Abstand zu gehen.",
"Fische":"Dein Mars in den Fischen will niemanden verletzen, will fließen, will Frieden. Unterdrückst du deine Wut, wird sie zu Opferhaltung oder diffuser Erschöpfung. Heute zeigt sich dieser Schatten, wenn deine Kraft sich auflöst, bevor sie ankommt, und du dich machtlos fühlst, statt zu handeln. Deine Wut verschwimmt, bevor du sie spürst. Deine Kraft liegt darin, deine Grenze zu setzen, auch wenn du dich dabei schuldig fühlst. Du darfst lernen, dass Nein sagen kein Verrat an deinem Mitgefühl ist.",
}

readings["suedknoten"] = {
"Widder":"Dein Südknoten im Widder zieht dich in den Alleingang. Es ist dir vertraut, alles selbst zu machen, niemanden ranzulassen, dich allein durchzukämpfen. Heute zeigt sich dieses Muster, wenn du unter Druck dichtmachst und glaubst, nur du kannst es richtig. Du isolierst dich genau dann, wenn du Verbindung am meisten brauchst. Es fühlt sich nach Stärke an und kostet dich Kraft und Nähe. Du wächst, wenn du lernst, dich zu verbinden und zuzulassen, dass andere dich tragen.",
"Stier":"Dein Südknoten im Stier zieht dich in die Sicherheit des Vertrauten. Es ist dir vertraut, am Bekannten festzuhalten, auch wenn es dich klein hält. Heute zeigt sich dieses Muster, wenn du unter Druck im Gewohnten verharrst, statt dich auf Tiefe oder Veränderung einzulassen. Du wählst das Bequeme vor dem Lebendigen. Es fühlt sich sicher an und hält dich gleichzeitig fest. Du wächst, wenn du dich der Wandlung stellst, vor der du dich drückst.",
"Zwillinge":"Dein Südknoten in den Zwillingen zieht dich in die Zerstreuung. Es ist dir vertraut, Informationen, Meinungen und Optionen zu sammeln, statt dich festzulegen. Heute zeigt sich dieses Muster, wenn du unter Druck redest, recherchierst und überall hörst, nur nicht auf dich. Du weichst über das Viele aus. Es fühlt sich klug an und hält dich von deiner Wahrheit fern. Du wächst, wenn du deiner inneren Stimme folgst statt allen anderen.",
"Krebs":"Dein Südknoten im Krebs zieht dich in Abhängigkeit und Fürsorge. Es ist dir vertraut, Halt im Umsorgen oder Umsorgtwerden zu suchen. Heute zeigt sich dieses Muster, wenn du unter Druck in die emotionale Sicherheit zurückfällst und dich an Menschen oder Rollen klammerst. Du machst dich klein, um gehalten zu werden. Es fühlt sich nach Geborgenheit an und hält dich von deiner Eigenständigkeit ab. Du wächst, wenn du Verantwortung übernimmst und für dich selbst stehst.",
"Löwe":"Dein Südknoten im Löwen zieht dich zur Bühne. Es ist dir vertraut, Bestätigung und Aufmerksamkeit zu suchen und dich darüber zu definieren. Heute zeigt sich dieses Muster, wenn du unter Druck darum kreist, wie du wirkst, und dein Selbstwert am Applaus hängt. Du machst dich zur Hauptrolle, auch wo es nicht um dich geht. Es fühlt sich nach Sichtbarkeit an und hält dich in der Abhängigkeit vom Blick anderer. Du wächst, wenn du dich einer Sache widmest, die größer ist als deine Anerkennung.",
"Jungfrau":"Dein Südknoten in der Jungfrau zieht dich in Kontrolle und Kritik. Es ist dir vertraut, zu optimieren, zu korrigieren und alles im Griff zu haben. Heute zeigt sich dieses Muster, wenn du unter Druck im Detail versinkst und dich und andere zerpflückst, bis nichts mehr fließt. Du machst dich zur Kritikerin, vor allem an dir. Es fühlt sich nach Sorgfalt an und hält dich im Mangel. Du wächst, wenn du vertraust, statt alles zu kontrollieren.",
"Waage":"Dein Südknoten in der Waage zieht dich in Anpassung. Es ist dir vertraut, zu gefallen, auszugleichen und Konflikte zu vermeiden. Heute zeigt sich dieses Muster, wenn du unter Druck nachgibst, um die Beziehung zu halten, und deine eigene Stimme verlierst. Du machst dich abhängig von der Zustimmung anderer. Es fühlt sich nach Harmonie an und kostet dich dich selbst. Du wächst, wenn du für dich einstehst, auch auf die Gefahr hin, jemanden zu enttäuschen.",
"Skorpion":"Dein Südknoten im Skorpion zieht dich in Intensität und Krise. Es ist dir vertraut, dich an das zu binden, was dich aufwühlt, und im Drama oder in der Kontrolle Halt zu suchen. Heute zeigt sich dieses Muster, wenn du unter Druck festhältst, misstraust oder dich in Tiefen verstrickst, statt loszulassen. Du suchst die Verwicklung. Es fühlt sich nach Wahrheit an und hält dich gefangen. Du wächst, wenn du loslässt und dir Einfachheit und Vertrauen erlaubst.",
"Schütze":"Dein Südknoten im Schützen zieht dich in die Flucht nach vorn. Es ist dir vertraut, die nächste Vision zu jagen, statt im Konkreten zu bleiben. Heute zeigt sich dieses Muster, wenn du unter Druck ins Große ausweichst, neue Pläne machst und das Naheliegende liegen lässt. Du läufst dem Horizont hinterher. Es fühlt sich nach Freiheit an und hält dich vom Vollenden ab. Du wächst, wenn du bleibst und im Detail Verantwortung übernimmst.",
"Steinbock":"Dein Südknoten im Steinbock zieht dich in Kontrolle und Pflicht. Es ist dir vertraut, zu arbeiten, zu leisten und stark zu sein, statt zu fühlen. Heute zeigt sich dieses Muster, wenn du unter Druck in die Härte gehst, alles allein trägst und dich über deine Funktion definierst. Du machst dich zur Verantwortlichen für alles. Es fühlt sich nach Stärke an und schneidet dich von dir selbst ab. Du wächst, wenn du dich emotional zeigst und dich anlehnst.",
"Wassermann":"Dein Südknoten im Wassermann zieht dich in Distanz. Es ist dir vertraut, von außen zu beobachten, cool zu bleiben und dich nicht einzulassen. Heute zeigt sich dieses Muster, wenn du unter Druck in den Kopf gehst und dich emotional zurückziehst, statt nah zu sein. Du machst dich zur Beobachterin deines eigenen Lebens. Es fühlt sich nach Freiheit an und hält dich allein. Du wächst, wenn du dich emotional einlässt und nahbar wirst.",
"Fische":"Dein Südknoten in den Fischen zieht dich in Auflösung und Flucht. Es ist dir vertraut, dich zurückzuziehen, zu träumen oder dich zu betäuben, wenn es zu viel wird. Heute zeigt sich dieses Muster, wenn du unter Druck verschwindest, dich ablenkst oder dich machtlos fühlst, statt zu handeln. Du löst dich auf, statt zu bleiben. Es fühlt sich nach Erleichterung an und hält dich aus deinem Leben heraus. Du wächst, wenn du dich erdest und präsent bleibst, auch wenn es weh tut.",
}

readings["deszendent"] = {
"Widder":"Dein Deszendent im Widder zieht starke, durchsetzungsfähige Menschen in dein Leben. Was dich an ihnen reizt oder triggert, ist oft deine eigene unterdrückte Kraft. Du überlässt anderen die Wut, das Vorangehen und das klare Nein, das du dir selbst verbietest. Heute zeigt sich das, wenn du dich über dominante Menschen aufregst und ihnen gleichzeitig folgst. Deine Aufgabe ist es, deine eigene Durchsetzung zu leben, statt sie an andere abzugeben.",
"Stier":"Dein Deszendent im Stier zieht ruhige, beständige Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene Sehnsucht nach Sicherheit, Ruhe und Genuss. Du überlässt anderen die Gelassenheit, die du dir selbst nicht erlaubst. Heute zeigt sich das, wenn du dich nach ihrer Bodenständigkeit sehnst und dich selbst dauernd antreibst. Deine Aufgabe ist es, deinen eigenen Wert und deine eigene Ruhe zu finden.",
"Zwillinge":"Dein Deszendent in den Zwillingen zieht kommunikative, geistig bewegliche Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene Leichtigkeit, die du zurückhältst. Du überlässt anderen das freie Reden und Spielen. Heute zeigt sich das, wenn du ihre Lockerheit bewunderst und dich selbst ernst und schwer machst. Deine Aufgabe ist es, deine eigene Stimme und Leichtigkeit zu nutzen.",
"Krebs":"Dein Deszendent im Krebs zieht fürsorgliche, emotionale Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene verdrängte Bedürftigkeit und Weichheit. Du überlässt anderen das Fühlen und Nähren. Heute zeigt sich das, wenn du dich nach ihrer Wärme sehnst und dir selbst keine Bedürftigkeit erlaubst. Deine Aufgabe ist es, deine eigene Zärtlichkeit zuzulassen.",
"Löwe":"Dein Deszendent im Löwen zieht selbstbewusste, strahlende Menschen in dein Leben. Was dich an ihnen reizt, ist oft dein eigenes zurückgehaltenes Strahlen. Du überlässt anderen die Bühne und das Sichtbarsein. Heute zeigt sich das, wenn du Menschen bewunderst, die sich zeigen, und dich selbst zurücknimmst. Deine Aufgabe ist es, dich selbst sichtbar zu machen und dein Licht zu zeigen.",
"Jungfrau":"Dein Deszendent in der Jungfrau zieht ordentliche, hilfsbereite, gewissenhafte Menschen in dein Leben. Was dich an ihnen reizt oder stört, ist oft dein eigenes Verhältnis zu Kontrolle und Dienst. Du überlässt anderen die Sorgfalt oder ärgerst dich über ihre Korrektheit. Heute zeigt sich das, wenn ihre Genauigkeit dich triggert, weil sie etwas in dir berührt. Deine Aufgabe ist es, dich selbst klar zu strukturieren, ohne dich zu verlieren.",
"Waage":"Dein Deszendent in der Waage zieht harmonische, diplomatische, ästhetische Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene Sehnsucht nach Ausgleich und Schönheit. Du überlässt anderen das Verbinden und Vermitteln. Heute zeigt sich das, wenn du dich nach ihrer Leichtigkeit im Miteinander sehnst und selbst dauernd kämpfst. Deine Aufgabe ist es, selbst für Balance zu sorgen, ohne dich aufzugeben.",
"Skorpion":"Dein Deszendent im Skorpion zieht intensive, tiefe, magnetische Menschen in dein Leben. Was dich an ihnen reizt oder triggert, ist oft deine eigene verdrängte Tiefe und Macht. Du überlässt anderen die Intensität, vor der du dich selbst zurückhältst. Heute zeigt sich das, wenn dich machtvolle Menschen anziehen und gleichzeitig verunsichern. Deine Aufgabe ist es, deine eigene Tiefe und Wirkung zu leben.",
"Schütze":"Dein Deszendent im Schützen zieht freiheitsliebende, überzeugte, weltoffene Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene zurückgehaltene Weite und Wahrheit. Du überlässt anderen die große Vision und den Mut zur eigenen Meinung. Heute zeigt sich das, wenn du ihre Freiheit bewunderst und dich selbst eng hältst. Deine Aufgabe ist es, deine eigene Wahrheit zu verfolgen und zu leben.",
"Steinbock":"Dein Deszendent im Steinbock zieht ernste, verantwortungsvolle, strukturierte Menschen in dein Leben. Was dich an ihnen reizt oder stört, ist oft dein eigenes Verhältnis zu Autorität und Macht. Du überlässt anderen die Führung und die Verantwortung. Heute zeigt sich das, wenn dich Autoritätspersonen triggern, weil sie deine eigene ungelebte Stärke spiegeln. Deine Aufgabe ist es, deine eigene Verantwortung und Macht zu übernehmen.",
"Wassermann":"Dein Deszendent im Wassermann zieht eigenwillige, unabhängige, unkonventionelle Menschen in dein Leben. Was dich an ihnen reizt, ist oft deine eigene unterdrückte Freiheit und Eigenart. Du überlässt anderen das Anderssein, das du dir selbst nicht erlaubst. Heute zeigt sich das, wenn du Menschen bewunderst, die sich nicht anpassen, und dich selbst einfügst. Deine Aufgabe ist es, deine eigene Eigenart offen zu leben.",
"Fische":"Dein Deszendent in den Fischen zieht sensible, hingebungsvolle, weiche Menschen in dein Leben. Was dich an ihnen reizt oder erschöpft, ist oft deine eigene verdrängte Sehnsucht und Empfindsamkeit. Du überlässt anderen das tiefe Fühlen und Mitschwingen. Heute zeigt sich das, wenn dich ihre Weichheit anzieht und gleichzeitig überfordert. Deine Aufgabe ist es, deine eigene Weichheit zuzulassen, ohne dich darin zu verlieren.",
}

readings["ic"] = {
"Widder":"Dein IC im Widder wurzelt in einem Zuhause, in dem du früh für dich selbst kämpfen musstest. Geborgenheit hieß bei dir, stark und selbstständig zu sein und niemandem zur Last zu fallen. Heute zeigt sich dieser Schatten, wenn du auch im Privaten nicht zur Ruhe kommst und keine Hilfe annimmst, weil du gelernt hast, alles allein zu stemmen. Tief in dir sitzt die Unruhe, dass du dich erst beweisen musst, bevor du dich ausruhen darfst. Deine Wurzelkraft ist die Frau, die sich selbst Halt gibt, ohne sich zu verhärten. Du darfst lernen, dass du auch im Stillstand sicher bist und dich anlehnen darfst.",
"Stier":"Dein IC im Stier wurzelt in der Sehnsucht nach Sicherheit und Beständigkeit, die in deiner Kindheit vielleicht gewackelt hat. Geborgenheit war an Materielles und an Verlässlichkeit geknüpft. Heute zeigt sich dieser Schatten, wenn du dich an Vertrautes klammerst und Veränderung im Innersten als Bedrohung erlebst, auch in deinem Business, wo du lieber am Sicheren festhältst. Tief sitzt die Angst, den Boden unter den Füßen zu verlieren. Deine Wurzelkraft ist eine innere Ruhe, die kein Außen erschüttern kann. Du darfst lernen, deine Sicherheit in dir zu verankern, nicht in dem, was du besitzt.",
"Zwillinge":"Dein IC in den Zwillingen wurzelt in einem Zuhause voller Worte, Reize und vielleicht wechselnder Stimmungen. Geborgenheit hieß, mitzudenken, zu vermitteln und die Atmosphäre zu lesen. Heute zeigt sich dieser Schatten, wenn du selbst im Privaten nicht abschaltest und Gefühle sofort zerredest, statt sie zu fühlen. Tief sitzt eine Unruhe, die nie ganz ankommt. Deine Wurzelkraft ist ein Geist, der sich selbst beruhigen kann. Du darfst lernen, in der Stille zu Hause zu sein und nicht nur im Reden.",
"Krebs":"Dein IC im Krebs wurzelt tief im Thema Familie, Mutter und Zugehörigkeit. Hier sitzt deine emotionale Grundprägung und das Bedürfnis nach einem Nest. Heute zeigt sich dieser Schatten, wenn du dich um alle kümmerst und deine eigene Bedürftigkeit versteckst, oder wenn alte Familienmuster dich im Privaten und im Business unbewusst steuern. Tief sitzt die Frage, ob du wirklich gehalten wirst. Deine Wurzelkraft ist die Fähigkeit, dir selbst ein Zuhause zu sein. Du darfst lernen, dich selbst zu nähren, so wie du andere nährst.",
"Löwe":"Dein IC im Löwen wurzelt in einem Zuhause, in dem Liebe vielleicht an Sichtbarkeit oder Leistung geknüpft war. Geborgenheit hieß, gesehen und besonders zu sein. Heute zeigt sich dieser Schatten, wenn du dich auch im Innersten beweisen musst und dich nur dann sicher fühlst, wenn du strahlst. Tief sitzt die Angst, ohne Glanz nicht zu genügen. Deine Wurzelkraft ist ein Herz, das aus sich selbst leuchtet. Du darfst lernen, dass du geliebt bist, auch ohne Bühne, auch ganz privat und leise.",
"Jungfrau":"Dein IC in der Jungfrau wurzelt in einem Zuhause, in dem Ordnung, Korrektheit oder Funktionieren wichtiger waren als Gefühl. Geborgenheit war, alles richtig zu machen. Heute zeigt sich dieser Schatten, wenn du dich selbst im Privaten bewertest und nie ganz loslassen kannst, weil ein innerer Kritiker mitläuft. Tief sitzt das Gefühl, erst genügen zu müssen, bevor du ruhen darfst. Deine Wurzelkraft ist eine ruhige, fürsorgliche Genauigkeit dir selbst gegenüber. Du darfst lernen, dich anzunehmen, auch ungeordnet und unfertig.",
"Waage":"Dein IC in der Waage wurzelt in einem Zuhause, in dem Frieden und Harmonie über allem standen. Geborgenheit hieß, keinen Streit zu machen und sich anzupassen. Heute zeigt sich dieser Schatten, wenn du auch im Innersten den Konflikt scheust und deine Wahrheit schluckst, um die Beziehung zu halten. Tief sitzt die Angst, dass deine Bedürfnisse den Frieden stören. Deine Wurzelkraft ist ein inneres Gleichgewicht, das nicht vom Außen abhängt. Du darfst lernen, ehrlich zu sein und dich trotzdem sicher zu fühlen.",
"Skorpion":"Dein IC im Skorpion wurzelt in einem Zuhause mit Tiefe, vielleicht auch mit Unausgesprochenem, Kontrolle oder verborgenen Spannungen. Geborgenheit war selten ganz offen. Heute zeigt sich dieser Schatten, wenn du selbst im Privaten niemanden ganz reinlässt und deine tiefsten Gefühle für dich behältst. Tief sitzt die frühe Erfahrung, dass Vertrauen gefährlich ist. Deine Wurzelkraft ist eine seelische Tiefe, die heilen kann. Du darfst lernen, dich an einem sicheren Ort wirklich zu zeigen, mit allem, was in dir ist.",
"Schütze":"Dein IC im Schützen wurzelt in einem Zuhause, das vielleicht von Suche, Weite oder fehlender Verwurzelung geprägt war. Geborgenheit war an Sinn oder Freiheit geknüpft, nicht an einen festen Ort. Heute zeigt sich dieser Schatten, wenn du dich im Innersten ruhelos fühlst und immer weiterziehst, statt anzukommen. Tief sitzt die Frage, wo du wirklich hingehörst. Deine Wurzelkraft ist ein inneres Zuhause, das du überallhin mitnimmst. Du darfst lernen, in dir selbst anzukommen, statt im nächsten Horizont.",
"Steinbock":"Dein IC im Steinbock wurzelt in einem Zuhause, in dem Pflicht, Ernst oder Leistung mehr Raum hatten als Wärme. Geborgenheit musstest du dir verdienen. Heute zeigt sich dieser Schatten, wenn du auch im Privaten funktionierst, dich hart führst und dir keine Schwäche erlaubst. Tief sitzt das Gefühl, dass Liebe an Tüchtigkeit hängt. Deine Wurzelkraft ist eine ruhige innere Autorität, die dich trägt. Du darfst lernen, dass du Wärme nicht verdienen musst, du darfst sie dir einfach geben.",
"Wassermann":"Dein IC im Wassermann wurzelt in einem Zuhause, das vielleicht anders, unkonventionell oder emotional distanziert war. Geborgenheit hieß, eigenständig und vernünftig zu sein. Heute zeigt sich dieser Schatten, wenn du dich selbst im Innersten von deinen Gefühlen abkoppelst und Nähe auf Abstand hältst. Tief sitzt das Gefühl, irgendwie nicht ganz dazuzugehören. Deine Wurzelkraft ist eine Freiheit, die trotzdem Bindung zulässt. Du darfst lernen, nah zu sein und dabei du selbst zu bleiben.",
"Fische":"Dein IC in den Fischen wurzelt in einem Zuhause voller Gefühl und Durchlässigkeit, vielleicht auch mit Auflösung oder fehlenden Grenzen. Geborgenheit war diffus, manchmal verschwommen. Heute zeigt sich dieser Schatten, wenn du im Innersten die Stimmungen aller aufnimmst und deine eigene Mitte verlierst, oder dich zurückziehst, wenn es zu viel wird. Tief sitzt die Sehnsucht nach einem Ort, der dich hält. Deine Wurzelkraft ist eine tiefe spirituelle Verbindung. Du darfst lernen, dich zu erden und dir selbst Grenzen zu geben, die dich schützen.",
}

for k,v in readings.items():
    missing = [s for s in SIGNS if s not in v]
    assert not missing, f"{k} fehlt: {missing}"

planetIntros = {
"lilith":"Lilith ist deine wilde, kompromisslose Kraft. Der Teil von dir, der sich nie unterworfen hat und den du weggesperrt hast, um dazuzugehören. Sie meldet sich genau dann, wenn du wächst und sichtbar wirst.",
"saturn":"Saturn ist deine tiefste Angst, nicht zu genügen. Sie kommt nicht nur aus deiner Kindheit, sie steuert dich heute über Leistung, Kontrolle und Rückzug.",
"pluto":"Pluto zeigt, wo du um Macht und Kontrolle ringst. Hier liegt deine Angst vor Kontrollverlust und gleichzeitig deine größte Kraft, dich zu verwandeln.",
"chiron":"Chiron ist deine Urwunde. Die Verletzung, die immer noch zieht, wenn das Leben sie heute berührt, und genau hier wirst du zur Heilerin für andere.",
"mond":"Der Mond ist dein inneres Kind und dein emotionaler Schatten. Das Bedürfnis, das du dir selbst nicht eingestehst und das dich heute leise steuert.",
"ic":"Der IC ist deine tiefste Wurzel. Dein Zuhause, deine Herkunft, die emotionale Prägung aus deiner Kindheit, und der private Teil von dir, den nur die Nächsten sehen.",
"mars":"Mars ist deine rohe Kraft. Deine Wut, dein Wollen, deine Durchsetzung, und der Teil davon, den du dir verbietest, bis er sich anders Bahn bricht.",
"suedknoten":"Der Südknoten ist deine alte Komfortzone. Das vertraute Muster, in das du heute noch zurückfällst, sobald es schwierig wird.",
"deszendent":"Der Deszendent zeigt, was du auf andere projizierst. Was dich an anderen am meisten triggert, ist oft dein eigener Schatten, von außen betrachtet.",
}

shadowQuestions = {
"lilith":"An welcher Stelle in deinem Leben machst du dich gerade kleiner, als du bist, um dazuzugehören?",
"saturn":"Wo treibst du dich gerade an, weil du tief glaubst, ohne diese Leistung nicht zu genügen?",
"pluto":"Woran hältst du gerade fest, obwohl du längst spürst, dass es vorbei ist?",
"chiron":"In welcher Situation in deinem jetzigen Leben fühlst du dich immer wieder wie das verletzte Kind von damals?",
"mond":"Welches Bedürfnis erfüllst du dir gerade nicht und wartest darauf, dass jemand anderes es tut?",
"ic":"Welches Muster aus deinem Elternhaus trägst du heute noch in dir, ohne es zu wollen?",
"mars":"Was willst du gerade wirklich, traust dich aber nicht, es laut auszusprechen?",
"suedknoten":"In welches alte Muster fällst du gerade zurück, sobald der Druck steigt?",
"deszendent":"Wer triggert dich gerade am stärksten, und welche Eigenschaft an dieser Person trägst du selbst in dir?",
}

shadowHouse = {
1:{"name":"1. Haus","theme":"Auftreten und Selbstbild","description":"Im ersten Haus wirkt dieser Schatten direkt in deinem Auftreten und deinem Selbstbild. Er entscheidet mit, wie du dich zeigst und wo du eine Maske trägst, sobald du den Raum betrittst."},
2:{"name":"2. Haus","theme":"Selbstwert und Besitz","description":"Im zweiten Haus wirkt dieser Schatten in deinem Selbstwert und deinem Umgang mit Geld. Hier sitzt oft die Angst, ohne Besitz oder Leistung wertlos zu sein, und genau hier machst du dich beim Fordern klein."},
3:{"name":"3. Haus","theme":"Denken und Sprechen","description":"Im dritten Haus wirkt dieser Schatten in deinem Denken und Sprechen. Hier hältst du zurück, was du eigentlich sagen willst, weil eine Stimme in dir früh gelernt hat zu schweigen."},
4:{"name":"4. Haus","theme":"Wurzeln und Innenwelt","description":"Im vierten Haus wirkt dieser Schatten in deinen Wurzeln und in deinem Innersten. Hier liegt die Prägung aus deiner Herkunft, die du heute unbewusst in jede Beziehung und jeden Raum mitnimmst."},
5:{"name":"5. Haus","theme":"Kreativität und Liebe","description":"Im fünften Haus wirkt dieser Schatten in deiner Kreativität, deiner Freude und deiner Art zu lieben. Hier verbirgt sich die Angst, dich zu zeigen, und genau hier hältst du dein Strahlen zurück."},
6:{"name":"6. Haus","theme":"Alltag und Körper","description":"Im sechsten Haus wirkt dieser Schatten in deinem Alltag, deiner Arbeit und deinem Körper. Hier zeigt er sich als Selbstkritik und Überfunktion, als ständiges Machen, das nie zur Ruhe kommt."},
7:{"name":"7. Haus","theme":"Beziehungen","description":"Im siebten Haus wirkt dieser Schatten in deinen engen Beziehungen. Hier begegnet dir im anderen genau der Teil von dir, den du selbst nicht annimmst, und deine Trigger werden zu deinen Lehrern."},
8:{"name":"8. Haus","theme":"Macht und Tiefe","description":"Im achten Haus wirkt dieser Schatten in dem, was du verbirgst: Macht, Sexualität, Geld und tiefe Bindung. Hier liegt dein größtes Tabu und gleichzeitig deine stärkste Kraft, dich zu verwandeln."},
9:{"name":"9. Haus","theme":"Glaube und Wahrheit","description":"Im neunten Haus wirkt dieser Schatten in deinem Glauben und deiner Wahrheit. Hier hältst du an Überzeugungen fest, die dich klein halten, und nennst sie Realität."},
10:{"name":"10. Haus","theme":"Berufung und Sichtbarkeit","description":"Im zehnten Haus wirkt dieser Schatten in deiner Berufung und deinem öffentlichen Bild. Hier sitzt die Angst, zu versagen oder nicht zu genügen, genau dort, wo du sichtbar wirst."},
11:{"name":"11. Haus","theme":"Zugehörigkeit und Visionen","description":"Im elften Haus wirkt dieser Schatten in deiner Zugehörigkeit und deinen Visionen. Hier passt du dich an, um dazuzugehören, aus alter Angst, ausgeschlossen zu sein."},
12:{"name":"12. Haus","theme":"Das Verborgene","description":"Im zwölften Haus wirkt dieser Schatten im Verborgenen, im Unbewussten. Hier liegt das, was du noch nicht einmal vor dir selbst zugibst, deine leiseste Selbstsabotage und dein größter blinder Fleck."},
}

def jd(o): return json.dumps(o, ensure_ascii=False)

planets_js = (
"const planets = [\n"
'  { key: "lilith",     icon: "⚸",  name: "Lilith" },\n'
'  { key: "saturn",     icon: "♄",  name: "Saturn" },\n'
'  { key: "pluto",      icon: "♇",  name: "Pluto" },\n'
'  { key: "chiron",     icon: "⚷",  name: "Chiron" },\n'
'  { key: "mond",       icon: "🌙", name: "Mond" },\n'
'  { key: "ic",         icon: "⌂",  name: "IC" },\n'
'  { key: "mars",       icon: "♂️", name: "Mars" },\n'
'  { key: "suedknoten", icon: "☋",  name: "Südknoten" },\n'
'  { key: "deszendent", icon: "⬇️", name: "Deszendent" }\n'
"];"
)

house_js = "const houseThemes = {\n" + ",\n".join(
    f"  {n}: {jd(shadowHouse[n])}" for n in range(1,13)
) + "\n};"

readings_order = ["lilith","saturn","pluto","chiron","mond","ic","mars","suedknoten","deszendent"]
readings_js = "const readings = {\n" + ",\n".join(
    f"  {k}: {jd(readings[k])}" for k in readings_order
) + "\n};"

intros_js = "const planetIntros = " + jd(planetIntros) + ";"
questions_js = "const shadowQuestions = " + jd(shadowQuestions) + ";"

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

      // Schattenpunkte -> window.__chart
      const chart = {
        lilith:     { sign: dsign(CP.lilith),    house: dhouse(CP.lilith) },
        saturn:     { sign: dsign(CB.saturn),    house: dhouse(CB.saturn) },
        pluto:      { sign: dsign(CB.pluto),     house: dhouse(CB.pluto) },
        chiron:     { sign: dsign(CB.chiron),    house: dhouse(CB.chiron) },
        mond:       { sign: dsign(CB.moon),      house: dhouse(CB.moon) },
        ic:         { sign: OPP[mcSign] || '',   house: '' },
        mars:       { sign: dsign(CB.mars),      house: dhouse(CB.mars) },
        suedknoten: { sign: dsign(CP.southnode), house: dhouse(CP.southnode) },
        deszendent: { sign: OPP[acSign] || '',   house: '' }
      };'''
sub_str(old_chart, new_chart, 1)

sub_str(
'let html = `<div class="results-header"><h2>Das Horoskop von ${name}</h2><p>Gelesen aus den Mustern deiner Geburtsenergie</p></div>`;',
'let html = `<div class="results-header"><h2>Dein Schatten-Reading, ${name}</h2><p>Gelesen aus den dunklen Schichten deines Charts</p></div>`;',
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
        ${shadowQuestions[p.key] ? `<div class="shadow-question"><span class="sq-label">Deine Schattenfrage</span>${shadowQuestions[p.key]}</div>` : ''}
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
      <h3>Dein Weg durch den Schatten</h3>
      <p>Dein Schatten ist nicht nur das Kind von damals. Er ist auch die Frau, die du heute bist, in deinem Business, in deinen Beziehungen, in deinem Geld.</p>
    </div>`;'''
sub_str(old_el, new_el, 1)

old_cta = '''  html += `
  <div class="cta-block">
    <h3>Dein AstroCode. Entschlüssle deine Identität.</h3>
    <p>Du hast gerade die erste Schicht deines astrologischen Blueprint berührt. Wer bin ich? ist die tiefste aller Fragen. Dieses Reading gibt dir einen ersten Blick. Im AstroCode blickst du tiefer. Du erkennst nicht nur, wer du bist. Du wirst es. Du bewegst dich zu der Frau, die du in dir trägst. Du führst dein Business, deine Beziehungen und dein Leben aus deiner tiefsten Identität heraus.</p>
    <p style="margin-top:20px; padding-top:18px; border-top: 1px solid rgba(201,169,110,0.2);">Speicher dir am besten dein Geburtshoroskop ab. Die nächsten Tage schicke ich dir noch weitere Impulse mit den passenden Prompts. Ich möchte Astrologie mit modernen Tools so praxisnah in dein Leben bringen, wie es heute möglich ist. Bewegte Astrologie hat mein ganzes Leben verändert. Dank der Möglichkeiten der KI können wir heute so viel tiefer ins Experiment Identität eintauchen.</p>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Zum AstroCode &rarr;</a>
  </div>`;'''
new_cta = ''  # CTA-Block komplett entfernt
sub_str(old_cta, new_cta, 1)

sub_str('<title>Astrologischer Selbst-Check</title>', '<title>Dein Schatten-Check</title>', 1)

old_head = '''    <p class="header-eyebrow">Dein kosmischer Spiegel</p>
    <h1>Dein AstroCheck</h1>
    <p class="subtitle">Entdecke, welche Energien du in dir trägst und wer du wirklich bist.</p>'''
new_head = '''    <p class="header-eyebrow">Emotioncode</p>
    <h1>Dein Schatten-Check</h1>
    <p class="subtitle">Begegne dem, was du nie sehen wolltest. Deine Chart ist der Spiegel.</p>'''
sub_str(old_head, new_head, 1)

sub_str(
'    <p><strong>Gib deine Geburtsdaten ein.</strong></p>',
'    <p><strong>Gib deine Geburtsdaten ein.</strong></p>',
1)

sub_str('>Mein astrologisches Reading anzeigen</button>', '>Mein Schatten-Reading anzeigen</button>', 1)
sub_str("btn.textContent = 'Berechne dein Horoskop…';", "btn.textContent = 'Berechne deinen Schatten…';", 1)
sub_str(
'<div class="error-msg" id="errorMsg">Bitte wähle mindestens ein Zeichen aus, um dein Reading zu erhalten.</div>',
'<div class="error-msg" id="errorMsg">Bitte gib deine Geburtsdaten ein, um dein Schatten-Reading zu erhalten.</div>',
1)

extra_css = '''<style>
.shadow-question{ margin-top:18px; padding:16px 18px; border-left:3px solid #C9A96E; background:rgba(201,169,110,0.08); border-radius:8px; font-style:italic; color:#E8D5B0; }
.shadow-question .sq-label{ display:block; font-style:normal; font-size:0.72rem; letter-spacing:0.14em; text-transform:uppercase; color:#C9A96E; margin-bottom:6px; }
</style>
</head>'''
sub_str('</head>', extra_css, 1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

os.makedirs("schatten-check-netlify", exist_ok=True)
with open(os.path.join("schatten-check-netlify","index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK  {SRC} ({orig_len} B) -> {OUT} ({len(html)} B)")
print("    + schatten-check-netlify/index.html")
