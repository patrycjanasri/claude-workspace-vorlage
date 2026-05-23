#!/bin/bash

VIDEO="videos/raw/Emotioncode2.mp4"
OUT="videos/clips"

echo "Starte Schnitt — 15 Clips..."

ffmpeg -ss 00:11:20 -to 00:11:33 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip01-du-fragst-nicht-um-erlaubnis.mp4" -y
echo "✓ Clip 01 — Du fragst nicht um Erlaubnis"

ffmpeg -ss 00:48:37 -to 00:48:56 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip02-es-gibt-immer-wege.mp4" -y
echo "✓ Clip 02 — Es gibt immer Wege"

ffmpeg -ss 00:16:28 -to 00:16:48 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip03-fuer-2-leute-kein-teamcall.mp4" -y
echo "✓ Clip 03 — Für 2 Leute kein Teamcall"

ffmpeg -ss 00:50:07 -to 00:50:26 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip04-imperium-beginnt-nicht-mit-million.mp4" -y
echo "✓ Clip 04 — Imperium beginnt nicht mit einer Million"

ffmpeg -ss 00:46:23 -to 00:46:48 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip05-ich-bin-gern-faenchen-im-wind.mp4" -y
echo "✓ Clip 05 — Ich bin gern ein Fähnchen im Wind"

ffmpeg -ss 00:44:22 -to 00:45:12 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip06-der-otto-macht-es-einfach.mp4" -y
echo "✓ Clip 06 — Der Otto macht es einfach"

ffmpeg -ss 00:54:50 -to 00:55:20 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip07-bauchgefuehl-ist-serotonin.mp4" -y
echo "✓ Clip 07 — Bauchgefühl ist Serotonin"

ffmpeg -ss 00:52:21 -to 00:54:01 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip08-serotonin-90-prozent-darm.mp4" -y
echo "✓ Clip 08 — Serotonin 90% im Darm"

ffmpeg -ss 00:05:11 -to 00:05:48 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip09-fokus-und-dopamin.mp4" -y
echo "✓ Clip 09 — Fokus und Dopamin"

ffmpeg -ss 00:35:48 -to 00:36:11 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip10-emotion-energie-in-bewegung.mp4" -y
echo "✓ Clip 10 — Emotion = Energie in Bewegung"

ffmpeg -ss 00:09:58 -to 00:11:33 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip11-ich-bin-immer-zu-viel.mp4" -y
echo "✓ Clip 11 — Ich bin immer zu viel"

ffmpeg -ss 00:14:23 -to 00:14:57 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip12-dankesbrief-einer-fremden.mp4" -y
echo "✓ Clip 12 — Dankesbrief einer Fremden"

ffmpeg -ss 00:06:52 -to 00:07:14 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip13-wer-schreibt-der-bleibt.mp4" -y
echo "✓ Clip 13 — Wer schreibt der bleibt"

ffmpeg -ss 00:35:48 -to 00:36:21 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip14-ich-wollte-nicht-launchen.mp4" -y
echo "✓ Clip 14 — Ich wollte das nicht launchen"

ffmpeg -ss 00:20:13 -to 00:20:38 -i "$VIDEO" -c:v libx264 -c:a aac "$OUT/clip15-wann-hast-du-wirklich-gelebt.mp4" -y
echo "✓ Clip 15 — Wann hast du wirklich gelebt"

echo ""
echo "Fertig! Alle Clips in videos/clips/ gespeichert."
