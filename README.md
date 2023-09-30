# OMRON 2JCIE-BU01

I juni 2023 fikk jeg et oppdrag av Robotek AS. 

Robotek AS har et stort prosjekt på gang hvor idéen er at industribåter lett kan benytte 3D-printere ombord til å printe reservedeler ved behov. Problemet er at store bølger og hardt føre kan gjøre at det er uforsvarlig å printe en reservedel. Min spesifikke oppgave var å utvikle en løsning som enkelt tillot mannskapet å vurdere tryggheten ved å starte en 3D-print. Forslaget til Robotek AS var at en sensor skulle benyttes, som skulle lyse grønt dersom det var trygt til å starte en 3D-print, og rødt hvis ikke. Alt jeg hadde å gå på var at det eksisterte en sensor, Omron 2JCIE-BU01, som hadde et led-lys og en laaaaang manual: [https://www.tme.eu/Document/9169aa37b81b2fce9aa97921bab1ba98/2JCIE-BU01-DTE.pdf](https://www.tme.eu/Document/9169aa37b81b2fce9aa97921bab1ba98/2JCIE-BU01-DTE.pdf)

Omron 2JCIE-BU01 registrerer mye data slik som temperatur, lyd og trykk. Men det mest interessante den registrerer er vinkel/bevegelse i alle retninger! Om for eksempel sensoren opplever en helning på 45°, er det mulig å hente dette ut ved å aksessere rett minneadresse.

Dermed var tanken dette:

For hvert sekund henter jeg ut vinkel til sensoren i alle retninger. Dermed sammenligner jeg med data fra det forrige sekundet, og ser om økningen i vinkel er stor. Om den er stor nok skal sensoren lyse rødt, om den er innafor grenseområdet lyser den grønt. På denne måten kan jeg indirekte finne ut om det er store bølger eller ikke! I tillegg er det viktig å sette en maksgrense for helning, for eksempel 30°.

Etter å ha lagt en plan var det bare å sette igang med å skjønne hvordan data kan hentes, hvordan jeg bør tolke den og hvordan få sensoren til å lyse rødt eller grønt. Heldigvis for meg finnes det allerede et bibliotek for å lese og skrive data fra Omron 2JCIE-BU01 - [https://github.com/nobrin/omron-2jcie-bu01](https://github.com/nobrin/omron-2jcie-bu01). Dessverre var den ikke helt komplett, det var noen minneaksesser som ikke var inkludert som jeg trengte, og dermed endret jeg på dette og lagde mitt eget bibliotek, [omron_2jcie_bu01_interact](https://pypi.org/project/omron-2jcie-bu01-interact/). Du vil se i **interface.py** at denne biblioteket blir importert, og brukt.

Herifra var det bare å kode i vei!

Mitt arbeid bidro vesentlig til å etablere en sikker og effektiv metode for mannskapet ombord til å benytte 3D-printingsteknologi.

## Bygging

Vi trenger biblioteket **omron_2jcie_bu01_interact** for å kunne kjøre applikasjonen. Last ned biblioteket med `pip install omron-2jcie-bu01-interact` i terminalen.
Det er mulig andre biblioteker også trengs, slik som **tkinter**, **pillow** osv.

## Kjøring av applikasjonen

**MERK: APPLIKASJONEN VIL KUN KJØRE DERSOM DU HAR PLUGGET INN EN OMRON 2JCIE-BU01 SENSOR I USB-PORT.**

For å kjøre applikasjonen er det bare å kjøre filen **interface.py**.

Dersom du ønsker å opprette en .exe fil av prosjektet, kan du laste ned PyInstaller og kjøre kommandoen `pyinstaller interface.py --onefile --i icon.ico --windowed`. Dette vil opprette en **dist**-mappe, med en .exe fil inni