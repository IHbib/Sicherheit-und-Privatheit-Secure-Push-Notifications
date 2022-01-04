# Sicherheit und Privatheit von Push-Notification-Services für mobile Apps

## Grundlagen von unsicheren Push Notifications
x

## Erklärung von Firebase/"Apple"
x

## Grundlagen von sicheren Push Notifications (Schlüssel Austausch)
Wenn eine Benachrichtigung eines App-Anbieters über einen Messaging Dienst wie FCM zum Endgerät gelangen soll, ist die Kommunikation zwischen Entwickler und Messaging Dienst, sowie die Kommunikation zwischen Messaging Dienst und Endgerät durch TLS verschlüsselt [1][2], jedoch wird der eigentliche Inhalt der Benachrichtigungen in Klartext übermittelt [1][2]. So handelt es sich dabei nicht um eine Ende-zu-Ende Verschlüsselung und der Inhalt der Nachricht kann von beispielsweise Google mitgelesen werden.

Bedenklich ist die Tatsache, dass alle Benachrichtigung recht einfach einer Person zugeordnet werden können und die Anbieter dieser Messaging Dienste meist US-amerikanische Firmen sind, welche beispielsweise Daten an Behörden weiterreichen müssten, falls gefordert [3].

Um den Inhalt von Push-Benachrichtigungen vor den Messaging Diensten zu schützen, muss der App-Anbieter sich also selbst um eine Ende-zu-Ende-Verschlüsselung kümmern.

Dies kann besonders wichtig sein, wenn es sich um Benachrichtigungen handelt, welche sensible Personen Informationen enthalten. Wenn es sich um Benachrichtigungen von Instant Messaging Diensten handelt, oder vielleicht sensiblere Daten von Banking Apps oder vergleichbarem, ist eine Verschlüsselung der Inhalte besonders erstrebenswert.

Eine solche Ende-zu-Ende-Verschlüsselung lässt sich über eine asymmetrische Verschlüsselung recht gut realisieren, wobei das Endgerät das Schlüsselpaar erzeugt und den Öffentlichen Schlüssel an den Entwickler schickt und dabei den Messaging Dienst außen vor lässt. Dabei muss man nicht die Funktionsweise des Messaging Dienstes einschränken und kann vorhandene Technologien weiter nutzen.

[1] https://github.com/google/capillary#introduction

[2] https://medium.com/@BackmaskSWE/push-messages-isnt-secure-enough-69121c683cc

[3] https://transparencyreport.google.com/user-data/us-national-security?hl=de


## Beispiel eines sicheren Notification Flow

![Secure-Flow](https://miro.medium.com/max/980/1*BbTrPX0DCH-76GjDGcJcqQ.png)

1.	Der Anwender erzeugt auf seinem Endgerät automatisiert ein Schlüsselpaar, bestehend aus einem Öffentlichen und einem Privaten Schlüssel.
2.	Der Öffentliche Schlüssel wird dem Entwickler nun über einen direkten Kommunikationsweg übermittelt.
3.	Der Entwickler speichert nun diesen Schlüssel und verknüpft ihn Lokal mit dem Messaging Dienst Identifier für das spezifische Endgerät. Nun ist er in der Lage mit dem Öffentlichen Schlüssel seine Ausgehende Benachrichtigen zu verschlüsseln.
4.	Die Verschlüsselte Benachrichtigung wird nun dem Messaging Dienst übermittelt, welcher diese, für ihn unlesbare Nachricht, an das Endgerät übermittelt.
5.	Das Endgerät kann bei Erhalt der Benachrichtigung, durch seinen lokal gespeicherten Privaten Schlüssel den Inhalt entschlüsseln und die Benachrichtigung kann dem Nutzer angezeigt werden.

Quelle: https://medium.com/adobetech/securing-push-notifications-in-mobile-apps-a23b6c20139e


## Beispiele an fertigen Lösungen für sichere Notifications
Um sichere Benachrichtigungen zu versenden, gibt es bereits vorgefertigte Bibliotheken, auch Google selbst stellt mit dem Projekt Capillary solch eine Möglichkeit zur Verfügung [1]. 

Capillary erweitert den simplen Schlüsselaustausch noch um weitere Funktionen, wie zum Beispiel, dass ein gestohlenes Endgerät die Möglichkeit der Entschlüsselung noch eingehender Benachrichtigungen entzogen werden kann [2].

Die Popularität dieser Bibliothek scheint, gemessen anhand der ungefähr 450 Github Stars  Stand Dezember 2021, recht eingeschränkt. Der letzte Commit war im Dezember 2018, womit das Projekt recht verlassen ausschaut.

[1] https://github.com/google/capillary

[2] https://www.golem.de/news/project-capillary-google-verschluesselt-pushbenachrichtigungen-ende-zu-ende-1806-134808.html


## Umsetzung in Open Source Projekten
x

## Protoyp....