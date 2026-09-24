# LKH Backup Binaries

This directory stores backup copies of the LKH-3 solver for reproducible
research experiments in AeroEdgeRL.

LKH is an external dependency authored by Keld Helsgaun. It is not part of
AeroEdgeRL and is not modified here. The author's page describes the code as
available for academic and non-commercial use, with rights reserved by the
author. Keep this directory only for research and lab-machine reproducibility.

Official source:

- <http://webhotel4.ruc.dk/~keld/research/LKH-3/>
- <http://akira.ruc.dk/~keld/research/LKH-3/>

Included files:

| File | Purpose | SHA256 |
| --- | --- | --- |
| `LKH-3.0.13.tgz` | Official LKH-3 source archive. | `693bb5e6b048e58f11584f32ac56325020f6d65fbabbec5d6da95528bcad3f04` |
| `LKH-3.exe` | Official Windows x64 executable from the author page. | `b44414b7c9aa111b4e782ba13fd2cf4684bf3ad505ba1f5d65822b8ad162c044` |
| `LKH-macos-arm64` | Locally compiled macOS arm64 executable from `LKH-3.0.13.tgz`. | `ff094512020c495a15e551d608314229804c298a4352572ad039813f5115c24e` |

Use the solver through the `AEROEDGE_LKH_BINARY` environment variable.

macOS:

```bash
export AEROEDGE_LKH_BINARY="$PWD/third_party/lkh/LKH-macos-arm64"
pytest -q tests/test_lkh.py
```

Windows PowerShell:

```powershell
$env:AEROEDGE_LKH_BINARY = "$PWD\third_party\lkh\LKH-3.exe"
pytest -q tests/test_lkh.py
```

WSL/Linux should build the source archive locally and point
`AEROEDGE_LKH_BINARY` to the compiled `LKH` executable.
