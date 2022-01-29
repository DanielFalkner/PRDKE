# PRDKE
Python 3.8 und pip sind benötigt um das Projekt in Linux zu starten. Empfohlen ist die IDE Pycharm.

Im Terminal folgende Zeile eingeben
```
flask run
```
Sollten Errors auftreten (bei manchen Versuchen waren Errors, bei manchen keine), fehlen normalerweise bestimmte Module welche installiert werden müssen.
In Pycharm muss man rechts unten auf Python 3.9(andere Vers. auch möglich) >> Interpreter Settings >> + >> 'Name des fehlenden Moduls' (in Error beschrieben) in Suchleiste eingeben.
Normalerweise treten Probleme nur bei Flask Marshmallow und WTForms SQLAlchemy auf. Sollten andere Module als fehlend angezeigt werden, müssen diese ebenfalls installiert werden.
