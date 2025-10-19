import csv
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Optional, Tuple, Dict, Any

from Services.phone_service import check_phone_availability
from Utils.regex_helper import is_valid_phone_number


DEFAULT_FIXTURES_DIR = os.path.join("Tests", "fixtures")
DEFAULT_RESULTS_DIR = os.path.join("Tests", "results")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _now_timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def validate_phones(phones: Optional[List[str]] = None,
                    fixture: Optional[str] = None,
                    out_dir: str = DEFAULT_RESULTS_DIR) -> Dict[str, Any]:
    """
    Validate a list of phone numbers or a CSV fixture. Writes a CSV report to `out_dir`.

    If `fixture` is provided, it is read from `Tests/fixtures/<fixture>` and the first column
    of each row is taken as the phone number. If rows have extra columns they are treated as
    expected values (expected_valid, expected_available) when present.

    Returns a summary dict with counts and the path to the generated report.
    """
    _ensure_dir(out_dir)

    entries: List[Tuple[str, Optional[str], Optional[str]]] = []

    if fixture:
        fixture_path = os.path.join(DEFAULT_FIXTURES_DIR, fixture)
        if not os.path.isfile(fixture_path):
            raise FileNotFoundError(f"Fixture not found: {fixture_path}")
        with open(fixture_path, newline='', encoding='utf-8') as fh:
            reader = csv.reader(fh)
            for row in reader:
                if not row:
                    continue
                phone = row[0].strip()
                expected_valid = row[1].strip() if len(row) > 1 and row[1] != "" else None
                expected_available = row[2].strip() if len(row) > 2 and row[2] != "" else None
                entries.append((phone, expected_valid, expected_available))
    elif phones is not None:
        for p in phones:
            entries.append((p, None, None))
    else:
        raise ValueError("Either phones or fixture must be provided")

    results = []
    counts = {"total": 0, "valid": 0, "invalid": 0, "available": 0, "unavailable": 0}

    for phone, expected_valid, expected_available in entries:
        counts["total"] += 1
        valid = bool(is_valid_phone_number(phone))
        available, msg = check_phone_availability(phone)
        counts["valid"] += 1 if valid else 0
        counts["invalid"] += 0 if valid else 1
        counts["available"] += 1 if available else 0
        counts["unavailable"] += 0 if available else 1

        note_parts = []
        if not valid:
            note_parts.append("invalid_format")
        if not available:
            note_parts.append("unavailable")
        note = ";".join(note_parts) if note_parts else "ok"

        results.append({
            "phone": phone,
            "valid": str(valid),
            "available": str(available),
            "message": msg,
            "expected_valid": expected_valid if expected_valid is not None else "",
            "expected_available": expected_available if expected_available is not None else "",
            "note": note,
        })

    report_name = f"report-{_now_timestamp()}.csv"
    report_path = os.path.join(out_dir, report_name)
    with open(report_path, "w", newline='', encoding='utf-8') as outfh:
        writer = csv.DictWriter(outfh, fieldnames=["phone", "valid", "available", "message", "expected_valid", "expected_available", "note"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    summary = {
        "report": report_path,
        "counts": counts,
        "total_rows": len(results),
    }
    return summary


class _Handler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict):
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != '/validate':
            self._send_json(404, {"error": "not found"})
            return
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            self._send_json(400, {"error": "empty body"})
            return
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception as e:
            self._send_json(400, {"error": "invalid json", "detail": str(e)})
            return

        try:
            phones = payload.get('phones')
            fixture = payload.get('fixture')
            summary = validate_phones(phones=phones, fixture=fixture)
            self._send_json(200, {"ok": True, "summary": summary})
        except Exception as e:
            self._send_json(500, {"ok": False, "error": str(e)})


def run_server(host: str = '127.0.0.1', port: int = 8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, _Handler)
    print(f"Validation API listening on http://{host}:{port} (POST /validate)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server")
    finally:
        httpd.server_close()


if __name__ == '__main__':
    import sys
    fixture = None
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            if a.startswith('fixture='):
                fixture = a.split('=', 1)[1]
    if fixture is None:
        fixture = 'mixed.csv'
    print('Running validation once against fixture:', fixture)
    summary = validate_phones(fixture=fixture)
    print('Summary:', summary)
