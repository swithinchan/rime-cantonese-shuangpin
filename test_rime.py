#!/usr/bin/env python3
"""Simulate keystrokes against a custom Rime schema using librime's C API.

This replaces rime_api_console, which is not shipped in Fedora's
librime-tools package, with a minimal ctypes binding around librime.so.
"""

from __future__ import annotations

import ctypes
import os
from pathlib import Path


LIBRIME = "/usr/lib64/librime.so.1"
USER_DATA_DIR = Path(__file__).resolve().parent
SHARED_DATA_DIR = Path("/usr/share/rime-data")
STAGING_DIR = USER_DATA_DIR / "build"


class RimeTraits(ctypes.Structure):
    _fields_ = [
        ("data_size", ctypes.c_int),
        ("shared_data_dir", ctypes.c_char_p),
        ("user_data_dir", ctypes.c_char_p),
        ("distribution_name", ctypes.c_char_p),
        ("distribution_code_name", ctypes.c_char_p),
        ("distribution_version", ctypes.c_char_p),
        ("app_name", ctypes.c_char_p),
        ("modules", ctypes.POINTER(ctypes.c_char_p)),
        ("min_log_level", ctypes.c_int),
        ("log_dir", ctypes.c_char_p),
        ("prebuilt_data_dir", ctypes.c_char_p),
        ("staging_dir", ctypes.c_char_p),
    ]


class RimeComposition(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_int),
        ("cursor_pos", ctypes.c_int),
        ("sel_start", ctypes.c_int),
        ("sel_end", ctypes.c_int),
        ("preedit", ctypes.c_char_p),
    ]


class RimeCandidate(ctypes.Structure):
    _fields_ = [
        ("text", ctypes.c_char_p),
        ("comment", ctypes.c_char_p),
        ("reserved", ctypes.c_void_p),
    ]


class RimeMenu(ctypes.Structure):
    _fields_ = [
        ("page_size", ctypes.c_int),
        ("page_no", ctypes.c_int),
        ("is_last_page", ctypes.c_int),
        ("highlighted_candidate_index", ctypes.c_int),
        ("num_candidates", ctypes.c_int),
        ("candidates", ctypes.POINTER(RimeCandidate)),
        ("select_keys", ctypes.c_char_p),
    ]


class RimeContext(ctypes.Structure):
    _fields_ = [
        ("data_size", ctypes.c_int),
        ("composition", RimeComposition),
        ("menu", RimeMenu),
        ("commit_text_preview", ctypes.c_char_p),
        ("select_labels", ctypes.POINTER(ctypes.c_char_p)),
    ]


class RimeCommit(ctypes.Structure):
    _fields_ = [
        ("data_size", ctypes.c_int),
        ("text", ctypes.c_char_p),
    ]


class RimeStatus(ctypes.Structure):
    _fields_ = [
        ("data_size", ctypes.c_int),
        ("schema_id", ctypes.c_char_p),
        ("schema_name", ctypes.c_char_p),
        ("is_disabled", ctypes.c_int),
        ("is_composing", ctypes.c_int),
        ("is_ascii_mode", ctypes.c_int),
        ("is_full_shape", ctypes.c_int),
        ("is_simplified", ctypes.c_int),
        ("is_traditional", ctypes.c_int),
        ("is_ascii_punct", ctypes.c_int),
    ]


class RimeTester:
    def __init__(
        self,
        user_data_dir: Path = USER_DATA_DIR,
        shared_data_dir: Path = SHARED_DATA_DIR,
        staging_dir: Path | None = None,
    ) -> None:
        self.lib = ctypes.CDLL(LIBRIME)
        self.user_data_dir = user_data_dir
        self.shared_data_dir = shared_data_dir
        self.staging_dir = staging_dir or (user_data_dir / "build")
        self._bind()

    def _bind(self) -> None:
        lib = self.lib
        def bind(name: str, argtypes: list[object] | None, restype: object | None) -> None:
            func = getattr(lib, name)
            if argtypes is not None:
                func.argtypes = argtypes
            if restype is not None:
                func.restype = restype

        bind("_Z9RimeSetupP13rime_traits_t", [ctypes.POINTER(RimeTraits)], None)
        bind("_Z14RimeInitializeP13rime_traits_t", [ctypes.POINTER(RimeTraits)], None)
        bind("_Z12RimeFinalizev", [], None)

        bind("_Z20RimeStartMaintenancei", [ctypes.c_int], ctypes.c_int)
        bind("_Z25RimeJoinMaintenanceThreadv", [], None)

        bind("_Z17RimeCreateSessionv", [], ctypes.c_ulong)
        bind("_Z18RimeDestroySessionm", [ctypes.c_ulong], ctypes.c_int)
        bind("_Z16RimeSelectSchemamPKc", [ctypes.c_ulong, ctypes.c_char_p], ctypes.c_int)
        bind("_Z20RimeGetCurrentSchemamPcm", [ctypes.c_ulong, ctypes.c_char_p, ctypes.c_size_t], ctypes.c_int)

        bind("_Z23RimeSimulateKeySequencemPKc", [ctypes.c_ulong, ctypes.c_char_p], ctypes.c_int)
        bind("_Z20RimeClearCompositionm", [ctypes.c_ulong], None)

        bind("_Z14RimeGetContextmP14rime_context_t", [ctypes.c_ulong, ctypes.POINTER(RimeContext)], ctypes.c_int)
        bind("_Z15RimeFreeContextP14rime_context_t", [ctypes.POINTER(RimeContext)], ctypes.c_int)

        bind("_Z13RimeGetCommitmP13rime_commit_t", [ctypes.c_ulong, ctypes.POINTER(RimeCommit)], ctypes.c_int)
        bind("_Z14RimeFreeCommitP13rime_commit_t", [ctypes.POINTER(RimeCommit)], ctypes.c_int)

        bind("_Z13RimeGetStatusmP13rime_status_t", [ctypes.c_ulong, ctypes.POINTER(RimeStatus)], ctypes.c_int)
        bind("_Z14RimeFreeStatusP13rime_status_t", [ctypes.POINTER(RimeStatus)], ctypes.c_int)

    def setup(self) -> None:
        traits = RimeTraits()
        traits.data_size = ctypes.sizeof(RimeTraits) - ctypes.sizeof(ctypes.c_int)
        traits.shared_data_dir = str(self.shared_data_dir).encode()
        traits.user_data_dir = str(self.user_data_dir).encode()
        traits.distribution_name = b"Rime"
        traits.distribution_code_name = b"fcitx-rime"
        traits.distribution_version = b"5.1.15"
        traits.app_name = b"rime.jyutping-nc-test"
        traits.min_log_level = 0
        traits.log_dir = b"/tmp"
        traits.prebuilt_data_dir = str(self.staging_dir).encode()
        traits.staging_dir = str(self.staging_dir).encode()

        getattr(self.lib, "_Z9RimeSetupP13rime_traits_t")(ctypes.byref(traits))
        getattr(self.lib, "_Z14RimeInitializeP13rime_traits_t")(ctypes.byref(traits))
        getattr(self.lib, "_Z20RimeStartMaintenancei")(True)
        getattr(self.lib, "_Z25RimeJoinMaintenanceThreadv")()

    def teardown(self) -> None:
        getattr(self.lib, "_Z12RimeFinalizev")()

    def run_case(self, keystrokes: str) -> tuple[bool, dict[str, object]]:
        session = getattr(self.lib, "_Z17RimeCreateSessionv")()
        info: dict[str, object] = {"session": session}
        try:
            selected = getattr(self.lib, "_Z16RimeSelectSchemamPKc")(session, b"jyutping_nc")
            info["selected_schema"] = selected

            current = ctypes.create_string_buffer(256)
            got_schema = getattr(self.lib, "_Z20RimeGetCurrentSchemamPcm")(session, current, len(current))
            info["current_schema"] = current.value.decode("utf-8", "replace") if got_schema else None

            sent = getattr(self.lib, "_Z23RimeSimulateKeySequencemPKc")(session, keystrokes.encode("utf-8"))
            info["simulate_ok"] = sent

            committed: list[str] = []
            while True:
                commit = RimeCommit()
                commit.data_size = ctypes.sizeof(RimeCommit) - ctypes.sizeof(ctypes.c_int)
                if not getattr(self.lib, "_Z13RimeGetCommitmP13rime_commit_t")(session, ctypes.byref(commit)):
                    break
                committed.append(ctypes.string_at(commit.text).decode("utf-8", "replace"))
                getattr(self.lib, "_Z14RimeFreeCommitP13rime_commit_t")(ctypes.byref(commit))
            info["committed"] = committed

            context = RimeContext()
            context.data_size = ctypes.sizeof(RimeContext) - ctypes.sizeof(ctypes.c_int)
            got_context = getattr(self.lib, "_Z14RimeGetContextmP14rime_context_t")(session, ctypes.byref(context))
            info["context_ok"] = got_context
            info["preedit"] = (
                ctypes.string_at(context.composition.preedit).decode("utf-8", "replace")
                if context.composition.preedit
                else ""
            )
            info["preview"] = (
                ctypes.string_at(context.commit_text_preview).decode("utf-8", "replace")
                if context.commit_text_preview
                else ""
            )

            candidates: list[str] = []
            num = context.menu.num_candidates
            for index in range(max(0, num)):
                text = context.menu.candidates[index].text
                candidates.append(ctypes.string_at(text).decode("utf-8", "replace"))
            info["candidates"] = candidates
            info["highlighted"] = context.menu.highlighted_candidate_index

            getattr(self.lib, "_Z15RimeFreeContextP14rime_context_t")(ctypes.byref(context))
            return bool(candidates or committed), info
        finally:
            getattr(self.lib, "_Z18RimeDestroySessionm")(session)


TEST_CASES = [
    ("lg lg", "靚靚"),
    ("ij", "關"),
    ("ttlb", "鐵路"),
    ("lc oc", "臘鴨"),
    ("ul gh bq", "規格表"),
]


def main() -> int:
    tester = RimeTester()
    failures = 0
    try:
        tester.setup()
        for keystrokes, expected in TEST_CASES:
            ok, info = tester.run_case(keystrokes)
            candidates = info.get("candidates", [])
            committed = info.get("committed", [])
            preview = info.get("preview", "")
            continuous = keystrokes.replace(" ", "")
            _, continuous_info = tester.run_case(continuous)
            continuous_candidates = continuous_info.get("candidates", [])
            continuous_committed = continuous_info.get("committed", [])
            continuous_preview = continuous_info.get("preview", "")
            if " " in keystrokes:
                # Multi-syllable tests are typed as a continuous double-pinyin
                # stream in real Rime usage. The spaces in the prompt separate
                # syllables visually; Rime itself uses them as candidate
                # selection keys.
                passed = bool(continuous_candidates) and continuous_candidates[0] == expected
            else:
                passed = bool(candidates) and candidates[0] == expected
            if not passed:
                failures += 1
            status = "PASS" if passed else "FAIL"
            print(f"[{status}] {keystrokes!r} -> expected {expected!r}")
            print(f"        candidates={candidates!r}")
            print(f"        committed={committed!r}")
            print(f"        continuous={continuous!r} candidates={continuous_candidates!r} "
                  f"committed={continuous_committed!r}")
            if not passed:
                print(f"        preedit={info.get('preedit')!r} "
                      f"preview={info.get('preview')!r} "
                      f"schema={info.get('current_schema')!r}")
    finally:
        tester.teardown()
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
