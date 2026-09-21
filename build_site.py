#!/usr/bin/env python3
"""Render index.html from projects.json. Add a project to the JSON, re-run this."""
import json, html, pathlib

D = json.load(open(pathlib.Path(__file__).parent / "projects.json"))
U = D["user"]
ALL = [p for g in D["groups"] for p in g["projects"]]

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#0f1419; --bg2:#0c1116; --panel:#171d24; --panel2:#1b2229; --line:#2a333f;
  --text:#e6edf3; --dim:#c5d1dd; --muted:#8b98a5;
  --accent:#4c9aff; --accent-soft:#9dc4ff;
  --good:#35b77d; --warn:#e0a33e; --bad:#e05c5c;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);
     line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:0 28px}
a{color:var(--accent-soft);text-decoration:none}
a:hover{text-decoration:underline}

/* ---- nav ---- */
nav{position:sticky;top:0;z-index:20;background:rgba(12,17,22,.88);
    backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;gap:26px;height:56px}
nav .who{font-weight:650;letter-spacing:-.01em;margin-right:auto;color:var(--text)}
nav a.nl{color:var(--muted);font-size:.9rem}
nav a.nl:hover{color:var(--text);text-decoration:none}
@media(max-width:700px){nav a.nl{display:none}}

/* ---- hero ---- */
header{padding:76px 0 52px;border-bottom:1px solid var(--line);
  background:radial-gradient(1000px 420px at 12% -8%, rgba(76,154,255,.13), transparent 62%)}
.role{color:var(--accent);font-family:var(--mono);font-size:.82rem;
  letter-spacing:.14em;text-transform:uppercase;margin:0 0 18px}
h1{font-size:clamp(2.1rem,5.2vw,3.1rem);line-height:1.1;margin:0 0 16px;
   letter-spacing:-.025em;font-weight:660}
.lede{font-size:1.13rem;color:var(--dim);max-width:60ch;margin:0}
.meta{color:var(--muted);font-size:.95rem;max-width:60ch;margin:16px 0 0}
.links{margin-top:30px;display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:10px 17px;border:1px solid var(--line);border-radius:8px;
  background:var(--panel);color:var(--text);font-size:.92rem;
  transition:border-color .15s,background .15s,transform .15s}
.btn:hover{border-color:var(--accent);background:var(--panel2);text-decoration:none;transform:translateY(-1px)}
.btn.primary{border-color:#3a6aa8;background:linear-gradient(180deg,#1b2d47,#152337);color:#fff}

/* stat strip */
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;
  overflow:hidden;margin-top:40px}
.strip div{background:var(--bg2);padding:16px 18px}
.strip b{display:block;font-size:1.32rem;font-weight:660;letter-spacing:-.01em}
.strip span{color:var(--muted);font-size:.8rem;font-family:var(--mono);letter-spacing:.04em}

/* ---- sections ---- */
section{padding:64px 0 8px;border-bottom:1px solid var(--line)}
section:last-of-type{border-bottom:0}
h2{font-size:.8rem;font-family:var(--mono);letter-spacing:.14em;text-transform:uppercase;
   color:var(--accent);margin:0 0 8px;font-weight:600}
.h2note{color:var(--muted);font-size:1rem;margin:0 0 6px;max-width:64ch}
h3.grp{font-size:1.02rem;font-weight:640;color:var(--text);margin:38px 0 2px;
  padding-top:22px;border-top:1px solid var(--line)}
h3.grp:first-of-type{border-top:0;padding-top:0;margin-top:30px}
.grpnote{color:var(--muted);font-size:.92rem;margin:0 0 18px}

/* ---- project cards ---- */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
.card{background:linear-gradient(180deg,var(--panel),#141a21);border:1px solid var(--line);
  border-radius:12px;padding:24px 26px 22px;display:flex;flex-direction:column;
  transition:border-color .18s,transform .18s}
.card:hover{border-color:#41536a;transform:translateY(-2px)}
.card h4{margin:0 0 6px;font-size:1.14rem;font-weight:640;letter-spacing:-.01em}
.card h4 a{color:var(--text)}
.card h4 a:hover{color:var(--accent-soft);text-decoration:none}
.q{color:var(--accent-soft);font-size:.89rem;font-style:italic;margin:0 0 14px;opacity:.9}
.finding{margin:0 0 18px;color:var(--dim);font-size:.96rem}
.finding strong{color:var(--text);font-weight:640}
.mrow{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 18px}
.m{background:#10161c;border:1px solid var(--line);border-radius:8px;padding:10px 11px}
.m b{display:block;font-size:1.02rem;font-weight:660;letter-spacing:-.01em;line-height:1.25}
.m.good b{color:var(--good)} .m.warn b{color:var(--warn)} .m.bad b{color:var(--bad)}
.m span{display:block;color:var(--muted);font-size:.72rem;line-height:1.4;margin-top:3px}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px}
.tag{font-size:.75rem;font-family:var(--mono);color:var(--muted);
  border:1px solid var(--line);border-radius:5px;padding:3px 8px;background:#10161c}
.cardlinks{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}
.chip{font-size:.84rem;padding:6px 12px;border-radius:7px;border:1px solid var(--line);
  background:#10161c;color:var(--accent-soft);transition:border-color .15s,background .15s}
.chip:hover{border-color:var(--accent);background:#15243a;text-decoration:none}
.chip.live::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;
  background:var(--good);margin-right:7px;vertical-align:1px}

/* ---- skills ---- */
.skills{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}
.sk{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.sk h5{margin:0 0 12px;font-size:.78rem;font-family:var(--mono);letter-spacing:.1em;
  text-transform:uppercase;color:var(--accent);font-weight:600}
.sk ul{margin:0;padding:0;list-style:none}
.sk li{color:var(--dim);font-size:.9rem;padding:4px 0 4px 15px;position:relative}
.sk li::before{content:"";position:absolute;left:0;top:13px;width:5px;height:5px;
  border-radius:50%;background:#3d4c5e}

/* ---- misc ---- */
pre{background:var(--bg2);border:1px solid var(--line);border-radius:10px;
  padding:20px 22px;overflow-x:auto;font-family:var(--mono);font-size:.85rem;
  color:var(--dim);line-height:1.75;margin:24px 0}
.cmt{color:var(--muted)}
p{max-width:68ch;color:var(--dim)}
blockquote{margin:24px 0;padding:14px 20px;border-left:3px solid var(--warn);
  background:rgba(224,163,62,.05);border-radius:0 8px 8px 0}
blockquote p{margin:0;font-size:.94rem;color:var(--dim)}
code{font-family:var(--mono);font-size:.88em;background:#10161c;border:1px solid var(--line);
  border-radius:4px;padding:1px 5px}
footer{padding:44px 0 60px;color:var(--muted);font-size:.9rem}
footer a{color:var(--muted);text-decoration:underline}
"""

def card(p):
    ms = "".join(
        f'<div class="m {m.get("tone","")}"><b>{html.escape(m["v"])}</b>'
        f'<span>{html.escape(m["l"])}</span></div>' for m in p["metrics"])
    tg = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in p["tags"])
    return f"""      <article class="card">
        <h4><a href="https://github.com/{U}/{p['repo']}">{html.escape(p['title'])}</a></h4>
        <p class="q">{html.escape(p['q'])}</p>
        <div class="mrow">{ms}</div>
        <p class="finding">{p['finding']}</p>
        <div class="tags">{tg}</div>
        <div class="cardlinks">
          <a class="chip live" href="https://{U}.github.io/{p['repo']}/dashboard/">Live dashboard</a>
          <a class="chip" href="https://github.com/{U}/{p['repo']}">Code and docs</a>
        </div>
      </article>"""

groups = "".join(
    f'\n    <h3 class="grp">{html.escape(g["label"])}</h3>\n'
    f'    <p class="grpnote">{html.escape(g["blurb"])}</p>\n'
    f'    <div class="grid">\n' + "\n".join(card(p) for p in g["projects"]) + "\n    </div>"
    for g in D["groups"])

skills = "".join(
    f'<div class="sk"><h5>{html.escape(s["group"])}</h5><ul>'
    + "".join(f"<li>{html.escape(i)}</li>" for i in s["items"])
    + "</ul></div>" for s in D["skills"])

STRIP = [("%d" % len(ALL), "end-to-end projects"), ("%d" % len(ALL), "live dashboards"),
         ("115k+", "synthetic records"), ("4", "BI outputs each"), ("100%", "synthetic data")]
strip = "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v, l in STRIP)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sahra Fanousi — Healthcare Operations Analytics</title>
<meta name="description" content="Healthcare appeals analyst. {len(ALL)} end-to-end analytics projects on synthetic payer operations data: SQL, Power BI, Tableau, and live dashboards.">
<meta property="og:title" content="Sahra Fanousi — Healthcare Operations Analytics">
<meta property="og:description" content="{len(ALL)} end-to-end analytics projects on synthetic payer operations data.">
<meta property="og:type" content="website">
<style>{CSS}</style>
</head>
<body>

<nav><div class="wrap">
  <span class="who">Sahra Fanousi</span>
  <a class="nl" href="#work">Work</a>
  <a class="nl" href="#skills">Skills</a>
  <a class="nl" href="#built">How it's built</a>
  <a class="nl" href="#data">About the data</a>
  <a class="nl" href="https://github.com/{U}">GitHub</a>
</div></nav>

<header><div class="wrap">
  <p class="role">Healthcare operations · Business analysis · Analytics</p>
  <h1>I find where operational<br>work loses time and money.</h1>
  <p class="lede">I work appeals on the operations side of a payer — intake through
  adjudication — and I build the SQL and reporting that operations leaders use to
  decide where to put people and money.</p>
  <p class="meta">Finishing an M.S. in Business Analytics and AI at Lamar University
  (May 2027). Based in Texas, open to remote analyst and BI roles.</p>
  <div class="links">
    <a class="btn primary" href="#work">See the work</a>
    <a class="btn" href="https://github.com/{U}">GitHub</a>
    <a class="btn" href="mailto:careersahrafanousi@gmail.com">careersahrafanousi@gmail.com</a>
  </div>
  <div class="strip">{strip}</div>
</div></header>

<section id="work"><div class="wrap">
  <h2>Portfolio</h2>
  <p class="h2note">{len(ALL)} end-to-end projects on fully synthetic healthcare data. Each one ships
  runnable code, a data-quality gate that excludes bad records rather than quietly fixing
  them, SQL analysis, a live dashboard, and the business-analysis documents that turn a
  finding into something a team can implement.</p>
  {groups}
</div></section>

<section id="skills"><div class="wrap">
  <h2>Skills</h2>
  <p class="h2note">Every item below is used in at least one project in this portfolio, not just listed.</p>
  <div class="skills">{skills}</div>
</div></section>

<section id="built"><div class="wrap">
  <h2>How it's built</h2>
  <p class="h2note">Every repository runs the same way from a clean clone:</p>
<pre>python src/generate_data.py    <span class="cmt"># synthetic source files</span>
python src/dq_checks.py       <span class="cmt"># data-quality gate</span>
python src/load_sqlite.py     <span class="cmt"># star schema</span>
python src/build_dashboard.py <span class="cmt"># interactive HTML</span>
python src/build_bi_assets.py <span class="cmt"># Excel, Tableau, Power BI, charts</span></pre>
  <p>The last step is the part worth a conversation. One file of SQL is the single
  definition of every number, and one generator renders it into five outputs: the
  interactive dashboard, an Excel workbook with native charts, a Tableau workbook, a
  Power BI semantic model in TMDL with DAX measures, and static PNG charts. Change a
  query and every artifact changes with it, so the dashboard and the workbook cannot
  drift apart.</p>
  <blockquote><p>There are no <code>.pbix</code> or <code>.twbx</code> files in these
  repositories, deliberately. A binary workbook cannot be diffed, cannot be reviewed in a
  pull request, cannot be opened without a licence, and carries its own copy of the data
  that drifts from the source. The Tableau XML and Power BI TMDL are committed as readable
  text instead.</p></blockquote>
</div></section>

<section id="data"><div class="wrap">
  <h2>About the data</h2>
  <p>All {len(ALL)} projects use fully synthetic data generated by the scripts in each repository.
  They do not use employer data, patient information, protected health information, or
  confidential business information. The operational patterns are modeled on real ones;
  the records are not real.</p>
</div></section>

<footer><div class="wrap">
  Built and maintained by Sahra Fanousi ·
  <a href="https://github.com/{U}">github.com/{U}</a> ·
  <a href="mailto:careersahrafanousi@gmail.com">careersahrafanousi@gmail.com</a>
</div></footer>

</body>
</html>
"""
out = pathlib.Path(__file__).parent / "index.html"
out.write_text(HTML)
print(f"wrote {out} ({len(HTML)} bytes, {len(ALL)} projects, {len(D['groups'])} groups)")
