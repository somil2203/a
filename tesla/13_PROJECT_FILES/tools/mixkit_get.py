"""Download Mixkit videos at 1080p only if the item page says 'Mixkit Stock Video Free License'.
usage: python3 mixkit_get.py OUTDIR MANIFEST.csv id:slug ...
"""
import csv, datetime, os, re, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) production-research"}

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()

out, man = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = []
for arg in sys.argv[3:]:
    vid, slug = arg.split(":", 1)
    page = f"https://mixkit.co/free-stock-video/{slug}-{vid}/"
    h = get(page).decode("utf-8", "ignore")
    main = h[h.find("<main"):] if "<main" in h else h
    lic_free = 'data-license="videoFree"' in main
    lic_restr = 'data-license="videoRestricted"' in main
    title = re.search(r"<title>([^<]+)</title>", h).group(1).split("|")[0].strip()
    m = re.search(r'"author"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"', h)
    author = m.group(1) if m else ""
    if lic_restr or not lic_free:
        print(f"SKIP {vid} {title}: free={lic_free} restricted={lic_restr}")
        continue
    data = None
    for res in ("1080", "720"):
        try:
            data = get(f"https://assets.mixkit.co/videos/{vid}/{vid}-{res}.mp4")
            break
        except Exception:
            pass
    fn = f"{out}/mixkit_{vid}_{slug[:40]}.mp4"
    open(fn, "wb").write(data)
    print(f"OK {vid} {title} {len(data)//1024}KB res={res}")
    rows.append([os.path.basename(fn), "video (B-roll)", "Mixkit", page, author, "Mixkit Stock Video Free License",
                 "Yes (incl. YouTube)", "No", "Yes", datetime.date.today().isoformat()])
new = not os.path.exists(man)
with open(man, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["asset_name", "asset_type", "source", "url", "creator", "license", "commercial_use",
                    "attribution_required", "modification_allowed", "date_accessed"])
    w.writerows(rows)
