#!/usr/bin/env python3
"""
Generate GPT_Papers_Diagram.svg
True vector diagram: boxes, arrowheads, tracks, year timeline
Output: 03_GPT_Evolution_and_Alignment/GPT_Papers_Diagram.svg
"""

# ── Palette ──────────────────────────────────────────────────────────────────
BG    = '#0f172a'
CARD  = '#1e293b'
FOUND = '#a78bfa'   # purple  – foundation
GPT   = '#38bdf8'   # blue    – gpt series
ENC   = '#34d399'   # teal    – encoder
ALIGN = '#fb923c'   # orange  – alignment
TEXT  = '#f1f5f9'
SUB   = '#94a3b8'

# ── Canvas & card geometry ────────────────────────────────────────────────────
VW, VH = 1800, 1250
CW, CH = 262, 122   # card width / height

def top(cy): return cy - CH // 2
def bot(cy): return cy + CH // 2
def lft(cx): return cx - CW // 2
def rgt(cx): return cx + CW // 2
def cid(c):  return {FOUND:'f', GPT:'g', ENC:'e', ALIGN:'a'}[c]

# ── Column X centres ──────────────────────────────────────────────────────────
GPT_X = 220
ENC_X = 535
AL1_X = 880    # InstructGPT / RLAIF
AL2_X = 1185   # HH-RLHF / DPO
AL3_X = 1500   # Constitutional AI / SELF-REFINE

# ── Year row Y centres ────────────────────────────────────────────────────────
Y17, Y18, Y19, Y20, Y22, Y23 = 195, 370, 545, 720, 935, 1110

# ── SVG buffer ───────────────────────────────────────────────────────────────
buf = []
def e(s): buf.append(s)

# ────────────────────────────────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────────────────────────────────
def card(cx, cy, color, title, byline, ln1, ln2, badge_text=None, badge_color=None):
    x, y = lft(cx), top(cy)
    hh = 38       # header stripe height
    e(f'<!-- {title} -->')
    e(f'<rect x="{x-5}" y="{y-5}" width="{CW+10}" height="{CH+10}" '
      f'rx="14" fill="{color}" fill-opacity="0.10"/>')
    e(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" '
      f'rx="10" fill="{CARD}" stroke="{color}" stroke-width="2.2"/>')
    e(f'<rect x="{x+4}" y="{y+4}" width="{CW-8}" height="{hh}" '
      f'rx="8" fill="{color}" fill-opacity="0.90"/>')
    # title
    e(f'<text x="{cx}" y="{y+28}" text-anchor="middle" '
      f'font-family="\'Courier New\',monospace" font-size="13.5" '
      f'font-weight="bold" fill="white">{title}</text>')
    # byline
    e(f'<text x="{cx}" y="{y+56}" text-anchor="middle" '
      f'font-family="system-ui,sans-serif" font-size="10.5" fill="{color}">{byline}</text>')
    # contribution lines
    e(f'<text x="{cx}" y="{y+75}" text-anchor="middle" '
      f'font-family="system-ui,sans-serif" font-size="10" fill="{SUB}">{ln1}</text>')
    e(f'<text x="{cx}" y="{y+93}" text-anchor="middle" '
      f'font-family="system-ui,sans-serif" font-size="10" fill="{SUB}">{ln2}</text>')
    # optional outcome badge
    if badge_text:
        bc = badge_color or color
        bw = len(badge_text) * 7 + 18
        bx = rgt(cx) - bw - 4
        by = bot(cy) - 22
        e(f'<rect x="{bx}" y="{by}" width="{bw}" height="18" rx="5" '
          f'fill="{bc}" fill-opacity="0.18" stroke="{bc}" stroke-width="1.2"/>')
        e(f'<text x="{bx+bw//2}" y="{by+13}" text-anchor="middle" '
          f'font-family="system-ui,sans-serif" font-size="9.5" '
          f'font-weight="bold" fill="{bc}">{badge_text}</text>')


def vline(cx, y1, y2, color, label=''):
    """Straight vertical arrow."""
    e(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" '
      f'stroke="{color}" stroke-width="2.2" '
      f'marker-end="url(#ah-{cid(color)})"/>')
    if label:
        e(f'<text x="{cx+10}" y="{(y1+y2)//2+5}" '
          f'font-family="system-ui,sans-serif" font-size="11" fill="{color}">{label}</text>')


def bezier(x1, y1, x2, y2, color, c1x, c1y, c2x, c2y,
           lw=2.5, dashed=False, label='', lbx=None, lby=None):
    """Cubic bezier arrow."""
    dash = ' stroke-dasharray="7,4"' if dashed else ''
    e(f'<path d="M {x1},{y1} C {c1x},{c1y} {c2x},{c2y} {x2},{y2}" '
      f'fill="none" stroke="{color}" stroke-width="{lw}"{dash} '
      f'marker-end="url(#ah-{cid(color)})"/>')
    if label:
        tx = lbx if lbx is not None else (x1 + x2) // 2
        ty = lby if lby is not None else min(y1, y2) - 16
        e(f'<rect x="{tx-58}" y="{ty-16}" width="116" height="22" rx="5" '
          f'fill="{BG}" fill-opacity="0.95" stroke="{color}" stroke-width="0.6" stroke-opacity="0.4"/>')
        e(f'<text x="{tx}" y="{ty}" text-anchor="middle" '
          f'font-family="system-ui,sans-serif" font-size="11" '
          f'font-weight="bold" fill="{color}">{label}</text>')

# ════════════════════════════════════════════════════════════════════════════
# SVG DOCUMENT
# ════════════════════════════════════════════════════════════════════════════
e(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<defs>
  <!-- Arrowhead markers for each track colour -->
  <marker id="ah-f" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="9" markerHeight="9" orient="auto">
    <path d="M 0 1 L 11 6 L 0 11 Z" fill="{FOUND}"/>
  </marker>
  <marker id="ah-g" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="9" markerHeight="9" orient="auto">
    <path d="M 0 1 L 11 6 L 0 11 Z" fill="{GPT}"/>
  </marker>
  <marker id="ah-e" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="9" markerHeight="9" orient="auto">
    <path d="M 0 1 L 11 6 L 0 11 Z" fill="{ENC}"/>
  </marker>
  <marker id="ah-a" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="9" markerHeight="9" orient="auto">
    <path d="M 0 1 L 11 6 L 0 11 Z" fill="{ALIGN}"/>
  </marker>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- ── Background ─────────────────────────────────────────────────── -->
<rect width="{VW}" height="{VH}" fill="{BG}"/>
''')

# ── Title ────────────────────────────────────────────────────────────────────
e(f'''
<!-- ── Title ──────────────────────────────────────────────────────── -->
<text x="900" y="44" text-anchor="middle"
      font-family="'Courier New',monospace" font-size="27"
      font-weight="bold" fill="{TEXT}">
  GPT Evolution &amp; Alignment — Research Map
</text>
<text x="900" y="70" text-anchor="middle"
      font-family="system-ui,sans-serif" font-size="13.5" fill="{SUB}">
  How pre-training &#8594; scale &#8594; alignment built the LLMs we use today (2017–2023)
</text>
''')

# ── Track header banners ─────────────────────────────────────────────────────
e(f'''
<!-- ── Track headers ──────────────────────────────────────────────── -->
<rect x="75"  y="86" width="330"  height="30" rx="7"
      fill="{GPT}"   fill-opacity="0.12" stroke="{GPT}"   stroke-width="1.3"/>
<text x="240" y="106" text-anchor="middle"
      font-family="system-ui,sans-serif" font-size="12.5"
      font-weight="bold" fill="{GPT}">&#8594; GPT SERIES (Decoder-Only)</text>

<rect x="410" y="86" width="315"  height="30" rx="7"
      fill="{ENC}"   fill-opacity="0.12" stroke="{ENC}"   stroke-width="1.3"/>
<text x="568" y="106" text-anchor="middle"
      font-family="system-ui,sans-serif" font-size="12.5"
      font-weight="bold" fill="{ENC}">&#8644; ENCODER MODELS</text>

<rect x="730" y="86" width="1058" height="30" rx="7"
      fill="{ALIGN}" fill-opacity="0.12" stroke="{ALIGN}" stroke-width="1.3"/>
<text x="1259" y="106" text-anchor="middle"
      font-family="system-ui,sans-serif" font-size="12.5"
      font-weight="bold" fill="{ALIGN}">&#9878; ALIGNMENT TRACK · Making GPT Helpful &amp; Safe</text>
''')

# ── Track dividers ────────────────────────────────────────────────────────────
e(f'''
<!-- ── Track dividers ─────────────────────────────────────────────── -->
<line x1="405" y1="120" x2="405" y2="1210"
      stroke="#1c2e42" stroke-width="1" stroke-dasharray="4,6"/>
<line x1="725" y1="120" x2="725" y2="1210"
      stroke="#1c2e42" stroke-width="1" stroke-dasharray="4,6"/>
''')

# ── Year labels & horizontal guide lines ─────────────────────────────────────
e('<!-- ── Year labels ────────────────────────────────────────────────── -->')
for yr, yc in [(2017,Y17),(2018,Y18),(2019,Y19),(2020,Y20),(2022,Y22),(2023,Y23)]:
    e(f'<text x="30" y="{yc+6}" font-family="system-ui,sans-serif" '
      f'font-size="15" font-weight="bold" fill="#4a6080">{yr}</text>')
    e(f'<line x1="78" y1="{top(yc)-16}" x2="1785" y2="{top(yc)-16}" '
      f'stroke="#16253a" stroke-width="0.9" stroke-dasharray="3,9"/>')

# ════════════════════════════════════════════════════════════════════════════
# ARROWS  — drawn before cards so cards sit on top
# ════════════════════════════════════════════════════════════════════════════
e('\n<!-- ── Arrows ──────────────────────────────────────────────────────── -->')

# Transformer → GPT-1
vline(GPT_X, bot(Y17), top(Y18), FOUND, label='decoder-only')

# Transformer right → BERT left  (diagonal)
bezier(rgt(GPT_X), Y17,
       lft(ENC_X), Y18,
       FOUND,
       c1x=420, c1y=Y17, c2x=410, c2y=Y18 - 60,
       label='encoder-only', lbx=435, lby=Y17 + 55)

# GPT-1 → GPT-2
vline(GPT_X, bot(Y18), top(Y19), GPT, label='10\u00d7 params')

# BERT → BART
vline(ENC_X, bot(Y18), top(Y19), ENC, label='+ decoder')

# GPT-2 → GPT-3
vline(GPT_X, bot(Y19), top(Y20), GPT, label='100\u00d7 params')

# GPT-3 → InstructGPT  (long diagonal)
bezier(rgt(GPT_X), Y20 - 10,
       lft(AL1_X), Y22,
       GPT,
       c1x=520, c1y=Y20, c2x=720, c2y=Y22 - 80,
       lw=2.8, label='RLHF alignment', lbx=580, lby=820)

# GPT-3 → HH-RLHF  (longer diagonal)
bezier(rgt(GPT_X), Y20 + 20,
       lft(AL2_X), Y22,
       GPT,
       c1x=570, c1y=Y20 + 30, c2x=1000, c2y=Y22 - 70,
       lw=2.8, label='Anthropic fork', lbx=750, lby=850)

# InstructGPT → RLAIF
vline(AL1_X, bot(Y22), top(Y23), ALIGN)

# HH-RLHF → DPO
vline(AL2_X, bot(Y22), top(Y23), ALIGN)

# CAI → SELF-REFINE
vline(AL3_X, bot(Y22), top(Y23), ALIGN)

# InstructGPT → CAI  (dashed arc across same row)
bezier(rgt(AL1_X), Y22 - 20,
       lft(AL3_X), Y22 - 20,
       ALIGN,
       c1x=1100, c1y=Y22 - 65, c2x=1370, c2y=Y22 - 65,
       lw=1.8, dashed=True, label='RLHF methodology', lbx=1190, lby=Y22 - 74)

# HH-RLHF → CAI  (short dashed)
bezier(rgt(AL2_X), Y22 + 10,
       lft(AL3_X), Y22 + 10,
       ALIGN,
       c1x=1310, c1y=Y22 - 18, c2x=1385, c2y=Y22 - 18,
       lw=1.5, dashed=True)

# ════════════════════════════════════════════════════════════════════════════
# PAPER CARDS  — drawn on top of arrows
# ════════════════════════════════════════════════════════════════════════════
e('\n<!-- ── Paper cards ──────────────────────────────────────────────────── -->')

card(GPT_X, Y17, FOUND,
     'Attention Is All You Need',
     'Vaswani et al. · Google · 2017',
     'Self-attention replaces RNN entirely',
     'Encoder-Decoder Transformer architecture')

card(GPT_X, Y18, GPT,
     'GPT-1',
     'Radford et al. · OpenAI · 2018',
     'Pre-train on BooksCorpus (~800M words)',
     'Fine-tune \u2192 SOTA on 9 of 12 NLP tasks')

card(ENC_X, Y18, ENC,
     'BERT',
     'Devlin et al. · Google · 2018',
     'Bidirectional MLM + NSP pre-training',
     'Encoder-only · best for NLU / classification')

card(GPT_X, Y19, GPT,
     'GPT-2',
     'Radford et al. · OpenAI · 2019',
     'Scale to 1.5B params, WebText ~8B tokens',
     'Zero-shot multitask transfer')

card(ENC_X, Y19, ENC,
     'BART',
     'Lewis et al. · Facebook AI · 2019',
     'BERT encoder + GPT decoder combined',
     'Denoising seq2seq · ROUGE-1 = 44.16')

card(GPT_X, Y20, GPT,
     'GPT-3',
     'Brown et al. · OpenAI · 2020',
     '175B params · 300B training tokens',
     'Few-shot in-context learning (no fine-tune)')

card(AL1_X, Y22, ALIGN,
     'InstructGPT',
     'Ouyang et al. · OpenAI · 2022',
     'SFT \u2192 Reward Model \u2192 PPO',
     '85% preferred over 175B raw GPT-3',
     badge_text='\u2192 ChatGPT', badge_color='#f472b6')

card(AL2_X, Y22, ALIGN,
     'HH-RLHF',
     'Bai et al. · Anthropic · 2022',
     'Helpful + Harmless tradeoff study',
     '~170K human preference pairs')

card(AL3_X, Y22, ALIGN,
     'Constitutional AI',
     'Bai et al. · Anthropic · 2022',
     'AI critiques itself via 16 written rules',
     'RLAIF: AI labels replace human feedback',
     badge_text='\u2192 Claude', badge_color=ALIGN)

card(AL1_X, Y23, ALIGN,
     'RLAIF',
     'Lee et al. · Google · 2023',
     'Validates: AI feedback \u2248 human feedback',
     '~71-73% win rate validated at scale')

card(AL2_X, Y23, ALIGN,
     'DPO',
     'Rafailov et al. · Stanford · 2023',
     'No reward model, no PPO required',
     'Closed-form preference optimisation')

card(AL3_X, Y23, ALIGN,
     'SELF-REFINE',
     'Madaan et al. · CMU / AI2 · 2023',
     'Generate \u2192 Critique \u2192 Refine loop',
     'No extra training · ~20% avg improvement')

# ── Legend ────────────────────────────────────────────────────────────────────
e(f'''
<!-- ── Legend ─────────────────────────────────────────────────────── -->
<rect x="75"  y="{VH-50}" width="14" height="14" rx="3" fill="{FOUND}"/>
<text x="96"  y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">Foundation Architecture</text>
<rect x="295" y="{VH-50}" width="14" height="14" rx="3" fill="{GPT}"/>
<text x="316" y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">GPT Series (Decoder-Only)</text>
<rect x="545" y="{VH-50}" width="14" height="14" rx="3" fill="{ENC}"/>
<text x="566" y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">Encoder Models (Bidirectional)</text>
<rect x="820" y="{VH-50}" width="14" height="14" rx="3" fill="{ALIGN}"/>
<text x="841" y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">Alignment Research</text>
<line x1="1090" y1="{VH-43}" x2="1120" y2="{VH-43}" stroke="{GPT}" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#ah-g)"/>
<text x="1128" y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">builds on</text>
<line x1="1260" y1="{VH-43}" x2="1290" y2="{VH-43}" stroke="{ALIGN}" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#ah-a)"/>
<text x="1298" y="{VH-38}" font-family="system-ui,sans-serif" font-size="12" fill="{SUB}">methodology influence</text>
''')

e('</svg>')

# ── Write file ────────────────────────────────────────────────────────────────
svg = '\n'.join(buf)
out = '03_GPT_Evolution_and_Alignment/GPT_Papers_Diagram.svg'
with open(out, 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'Saved: {out}  ({len(svg):,} bytes)')
