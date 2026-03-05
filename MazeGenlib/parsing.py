import re
from typing import Callable, Any
from .errors import MazeError


class Parsing:
    @staticmethod
    def parse_config(filename: str) -> dict[str, Any]:
        MANDATORY_KEYS: dict[str, Callable[[str], Any]] = {
            "WIDTH": int,
            "HEIGHT": int,
            "ENTRY": lambda v: tuple(map(int, v.split(','))),
            "EXIT": lambda v: tuple(map(int, v.split(','))),
            "OUTPUT_FILE": str,
            "PERFECT": lambda v: v.lower() == "true",
            "SEED": int
        }

        config: dict[str, Any] = {}

        try:
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
                        raise MazeError(f"Invalid config line: '{line}'")
        except Exception as e:
            raise MazeError(f"config file error: {e}")

        for key, converter in MANDATORY_KEYS.items():
            if key not in config:
                raise MazeError(f"Mandatory key '{key}' not found in config.")
            try:
                config[key] = converter(config[key])
            except Exception as e:
                raise MazeError(
                    f"Invalid value for {key}: {
                        config[key]!r} ({e})")
        for key in config:
            if key not in MANDATORY_KEYS:
                config[key] = config[key].strip()
        return config


class Config:
    def __init__(self, filename: str) -> None:
        self.WIDTH: int
        self.HEIGHT: int
        self.ENTRY: tuple[int, int]
        self.EXIT: tuple[int, int]
        self.OUTPUT_FILE: str
        self.PERFECT: bool
        self.SEED: int
        self.pattern: bool = False

        if filename:
            entries = Parsing.parse_config(filename)
            self.__dict__.update(entries)
        if self.HEIGHT >= 7 and self.WIDTH >= 9:
            self.pattern = True
        else:
            self.pattern = False

        MIN_WIDTH, MAX_WIDTH = 3, 250
        MIN_HEIGHT, MAX_HEIGHT = 3, 180

        if self.WIDTH < MIN_WIDTH or self.HEIGHT < MIN_HEIGHT:
            raise MazeError(
                f"Maze too small: WIDTH={
                    self.WIDTH}, HEIGHT={
                    self.HEIGHT}. Minimum is {MIN_WIDTH}x{MIN_HEIGHT}.")

        if self.WIDTH > MAX_WIDTH or self.HEIGHT > MAX_HEIGHT:
            raise MazeError(
                f"Maze too small: WIDTH={
                    self.WIDTH}, HEIGHT={
                    self.HEIGHT}. Maximu is {MAX_WIDTH}x{MAX_HEIGHT}.")

        if not (0 <= self.ENTRY[0] < self.WIDTH and 0 <=
                self.ENTRY[1] < self.HEIGHT):
            raise MazeError(
                f"ENTRY coordinates {
                    self.ENTRY} are out of bounds for maze size {
                    self.WIDTH}x{
                    self.HEIGHT}")

        if not (0 <= self.EXIT[0] < self.WIDTH and 0 <=
                self.EXIT[1] < self.HEIGHT):
            raise MazeError(
                f"EXIT coordinates {
                    self.EXIT} are out of bounds for maze size {
                    self.WIDTH}x{
                    self.HEIGHT}")

        if self.ENTRY == self.EXIT:
            raise MazeError(
                f"ENTRY and EXIT cannot be the same position: {
                    self.ENTRY}")
