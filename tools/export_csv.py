"""Esporta tutte le righe degli scontrini (receipts/*.json) in receipts/righe.csv.

Una riga per voce di scontrino; serve come sorgente per il cruscotto spesa/prezzi.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RATES = {"A": 7, "B": 19}
COLS = ["scontrino_id", "data", "esercente", "citta", "articolo", "descrizione",
        "quantita", "unita", "prezzo_unitario", "unita_prezzo", "importo",
        "codice_iva", "aliquota_iva", "alimentare", "proteine_g"]

rows = []
for f in sorted((ROOT / "receipts").glob("*.json")):
    r = json.loads(f.read_text())
    sid = f.stem
    citta = r["esercente"]["indirizzo"].split(",")[-1].strip().split(" ", 1)[-1]
    for it in r["righe"]:
        up = it["prezzo_unitario"]
        if up is None:
            up, uprice = it["importo"], "€/conf."
        else:
            uprice = "€/kg" if it["unita"] == "kg" else "€/pz"
        rows.append({
            "scontrino_id": sid, "data": r["documento"]["data"],
            "esercente": r["esercente"]["ragione_sociale"], "citta": citta,
            "articolo": it["articolo"], "descrizione": it["descrizione"],
            "quantita": it["quantita"], "unita": it["unita"],
            "prezzo_unitario": up, "unita_prezzo": uprice, "importo": it["importo"],
            "codice_iva": it["codice_iva"], "aliquota_iva": RATES.get(it["codice_iva"], ""),
            "alimentare": "si" if it["alimentare"] else "no",
            "proteine_g": it.get("proteine_g", ""),
        })

out = ROOT / "receipts" / "righe.csv"
with out.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} righe -> {out}")
