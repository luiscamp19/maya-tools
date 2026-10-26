# maya-tools

Python tools for Autodesk Maya, aimed at speeding up everyday animation and
rigging pipeline tasks. Built by Luis Martinez, 3D generalist moving into
Pipeline TD work.

## Tools

| Tool | What it does |
|------|--------------|
| [`batch_renamer.py`](scripts/batch_renamer.py) | Rename selected nodes with patterns (`L_arm_##_JNT`), search/replace, prefix and suffix. One undo step. |

## Install

1. Copy the files in `scripts/` to your Maya scripts folder
   (e.g. `Documents/maya/<version>/scripts`).
2. In the Script Editor (Python tab):

```python
import batch_renamer
batch_renamer.show()
```

Tested with Maya 2022+ (Python 3).

## Roadmap

- [ ] Scene cleanup checker (unused nodes, bad names, non-frozen transforms)
- [ ] Playblast exporter with naming conventions
- [ ] Shelf installer
