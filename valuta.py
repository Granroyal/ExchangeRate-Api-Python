import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Pege på .env filen i projektmappen
ENV_FILE = Path(".env")


def save_key(key: str) -> None:
    """
    Gemmer API-nøglen i .env filen.
    Overskriver filen hvis den allerede findes.
    """
    ENV_FILE.write_text(f"API_KEY={key}\n", encoding="utf-8")
    print("API key gemt i .env")


def load_key() -> str | None:
    """
    Indlæser API-nøglen fra .env.
    Returnerer None hvis filen ikke findes.
    """
    if not ENV_FILE.exists():
        return None

    load_dotenv()  # Læser variabler fra .env ind i miljøet
    return os.getenv("API_KEY")


def parse_amount(text: str) -> float:
    """
    Konverterer brugerens input til float.
    Accepterer både punktum og komma som decimaltegn.
    """
    return float(text.strip().replace(",", "."))


def normalize_currency(text: str) -> str:
    """
    Normaliserer valuta-input.
    Gør input uppercase og mapper fx 'Euro' -> 'EUR'.
    """
    t = text.strip().upper()

    aliases = {
        "EURO": "EUR",
        "KR": "DKK",
        "KR.": "DKK",
        "KRONER": "DKK",
        "DANSKEKRONER": "DKK",
        "DANISHKRONER": "DKK",
        "DOLLAR": "USD",
    }

    # Hvis ikke fundet i alias, returneres værdien som den er
    return aliases.get(t, t)


def fetch_rates(api_key: str, base: str) -> dict:
    """
    Henter valutakurser fra ExchangeRate-API (v6).
    Returnerer dictionary med conversion_rates.
    """
    base = normalize_currency(base)

    # Bygger API URL
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"

    # Sender HTTP GET request
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    data = r.json()

    # Tjekker om API kaldet lykkedes
    if data.get("result") != "success":
        raise RuntimeError(data.get("error-type", "API fejl"))

    return data["conversion_rates"]


def build_parser() -> argparse.ArgumentParser:
    """
    Opretter og konfigurerer argparse CLI parseren.
    """
    parser = argparse.ArgumentParser(
        prog="valuta",
        description="Valuta CLI til omregning",
    )

    # Optional argument til at gemme API key
    parser.add_argument("--key", help="Gem API nøgle i .env")

    # Positional arguments til konvertering
    parser.add_argument("amount", nargs="?", help="Beløb, fx 1234,5")
    parser.add_argument("from_currency", nargs="?", help="Fra valuta, fx EUR eller Euro")
    parser.add_argument("to_currency", nargs="?", help="Til valuta, fx DKK")

    return parser


def main() -> int:
    """
    Programmets entry point.
    Håndterer CLI input og styrer programflow.
    """
    parser = build_parser()
    args = parser.parse_args()

    # 1) Hvis --key bruges, gem nøglen og afslut
    if args.key:
        save_key(args.key)
        return 0

    # 2) Ellers hent API key fra .env
    api_key = load_key()
    if not api_key:
        parser.exit(1, "Ingen API key fundet. Brug: python3 valuta.py --key DINKEY\n")

    # 3) Tjek at nødvendige argumenter er angivet
    if args.amount is None or args.from_currency is None or args.to_currency is None:
        parser.exit(2, "Brug: python3 valuta.py <amount> <FROM> <TO>\n")

    # 4) Konverter beløbet til float
    try:
        amount = parse_amount(args.amount)
    except ValueError:
        parser.exit(2, f"Ugyldigt beløb: {args.amount}\n")

    # 5) Normaliser valuta input
    from_cur = normalize_currency(args.from_currency)
    to_cur = normalize_currency(args.to_currency)

    # 6) Hent valutakurser fra API
    try:
        rates = fetch_rates(api_key, from_cur)
    except Exception as e:
        parser.exit(1, f"Kunne ikke hente kurser: {e}\n")

    # 7) Tjek om target valuta findes
    if to_cur not in rates:
        parser.exit(2, f"Ukendt valuta: {to_cur}\n")

    # 8) Udfør selve konverteringen
    converted = amount * float(rates[to_cur])

    # 9) Udskriv resultat
    print(f"{amount:.2f} {from_cur} = {converted:.2f} {to_cur}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())