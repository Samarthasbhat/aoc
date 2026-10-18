"""Reusable Advent of Code helpers. Import with: from toolbox import *"""
import re
import heapq
from collections import deque, defaultdict, Counter
from functools import cache
from itertools import product, combinations, permutations, pairwise
from math import gcd, lcm, prod

# ---------- Parsing ----------
def ints(s):
    """All integers in a string, including negatives."""
    return list(map(int, re.findall(r"-?\d+", s)))

def parse_grid(text):
    """Return dict {(row, col): char} plus (rows, cols)."""
    lines = text.splitlines()
    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}
    return grid, len(lines), len(lines[0])

def blocks(text):
    """Split input on blank lines."""
    return text.strip().split("\n\n")

# ---------- Grid ----------
DIRS4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
DIRS8 = DIRS4 + [(-1, 1), (1, 1), (1, -1), (-1, -1)]

def neighbors(pos, grid, dirs=DIRS4):
    r, c = pos
    for dr, dc in dirs:
        n = (r + dr, c + dc)
        if n in grid:
            yield n

def find(grid, ch):
    return next(p for p, v in grid.items() if v == ch)

# ---------- Graph search ----------
def bfs(start, goal_fn, next_fn):
    """Shortest steps from start to any state where goal_fn is True."""
    q = deque([(start, 0)])
    seen = {start}
    while q:
        state, d = q.popleft()
        if goal_fn(state):
            return d
        for n in next_fn(state):
            if n not in seen:
                seen.add(n)
                q.append((n, d + 1))
    return None

def dijkstra(start, goal_fn, next_fn):
    """next_fn(state) yields (neighbor, cost). Returns min cost or None."""
    pq = [(0, start)]
    best = {start: 0}
    while pq:
        cost, state = heapq.heappop(pq)
        if goal_fn(state):
            return cost
        if cost > best.get(state, float("inf")):
            continue
        for n, w in next_fn(state):
            nc = cost + w
            if nc < best.get(n, float("inf")):
                best[n] = nc
                heapq.heappush(pq, (nc, n))
    return None

# ---------- Math ----------
def crt(rems, mods):
    """Chinese Remainder Theorem (moduli must be pairwise coprime)."""
    M = prod(mods)
    return sum(r * (M // m) * pow(M // m, -1, m) for r, m in zip(rems, mods)) % M

def merge_intervals(ivs):
    """Merge inclusive (lo, hi) intervals."""
    out = []
    for lo, hi in sorted(ivs):
        if out and lo <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return [tuple(x) for x in out]

# ---------- Cycle detection ----------
def run_with_cycle(state, step_fn, total):
    """Apply step_fn `total` times, skipping ahead once a state repeats.
    State must be hashable."""
    seen = {}
    history = []
    i = 0
    while i < total:
        if state in seen:
            start = seen[state]
            period = i - start
            return history[start + (total - start) % period]
        seen[state] = i
        history.append(state)
        state = step_fn(state)
        i += 1
    return state