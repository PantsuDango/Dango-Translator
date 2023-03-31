import requests


def detectPort(port=6666):
    try:
        return requests.head("http://127.0.0.1:%d/ocr/api" % port, timeout=2).headers.get("Dango-OCR") == "OK"
    except Exception:
        return False
