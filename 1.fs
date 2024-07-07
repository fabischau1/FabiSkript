say "Willkommen zum einfachen Beispiel in FabiSkript!"

/ui name Bitte gib deinen Namen ein: 

say "Hallo," $name "!"

wait 2

set filename example.txt
write $filename "Dies ist ein Beispieltext für FabiSkript."

read $filename file_content

say "Dateiinhalt:" $file_content

say "Das Beispiel ist beendet. Auf Wiedersehen!"
