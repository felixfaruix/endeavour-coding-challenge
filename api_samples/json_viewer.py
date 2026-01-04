import json

with open("api_samples/pikachu.json", "r", encoding="utf-16") as f:
    data = json.load(f)

with open("api_samples/pikachu_clean.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

