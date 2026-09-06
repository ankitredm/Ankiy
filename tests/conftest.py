"""Shared pytest fixtures."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def smoke_bin(tmp_path):
    """A tiny token .bin file with a known token stream."""
    # 40 tokens, ids in [0, 20) — enough to create several 8-wide windows.
    stream = np.arange(0, 40, dtype=np.uint16) % 20
    path = tmp_path / "data.bin"
    stream.tofile(str(path))
    return str(path)
