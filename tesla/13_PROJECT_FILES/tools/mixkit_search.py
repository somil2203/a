"""Search Mixkit (Mixkit License: free commercial use, no attribution) and build thumbnail sheets.
usage: python3 mixkit_search.py OUTDIR term1 term2 ...
"""
import io, json, re, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) production-research"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def search(term):
    html = get(f"https://mixkit.co/free-stock-video/{term}/").decode("utf-8", "ignore")
    items = []
    for m in re.finditer(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"', html):
        slug, vid = m.group(1), m.group(2)
        if vid not in [i[0] for i in items]:
            items.append((vid, slug))
    return items


def sheet(term, items, out):
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 14)
    tiles = []
    for vid, slug in items[:40]:
        try:
            html = get(f"https://mixkit.co/free-stock-video/{slug}-{vid}/").decode("utf-8", "ignore")
            thumbs = re.findall(rf"https://assets\.mixkit\.co/videos/{vid}/[^\"']+?\.jpg", html)
            main = html[html.find("<main"):] if "<main" in html else html
            free = 'data-license="videoFree"' in main and 'data-license="videoRestricted"' not in main
            if not free:
                continue
            im = Image.open(io.BytesIO(get(thumbs[0]))).convert("RGB")
        except Exception:
            continue
        im.thumbnail((320, 320))
        t = Image.new("RGB", (320, 220), (20, 20, 20))
        t.paste(im, ((320 - im.width) // 2, 0))
        ImageDraw.Draw(t).text((4, 200), f"{vid} {slug[:34]}", font=f, fill=(255, 220, 0))
        tiles.append(t)
    if not tiles:
        return
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    s = Image.new("RGB", (cols * 320, rows * 220))
    for i, t in enumerate(tiles):
        s.paste(t, ((i % cols) * 320, (i // cols) * 220))
    s.save(f"{out}/sheet_{term}.jpg", quality=80)


if __name__ == "__main__":
    out = sys.argv[1]
    res = {}
    for term in sys.argv[2:]:
        try:
            items = search(term)
        except Exception as e:
            print(term, "ERR", e)
            continue
        res[term] = items
        print(term, len(items))
        sheet(term, items, out)
    json.dump(res, open(f"{out}/mixkit_candidates.json", "a"), indent=1)
