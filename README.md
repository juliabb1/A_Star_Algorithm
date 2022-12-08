# KI-2022-_Suchverfahren_A*
 
 ## Aufgabenstellung: Wegsuche im Gelände

_Einzusetzende Methode: Suchverfahren A*_ <br>

Es gilt den Weg durch ein labyrinthartiges Gebiet zu finden. Die Landschaft ist von Felswänden, Flüssen, Waldgebieten und Ebenen, sowie teils präparierten Wegen geprägt. Start und Ziel sind bekannt. 
Nun soll der günstigste Weg gefunden werden. Eine in Planquadrate aufgeteilte Karte des Gebietes 
liegt vor, diese kennt zwar keine Weglängen, kann jedoch Entfernungen durch die Planquadrate einschätzen. Die Spielfigur, die den Weg durchlaufen soll, verfügt über ein Schlauchboot mit dem sie einen 
Fluss überqueren kann. Dies geht jedoch nur einmal, da das Boot dann am Fluss zurückbleiben muss.
Ist sie im Boot, kann sie jedoch entlang des Flusses weiterfahren. Sobald sie aussteigt ist das Boot 
nicht mehr nutzbar.

Solange das Boot getragen wird sind Felswände unüberwindbar. Zur Vereinfachung: jedes Planquadrat 
wird als ein Schritt angesehen. Jedem Planquadrat ist genau eine Landschaftsform zugeordnet. Jeder 
Landschaftsform sind Kosten zugewiesen, die z.B. einen Zeitverbrauch bei der Durchquerung (berechnet beim Verlassen) darstellen. Planquadrate werden nicht diagonal durchlaufen.

## Eingangsdaten:
- Matrix mit Beschreibung des Gebietes
- Kostentabelle für die oben genannten Landschaftsformen
- Start- und Zielposition

## Aufgabe:
- Software entwickeln
- Eingabe einer Datei mit Testdaten ermöglichen
- Ausgabe des bestgeeignetsten Weges, bestimmt mit Hilfe des A* Algorithmus 
- Duskussion der Konfiguration und des Ergebnisses

## Programmiersprache:
- Python
