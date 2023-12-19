def inbounds(pos, bounds):
    for p, b in zip(pos, bounds):
        if p < 0 or p >= b:
            return False
    return True


def next(grid, beam):
    pos, direction = beam
    c = grid[pos[0]][pos[1]]
    if c == '/':
        direction = (-direction[1], -direction[0])
    if c == '\\':
        direction = (direction[1], direction[0])
    if c == '|' and direction in [(0, 1), (0, -1)]:
        return [((pos[0]-1, pos[1]), (-1, 0)), ((pos[0]+1, pos[1]), (1, 0))]
    if c == '-' and direction in [(1, 0), (-1, 0)]:
        return [((pos[0], pos[1]-1), (0, -1)), ((pos[0], pos[1]+1), (0, 1))]
    pos = pos[0] + direction[0], pos[1] + direction[1]
    return [(pos, direction)]


def part1(lines):
    grid_bounds = (len(lines), len(lines[0]))

    stack = [((0, 0), (0, 1))]
    seen = {}
    while stack:
        top = stack.pop()
        if not inbounds(top[0], grid_bounds):
            continue
        if top[0] not in seen:
            seen[top[0]] = []

        if top[1] in seen[top[0]]:
            continue
        seen[top[0]] = [top[1]]

        stack.extend(next(lines, top))

    print(len(seen))


def part2(lines):
    grid_bounds = (len(lines), len(lines[0]))

    starts = [((x, 0), (0,1)) for x in range(grid_bounds[0])]
    starts += [((x, grid_bounds[1]-1), (0,-1)) for x in range(grid_bounds[0])]
    starts += [((0, y), (1, 0)) for y in range(grid_bounds[1])]
    starts += [((grid_bounds[0]-1, y), (-1, 0)) for y in range(grid_bounds[1])]

    maxlen = 0
    for start in starts:
        stack = [start]
        seen = {}
        while stack:
            top = stack.pop()
            if not inbounds(top[0], grid_bounds):
                continue
            if top[0] not in seen:
                seen[top[0]] = []

            if top[1] in seen[top[0]]:
                continue
            seen[top[0]] = [top[1]]

            stack.extend(next(lines, top))
        maxlen = max(maxlen, len(seen))

    print(maxlen)


def main(input):
    part2(input.strip().split('\n'))


input = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
main(input)

input = r"""
\...........-..../..........|..\..-....-......-...../........|......................./............-.\......|..
......-.........../............-......../...............................|...../.........-...........\.........
\...............-............\.............................................-......-...|....\..................
.........|...-.....-............../.....\.................................\.................|/..........-.....
......./....-..........\-...\.........../...........................-........./...........-..................|
....................\.....|.../.......\-...........\......../........|..../................-..........|\-.....
......./....|.../..........-...|../...|..../-..../...............\..|......./...............-.................
............-.........../..|.......................\..\.........\........|........\............\.......-......
...../.......|-..-||............\......................|.../...........-................-.....|..../../.......
....\........|.................|...-.................\.......||............|../....../\.......-...|...........
......\.....................................|.........-....-..|.|.../-../..........\..................../.....
..|.........................................\........./.....\......./...||........|.................|.\....|..
/|...../......../...\../.........\......-..........................\..-.......\......................|..-.....
............../.............\...................\..............|......./...........|..................\.......
./..-.-.../......\............................/.................\..........-../........\......................
.....|............................./....\.........\......\............-.--.............|..........|...|.......
............-................................................\..\..............|.....................\.-..\/..
..\.................../........................|...|........|....\...\......../..........|...............-....
.............../........................./\...............-...................../.........................-./.
...........................//...............|.............\-..................|...\..........|..-........\....
.../.........//.../.....././.....|........-....-..\.......-.|..............|............-...........-..\..\...
/.......................-...............|....../.../|-.............-../..../................|.........|..../-.
|............\..-\\.\..../-.....||...\......-......||.........|....\....-.........-..............-............
.........\....../.|......-....................................\./........./...........................\.\.....
...............\................................................./-..............|/.................-.........
......\.\.......\...|........./.................../..|.....|...-................./.-/.-.....\................-
.......\.................../.\........../.../......./......\.......-..../...\.......|........|..\...\....|..-.
..\.........\....................................-....../../../..\.........|.....\..........\................-
..........--........\....-...\/......../.../......|.\./..............................................-/.....\.
...................\.....-...\|......\.......\....|.............|...........|.................-...........|...
.../.........|.........-.....................|....-.................-....|..............................|.../|
............|................/....\.................................................\./..|.........../...../..
..|................/....................|/........-......................|........./\................\........
.-......|......./..|../..............................|..........|........\...............................-....
...../............|................|.../..-........-......\..........\..../..................../.-............
..../............|.........../.....-....\.............-....\..................|.........................-.....
....|.........-\..........|............-...............\.............--.-....................-........-..-....
...............-.-.........|............../...../|........\..\...........-...\.|..............................
......-../.........\...........................|................/........|........|/.........../....-.........
................./......\......................\\....|............/.-\....|....................|......|.......
|...............|.|-........\\................/.....................-.........-..-..../..--...................
.........\.....\....\..\....-.......|........|...............................|......../............\\...\.....
....|../...................|../.........../.............|........-............................../........../..
...\..................-..|...................|\.....|.........\....\./.\.../.........-....|...................
......\.\..........-....\.\/../........./..............|......\........./........\...../...../................
......../............-..../.-...\.|.|-...........|...-..-................................/....................
.........../..\...-.......|......./.......-.............-............-.............../\...............|\......
..|.......-......................\.\../.........|-/........|\-.../...-.-..-...............|-/........-././/...
......|...|............|................\|.........-.........../..../.....-.........../........\.......\......
.|\..|.......\.\..................\|........./......\/.|................./............\........|\......./....-
........\||....\/...-.........\...|....-..-.-.........................../.....|..........\..|.....\........./.
...............................-......|..............-.............\.........\.|........./....................
........-.........................-.................-.......-.\.........../..../.\.............|.....|/...--..
......|.............\-|..................-........./....../...............\....\....-................-........
..-........-../.\|...........\...................--.....-.....................................................
.../../.............../....|........./.\.....-...........\..../..........|.......-.......................\../.
...............\............-........../.-.............-.............|...........|................|./....|....
............-.....-...................-...................|.../.\.-......-.....-.\............/.............-\
.../.........../........................................\.......................................--............
..|.\..|.|\...-..\.............|.....\...........................|\...........\.........-......\....-...\.\...
....../......................|.......|.........-......\.....|..../.............................\...../-.......
..-..................\...\................/............./...............-....-./........./......|..........\|.
..|.....|..........|................\.\./.........../.............\./....\........--.-..-.../...\./-..........
........-.....-........\............-|..........................\...\../..-.....\...|.........................
..........|...-.............\..............|......./......../............./.-........................./..\....
............|........../..................-................-.......|...../...|/.......-.......................
.............\........|............../..-...-.-...\\..../..\.....-............./....-..../\......./.......-...
................-.....|.......................................|....................\................/.........
.....\......../..\-......\...-.....-............................-......./........\.-............/.............
.............................................-.................................../\.....|.....................
|................|.....|.||...\................/...\........-........../.............\....-./........-........
../.....................\..............-.............-................|................-/.....|......./.......
........|../........|......\......................../..\..|............|.....\......\.........../..|.\.../....
|/..../......-.............../....\../......................|..............|..........|................/.-...-
..../.......\.............../.\...........\.....-..........................|............\.....|...............
.....................................\....-..................\-.....................\.|....|...........\......
../.\..........|.....-......../......../|..........|................./.\................................../.-.
.............\....|.|........-....|......................\.....\....../..........--.......-./.\........./.....
........................................-..-\..|.........-\.\\.......\.................................\-..../
......../......-.....-....-........-..\..\.-....\....././............/..../.......|........../.--......../....
...-...-................/...................../../.-...............\./......-...|.|................./.........
.......|/............\\............/....\.....|.........\......-....../............./.....\.........-.........
..-................................/....................\......|............./...-........|.....-...../.......
.-...|......./....-............\..........-......\............-.....................|......|............\...\.
./............-.......................-.../...................|......../........\.-...........................
...............\................./.|......../.........|...........................|..................\........
.......................|.......|..../.....|......|.....-...........|.................|...............|........
...\../....../...|...........-...........-.....\..................-..............|..............\../....../...
.........|\/..-\....../.......................|...|../.........-...../.-..-...-........./...................-.
|........./-..|............./.....|........|.....\................-..|..-........................../......-...
.........................................-................\..................\............................-../
....|...........|../../........................\.........\.....-....................-....-...\./..............
....|.........|/..../|..............................-/...........-.........||.........|....-...............\..
........|-.......|............-\\........|............-.\............\...|..|................|................
............\.......-............../..........|.....................-.........-................./|............
.\................\..|.|......................\........\...........\................-..........-....../.....\.
\.........................|......|............|........-....\...../........|.............\....\............-..
./................\.../...................|..................-......//............./......\...................
.........\......../....\..................../-........................-...........|...-.......................
...........\....../......|...........................................\./.........\...|.......\.......|....-...
............/.......................|.....|...........|...........|......./|.........................\........
...............-........................../..................|...........................|/..\..........-.\.\.
......|../................-.../.............|..........|............../.\........--....|................././..
..../......|.../.............-...../........\.........\..../...-...........\...\....-......../..-...-.../|.|..
.........|.................|......................-................|...-..................................\...
............................./...............||./.\../...................\.............../................./..
./...................-.....................-............-.-//......-\............../..............\.\...|....-
...................-...............|...../.......-../......\..-.........|....../\....\.....\..................
|............/....\....-.......-......................-........................|...................../........
......../.-....\..........\............................-....-......................\..\.................-...\\
"""
main(input)