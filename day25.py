def part1(lines):
    map = {}
    for l in lines:
        l = l.split(':')
        k = l[0]
        vs = l[1].strip().split(' ')
        if k not in map:
            map[k] = []
        map[k] += vs
        for v in vs:
            if v not in map:
                map[v] = []
            map[v].append(v)

    selected = None
    for k, v in map.items():
        if len(v) == 1:
            selected = k
            break

    print("Selected", selected)

    seen = {}
    seen[selected] = 0
    q = [(selected, [])]
    i = 0
    while q:
        i += 1
        q.append(None)
        while q[0]:
            top, path = q.pop(0)
            path = path + [top]
            for v in map[top]:
                if v not in seen:
                    seen[v] = i, path
                    q.append(v, path)
        q.pop()










def main(input):
    part1(input.strip().split('\n'))

input = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""