#!/usr/bin/env python3
"""Build SE7-branded COA + spec sheet from the mill data, with no mill identity."""
import html, pathlib

OUT = pathlib.Path("/home/arriee/business/se7-deploy/proof-media")

COA_ROWS = [
    ("1", "Appearance", "Pale yellow, viscous, clear liquid", "Pale yellow, viscous, clear liquid"),
    ("2", "Moisture (K.F.)", "0.25% max", "0.16%"),
    ("3", "Free fatty acids (as oleic)", "1.0% max", "0.52%"),
    ("4", "Acid value (mg KOH/g)", "2.00 max", "1.04"),
    ("5", "Iodine value (Wijs method)", "82 – 90", "84.48"),
    ("6", "Saponification value (mg KOH/g)", "177 – 185", "180.28"),
    ("7", "Hydroxyl value (mg KOH/g)", "158 – 165", "162.47"),
    ("8", "Insoluble impurities", "0.02", "0.00"),
    ("9", "Viscosity @ 25 °C (poise)", "6.0 – 9.0 cps", "7.3"),
    ("10", "Refractive index @ 20 °C", "1.477 – 1.481", "1.4773"),
    ("11", "Specific gravity @ 30 °C", "0.954 – 0.960", "0.957"),
    ("12", "Identification", "Positive", "Pass"),
    ("13", "Odour", "Characteristic, comparable to standard", "Pass"),
    ("14", "Peroxide value", "4.0 meq/kg", "1.67 meq/kg"),
    ("15", "Ricinoleic acid", "85 min", "87.45"),
    ("16", "Unsaponifiable matter", "1.0% max", "0.40%"),
    ("17", "Colour (Gardner)", "4.00 max", "3.0"),
    ("18", "Colour (Lovibond, 5.25\" cell)", "Y 20.0 max · R 2.0 max", "Y 17.0 · R 1.7"),
]

SPEC_ROWS = [
    ("Appearance", "Pale yellow, viscous, clear liquid"),
    ("Moisture", "0.25% max"),
    ("Free fatty acids (F.F.A.)", "1.00% max"),
    ("Acid value", "2.00% max"),
    ("Hydroxyl value", "160 – 168"),
    ("Iodine value", "82 – 90"),
    ("Saponification value", "175 – 187"),
    ("Insoluble impurities", "Nil"),
    ("Relative density @ 20 °C", "0.954 – 0.967"),
    ("Refractive index @ 20 °C", "1.4700 – 1.4810"),
    ("Unsaponifiable matter", "1.0 max"),
    ("Solubility in ethyl alcohol", "Complete, without turbidity"),
    ("Colour (1\" cell, Lovibond)", "Y + 5R ≤ 2.2Y, 0.3R max"),
    ("Colour (5.25\" cell, Lovibond)", "Y 20.0 max · R 2.0 max"),
]

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; background:#fff; color:#141414;
       font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; }
.page { width:210mm; height:297mm; padding:16mm 16mm 14mm; position:relative; }
.top { display:flex; align-items:flex-start; justify-content:space-between; }
.mark { display:flex; align-items:center; gap:10px; }
.logo { width:34px; height:34px; background:#141414; color:#FCFCFA; border-radius:8px;
        font-weight:800; font-size:15px; letter-spacing:.5px;
        display:flex; align-items:center; justify-content:center; }
.brand { font-size:13px; font-weight:800; letter-spacing:3px; }
.brand small { display:block; font-size:9px; letter-spacing:2px; color:#6b6b66; font-weight:600; margin-top:3px; }
.docref { text-align:right; font-size:9px; letter-spacing:1.4px; color:#6b6b66; line-height:1.7; }
h1 { font-size:21px; letter-spacing:2.4px; margin:16mm 0 2mm; font-weight:800; }
.sub { font-size:12px; color:#3a3a36; margin-bottom:7mm; }
.sub b { color:#141414; }
.rule { height:2px; background:#141414; margin-bottom:6mm; }
.rule span { display:block; width:42mm; height:2px; background:#E23A2E; margin-top:0; }
table.meta { width:100%; border-collapse:collapse; margin-bottom:7mm; font-size:9.5px; }
table.meta td { padding:4.2px 6px; border-bottom:1px solid #E4E2DB; vertical-align:top; }
table.meta td.k { width:38mm; color:#6b6b66; letter-spacing:.7px; font-size:8.2px;
                  text-transform:uppercase; font-weight:700; }
table.data { width:100%; border-collapse:collapse; font-size:9.6px; }
table.data th { text-align:left; background:#141414; color:#FCFCFA; font-size:8.2px;
                letter-spacing:1.3px; text-transform:uppercase; padding:6.5px 7px; font-weight:700; }
table.data td { padding:5.4px 7px; border-bottom:1px solid #E9E7E0; }
table.data tr:nth-child(even) td { background:#FAF9F5; }
table.data td.n { color:#9b988f; width:9mm; }
table.data td.v { font-weight:700; }
.foot { position:absolute; left:16mm; right:16mm; bottom:12mm; border-top:1px solid #D9D7D0; padding-top:4mm;
        font-size:8.2px; color:#6b6b66; line-height:1.6; display:flex; justify-content:space-between; gap:10mm; }
.foot b { color:#141414; }
.note { margin-top:5mm; font-size:8.6px; color:#6b6b66; line-height:1.65; }
"""


def page(doc_title, subtitle, meta, head, rows, note, ref):
    meta_html = "".join(f'<tr><td class="k">{html.escape(k)}</td><td>{html.escape(v)}</td></tr>'
                        for k, v in meta)
    head_html = "".join(f"<th>{html.escape(h)}</th>" for h in head)
    if len(head) == 4:
        body = "".join(f'<tr><td class="n">{html.escape(n)}</td><td>{html.escape(p)}</td>'
                       f'<td>{html.escape(s)}</td><td class="v">{html.escape(v)}</td></tr>'
                       for n, p, s, v in rows)
    else:
        body = "".join(f'<tr><td>{html.escape(p)}</td><td class="v">{html.escape(s)}</td></tr>'
                       for p, s in rows)
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style>
<div class="page">
  <div class="top">
    <div class="mark">
      <div class="logo">SE7</div>
      <div class="brand">SANDHU EXPORTS<small>PRAGUE · INDIA</small></div>
    </div>
    <div class="docref">SE7 / CASTOR OIL FSG<br>{html.escape(ref)}<br>ISSUED 22 OCT 2026</div>
  </div>
  <h1>{html.escape(doc_title)}</h1>
  <div class="sub">{subtitle}</div>
  <div class="rule"><span></span></div>
  <table class="meta">{meta_html}</table>
  <table class="data"><thead><tr>{head_html}</tr></thead><tbody>{body}</tbody></table>
  <div class="note">{note}</div>
  <div class="foot">
    <div><b>SE7 · Sandhu Exports</b><br>Prague, Czech Republic · mill-direct from India<br>hello@se7.studio · se7.studio</div>
    <div style="text-align:right">Mill name and signed original<br>released to buyers on request.</div>
  </div>
</div>"""


coa = page(
    "CERTIFICATE OF ANALYSIS",
    'Refined <b>Castor Oil — First Special Grade (FSG)</b>, analysed on the manufacturer\'s lot certificate.',
    [("Product", "Refined castor oil, first special grade (FSG)"),
     ("Lot reference", "14072025"),
     ("Manufactured", "14 July 2025"),
     ("Retest / expiry", "14 July 2027"),
     ("Packing", "200 kg HDPE drums on pallets · 16 MT net per 20-ft"),
     ("Port", "FOB Mundra, India"),
     ("Standard", "As per the agreed specification for castor oil FSG")],
    ["#", "Parameter", "Specified limit", "Result"],
    COA_ROWS,
    "All parameters conform to the specification above. Results apply to the lot named on this certificate. "
    "Method references: K.F., Wijs, Gardner and Lovibond as stated.",
    "CERTIFICATE OF ANALYSIS · COA-01")

spec = page(
    "PRODUCT SPECIFICATION",
    'Refined <b>Castor Oil — First Special Grade (FSG)</b>, BSS-75. Mill-direct, FOB Mundra.',
    [("Product", "Refined castor oil, first special grade (FSG) / BSS-75"),
     ("Packing", "200 kg HDPE drums on pallets · 16 MT net per 20-ft"),
     ("Port", "FOB Mundra, India"),
     ("MOQ", "16 MT net · 1 × 20-ft"),
     ("Applications", "Lubricants and greases · cosmetics · plastics · paints and resins · pharmaceuticals"),
     ("Storage", "Dry, ambient, away from direct sunlight; keep drums sealed"),
     ("Documents", "Full mill COA with lot traceability released on request")],
    ["Parameter", "Specification"],
    SPEC_ROWS,
    "Specification values are the mill's declared limits for this grade. Every lot is released against a "
    "certificate of analysis; the signed original and the mill's name are shared with buyers on request.",
    "PRODUCT SPECIFICATION · TDS-01")

(OUT / "se7-castor-fsg-coa.html").write_text(coa, encoding="utf-8")
(OUT / "se7-castor-fsg-spec.html").write_text(spec, encoding="utf-8")
print("written", OUT / "se7-castor-fsg-coa.html", OUT / "se7-castor-fsg-spec.html")
