import json

def save_data(file, data):
    with open(file, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)   

def load_data(file):
    with open(file, "r", encoding="UTF-8") as f:
        data = json.load(f)

    return data