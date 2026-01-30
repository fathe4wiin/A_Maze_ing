from dataclasses import dataclass

@dataclass
class Config:
    width
    height
    entry
    exit
    perfect
    output_file
    seed = None


def parse_bool(v):
    return v.lower() in ("1", "true", "yes", "y")


def parse_config(file):
    data = {}

    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid line: {line}")
        k, v = map(str.strip, line.split("=", 1))
        if k in data:
            raise ValueError(f"Duplicate key: {k}")
        data[k] = v

    for k in ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"):
        if k not in data:
            raise ValueError(f"Missing key: {k}")

    width = int(data["WIDTH"])
    height = int(data["HEIGHT"])

    entry = tuple(map(int, data["ENTRY"].split(",")))
    exit_ = tuple(map(int, data["EXIT"].split(",")))

    if width < 1 or height < 1:
        raise ValueError("WIDTH and HEIGHT must be >= 1")

    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit_)):
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"{name} out of bounds")

    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different")

    return Config(
        width,
        height,
        entry,
        exit_,
        parse_bool(data["PERFECT"]),
        data["OUTPUT_FILE"],
        int(data["SEED"]) if "SEED" in data else None
    )
