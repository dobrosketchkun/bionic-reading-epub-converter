"""Tests for brec_v2 CLI exit codes."""
import sys
import zipfile

import brec_v2


def test_main_missing_input_returns_nonzero(tmp_path, capsys, monkeypatch):
    missing = tmp_path / "does-not-exist.epub"
    out = tmp_path / "out.epub"
    monkeypatch.setattr(sys, "argv", ["brec_v2", str(missing), str(out)])
    result = brec_v2.main()
    assert result == 1
    captured = capsys.readouterr()
    assert "does-not-exist.epub" in captured.out


def test_main_success_returns_zero(tmp_path, monkeypatch):
    src = tmp_path / "in.epub"
    with zipfile.ZipFile(src, "w") as zf:
        zf.writestr("OEBPS/ch1.html", "<html><body><p>Hello world</p></body></html>")
    out = tmp_path / "out.epub"
    monkeypatch.setattr(sys, "argv", ["brec_v2", str(src), str(out)])
    result = brec_v2.main()
    assert result == 0
    assert out.exists()
