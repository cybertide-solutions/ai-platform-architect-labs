"""AsterWorks enterprise AI platform laboratory. All business data is fictional."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
def read_data(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
