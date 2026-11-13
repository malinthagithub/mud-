"""MUD system - import stock, FIFO deduction, MUD form.  Run:  python app.py"""



import os, io, re, time, secrets, datetime as dt



import pandas as pd



from flask import Flask, request, redirect, url_for, render_template, flash, send_file, session, g, abort



from werkzeug.security import generate_password_hash, check_password_hash



from jinja2 import DictLoader



from sqlalchemy import (create_engine, Column, Integer, String, Float, Date, DateTime,



                        ForeignKey, Text, func)



from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect, text



from copy import copy



from openpyxl import load_workbook
from openpyxl.styles import Color







# ---- DATABASE: XAMPP MySQL (create empty database "mud_system" in phpMyAdmin first) ----



DB_URL = os.environ.get("DATABASE_URL",



                        "mysql+pymysql://root:@localhost:3306/mud_system?charset=utf8mb4")



engine = create_engine(DB_URL, pool_pre_ping=True)



Session = sessionmaker(bind=engine)



Base = declarative_base()











class User(Base):



    __tablename__ = "users"



    id = Column(Integer, primary_key=True)



    username = Column(String(30), unique=True, nullable=False)   # stored in lower case



    full_name = Column(String(80))



    email = Column(String(120))



    password_hash = Column(String(255), nullable=False)          # never the real password



    role = Column(String(10), default="user")                    # admin / user



    active = Column(Integer, default=0)                          # 0 = waiting for admin approval



    created = Column(DateTime, default=dt.datetime.now)











class ImportItem(Base):



    __tablename__ = "imports"



    id = Column(Integer, primary_key=True)



    entry_no = Column(String(30), index=True)



    item_no = Column(Integer, default=1)



    year = Column(Integer)



    date = Column(Date)



    hs_code = Column(String(20))



    description = Column(String(120), index=True)



    unit = Column(String(20))



    imported_qty = Column(Float)



    opening_balance = Column(Float)      # balance when uploaded (capped at imported qty)



    note = Column(String(200))











class Mapping(Base):



    __tablename__ = "mapping"



    id = Column(Integer, primary_key=True)



    key = Column(String(40))             # ERP product family (e.g. FPMC) or part-no prefix



    mud_label = Column(String(120))      # name printed on the MUD



    import_desc = Column(String(300))    # import-list descriptions, comma separated (blank = ignore)



    ratio = Column(Float, default=1.0)   # used qty = ERP qty x ratio











class Shipment(Base):



    __tablename__ = "shipments"



    id = Column(Integer, primary_key=True)



    ref_no = Column(String(40))



    export_entry = Column(String(40))



    date = Column(Date)



    hs_code = Column(String(20), default="0902.30.11")



    product = Column(String(60), default="Tea Bags")



    qty_nos = Column(Float)



    qty_kgs = Column(Float)



    approval_no = Column(String(10), default="227")



    status = Column(String(12), default="draft")   # draft / confirmed / cancelled



    created = Column(DateTime, default=dt.datetime.now)











class UnmatchedIFS(Base):
    __tablename__ = "unmatched_ifs"
    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), index=True)
    excel_row = Column(Integer)
    part_no = Column(String(120))
    product_family = Column(String(100))
    part_description = Column(Text)
    order_qty = Column(Float)
    reason = Column(String(250))


class ShipmentLine(Base):



    __tablename__ = "shipment_lines"



    id = Column(Integer, primary_key=True)



    shipment_id = Column(Integer, ForeignKey("shipments.id"))



    label = Column(String(120))



    import_desc = Column(String(300))



    hs_code = Column(String(500), nullable=True)  # Comma-separated HS codes from the Qty Rule



    required = Column(Float)











class Ledger(Base):                       # every deduction ever made (gives history + undo)



    __tablename__ = "ledger"



    id = Column(Integer, primary_key=True)



    import_id = Column(Integer, ForeignKey("imports.id"), index=True)



    shipment_id = Column(Integer, ForeignKey("shipments.id"), index=True)



    line_id = Column(Integer, ForeignKey("shipment_lines.id"))



    qty = Column(Float)



    created = Column(DateTime, default=dt.datetime.now)











class QtyRule(Base):



    """IFS material deduction uses ORDER_QTY (per_unit is legacy/display only)."""



    __tablename__ = "qty_rules"



    id = Column(Integer, primary_key=True)



    key = Column(String(40), nullable=True)  # ERP product family or PART_NO prefix
    description_keyword = Column(String(200), nullable=True)  # IFS PART_DESCRIPTION keyword



    mud_label = Column(String(120))



    import_desc = Column(String(300))



    hs_code = Column(String(500), nullable=True)  # Multiple comma-separated HS codes



    basis = Column(String(5), default="nos")     # legacy/display field; not used for calculation



    per_unit = Column(Float, default=1.0)        # multiplier for IFS ORDER_QTY



    ratio_text = Column(String(60))              # text printed for information, e.g. 1Kgs:5400 TB



    active = Column(Integer, default=1)











DEFAULT_RULES = [   # from the ratios on your MUD.xlsx - please check / edit on the "Qty rules" page



    ("Filter Papers", "Filter Papers", "nos", 1 / 5400, "1Kgs:5400 TB", 1),



    ("Tea Bag Cotton Thread", "Threads", "nos", 1 / 125000, "1Cone:125,000TB", 1),



    ("Alu Wire", "Alu Wire", "nos", 1 / 36500, "1Kgs:36,500TB", 1),



    ("T/B Tags", "Tea Bags Tags", "nos", 1.0, "1:1TB", 1),



    ("Paper Envelopes", "Envelopes", "nos", 1.0, "1:1TB", 1),



    ("Tea Flavour", "Tea Flavours", "kgs", 0.05, "1Kgs Tea:0.05 Flv", 0),



    ("Fruit Particles", "Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces", "kgs", 0.075, "1Kgs:0.075 Herbs", 0),



    ("Herbs", "Herbs,Dried Herbs,Flowers", "kgs", 0.2, "1Kgs:0.2 Herbs", 0),



]







DEFAULT_MAP = [  # starting mapping - please review on the Mapping page



    ("FPMC", "Corrugated Cartons", "Corrugated Cartons", 1),



    ("SPIC", "Inner Cartons", "Tea Cartons", 1),



    ("SPMT", "Empty Tins", "Empty Tins", 1),



    ("PSIP", "Inner Pouch", "Laminating Pouch,Empty Pouch", 1),



    ("ACST", "Stickers", "Holographic Label", 1),



    ("ACTG", "T/B Tags", "Tea Bags Tags", 1),



    ("ACTH", "Tea Bag Cotton Thread", "Threads", 1),



    ("ACTP", "Self Adhesive Tape", "Adhesive Tape", 1),



    ("FLLI", "Tea Flavour", "Tea Flavours", 1),



    ("FLPT", "Herbs / Flowers", "Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers", 1),



    ("FRPT", "Fruit Particles", "Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces", 1),



    ("FPPE", "Poly Bags", "Poly Bags", 1),



    ("OWBP", "Bopp Cut Sheet", "Bopp Cut Sheet", 1),



    ("PPFP", "Filter Papers", "Filter Papers", 1),



    ("SPEF", "Paper Envelopes", "Envelopes", 1),



    ("GREIM", "China Green Tea", "China Green Tea", 1),



    ("ACSP", "Plastic Strapping", "", 1),



    ("BLKCY", "Local tea (ignored)", "", 1), ("GRECY", "Local tea (ignored)", "", 1),



    ("FGPAK", "Finished goods (ignored)", "", 1), ("SFFLT", "Semi finished (ignored)", "", 1),



    ("SFMTB", "Semi finished (ignored)", "", 1),



]







# ------------------------------------------------------------------ helpers



def parse_date(v):



    """Text dd/mm/yyyy -> date. Excel dates in the import list have day/month swapped."""



    if v is None or (not isinstance(v, str) and pd.isna(v)):



        return None



    if isinstance(v, (dt.datetime, pd.Timestamp)):



        d = v.date()



        if d.day <= 12:                       # Excel read dd/mm as mm/dd -> swap back



            return dt.date(d.year, d.day, d.month)



        return d



    m = re.match(r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$", str(v))



    if m:



        try:



            return dt.date(int(m[3]), int(m[2]), int(m[1]))



        except ValueError:



            return None



    return None











def norm_unit(u):



    u = str(u or "").strip().lower()



    return {"kgs": "Kgs", "kg": "Kgs", "ltr": "Ltrs", "ltrs": "Ltrs", "nos": "Nos", "pcs": "Pcs",



            "roll": "Roll", "reels": "Reels"}.get(u, u.title())











def num(v):



    try:



        return None if pd.isna(v) else float(v)



    except (TypeError, ValueError):



        return None











def load_imports(file):



    df = pd.read_excel(file, header=0)



    out, last, warns = [], None, []



    for i, r in df.iterrows():



        desc = r.get("Description")



        if pd.isna(desc):



            continue



        entry = None if pd.isna(r.get("Entry No")) else re.sub(r"\s+", " ", str(r["Entry No"]).strip())



        date = parse_date(r.get("Date"))



        year = num(r.get("Year"))



        if entry:



            last = (entry, date, year)



        elif last:



            entry, date, year = last



        else:



            continue



        imp = num(r.get("IM Qmty"))



        if imp is None:



            continue



        bal = num(r.get("Balance - Qnty"))



        note = ""



        if bal is None:



            bal = imp



        elif bal > imp:



            note = f"Balance in file ({bal:g}) > imported qty - capped"



            bal = imp



        out.append(dict(entry_no=entry, item_no=int(num(r.get("Item No")) or 1),



                        year=int(year) if year else (date.year if date else None), date=date,



                        hs_code=str(int(num(r.get("HS Code")))) if num(r.get("HS Code")) else "",



                        description=str(desc).strip(), unit=norm_unit(r.get("Uom")),



                        imported_qty=imp, opening_balance=bal, note=note))



    return out











UNITS = ["Kgs", "Nos", "Pcs", "Ltrs", "Roll", "Reels"]











def norm_entry(e):



    """h3232 / H-3232 / h  3232  ->  H 3232"""



    e = re.sub(r"\s+", " ", str(e or "").strip().upper())



    m = re.match(r"^([A-Z]+)\s*-?\s*(\d+)$", e)



    return f"{m[1]} {m[2]}" if m else e











def canon_desc(s, d):



    """Use the group name that already exists (ignores upper/lower case and extra spaces)."""



    d = re.sub(r"\s+", " ", (d or "").strip())



    for (x,) in s.query(ImportItem.description).distinct():



        if x.lower() == d.lower():



            return x



    return d











def clean_import_form(s, f, skip_id=None):



    """Validate the Add / Edit import form. Returns (data, error)."""



    entry, desc = norm_entry(f.get("entry_no")), canon_desc(s, f.get("description"))



    if not entry or not desc:



        return None, "Entry no and Description (group) are required."



    try:



        date = dt.date.fromisoformat(f.get("date", ""))



    except ValueError:



        return None, "Date is required (needed for FIFO order)."



    qty = to_float(f.get("imported_qty"))



    if qty <= 0:



        return None, "Imported qty must be more than 0."



    item_no = int(to_float(f.get("item_no")) or 0)



    if item_no <= 0:



        if s.query(ImportItem).filter_by(entry_no=entry, description=desc).first() and not skip_id:



            return None, f"{entry} - {desc} already exists. Edit that line instead (or type an Item no)."



        mx = [i.item_no or 0 for i in s.query(ImportItem).filter_by(entry_no=entry)]



        item_no = (max(mx) + 1) if mx else 1



    dup = s.query(ImportItem).filter_by(entry_no=entry, item_no=item_no, description=desc).first()



    if dup and dup.id != skip_id:



        return None, f"{entry} item {item_no} ({desc}) already exists."



    bal = to_float(f["opening_balance"]) if f.get("opening_balance", "").strip() else qty



    if bal < 0 or bal > qty:



        return None, "Balance must be between 0 and the imported qty."



    unit = norm_unit(f.get("unit"))



    same = s.query(ImportItem.unit).filter(ImportItem.description == desc).first()



    note = ""



    if same and same[0] and same[0] != unit:



        note = f"Unit differs from the other '{desc}' lines ({same[0]})."



    return dict(entry_no=entry, item_no=item_no, date=date, year=date.year,



                hs_code=re.sub(r"\D", "", f.get("hs_code", "")), description=desc, unit=unit,



                imported_qty=qty, opening_balance=bal, note=(f.get("note") or "").strip()[:190]), note











def balances(s):



    used = dict(s.query(Ledger.import_id, func.sum(Ledger.qty)).group_by(Ledger.import_id).all())



    return {i.id: round((i.opening_balance or 0) - (used.get(i.id) or 0), 4)



            for i in s.query(ImportItem).all()}











def normalise_hs_code(value):



    """Compare HS codes consistently, ignoring dots, spaces and hyphens."""



    return re.sub(r"\D", "", str(value or "").strip())







def parse_hs_codes(value):
    """Parse multiple HS codes, including accidentally joined 8-digit codes."""
    result = []
    for part in re.split(r"[,;\n\s]+", str(value or "")):
        code = normalise_hs_code(part)
        if not code:
            continue
        # Recover legacy values like 3919100039199090 (two 8-digit codes).
        # Do not split a valid 10-digit HS code or arbitrary lengths.
        pieces = ([code[i:i + 8] for i in range(0, len(code), 8)]
                  if len(code) >= 16 and len(code) % 8 == 0 else [code])
        for item in pieces:
            if item not in result:
                result.append(item) 
    return result


def save_hs_codes(value):
    """Store HS codes in a stable comma-separated format."""
    return ",".join(parse_hs_codes(value)) or None


def normalise_import_description(value):
    return " ".join(str(value or "").split()).casefold()


def parse_import_descriptions(value):
    """Allow comma, slash, semicolon and newline-separated import groups."""
    return {normalise_import_description(part)
            for part in re.split(r"[,;/\r\n]+", str(value or ""))
            if normalise_import_description(part)}


def plan(s, lines, prefs=None):
    """Preview FIFO allocations by import description and all rule HS codes."""
    bal = balances(s)
    result = []
    for ln in lines:
        descs = parse_import_descriptions(ln.import_desc)
        allowed_hs = set(parse_hs_codes(ln.hs_code))
        items = [it for it in s.query(ImportItem).all()
                 if normalise_import_description(it.description) in descs
                 and (not allowed_hs or normalise_hs_code(it.hs_code) in allowed_hs)]
        # Strict FIFO across all eligible HS codes: oldest import date first.
        # No user-selected entry can override the chronological order.
        items.sort(key=lambda it: (it.date is None,
                                   it.date or dt.date.max, it.id))
        available_total = round(sum(max(0, bal.get(it.id, 0)) for it in items), 4)
        need = round(max(0, ln.required or 0), 4)
        allocs = []
        for it in items:
            if need <= 0:
                break
            before = max(0, bal.get(it.id, 0))
            if before <= 0:
                continue
            take = round(min(need, before), 4)
            allocs.append(dict(item=it, take=take, before=before,
                               after=round(before - take, 4)))
            bal[it.id] = round(before - take, 4)
            need = round(need - take, 4)
        result.append(dict(line=ln, allocs=allocs, short=max(0, need),
                           candidates=items, available_total=available_total,
                           allowed_hs=sorted(allowed_hs)))
    return result


# Pending shortages are derived from immutable shipment requirements minus
# actual ledger deductions. No fictitious negative stock is ever recorded.
def pending_shortages(s):
    deducted = dict(s.query(Ledger.line_id, func.sum(Ledger.qty)).group_by(Ledger.line_id).all())
    rows = (s.query(ShipmentLine, Shipment)
            .join(Shipment, Shipment.id == ShipmentLine.shipment_id)
            .filter(Shipment.status == "confirmed")
            .order_by(Shipment.date, Shipment.id, ShipmentLine.id).all())
    return [(ln, sh, round(max(0, (ln.required or 0) - (deducted.get(ln.id) or 0)), 4))
            for ln, sh in rows if (ln.required or 0) - (deducted.get(ln.id) or 0) > 0.00005]


def pending_reconciliation_plan(s):
    """Simulate allocations without writing to the ledger; oldest MUD first."""
    pending = pending_shortages(s)
    if not pending:
        return []
    virtual = [ShipmentLine(id=ln.id, shipment_id=ln.shipment_id,
                            label=ln.label, import_desc=ln.import_desc,
                            hs_code=ln.hs_code, required=short)
               for ln, sh, short in pending]
    previews = plan(s, virtual)
    return [dict(line=ln, shipment=sh, pending=short,
                 allocs=preview['allocs'], remaining=preview['short'])
            for (ln, sh, short), preview in zip(pending, previews)]


def pending_summary(s):
    rows = pending_reconciliation_plan(s)
    return dict(rows=rows, pending=round(sum(x['pending'] for x in rows), 4),
                possible=round(sum(a['take'] for x in rows for a in x['allocs']), 4))


# ------------------------------------------------------------------ web app



app = Flask(__name__)



HERE = os.path.dirname(os.path.abspath(__file__))











def load_secret():



    """Random key kept in secret.key (created on first run) - used to sign login cookies."""



    if os.environ.get("SECRET_KEY"):



        return os.environ["SECRET_KEY"]



    path = os.path.join(HERE, "secret.key")



    if not os.path.exists(path):



        with open(path, "w") as fh:



            fh.write(secrets.token_hex(32))



    return open(path).read().strip()











app.secret_key = load_secret()



app.config.update(SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_HTTPONLY=True,



                  PERMANENT_SESSION_LIFETIME=dt.timedelta(hours=12))



BASE = """<!doctype html><html><head><title>MUD System</title><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f4f6f9;color:#20334c}
nav{width:100%;background:linear-gradient(105deg,#142c49,#204c70);padding:12px clamp(16px,2.5vw,44px);display:flex;align-items:center;gap:20px;box-shadow:0 5px 20px rgba(12,35,58,.15);position:relative;z-index:20}
nav .brand{display:flex;align-items:center;gap:10px;white-space:nowrap;color:#fff;text-decoration:none;font-size:17px;font-weight:800;letter-spacing:.4px;margin-right:14px}
nav .brand-mark{display:inline-grid;place-items:center;width:39px;height:39px;border-radius:12px;background:linear-gradient(135deg,#267b95,#24b0b5);color:#fff;font-size:13px;box-shadow:0 4px 14px rgba(0,0,0,.13)}
nav .nav-links{display:flex;align-items:center;flex:1;gap:5px;flex-wrap:wrap}
nav .nav-links a{color:#e4eef7;text-decoration:none;font-weight:600;font-size:13px;padding:11px 13px;border-radius:10px;white-space:nowrap;transition:background .2s,color .2s}
nav .nav-links a:hover,nav .nav-links a.active{background:rgba(255,255,255,.16);color:#fff}
nav .nav-account{display:flex;align-items:center;gap:12px;margin-left:auto;white-space:nowrap;color:#fff;font-size:13px}
nav .nav-account small{color:#b9d4e8}nav .nav-account form{margin:0}
nav .logout-btn{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);padding:9px 14px;border-radius:9px;color:#fff;font-weight:700;cursor:pointer}
nav .logout-btn:hover{background:rgba(255,255,255,.24)}
main{padding:26px clamp(16px,2.5vw,44px);max-width:1900px;margin:auto}
table{border-collapse:collapse;background:#fff;width:100%;margin:10px 0}td,th{border:1px solid #ccc;padding:5px 8px;font-size:14px}th{background:#e8ecf2;text-align:left}
.box{background:#fff;padding:14px;margin:10px 0;border:1px solid #ccc}.ok{color:#0a7a2f}.bad{color:#c00;font-weight:bold}
.flash{background:#fff3cd;padding:8px;margin:8px 0;border:1px solid #e0c36a}
button,input[type=submit]{background:#1f3a5f;color:#fff;border:0;padding:7px 14px;cursor:pointer}
input,select{padding:4px}.num{text-align:right}.small{font-size:12px;color:#666}
@media(max-width:1100px){nav{flex-wrap:wrap;gap:8px 16px}nav .nav-links{order:3;width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:3px}nav .nav-account{margin-left:auto}}
@media(max-width:600px){nav .brand{font-size:15px}nav .nav-account{font-size:11px;gap:7px}nav .nav-links a{padding:9px 10px;font-size:12px}main{padding:16px}}

/* Presentation-only popup alerts; no application logic is changed. */
.mud-alert-shade{position:fixed;inset:0;z-index:99999;background:rgba(12,28,48,.55);display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(3px)}
.mud-alert-card{width:min(100%,470px);background:white;border-radius:20px;box-shadow:0 25px 85px rgba(10,25,45,.28);overflow:hidden;animation:mud-pop .22s ease-out;text-align:center;color:#20334c}
.mud-alert-top{padding:29px 28px 5px}.mud-alert-symbol{width:70px;height:70px;margin:0 auto 15px;display:grid;place-items:center;border-radius:50%;font-size:33px;font-weight:800;background:#e8f7ee;color:#168653}
.mud-alert-card[data-kind=warning] .mud-alert-symbol{background:#fff4da;color:#b77900}.mud-alert-card[data-kind=error] .mud-alert-symbol{background:#fee8e8;color:#c63838}
.mud-alert-title{font-size:23px;font-weight:750;margin:0 0 10px}.mud-alert-text{font-size:15px;line-height:1.7;color:#536277;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:0 29px 22px}
.mud-alert-footer{padding:0 28px 28px}.mud-alert-ok{width:100%;padding:12px 20px;border-radius:11px;border:0;background:#1f7a56;color:white;font-weight:700;font-size:15px;cursor:pointer}
.mud-alert-card[data-kind=warning] .mud-alert-ok{background:#b77900}.mud-alert-card[data-kind=error] .mud-alert-ok{background:#bf3636}
.mud-alert-ok:focus-visible{outline:3px solid #81b6f0;outline-offset:3px}
@keyframes mud-pop{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}
@media(prefers-reduced-motion:reduce){.mud-alert-card{animation:none}}
</style></head><body>
{% if cur_user %}<nav>
<a class="brand" href="/"><span class="brand-mark">MUD</span><span>Bond MUD System</span></a>
<div class="nav-links">
<a href="/" class="{{'active' if request.path == '/' else ''}}">Home</a>
<a href="/imports" class="{{'active' if request.path.startswith('/imports') else ''}}">Import Stock</a><a href="/imports/reconcile">Pending Shortages</a>
<a href="/mapping" class="{{'active' if request.path.startswith('/mapping') else ''}}">Mapping</a>
<a href="/rules" class="{{'active' if request.path.startswith('/rules') else ''}}">Quantity Rules</a>
<a href="/shipments/new" class="{{'active' if request.path == '/shipments/new' else ''}}">New MUD</a>
<a href="/shipments" class="{{'active' if request.path == '/shipments' or (request.path.startswith('/shipments/') and request.path != '/shipments/new') else ''}}">History</a>
{% if cur_user.role == 'admin' %}<a href="/users" class="{{'active' if request.path.startswith('/users') else ''}}">Users</a>{% endif %}
</div>
<div class="nav-account"><span>{{cur_user.name}} <small>({{cur_user.role}})</small></span><form method="post" action="/logout"><button class="logout-btn" type="submit">Logout</button></form></div>
</nav>{% endif %}
<main>{% for m in get_flashed_messages() %}<span class="mud-flash-data" hidden>{{m}}</span>{% endfor %}{% block body %}{% endblock %}</main>
<script>
(function(){
  var messages=document.querySelectorAll('.mud-flash-data');
  if(!messages.length)return;
  var queue=Array.prototype.map.call(messages,function(node){return node.textContent.trim()}).filter(Boolean);
  if(!queue.length)return;
  var shade=document.createElement('div');shade.className='mud-alert-shade';
  shade.innerHTML='<section class="mud-alert-card" role="alertdialog" aria-modal="true" aria-labelledby="mud-alert-title" aria-describedby="mud-alert-text"><div class="mud-alert-top"><div class="mud-alert-symbol" aria-hidden="true"></div><h2 class="mud-alert-title" id="mud-alert-title"></h2></div><p class="mud-alert-text" id="mud-alert-text"></p><div class="mud-alert-footer"><button type="button" class="mud-alert-ok">OK, Got it</button></div></section>';
  document.body.appendChild(shade);
  var card=shade.querySelector('.mud-alert-card'),symbol=shade.querySelector('.mud-alert-symbol'),title=shade.querySelector('.mud-alert-title'),body=shade.querySelector('.mud-alert-text'),ok=shade.querySelector('.mud-alert-ok');
  var prior=document.activeElement;
  function show(){
    if(!queue.length){shade.remove();if(prior&&prior.focus)prior.focus();return;}
    var msg=queue.shift();var lower=msg.toLowerCase();
    var error=/^(not |cannot |failed|error|wrong |invalid|too many|no matching|unable)|not saved|not added|not permitted|not found|not understood|cannot be|must be|is required|waiting for the administrator/.test(lower);
    var warning=!error&&/warning|shortage|pending|review|choose yes or no|no deduction|unchanged|already exist|skipped|caution/.test(lower);
    var kind=error?'error':warning?'warning':'success';card.dataset.kind=kind;
    symbol.textContent=error?'!':warning?'!':'✓';title.textContent=error?'Action Unsuccessful':warning?'Attention Required':'Success';body.textContent=msg;
    ok.focus();
  }
  ok.addEventListener('click',show);
  shade.addEventListener('click',function(e){if(e.target===shade)show()});
  document.addEventListener('keydown',function(e){if(!shade.isConnected)return;if(e.key==='Escape'){e.preventDefault();show()}else if(e.key==='Tab'){e.preventDefault();ok.focus()}});
  show();
})();
</script>
</body></html>"""







PAGES = {



"base.html": BASE,



"auth_base.html": """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}} - MUD System</title>
<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'Segoe UI',Arial,sans-serif;background:#eef3f7;color:#20334c}
.auth-shell{min-height:100vh;display:grid;grid-template-columns:minmax(0,1.08fr) minmax(420px,.92fr)}
.auth-visual{position:relative;min-height:100vh;background:#183c4d url('static/young-businesswoman-working-computer-outside-cafe.jpg') center/cover no-repeat;display:flex;flex-direction:column;justify-content:space-between;padding:48px;isolation:isolate;color:#fff}

.auth-visual:before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: linear-gradient(
        155deg,
        rgba(8, 35, 58, 0.36),
        rgba(12, 57, 66, 0.18) 48%,
        rgba(6, 24, 44, 0.42)
    );
}

.visual-brand{display:flex;align-items:center;gap:13px;font-size:18px;font-weight:750;letter-spacing:.2px}
.brand-icon,.logo{display:grid;place-items:center;background:linear-gradient(135deg,#20a19c,#176d86);color:white;font-weight:800;border-radius:14px}
.brand-icon{height:46px;width:46px;font-size:14px;box-shadow:0 8px 24px #0003}
.visual-copy{max-width:550px}.visual-tag{display:inline-block;padding:9px 14px;border:1px solid #ffffff70;border-radius:30px;background:#ffffff1c;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;backdrop-filter:blur(8px)}
.visual-copy h2{font-size:clamp(36px,4vw,60px);line-height:1.1;letter-spacing:-1.7px;margin:22px 0 18px;color:white}
.visual-copy p{font-size:17px;line-height:1.75;color:#e0ecf1;max-width:490px}
.visual-foot{font-size:12px;color:#e2edf2}
.auth-right{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:48px 36px;background:linear-gradient(145deg,#fff,#f4f8fa)}
.card{width:100%;max-width:440px;animation:appear .4s ease both}
.logo{height:54px;width:54px;font-size:16px;margin-bottom:25px;box-shadow:0 9px 20px #137e8030}
h1{font-size:32px;line-height:1.2;letter-spacing:-.8px;color:#18334e;margin:0 0 8px}
.sub{color:#718096;font-size:14px;line-height:1.6;margin:0 0 27px}
label{display:block;font-size:13px;font-weight:650;color:#34465b;margin:16px 0 7px}
input[type=text],input[type=password],input[type=email]{display:block;width:100%;padding:13px 15px;border:1px solid #d8e1e9;border-radius:11px;background:#fff;color:#1d344b;font-size:14px;transition:border-color .2s,box-shadow .2s}
input::placeholder{color:#a0acb9}input:focus{outline:0;border-color:#1c9b91;box-shadow:0 0 0 4px #1c9b911c}
.btn{display:block;width:100%;margin-top:24px;padding:14px;border:0;border-radius:11px;background:linear-gradient(110deg,#147d66,#179e83);color:#fff;font-weight:750;font-size:15px;cursor:pointer;box-shadow:0 8px 18px #148c702b;transition:transform .2s,filter .2s}
.btn:hover{transform:translateY(-1px);filter:brightness(1.05)}
.row{display:flex;align-items:center;justify-content:space-between;margin-top:14px;font-size:13px;color:#64748b}
.row label{display:inline;margin:0;font-weight:400;cursor:pointer}.row input[type=checkbox]{accent-color:#158c75;vertical-align:middle;margin-right:5px}
.alt{text-align:center;margin-top:24px;font-size:14px;color:#64748b}.alt a{color:#0d866f;font-weight:750;text-decoration:none}.alt a:hover{text-decoration:underline}
.hint{font-size:12px;color:#8a98a8;margin-top:5px}.foot{text-align:center;color:#9aa7b5;font-size:11px;margin-top:32px}
@keyframes appear{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:850px){.auth-shell{grid-template-columns:1fr}.auth-visual{min-height:220px;padding:27px 30px}.visual-copy h2{font-size:29px;margin:12px 0 5px}.visual-copy p{font-size:13px;margin:0}.visual-tag,.visual-foot{display:none}.auth-right{min-height:auto;padding:36px 24px 55px}.card{max-width:460px}}
@media(max-width:480px){.auth-visual{min-height:170px;padding:22px}.visual-copy h2{font-size:25px}.visual-copy p{display:none}.auth-right{padding:30px 20px 48px}h1{font-size:28px}}
@media(prefers-reduced-motion:reduce){.card{animation:none}.btn{transition:none}}
/* Existing flash-message popup design retained */
.mud-alert-shade{position:fixed;inset:0;z-index:99999;background:rgba(12,28,48,.55);display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(3px)}
.mud-alert-card{width:min(100%,470px);background:white;border-radius:20px;box-shadow:0 25px 85px rgba(10,25,45,.28);overflow:hidden;animation:mud-pop .22s ease-out;text-align:center;color:#20334c}
.mud-alert-top{padding:29px 28px 5px}.mud-alert-symbol{width:70px;height:70px;margin:0 auto 15px;display:grid;place-items:center;border-radius:50%;font-size:33px;font-weight:800;background:#e8f7ee;color:#168653}
.mud-alert-card[data-kind=warning] .mud-alert-symbol{background:#fff4da;color:#b77900}.mud-alert-card[data-kind=error] .mud-alert-symbol{background:#fee8e8;color:#c63838}
.mud-alert-title{font-size:23px;font-weight:750;margin:0 0 10px}.mud-alert-text{font-size:15px;line-height:1.7;color:#536277;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:0 29px 22px}
.mud-alert-footer{padding:0 28px 28px}.mud-alert-ok{width:100%;padding:12px 20px;border-radius:11px;border:0;background:#1f7a56;color:white;font-weight:700;font-size:15px;cursor:pointer}
.mud-alert-card[data-kind=warning] .mud-alert-ok{background:#b77900}.mud-alert-card[data-kind=error] .mud-alert-ok{background:#bf3636}
.mud-alert-ok:focus-visible{outline:3px solid #81b6f0;outline-offset:3px}
@keyframes mud-pop{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}
@media(prefers-reduced-motion:reduce){.mud-alert-card{animation:none}}
</style></head><body>
<div class="auth-shell">
<aside class="auth-visual" aria-label="MUD system introduction">
<div class="visual-brand"><span class="brand-icon">MUD</span> Jafferjee Brothers</div>
<div class="visual-copy"><span class="visual-tag">Bond MUD Management</span><h2>Smarter stock.<br>Seamless workflow.</h2><p>Manage imported materials, track stock deductions and prepare MUD documents with confidence.</p></div>
<div class="visual-foot">Bond MUD System &bull; Secure workspace</div>
</aside>
<main class="auth-right"><div class="card"><div class="logo">MUD</div>
{% block head %}{% endblock %}
{% for m in get_flashed_messages() %}<span class="mud-flash-data" hidden>{{m}}</span>{% endfor %}
{% block form %}{% endblock %}
<div class="foot">Jafferjee Brothers &middot; Bond MUD System</div>
</div></main></div>
<script>function sp(b){var f=document.querySelectorAll('input.pw');for(var i=0;i<f.length;i++){f[i].type=b.checked?'text':'password'}}</script>
<script>
(function(){
  var messages=document.querySelectorAll('.mud-flash-data');
  if(!messages.length)return;
  var queue=Array.prototype.map.call(messages,function(node){return node.textContent.trim()}).filter(Boolean);
  if(!queue.length)return;
  var shade=document.createElement('div');shade.className='mud-alert-shade';
  shade.innerHTML='<section class="mud-alert-card" role="alertdialog" aria-modal="true" aria-labelledby="mud-alert-title" aria-describedby="mud-alert-text"><div class="mud-alert-top"><div class="mud-alert-symbol" aria-hidden="true"></div><h2 class="mud-alert-title" id="mud-alert-title"></h2></div><p class="mud-alert-text" id="mud-alert-text"></p><div class="mud-alert-footer"><button type="button" class="mud-alert-ok">OK, Got it</button></div></section>';
  document.body.appendChild(shade);
  var card=shade.querySelector('.mud-alert-card'),symbol=shade.querySelector('.mud-alert-symbol'),title=shade.querySelector('.mud-alert-title'),body=shade.querySelector('.mud-alert-text'),ok=shade.querySelector('.mud-alert-ok');
  var prior=document.activeElement;
  function show(){
    if(!queue.length){shade.remove();if(prior&&prior.focus)prior.focus();return;}
    var msg=queue.shift();var lower=msg.toLowerCase();
    var error=/^(not |cannot |failed|error|wrong |invalid|too many|no matching|unable)|not saved|not added|not permitted|not found|not understood|cannot be|must be|is required|waiting for the administrator/.test(lower);
    var warning=!error&&/warning|shortage|pending|review|choose yes or no|no deduction|unchanged|already exist|skipped|caution/.test(lower);
    var kind=error?'error':warning?'warning':'success';card.dataset.kind=kind;
    symbol.textContent=error?'!':warning?'!':'✓';title.textContent=error?'Action Unsuccessful':warning?'Attention Required':'Success';body.textContent=msg;
    ok.focus();
  }
  ok.addEventListener('click',show);
  shade.addEventListener('click',function(e){if(e.target===shade)show()});
  document.addEventListener('keydown',function(e){if(!shade.isConnected)return;if(e.key==='Escape'){e.preventDefault();show()}else if(e.key==='Tab'){e.preventDefault();ok.focus()}});
  show();
})();
</script>
</body></html>""",

"login.html": """{% extends 'auth_base.html' %}
{% block head %}<h1>Welcome back</h1><p class="sub">Sign in to continue to your MUD workspace.</p>{% endblock %}
{% block form %}
<form method="post">
<input type="hidden" name="next" value="{{next}}">
<label for="login-username">Username</label>
<input id="login-username" type="text" name="username" value="{{username}}" placeholder="Enter your username" autofocus required autocomplete="username">
<label for="login-password">Password</label>
<input id="login-password" class="pw" type="password" name="password" placeholder="Enter your password" required autocomplete="current-password">
<div class="row"><span><input type="checkbox" onclick="sp(this)" id="show-login"><label for="show-login">Show password</label></span></div>
<button class="btn" type="submit">Sign in</button>
</form>
<div class="alt">Don't have an account? <a href="/register">Create an account</a></div>
{% endblock %}""",

"register.html": """{% extends 'auth_base.html' %}
{% block head %}<h1>Create your account</h1><p class="sub">Join the Bond MUD System to manage your workflow.</p>{% endblock %}
{% block form %}
<form method="post">
<label for="reg-name">Full name</label>
<input id="reg-name" type="text" name="full_name" value="{{v.full_name}}" placeholder="Enter your full name" required autocomplete="name">
<label for="reg-username">Username</label>
<input id="reg-username" type="text" name="username" value="{{v.username}}" placeholder="Choose a username" required autocomplete="username">
<div class="hint">3–30 letters, numbers, dots or underscores</div>
<label for="reg-email">Email (optional)</label>
<input id="reg-email" type="email" name="email" value="{{v.email}}" placeholder="you@example.com" autocomplete="email">
<label for="reg-password">Password</label>
<input id="reg-password" class="pw" type="password" name="password" placeholder="Create a password" required autocomplete="new-password">
<div class="hint">At least 8 characters</div>
<label for="reg-confirm">Confirm password</label>
<input id="reg-confirm" class="pw" type="password" name="password2" placeholder="Re-enter your password" required autocomplete="new-password">
<div class="row"><span><input type="checkbox" onclick="sp(this)" id="show-register"><label for="show-register">Show passwords</label></span></div>
<button class="btn" type="submit">Create account</button>
</form>
<div class="alt">Already registered? <a href="/login">Sign in</a></div>
{% endblock %}""",

"users.html": """{% extends 'base.html' %}{% block body %}<h2>Users</h2>



<p class="small">New registrations wait here until you approve them. The first user is the administrator.</p>



<table><tr><th>Username</th><th>Name</th><th>Email</th><th>Role</th><th>Registered</th><th>Status</th><th></th></tr>



{% for u in rows %}<tr><td><b>{{u.username}}</b></td><td>{{u.full_name}}</td><td>{{u.email or ''}}</td><td>{{u.role}}</td>



<td>{{u.created.strftime('%d/%m/%Y %H:%M') if u.created else ''}}</td>



<td class="{{'ok' if u.active else 'bad'}}">{{'Active' if u.active else 'Waiting approval'}}</td>



<td>{% if u.id != cur_user.id %}<form method="post" action="/users/{{u.id}}/toggle" style="display:inline"><button>{{'Disable' if u.active else 'Approve'}}</button></form>{% endif %}</td></tr>{% endfor %}</table>{% endblock %}""",



"index.html": """{% extends 'base.html' %}{% block body %}
<style>
.home-dashboard{font-family:Segoe UI,Arial,sans-serif;color:#20334c}
.home-dashboard *{box-sizing:border-box}

.home-dashboard .hero {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 38px 42px;
    color: #fff;

    background:
        linear-gradient(
            90deg,
            rgba(9, 27, 45, 0.25) 0%,
            rgba(9, 27, 45, 0.10) 47%,
            rgba(9, 27, 45, 0.00) 100%
        ),
        url('https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1600&q=85')
        center 54% / cover no-repeat;

    box-shadow: 0 14px 34px rgba(23, 53, 82, 0.17);
}

.home-dashboard .eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:2px;font-weight:700;color:#a6e7e1;margin-bottom:10px}
.home-dashboard .hero h1{font-size:clamp(27px,4vw,39px);line-height:1.2;margin:0 0 12px;font-weight:750;color:#fff}
.home-dashboard .hero p{color:#e1edf4;max-width:610px;font-size:15px;line-height:1.7;margin:0 0 22px}
.home-dashboard .hero-actions{display:flex;gap:12px;flex-wrap:wrap}
.home-dashboard .hero-btn{display:inline-block;padding:12px 19px;border-radius:10px;background:#fff;color:#153c59;text-decoration:none;font-weight:700;font-size:14px;transition:transform .2s,box-shadow .2s}
.home-dashboard .hero-btn.secondary{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.45)}
.home-dashboard .hero-btn:hover{transform:translateY(-2px);box-shadow:0 7px 18px rgba(0,0,0,.12)}
.home-dashboard .section-title{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:30px 0 14px}
.home-dashboard .section-title h2{font-size:19px;margin:0;color:#20334c}
.home-dashboard .section-title span{font-size:12px;color:#748296}
.home-dashboard .stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.home-dashboard .stat{background:#fff;border:1px solid #e6edf3;border-radius:17px;padding:22px 24px;box-shadow:0 5px 22px rgba(25,53,85,.05);display:flex;align-items:center;gap:18px}
.home-dashboard .stat-icon{width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:16px;font-size:26px;flex-shrink:0;background:#e8f4ff;color:#235b9d}
.home-dashboard .stat:nth-child(2) .stat-icon{background:#e4f8ee;color:#168153}
.home-dashboard .stat-label{color:#68798e;font-size:13px;font-weight:600;margin-bottom:4px}
.home-dashboard .stat-value{font-size:33px;font-weight:750;color:#18334e;line-height:1.15;font-variant-numeric:tabular-nums}
.home-dashboard .links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.home-dashboard .link-card{display:block;background:#fff;border:1px solid #e6edf3;border-radius:16px;padding:22px;text-decoration:none;color:#233950;box-shadow:0 5px 20px rgba(25,53,85,.045);transition:transform .2s,border-color .2s,box-shadow .2s}
.home-dashboard .link-card:hover{transform:translateY(-3px);border-color:#83b5ce;box-shadow:0 12px 26px rgba(25,53,85,.1)}
.home-dashboard .link-icon{font-size:25px;margin-bottom:12px}
.home-dashboard .link-card h3{font-size:16px;margin:0 0 7px;color:#20334c}
.home-dashboard .link-card p{font-size:13px;line-height:1.55;color:#738297;margin:0 0 12px}
.home-dashboard .link-card .go{font-size:13px;font-weight:700;color:#137b89}
.home-dashboard .workflow{background:#fff;border:1px solid #e6edf3;border-radius:16px;padding:22px 26px;margin-bottom:22px}
.home-dashboard .steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.home-dashboard .step{position:relative;font-size:13px;line-height:1.5;color:#64748b}
.home-dashboard .step strong{display:block;color:#263b53;margin:9px 0 4px;font-size:14px}
.home-dashboard .step-num{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:#e7f3f5;color:#116b79;font-weight:800}
@media(max-width:850px){.home-dashboard .links{grid-template-columns:repeat(2,minmax(0,1fr))}.home-dashboard .steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:540px){.home-dashboard .hero{padding:27px 22px}.home-dashboard .stats,.home-dashboard .links,.home-dashboard .steps{grid-template-columns:1fr}.home-dashboard .stat{padding:18px}.home-dashboard .stat-value{font-size:28px}}
</style>
<div class="home-dashboard">
  <section class="hero">
    <div class="eyebrow">Jafferjee Brothers &bull; Bond MUD System</div>
    <h1>Welcome to your MUD Dashboard</h1>
    <p>Manage imported stock, prepare MUD documents, and track material deductions with a clear, organized workflow.</p>
    <div class="hero-actions"><a class="hero-btn" href="/shipments/new">+ Create New MUD</a><a class="hero-btn secondary" href="/imports">View Import Stock</a></div>
  </section>
  <div class="section-title"><h2>Overview</h2><span>Current system records</span></div>
  <section class="stats">
    <div class="stat"><div class="stat-icon" aria-hidden="true">&#128230;</div><div><div class="stat-label">Import Entries</div><div class="stat-value">{{n_imp}}</div></div></div>
    <div class="stat"><div class="stat-icon" aria-hidden="true">&#10003;</div><div><div class="stat-label">Confirmed MUDs</div><div class="stat-value">{{n_ship}}</div></div></div>
  </section>
  <div class="section-title"><h2>Quick Access</h2><span>Choose where to work</span></div>
  <section class="links">
    <a class="link-card" href="/imports"><div class="link-icon">&#128230;</div><h3>Import Stock</h3><p>Upload import lists, review quantities and manage stock entries.</p><span class="go">Open Imports &rarr;</span></a>
    <a class="link-card" href="/shipments/new"><div class="link-icon">&#128196;</div><h3>Create New MUD</h3><p>Upload an IFS QuickReport and prepare a new MUD draft.</p><span class="go">Create MUD &rarr;</span></a>
    <a class="link-card" href="/shipments"><div class="link-icon">&#128203;</div><h3>MUD History</h3><p>Review previous drafts and confirmed MUD documents.</p><span class="go">View History &rarr;</span></a>
    <a class="link-card" href="/mapping"><div class="link-icon">&#128279;</div><h3>Material Mapping</h3><p>Review ERP material mappings and import descriptions.</p><span class="go">Open Mapping &rarr;</span></a>
    <a class="link-card" href="/rules"><div class="link-icon">&#9881;</div><h3>Quantity Rules</h3><p>Manage the material matching rules used for deductions.</p><span class="go">View Rules &rarr;</span></a>
    {% if cur_user.role == 'admin' %}<a class="link-card" href="/users"><div class="link-icon">&#128101;</div><h3>User Management</h3><p>Review accounts and manage user approvals.</p><span class="go">Manage Users &rarr;</span></a>{% endif %}
  </section>
  <div class="section-title"><h2>How It Works</h2><span>Standard MUD workflow</span></div>
  <section class="workflow"><div class="steps">
    <div class="step"><span class="step-num">1</span><strong>Upload Imports</strong>Upload IMPORT_LIST.xlsx on the Imports page.</div>
    <div class="step"><span class="step-num">2</span><strong>Review Mapping</strong>Check material mappings and quantity rules.</div>
    <div class="step"><span class="step-num">3</span><strong>Create MUD</strong>Upload the IFS report, preview FIFO and confirm.</div>
    <div class="step"><span class="step-num">4</span><strong>Download Excel</strong>Download the confirmed MUD document.</div>
  </div></section>
</div>{% endblock %}""",



"imports.html": """{% extends 'base.html' %}{% block body %}



<style>



.imp .card{background:#fff;border-radius:12px;box-shadow:0 1px 5px rgba(20,40,80,.10);padding:16px 20px;margin:14px 0}



.imp h2{margin:4px 0 0;color:#1f3a5f}.imp .sub{color:#6b7785;font-size:13px;margin:2px 0 8px}



.imp h3{margin:0 0 10px;font-size:15px;color:#1f3a5f}



.imp label{display:block;font-size:12px;font-weight:bold;color:#55606e;margin-bottom:3px}



.imp input,.imp select{border:1px solid #cfd6df;border-radius:7px;padding:8px 10px;width:100%;box-sizing:border-box;font-size:14px;background:#fff}



.imp input:focus,.imp select:focus{outline:2px solid #9ec5fe;border-color:#6aa6f8}



.imp .fgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 14px}.imp .span2{grid-column:span 2}



.imp .btn{background:#1f7a4d;color:#fff;border:0;border-radius:7px;padding:9px 20px;font-weight:bold;cursor:pointer;font-size:14px}



.imp .btn:hover{background:#176640}.imp .btn.blue{background:#1f3a5f}.imp .btn.blue:hover{background:#2c4f80}



.imp .hint{font-size:12px;color:#6b7785;margin-top:8px}



.imp .toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.imp .toolbar input{width:260px}



.imp .chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}



.imp .chip{text-decoration:none;font-size:12px;padding:4px 11px;border-radius:999px;border:1px solid;font-weight:bold}



.imp .chip.all{background:#eef1f5;color:#44505e;border-color:#cdd5df}



.imp table.t{border-collapse:separate;border-spacing:0;width:100%;background:transparent;margin:6px 0}



.imp table.t th{background:#1f3a5f;color:#fff;border:0;padding:9px 10px;font-size:12px;text-transform:uppercase;letter-spacing:.4px;position:sticky;top:0;z-index:10;box-shadow:0 2px 4px rgba(0,0,0,.18)}



.imp table.t th:first-child{border-radius:8px 0 0 0}.imp table.t th:last-child{border-radius:0 8px 0 0}



.imp table.t td{background:#fff;border:0;border-bottom:1px solid #edf0f4;padding:8px 10px;font-size:14px}



.imp table.t tr.gap td{background:transparent;border:0;height:18px;padding:0}



.imp table.t tr.ghead td{font-weight:bold;padding:10px 12px;border-bottom:0}



.imp .gname{font-size:15px}.imp .gmeta{font-size:12px;font-weight:normal;opacity:.85;margin-left:10px}



.imp td.num{text-align:right;font-variant-numeric:tabular-nums}



.imp .badge{display:inline-block;min-width:78px;text-align:right;padding:3px 9px;border-radius:999px;font-weight:bold;font-size:13px}



.imp .good{background:#dcf5e5;color:#12703a}.imp .low{background:#ffe9c7;color:#9a5a00}.imp .zero{background:#fde0e0;color:#b42323}



.imp .bar{height:4px;background:#e7ebf0;border-radius:3px;margin-top:4px;overflow:hidden}.imp .bar span{display:block;height:100%}



.imp .good~.bar span{background:#2fb36b}.imp .low~.bar span{background:#f0a020}.imp .zero~.bar span{background:#d94b4b}



.imp .act a{font-size:12px;text-decoration:none;background:#eaf1fb;color:#1f3a5f;padding:4px 10px;border-radius:6px;font-weight:bold}



.imp .act a:hover{background:#d5e4f8}.imp .act button{background:#fde0e0;color:#b42323;border:0;border-radius:6px;padding:4px 9px;font-weight:bold;cursor:pointer}



.imp .note{font-size:12px;color:#8a6d00}.imp .nodate{color:#c00;font-weight:bold}



.imp .c0{--bg:#e3eeff;--fg:#1f4e9c;--ac:#4a86e8}.imp .c1{--bg:#dff5e8;--fg:#1c6b43;--ac:#2fb36b}



.imp .c2{--bg:#fff0d9;--fg:#935300;--ac:#f0a020}.imp .c3{--bg:#efe6fb;--fg:#5b3a96;--ac:#8e63d0}



.imp .c4{--bg:#d9f3f4;--fg:#116066;--ac:#27a8b0}.imp .c5{--bg:#fde4ec;--fg:#9c2a53;--ac:#e0568a}



.imp tr.ghead td{background:var(--bg);color:var(--fg);border-left:6px solid var(--ac)}



.imp tr.row td:first-child{border-left:6px solid var(--ac)}



.imp .chip[class*=c]{background:var(--bg);color:var(--fg);border-color:var(--ac)}



@media(max-width:800px){.imp .fgrid{grid-template-columns:repeat(2,1fr)}}



</style>



<div class="imp">



<h2>Import stock</h2><div class="sub">Each colour = one group. Strict FIFO uses oldest eligible import date across all matching descriptions and HS codes.</div>







<div class="card"><h3>Add new import item</h3>



<form method="post" action="/imports/add"><datalist id="groups">{% for g in groups %}<option value="{{g}}">{% endfor %}</datalist>



<div class="fgrid">



<div><label>Entry no</label><input name="entry_no" placeholder="H 12345" required></div>



<div><label>Item no</label><input name="item_no" placeholder="auto"></div>



<div><label>Import date</label><input type="date" name="date" required></div>



<div><label>HS code</label><input name="hs_code" placeholder="39199090"></div>



<div class="span2"><label>Group / Description</label><input name="description" list="groups" required placeholder="choose from the list, or type a NEW group"></div>



<div><label>Unit</label><select name="unit">{% for u in units %}<option>{{u}}</option>{% endfor %}</select></div>



<div><label>Imported qty</label><input name="imported_qty" required placeholder="0.00"></div>



<div><label>Balance (blank = same as imported)</label><input name="opening_balance" placeholder="optional"></div>



<div style="align-self:end"><button class="btn" type="submit">+ Add item</button></div>



</div>



<div class="hint"><a href="/imports/reconcile">Review existing MUD shortages before / after stock updates</a>. Pick the description from the list so the item joins the correct group. A new name creates a new group.</div></form></div>







<div class="card"><div class="toolbar"><h3 style="margin:0">Find / groups</h3>



<form method="get" class="toolbar" style="margin:0"><input name="q" value="{{q}}" placeholder="Search entry no or description"><button class="btn blue" type="submit">Search</button></form>



<form method="post" action="/imports/upload" enctype="multipart/form-data" class="toolbar" style="margin:0 0 0 auto">



<input type="file" name="file" required style="width:230px"><button class="btn blue" type="submit">Upload IMPORT_LIST.xlsx</button></form></div>



<div class="chips"><a class="chip all" href="/imports">All ({{groups|length}} groups)</a>



{% for g,v in groups.items() %}<a class="chip c{{gidx[g] % 6}}" href="/imports?q={{g|urlencode}}">{{g}} &middot; {{v[0]}}</a>{% endfor %}</div></div>







{% set ns = namespace(g=None) %}



<table class="t"><thead><tr><th>Entry</th><th>Item</th><th>Date</th><th>HS</th><th>Description</th><th>Unit</th><th style="text-align:right">Imported</th><th style="text-align:right">Balance</th><th>Note</th><th></th></tr></thead><tbody>



{% for i in rows %}{% if i.description != ns.g %}{% set ns.g = i.description %}



{% if not loop.first %}<tr class="gap"><td colspan="10"></td></tr>{% endif %}



<tr class="ghead c{{gidx[i.description] % 6}}"><td colspan="10"><span class="gname">{{i.description}}</span>



<span class="gmeta">{{gstat[i.description][0]}} lines &middot; total balance {{'{:,.2f}'.format(gstat[i.description][1])}} {{i.unit}}</span></td></tr>{% endif %}



{% set b = bal[i.id] %}{% set pct = ((b / i.imported_qty * 100) if i.imported_qty else 0) %}



{% set cls = 'zero' if b <= 0 else ('low' if pct < 20 else 'good') %}



<tr class="row c{{gidx[i.description] % 6}}"><td style="white-space:nowrap"><b>{{i.entry_no}}</b></td><td>{{i.item_no}}</td>



<td>{% if i.date %}{{i.date.strftime('%d/%m/%Y')}}{% else %}<span class="nodate">no date</span>{% endif %}</td><td>{{i.hs_code}}</td>



<td>{{i.description}}</td><td>{{i.unit}}</td><td class="num">{{'{:,.2f}'.format(i.imported_qty)}}</td>



<td class="num"><span class="badge {{cls}}">{{'{:,.2f}'.format(b)}}</span><div class="bar"><span style="width:{{[[pct,0]|max,100]|min}}%"></span></div></td>



<td class="note">{{i.note}}</td>



<td class="act" style="white-space:nowrap"><a href="/imports/{{i.id}}/edit">Edit</a>{% if i.id not in used %} <form method="post" action="/imports/{{i.id}}/delete" style="display:inline" onsubmit="return confirm('Delete this import line?')"><button>&times;</button></form>{% endif %}</td></tr>



{% endfor %}</tbody></table></div>{% endblock %}""",



"edit.html": """{% extends 'base.html' %}{% block body %}<h2>Edit import line</h2>



<form method="post" class="box"><datalist id="groups">{% for g in groups %}<option value="{{g}}">{% endfor %}</datalist><table>



<tr><td>Entry no</td><td><input name="entry_no" value="{{i.entry_no}}"></td><td>Item no</td><td><input name="item_no" value="{{i.item_no}}" size="4"></td></tr>



<tr><td>Date</td><td><input type="date" name="date" value="{{i.date or ''}}"></td><td>HS code</td><td><input name="hs_code" value="{{i.hs_code}}"></td></tr>



<tr><td>Group / Description</td><td colspan="3"><input name="description" list="groups" value="{{i.description}}" size="40"></td></tr>



<tr><td>Imported qty</td><td><input name="imported_qty" value="{{i.imported_qty}}"></td><td>Opening balance</td><td><input name="opening_balance" value="{{i.opening_balance}}"></td></tr>



<tr><td>Unit</td><td><select name="unit">{% for u in units %}<option {{'selected' if u==i.unit}}>{{u}}</option>{% endfor %}</select></td><td>Note</td><td><input name="note" value="{{i.note or ''}}"></td></tr></table>



<div class="small">Opening balance = stock BEFORE MUD deductions, NOT the current available balance. Existing ledger deductions remain unchanged when you edit. Current balance now: <b>{{'{:,.2f}'.format(cur)}}</b></div>



 <input type="submit" value="Save"> <a href="/imports">Cancel</a> &nbsp; <a href="/imports/reconcile">Review Pending MUD Shortages</a></form>
 <div class="box" style="border:2px solid #2a8b72;border-radius:10px;margin-top:20px">
 <h3 style="margin-top:0">Add Stock to This Import Entry</h3>
 <p>Use this form when you receive more stock for this SAME import entry. Do not change Opening Balance to the new receipt quantity. This action adds the quantity to both Imported Qty and Opening Balance, while keeping all previous MUD deductions unchanged.</p>
 <p><b>Current available:</b> {{'{:,.2f}'.format(cur)}} {{i.unit}} &nbsp; | &nbsp; <b>Already deducted:</b> {{'{:,.2f}'.format(used)}} {{i.unit}}</p>
 <form method="post" action="/imports/{{i.id}}/add-stock" onsubmit="return confirm('Add this stock to the existing import entry? Previous MUD deductions will remain unchanged. You will then review pending shortages before any new deduction.');">
 <label>Additional Stock Quantity (not total balance)</label>
 <input type="number" name="add_qty" min="0.0001" step="any" required placeholder="e.g. 10000" style="padding:9px;width:220px">
 <button type="submit" style="background:#18744c;padding:10px 16px">+ Add Stock and Review Pending MUDs</button>
 </form>
 <p class="small">This keeps the existing import date and FIFO position. If the stock belongs to a different customs entry/date, use Add New Import Item instead.</p>
 </div>{% endblock %}""",



 "reconcile.html": """{% extends 'base.html' %}{% block body %}
<h2>Pending MUD shortages — stock reconciliation</h2>
<div style="padding:18px;border:2px solid #d69e16;background:#fff3cd;border-radius:10px;margin:12px 0">
  <strong style="font-size:19px;color:#8b3e00">ACTION REQUIRED — Existing MUD shortages</strong>
  <p>Import stock update is saved. <b>NO stock was deducted from pending MUDs by that update.</b>
  Choose YES to deduct eligible stock, or NO to keep all shortages pending.</p>
</div>
<p>These MUDs were already issued. The quantities below are <b>not yet deducted</b>. Stock deductions happen only when you choose Yes. Strict FIFO applies across all eligible HS codes, and older issued MUDs are fulfilled first.</p>
<div class="box"><b>Total pending:</b> {{'{:,.2f}'.format(summary.pending)}} &nbsp; | &nbsp; <b>Can deduct from current stock:</b> {{'{:,.2f}'.format(summary.possible)}}</div>
{% if summary.rows %}
<table><tr><th>MUD</th><th>Material</th><th>Pending before</th><th>FIFO imports that can be deducted now</th><th>Still pending after Yes</th></tr>
{% for r in summary.rows %}<tr><td><a href="/shipments/{{r.shipment.id}}">{{r.shipment.ref_no or r.shipment.id}}</a></td><td>{{r.line.label}}<div class="small">{{r.line.import_desc}} | HS: {{r.line.hs_code or 'Any'}}</div></td><td class="num">{{'{:,.2f}'.format(r.pending)}}</td>
<td>{% for a in r.allocs %}<div>{{a.item.entry_no}} / {{a.item.hs_code}} / {{a.item.date}}: <b>{{'{:,.2f}'.format(a.take)}}</b></div>{% else %}No matching stock yet{% endfor %}</td><td class="num">{{'{:,.2f}'.format(r.remaining)}}</td></tr>{% endfor %}</table>
<form method="post"><button name="decision" value="yes" {% if summary.possible <= 0 %}disabled{% endif %} onclick="return confirm('YES: Deduct available stock now using strict FIFO against previously issued MUD shortages? This will update the ledger.')">YES — Deduct pending MUD shortages</button>
<button name="decision" value="no">NO — Keep shortages pending</button></form>
{% else %}<p class="ok">No pending MUD shortages.</p>{% endif %}
<p><a href="/imports">Return to Import Stock</a></p>{% endblock %}""",

"mapping.html": """{% extends 'base.html' %}{% block body %}<h2>Mapping (ERP part -> MUD item -> import list)</h2>



<p class="small">Key = ERP product family (FPMC) or start of a part number. Leave "Import descriptions" blank to ignore. Several descriptions: separate with commas.</p>



<form method="post" action="/mapping/save"><table><tr><th>Key</th><th>MUD name</th><th>Import descriptions</th><th>Ratio</th><th>Delete</th></tr>



{% for m in rows %}<tr><td><input name="key_{{m.id}}" value="{{m.key}}" size="10"></td><td><input name="label_{{m.id}}" value="{{m.mud_label}}" size="28"></td>



<td><input name="desc_{{m.id}}" value="{{m.import_desc}}" size="60"></td><td><input name="ratio_{{m.id}}" value="{{m.ratio}}" size="6"></td>



<td><input type="checkbox" name="del_{{m.id}}"></td></tr>{% endfor %}



<tr><td><input name="key_new" size="10"></td><td><input name="label_new" size="28"></td><td><input name="desc_new" size="60"></td><td><input name="ratio_new" value="1" size="6"></td><td>new</td></tr>



</table><input type="submit" value="Save"></form>



<p class="small">Import descriptions in your list: {{descs}}</p>{% endblock %}""",



"rules.html": """{% extends 'base.html' %}{% block body %}<h2>Qty rules (IFS ORDER_QTY only)</h2>



<p class="small">Each IFS row deducts exactly its ORDER_QTY (Per 1 unit is NOT used). Match by PRODUCT_FAMILY or PART_NO prefix. ACGM, ACTP, OWBP, PSIP, SPEF and SPMT use specific PART_DESCRIPTION conditions to select one Qty Rule ID; other families use the same-HS lowest-ID fallback. Different HS code sets for unconfigured families are flagged as ambiguous. Enter multiple HS codes separated by commas (e.g. 48239090, 48232000). All assigned codes are shown below. If you previously entered two 8-digit codes without a comma, they will be separated automatically when you save. Blank means any HS code within the selected import descriptions. HS codes filter FIFO stock.</p>



<form method="post" action="/rules/save"><table><tr><th>Key</th><th>MUD name</th><th>Import descriptions</th><th>HS Codes (all)</th><th>Basis (legacy)</th><th>Per 1 unit (unused)</th><th>Ratio text</th><th>Active</th><th>Delete</th></tr>



{% for m in rows %}<tr><td><input name="key_{{m.id}}" value="{{m.key or ''}}" size="12"></td><td><input name="label_{{m.id}}" value="{{m.mud_label}}" size="22"></td><td><input name="desc_{{m.id}}" value="{{m.import_desc}}" size="40"></td>



<td style="min-width:260px"><input name="hs_{{m.id}}" value="{{parse_hs_codes(m.hs_code)|join(', ')}}" size="32" placeholder="48239090, 48232000" style="width:96%;box-sizing:border-box">
<div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:6px">
{% for hs in parse_hs_codes(m.hs_code) %}<span style="background:#e6f0ff;color:#183e6a;padding:3px 7px;border-radius:5px;font-size:12px;font-weight:bold">{{hs.strip()}}</span>{% else %}<span class="small">Any HS code</span>{% endfor %}
</div></td>



<td><select name="basis_{{m.id}}"><option value="nos" {{'selected' if m.basis=='nos'}}>nos</option><option value="kgs" {{'selected' if m.basis=='kgs'}}>kgs</option></select></td>



<td><input name="per_{{m.id}}" value="{{m.per_unit}}" size="14"></td><td><input name="text_{{m.id}}" value="{{m.ratio_text or ''}}" size="16"></td>



<td><input type="checkbox" name="act_{{m.id}}" {{'checked' if m.active}}></td><td><input type="checkbox" name="del_{{m.id}}"></td></tr>{% endfor %}



<tr><td><input name="key_new" size="12"></td><td><input name="label_new" size="22"></td><td><input name="desc_new" size="40"></td><td><input name="hs_new" size="32" placeholder="HS1, HS2, HS3"></td><td><select name="basis_new"><option value="nos">nos</option><option value="kgs">kgs</option></select></td>



<td><input name="per_new" size="14"></td><td><input name="text_new" size="16"></td><td><input type="checkbox" name="act_new" checked></td><td>new</td></tr></table>



<input type="submit" value="Save"></form>{% endblock %}""",



"new.html": """{% extends 'base.html' %}{% block body %}<h2>New MUD MUD</h2>



<form method="post" enctype="multipart/form-data" class="box"><table>



<tr><td>Ref no</td><td><input name="ref_no" value="JB - "></td><td>Export entry no</td><td><input name="export_entry"></td></tr>



<tr><td>Date</td><td><input type="date" name="date" value="{{today}}"></td><td>HS code</td><td><input name="hs_code" value="0902.30.11"></td></tr>



<tr><td>Product</td><td><input name="product" value="Tea Bags"></td><td>Approval no</td><td><input name="approval_no" value="227"></td></tr>



<tr><td colspan="4">Material quantities are calculated ONLY from IFS Excel ORDER_QTY (not export Nos/Kgs).</td></tr>



<tr><td>IFS QuickReport.xlsx</td><td colspan="3"><input type="file" name="file" accept=".xlsx,.xls" required></td></tr>



</table>



<input type="submit" value="Create draft"></form>{% endblock %}""",



"list.html": """{% extends 'base.html' %}{% block body %}<h2>MUD history</h2>



<table><tr><th>#</th><th>Ref</th><th>Export entry</th><th>Date</th><th>Product</th><th>Qty Nos</th><th>Status</th></tr>



{% for x in rows %}<tr><td><a href="/shipments/{{x.id}}">{{x.id}}</a></td><td>{{x.ref_no}}</td><td>{{x.export_entry}}</td><td>{{x.date}}</td>



<td>{{x.product}}</td><td class="num">{{'{:,.0f}'.format(x.qty_nos or 0)}}</td><td>{{x.status}}</td></tr>{% endfor %}</table>{% endblock %}""",



"view.html": """{% extends 'base.html' %}{% block body %}



<h2>MUD #{{sh.id}} - {{sh.status}}</h2>



<div class="box">{{sh.ref_no}} | Export entry {{sh.export_entry}} | {{sh.date}} | {{sh.product}} {{'{:,.0f}'.format(sh.qty_nos or 0)}} Nos / {{sh.qty_kgs or 0}} Kgs</div>



<form method="post"><table><tr><th>MUD item</th><th>Required</th><th>Strict FIFO allocation (oldest first across all HS codes)</th><th>Short</th></tr>



{% for p in plans %}<tr><td>{{p.line.label}}<div class="small">{{p.line.import_desc}}</div><div class="small">Allowed HS codes: {{p.line.hs_code or "Any"}}</div></td>



<td class="num">{% if sh.status=='draft' %}<input name="qty_{{p.line.id}}" value="{{p.line.required}}" size="10">{% else %}{{p.line.required}}{% endif %}</td>



<td><div class="small">Matching available: <b>{{'{:,.2f}'.format(p.available_total) if p.available_total is not none else '—'}}</b></div>
<table><tr><th>Entry</th><th>HS code</th><th>Date</th><th>Available at preview</th><th>Reduce</th><th>Remaining at preview</th></tr>
{% for a in p.allocs %}<tr><td>{{a.item.entry_no}}</td><td>{{a.item.hs_code}}</td><td>{{a.item.date or ''}}</td><td>{{'{:,.2f}'.format(a.before) if sh.status=='draft' else '—'}}</td><td><b>{{'{:,.2f}'.format(a.take)}}</b></td><td>{{'{:,.2f}'.format(a.after) if sh.status=='draft' else '—'}}</td></tr>{% endfor %}</table>
{% if sh.status=='draft' %}<details><summary>Show all matching imports ({{p.candidates|length}})</summary><table><tr><th>Entry</th><th>HS</th><th>Current balance</th></tr>{% for c in p.candidates %}<tr><td>{{c.entry_no}}</td><td>{{c.hs_code}}</td><td>{{'{:,.2f}'.format(bal[c.id])}}</td></tr>{% endfor %}</table></details>{% endif %}</td>



<td class="{{'bad' if p.short>0 else 'ok'}}">{{'{:,.2f}'.format(p.short) if p.short>0 else 'OK'}}</td>



</tr>{% endfor %}</table>



</form>
{% if unmatched %}
<h3 style="color:#a33">Unmatched IFS items ({{unmatched|length}}) - not deducted</h3>
<p><b>Manual review required:</b> Nothing is created automatically. For each IFS row, select an existing active Qty Rule, or enter the correct rule details yourself. The system shows matching Import Stock and its current balance. If stock is missing, add a real customs import entry on <a href="/imports" target="_blank">Import Stock</a> first. No fake stock is created. You can resolve rows without deleting or uploading the IFS draft again. Confirm remains disabled until all rows are reviewed.</p>
<table><tr><th>Excel row</th><th>PART_NO</th><th>Family</th><th>PART_DESCRIPTION</th><th>ORDER_QTY</th><th>Reason</th></tr>
{% for u in unmatched %}<tr><td>{{u.excel_row}}</td><td>{{u.part_no}}</td><td>{{u.product_family}}</td><td>{{u.part_description}}</td><td>{{u.order_qty}}</td><td class="bad">{{u.reason}}</td></tr>
<tr><td colspan="6" style="background:#f3f7fc;padding:14px">
<form method="post" action="/shipments/{{sh.id}}/resolve/{{u.id}}" style="border:1px solid #c7d8eb;border-radius:9px;padding:12px;background:white">
<b>Resolve Excel row {{u.excel_row}} manually</b>
<p class="small">Choose a configured active rule below, OR create a rule by filling all new-rule fields. Only the rule you choose will apply to this IFS row. ORDER_QTY {{u.order_qty}} is the required MUD quantity (no multiplier).</p>
<label>Existing active Qty Rule:</label>
<select name="rule_id" style="min-width:330px;max-width:100%;padding:7px"><option value="">-- Create a rule manually below --</option>{% for r in active_rules %}<option value="{{r.id}}">#{{r.id}} | {{r.key}} | {{r.mud_label}} | {{r.import_desc}} | HS {{r.hs_code or 'Any'}}</option>{% endfor %}</select>
<details style="margin:12px 0"><summary><b>Or enter a NEW Qty Rule manually</b> (only if no existing rule is selected)</summary>
<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:10px">
<label>IFS KEY / Family<br><input name="new_key" value="{{u.product_family}}" required></label>
<label>MUD name<br><input name="new_label" placeholder="e.g. Poly Bags"></label>
<label>Import Stock description<br><input name="new_desc" list="manual_import_groups" placeholder="Exact import group name" size="30"></label>
<label>Allowed HS codes<br><input name="new_hs" placeholder="e.g. 39232190"></label>
</div><p class="small">Check the existing Import Stock groups and HS codes before saving. Blank HS means any HS for that import description. Rule is created only when you submit this form.</p></details>
<button type="submit" onclick="return confirm('Resolve this IFS row using the rule you selected or entered? No stock will be created automatically.')">Save rule choice &amp; add to MUD draft</button>
{% if u.reason == 'No active Qty Rule for KEY' %}
<p style="margin-top:12px"><button type="submit" form="skip-ifs-{{u.id}}" style="background:#a44" onclick="return confirm('Mark this IFS row as No MUD Required? It will be excluded from this draft without stock deduction or a Qty Rule.')">No MUD Required — exclude this row</button></p>
{% endif %}
</form>
{% if u.reason == 'No active Qty Rule for KEY' %}<form id="skip-ifs-{{u.id}}" method="post" action="/shipments/{{sh.id}}/skip-unruled/{{u.id}}"></form>{% endif %}
</td></tr>{% endfor %}</table>
<datalist id="manual_import_groups">{% for name in import_groups %}<option value="{{name}}">{% endfor %}</datalist>
<p><a href="/rules" target="_blank">Open Qty Rules</a> &nbsp; | &nbsp; <a href="/imports" target="_blank">Check / add real Import Stock</a></p>
{% endif %}
<form method="post">
{% if sh.status=='draft' %}<div class="box">Add line: name <input name="new_label"> import descriptions <input name="new_desc" size="30"> qty <input name="new_qty" size="10"></div>



<button name="action" value="preview">Refresh preview</button> <button name="action" value="confirm" {% if unmatched %}disabled title="Resolve unmatched IFS rows first"{% endif %} onclick="return confirm('Issue this MUD? Available stock will be deducted; shortage will remain pending for later reconciliation.')">ISSUE MUD (allow shortage)</button>



<button name="action" value="delete" onclick="return confirm('Delete draft?')">Delete draft</button>{% endif %}</form>



{% if sh.status=='confirmed' %}{% if plans|selectattr('short','gt',0)|list %}<p class="bad">This issued MUD still has pending stock shortages. <a href="/imports/reconcile">Review pending deductions</a>.</p>{% endif %}<p><a href="/shipments/{{sh.id}}/mud.xlsx"><button>Download MUD (Excel)</button></a>



<form method="post" style="display:inline"><button name="action" value="undo" onclick="return confirm('Cancel this MUD and give the quantities back?')">Undo / cancel MUD</button></form>{% endif %}{% endblock %}""",



}



app.jinja_loader = DictLoader(PAGES)











# ------------------------------------------------------------------ login / register



FAILS = {}                                   # (ip, username) -> [count, first_time]



DUMMY_HASH = generate_password_hash("dummy-password")



OPEN_PAGES = {"login", "register", "static"}











@app.before_request



def guard():



    g.user = None



    uid = session.get("uid")



    if uid:



        with Session() as s:



            u = s.get(User, uid)



            if u and u.active:



                g.user = {"id": u.id, "username": u.username, "name": u.full_name or u.username, "role": u.role}



            else:



                session.clear()



    if request.endpoint in OPEN_PAGES or request.endpoint is None:



        return None



    if not g.user:



        nxt = request.full_path.rstrip("?") if request.method == "GET" else "/"



        return redirect(url_for("login", next=nxt))



    return None











@app.context_processor



def inject_user():



    return {"cur_user": g.get("user")}











def safe_next(n):



    return n if n and n.startswith("/") and not n.startswith("//") and "\\\\" not in n else "/"











@app.route("/login", methods=["GET", "POST"])



def login():



    if g.user:



        return redirect("/")



    nxt, username = safe_next(request.values.get("next")), ""



    if request.method == "POST":



        username = request.form.get("username", "").strip().lower()



        pw, key = request.form.get("password", ""), (request.remote_addr, username)



        cnt, first = FAILS.get(key, [0, time.time()])



        if time.time() - first > 300:



            cnt, first = 0, time.time()



        if cnt >= 5:



            flash("Too many wrong attempts. Please wait 5 minutes and try again.")



        else:



            with Session() as s:



                u = s.query(User).filter_by(username=username).first()



                ok = check_password_hash(u.password_hash if u else DUMMY_HASH, pw) and u is not None



                if not ok:



                    FAILS[key] = [cnt + 1, first]



                    flash("Wrong username or password.")



                elif not u.active:



                    flash("Your account is waiting for the administrator's approval.")



                else:



                    FAILS.pop(key, None)



                    session.clear(); session["uid"] = u.id; session.permanent = True



                    return redirect(nxt)



    return render_template("login.html", title="Sign in", next=nxt, username=username)











@app.route("/register", methods=["GET", "POST"])



def register():



    if g.user:



        return redirect("/")



    v = dict(full_name="", username="", email="")



    if request.method == "POST":



        f = request.form



        v = dict(full_name=f.get("full_name", "").strip(), username=f.get("username", "").strip().lower(),



                 email=f.get("email", "").strip())



        err = None



        if not v["full_name"]:



            err = "Please enter your full name."



        elif not re.fullmatch(r"[a-z0-9_.]{3,30}", v["username"]):



            err = "Username must be 3-30 characters: letters, numbers, dot or underscore."



        elif v["email"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", v["email"]):



            err = "That email address does not look right."



        elif len(f.get("password", "")) < 8:



            err = "Password must be at least 8 characters."



        elif f.get("password") != f.get("password2"):



            err = "The two passwords do not match."



        if not err:



            with Session() as s:



                if s.query(User).filter_by(username=v["username"]).first():



                    err = "That username is already taken."



                else:



                    first = s.query(User).count() == 0



                    s.add(User(username=v["username"], full_name=v["full_name"][:80], email=v["email"][:120],



                               password_hash=generate_password_hash(f["password"]),



                               role="admin" if first else "user", active=1 if first else 0))



                    s.commit()



                    flash("Account created. You are the administrator - please sign in." if first else



                          "Account created. The administrator must approve it before you can sign in.")



                    return redirect("/login")



        flash(err)



    return render_template("register.html", title="Register", v=v)











@app.post("/logout")



def logout():



    session.clear()



    flash("You have been signed out.")



    return redirect("/login")











@app.route("/users")



def users():



    if g.user["role"] != "admin":



        abort(403)



    with Session() as s:



        return render_template("users.html", rows=s.query(User).order_by(User.id).all())











@app.post("/users/<int:uid>/toggle")



def users_toggle(uid):



    if g.user["role"] != "admin" or uid == g.user["id"]:



        abort(403)



    with Session() as s:



        u = s.get(User, uid)



        if u:



            u.active = 0 if u.active else 1; s.commit()



    return redirect("/users")











@app.route("/")



def index():



    with Session() as s:



        return render_template("index.html", n_imp=s.query(ImportItem).count(),



                               n_ship=s.query(Shipment).filter_by(status="confirmed").count())











@app.route("/imports")



def imports():



    q = request.args.get("q", "").strip()



    with Session() as s:



        qs = s.query(ImportItem)



        if q:



            qs = qs.filter((ImportItem.description.like(f"%{q}%")) | (ImportItem.entry_no.like(f"%{q}%")))



        rows = qs.order_by(ImportItem.description, ImportItem.date, ImportItem.id).all()



        bal = balances(s)



        groups = {}



        for i in s.query(ImportItem).order_by(ImportItem.description):



            g = groups.setdefault(i.description, [0, i.unit, 0.0])



            g[0] += 1; g[2] += bal[i.id]



        used = {x for (x,) in s.query(Ledger.import_id).distinct()}



        gidx = {g: k for k, g in enumerate(groups)}                  # fixed colour per group



        gstat = {}



        for i in rows:                                                # lines / balance of the rows shown



            g = gstat.setdefault(i.description, [0, 0.0]); g[0] += 1; g[1] += bal[i.id]



        return render_template("imports.html", rows=rows, bal=bal, q=q, groups=groups, units=UNITS,



                               used=used, gidx=gidx, gstat=gstat)











@app.post("/imports/add")



def imports_add():



    with Session() as s:



        d, msg = clean_import_form(s, request.form)



        if d is None:



            flash("Not added: " + msg); return redirect("/imports")



        s.add(ImportItem(**d)); s.commit()



        flash(f"Added {d['entry_no']} item {d['item_no']} - {d['description']} ({d['imported_qty']:g} {d['unit']})." + (" Warning: " + msg if msg else ""))



    return redirect("/imports/reconcile" if _has_pending() else "/imports")











@app.route("/imports/<int:iid>/edit", methods=["GET", "POST"])



def imports_edit(iid):



    with Session() as s:



        it = s.get(ImportItem, iid)



        if request.method == "POST":



            d, msg = clean_import_form(s, request.form, skip_id=iid)



            if d is None:



                flash("Not saved: " + msg); return redirect(f"/imports/{iid}/edit")



            already_used = float(s.query(func.coalesce(func.sum(Ledger.qty), 0))
                                 .filter(Ledger.import_id == iid).scalar() or 0)
            if d["opening_balance"] + 0.00005 < already_used:
                flash(f"Not saved: opening balance {d['opening_balance']:,.2f} cannot be below "
                      f"the {already_used:,.2f} already deducted for confirmed MUDs.")
                return redirect(f"/imports/{iid}/edit")
            if already_used > 0.00005 and any(
                    d[field] != getattr(it, field) for field in
                    ("entry_no", "item_no", "date", "hs_code", "description", "unit")):
                flash("Not saved: this import entry has existing MUD deductions. "
                      "Its identity, date, HS code, description and unit cannot be changed; "
                      "you may correct quantities without rewriting MUD history.")
                return redirect(f"/imports/{iid}/edit")
            for k, v in d.items():



                setattr(it, k, v)



            s.commit(); flash("Import stock saved. No pending-MUD stock deduction was performed." + (" Warning: " + msg if msg else ""))



            return redirect("/imports/reconcile" if _has_pending() else "/imports")



        groups = [g for (g,) in s.query(ImportItem.description).distinct().order_by(ImportItem.description)]



        used = float(s.query(func.coalesce(func.sum(Ledger.qty), 0))
                           .filter(Ledger.import_id == iid).scalar() or 0)
        return render_template("edit.html", i=it, groups=groups, units=UNITS,
                               cur=balances(s)[iid], used=used)











@app.post("/imports/<int:iid>/add-stock")
def imports_add_stock(iid):
    """Increase stock without rewriting past ledger deductions or creating a new table."""
    from decimal import Decimal, InvalidOperation
    raw = (request.form.get("add_qty") or "").strip()
    try:
        quantity = Decimal(raw)
    except InvalidOperation:
        quantity = Decimal("0")
    if not quantity.is_finite() or quantity <= 0 or quantity > Decimal("1000000000000"):
        flash("Stock was not added. Enter a positive additional quantity.")
        return redirect(f"/imports/{iid}/edit")
    with Session() as s:
        # Lock the import row before reading/updating quantities.
        it = s.query(ImportItem).filter(ImportItem.id == iid).with_for_update().first()
        if it is None:
            abort(404)
        used = float(s.query(func.coalesce(func.sum(Ledger.qty), 0))
                     .filter(Ledger.import_id == iid).scalar() or 0)
        opening = float(it.opening_balance or 0)
        imported = float(it.imported_qty or 0)
        if opening + 0.00005 < used:
            flash("Stock not added: existing stock history is inconsistent. Contact the administrator.")
            return redirect(f"/imports/{iid}/edit")
        qty = float(quantity)
        it.opening_balance = round(opening + qty, 4)
        it.imported_qty = round(imported + qty, 4)
        if it.opening_balance > it.imported_qty + 0.00005:
            s.rollback()
            flash("Stock not added: opening balance cannot exceed imported quantity.")
            return redirect(f"/imports/{iid}/edit")
        # Retain a compact receipt marker within the existing note field.
        marker = f"Stock +{qty:g} on {dt.date.today().isoformat()}"
        prior = (it.note or "").strip()
        it.note = (prior + " | " + marker if prior else marker)[-200:]
        s.commit()
    flash(f"Added {qty:,.2f} stock to this import entry. Previous MUD deductions unchanged. Review pending MUD shortages and choose YES or NO.")
    return redirect("/imports/reconcile" if _has_pending() else "/imports")


@app.post("/imports/<int:iid>/delete")



def imports_delete(iid):



    with Session() as s:



        if s.query(Ledger).filter_by(import_id=iid).count():



            flash("Cannot delete: this line is already used in a MUD.")



        else:



            s.query(ImportItem).filter_by(id=iid).delete(); s.commit(); flash("Deleted.")



    return redirect("/imports")











@app.post("/imports/upload")



def imports_upload():



    data = load_imports(request.files["file"])



    with Session() as s:



        exist = {(i.entry_no, i.item_no, i.description) for i in s.query(ImportItem).all()}



        added = 0



        for d in data:



            k = (d["entry_no"], d["item_no"], d["description"])



            if k in exist:



                continue



            s.add(ImportItem(**d)); exist.add(k); added += 1



        s.commit()



    flash(f"{added} new import lines added, {len(data) - added} already existed. Existing rows were NOT overwritten.")



    return redirect("/imports/reconcile" if _has_pending() else "/imports")











def _has_pending():
    with Session() as s:
        return bool(pending_shortages(s))


@app.route("/imports/reconcile", methods=["GET", "POST"])
def imports_reconcile():
    with Session() as s:
        if request.method == "POST":
            if request.form.get("decision") == "no":
                flash("No deduction made. Existing MUD shortages remain pending.")
                return redirect("/imports")
            if request.form.get("decision") != "yes":
                abort(400)
            # Serialize reconciliation with other ledger writes in MySQL.
            if engine.dialect.name == "mysql":
                s.execute(text("SELECT id FROM imports ORDER BY id FOR UPDATE")).all()
                s.execute(text("SELECT id FROM shipment_lines ORDER BY id FOR UPDATE")).all()
            rows = pending_reconciliation_plan(s)
            count = 0
            qty = 0.0
            for row in rows:
                for a in row["allocs"]:
                    if a["take"] > 0:
                        s.add(Ledger(import_id=a["item"].id,
                                     shipment_id=row["shipment"].id,
                                     line_id=row["line"].id, qty=a["take"]))
                        qty += a["take"]
                        count += 1
            s.commit()
            flash(f"Reconciled {qty:,.2f} units in {count} FIFO deductions. Remaining shortages stay pending.")
            return redirect("/imports/reconcile")
        return render_template("reconcile.html", summary=pending_summary(s))


@app.route("/mapping")



def mapping():



    with Session() as s:



        descs = ", ".join(sorted({d for (d,) in s.query(ImportItem.description).distinct()}))



        return render_template("mapping.html", rows=s.query(Mapping).order_by(Mapping.key).all(), descs=descs)











@app.post("/mapping/save")



def mapping_save():



    f = request.form



    with Session() as s:



        for m in s.query(Mapping).all():



            if f.get(f"del_{m.id}"):



                s.delete(m); continue



            m.key, m.mud_label = f[f"key_{m.id}"].strip(), f[f"label_{m.id}"].strip()



            m.import_desc, m.ratio = f[f"desc_{m.id}"].strip(), (to_float(f[f"ratio_{m.id}"]) or 1)



        if f.get("key_new", "").strip():



            s.add(Mapping(key=f["key_new"].strip(), mud_label=f["label_new"].strip(),



                          import_desc=f["desc_new"].strip(), ratio=(to_float(f["ratio_new"]) or 1)))



        s.commit()



    flash("Mapping saved.")



    return redirect("/mapping")











def to_float(x):



    """Accepts 15,411.00 / 15411 / 1/5400 / blank (=0)."""



    x = str(x or "").replace(",", "").replace(" ", "").strip()



    if "/" in x:



        a, b = x.split("/", 1)



        return float(a) / float(b)



    return float(x or 0)











@app.errorhandler(ValueError)



def bad_number(e):



    flash(f"Number not understood ({e}). Please type numbers like 15411 or 15411.5")



    return redirect(request.referrer or "/")











@app.route("/rules")



def rules():



    with Session() as s:



        return render_template("rules.html", rows=s.query(QtyRule).order_by(QtyRule.id).all(), parse_hs_codes=parse_hs_codes)











@app.post("/rules/save")

def rules_save():

    f = request.form

    with Session() as s:

        for m in s.query(QtyRule).all():

            if f.get(f"del_{m.id}"):

                s.delete(m)

                continue

            m.key = f.get(f"key_{m.id}", "").strip() or None
            m.description_keyword = None  # IFS matching is key-only

            m.mud_label = f[f"label_{m.id}"].strip()

            m.import_desc = f[f"desc_{m.id}"].strip()

            m.hs_code = save_hs_codes(f.get(f"hs_{m.id}", ""))

            m.basis = f[f"basis_{m.id}"]        

            m.per_unit = to_float(f[f"per_{m.id}"])

            m.ratio_text = f[f"text_{m.id}"].strip()

            m.active = 1 if f.get(f"act_{m.id}") else 0



        if f.get("label_new", "").strip():
            

            s.add(QtyRule(

                key=f.get("key_new", "").strip() or None,
                description_keyword=None,  # IFS matching is key-only

                mud_label=f["label_new"].strip(),

                import_desc=f["desc_new"].strip(),

                hs_code=save_hs_codes(f.get("hs_new", "")),

                basis=f["basis_new"],

                per_unit=to_float(f["per_new"]),

                ratio_text=f["text_new"].strip(),

                active=1 if f.get("act_new") else 0

            ))

        s.commit()

    flash("Qty rules saved.")

    return redirect("/rules")





@app.route("/shipments")



def shipments():



    with Session() as s:



        return render_template("list.html", rows=s.query(Shipment).order_by(Shipment.id.desc()).all())











def _ifs_string(value):
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


# IFS product-family specific rules. These are existing QtyRule database IDs.
# Only the selected rule contributes ORDER_QTY; no per_unit multiplier.
IFS_RULE_IDS = {
    "ACGM": (44, 45), "ACTP": (15, 16),
    "OWBP": (14, 20, 25), "PSIP": (11, 12),
    "SPEF": (22, 23, 24), "SPMT": (33, 34, 35, 36),
}


def _ifs_contains(description, phrase):
    """Match a whole phrase, ignoring case and repeated whitespace."""
    normalized = re.sub(r"\s+", " ", description or "").casefold()
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase.casefold())
                     + r"(?![a-z0-9])", normalized) is not None


def _choose_special_rule_id(family, description):
    """Return the intended QtyRule ID for a known duplicate family.

    Priority matters: BOPP Films overrides Heat Sealable; Foil Envelopes
    overrides Heat Seal; 150g must not be confused with 100g.
    """
    d = re.sub(r"\s+", " ", description or "").strip()
    if family == "ACGM":
        return 45 if _ifs_contains(d, "hot melt") else 44
    if family == "ACTP":
        # Configure these two IDs here if your Qty Rules are reversed.
        if re.search(r'(?<!\d)1\s*/\s*2\s*(?:inches?\b|")', d, re.I):
            return 15
        if re.search(r'(?<![\d/])2\s*(?:inches?\b|")', d, re.I):
            return 16
        return 15  # unspecified tape width
    if family == "PSIP":
        return 11 if re.search(r"\bpouches?\b", d, re.I) else 12
    if family == "SPEF":
        if _ifs_contains(d, "foil envelopes"):
            return 22
        if _ifs_contains(d, "heat seal") or _ifs_contains(d, "heat sealable"):
            return 24
        return 23
    if family == "SPMT":
        if re.search(r"(?<!\d)100\s*g\b", d, re.I):
            return 33
        if re.search(r"(?<!\d)200\s*g\b", d, re.I):
            return 34
        if re.search(r"(?<!\d)150\s*g\b", d, re.I):
            return 36
        return 35
    if family == "OWBP":
        if re.search(r"\bbopp\s+films?\b", d, re.I):
            return 20
        if _ifs_contains(d, "heat sealable"):
            return 25
        return 14
    return None


def choose_ifs_rule(row, rules):
    """Match IFS family/key, then description ONLY for configured families.

    Missing/inactive configured IDs are reported, never silently replaced.
    Other families keep the previous safe same-HS duplicate behavior.
    """
    part = _ifs_string(row.get("PART_NO")).upper()
    family = _ifs_string(row.get("PRODUCT_FAMILY")).upper()
    description = _ifs_string(row.get("PART_DESCRIPTION"))
    eligible = [
        rule for rule in rules
        if rule.key and rule.key.strip() and (
            family == rule.key.strip().upper()
            or part.startswith(rule.key.strip().upper())
        )
    ]
    if not eligible:
        return None, "No active Qty Rule for KEY"

    longest = max(len(rule.key.strip()) for rule in eligible)
    eligible = [rule for rule in eligible if len(rule.key.strip()) == longest]

    # The six user-specified families use their own description-based branches.
    # Do not use HS code equality to choose between different material rules.
    if family in IFS_RULE_IDS:
        rule_id = _choose_special_rule_id(family, description)
        match = next((r for r in eligible if r.id == rule_id
                      and r.key.strip().upper() == family), None)
        if match is None:
            return None, (f"{family}: expected Qty Rule ID {rule_id} "
                          "is missing, inactive, or has the wrong KEY")
        return match, None

    hs_sets = {frozenset(parse_hs_codes(rule.hs_code)) for rule in eligible}
    if len(hs_sets) > 1:
        return None, "Same KEY has different HS Code sets; check Qty Rules"
    return min(eligible, key=lambda rule: rule.id), None


def calculate_ifs_lines(qr, rules, ignored_families=()):
    """Sum IFS ORDER_QTY without multiplying by per_unit; return skipped rows."""
    required_columns = {"PART_NO", "PRODUCT_FAMILY", "ORDER_QTY"}
    missing = required_columns - set(qr.columns)
    if missing:
        raise ValueError("IFS Excel missing columns: " + ", ".join(sorted(missing)))
    totals, skipped = {}, []
    ignored = {x.upper() for x in ignored_families}
    for idx, row in qr.iterrows():
        if _ifs_string(row.get("PRODUCT_FAMILY")).upper() in ignored:
            continue
        rule, reason = choose_ifs_rule(row, rules)
        qty = pd.to_numeric(row.get("ORDER_QTY"), errors="coerce")
        if pd.isna(qty) or not float("-inf") < float(qty) < float("inf") or qty < 0:
            reason = "Invalid ORDER_QTY"
        if reason:
            skipped.append(dict(excel_row=idx + 2, part_no=_ifs_string(row.get("PART_NO"))[:120],
                                product_family=_ifs_string(row.get("PRODUCT_FAMILY"))[:100],
                                part_description=_ifs_string(row.get("PART_DESCRIPTION")),
                                order_qty=float(qty) if pd.notna(qty) else None, reason=reason))
            continue
        if not rule.import_desc or not rule.import_desc.strip():
            skipped.append(dict(excel_row=idx + 2, part_no=_ifs_string(row.get("PART_NO"))[:120],
                                product_family=_ifs_string(row.get("PRODUCT_FAMILY"))[:100],
                                part_description=_ifs_string(row.get("PART_DESCRIPTION")),
                                order_qty=float(qty), reason=f"Rule {rule.id} has no import description"))
            continue
        key = (rule.mud_label, rule.import_desc, save_hs_codes(rule.hs_code))
        totals[key] = totals.get(key, 0.0) + float(qty)
    return totals, skipped


@app.route("/shipments/new", methods=["GET", "POST"])
def shipment_new():
    if request.method == "GET":
        return render_template("new.html", today=dt.date.today().isoformat())
    f = request.form
    up = request.files.get("file")
    if not up or not up.filename:
        flash("Please upload an IFS QuickReport Excel file.")
        return redirect("/shipments/new")
    try:
        qr = pd.read_excel(up)
    except Exception as exc:
        flash(f"Could not read IFS Excel: {exc}")
        return redirect("/shipments/new")
    with Session() as s:
        rules = s.query(QtyRule).filter_by(active=1).all()
        try:
            ignored_families = {m.key for m in s.query(Mapping).all()
                                if m.key and not (m.import_desc or "").strip()}
            totals, skipped = calculate_ifs_lines(qr, rules, ignored_families)
        except ValueError as exc:
            flash(str(exc))
            return redirect("/shipments/new")
        if not totals and not skipped:
            flash("No material lines found in IFS Excel.")
            return redirect("/shipments/new")
        sh = Shipment(ref_no=f.get("ref_no", ""), export_entry=f.get("export_entry", ""),
                      date=dt.date.fromisoformat(f["date"]), hs_code=f.get("hs_code", ""),
                      product=f.get("product", ""), qty_nos=None, qty_kgs=None,
                      approval_no=f.get("approval_no", ""))
        s.add(sh)
        s.flush()
        for missing in skipped:
            s.add(UnmatchedIFS(shipment_id=sh.id, **missing))
        for (label, desc, line_hs), quantity in totals.items():
            s.add(ShipmentLine(shipment_id=sh.id, label=label, import_desc=desc,
                               hs_code=line_hs, required=round(quantity, 4)))
        s.commit()
        flash(f"IFS processed: {len(totals)} matched MUD lines and {len(skipped)} unmatched rows. "
              "Unmatched rows are displayed below; confirmation is blocked until they are resolved.")
        return redirect(f"/shipments/{sh.id}")


@app.post("/shipments/<int:sid>/skip-unruled/<int:uid>")
def skip_unruled_ifs(sid, uid):
    """Explicit one-row exclusion, only for missing active KEY rules."""
    with Session() as s:
        sh = s.get(Shipment, sid)
        u = s.get(UnmatchedIFS, uid)
        if not sh or sh.status != "draft" or not u or u.shipment_id != sid:
            abort(404)
        if u.reason != "No active Qty Rule for KEY":
            flash("No MUD Required is available only for 'No active Qty Rule for KEY' rows.")
            return redirect(f"/shipments/{sid}")
        row = u.excel_row
        s.delete(u)
        s.commit()
        flash(f"IFS row {row} excluded manually: No MUD Required. No rule or import stock created; no deduction.")
        return redirect(f"/shipments/{sid}")


@app.post("/shipments/<int:sid>/resolve/<int:uid>")
def resolve_unmatched_manually(sid, uid):
    """User-directed resolution only; never creates import stock or auto-selects rules."""
    with Session() as s:
        sh = s.get(Shipment, sid)
        u = s.get(UnmatchedIFS, uid)
        if not sh or sh.status != "draft" or not u or u.shipment_id != sid:
            abort(404)
        f = request.form
        selected = (f.get("rule_id") or "").strip()
        if selected:
            try:
                rule = s.get(QtyRule, int(selected))
            except ValueError:
                rule = None
            if not rule or not rule.active:
                flash("Select a valid active Qty Rule.")
                return redirect(f"/shipments/{sid}")
            family = (u.product_family or "").strip().upper()
            part = (u.part_no or "").strip().upper()
            key = (rule.key or "").strip().upper()
            if not key or not (family == key or part.startswith(key)):
                flash("Selected Qty Rule KEY does not match this IFS family / PART_NO.")
                return redirect(f"/shipments/{sid}")
        else:
            key = (f.get("new_key") or "").strip().upper()
            label = (f.get("new_label") or "").strip()
            desc = (f.get("new_desc") or "").strip()
            hs = save_hs_codes(f.get("new_hs", ""))
            family = (u.product_family or "").strip().upper()
            part = (u.part_no or "").strip().upper()
            if not key or not (family == key or part.startswith(key)) or not label or not desc:
                flash("Enter a matching KEY, MUD name and exact Import Stock description.")
                return redirect(f"/shipments/{sid}")
            if s.query(QtyRule).filter(func.upper(QtyRule.key) == key).first():
                flash("A Qty Rule already uses this KEY. Select an existing active rule or edit it on Qty Rules; duplicate rules are not created.")
                return redirect(f"/shipments/{sid}")
            rule = QtyRule(key=key, description_keyword=None, mud_label=label,
                           import_desc=desc, hs_code=hs, basis="nos",
                           per_unit=1.0, ratio_text="IFS ORDER_QTY", active=1)
            s.add(rule)
            s.flush()
        if not (rule.import_desc or "").strip() or not (rule.mud_label or "").strip():
            flash("Selected Qty Rule needs a MUD name and Import Stock description.")
            return redirect(f"/shipments/{sid}")
        qty = u.order_qty
        if qty is None or not (0 <= qty < float("inf")):
            flash("Invalid IFS ORDER_QTY; cannot resolve this row.")
            return redirect(f"/shipments/{sid}")
        line_hs = save_hs_codes(rule.hs_code)
        line = (s.query(ShipmentLine).filter_by(shipment_id=sid, label=rule.mud_label,
                                                import_desc=rule.import_desc, hs_code=line_hs).first())
        if line:
            line.required = round((line.required or 0) + qty, 4)
        else:
            s.add(ShipmentLine(shipment_id=sid, label=rule.mud_label,
                               import_desc=rule.import_desc, hs_code=line_hs,
                               required=round(qty, 4)))
        descs = parse_import_descriptions(rule.import_desc)
        allowed = set(parse_hs_codes(rule.hs_code))
        stock = [it for it in s.query(ImportItem).all()
                 if normalise_import_description(it.description) in descs
                 and (not allowed or normalise_hs_code(it.hs_code) in allowed)]
        bal = balances(s)
        available = round(sum(max(0, bal.get(it.id, 0)) for it in stock), 4)
        excel_row, rule_id = u.excel_row, rule.id
        s.delete(u)
        s.commit()
        flash(f"IFS row {excel_row} manually resolved using Qty Rule #{rule_id}. "
              f"Matching import balance: {available:g}. "
              + ("Check FIFO preview before confirming." if available else
                 "No matching stock available. Add a REAL import entry manually on Import Stock, or issue with pending shortage."))
        return redirect(f"/shipments/{sid}")


@app.route("/shipments/<int:sid>", methods=["GET", "POST"])



def shipment_view(sid):



    with Session() as s:



        sh = s.get(Shipment, sid)



        prefs, action = {}, None  # prefs retained for compatibility; strict FIFO ignores it



        if request.method == "POST":



            f, action = request.form, request.form.get("action")



            if action == "delete" and sh.status == "draft":



                s.query(UnmatchedIFS).filter_by(shipment_id=sid).delete()
                s.query(ShipmentLine).filter_by(shipment_id=sid).delete(); s.delete(sh); s.commit()



                return redirect("/shipments")



            if action == "undo" and sh.status == "confirmed":



                s.query(Ledger).filter_by(shipment_id=sid).delete(); sh.status = "cancelled"; s.commit()



                flash("MUD cancelled, balances restored.")



                return redirect(f"/shipments/{sid}")



            if sh.status == "draft":



                for ln in s.query(ShipmentLine).filter_by(shipment_id=sid):



                    if f"qty_{ln.id}" in f:



                        ln.required = to_float(f[f"qty_{ln.id}"])



                if f.get("new_label") and f.get("new_qty"):



                    s.add(ShipmentLine(shipment_id=sid, label=f["new_label"], import_desc=f.get("new_desc", ""),



                                       required=to_float(f["new_qty"])))



                s.flush()



        lines = s.query(ShipmentLine).filter_by(shipment_id=sid).order_by(ShipmentLine.id).all()



        if sh.status == "confirmed":   # show what was really deducted



            plans = []



            for ln in lines:



                al = [dict(item=s.get(ImportItem, l.import_id), take=l.qty,
                           before=0, after=0)
                      for l in s.query(Ledger).filter_by(line_id=ln.id)]
                already = round(sum(a["take"] for a in al), 4)
                plans.append(dict(line=ln, allocs=al,
                                  short=round(max(0, (ln.required or 0) - already), 4),
                                  candidates=[], available_total=None))



        else:



            plans = plan(s, lines, prefs)



        if action == "confirm" and sh.status == "draft":

            if s.query(UnmatchedIFS).filter_by(shipment_id=sid).count():
                flash("Cannot confirm: manually resolve every unmatched IFS row first. No automatic rules or stock will be created.")
            else:



                for p in plans:



                    for a in p["allocs"]:



                        s.add(Ledger(import_id=a["item"].id, shipment_id=sid, line_id=p["line"].id, qty=a["take"]))



                sh.status = "confirmed"; s.commit()



                flash("MUD issued. Available stock deducted using strict FIFO; any shortage remains PENDING until explicitly reconciled.")



                return redirect(f"/shipments/{sid}")



        s.commit()



        unmatched = s.query(UnmatchedIFS).filter_by(shipment_id=sid).order_by(UnmatchedIFS.excel_row).all()
        return render_template("view.html", sh=sh, plans=plans, prefs=prefs,
                               bal=balances(s), unmatched=unmatched,
                               active_rules=s.query(QtyRule).filter_by(active=1).order_by(QtyRule.key, QtyRule.id).all(),
                               import_groups=sorted({i.description for i in s.query(ImportItem).all() if i.description}))











TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MUD_template.xlsx")



ALIAS = {"herbs / flowers": "herbs", "self adhesive tape": "self adhesive tape-1/2", "poly bags": "poly bags", "tea bag foil envelopes": "paper envelopes", "tea bags cotton threads": "tea bag cotton thread"}


def mud_excel_row_key(label, template_rows):
    """Find an existing template row for harmless spelling/plural variants.

    Explicit business aliases take precedence. Only exact normalized word matches
    (with a simple trailing-s plural equivalence) are automatic: no fuzzy
    similarity guesses that could merge genuinely different materials.
    """
    def words(value):
        value = re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold())
        return tuple(w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
                     for w in value.split())

    key = str(label or "").strip().casefold()
    key = ALIAS.get(key, key)
    if key in template_rows:
        return key
    comparable = words(key)
    matches = [name for name in template_rows if words(name) == comparable]
    return matches[0] if len(matches) == 1 else key












def copy_style(ws, src, dst):



    for c in range(1, 10):



        ws.cell(dst, c)._style = copy(ws.cell(src, c)._style)











@app.route("/shipments/<int:sid>/mud.xlsx")



def mud_xlsx(sid):



    """Fills YOUR MUD layout (MUD_template.xlsx) - same header, full item list, ratios, declarant."""



    with Session() as s:



        sh = s.get(Shipment, sid)



        wb = load_workbook(TEMPLATE); ws = wb.active; ws.title = "Tea Bags"



        fmt = lambda d: d.strftime("%d/%m/%Y") if d else ""



        # ---- header (only the changing fields; other header text stays as in your MUD)



        ws["H8"] = sh.ref_no or ""



        ws["D13"] = sh.export_entry or ""



        ws["D15"] = fmt(sh.date)



        ws["I13"] = f": {sh.product}"



        ws["G15"] = f": {sh.hs_code}"



        ws["G16"] = sh.qty_nos or None



        ws["G17"] = sh.qty_kgs or None



        # ---- item table



        first = 21



        last = next(r for r in range(first, ws.max_row + 1) if str(ws.cell(r, 1).value or "").startswith("Consi")) - 1



        for r in range(first, last + 1):                 # clear last MUD's import / used numbers



            for c in (3, 4, 5, 8):



                ws.cell(r, c).value = None



        rows = {str(ws.cell(r, 1).value or "").strip().lower(): r for r in range(first, last + 1)}



        lines = []                                       # (label, allocations, rule HS code override)



        for ln in s.query(ShipmentLine).filter_by(shipment_id=sid).order_by(ShipmentLine.id):



            al = [(s.get(ImportItem, l.import_id), l.qty) for l in s.query(Ledger).filter_by(line_id=ln.id)]



            if al:



                lines.append((ln.label, al, ln.hs_code))



        # Resolve similar labels to the existing template row before inserting rows.
        # Merge lines that target the same material so the first allocation is not
        # overwritten by another spelling of the same material.
        grouped = {}
        for label, allocations, line_hs in lines:
            row_key = mud_excel_row_key(label, rows)
            if row_key not in grouped:
                grouped[row_key] = [label, [], line_hs]
            grouped[row_key][1].extend(allocations)
        lines = [(label, allocations, hs) for label, allocations, hs in grouped.values()]

        extra = [x for x in lines if mud_excel_row_key(x[0], rows) not in rows]

    

        if extra:                                        # items not in your template list -> added at the end of the table



            ws.insert_rows(last + 1, amount=len(extra))



            for i, (label, al, line_hs) in enumerate(extra):



                r = last + 1 + i



                copy_style(ws, last, r)



                for c in range(1, 10):



                    ws.cell(r, c).value = None



                ws.cell(r, 1).value, ws.cell(r, 6).value = label, sh.approval_no



                ws.cell(r, 7).value, ws.cell(r, 9).value = al[0][0].hs_code, al[0][0].unit



                rows[label.strip().lower()] = r



            last += len(extra)



        rest = {}



        for label, al, line_hs in lines:



            r = rows[mud_excel_row_key(label, rows)]



            for k, (it, q) in enumerate(al):



                if k == 0:



                    tgt = r



                    # Print the actual HS code of the imported stock used.



                    ws.cell(r, 7).value = it.hs_code



                    if not ws.cell(r, 9).value: ws.cell(r, 9).value = it.unit



                    ws.cell(r, 3).value, ws.cell(r, 4).value = it.imported_qty, it.entry_no



                    ws.cell(r, 5).value, ws.cell(r, 8).value = it.date, q



                    ws.cell(r, 5).number_format = "dd/mm/yyyy"



                else:



                    rest.setdefault(r, []).append((it, q, line_hs))



        for r in sorted(rest, reverse=True):             # second / third import entry of the same item -> extra rows below



            ws.insert_rows(r + 1, amount=len(rest[r]))

            for j, (it, q, line_hs) in enumerate(rest[r]):


                rr = r + 1 + j



                copy_style(ws, r, rr)



                for c in range(1, 10):



                    ws.cell(rr, c).value = None



                ws.cell(rr, 6).value = ws.cell(r, 6).value



                ws.cell(rr, 7).value = it.hs_code



                ws.cell(rr, 9).value = ws.cell(r, 9).value



                ws.cell(rr, 3).value, ws.cell(rr, 4).value = it.imported_qty, it.entry_no



                ws.cell(rr, 5).value, ws.cell(rr, 8).value = it.date, q



                ws.cell(rr, 5).number_format = "dd/mm/yyyy"



        added = len(extra) + sum(len(v) for v in rest.values())



        ws.print_area = f"A1:I{68 + added}" 



        for r in range(first, ws.max_row + 1):           # declarant date



            if str(ws.cell(r, 2).value or "").strip() == "Date" and ws.cell(r, 1).value is None:



                ws.cell(r, 4).value = fmt(sh.date)



        # Excel visibility fix: the MUD template uses a white/theme-0 font
        # in some imported-quantity, entry-number and date cells. Values were
        # written correctly but appeared blank on the white worksheet.
        # Change only the font colour, preserving font size, bold, borders,
        # number formats, merged cells and the rest of the original template.
        for excel_row in range(first, last + 1 + sum(len(v) for v in rest.values())):
            for excel_col in (3, 4, 5):  # C=Imported, D=Entry, E=Import date
                cell = ws.cell(excel_row, excel_col)
                if cell.value is not None:
                    visible_font = copy(cell.font)
                    visible_font.color = "FF000000"  # opaque black
                    cell.font = visible_font

        buf = io.BytesIO(); wb.save(buf); buf.seek(0)



        return send_file(buf, as_attachment=True, download_name=f"MUD_{sh.export_entry or sid}.xlsx")











def init_db():



    Base.metadata.create_all(engine)



    # create_all does not widen existing columns: migrate them in place.
    # Existing HS values and shipment history are preserved.
    if engine.dialect.name == "mysql":
        with engine.begin() as conn:
            for table_name in ("qty_rules", "shipment_lines"):
                cols = inspect(conn).get_columns(table_name)
                hs_col = next(c for c in cols if c["name"] == "hs_code")
                if getattr(hs_col["type"], "length", None) is not None and hs_col["type"].length < 500:
                    conn.execute(text(f"ALTER TABLE {table_name} MODIFY COLUMN hs_code VARCHAR(500) NULL"))


    with Session() as s:



        if s.query(Mapping).count() == 0:



            for k, l, d, r in DEFAULT_MAP:



                s.add(Mapping(key=k, mud_label=l, import_desc=d, ratio=r))



            s.commit()



        if s.query(QtyRule).count() == 0:



            for lab, d, b, p, tx, a in DEFAULT_RULES:



                s.add(QtyRule(mud_label=lab, import_desc=d, basis=b, per_unit=p, ratio_text=tx, active=a))



            s.commit()











if __name__ == "__main__":



    init_db()



    print("Open htt&#x70;*\\:*//127.0.0.1:5000 in your browser")



    app.run(host="127.0.0.1", port=5000)