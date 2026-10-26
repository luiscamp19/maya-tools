"""Batch Renamer for Maya.

Rename the selected nodes with a prefix, suffix, search/replace and
optional numbering, e.g. ``L_arm_##_JNT`` -> ``L_arm_01_JNT``, ``L_arm_02_JNT``.

Usage (Maya Script Editor, Python tab)::

    import batch_renamer
    batch_renamer.show()

Author: Luis Martinez (luiscamp19)
"""

import re

from maya import cmds

WINDOW = "batchRenamerWin"


def build_name(base, index, prefix="", suffix="", search="", replace="",
               pattern="", start=1, padding=2):
    """Return the new name for one node. Pure Python, testable outside Maya."""
    if pattern:
        # '#' run in the pattern is replaced by the padded number.
        runs = re.findall(r"#+", pattern)
        hashes = max(len(r) for r in runs) if runs else 0
        number = str(start + index).zfill(max(padding, hashes))
        name = pattern.replace("#" * hashes, number) if hashes else pattern
    else:
        name = base.replace(search, replace) if search else base
    return "{}{}{}".format(prefix, name, suffix)


def rename_selection(prefix="", suffix="", search="", replace="",
                     pattern="", start=1, padding=2):
    """Rename selected nodes inside a single undo chunk. Returns new names."""
    nodes = cmds.ls(selection=True, long=True) or []
    if not nodes:
        cmds.warning("Batch Renamer: select something first.")
        return []

    # Rename deepest nodes first so parent paths stay valid.
    order = sorted(range(len(nodes)), key=lambda i: nodes[i].count("|"),
                   reverse=True)
    new_names = [None] * len(nodes)

    cmds.undoInfo(openChunk=True, chunkName="batchRename")
    try:
        for i in order:
            short = nodes[i].split("|")[-1]
            target = build_name(short, i, prefix, suffix, search, replace,
                                pattern, start, padding)
            new_names[i] = cmds.rename(nodes[i], target)
    finally:
        cmds.undoInfo(closeChunk=True)

    print("Batch Renamer: renamed {} node(s).".format(len(nodes)))
    return new_names


def show():
    """Open the Batch Renamer window."""
    if cmds.window(WINDOW, exists=True):
        cmds.deleteUI(WINDOW)

    cmds.window(WINDOW, title="Batch Renamer", widthHeight=(320, 230))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=4)

    fields = {}
    for key, label in (("pattern", "Pattern (##)"), ("search", "Search"),
                       ("replace", "Replace"), ("prefix", "Prefix"),
                       ("suffix", "Suffix")):
        fields[key] = cmds.textFieldGrp(label=label, columnWidth2=(90, 210))
    start = cmds.intFieldGrp(label="Start / Pad", numberOfFields=2,
                             value1=1, value2=2, columnWidth3=(90, 100, 100))

    def _apply(*_):
        values = {k: cmds.textFieldGrp(f, query=True, text=True)
                  for k, f in fields.items()}
        rename_selection(start=cmds.intFieldGrp(start, query=True, value1=True),
                         padding=cmds.intFieldGrp(start, query=True, value2=True),
                         **values)

    cmds.button(label="Rename", height=32, command=_apply)
    cmds.showWindow(WINDOW)
