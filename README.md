# Valuta CLI
Et Command Line Interface (CLI) program til valutaomregning.
Programmet bruger https://www.exchangerate-api.com/ til at hente aktuelle valutakurser

Første gang programmet køres, gemmes din API key. Den gemmes lokalt i en `.env` fil.

---

## Krav
 - Python 3 installeret
 - En API key fra https://www.exchangerate-api.com/

 ---

 # Sådan kommer du igang

 ## Klon Projektet fra GitHub
 git clone (https://github.com/Granroyal/ExchangeRate-Api-Python.git)
 cd valuta-cli

* macOS/Linux

 Opret miljø:
 python3 -m venv .venv

 Aktivér miljø:
 source .venv/bin/activate

* Windows (PowerShell)
Opret miljø:
 python -m venv .venv

 Aktivér miljø:
 .venv\bin\Activate

 Når miljøet er aktivt, vil du se (.venv) i terminalen.

 Installér dependencies:
 pip install -r requirements.txt

```bash
 Api bliver gemt først gang
 python3 valuta.py --key DIN_API_KEY
 Dette opretter en .env fil i projektmappen.

 ## Brug Programmet
 python3 valuta.py <amount> <FROM> <TO>

Eksempler:

```bash
 python3 valuta.py 100 EUR DKK
 python3 valuta.py 600 euro dkk
 python3 valuta.py 1234,5 USD eur

 Programmet accepterer både store og små bogstaver.

## Deaktivér virtual environment
deactivate