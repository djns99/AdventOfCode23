def part1(lines):
    count_row = [0 for _ in lines]
    count_col = [0 for _ in lines[0]]
    galaxies = []
    for row, l in enumerate(lines):
        for col, v in enumerate(l):
            inc = 0
            if v == '#':
                galaxies.append((row, col))
                inc = 1
            count_col[col] += inc
            count_row[row] += inc

    indices = [[(0,0) for _ in l] for l in lines]
    row = 0
    for r, l in enumerate(lines):
        col = 0
        for c, v in enumerate(l):
            indices[r][c] = (row, col)
            col += 1
            if count_col[c] == 0:
                col += 1

        row += 1
        if count_row[r] == 0:
            row += 1

    result = 0
    for i, (g1x, g1y) in enumerate(galaxies[:-1]):
        g1x, g1y = indices[g1x][g1y]
        for g2x, g2y in galaxies[i+1:]:
            g2x, g2y = indices[g2x][g2y]
            dist = abs(g1x-g2x) + abs(g1y-g2y)
            result += dist

    print(result)


def part2(lines):
    count_row = [0 for _ in lines]
    count_col = [0 for _ in lines[0]]
    galaxies = []
    for row, l in enumerate(lines):
        for col, v in enumerate(l):
            inc = 0
            if v == '#':
                galaxies.append((row, col))
                inc = 1
            count_col[col] += inc
            count_row[row] += inc

    indices = [[(0,0) for _ in l] for l in lines]
    row = 0
    expansion = 999999
    for r, l in enumerate(lines):
        col = 0
        for c, v in enumerate(l):
            indices[r][c] = (row, col)
            col += 1
            if count_col[c] == 0:
                col += expansion

        row += 1
        if count_row[r] == 0:
            row += expansion

    result = 0
    for i, (g1x, g1y) in enumerate(galaxies[:-1]):
        g1x, g1y = indices[g1x][g1y]
        for g2x, g2y in galaxies[i+1:]:
            g2x, g2y = indices[g2x][g2y]
            dist = abs(g1x-g2x) + abs(g1y-g2y)
            result += dist

    print(result)


def main(input):
    part1(input.strip().split('\n'))
    part2(input.strip().split('\n'))


input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
main(input)
input = """
.....................#......#...................#...............#........................................#..................................
...........................................................#.............................................................#..................
.....................................................................#.........#......#...........#.............#...........................
.....................................................#.......................................#..............................................
......#.................................#..........................................................................................#........
....................#.........#.............................................................................#...............................
..#.........................................................#.............................................................................#.
........................................................................................#...........#..................#....................
........#....................................#........................#.........................................................#...........
..............................................................................#................................#............................
..................................................#............#............................................................................
.........................#......#........#................................................#..........................................#......
......#..............................................................................#...............#......................................
...................................................................#........................................................................
....................#...........................#............................................................#..............#.....#.........
..................................#....................#.........................................#......#..............................#....
.#..........................................................................................................................................
........#.....#........................#...........#.............#.....................#....................................................
..........................#.................................#.....................#.........................................................
.............................................................................................................................#.............#
...................................#......................................................#....................#............................
.....................#...................#............#..................#.............................................#...........#........
..............................................................................................#.............................................
....#..........#...............#..........................................................................#.................................
.............................................#..............................................................................................
...................................................................#..............#.................................#.......................
..................#........................................................#................................................................
..#.................................#...................#..............................#.........................................#.......#..
...............................................................#...............#.....................#..........#.........#.................
.........#......................#.............................................................#.............................................
..............#...............................#.............................................................................................
........................................#.................................#............................................................#....
..............................................................................................................#......#......#...............
.........................#..........#.............................................#........#................................................
....................................................................#.....................................#.................................
....#...............#........#...............................#........................#........................................#............
........................................................#...................................................................................
............................................#...........................#......................#.....#......................................
.........................................................................................#.............................................#....
...........#....................#..................................#.................................................#...........#..........
.#..........................................................................................................................................
................#........................#..........#.......................................................................................
........................#........................................................................................#..........................
........................................................................#.........#...................#...................#.................
........................................................#......................................................................#............
.....#.....................................................................................#................................................
...............#...................................#.................#..............................................................#.......
.........#..................#..................................#..................................................#.........................
......................................#.......#....................................#......................................................#.
..........................................................................................................#......................#..........
...#..............#.......................#.....................................................#...........................................
................................#...............................................#..........#................................................
..........................#......................#......................#...................................................................
..................................................................#................................#........................................
......................................................#.................................#.........................#...................#.....
..............#..........................#..................................................................................#...............
......#......................#.................................................................#...........#................................
.............................................................................#..............................................................
.......................#..........................#......................................................................#..........#.......
.#.................................#................................................................#....................................#..
........#......#................................................#...............................................#...........................
..........................................................................#.....#.........................#...........#.....#...............
............................#..............#..........#....................................#................................................
............................................................................................................................................
............#..........#....................................................................................................................
............................................................#.......................#..............#........................................
.....................................#...............................#...................................#..................................
.........#.....................................................................#.....................................#...............#.....#
#.............#.............................................................................................................................
......................................................#....................................#....................................#...........
...................................................................#............................................#...........................
............................................................................................................................................
....................#............................#................................................#......................................#..
.............................#...................................................#..........................................................
.........................................................................#...............#.................#................................
.............#.........#.........#.....#......................#............................................................#................
............................................................................................................................................
.............................................#..........#.....................#..................................#..........................
............................................................................................................................................
...................................#.............#................#.....#.....................................................#.............
....#.....................#..................................#..............................................................................
............................................................................................................................................
#.....................................#...................................................................................#.................
...............................................#......................#.....#...................................#...........................
.........#...................#.....................................................#.................#......................................
.......................#...............................#........................................#..............................#............
...#.....................................#..................................................................#...............................
...................................................#......................................#...........................................#.....
.................#..........................................................................................................................
...................................................................................................................#......#.................
.................................#..............#.....#......................#.................#.........#..................................
#....................................................................#........................................#...........................#.
............................................................................................................................................
.........................#..................................................................................................................
...............................#.......................................................................................#....................
..........#...................................#..................#.....................#....................#...............................
............................................................................#.....#.........................................................
....#............#............................................................................#.......#..........#..........................
..................................................................................................................................#.........
...................................#...........................................#............................................................
.............................#..........................#.................................#........#........................................
..............#....................................................#........................................#.............#...........#.....
...............................................#.............#.......................................................#......................
........#..............................................................#....................................................................
.......................................................................................#........#...........................................
......................#........#.........................#..................#........................#......................#...............
.#.........#.....#..............................................#........................................................................#..
.....................................................#......................................................................................
.........................................#...........................#..............................................#.......................
.............................................................#................................................#................#............
......#.......................................#.......................................#...............#.....................................
....................#.......#............................#................#...........................................................#.....
...........#.....................................................................................................#..........................
..........................................................................................#..............#..................................
..................................................#..........................................................................#..............
...............#............................................#.....................................................................#.........
........................#...........................................#............................#..................#.......................
................................................................................#..............................#.......................#....
......................................#...................................#..............#..............#...................................
..#............................................#..............#...........................................................#.................
.........#........................#...................#.....................................................................................
.............................#..............................................................................................................
....................................................................................#.......................................................
.........................#.............#............................................................#......#......#.........#......#........
...................#...........................................................................#...........................................#
.......#...............................................#.....#........#..........#..........................................................
..............#....................#........................................................................................................
........................................................................................................#.................#...........#.....
..#...............................................................#.........#.......#.......................................................
.........#......................#..........................#.....................................#............#.............................
...................#.................................#.................................................................#....................
....................................#.......................................................................................................
...........................#......................................................................................................#.........
............................................#.................#............#...................#.......#...................#................
............#.....................................#.........................................................................................
...........................................................................................................#......#.........................
.....................................#..............................................#......#................................................
.........................................................................#..............................................#...................
#....................#........#...................................................................#.....................................#...
.....#........................................#.........#........................#..........................................................
"""
main(input)
