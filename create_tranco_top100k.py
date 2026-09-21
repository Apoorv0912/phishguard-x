from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

SOURCE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "tranco_GQJ9K.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "tranco_top100k.csv"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

count = 0

with open(SOURCE, "r", encoding="utf-8") as src, \
     open(OUTPUT, "w", encoding="utf-8") as dst:

    for line in src:
        line = line.strip()

        if not line:
            continue

        parts = line.split(",", 1)

        if len(parts) != 2:
            continue

        rank = parts[0].strip()

        try:
            rank = int(rank)
        except ValueError:
            continue

        if rank > 100000:
            break

        dst.write(line + "\n")
        count += 1

print("Top 100K Tranco domains created.")
print("Rows:", count)
print("Output:", OUTPUT)