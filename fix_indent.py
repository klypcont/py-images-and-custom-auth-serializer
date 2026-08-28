
path = "cinema/models.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "image = models.ImageField" in line or "null=True" in line and i > 95:
        # ќчистим блок вокруг 104 строки и заменим его правильным синтаксисом
        pass

# ѕолна€ безопасна€ замена проблемного фрагмента через регул€рки или поиск
content = "".join(lines)
target = "image = models.ImageField(\n        null=True,\n        upload_to=movie_image_file_path,\n    )"
# ≈сли там сломана индентаци€, заменим всю модель или метод

