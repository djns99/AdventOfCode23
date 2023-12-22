import math


def build(lines):
    nodes = {}
    for l in lines:
        l = l.split('->')
        node, dests = l[0].strip(), l[1].strip().split(',')
        dests = [d.strip() for d in dests]
        type = node[0]
        node = node[1:] if type != "b" else "broadcaster"
        nodes[node] = [type, dests, False, {}]

    for key, value in nodes.items():
        for d in value[1]:
            if d in nodes:
                nodes[d][3][key] = False
    return nodes


def do(nodes, start="broadcaster", fin_node=None):
    pulses = [0, 0]
    pulseq = []

    # print("================\nPressing button time", i)
    q = [("button", False, start)]
    i = 0
    while q:
        i += 1
        src, pulse, name = q.pop(0)
        # print("Received", src, "-", pulse, "->", name)
        if not fin_node or name == fin_node:
            pulses[pulse] += 1
            if not pulse:
                pulseq += [i]

        if name not in nodes:
            continue

        type, dests, state, states = nodes[name]

        signal = pulse
        if type == "%":
            if pulse:
                continue
            signal = not state
            nodes[name][2] = signal
        elif type == "&":
            states[src] = pulse
            signal = not all(states.values())

        for d in dests:
            q.append((name, signal, d))

    return nodes, pulses, pulseq, i


def part1(lines):
    grid = build(lines)
    pulses = [0, 0]
    for i in range(1000):
        grid, newpulse, _, _ = do(grid)
        pulses = list(a + b for a, b in zip(newpulse, pulses))
    print(pulses)


import math


def factorize_r(val):
    factors = []
    for i in range(2, int(math.sqrt(val)) + 1):
        if val % i == 0:
            factors = factorize_r(i) + factorize_r(val // i)
    if not factors:
        factors = [val]
    return factors


def factorize(val):
    factors = factorize_r(val)

    print("val", val, "has factors", factors)
    out = {}
    for f in factors:
        if f not in out:
            out[f] = 0
        out[f] += 1
    return out


def part2(lines):
    nodes = build(lines)

    q = [("broadcaster", []), None]
    sets = {"kn": set(), "fb": set(), "ln": set(), "vl": set()}
    paths = {}
    while q[0]:
        while q[0]:
            top, path = q.pop(0)
            if path:
                sets[path[0]].add(top)
                paths[path[0]] = path
            print(top, end=',')
            if top in nodes and not top in path[:-1]:
                for d in nodes[top][1]:
                    q.append((d, path + [d]))
            else:
                print('(loop) ', end='')
        print()
        q.pop(0)
        q.append(None)

    for k, p in paths.items():
        print(k, [(nodes[l][0] if l in nodes else "") + l for l in p])

    miniters = []
    for d in nodes["broadcaster"][1]:
        for i in range(10000):
            nodes, _, lowpulse, numpulse = do(nodes, d, fin_node=paths[d][-3])
            if lowpulse:
                miniters.append(i+1)
                print(d, "pulses", lowpulse, '/', numpulse, "on iter", i)
                break

    primes = {}
    for v in miniters:
        facts = factorize(v)
        for f, c in facts.items():
            if f not in primes:
                primes[f] = c
            else:
                primes[f] = max(primes[f], c)

    print("Prime map", primes)

    result = 1
    for k, c in primes.items():
        result *= k ** c

    print(result)


def main(input):
    # part1(input.strip().split('\n'))
    part2(input.strip().split('\n'))


inputs = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
# main(inputs)
inputs = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
# main(inputs)
inputs = """
%nr -> mr
&sx -> zh
%rk -> dc, bl
%lx -> rs
%hx -> bl
%hp -> bj
%dk -> mr, lf
%hc -> xc
%bj -> vv, rd
&jt -> zh
&bl -> ks, kn, dc, hc, zk
&zh -> rx
%sp -> hz, bl
%rd -> vv, tp
%cg -> dk
%rg -> jl, pv
%jl -> js
%fb -> vv, zd
%gv -> lx
%lr -> vj, bl
%vz -> hc, bl
%kn -> bl, zk
%rj -> mr, nr
%cn -> pv, sb
%rs -> vv, hp
&mr -> qc, kb, gc, vl, bs, cg, lf
%rb -> qj
%sm -> bv, vv
%dh -> rg
%zk -> vz
%qj -> xs, pv
%ng -> ql, pv
%vj -> bl, sp
&kb -> zh
%sb -> pv
%vl -> mr, cz
%dc -> lr
%xc -> rk, bl
%cz -> cg, mr
%hz -> bl, hx
%xs -> pv, cn
%js -> ng
%cb -> mr, nc
%qb -> vv
%gc -> qc
%bv -> qb, vv
broadcaster -> kn, fb, ln, vl
%bs -> cb
%lf -> gc
%nc -> mr, rj
%ln -> pv, dh
%qc -> bs
&vv -> zd, jt, fb, hp, gv, lx
&ks -> zh
%ql -> rb
%tp -> sm, vv
&pv -> sx, dh, jl, ln, js, rb, ql
%zd -> gv
"""
main(inputs)

custom_order = """
%nr -> mr
%rk -> dc, bl
%lx -> rs
%hx -> bl
%hp -> bj
%dk -> mr, lf
%hc -> xc
%bj -> vv, rd
&jt -> zh
&bl -> ks, kn, dc, hc, zk

%sp -> hz, bl
%rd -> vv, tp
%cg -> dk

%fb -> vv, zd
%gv -> lx
%lr -> vj, bl
%vz -> hc, bl
%kn -> bl, zk
%rj -> mr, nr
%rs -> vv, hp
&mr -> qc, kb, gc, vl, bs, cg, lf
%sm -> bv, vv
%zk -> vz
%vj -> bl, sp

%vl -> mr, cz
%dc -> lr
%xc -> rk, bl
%cz -> cg, mr
%hz -> bl, hx


%cb -> mr, nc
%qb -> vv
%gc -> qc
%bv -> qb, vv
broadcaster -> kn, fb, ln, vl
%bs -> cb
%lf -> gc
%nc -> mr, rj


&kb -> zh
%qc -> bs
&vv -> zd, jt, fb, hp, gv, lx
&ks -> zh
%tp -> sm, vv
%zd -> gv


%ln -> pv, dh
&pv -> sx, dh, jl, ln, js, rb, ql
%dh -> rg
%rg -> jl, pv
%jl -> js
%js -> ng
%ng -> ql, pv
%ql -> rb
%rb -> qj
%qj -> xs, pv
%xs -> pv, cn
%cn -> pv, sb
%sb -> pv
&sx -> zh

&zh -> rx
"""
# main(inputs)
