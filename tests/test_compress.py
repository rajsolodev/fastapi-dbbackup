# tests/test_compress.py
from fastapi_dbbackup.compress import compress, decompress

def test_compress_file(tmp_path):
    file = tmp_path / "test.dump"
    file.write_text("hello")

    gz = compress(file)

    assert gz.exists()
    assert gz.suffix.endswith(".gz")
    assert not file.exists()

def test_decompress_file(tmp_path):
    file = tmp_path / "test.dump"
    file.write_text("hello")

    gz = compress(file)
    decompressed = decompress(gz)

    assert decompressed.exists()
    assert decompressed.suffix == ".dump"
    assert decompressed.read_text() == "hello"
    assert not gz.exists()
