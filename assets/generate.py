"""Generate the profile README's SVG assets in light and dark variants.

Run: python assets/generate.py   (writes into assets/)
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

THEMES = {
    "dark": dict(
        bg1="#0b1220", bg2="#111a2e", border="#263248", text="#e6edf3", muted="#8b98a9",
        dot="#1c2840", teal="#2dd4bf", violet="#a78bfa", blue="#60a5fa",
        chip_bg="#152036", chip_border="#2a3a57", node_bg="#0f1a2e",
    ),
    "light": dict(
        bg1="#ffffff", bg2="#f3f6fb", border="#d0d7de", text="#1f2328", muted="#59636e",
        dot="#e3e8f0", teal="#0d9488", violet="#7c3aed", blue="#2563eb",
        chip_bg="#f6f8fa", chip_border="#d0d7de", node_bg="#ffffff",
    ),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
MONO_CHAR = 0.6  # monospace glyph width in em; keeps chip widths predictable


def chips(items, x, y, size, t, gap=10, pad=14, h=30):
    """Pill chips in a row; returns (svg, end_x)."""
    out = []
    for item in items:
        w = len(item) * size * MONO_CHAR + pad * 2
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" '
            f'fill="{t["chip_bg"]}" stroke="{t["chip_border"]}"/>'
            f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.35:.1f}" text-anchor="middle" '
            f'class="mono" font-size="{size}" fill="{t["text"]}">{escape(item)}</text>'
        )
        x += w + gap
    return "".join(out), x


def frame(w, h, t, body, css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
{css}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['teal']}"/><stop offset=".5" stop-color="{t['blue']}"/><stop offset="1" stop-color="{t['violet']}"/></linearGradient>
<clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['dot']}"/></pattern>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#frame)">{body}</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="{t['border']}"/>
</svg>
"""


def header(t):
    w, h = 1200, 360
    cx, cy, r = 960, 180, 108
    nodes = [("plan", 0, -1), ("retrieve", 1, 0), ("act", 0, 1), ("evaluate", -1, 0)]
    node_svg = []
    for label, dx, dy in nodes:
        nx, ny = cx + dx * r, cy + dy * r
        node_svg.append(
            f'<line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{t["chip_border"]}" stroke-width="1.5" class="flow"/>'
            f'<circle cx="{nx}" cy="{ny}" r="9" fill="{t["node_bg"]}" stroke="{t["teal"]}" stroke-width="2.5"/>'
        )
        if dy == -1:
            lx, ly, anchor = nx, ny - 22, "middle"
        elif dy == 1:
            lx, ly, anchor = nx, ny + 34, "middle"
        elif dx == 1:
            lx, ly, anchor = nx + 22, ny + 5, "start"
        else:
            lx, ly, anchor = nx - 22, ny + 5, "end"
        node_svg.append(
            f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" class="mono" font-size="15" fill="{t["muted"]}">{label}</text>'
        )
    tag_chips, _ = chips(["Agents", "RAG", "Voice", "Vision", "LLMOps"], 64, 262, 14, t)
    css = f"""
.flow {{ stroke-dasharray: 4 6; animation: flow 1.6s linear infinite; }}
@keyframes flow {{ to {{ stroke-dashoffset: -20; }} }}
.orbit {{ transform-origin: {cx}px {cy}px; animation: spin 9s linear infinite; }}
.orbit2 {{ transform-origin: {cx}px {cy}px; animation: spin 9s linear infinite; animation-delay: -4.5s; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.pulse {{ transform-origin: {cx}px {cy}px; animation: pulse 3s ease-in-out infinite; }}
@keyframes pulse {{ 50% {{ opacity: .35; transform: scale(1.12); }} }}
"""
    body = f"""
<rect x="700" y="1" width="499" height="{h-2}" rx="18" fill="url(#dots)" opacity=".9"/>
<rect x="0" y="0" width="{w}" height="5" fill="url(#accent)" rx="2"/>
<text x="64" y="86" class="mono" font-size="15" letter-spacing="2.5" fill="{t['teal']}">SENIOR AI SOLUTIONS ENGINEER · SINGAPORE</text>
<text x="62" y="156" class="sans" font-size="66" font-weight="700" fill="{t['text']}">Arshi Saxena</text>
<text x="64" y="202" class="sans" font-size="23" fill="{t['muted']}">Full-stack software engineer shipping</text>
<text x="64" y="234" class="sans" font-size="23" fill="{t['muted']}">production GenAI on <tspan fill="{t['text']}" font-weight="600">Azure</tspan>.</text>
{tag_chips}
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t['chip_border']}" stroke-width="1.5" stroke-dasharray="2 7"/>
<circle cx="{cx}" cy="{cy}" r="58" fill="{t['teal']}" opacity=".10" class="pulse"/>
{''.join(node_svg)}
<g class="orbit"><circle cx="{cx}" cy="{cy - r}" r="5" fill="{t['violet']}"/></g>
<g class="orbit2"><circle cx="{cx}" cy="{cy - r}" r="4" fill="{t['blue']}"/></g>
<rect x="{cx-50}" y="{cy-22}" width="100" height="44" rx="12" fill="{t['node_bg']}" stroke="url(#accent)" stroke-width="2"/>
<text x="{cx}" y="{cy+6}" text-anchor="middle" class="mono" font-size="17" font-weight="700" fill="{t['text']}">agent</text>
"""
    return frame(w, h, t, body, css)


def card(t, eyebrow, title, lines, tags):
    w, h = 600, 312
    text = "".join(
        f'<text x="36" y="{140 + i*28}" class="sans" font-size="19" fill="{t["muted"]}">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    tag_svg, _ = chips(tags, 36, 254, 13, t, gap=8, pad=11, h=28)
    body = f"""
<rect x="0" y="0" width="{w}" height="5" fill="url(#accent)" rx="2"/>
<text x="36" y="56" class="mono" font-size="13" letter-spacing="2" fill="{t['teal']}">{escape(eyebrow)}</text>
<text x="36" y="96" class="sans" font-size="30" font-weight="700" fill="{t['text']}">{escape(title)}</text>
<text x="{w-36}" y="96" text-anchor="end" class="sans" font-size="26" fill="{t['muted']}">↗</text>
{text}
{tag_svg}
"""
    return frame(w, h, t, body)


def chip_wrap(items, x, y, max_w, size, t, gap=8, pad=11, h=28, row_gap=8):
    """Chips that wrap onto new rows inside max_w; returns (svg, bottom_y)."""
    out, cx, cy = [], x, y
    for item in items:
        w = len(item) * size * MONO_CHAR + pad * 2
        if cx + w > x + max_w and cx > x:
            cx, cy = x, cy + h + row_gap
        svg, _ = chips([item], cx, cy, size, t, gap=gap, pad=pad, h=h)
        out.append(svg)
        cx += w + gap
    return "".join(out), cy + h


PRINCIPLES = [
    ("the model is the easy part", "so I build the system around it"),
    ("context is engineered", "hybrid search, reranking, metadata filters"),
    ("harness over hope", "schema-constrained output, deterministic checks"),
    ("evals before vibes", "golden sets and LLM-as-judge, gated in CI"),
    ("confidence from log-probs", "not the model's self-report"),
    ("humans confirm what matters", "human-in-the-loop by design"),
    ("secure by default", "OWASP LLM Top 10 guardrails, SAST in CI"),
    ("ship it", "production users, not notebooks"),
]


def terminal(t):
    """Animated eval run: lines appear one by one, hold, then the loop restarts."""
    w, size, step = 1200, 17, 34
    cw = size * MONO_CHAR
    rows = [("cmd", None), ("gap", None)] + [("ok", p) for p in PRINCIPLES] + [("gap", None), ("sum", None)]
    h = 104 + step * len(rows) - 6
    cycle, first, each = 18.0, 0.4, 0.75
    css, lines, y, i = [], [], 104, 0
    for kind, item in rows:
        if kind == "gap":
            y += step
            continue
        on = (first + i * each) / cycle * 100
        css.append(f".l{i} {{ animation: r{i} {cycle}s linear infinite; }} "
                   f"@keyframes r{i} {{ 0%, {on:.2f}% {{ opacity: 0; }} {on + 0.6:.2f}%, 95% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
        if kind == "cmd":
            body = (f'<tspan fill="{t["teal"]}">$</tspan> evals run '
                    f'<tspan fill="{t["violet"]}">--suite</tspan> arshi')
        elif kind == "ok":
            name, note = item
            body = (f'<tspan fill="{t["teal"]}">✓</tspan> <tspan font-weight="700">{escape(name)}</tspan>'
                    f'<tspan x="{56 + cw * 32:.1f}" fill="{t["muted"]}"># {escape(note)}</tspan>')
        else:
            n = len(PRINCIPLES)
            summary = f"{n}/{n} passed · 0 vibes-based releases"
            body = (f'<tspan fill="{t["teal"]}" font-weight="700">{n}/{n} passed</tspan>'
                    f'<tspan fill="{t["muted"]}"> · 0 vibes-based releases</tspan>')
            cur_x = 56 + cw * (len(summary) + 1)
            css.append(".cur { animation: blink 1s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } }")
            lines.append(f'<g class="l{i}"><rect class="cur" x="{cur_x:.1f}" y="{y - size + 3}" '
                         f'width="{cw:.1f}" height="{size + 2}" fill="{t["teal"]}"/></g>')
        lines.append(f'<text x="56" y="{y}" class="mono l{i}" font-size="{size}" fill="{t["text"]}">{body}</text>')
        y += step
        i += 1
    dots = "".join(f'<circle cx="{32 + k * 22}" cy="26" r="6.5" fill="{c}"/>'
                   for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    body = f"""
<rect x="0" y="0" width="{w}" height="52" fill="{t['chip_bg']}"/>
<line x1="0" y1="52" x2="{w}" y2="52" stroke="{t['border']}"/>
{dots}
<text x="{w / 2}" y="31" text-anchor="middle" class="mono" font-size="14" fill="{t['muted']}">~/arshi — how I build</text>
{''.join(lines)}
"""
    return frame(w, h, t, body, "\n".join(css))


SYSTEM = [
    ("CONTEXT ENGINEERING", ["Agentic RAG", "Hybrid search", "Semantic reranking", "Metadata filters", "Azure AI Search"]),
    ("HARNESS ENGINEERING", ["Guardrails", "Structured output", "Deterministic validation", "State machines", "Human-in-the-loop"]),
    ("EVALS & LLMOPS", ["Golden sets", "LLM-as-judge", "promptfoo", "Langfuse", "OWASP LLM Top 10"]),
    ("AGENTS", ["LangGraph", "Azure AI Foundry", "ReAct", "Tool use", "Multi-agent"]),
    ("VOICE & VISION", ["Realtime voice", "Azure Speech", "Document Intelligence", "YOLO", "PyTorch", "OpenCV"]),
    ("THE APP AROUND IT", ["FastAPI", "React", "Angular", "Spring Boot", "PostgreSQL", "Entra ID"]),
]
SHIPS_ON = ["Azure", "AWS", "Docker", "Kubernetes", "Azure DevOps", "GitHub Actions"]


def system(t):
    """The system around the model: capability cards wired to a small LLM box."""
    w, pad, gap = 1200, 40, 30
    cw, ch = (w - 2 * pad - 2 * gap) / 3, 186
    r1 = 84
    r2 = r1 + ch + 116
    bx, by, bw, bh = w / 2 - 150, r1 + ch + 30, 300, 56
    cards, wires = [], []
    for k, (title, items) in enumerate(SYSTEM):
        col, top_row = k % 3, k < 3
        x, y = pad + col * (cw + gap), (r1 if top_row else r2)
        chip_svg, bottom = chip_wrap(items, x + 20, y + 54, cw - 40, 13, t)
        assert bottom < y + ch - 10, f"{title} overflows card"
        cards.append(
            f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="14" fill="{t["node_bg"]}" stroke="{t["chip_border"]}"/>'
            f'<text x="{x + 20:.1f}" y="{y + 34}" class="mono" font-size="13" letter-spacing="2" fill="{t["teal"]}">{escape(title)}</text>'
            + chip_svg)
        ax = x + cw / 2
        ay, ty = (y + ch, by) if top_row else (y, by + bh)
        tx = bx + bw / 2 + (col - 1) * 90
        my = (ay + ty) / 2
        wires.append(f'<path d="M{ax:.1f},{ay} C{ax:.1f},{my:.1f} {tx:.1f},{my:.1f} {tx:.1f},{ty}" '
                     f'fill="none" stroke="{t["muted"]}" stroke-opacity=".55" stroke-width="1.5" class="flow"/>')
    ship_y = r2 + ch + 34
    ship_svg, _ = chips(SHIPS_ON, 190, ship_y, 13, t, gap=8, pad=11, h=28)
    h = ship_y + 28 + 30
    css = """
.flow { stroke-dasharray: 4 6; animation: flow 1.6s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -20; } }
"""
    body = f"""
<rect x="0" y="0" width="{w}" height="{h}" fill="url(#dots)" opacity=".7"/>
<rect x="0" y="0" width="{w}" height="5" fill="url(#accent)" rx="2"/>
<text x="{pad}" y="52" class="mono" font-size="14" letter-spacing="2.5" fill="{t['teal']}">THE SYSTEM AROUND THE MODEL</text>
<text x="{w - pad}" y="52" text-anchor="end" class="sans" font-size="17" font-style="italic" fill="{t['muted']}">everything that makes an LLM safe to ship</text>
{''.join(wires)}
{''.join(cards)}
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{t['node_bg']}" stroke="url(#accent)" stroke-width="2"/>
<text x="{w / 2}" y="{by + 25}" text-anchor="middle" class="mono" font-size="17" font-weight="700" fill="{t['text']}">LLM</text>
<text x="{w / 2}" y="{by + 44}" text-anchor="middle" class="mono" font-size="12" fill="{t['muted']}">Azure OpenAI · Claude</text>
<text x="{pad}" y="{ship_y + 19}" class="mono" font-size="13" letter-spacing="2" fill="{t['teal']}">SHIPS ON</text>
{ship_svg}
"""
    return frame(w, round(h), t, body, css)


def button(t, label):
    """Small link button; the README wraps it in an <a>."""
    w, h = 64 + len(label) * 15 * MONO_CHAR + 40, 52
    body = f"""
<rect x="0" y="0" width="5" height="{h}" fill="url(#accent)"/>
<text x="30" y="{h/2 + 5.5}" class="mono" font-size="15" font-weight="700" fill="{t['text']}">{escape(label)}</text>
<text x="{w-24}" y="{h/2 + 7}" text-anchor="end" class="sans" font-size="20" fill="{t['teal']}">↗</text>
"""
    return frame(round(w), h, t, body).replace('rx="18"', 'rx="12"')


CARDS = {
    "card-ad-generator": dict(
        eyebrow="AGENTS · NUS-ISS 2026",
        title="Ad Generator Agent",
        lines=[
            "LangGraph agent on Claude with a bounded ReAct loop,",
            "human-in-the-loop interrupt and layered guardrails.",
            "Every merge gated on pytest and promptfoo evals,",
            "including prompt-injection tests.",
        ],
        tags=["LangGraph", "Claude", "FastAPI", "AWS EKS", "promptfoo"],
    ),
    "card-apneasense": dict(
        eyebrow="MULTIMODAL · NUS-ISS 2026",
        title="ApneaSense",
        lines=[
            "Sleep apnea screening from one overnight video:",
            "audio spectrogram classification and self-attention",
            "fusion of RGB, depth and pose for sleep posture.",
            "Shipped as a Streamlit app.",
        ],
        tags=["PyTorch", "ResNet18", "YOLOv8-pose", "Depth Anything"],
    ),
}

if __name__ == "__main__":
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"terminal-{name}.svg").write_text(terminal(t), encoding="utf-8")
        (OUT / f"system-{name}.svg").write_text(system(t), encoding="utf-8")
        (OUT / f"linkedin-{name}.svg").write_text(button(t, "Connect on LinkedIn"), encoding="utf-8")
        for key, c in CARDS.items():
            (OUT / f"{key}-{name}.svg").write_text(card(t, **c), encoding="utf-8")
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
