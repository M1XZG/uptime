import yaml
import os
import glob
import json

CONFIG = ".upptimerc.yml"
HISTORY_DIR = "history"
OUTPUT = "status-dashboard.html"

def load_config():
    with open(CONFIG, "r") as f:
        return yaml.safe_load(f)

def get_status(site_name):
    # Try to find a matching history file
    pattern = os.path.join(HISTORY_DIR, f"{site_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '').replace('.', '').replace('_', '-')}.yml")
    matches = glob.glob(pattern)
    if not matches:
        return "unknown"
    try:
        with open(matches[0], "r") as f:
            for line in f:
                if line.startswith("status:"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        return "unknown"
    return "unknown"

def main():
    config = load_config()
    sites = config.get("sites", [])
    rows = []
    for site in sites:
        name = site.get("name", "")
        url = site.get("url", "")
        status = get_status(name)
        rows.append(f"<tr><td>{name}</td><td><a href='{url}'>{url}</a></td><td>{status}</td></tr>")
    html = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>Uptime Dashboard</title>
    <style>
        body {{ font-family: sans-serif; background: #f9f9f9; }}
        table {{ border-collapse: collapse; margin: 2em auto; background: #fff; box-shadow: 0 2px 8px #0001; }}
        th, td {{ padding: 0.7em 1.2em; border: 1px solid #ddd; }}
        th {{ background: #222; color: #fff; }}
        tr:nth-child(even) {{ background: #f3f3f3; }}
        .up {{ color: green; font-weight: bold; }}
        .down {{ color: red; font-weight: bold; }}
        .unknown {{ color: #888; }}
    </style>
</head>
<body>
    <h2 style='text-align:center'>Uptime Dashboard</h2>
    <table>
        <tr><th>Name</th><th>URL</th><th>Status</th></tr>
        {''.join(rows)}
    </table>
</body>
</html>
"""
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"Dashboard generated: {OUTPUT}")

if __name__ == "__main__":
    main()
