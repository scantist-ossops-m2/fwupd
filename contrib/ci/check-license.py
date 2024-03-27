#!/usr/bin/python3
#
# Copyright (C) 2021 Richard Hughes <richard@hughsie.com>
# Copyright (C) 2021 Mario Limonciello <superm1@gmail.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import glob
import os
import sys
import fnmatch


def _is_source_file(filename: str) -> bool:
    for pat in ["*.c", "*.h", "*.py", "*.rs"]:
        if fnmatch.fnmatch(filename, pat):
            return True
    return False


def test_files() -> int:
    rc: int = 0
    build_dirs = [os.path.dirname(cf) for cf in glob.glob("**/config.h")]

    for fn in glob.glob("**", recursive=True):
        if not _is_source_file(fn):
            continue
        if "meson-private" in fn:
            continue
        if os.path.isdir(fn):
            continue
        if fn.startswith(tuple(build_dirs)):
            continue
        if fn.startswith("subprojects"):
            continue
        if fn.startswith("venv"):
            continue
        if fn.startswith("dist"):
            continue
        if fn.endswith("check-license.py"):
            continue
        lic: str = ""
        cprts: list[str] = []
        lines: list[str] = []
        with open(fn, "r") as f:
            for line in f.read().split("\n"):
                lines.append(line)
        if len(lines) < 2:
            continue
        for line in lines:
            if line.find("SPDX-License-Identifier:") != -1:
                lic = line.split(":")[1]
            if line.find("Copyright") != -1:
                cprts.append(line.strip())
        if not lic:
            print(f"{fn} does not specify a license")
            rc = 1
            continue
        if not cprts:
            print(f"{fn} does not specify any copyright")
            rc = 1
            continue
        if "LGPL-2.1-or-later" not in lic:
            print(f"{fn} does not contain LGPL-2.1-or-later ({lic})")
            rc = 1
            continue
    return rc


if __name__ == "__main__":
    # all done!
    sys.exit(test_files())
