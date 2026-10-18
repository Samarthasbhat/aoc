import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from toolbox import *

HERE = Path(__file__).parent

WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def parse(text):
    return text.strip().splitlines()

def calibration(line, use_words):
    digits = []
    for i, ch in enumerate(line):
        if ch.isdigit():
            digits.append(int(ch))
        elif use_words:
            for value, word in enumerate(WORDS, start=1):
                if line.startswith(word, i):
                    digits.append(value)
    if not digits:
        return 0
    return digits[0] * 10 + digits[-1]

def part1(data):
    return sum(calibration(line, use_words=False) for line in data)

def part2(data):
    return sum(calibration(line, use_words=True) for line in data)

if __name__ == "__main__":
    fname = "sample.txt" if "-s" in sys.argv else "input.txt"
    data = parse((HERE / fname).read_text())
    for name, fn in (("Part 1", part1), ("Part 2", part2)):
        t = time.perf_counter()
        ans = fn(data)
        print(f"{name}: {ans}  ({time.perf_counter() - t:.3f}s)")