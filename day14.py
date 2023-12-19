import re


def part1(lines):
    grid = lines
    print(grid)
    w = len(lines[0])
    h = len(lines)
    trans_grid = [[grid[y][x] for y in range(h)] for x in range(w)]

    result = 0
    for r in trans_grid:
        sections = "".join(["".join(sorted(x, reverse=True)) for x in re.split(r'(#)', "".join(r))])
        result += sum([len(r) - i for i, c in enumerate(sections) if c == "O"])

    print(result)


rev_iters = [2, 3]

def score_grid(s):
    lines = s
    if isinstance(s, str):
        lines = s.split("\n")
    h = len(lines)
    sum = 0
    for i, l in enumerate(lines):
        assert len(l) == h
        sum += len([0 for c in l if c == 'O']) * (h - i)
    return sum

class Line:
    def __init__(self, pos, line):
        self.end_lines = [None for _ in line]
        self.count = len([0 for c in line if c == "O"])
        self.pos = pos[1]
        self.line_idx = pos[0]
        self.len = len(line)

    def init(self, pos, l):
        self.end_lines[pos - self.pos] = l

    def process(self, iter):
        if not self.len:
            return
        slice = self.end_lines[:self.count]
        if iter % 4 in rev_iters and self.count:
            slice = self.end_lines[-self.count:]
        # print(self, (self.line_idx, self.pos), "has", self.count)
        for l in slice:
            l.count += 1
            # print((self.line_idx, self.pos), "Incremented", (l.line_idx, l.pos), 'to', l.count)
        self.count = 0
        return slice

    def score(self, w):
        return sum([w - (self.pos + i) for i in range(self.count)])

    def __repr__(self):
        return "O" * self.count + "." * (self.len - self.count)


def build_lines(grid):
    grid_lines = []
    lines = []
    for i, r in enumerate(grid):
        count = 0
        grid_lines.append([])
        for split in re.split(r'(#)', "".join(r)):
            if split == '#':
                grid_lines[-1] += [None]
            else:
                l = Line((i, count), split)
                lines.append(l)
                grid_lines[-1] += [l for _ in split]
            count += len(split)
    return grid_lines, lines


def print_grid(lines, iter, trans, w):
    last_line = -1
    print('======{}======='.format(iter))
    s = []
    score = 0
    for l in lines:
        if l.line_idx != last_line:
            s.append("")
        elif l.line_idx == last_line:
            s[-1] += '#'
        if iter % 4 not in rev_iters:
            s[-1] += str(l)
        else:
            s[-1] += "".join(reversed(str(l)))
        last_line = l.line_idx
        score += l.score(w)

    if trans:
        s = ["".join([s[y][x] for y in range(len(s))]) for x in range(len(s[0]))]

    fscore = score_grid(s)
    print("\n".join(s))

    print(fscore,score)
    print('===============')


def part2(lines):
    grid = lines
    print(grid)

    w = len(grid[0])
    h = len(grid)

    trans_grid = [[grid[y][x] for y in range(h)] for x in range(w)]

    horizontal_lines, all_hor_lines = build_lines(grid)
    vertical_lines, all_ver_lines = build_lines(trans_grid)

    print_grid(all_ver_lines, 0, True, w)

    ver_toprocess = set()
    hor_toprocess = set()
    for x in range(w):
        for y in range(h):
            hor = horizontal_lines[y][x]
            ver = vertical_lines[x][y]
            # print(hor, ver, (x, y))
            if hor:
                assert ver
                ver_toprocess.add(ver)
                hor.init(x, ver)
                ver.init(y, hor)

    for hor in all_hor_lines:
        hor.count = 0  # Starts zero since we start vertical

    cycles = 1000000000

    seen = dict()
    #cycles = 2
    i = 0
    cycles = cycles * 2
    while i < cycles:
        if i % 10000 < 2:
            print(i)
        iter = i * 2

        hor_toprocess.clear()
        for l in ver_toprocess:
            hor_toprocess.update(l.process(iter))

        num = i % 2
        for l in all_hor_lines:
            num *= l.len+1
            num += l.count

        if seen is not None and num in seen:
            last_iter = seen[num]
            assert last_iter % 2 == i % 2
            print("Seen before at index", last_iter, 'again at', i)
            print_grid(all_hor_lines, iter + 1, False, w)

            cycle_len = i - last_iter
            remaining_iter = cycles - i
            remaining_cycles = remaining_iter // cycle_len
            i += remaining_cycles * cycle_len
            iter = i * 2
            seen = None
        elif seen is not None:
            seen[num] = i

        #if i % 10000 < 2 or iter + 1 >= cycles - 10:
        print_grid(all_hor_lines, iter + 1, False, w)

        ver_toprocess.clear()
        for l in hor_toprocess:
            ver_toprocess.update(l.process(iter + 1))
        #if i % 10000 < 2 or iter + 2 >= cycles - 10:
        print_grid(all_ver_lines, iter + 2, True, w)

        i += 1


import sys

def main(input):
    part2(input.strip().split("\n"))


input = """
#.O
O.#
.O.
"""
#main(input)
#exit(0)

input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
main(input)
#exit(0)

input = """
.#..#..O..O.....#O..O#O.O#.#.##O........#O..O...O#.O.O....##..#O..#..O.O#.O..#.O#O.#.#...#...#....O.
#.O#.##..O.OO#..OO..O...O...#.O..#O...#..O...OO#....O...O#O...OO..##...O.O.O.....OO..#......O..##...
..........O..O.OO...O.O....O...O..O..#O#O.O.#........O..O.O.O..O##.#O...O#...O..O....#...OO.#O..#.#.
..O.O..O.O#....O...O#.....O.....##O..O#.O...O......#O#...OO...##O....O.O#OO#.....O##.....#O.OO....#O
OOO...O....##...#OO.O.O.#OO.O#O.O.O..O.OO.##.O...O.........O...#.#O.......O#...O###.#...#O.#.....#..
O..#..#......O...OO..#....#..O...O#.#...O#...#.##...#.#....O..O#.......O.......O..O.O......##..O....
.....###..O#........OOO.#...#O.O#O..OO...O#...O..................#....O..##.#.O.O.#.#O...#.##.O...##
OOOO......#O..O.#...O..O..O...#....#..O.#O..OOO.##....#.O......#.#.#O.O.O.#.O##.OOOO.O.#O.#O###..O.#
#.....O#..O...O..O.O..#...O..#..#..#.....#..O.#OO...#.O.....#..O.....O.O.#O#......#.O.O#...#.O..#...
O....O....O....OO.O...#......O.O.#O........O#.....#...........O.#.O.##.....O......#..#....O.....#...
.........O##.###....#......#....#O.O..#...O.O.....O..OO.O...O.OO..#.O.#OO..#.#...O.##.OO..#.OO.O....
......O###....O.#..O..OO#O.......#.......#O..#...O.O......O...O.....###.#O..#O.O...#O.#OO...##O..O.#
....#O#.....O...O........#.##O.O..O....#.....O.O#...#.##....##.....O.O.#.O..O#.O..O#...........O.OO.
#.O......#.##...OO...#.#.....#.###.OO..##O##.O.#.....O#..OOO...O.#O#..O...#..#....##......##.OO..O..
OOO.##OOOO#.........O.#OOOO...O....OO#O##.O......#.........#.O..#....O..#....#..#....#..#.O....#..OO
.#O......O#...........O.O....#.O....#...##..O......#.O..#..OOO.#....#...#O.....O....#OO..#.#O..O....
...#.....##..O..##...##...O#OO.O..O#..O##..O.....#O#..O...O#...O..##OO...OO#..O...#.O#...##....O.O#O
.......#.....O...#O..OO.O#O.....O.......O#.O...O.O#...O.#...O...O......O.O.##........#...#.##..O....
#O....O.O...#.OO....O#.O........O.....#....OO..#O#..O.O#.#.O.##OO...O.#..O......O#.#..O.###.....OO..
....O..OO.O..O..O#.........O..O...O.#..#....O.O.#.#O....O....O#.#......O..#.#..#.#..O.#.##.##O.O#.#O
O......O#.O.....O.#....O......OO....O.#O.O....#...O#.........O..O.O.O..........O....#.....O#...O.OO#
#OO...O...O...O.......##..O..##O..##......O...O...#O.O.OOO..O........#..##.OO.O.#.......O..#..O...OO
...#.#.O#OO.O.#...#.OO.....OO..#.O..#.OO......OO..........OO..O#...........O.#.#O.....#.O..O#..##...
..O..O..##.OO...O...O.#......O.#....#.O#..OOOO#.##.O......#.O...O.OO....OOOOO.........#.O.O....O..#.
.##.#...O#...OO.#.......#.##.O.......O.O.#.#O#..O#O#...O...#.O.............O......OO...O.......OO.##
...OO..#.O..O.#...O...........O##OOO...O.O##...O.#...O....#..O.O.OO....##O#.#O...#O.#...OO#.##.#.OO.
#...#......#.OO..#.#.O.O.....O..O..O#..#.....O.#..#.#.O.#O.#OO......OO.....O.##OO.#...OOOO#OO.....O.
.....###O##.##.......##O.##.O...#..OO....OO.O.........O#.....OOOO....#OO#...#O.OOO..O#....O.......#.
........#O.O..#O#O#O..OOO....O.....O.#..#.......O.....#....O.....#.O##..O#....OO.#..O#.O........#...
.#O...#..#.......#...O..O.O.#OO..#.O.#O#....O.#O..#....#..OO.#OOO.O#.O.#...O.O..O....#.#.O.......#..
O.......##.O#...OO.O#O.O.O....O#.....O...O..#.....#O..O..#.#O.##....O...#O...##..O....O...#OO.#.O...
.O.#..O.OO.O##..OO.##.#O#O..OO..O..........OO...O###..............O.....#.##...O.....#.OO.O#..O#O...
O.#....O.#.##..#...O....#...#.OO.#.##.#...#.#O.#.##O.....##O.O....O..O..O##.......O#...O##.......OO.
...#......#OO.........#..OO.O.O........#..O...O.O....O#O..OO#...#..#O..#.#OO....O.#..O.O.........O.O
...O...O..O#.#O#O#O#O.#..##..##.OO##........O.O......##.O.O.#..#.....O#O#..O.O.#....OO...#.O...O#O.O
##....#.....O.......#OOOOO..O....#...#........#....O.#....#.#..#.O##.##....O...#.#O...O...O..O......
..OO..O...O#.O#..#....##...#........###.O.OO...##.......#..#....O..O..O.#OOO..#..#O........O..OO...O
..#...#..........O..O.###..OO..O.O....#..#.OO#....#.#...O#..O..O..OO##....O.#...#.#...#..#.#......O.
..OO..#.O.........O#.O.OO.O..O.O#.OOO..O..#.#.O#....O#.OO..O#..##.#..#O#..#..O.#.O#...O...O..#O....O
..O#..O..O#O...#..#.OO.....#....OOOO.....O...O..OO.O.#.O...#OO.O##O..O#....##.OO#.......O.#....#.#..
......O.#......#....OO.#.O...#OO.#O..#....O#.O.OOOO..OO.O....##O.#....O#..OO#.OO#O##..O.#........O..
.O...........#O...O..O#..#..O.O..#O#.#..O..OO..O.O.#O...#..OOO.#...OO.....O........O...##..#...O...#
......#O...O...#O.O...O..#OO....O..O.#OO..O....O#..#OO...#.#.#.##OOO.O.#OO..OO#........#.##.O..#....
OOO.O..O.O....O.....O##.......#OO...#O.......O..#O....O....OO..O.#.........O.O.OO.....O#.........OO#
.#.OO......O...#.#..O....O...O...............O..O...O.OO....O.#O....#........#...#.#......O......O..
#.......#O.#...###....O.O....#.###.OO..#OO....#....O.....#O.OO##OO..O.O....#O..#......#..#O#...#.O..
OOOO..#...##O........#....OO.....O.O##..#O..OO..O#.##O..O#...#.OOOO##...........#.#O...#.O#.O....O.O
O#..O#..#.O..#.O.OO.O#O.O..#......O.#...O#O#..O..OO.#..O.OO#..OOO............O.....OOO#.O###.....##.
O....##.........O.O.O.O..OOO...O..O.O....O......#..........#...#.....#..#..#.....#.###..#...O#......
OOOO...#O##.O.O#...#.#..OO.O#...#O.O.....#....OOO....#..#O..##.....OO...O..OO#...O..OOO...#.O.O...OO
..#O#...O......O##..OO#..#O#..#O#.O...#.###.O.O....O.....#..OO.O...O.#.......#..#.#.#.....#O..O.O...
..#....O.O.......OO..O#..OOOO..#.........#OO......O..O...O..O.###.......#O#...#.O..OOO.......O#.#.#.
.O.O..#........OOO.O.##..#.O...O.O.OO..#..O#O.##.OOO#.OO...#....OO#O#.......O##.....O....#OOO.O...O.
#....O.......#..#OO.#.#.O....#..#.#...O..O.O..O....OOO....#.O.#OOOO.#.......#.#.OO...OOO....#..#....
.OO.O.O......O#.O....#......#O..##.....O.#..##..O...O.O...OO..OO..#..O..O....#......O.O.......#O.#.O
....O.#..O....O#.OOO.O..#....O..O...#.OO........O.#OO#O#.##..O..O##.O#...O......O....#O#..#...#O.#..
#.....#..O#..O..OOO..O.#....#.......OO.O##.#......OO.....OO....O.O...#.#.O#...OO.......OO....#.....#
....O.OO#....#O#..O..#O.....#..O...O...O.##...O....#.....#.O....O##O..O#O.....O..##...O....O.O#.....
..O.#.#..OO......#..#.#.#.#.....O..#O..O.........O#...O##.#.....#O.O..O....#.##O.#O..OO...##....#..O
O......#............#.....##O..O..OO.....##..O..O.......O.......#OO...#O.....O.O.O.......OOO.O.#OOO.
O..OO.#....#...O..O...##..OO...O........OO....O..........#OO.....#..#O...O#.#....#O..O#..#.O......O.
..O#.##O..O.#..#.......O...#...O..O.#O....#.#....#O#.O..#O...O..#OO.O#O.....O....#.....#..O.......#.
.O.O..OO.O...O.#O....OOO..O.O................O..##......OO.O.......OO.O................#.O....OOO#O.
......O.O.#O#...O#..#.........#O#.#O......O...#O....#.#O..O...O..#...O.O.#OO.O...#.........OO..OO...
.#.O..O...#O.##.O.......##....O...##.......OOO..O...#.O#.......#...OO#.#.#......#O..#OO..O...OO...O.
.O....O........#O.#..#.#...##.#..........O..O.#..#..#.##..#.#.#.#..#......O#........OO.....OO.#..#..
#O..O.#....O.#..OO#......#.#.O.O..O.##.#.....#O..OO..O......O#...O#..O..O.....OO.#........O......#..
O.#....O..#....O.O.OO#O..#...O##..OO#......O.#....O...#.O....##..O.O#OO..O......O.O.......#...O.O.#.
..O......O..OO.OOO.....#...O...#..#.#...OOO.O.#O...O.#O.....OO.O.....O.O#.O.O..##..............OO...
...OO#....O....#.......OOOO....#OO.O.O.O##.#.O..O.O......#.............#......O.O....#O##O.#.O.#O...
.#..O..#..#O...##O..O#O...#..O#...#.O.........O..O.O......O##O.#O.....O.O..##.#.........#.......O...
.O.OOOO.#...##.O#O#.#..#...#..OO..O##..##..OO.#...#...#....O..#O#.#...OO..O..O..#O..#.#OO.O#..O.O.##
..O...#....O#........O......OO.......O..##.O...O...#O..O.....#...O#...O.O#.#.O.#.#OO.##.....O..O..O.
.......#.O...O....O.O..#O.O..#O.#....##...................O#OO.....#....OO...O...##.#.O..#O#..#.O#..
.OO.#...##....#O#.........OOOO.OO.#.#.O.#....#......O.O.O#..###.O#..#..##....OO.#..#....#.#.....O#..
O.O...O..#....O.#......O##..#.O..#OO#O..........#O.OOO.......O......#OO#.....#..O#.#...##O..O.O.O...
.....O.....#O###..........O...O...#O.O.#.O.....O..O...O...#O...##...O#.#...OO.........O...#.##O....#
#OO.OO..##..O.O..OO.OO.O#.##.O.O..O##OO..#...#.O...OO.#.#...OO#.OO.....OO...##O..O...O....#.O...O##O
#.O...O.#O.##O..##.#.#O.#OO.O.O.O.#..............#...#.O...#.O..#O..O.O.O.#.O..OO#..O#..#..O..#.#...
.OO.#.O.O.O....O##O..O...O..O.##....#....#.......O...O.OO..#...#.O..#O....O......OO#O........##.O...
..#.......#.....##O.###..OO.#....O.O.#..#.O.#O#O##..##.....#.#.........#...O........#..#..#...#O..#.
..O#OO.#.OO#.OO...##..O..O.O.O......O.....#.....#O#.#.#O.#......#...O.....#O..O.#O...#.OOOO.OO......
....#...#......O#.......#......#O....O.O#O......O..O...O..##..OOO.O.#..#.O.OO..#.#..#...O.#......O..
O..O....O#....O...##O...#O##.#.....O..#.....#.#......#......O.....#.#.#..O.OO#..O...OO..OOOO.O......
.O....O..O...OO....O.....O#.......O........O....O....O.......O..O..#..OO..#O...#......##.#....O..OO#
.....#..OO.O.#.....O.O.O#O.#O#..O.O..O...#.#.O.O...#....O..#..#...##OO..#.#..#O.O...#.O#O......O.#..
O..##.#.O..#.O#.#O....#O.##..#O.#....O...OOO.O......O....#.O..##..#.O...#........#.#..O..OO.O..###..
....#O...O.O......#..O.O..........#.#OO.O#..#O..OO...#.O.O.#.#O...O..#...#..O#.O.OO..O........#OO...
..#...O......O.##...#O.#.O...O#O..O..O......O#.......#...#O...O#.#.#........#.....O##O.#..#O#..OO..#
#O#O#.O#..#.O...OO..........##.O#.....#.O...O.....O....O#OO..#O..O.....OO.#..#..O....#.O..O......O.#
OO#.#.#......#......###.#.........#..OO.O.O#.....O#O.#.O...O##.....#..##OO..OO#.###.O.O.......#.O.##
#.#O...#....#..#.......O......O..##....#..##..O...##O#..OO.....O..OOO.OO.O.#OO....O...#.......O..#..
.O.#O.....#.O......OO..O....###.#...O.O...#....#OO..........O#O....O.........O..##OO.O..#.#..O##.#..
.#..O..O.OOO.OOO.OO.O........##...OO#.O.O..O...O..O..#O.#.O.....OO...#....OO.#..O#.#.......#.O#....O
....O.O#.O#...OO...#..#.##.OOO.....O.O.O.....OO..OO..OOO.#.......O...O...#....#O...O#.O...O##.##.#..
##O#...O....O..OO.O..##OO.O#.O.....#.#.O.O.......O#...#..#.OO...#...#..OOO###.......#.O.....O.#O...O
#.O..#.O.....OO..OO.#....###.#.#O..OO..........#O...O.O....O..##O..#..O..O.#OO...#....#...##..#.....
#..O..###..#.O.........OO...#O........O..O..O...O......O....O...O...##.....O.......#.#...O#....O.O..
.#O...O#....#....#...O.#...#O..#...O#...O.OO......O..OOO..#..O.#.O..O..#O.......O####O#.OO#..O.O.O..
...#.#O#..#........O.#O....OO....O#..#.#.O..O....O....#.O#.#.#......O.#......O#..OO...##O.#O.....O#O
"""
main(input)
