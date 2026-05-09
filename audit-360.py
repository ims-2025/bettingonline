#!/usr/bin/env python3
"""360-degree audit of the website. Outputs structured findings."""
import re
import json
import collections
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://www.bettingonline.org"


def text_word_count(html):
    txt = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    txt = re.sub(r'<style[^>]*>.*?</style>', '', txt, flags=re.DOTALL)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    return len(re.findall(r"\b[\w'\-]+\b", txt))


def main():
    pages = [p for p in ROOT.rglob('*.html') if 'node_modules' not in str(p)]
    print(f"=== AUDIT 360 — {len(pages)} HTML pages ===\n")

    # ===== 1. CONTENT DEPTH =====
    print("1. CONTENT DEPTH")
    word_counts = {}
    for p in pages:
        try:
            wc = text_word_count(p.read_text(errors='ignore'))
            word_counts[str(p.relative_to(ROOT))] = wc
        except Exception:
            pass

    buckets = {'<200': 0, '200-499': 0, '500-999': 0, '1000-1999': 0, '2000-3999': 0, '4000+': 0}
    for wc in word_counts.values():
        if wc < 200: buckets['<200'] += 1
        elif wc < 500: buckets['200-499'] += 1
        elif wc < 1000: buckets['500-999'] += 1
        elif wc < 2000: buckets['1000-1999'] += 1
        elif wc < 4000: buckets['2000-3999'] += 1
        else: buckets['4000+'] += 1
    for k, v in buckets.items():
        print(f"  {k.ljust(12)} {v} pages")

    thin = sorted([(p, wc) for p, wc in word_counts.items() if wc < 200])[:15]
    if thin:
        print(f"\n  Thinnest pages (under 200 words):")
        for p, wc in thin:
            print(f"    {wc:>4}w  {p}")

    # ===== 2. TITLE TAG ANALYSIS =====
    print("\n2. TITLE TAGS")
    title_lengths = []
    no_title = 0
    duplicates = collections.Counter()
    for p in pages:
        txt = p.read_text(errors='ignore')
        m = re.search(r'<title>([^<]+)</title>', txt)
        if not m:
            no_title += 1
            continue
        t = m.group(1).strip()
        title_lengths.append(len(t))
        duplicates[t] += 1

    short = sum(1 for l in title_lengths if l < 30)
    optimal = sum(1 for l in title_lengths if 30 <= l <= 65)
    long = sum(1 for l in title_lengths if l > 65)
    print(f"  Pages without <title>: {no_title}")
    print(f"  Short (<30 chars): {short}")
    print(f"  Optimal (30-65):   {optimal}")
    print(f"  Long (>65):        {long}")
    dup_titles = [(t, c) for t, c in duplicates.items() if c > 1]
    print(f"  Duplicate titles: {len(dup_titles)}")
    if dup_titles[:5]:
        for t, c in dup_titles[:5]:
            print(f"    {c}× '{t[:80]}'")

    # ===== 3. META DESCRIPTIONS =====
    print("\n3. META DESCRIPTIONS")
    desc_lengths = []
    no_desc = 0
    desc_dupes = collections.Counter()
    for p in pages:
        txt = p.read_text(errors='ignore')
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', txt)
        if not m:
            no_desc += 1
            continue
        d = m.group(1)
        desc_lengths.append(len(d))
        desc_dupes[d[:50]] += 1

    short = sum(1 for l in desc_lengths if l < 100)
    optimal = sum(1 for l in desc_lengths if 100 <= l <= 160)
    long = sum(1 for l in desc_lengths if l > 160)
    print(f"  Pages without description: {no_desc}")
    print(f"  Short (<100): {short}")
    print(f"  Optimal (100-160): {optimal}")
    print(f"  Long (>160): {long}")
    dup_descs = [(d, c) for d, c in desc_dupes.items() if c > 1]
    print(f"  Duplicate descriptions (first 50 chars): {len(dup_descs)}")

    # ===== 4. H1 COVERAGE =====
    print("\n4. H1 TAGS")
    no_h1 = 0
    multi_h1 = 0
    for p in pages:
        txt = p.read_text(errors='ignore')
        h1s = re.findall(r'<h1[^>]*>', txt, re.IGNORECASE)
        if len(h1s) == 0:
            no_h1 += 1
        elif len(h1s) > 1:
            multi_h1 += 1
    print(f"  Pages without H1: {no_h1}")
    print(f"  Pages with multiple H1: {multi_h1}")

    # ===== 5. SCHEMA COVERAGE =====
    print("\n5. STRUCTURED DATA (JSON-LD)")
    schema_types = collections.Counter()
    no_schema = 0
    for p in pages:
        txt = p.read_text(errors='ignore')
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.DOTALL)
        if not blocks:
            no_schema += 1
            continue
        for b in blocks:
            try:
                obj = json.loads(b)
                t = obj.get('@type', 'Unknown')
                if isinstance(t, list): t = t[0]
                schema_types[t] += 1
            except Exception:
                schema_types['INVALID'] += 1
    print(f"  Pages without any schema: {no_schema}")
    print(f"  Schema type distribution:")
    for t, c in schema_types.most_common(15):
        print(f"    {c:>5}  {t}")

    # ===== 6. CANONICAL COVERAGE =====
    print("\n6. CANONICAL URLS")
    no_canonical = 0
    non_self = 0
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        txt = p.read_text(errors='ignore')
        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', txt)
        if not m:
            no_canonical += 1
            continue
        canonical = m.group(1)
        # Self-canonical heuristic: URL must contain the page path
        path_only = rel.replace('/index.html', '/').replace('index.html', '')
        if not (path_only in canonical or path_only == 'index.html'):
            if rel != 'index.html' and rel != '404.html':
                non_self += 1
    print(f"  Pages without canonical: {no_canonical}")
    print(f"  Pages with non-self canonical: {non_self}")

    # ===== 7. INTERNAL LINK DEPTH =====
    print("\n7. INTERNAL LINKING")
    incoming = collections.Counter()
    outgoing = []
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        txt = p.read_text(errors='ignore')
        # Count outgoing internal links
        links = re.findall(r'href=["\']([^"\']+)["\']', txt)
        internal_links = [l for l in links if not l.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '//'))]
        outgoing.append((rel, len(internal_links)))
        for l in internal_links:
            incoming[l] += 1

    avg_out = sum(c for _, c in outgoing) / len(outgoing) if outgoing else 0
    print(f"  Average outgoing internal links per page: {avg_out:.1f}")
    sparse = sorted([(p, c) for p, c in outgoing if c < 5])[:5]
    if sparse:
        print(f"  Pages with very few internal links (<5):")
        for p, c in sparse:
            print(f"    {c} links  {p}")

    # ===== 8. IMAGE ALT TEXT =====
    print("\n8. IMAGES")
    img_no_alt = 0
    img_total = 0
    for p in pages:
        txt = p.read_text(errors='ignore')
        for m in re.finditer(r'<img\b[^>]*>', txt):
            img_total += 1
            if 'alt=' not in m.group(0):
                img_no_alt += 1
    print(f"  Total <img> tags: {img_total}")
    print(f"  Without alt attribute: {img_no_alt}")

    # ===== 9. TYPES OF PAGES =====
    print("\n9. PAGE TYPES (by directory)")
    types = collections.Counter()
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        if '/' in rel:
            types[rel.split('/')[0]] += 1
        else:
            types['(root)'] += 1
    for t, c in types.most_common(20):
        print(f"  {c:>4}  {t}/")

    # ===== 10. AUTHOR/E-E-A-T =====
    print("\n10. E-E-A-T (Author bylines)")
    has_byline = 0
    has_updated_stamp = 0
    for p in pages:
        txt = p.read_text(errors='ignore')
        if 'class="byline' in txt or 'authors/' in txt:
            has_byline += 1
        if re.search(r'(Last\s+updated|Updated\s+\w+\s+\d{4}|datePublished|dateModified)', txt, re.IGNORECASE):
            has_updated_stamp += 1
    print(f"  Pages with author byline: {has_byline}/{len(pages)}")
    print(f"  Pages with updated/date stamp: {has_updated_stamp}/{len(pages)}")

    # ===== 11. BREADCRUMBS =====
    print("\n11. BREADCRUMBS")
    no_breadcrumbs = 0
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        if rel in ('index.html', '404.html'):
            continue
        txt = p.read_text(errors='ignore')
        if 'class="crumbs"' not in txt and '"BreadcrumbList"' not in txt:
            no_breadcrumbs += 1
    print(f"  Non-root pages without breadcrumb: {no_breadcrumbs}")

    # ===== 12. COMMON ON-PAGE GAPS =====
    print("\n12. ON-PAGE OPPORTUNITIES")
    no_internal_links_in_body = 0
    no_faq = 0
    no_table_of_contents = 0
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        # Skip utility pages
        if any(rel.endswith(s) for s in ('404.html', 'sitemap.html')):
            continue
        txt = p.read_text(errors='ignore')
        # Pages > 1000 words without FAQ
        wc = word_counts.get(rel, 0)
        if wc > 1000 and 'FAQPage' not in txt:
            no_faq += 1
    print(f"  Substantive pages (>1000w) without FAQPage schema: {no_faq}")

    # ===== 13. SITEMAP / SEARCH-INDEX SYNC =====
    print("\n13. SITEMAP & SEARCH INDEX")
    sitemap = ROOT / 'sitemap.xml'
    if sitemap.exists():
        urls = re.findall(r'<loc>([^<]+)</loc>', sitemap.read_text())
        print(f"  Sitemap entries: {len(urls)}")
    si = ROOT / 'assets/js/search-index.json'
    if si.exists():
        data = json.loads(si.read_text())
        print(f"  Search index entries: {len(data)}")

    # ===== 14. CSS/JS ASSET SIZE =====
    print("\n14. ASSET WEIGHTS")
    for f in ['assets/css/main.css', 'assets/css/main.min.css', 'assets/js/main.js', 'assets/js/search-index.json']:
        p = ROOT / f
        if p.exists():
            print(f"  {f.ljust(40)} {p.stat().st_size // 1024} KB")

    # ===== 15. REVIEW SCHEMA / RICH RESULTS COVERAGE =====
    print("\n15. RICH RESULT SCHEMA TYPES")
    review_count = sum(c for t, c in schema_types.items() if t in ('Review', 'AggregateRating', 'Product'))
    faq_count = schema_types.get('FAQPage', 0)
    article_count = schema_types.get('Article', 0)
    howto_count = schema_types.get('HowTo', 0)
    person_count = schema_types.get('Person', 0)
    print(f"  Article schema:        {article_count}")
    print(f"  FAQPage schema:        {faq_count}")
    print(f"  HowTo schema:          {howto_count}")
    print(f"  Review/Aggregate/Prod: {review_count}")
    print(f"  Person schema:         {person_count}")
    print(f"  BreadcrumbList:        {schema_types.get('BreadcrumbList', 0)}")
    print(f"  Organization:          {schema_types.get('Organization', 0)}")
    print(f"  WebSite:               {schema_types.get('WebSite', 0)}")
    print(f"  CollectionPage:        {schema_types.get('CollectionPage', 0)}")
    print(f"  ItemList:              {schema_types.get('ItemList', 0)}")
    print(f"  DefinedTermSet:        {schema_types.get('DefinedTermSet', 0)}")


if __name__ == "__main__":
    main()
