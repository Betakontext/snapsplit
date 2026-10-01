#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# i18n_finish.py - converts the SnapSplit code base from key-based tr() to Blender-native i18n.
#
# Usage (dry run is the default, nothing is written):
#   python3 i18n_finish.py --src-dir ../snapsplit [--diff]
#   python3 i18n_finish.py --src-dir ../snapsplit --apply
# The script is idempotent: run it again if it reports skipped overlapping edits.

import argparse
import ast
import difflib
import re
import runpy
import shutil
import time
from pathlib import Path

SKIP_FILES = {"languages.py", "localization.py", "utils.py", "__init__.py"}
KEY_RE = re.compile(r"^[A-Za-z_]+(\.[A-Za-z0-9_]+)+$")
PLACEHOLDER_RE = re.compile(r"\{[A-Za-z_]\w*(:[^}]*)?\}")

# Keys whose final English text differs from the code default (wins over the code)
FORCE_EN = {
    "ui.less": "Less...",
    "ui.more_less_more": "More...",
    "ui.cap_seams_during_split_short": "Cap seams during split",
    "ui.sphere_diameter_mm": "Sphere Diameter (mm)",
    "op.split.many_parts_hint": "Splitting into many parts can take a while on dense meshes...",
    "op.connect.dovetail.warn.hardcut_build_fail": "Hard-side cut: could not build combined surface (seam may not be closed); connector left untrimmed.",
    "op.connect.dovetail.warn.hardcut_tenon_fail": "Hard-side cut failed on the connector; keeping untrimmed connector geometry.",
}

# f-string call sites: key -> (template, placeholder names in order of appearance)
FSTR = {
    "INFO_ALIGNED": ("Aligned {name} to {name2}.", ["name", "name2"]),
    "INFO_PICKED_A": ("Picked A: {name} face {fidx}", ["name", "fidx"]),
    "INFO_PICKED_B": ("Picked B: {name} face {fidx}", ["name", "fidx"]),
    "ERR_FACE_FRAMES_COMPUTE": ("Could not compute face frames: {error}", ["error"]),
    "op.connect.custom.warn.nonmanifold": (
        "Custom connector source mesh '{name}' has non-manifold geometry "
        "(open or multi-shared edges); boolean results may be unreliable.", ["name"]),
    "op.common.warn.mod_apply_fail": ("Modifier apply failed ({name}): {error}", ["name", "error"]),
    "op.connect.preview.warn.cap": (
        "Connector live preview stopped at {cap} objects; remaining points are not shown.", ["cap"]),
    "op.connect.click.err.modal": ("Modal error: {error}", ["error"]),
    "op.connect.batch.info.done": ("{value} connectors created.", ["value"]),
    "op.common.warn.bevel_apply": ("Bevel apply failure: {error}", ["error"]),
    "op.connect.click.err.place": ("Placement failed: {error}", ["error"]),
}


def is_str(n):
    """True if the AST node is a plain string constant."""
    return isinstance(n, ast.Constant) and isinstance(n.value, str)


class Src:
    """Parsed source with byte offsets (ast columns are UTF-8 byte offsets)."""

    def __init__(self, raw):
        self.raw = raw
        self.tree = ast.parse(raw)
        self.offs = [0]
        for line in raw.splitlines(keepends=True):
            self.offs.append(self.offs[-1] + len(line))
        self.parents = {c: p for p in ast.walk(self.tree) for c in ast.iter_child_nodes(p)}

    def s(self, n):
        return self.offs[n.lineno - 1] + n.col_offset

    def e(self, n):
        return self.offs[n.end_lineno - 1] + n.end_col_offset

    def lines(self, n):
        """Byte span covering all whole lines of node n."""
        return self.offs[n.lineno - 1], self.offs[n.end_lineno]


def elements(call):
    """Positional and keyword arguments of a call in source order."""
    return sorted(list(call.args) + list(call.keywords), key=lambda n: (n.lineno, n.col_offset))


def drop_elem(src, call, target):
    """Edit that removes ', target' from a call."""
    els = elements(call)
    i = els.index(target)
    return (src.e(els[i - 1]), src.e(target), b"") if i else (src.s(target), src.e(target), b"")


def apply_edits(raw, edits):
    """Apply (start, end, bytes) edits back to front; return (new_raw, skipped_overlaps)."""
    out, last, skipped = raw, None, 0
    for s, e, new in sorted(set(edits), key=lambda x: (x[0], x[1]), reverse=True):
        if last is not None and e > last:
            skipped += 1
            continue
        out = out[:s] + new + out[e:]
        last = s
    return out, skipped


# ---------------------------------------------------------------- passes
# Every pass returns (edits, manual, warnings).

def pass_defs(src, fname, msgids):
    """Remove module-level helper definitions of _trf (the shared one lives in utils)."""
    edits = []
    for n in src.tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == "_trf":
            s, e = src.lines(n)
            edits.append((s, e, b""))
    return edits, [], []


def pass_report(src, fname, msgids):
    """Drop the legacy msg_de argument of report_user() and flag bare translation keys."""
    edits, manual = [], []
    for n in ast.walk(src.tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        if not ((isinstance(f, ast.Name) and f.id == "report_user")
                or (isinstance(f, ast.Attribute) and f.attr == "report_user")):
            continue
        if len(n.args) >= 4:
            edits.append(drop_elem(src, n, n.args[3]))
        for k in n.keywords:
            if k.arg == "msg_de":
                edits.append(drop_elem(src, n, k))
        if len(n.args) >= 3 and is_str(n.args[2]) and KEY_RE.match(n.args[2].value):
            manual.append(f"{fname}:{n.lineno}: report_user() gets a bare key {n.args[2].value!r}")
    return edits, manual, []


def pass_convert(src, fname, msgids):
    """tr()/_trf() -> English literals and templates."""
    edits, manual, warns = [], [], []

    def check(text, line):
        if msgids is not None and text not in msgids:
            warns.append(f"{fname}:{line}: not a msgid in localization.py: {text[:70]!r}")

    for n in ast.walk(src.tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)):
            continue
        if n.func.id == "_trf":
            a = n.args
            if len(a) >= 2 and is_str(a[0]) and is_str(a[1]):
                if a[0].value in FORCE_EN:
                    edits.append((src.s(n), src.e(n), f"_trf({FORCE_EN[a[0].value]!r})".encode()))
                else:
                    check(a[1].value, n.lineno)
                    edits.append((src.s(a[0]), src.s(a[1]), b""))
            elif len(a) >= 2 and is_str(a[0]):
                manual.append(f"{fname}:{n.lineno}: _trf({a[0].value!r}, <non-literal>)")
            continue
        if n.func.id != "tr":
            continue

        a = n.args
        kw = {k.arg: k.value for k in n.keywords if k.arg}
        key = a[0] if a else kw.get("key")
        dflt = a[1] if len(a) > 1 else kw.get("default")
        if not is_str(key):
            manual.append(f"{fname}:{n.lineno}: tr() with non-literal key")
            continue
        k = key.value

        # Is the call followed by .format(...)?
        outer, par = None, src.parents.get(n)
        if isinstance(par, ast.Attribute) and par.attr == "format":
            gp = src.parents.get(par)
            if isinstance(gp, ast.Call) and gp.func is par:
                outer = gp
        target = outer or n

        if k in FSTR:
            tpl, phs = FSTR[k]
            vals = [v for v in dflt.values if isinstance(v, ast.FormattedValue)] \
                if isinstance(dflt, ast.JoinedStr) else None
            if vals is None or len(vals) != len(phs) or any(v.format_spec or v.conversion != -1 for v in vals):
                manual.append(f"{fname}:{n.lineno}: {k!r} f-string does not match the template table")
                continue
            check(tpl, n.lineno)
            args = ", ".join(f"{p}={ast.unparse(v.value)}" for p, v in zip(phs, vals))
            edits.append((src.s(target), src.e(target), f"_trf({tpl!r}, {args})".encode()))
        elif k in FORCE_EN:
            lit = repr(FORCE_EN[k])
            edits.append((src.s(target), src.e(target), (f"_trf({lit})" if outer else lit).encode()))
        elif is_str(dflt) and dflt.value.strip():
            text = dflt.value
            check(text, n.lineno)
            if outer is not None:
                if outer.args:
                    manual.append(f"{fname}:{n.lineno}: {k!r} .format() with positional arguments")
                    continue
                args = "".join(f", {x.arg}={ast.unparse(x.value)}" for x in outer.keywords if x.arg)
                edits.append((src.s(outer), src.e(outer), f"_trf({text!r}{args})".encode()))
            elif PLACEHOLDER_RE.search(text):
                manual.append(f"{fname}:{n.lineno}: {k!r} has placeholders but no .format()")
            else:
                edits.append((src.s(n), src.e(n), repr(text).encode()))
        else:
            manual.append(f"{fname}:{n.lineno}: {k!r} has no plain English default")
    return edits, manual, warns


def tr_still_used(src):
    """Lines where tr(...) is still called as a plain name."""
    return [n.lineno for n in ast.walk(src.tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "tr"]


def pass_imports(src, fname, msgids):
    """Remove 'tr' from languages/utils imports once no call is left."""
    edits, manual = [], []
    left = tr_still_used(src)
    if left:
        return [], [f"{fname}: tr() still called at lines {left}; imports kept"], []

    def fix(node, whole_stmt):
        names = [a for a in node.names if a.name != "tr"]
        if len(names) == len(node.names):
            return
        if names:
            txt = ", ".join(a.name + (f" as {a.asname}" if a.asname else "") for a in names)
            edits.append((src.s(node), src.e(node), f"from .{node.module} import {txt}".encode()))
        else:
            edits.append((*src.lines(whole_stmt), b""))

    for n in src.tree.body:
        if isinstance(n, ast.Try) and n.body and isinstance(n.body[0], ast.ImportFrom) \
                and n.body[0].module == "languages" and n.body[0].level == 1 \
                and all(a.name == "tr" for a in n.body[0].names):
            edits.append((*src.lines(n), b""))
        elif isinstance(n, ast.ImportFrom) and n.level == 1 and n.module in ("languages", "utils"):
            fix(n, n)
    return edits, manual, []


def pass_addimport(src, fname, msgids):
    """Add 'from .utils import _trf' if the module calls _trf but does not have it."""
    used = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "_trf"
               for n in ast.walk(src.tree))
    have = any(isinstance(n, ast.FunctionDef) and n.name == "_trf" for n in src.tree.body) or any(
        isinstance(n, ast.ImportFrom) and any(a.name == "_trf" for a in n.names) for n in src.tree.body)
    if not used or have:
        return [], [], []
    last = None
    for n in src.tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            break
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            last = n
    if last is None:
        return [], [f"{fname}: add 'from .utils import _trf' by hand"], []
    pos = src.offs[last.end_lineno]
    return [(pos, pos, b"from .utils import _trf\n")], [], []


PASSES = (pass_defs, pass_report, pass_convert, pass_imports, pass_addimport)


def transform(path, msgids):
    """Run all passes over one file; return (new_text, edit_count, manual, warnings)."""
    raw, total, manual, warns = path.read_bytes(), 0, [], []
    for fn in PASSES:
        edits, m, w = fn(Src(raw), path.name, msgids)
        manual += m
        warns += w
        raw, skipped = apply_edits(raw, edits)
        total += len(edits) - skipped
        if skipped:
            manual.append(f"{path.name}: {skipped} overlapping edit(s) skipped, run the script again")
        ast.parse(raw)  # never continue with a file that does not parse
    return raw.decode("utf-8"), total, manual, warns


def main():
    ap = argparse.ArgumentParser(description="Finish the SnapSplit i18n migration.")
    ap.add_argument("--src-dir", required=True, help="add-on folder with the .py files")
    ap.add_argument("--apply", action="store_true", help="write files (default: dry run)")
    ap.add_argument("--diff", action="store_true", help="print a short diff per file")
    args = ap.parse_args()

    src_dir = Path(args.src_dir).expanduser().resolve()
    try:
        data = runpy.run_path(str(src_dir / "localization.py"))["DICTIONARY"]
        msgids = {k[1] for entries in data.values() for k in entries}
    except Exception as exc:
        print(f"NOTE: localization.py not readable ({exc}); msgid check skipped.")
        msgids = None

    backup = src_dir.parent / "i18n_migration" / f"backup_finish_{time.strftime('%Y%m%d_%H%M%S')}"
    all_manual, all_warns, changed = [], [], 0
    for path in sorted(src_dir.glob("*.py")):
        if path.name in SKIP_FILES or "00" in path.stem:
            continue
        try:
            new, n, manual, warns = transform(path, msgids)
        except SyntaxError as exc:
            all_manual.append(f"{path.name}: cannot parse, skipped ({exc})")
            continue
        all_manual += manual
        all_warns += warns
        old = path.read_text(encoding="utf-8")
        if new == old:
            continue
        changed += 1
        print(f"{path.name}: {n} edit(s)")
        if args.diff:
            for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0))[:120]:
                print("   " + line)
        if args.apply:
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup / path.name)
            path.write_text(new, encoding="utf-8")

    print(f"\nDry run: {not args.apply}   Files changed: {changed}")
    if args.apply and changed:
        print(f"Backup: {backup}")
    for title, items in (("Text not in localization.py", all_warns), ("Manual work", all_manual)):
        print(f"\n== {title}: {len(items)}")
        for item in items:
            print(f"   {item}")


if __name__ == "__main__":
    main()
