import os, re, glob, difflib, socket
import gradio as gr

# --- Ayarlar ---
BASE = os.environ.get("IST_TRAVEL_DATA",
                      "/content/drive/MyDrive/Colab Notebooks/zey second akbank proje/data/istanbul")

# --- Yardımcılar ---
STOPWORDS = {"olsun","lütfen","lutfen","biraz","bir","şu","bu","şöyle","böyle","gibi","ve","ya","ile","da","de"}

def _norm(s: str) -> str:
    s = (s or "").casefold()
    s = re.sub(r"[^a-zçğıöşü0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def detect_slot_from_hint(hint_norm: str) -> str | None:
    words = set(hint_norm.split())
    if "sabah" in words: return "Sabah"
    if "öğle" in words or "ogle" in words: return "Öğle"
    if "akşam" in words or "aksam" in words: return "Akşam"
    return None

def detect_day_from_hint(hint_norm: str) -> int | None:
    # ikinci gün / 2. gün / gün 2
    if re.search(r"\b(ikinci|2\.?|2)\s*g[uü]n\b|\bg[uü]n\s*2\b", hint_norm):
        return 2
    # birinci gün / 1. gün / ilk gün / gün 1
    if re.search(r"\b(birinci|ilk|1\.?|1)\s*g[uü]n\b|\bg[uü]n\s*1\b", hint_norm):
        return 1
    return None

def pick_place_from_hint(hint: str, candidates: set[str]) -> str | None:
    hn = _norm(hint)
    core = " ".join(w for w in hn.split() if w not in STOPWORDS) or hn
    best, best_score = None, 0.0
    for p in candidates:
        pn = _norm(p)
        if core and (core in pn or pn in core):
            score = 1.0
        else:
            score = difflib.SequenceMatcher(None, core, pn).ratio()
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= 0.45 else None

def _pin_to_slot(slots: dict, place: str, slot_name: str) -> dict:
    # diğer slotlardan çıkar
    for k in ("Sabah","Öğle","Akşam"):
        if slots.get(k):
            items = [x.strip() for x in slots[k].split(",") if x.strip()]
            items = [x for x in items if x.lower() != place.lower()]
            slots[k] = ", ".join(items)
    # hedef slotun başına koy
    items = [x.strip() for x in (slots.get(slot_name) or "").split(",") if x.strip()]
    items = [place] + [x for x in items if x.lower() != place.lower()]
    slots[slot_name] = ", ".join(items)
    return slots

# --- Veri yükle ---
pattern_title = re.compile(r"^##\s*\[[^\]]*\]\s*([^\n]+)", re.MULTILINE)
score_pattern = re.compile(r"\b(müze|sultanahmet|topkapı|ayasofya|arkeoloji|yerebatan|gülhane|kapalı|galata|dolmabahçe)\b",
                           re.IGNORECASE)

md_files = sorted(glob.glob(os.path.join(BASE, "*.md")))
if not md_files:
    raise FileNotFoundError(f"Markdown bulunamadı: {BASE} altında *.md bekliyordum.")

place_names = set()
file_hits = []
for fp in md_files:
    with open(fp, "r", encoding="utf-8") as f:
        txt = f.read()
    for m in pattern_title.finditer(txt):
        title = re.sub(r"\s+", " ", m.group(1).strip())
        place_names.add(title)
    sc = len(score_pattern.findall(txt))
    file_hits.append((sc, os.path.basename(fp)))
file_hits.sort(reverse=True, key=lambda x: x[0])
sources = [f"[Kaynak {i}] {name} (skor={sc})" for i, (sc, name) in enumerate(file_hits, 1)]

# --- Varsayılan tercih listeleri ---
preferred_day1 = [
    "Ayasofya Camii",
    "Topkapı Sarayı Müzesi",
    "İstanbul Arkeoloji Müzeleri",
    "Gülhane Parkı",
    "Yerebatan Sarnıcı",
    "Sultan Ahmet Camii",
    "Sultanahmet Meydanı",
]
preferred_day2 = [
    "Türk ve İslam Eserleri Müzesi",
    "Kapalı Çarşı (Grand Bazaar)",
    "Galata Kulesi",
    "Dolmabahçe Sarayı",
    "Taksim Meydanı",
]

# Kategori eşlemesi (manuel, sade)
CATEGORY_MAP = {
    "müze": [
        "Topkapı Sarayı Müzesi",
        "İstanbul Arkeoloji Müzeleri",
        "Türk ve İslam Eserleri Müzesi",
        "Yerebatan Sarnıcı",
        "Ayasofya Camii",
        "Dolmabahçe Sarayı",
        "Galata Kulesi",
    ],
    "yürüyüş": [
        "Gülhane Parkı",
        "Sultanahmet Meydanı",
        "Taksim Meydanı",
        "Kapalı Çarşı (Grand Bazaar)",
    ],
    "yemek": [
        "Kapalı Çarşı (Grand Bazaar)",
        "Sultanahmet Meydanı",
        "Taksim Meydanı",
    ],
}

def fuzzy_pick(candidates, available):
    picked = []
    for cand in candidates:
        if cand in available:
            picked.append(cand); continue
        alt = [p for p in available if cand.lower() in p.lower() or p.lower() in cand.lower()]
        if alt: picked.append(alt[0])
    seen, uniq = set(), []
    for p in picked:
        if p not in seen:
            uniq.append(p); seen.add(p)
    return uniq

def apply_filters(seq, chosen):
    if not chosen: return seq
    allowed = set()
    for c in chosen:
        allowed.update(CATEGORY_MAP.get(c, []))
    out = []
    for item in seq:
        if any(item.lower() in a.lower() or a.lower() in item.lower() for a in allowed):
            out.append(item)
    return out or seq

# --- Plan oluşturucu ---
def build_plan(chosen_categories, extra_hint):
    try:
        chosen_categories = list(chosen_categories) if chosen_categories else []
        extra_hint = (extra_hint or "").strip()

        hint_norm    = _norm(extra_hint)
        slot_hint    = detect_slot_from_hint(hint_norm)   # "Sabah" / "Öğle" / "Akşam" / None
        day_hint     = detect_day_from_hint(hint_norm)    # 1 / 2 / None
        pinned_place = pick_place_from_hint(extra_hint, place_names) if extra_hint else None

        d1 = fuzzy_pick(preferred_day1, place_names)
        d2 = fuzzy_pick(preferred_day2, place_names)

        def apply_with_pin(seq):
            if not chosen_categories:
                return seq
            kept = apply_filters(seq, chosen_categories)
            if pinned_place and pinned_place in seq and pinned_place not in kept:
                kept = [pinned_place] + [x for x in kept if x != pinned_place]
            return kept

        d1 = apply_with_pin(d1)
        d2 = apply_with_pin(d2)

        if pinned_place:
            if day_hint == 2:
                d1 = [x for x in d1 if x != pinned_place]
                if pinned_place in d2:
                    d2 = [pinned_place] + [x for x in d2 if x != pinned_place]
                else:
                    d2 = [pinned_place] + d2
            else:
                d2 = [x for x in d2 if x != pinned_place]
                if pinned_place in d1:
                    d1 = [pinned_place] + [x for x in d1 if x != pinned_place]
                else:
                    d1 = [pinned_place] + d1

        def to_slots(seq):
            slots = {"Sabah": "", "Öğle": "", "Akşam": ""}
            if not seq: return slots
            if len(seq) == 1:
                slots["Sabah"] = seq[0]
            elif len(seq) == 2:
                slots["Sabah"], slots["Öğle"] = seq
            else:
                third = max(1, len(seq)//3)
                slots["Sabah"] = ", ".join(seq[:third])
                slots["Öğle"]  = ", ".join(seq[third:2*third]) if len(seq) >= 2*third else ""
                slots["Akşam"] = ", ".join(seq[2*third:]) if len(seq) > 2*third else ""
            return slots

        s1, s2 = to_slots(d1), to_slots(d2)

        if pinned_place:
            target = s2 if day_hint == 2 else s1
            target_slot = slot_hint or "Sabah"
            _pin_to_slot(target, pinned_place, target_slot)

        lines = []
        lines.append("**Gün 1**")
        lines.append(f"- **Sabah:** {s1['Sabah'] or '(boş)'}")
        lines.append(f"- **Öğle:** {s1['Öğle'] or '(boş)'}")
        lines.append(f"- **Akşam:** {s1['Akşam'] or '(boş)'}\n")
        lines.append("**Gün 2**")
        lines.append(f"- **Sabah:** {s2['Sabah'] or '(boş)'}")
        lines.append(f"- **Öğle:** {s2['Öğle'] or '(boş)'}")
        lines.append(f"- **Akşam:** {s2['Akşam'] or '(boş)'}\n")
        if chosen_categories:
            lines.append(f"**Filtreler:** {', '.join(chosen_categories)}")
        if extra_hint:
            lines.append(f"**Not:** İpucunu dikkate aldım → {extra_hint}\n")
        lines.append("**Kaynaklar**")
        for s in sources[:5]:
            lines.append(s)
        return "\n".join(lines)

    except Exception as e:
        return f"> ⚠️ Plan oluşturulurken hata oluştu:\n```\n{repr(e)}\n```"

# --- UI ---
theme = gr.themes.Soft(primary_hue="orange")
with gr.Blocks(title="Travel Mini-Planner (Offline RAG)", theme=theme) as demo:
    gr.Markdown("## Travel Mini-Planner (Offline RAG) — İstanbul / 2 Gün")
    with gr.Row():
        cats = gr.CheckboxGroup(["müze","yürüyüş","yemek"], value=["müze"], label="Kategori filtreleri")
        hint = gr.Textbox(label="Mini ipucu (opsiyonel)",
                          placeholder="örn. 'Ayasofya sabah olsun' | 'Topkapı 2. gün öğle'")
    btn = gr.Button("Plan Oluştur", variant="primary")
    out = gr.Markdown()
    btn.click(build_plan, inputs=[cats, hint], outputs=[out])

# --- LAUNCH (sağlam) ---
def _find_free_port(start=7860, end=7890):
    for p in range(start, end+1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", p))
                return p
            except OSError:
                continue
    return 7860  # fallback

if __name__ == "__main__":
    try:
        gr.close_all()
    except Exception:
        pass
    demo.queue().launch(
        share=True,
        server_name="0.0.0.0",
        server_port=_find_free_port(),
        inline=False,
        debug=False,
        show_error=True
    )
