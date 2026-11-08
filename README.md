# ProteinAccountant

Archivio scontrini della spesa con apporto proteico stimato per riga.

- `receipts/AAAA-MM-GG_esercente_citta.json`: scontrino strutturato (testata, pagamento, righe, riepilogo IVA, proteine stimate)
- `receipts/images/`: foto originale dello scontrino
- `receipts/righe.csv`: tutte le righe di tutti gli scontrini, rigenerato con `python3 tools/export_csv.py`; è la sorgente del cruscotto "Spesa e prezzi"
