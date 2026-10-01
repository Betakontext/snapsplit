#!/usr/bin/env python3
"""check_i18n.py - read-only diagnosis of the SnapSplit translation setup (step D0).

Usage (plain Python, Blender is NOT required):
    python3 check_i18n.py /path/to/snapsplit --verbose --out check_i18n_report.txt

Optional (uses the real locale list of the running Blender):
    blender -b -P check_i18n.py -- /path/to/snapsplit --verbose

The script never imports the add-on and never modifies any file.
"""
import argparse
import ast
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Blender 5.2 locale list (taken from bpy.app.translations.locales on the dev machine).
# If bpy is available, the real list of the running Blender replaces it.
# ---------------------------------------------------------------------------
BLENDER_LOCALES = {
    'ab', 'ar_EG', 'eu_EU', 'be', 'bg_BG', 'ca_AD', 'zh_HANS', 'zh_HANT', 'hr', 'cs_CZ',
    'da', 'nl_NL', 'en_GB', 'en_US', 'eo', 'fi_FI', 'fr_FR', 'ka', 'de_DE', 'el_GR',
    'he_IL', 'hi_IN', 'hu_HU', 'id_ID', 'it_IT', 'ja_JP', 'ko_KR', 'ky_KG', 'lt', 'ml',
    'nb', 'fa_IR', 'pl_PL', 'pt_BR', 'pt_PT', 'ro_RO', 'ru_RU', 'sr_RS', 'sr_RS@latin',
    'sk_SK', 'sl', 'es', 'sw', 'sv_SE', 'ta', 'th_TH', 'tr_TR', 'uk_UA', 'ur', 'vi_VN',
}
try:
    import bpy  # only available when started through Blender
    BLENDER_LOCALES = set(bpy.app.translations.locales)
    LOCALES_SOURCE = "bpy.app.translations.locales (live)"
except Exception:
    LOCALES_SOURCE = "hard-coded list from Blender 5.2"

# Dictionary block code -> Blender locale code.  None = keep the block but do not register it.
DICT_TO_BLENDER = {
    "zh_CN": "zh_HANS",
    "zh_TW": "zh_HANT",
    "ar_SA": "ar_EG",
    "sl_SI": "sl",
    "sw_KE": "sw",
    "bn_BD": None,  # Bengali: not a Blender locale, kept for later
}

# Keys already decided for removal (tooltip tolerance, reload button leftovers)
PLANNED_REMOVALS = {
    "profiles.mat.tooltip", "ui.reload_language", "ui.reload_language_desc",
    "prefs.language_note", "prefs.reload_language", "prefs.reload_language_desc",
}

TR_FUNCS = {"tr", "_trf"}                 # translation helpers
STATIC_KW = {"name", "description", "items"}   # keyword args that are evaluated once
STATIC_ATTR = {"bl_label", "bl_description"}   # class attributes evaluated once
PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
SKIP_FILE_RE = re.compile(r"(\d\d\.py$|^check_.*\.py$|^fix_.*\.py$|^languages\.py$)")


# ---------------------------------------------------------------------------
# Report helper
# ---------------------------------------------------------------------------
class Report:
    def __init__(self, verbose):
        self.lines = []
        self.verbose = verbose

    def p(self, text=""):
        self.lines.append(text)

    def head(self, title):
        self.p()
        self.p("=" * 78)
        self.p(title)
        self.p("=" * 78)

    def items(self, rows, limit=15):
        """Print rows; truncate long lists unless --verbose is set."""
        rows = list(rows)
        shown = rows if self.verbose else rows[:limit]
        for r in shown:
            self.p("  " + r)
        if len(rows) > len(shown):
            self.p(f"  ... +{len(rows) - len(shown)} more (use --verbose)")


# ---------------------------------------------------------------------------
# Parsing languages.py (AST only, no import)
# ---------------------------------------------------------------------------
def parse_translations(path):
    """Return (blocks, info). Later duplicate keys win, exactly like Python does."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    top = None
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.target.id == "translations":
            top = node.value
        elif isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "translations" for t in node.targets):
            top = node.value
    if not isinstance(top, ast.Dict):
        raise SystemExit("ERROR: 'translations = {...}' literal not found in languages.py")

    blocks, lines = {}, {}
    info = {"top_dups": [], "inner_dups": defaultdict(list), "non_literal": []}
    for knode, vnode in zip(top.keys, top.values):
        if not (isinstance(knode, ast.Constant) and isinstance(knode.value, str)
                and isinstance(vnode, ast.Dict)):
            continue
        code = knode.value
        data = {}
        for k2, v2 in zip(vnode.keys, vnode.values):
            if not (isinstance(k2, ast.Constant) and isinstance(k2.value, str)):
                info["non_literal"].append((code, getattr(k2, "lineno", 0)))
                continue
            try:
                value = ast.literal_eval(v2)
            except Exception:
                value = "<non-literal>"
                info["non_literal"].append((code, k2.lineno))
            if k2.value in data:
                info["inner_dups"][code].append((k2.value, k2.lineno))
            data[k2.value] = value
        if code in blocks:
            info["top_dups"].append((code, lines[code], knode.lineno, len(blocks[code]), len(data)))
        blocks[code] = data        # the later block replaces the earlier one
        lines[code] = knode.lineno
    info["lines"] = lines
    return blocks, info


# ---------------------------------------------------------------------------
# Scanning the add-on code
# ---------------------------------------------------------------------------
def enclosing_scope(node, parents):
    """Name of the nearest function, or a marker for class body / module level."""
    cur = node
    while cur in parents:
        cur = parents[cur]
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cur.name
        if isinstance(cur, ast.ClassDef):
            return f"<class {cur.name}>"
    return "<module>"


def static_context(node, parents):
    """Return 'kw:name' / 'assign:bl_label' ... if the text is evaluated only once."""
    cur = node
    while cur in parents:
        par = parents[cur]
        if isinstance(par, ast.keyword) and par.arg in STATIC_KW:
            return f"kw:{par.arg}"
        if isinstance(par, ast.Assign):
            for t in par.targets:
                nm = t.attr if isinstance(t, ast.Attribute) else getattr(t, "id", None)
                if nm in STATIC_ATTR:
                    return f"assign:{nm}"
            return None
        if isinstance(par, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            return None
        cur = par
    return None


def const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def call_name(call):
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def scan_code(addon_dir):
    """Collect tr()/_trf() calls, report_user key usages and every string constant."""
    calls, report_keys, all_strings, files = [], [], set(), []
    for path in sorted(addon_dir.glob("*.py")):
        if SKIP_FILE_RE.search(path.name):
            continue
        files.append(path.name)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as ex:
            print(f"WARNING: cannot parse {path.name}: {ex}", file=sys.stderr)
            continue
        parents = {}
        for n in ast.walk(tree):
            for c in ast.iter_child_nodes(n):
                parents[c] = n
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                all_strings.add(n.value)
            if not isinstance(n, ast.Call):
                continue
            name = call_name(n)
            if name in TR_FUNCS and n.args:
                key = const_str(n.args[0])
                default, kind = None, "none"
                dnode = n.args[1] if len(n.args) > 1 else next(
                    (k.value for k in n.keywords if k.arg in ("default", "fallback")), None)
                if dnode is not None:
                    default = const_str(dnode)
                    kind = ("const" if default is not None
                            else "fstring" if isinstance(dnode, ast.JoinedStr) else "expr")
                calls.append({
                    "file": path.name, "line": n.lineno, "func": name, "key": key,
                    "default": default, "dkind": kind,
                    "scope": enclosing_scope(n, parents),
                    "static": static_context(n, parents),
                })
            elif name == "report_user" and len(n.args) >= 3:
                text = const_str(n.args[2])
                if text and "." in text and " " not in text:
                    report_keys.append((path.name, n.lineno, text))
    return calls, report_keys, all_strings, files


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Read-only SnapSplit i18n diagnosis")
    ap.add_argument("addon_dir", nargs="?", default=".", help="folder containing languages.py")
    ap.add_argument("--verbose", action="store_true", help="do not truncate long lists")
    ap.add_argument("--out", help="also write the report to this file")
    args = ap.parse_args(argv)

    addon_dir = Path(args.addon_dir).expanduser().resolve()
    lang_path = addon_dir / "languages.py"
    if not lang_path.is_file():
        raise SystemExit(f"ERROR: {lang_path} not found")

    blocks, info = parse_translations(lang_path)
    if "en_US" not in blocks:
        raise SystemExit("ERROR: no en_US block in translations")
    en = blocks["en_US"]
    calls, report_keys, all_strings, files = scan_code(addon_dir)
    R = Report(args.verbose)
    summary = []

    R.p(f"SnapSplit i18n diagnosis | addon dir: {addon_dir}")
    R.p(f"Scanned code files ({len(files)}): {', '.join(files)}")
    R.p(f"Blender locales: {LOCALES_SOURCE}")

    # ---- 1. Blocks, Blender codes, key coverage ---------------------------------------
    R.head("1. Language blocks (entries, Blender code, coverage vs en_US)")
    R.p(f"  {'block':<8} {'line':>5} {'entries':>7} {'missing':>7} {'extra':>5}  blender code / status")
    bad_blocks = 0
    for code, data in blocks.items():
        if not data:
            status = "EMPTY base bucket -> remove"
        else:
            target = DICT_TO_BLENDER.get(code, code)
            if target is None:
                status = "kept, NOT registered (no Blender locale)"
            elif target not in BLENDER_LOCALES:
                status = f"{target}: NOT A BLENDER LOCALE"
                bad_blocks += 1
            elif target != code:
                status = f"-> {target} (rename)"
            else:
                status = f"{target} ok"
        missing = [k for k in en if k not in data] if data else []
        extra = [k for k in data if k not in en] if code != "en_US" else []
        R.p(f"  {code:<8} {info['lines'][code]:>5} {len(data):>7} {len(missing):>7} {len(extra):>5}  {status}")
    for code, data in blocks.items():
        if data and code != "en_US":
            extra = [k for k in data if k not in en]
            if extra:
                R.p(f"  keys in {code} but not in en_US:")
                R.items(extra, 8)
    if info["top_dups"]:
        R.p()
        R.p("  Duplicate top-level block names (the LATER block silently wins):")
        for code, l1, l2, n1, n2 in info["top_dups"]:
            R.p(f"    '{code}': line {l1} ({n1} entries) replaced by line {l2} ({n2} entries)")
    for code, dups in info["inner_dups"].items():
        R.p(f"  Duplicate keys inside {code} (last wins):")
        R.items([f"{k} (line {ln})" for k, ln in dups], 8)
    if info["non_literal"]:
        R.p("  Non-literal entries (could not be evaluated):")
        R.items([f"{c} line {ln}" for c, ln in info["non_literal"]], 8)
    summary.append(f"blocks: {len(blocks)} | not-Blender codes: {bad_blocks} | "
                   f"top-level dups: {len(info['top_dups'])}")

    # ---- 2. Keys missing in en_US or only in some languages ---------------------------
    R.head("2. Keys that are not present in every full language block")
    full = {c: d for c, d in blocks.items() if d and c != "en_US"}
    all_keys = set(en)
    for d in full.values():
        all_keys |= set(d)
    partial = []
    for k in sorted(all_keys):
        have = [c for c, d in full.items() if k in d] + (["en_US"] if k in en else [])
        if len(have) < len(full) + 1:
            absent = [c for c in list(full) + ["en_US"] if c not in have]
            partial.append(f"{k}  (missing in {len(absent)}: {', '.join(absent[:6])}"
                           f"{'...' if len(absent) > 6 else ''})")
    R.p(f"  {len(partial)} key(s) are not in all blocks (partial blocks such as uk_UA/tr_TR fall back to en_US).")
    R.items(partial, 12)
    summary.append(f"keys not in all blocks: {len(partial)}")

    # ---- 3. Defaults in code vs en_US text --------------------------------------------
    R.head("3. tr()/_trf() defaults that differ from the en_US text")
    mismatch, fstr = [], []
    for c in calls:
        if c["key"] is None or c["key"] not in en:
            continue
        if c["dkind"] == "const" and c["default"] != en[c["key"]]:
            mismatch.append(f"{c['file']}:{c['line']} {c['key']}\n      code : {c['default']!r}\n      en_US: {en[c['key']]!r}")
        elif c["dkind"] == "fstring":
            fstr.append(f"{c['file']}:{c['line']} {c['key']} | en_US has placeholder: "
                        f"{'yes' if PLACEHOLDER_RE.search(en[c['key']]) else 'NO'}")
    R.p(f"  {len(mismatch)} constant default(s) differ (static texts must match en_US EXACTLY):")
    R.items(mismatch, 10)
    R.p(f"  {len(fstr)} call(s) use an f-string default (the translated text cannot hold the runtime value):")
    R.items(fstr, 10)
    summary.append(f"default != en_US: {len(mismatch)} | f-string defaults: {len(fstr)}")

    # ---- 4. Keys used in code but missing in the dictionary ---------------------------
    R.head("4. Keys used in code but missing in en_US")
    used_missing = sorted({(c["file"], c["line"], c["key"]) for c in calls
                           if c["key"] and c["key"] not in en})
    used_missing += sorted({(f, ln, k) for f, ln, k in report_keys if k not in en})
    R.p(f"  {len(used_missing)} usage(s) without an en_US entry (they always show the code default):")
    R.items([f"{f}:{ln} {k}" for f, ln, k in used_missing], 15)
    dynamic = [c for c in calls if c["key"] is None]
    R.p(f"  {len(dynamic)} call(s) with a non-constant key (dead-key list below may be incomplete):")
    R.items([f"{c['file']}:{c['line']} in {c['scope']}" for c in dynamic], 8)
    summary.append(f"used but missing: {len(used_missing)} | dynamic keys: {len(dynamic)}")

    # ---- 5. Dead keys -----------------------------------------------------------------
    R.head("5. Keys in en_US that the code never uses")
    used = {c["key"] for c in calls if c["key"]} | {k for _, _, k in report_keys}
    dead = sorted(k for k in en if k not in used and k not in all_strings)
    planned = [k for k in dead if k in PLANNED_REMOVALS]
    other_dead = [k for k in dead if k not in PLANNED_REMOVALS]
    R.p(f"  {len(dead)} dead key(s); {len(planned)} of them are already on the removal list.")
    R.items(planned, 10)
    R.p("  Other dead keys (check before deleting):")
    R.items(other_dead, 25)
    still_used = sorted(k for k in PLANNED_REMOVALS if k in used)
    if still_used:
        R.p("  WARNING - keys planned for removal are still used in code:")
        R.items(still_used, 10)
    summary.append(f"dead keys: {len(dead)} (planned removals among them: {len(planned)})")

    # ---- 6. Same English text, different translations ---------------------------------
    R.head("6. Identical English texts on different keys with DIFFERENT translations")
    groups = defaultdict(list)
    for k, t in en.items():
        groups[t].append(k)
    conflicts, harmless = [], 0
    for text, keys in groups.items():
        if len(keys) < 2:
            continue
        bad = [c for c, d in full.items() if len({d[k] for k in keys if k in d}) > 1]
        if bad:
            conflicts.append(f"{text!r}\n      keys: {', '.join(keys)}\n      differs in: {', '.join(bad[:6])}"
                             f"{'...' if len(bad) > 6 else ''}")
        else:
            harmless += 1
    R.p(f"  {len(conflicts)} conflicting group(s) need a translation context; {harmless} duplicate group(s) are harmless.")
    R.items(conflicts, 10)
    summary.append(f"text conflicts: {len(conflicts)} | harmless duplicates: {harmless}")

    # ---- 7. Placeholder consistency ---------------------------------------------------
    R.head("7. Placeholder consistency ({...}) against en_US")
    ph_bad = []
    for code, d in full.items():
        for k, t in d.items():
            if k in en and isinstance(t, str) and \
                    Counter(PLACEHOLDER_RE.findall(t)) != Counter(PLACEHOLDER_RE.findall(en[k])):
                ph_bad.append(f"{code} {k}")
    R.p(f"  {len(ph_bad)} translation(s) with different placeholders than en_US:")
    R.items(ph_bad, 15)
    summary.append(f"placeholder mismatches: {len(ph_bad)}")

    # ---- 8. Static tr() calls (input for step D3) -------------------------------------
    R.head("8. tr() calls that are evaluated only once (bl_label, name=, description=, items=)")
    static = [c for c in calls if c["static"]]
    by_file = Counter((c["file"], c["static"]) for c in static)
    for (f, kind), n in sorted(by_file.items()):
        R.p(f"  {f:<22} {kind:<22} {n}")
    R.p("  Details (scope tells WHEN the text is fixed):")
    R.items([f"{c['file']}:{c['line']} {c['static']:<18} scope={c['scope']:<22} key={c['key']}"
             for c in static], 20)
    reg = sum(1 for c in static if c["scope"] == "register")
    R.p(f"  assigned inside register(): {reg} | at import time (class body/module): "
        f"{sum(1 for c in static if c['scope'].startswith('<'))}")
    summary.append(f"static tr() calls: {len(static)} (in register(): {reg})")

    # ---- Summary ----------------------------------------------------------------------
    R.head("SUMMARY (paste this block if the full report is too long)")
    for s in summary:
        R.p("  " + s)

    text = "\n".join(R.lines)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"\n[report written to {args.out}]")


if __name__ == "__main__":
    main()
