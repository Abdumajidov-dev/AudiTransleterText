import os

# Cloud AI chiqargan matn
with open("output.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Belgilar bo‘yicha bo‘lish (masalan, ###)
sections = text.split("###")

for i, section in enumerate(sections, start=1):
    filename = f"section_{i}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(section.strip())

# GitHub’ga push qilish
os.system("git add .")
os.system('git commit -m "Cloud AI output bo‘limlarga bo‘lindi"')
os.system("git push origin main")
