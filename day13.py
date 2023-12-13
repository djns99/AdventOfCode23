def find_reflect_column(grid, num_failure):
    #print(grid)
    w = len(grid[0])
    for col in range(1, w):
        failure = 0
        for line in grid:
            col_s = col - min(col, w-col)
            col_e = col + min(col, w-col)
            first = line[col_s:col]
            second = reversed(line[col:col_e])
            for x, y in zip(first, second):
                if x != y:
                    failure += 1
            if failure > 1:
                break
        if failure == num_failure:
            return col


    return -1

def doloop(grids, numfailure):
    result = 0
    for g in grids:
        grid = g.split('\n')
        grid = list(map(list, grid))
        w = len(grid[0])
        h = len(grid)

        col = find_reflect_column(grid, numfailure)

        if col != -1:
            result += col
            continue

        trans_grid = [[grid[y][x] for y in range(h)] for x in range(w)]
        row = find_reflect_column(trans_grid, numfailure)

        assert row != -1, "Failed on grid\n" + str(g)
        result += 100 * row

    print(result)


def part1(grids):
    doloop(grids, 0)

def part2(grids):
    doloop(grids, 1)


def main(input):
    part1(input.strip().split("\n\n"))
    part2(input.strip().split("\n\n"))


input = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
main(input)

input = """
##.##......
##.########
...#...##..
..#.#......
###..#....#
###.#......
##..##.##.#
..#...####.
..##..####.
#####.#..#.
###.##.##.#
....#######
#.#........

#..###......#
..#.#........
#.#####....##
..##.#..##..#
.###.#..##..#
#.#####....##
..#.#........
#..###......#
##...#..##..#
#.###..#..#..
.##...##..##.
###.#########
#..#.#.#..#.#
.##.##......#
#..#####..###

.##.....##.
####.#..#.#
#####......
.......#.##
.##..######
#..#.....##
#####..####
.##.....#..
....###....
....###....
.##....##..

.##.###.###...#
....#.##....###
####.###...###.
#..#.##....##..
.....#######.#.
.##.###.....#..
#..#.#....####.
####.##.#..##..
.......#.#####.
.##.......#...#
.....##..#.#.##
.....##..#.#.##
.##.......#...#
.......#.#####.
####.####..##..
#..#.#....####.
.##.###.....#..

#..####..#....#
..##..##..####.
....##.....##..
...#..#........
#.##..##.#.##.#
.##.##.##.####.
.##.##.##......
#......#.######
.#..##..#......

.#..#.#...#....
#.##.#.#.#.....
#....#.##......
#....#.##......
#.##.#.#.#.....
.#..#.#.#.#....
.#..#...###....
.#..#.##.#..##.
########.#.#.#.
#....##.##...#.
.......###.####
......#####.###
.#..#.#.#.###..
##..###..#.#..#
##..##..##.#.##
#########.#.###
#.##.##.###..##

..###.#
####..#
##..##.
##..##.
...#..#
...####
..#.##.
##.####
##.####
####..#
...#..#
##.#..#
..#####
##.####
..#.##.
..#####
....##.

.#.##.##....##.
...#...######..
#....##########
..#.#....##....
#..###.######.#
#..###.######.#
..#.#....##....
#....##########
...#...######..
.#.##.##....##.
.#####..####..#
#......######..
.....##.#..#.#.
.#...###....###
..##..#......#.
##..###.#..#.##
.#.#.#........#

#..#####.##.#..
.#..##.#.####..
...##..##.#..##
.######.#.#.#..
#.#..###.....##
....##..#....##
..##.#.#.#.#.##
##..#...#..##..
#...###..##.###
.###..#.#.#..##
..#.###.##..###
###.#.#####....
#.#.#.#####....
..#.###.##..###
.###..#.#.#..##

#..###.
.....##
#..#..#
#..#..#
.....##
#.####.
#.####.
.....##
#..#..#
#..#..#
.....##
#..###.
.#.#.##

##.#..#####.#
##.#..#####.#
#......#.#..#
##..##......#
..###....#.#.
...###.#.#.##
#.#.##..##.##
#.#.#...##.##
...###.#.#.##

##.#.........
.#.##...#####
#...#####.#..
.....##.#.#..
#.#.#.###..##
#....##...#..
#....##.#.#..

##.##.##.##.##.
..##.###....###
###.#.###..###.
###.##..####..#
..#####.####.##
##....###..###.
..###..#.##.#..
..##....#..#...
...##....##....
###.####.##.###
###.##...#....#
##..#..##..##..
...#..########.
...#.#.######.#
##.#...######..
..#..##......##
..#.####.##.###

.###..#######
..#..########
..###.#....#.
#......#..#..
###..#.#..#.#
#..#.########
##.####....##
##.#..#.##.#.
.#...###..###
#.##..##..##.
.....##.##.##
...##..#..#..
...##..#..#..
.....##.##.##
#.##..##..##.
.#...###..###
##.#..#.##.#.

..###..##
.#.##..##
##.######
.#.......
.#.#....#
##.######
.#.##..##

#..#.###.
#..#.#.#.
.##.#.##.
.#..#.#..
...#.####
...#.####
.#..#.#..

.#..#####.....#
..########...#.
###.#.###.#.#.#
#.###.#..#...#.
#.###.#..#...#.
###.#.###.#.#.#
...#######...#.
.#..#####.....#
..###...##.#.##
###..###...##..
##...#####..#..
....#####.#...#
....#####.#...#
##...#####..#..
###..###...##..

###....#.
###..#...
###...#..
###...#..
###..#...
##.....#.
.########
#..#.#.##
#..#.#.##

##.##.#....
##..#.#....
.#.#.###...
....#..####
..##..###..
#..##.##.##
#######..##
#..######..
.#.#.#.#...

##########.##..
.............#.
.#....#.##..###
##.##.##.##.#.#
############.##
.........####.#
#..##..###.##.#
#..##..##..##.#
.........####.#

.##.#....
.....#.##
...###..#
###..###.
...#.##..
...#.##..
###..###.
...###..#
.....#.##
.##.#....
#...#....
#...#....
###.#....

##.####
###.#.#
...#.#.
###..##
###...#
##.#..#
....###
...#..#
...#..#
....###
###..##
#.###.#
####..#
##.#..#
##.#..#

...#.###...#.#.
#.#...#.#.#....
..#..##.#.#....
.....#####.#..#
.#....###.#.###
#...#####.####.
###...#.##.#.#.
##.#..####..#..
##.#..####..#.#
..#..#..####.##
###.####.##.##.
....###.##.#..#
....###.##.#..#
###.####.##.##.
..#..#..####.##
##.#..####..#.#
##.#..####..#..

..##..###..#.##
..###.##.####.#
..###.##.####.#
..##..###..#.##
#.##...#.##.#.#
#..#..#.##.##..
##.#.###....##.
..#....###.##..
#######..####..
#.###...#...#..
#.####..#...#..

....#.##.#.##.#
.##...##.#....#
####...###.##.#
.##...#........
.....##...####.
#..#..#.##....#
.##....####..##
####...###....#
.##.####.##..##
#..###...#.##.#
.###.###..#..#.
....#.#########
.##.#.####.##.#
.##.##..###..##
#..#.##..##..##

.#..#..#.....
.###.##.###..
.###....###..
....####.....
#.#..##..#.##
####.##.#####
##.#.##.#.###
....####.....
..##....##...
##.##..##.###
##.######.###
..#..##..#...
.##.####.##..

..##..#..####..#.
##..##..#....#..#
#.##.#..##..##..#
##..####......###
#....##.#.##.#.##
######..#.##.#..#
..##.........#...
#....#..#....#..#
#.##.#.########.#
..##...#.#..#.#..
.####.#........#.
#.##.##..#..#..##
#....#..######..#
######.#.#..#.#.#
.#..#..########..

....####...
..#......#.
...#....#..
##...##...#
##...##...#
##..#..#..#
...##..###.
##..#..#..#
.....##....

####....####.
..#.#..#.#..#
#..#....#..##
.#.#....#.###
.#.######.#.#
#####..#####.
...#....#...#
###......####
###......####

#.##.##
#.##.##
####..#
#.#..#.
###.###
.#...##
.##..##
###.###
#.#..#.

.#.#....#.#..
##.#....#.###
##.#....#.###
.#.#....#.#..
..########..#
#.##.##.##.##
.##...#..##..
#.#......#.##
..##....##..#

###..#####.
.#.####.###
.####...###
.####...###
.#.##.#.###
###..#####.
..#.######.
.#.#..#...#
.##.#.##..#
.##.#.##..#
.#.#..#...#
..#.######.
###..#####.

##..#.##.#..#
..#.#....#.#.
#..#..##..#..
#..#..##..#..
#.#.#....#.#.
##..#.##.#..#
..#..#..#..#.
#.#.##..##.#.
##...####...#
...#.#..#.#..
..#.######.#.
##...####...#
.##...##...##

####...#..#..#..#
##.#.####.#..#.##
.#.#.#..##....##.
.##..#.##########
.#.##.#...####...
###.###...####...
.#.#.#.##.####.##
#.##....###..###.
..##...##.#..#.##
..#........##....
...#..#..##..##..
...#..#..##..##..
#.#........##....

#.###...###
....##.#..#
.###.##.##.
.#.###..##.
..####.....
..####.....
.#.###..##.
.###.##.##.
....##.#..#
#.###...###
...#.....##
...#.....##
#.###...###
....#..#..#
.###.##.##.
.#.###..##.
..####.....

.##...##.
....#....
#.####..#
.#..#....
###.#....
#.####..#
.#.##....
####.#..#
.#..#####
###..####
###..####
.#..#####
.###.#..#

####...
...####
#.#....
#.###..
##.....
##..###
##..###
#......
#.###..
#.#....
...####

##..#.#..#.
....###.#..
.########.#
#.####...##
.#.#..#.#.#
#..####.#..
#..####.#.#
.#.#..#.#.#
#.####...##
.########.#
....###.#..
##..#.#..#.
####.......
#.##.##..##
#.##.##..##

.###.##..#.#.####
##.#...###..#####
..#..###.#.#.....
..#.#..#..##.....
..#...####.##.#..
##....##.#.......
##.####.#.#####..
.#.#.##.#.##.#.##
#.##.##..##..####
..###..#.##.###..
.#.###.######.#..
..#...###.##.##..
..#...###.##.##..
.#.###.######.#..
..###..#.##.###..
#.##.##..##...###
.#.#.##.#.##.#.##

#.##.#.#.##....
#.##.#.#.##....
######.####.#..
#######......#.
##########.#..#
.#..#...#...##.
..##.....##..#.
.##.#.##.....##
.#..#...#..#...
.####......##.#
.####.#.###...#
##..###.#......
######...#..#.#

.##....##...#
###########.#
.##....##..#.
####..####.#.
....##......#
..#....#..#..
#..####..#.##

.#..######..#.##.
#.##..##..##.####
.##..####..##....
.####.##.####.##.
###.#.##.#.###..#
..##..##..##..##.
##.##....##.##..#
#.#.#....#.#.#..#
..###.##.###.....
.....#..#..#.....
..##..##..##..##.
..###.##.###..##.
...#......#......

##.#.##.....#.###
.#..##...#.#...#.
#..##.####...###.
..###.###...##..#
.#..########..#.#
##.#.##.##.##.##.
..##..###.###.###
...#..#......#..#
.###...#######..#
.###...#######..#
...#..#......#...
..#######.#.#####
..#######.#.#####
...#..#......#...
.###...#######..#
.###...#######..#
...#..#......#..#

###...#..#.
#.#........
###.#......
....#......
###........
...#..####.
..##.##..##
#####......
..#..#.##.#
..#..#.##.#
##.#...##..
..##.......
######....#
...##......
..#..######

.##.#.##..##.
###...##..##.
.##..#..##..#
.##.#........
#....#..##..#
#.#.##..##..#
.###.########
.#...........
.#.#.........
#.###########
...###..##..#
.####........
..###..#..#..
#..##########
##.#.........

..#.##..#
..#.##..#
##..##..#
..##.###.
####.#.##
#...#.#.#
..#....#.

...#....#....
...#....#....
...######...#
.##..##..##..
##........###
.#..#..#..#..
.....##...#.#
.##......##..
.#...##...#..
...#.##.#...#
##.#....#.##.
...##..##...#
####....#####
...#.##.#...#
#....##....##
#.###..###.##
#.#.#..#.#.#.

.####..#..#..##
#....#...#...#.
#....#.#.#...#.
.####..#..#..##
.####.##...#.#.
.####.##.####.#
#....####.#...#
.#..#...#..#...
.####...#.#.#..

......#..
#.###.#.#
#.###.#..
..#.##.##
#....#.##
.##...#..
...###...
#...#####
#.##.#.##
.#..###..
.#..###..
#.##.#.##
#...#####
...###...
.##...#..

##...........
..#.##.##.##.
####.#.##.#.#
..#..######..
###.########.
##.#..#..#..#
..###......##
##..#.####.#.
....#..##..#.
..#.##...###.
...#..####..#
#####......##
#######..####
######.##.###
###..#.##.#..

.##.##....##..##.
#.###.##.#..##..#
#.#####..........
####.##.##..##..#
..##.#.##.##..##.
.#.#..####.####.#
.##.#####........
#.#...#..#..##..#
..#.#.#..########

.#..###.#
..#.##.##
..#.##.##
.#..###.#
#.#.#####
#.#....##
#.##..###
.#..#....
..#......
.###..#..
.#.#..#..
..#......
.#..#....

##.........
...###..###
...##.##.##
#.##......#
#..##.##.##
##.##.##.##
#....#..#..
##.###..###
.#.........
##.########
.#.##.##.##
.#.##.##.##
##.###..###
.#.........
##.###..###
#....#..#..
##.##.##.##

##..#.#....#.##
.####..#.#.#..#
#..##.####.##.#
.#.....#..##..#
.##.#.#..###..#
.##.#.#..###..#
.#.....#..##...
#..##.####.##.#
.####..#.#.#..#
##..#.#....#.##
#.#..##...#.#.#
.#.#..##..#..#.
.#.#..##..#..#.

#.#..######
...###..##.
...###..##.
#.#..######
#.......#..
.#.##.#.##.
.....#.....

#.####.#.
#.####.#.
........#
########.
#.####.##
##....##.
##....###
#.#..#.#.
#.####.##
.#....#..
..#####..

#.#.#######..##..
.#.##..#####....#
.....#...###....#
..#.#######..##..
..#.#.#..###.##.#
..#.#.#..###.##.#
..#.#######..##..
.....#...###....#
.#.##..#.###....#
#.#.#######..##..
.##.###...##....#
#.#.###....#.##.#
#.###....##.#..#.
#....#######.##.#
#.#.#...##..####.
#....#....#......
..........#######

#..##..#.#..#.###
#.....####..#..##
#.....####..#..##
#..##..#.#..#.###
#.##....##....#..
.######..###...#.
#....##...##.#...
#....##...##.#...
.######..###...#.
#.##..#.##....#..
#..##..#.#..#.###

####.#.##
####.####
.##..#..#
#####.#.#
#..###.##
#####..#.
......#.#
#######.#
.##.#####

.##..##....#...
####.##.#..##.#
.##.#..#.#..#..
#..#..###..#.##
#..#..###..#.##
.##.#..#.#..#..
####.##.#..##.#
.##..##....#...
.##.####.##.#..
..##..#..#####.
..#.#..#.#..#..
..#.#..#.#..#..
..##..#..#####.
.##.####.##.#..
.##..##....#...
.###.##.#..##.#
.##.#..#.#..#..

#.#.####.
##.#.#.#.
##..#.#..
.###.##.#
####.#.#.
####.#.#.
.###.##.#
##..#.#..
##.#.#.#.
#.#.#.##.
#.#.#.##.

#.#....#.####
.##.#.#.#.##.
.#..#.#......
..##.###.####
..##.###.####
.#..#.#......
.##.#.#.#.##.
#.#....#.####
###....#.#...
.#.#...##.##.
.#.##.#..#..#
..#.#....####
.#..#.#.#....
....#####.##.
.#.#..##.####

...##.##.
..#.#####
..#.#####
...##.##.
#.......#
#..#.#.##
#.######.
.#....#.#
#.###..##
##.#.....
##.#.....
#.###..##
.#....#.#
#.######.
#..#.#.##
#.......#
.#.##.##.

..#########
.#.#.#....#
##.##..##..
.#.##..#...
.#.###.##.#
..##.##..##
.###.#.##.#
.###.##..##
.#..#.#..#.
.#....####.
.#.##..##..
###...#..#.
#..........
.###.......
.#.#.##..##
.#.#.##..##
.###.......

#..#.##.#..
....#..#...
.###.##.###
#.#.####.#.
#..#....#..
#..#....#..
#.#.####.#.
.###.##.###
....#..#...
#..#.##.#..
.#........#
#....##.#..
#.##....##.
#...#..#...
..###..###.
..#.#..#.#.
.##......##

....#..#...
####.......
#..#.#....#
.....#....#
#####......
####.######
.##.##....#

.#.#..#.#..
###.##.####
#..#..#..##
.##..#.##..
.#..##..#..
.##.##.##..
....##.....

#.####.#..#
#.#..#.#.##
#......##.#
###..####.#
..#..#..#..
##.##.#####
.##..##.###
...##....##
...##....##
.##..##.###
##.##.#####
..#..#.....
###..####.#

#.###...#
#.###.#.#
#.#.#..##
#.#######
.#..#..##
.###.####
.########
.##..###.
.##..###.
.########
.###.####
.#..#..##
#.#######
#.#.#..##
#.###.#.#

##.######.#
..#.#..#.#.
..########.
........#..
####.##.###
....####...
###.####.##
##........#
##........#
##.#....#.#
..##....##.
...#.##.#..
..###..###.
##.#.##.#.#
##.######.#
...#....#..
###..##..##

##.#..#
###.##.
#..#.##
.#.####
.#..##.
..#####
..#####
.#..##.
.#.####

.....##.###..
....#..####.#
####.#.#..##.
#.#..##.##...
#.#..##.##...
####.#.#..##.
....#..####.#
.....##.###.#
.#.#..###..#.
..###.#.#...#
..###.#.#...#

.##.###..#.
..#.###.#.#
######.#..#
######.#..#
..#.###.#.#
.##.###..#.
#.#.##..###
##.....####
#.##.##..##
..#########
..#.....##.
..###..#...
..###..#...
..#.....##.
..#########
#.##.##..##
##......###

.#..#.#....#.
#....##....##
.#..#...##...
.......#..#..
#######.##.##
#....########
######.#..#.#
#....#.#..#..
.####...##...

####.##..##.###
####..#..#..###
..#.###..#.#.#.
#####..##..####
...##..##..##..
..#####..#####.
....#.#..#.#...

####.#..####..#
###.###########
.##.#..........
.##.#..........
###.###########
####.#..####..#
######.######.#
.####.#.####.#.
###.##.##..#..#
.######..##..##
..#.#.##.##.##.
##..###..##..##
#......#....#..
.........##....
...#.#.##..##.#

..#..##..#...
###..##..####
###..##..####
.##..##..##..
#..##..##..##
##...##...###
####....#####
...######....
##.#.##.#.##.

####.##
######.
......#
......#
.##...#
#..###.
#..#.#.
#..#.#.
#..###.
.##...#
......#
#..#..#
######.
####.##
####..#

...#....#
#..#.####
..######.
##....###
##...#.#.
..#....##
###.##...
.....###.
.....###.
###.##...
..#....##
##...#.#.
##....###

########..#.#
#######..####
..####....##.
.#.##.#.##...
..####..####.
.##..##..#.##
#.#..#.###...
........#.#.#
.#....#.#....
#......#.#..#
#......#.#..#

.#..##....#
.#..##....#
#.##.#....#
#..###.##.#
##..###..##
#.##.#.####
#.###......

.##.#....#.##..#.
#..#..##..#..#.#.
.#..#.##.#..#...#
#..##....##..##..
#..##....##..#.#.
#.#..#..#..#.####
.#..#.##....#...#
#.###....###.#...
..##..##..##....#
##...#..#...##...
####..##..#####.#
###.######.###..#
#.##.####.##.####
#.##.####.##.####
###.######.###..#
####..##..#####.#
##...#..#...##...

####..##########.
#..####..#..#..##
.#.####.#....#.##
.###..###....###.
..#.#..#......#..
##......######...
.##....##....##..
.########.##.####
##......######...

##..#....##.##.##
#..##.#.#.#....#.
....###.#..#..#..
....###.#..#..#..
#..##.#.#.#....#.
##..#....##.##.##
#....##.###.##.##
.##.##..#.#......
##.#...##.##..##.
.#..#..##........
....#.#.#..####..
##.#..####.####.#
####.#.#.#......#
#.#..#.##..#..#..
#.###..#....##...

..#.####...##..
.....#####....#
##..#..####..##
##...#..##.##.#
..#.##..###..##
##.#...#.######
....#.#..######
##.##.##.##..##
##.#######.##..
..##.###...##..
#####...##.##.#
##.#.##..#.##.#
##..#..##.####.
####....#..##..
##.##..#.#....#

#.###...#..#.
.#.#.#..#..#.
...####..##.#
.#.###..#.###
.#.##..#.####
.######...#..
#.#......##..
#.#......##..
..#####...#..
.#.##..#.####
.#.###..#.###
...####..##.#
.#.#.#..#..#.
#.###...#..#.
#.###...#..#.

.........#.
#..##..##.#
........##.
.##..##...#
........#.#
........###
#..##..##..
...##...###
..........#
.##..##..##
.##..##....
#..##..#.#.
........##.

.....######......
####.##..##.####.
##..#.####.#..##.
.#..#.....##..#.#
.#..##.##.##..#..
.#...######...#..
#.#..........#.##
.###.#.##.#.###..
.###.#.##.#.###..

.###.#.#..#.##.#.
....###..########
.##.....#..#..#..
#.#..#..#........
...###.#.#..##..#
#.#.........##...
.###.#.#.##.##.##
####.###....##...
##.####.#...##...
##..###...#....#.
.#...#.#..##..##.
.#...#.#..##..##.
##.####...#....#.

#.#.#..#.##
###.#.##..#
###.#.##..#
#.#.#..#.##
#.##.####..
.#.###...#.
.#.########
.#.###.####
.#.###...#.

##..##..###.#
##.#..#.#####
..##..##..##.
.##....##.#..
#..#..#..###.
#.##..##.#.#.
#.#.##.#.####
#.######.#..#
#.######.#..#
#.#.##.#.###.
#.##..##.#.#.

######.##..
.#.#..##...
.#.#..##...
######.##..
.#..#.#.##.
#######...#
#.#.#..##..
.##.#...##.
.#..###.#..
.....#.#..#
.....#.#..#
.#..###.#..
.##.##..##.
#.#.#..##..
#######...#
.#..#.#.##.
######.##..

######.##
###.##.##
#.######.
#.######.
###.##.##
######.##
....##.##
##.##.#.#
####.##..

.#...#..#
##...#...
....#..#.
....#..#.
##...#...
.#..##..#
####...##
##.#..#.#
#.......#
.#.....#.
..#.##.##
.#.#.....
..###.#.#
#..###.##
.##....##
..#######
..#######

.######
#####.#
#...##.
#...##.
#####.#
.######
..#...#
.#.#...
##..#..
#...##.
#...##.
##..##.
.#.#...

.#.##..#.##.#
.##.#....##..
#..####.####.
.##.#...####.
####.##.####.
#.####..#..#.
####...#.##.#
####...#.##.#
#.###...#..#.
####.##.####.
.##.#...####.

.##.#.#.....#..##
##.#..#.#.##.#.#.
.#..####....#...#
.#.#.#..##.###..#
...#.#.#....####.
..##...###.#....#
##.....###.#.....
##.....###.#.#...
..##...###.#....#
...#.#.#....####.
.#.#.#..##.###..#
.#..####....#...#
##.#..#.#.##.#.#.
.##.#.#.....#..##
.##.#.#.....#..##

#.....#..
#..##..##
.##.##.#.
###.##.#.
#..##..##
#.....#..
#.#.#.###
#....#...
#.#...##.
#.##..##.
######...
######...
#.##..##.

##..#.#
###.#.#
###.#.#
##..#.#
#.##.#.
.#....#
..#.###
..#.#.#
.##..#.
....###
###....
#..#.##
######.
.##..##
#.###.#

..##..#.#.##.#.
#..#..##.#..#.#
######..######.
..#####........
######.##.##.##
######.##.##.##
..#####........
######..######.
#.....##.#..#.#
"""
main(input)