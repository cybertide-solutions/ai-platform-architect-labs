"""Point every notebook's setup cell at your GitHub copy of this course.

Usage (run once from the course folder, after you create the GitHub repo):
    python tools/set_repo_url.py https://github.com/<your-username>/ai-platform-architect-labs.git
"""
import json, pathlib, re, sys

if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
    sys.exit(__doc__)
url = sys.argv[1]
root = pathlib.Path(__file__).resolve().parent.parent
pattern = re.compile(r'REPO_URL = "https://[^"]*"')
for nb_path in sorted((root / "notebooks").glob("*.ipynb")):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            if "REPO_URL = " in src:
                cell["source"] = pattern.sub(f'REPO_URL = "{url}"', src)
    nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("updated", nb_path.name)

readme = root / "README.md"
if readme.exists():
    gh = url.removesuffix(".git").replace("https://github.com/", "")
    readme.write_text(re.sub(r"YOUR-GITHUB-USERNAME/ai-platform-architect-labs", gh, readme.read_text(encoding="utf-8")),
                      encoding="utf-8")
    print("updated README.md Colab links")
