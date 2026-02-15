import re


class Parsing:
    @staticmethod
    def parse_config(filename):
        # Define mandatory keys and conversion logic
        MANDATORY_KEYS = {
            "WIDTH": int,
            "HEIGHT": int,
            "ENTRY": lambda v: tuple(map(int, v.split(','))),
            "EXIT": lambda v: tuple(map(int, v.split(','))),
            "OUTPUT_FILE": str,
            "PERFECT": lambda v: v.lower() == "true"
        }

        config = dict()

        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = re.match(r'^(\w+)\s*=\s*(.+)$', line)
                if match:
                    key, value = match.groups()
                    config[key] = value
                else:
                    raise ValueError(f"Invalid config line: '{line}'")

        # Check presence and parse types for mandatory keys
        for key, converter in MANDATORY_KEYS.items():
            if key not in config:
                raise KeyError(f"Mandatory key '{key}' not found in config.")
            try:
                config[key] = converter(config[key])
            except Exception as e:
                raise ValueError(f"Invalid value for {key}: {config[key]!r} ({e})")
        # Convert optional entries to str (keep as raw)
        for key in config:
            if key not in MANDATORY_KEYS:
                config[key] = config[key].strip()
        return config


class Config:
    def __init__(self, filename):
        # Initialize default attributes for mandatory keys
        self.WIDTH = None
        self.HEIGHT = None
        self.ENTRY = None
        self.EXIT = None
        self.OUTPUT_FILE = None
        self.PERFECT = None

        if filename:
            entries = Parsing.parse_config(filename)
            self.__dict__.update(entries)
    
    
    
    


# Example usage:
# config = parse_config("maze.conf")
# print(config)