import math


class Rule:
    def __init__(self, string):
        self.string = string
        string = string.split(':')
        self.cat = None
        self.val = None
        if len(string) >= 1:
            self.next = string[-1]
        if len(string) == 2:
            condition = string[0]
            if '>' in condition:
                condition = condition.split('>')
                self.comp = lambda x, y: x > y
                self.greater = True
            elif '<' in condition:
                condition = condition.split('<')
                self.comp = lambda x, y: x < y
                self.greater = False
            else:
                assert False

            self.cat = condition[0]
            self.val = int(condition[1])

    def do(self, o):
        if self.cat and not self.comp(o[self.cat], self.val):
            return None
        return self.next


class Workflow:
    def __init__(self, parts):
        parts = parts.split(',')
        self.rules = []
        for p in parts:
            self.rules.append(Rule(p))

    def do(self, o):
        for rule in self.rules:
            r = rule.do(o)
            if r is not None:
                return r
        assert False


def part1(lines):
    workflows = {}
    morerules = True
    result = 0
    for l in lines:
        if l == "":
            morerules = False
            continue

        l = l.split('{')
        if morerules:
            workflows[l[0]] = Workflow(l[1][:-1])
        else:
            o = {}
            for cat in l[1][:-1].split(','):
                cat = cat.split('=')
                o[cat[0]] = int(cat[1])
            wf = 'in'
            while wf not in 'RA':
                wf = workflows[wf]
                wf = wf.do(o)
            if wf == 'A':
                result += sum(o.values())
    print(result)


class Range:
    def __init__(self, ranges=None):
        if not ranges:
            ranges = {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}
        self.ranges = ranges

    def zero(self):
        return any(l == r for l, r in self.ranges.items())

    def shrink(self, rule):
        if self.zero():
            return None
        if not rule.val:
            return rule.next, self
        if rule.greater:
            split = rule.val + 1
        else:
            split = rule.val

        newrange = Range(self.ranges.copy())
        original_range = newrange.ranges[rule.cat]
        left = original_range[0]
        mid = min(max(split, original_range[0]+1), original_range[1])
        right = original_range[1]

        pass_range = (left, mid)
        fail_range = (mid, right)

        if rule.greater:
            pass_range, fail_range = fail_range, pass_range

        #print("Fail", fail_range, "Pass", pass_range)
        self.ranges[rule.cat] = fail_range
        newrange.ranges[rule.cat] = pass_range
        #print(self.ranges, "->", newrange.ranges)
        if newrange.zero():
            return None
        return rule.next, newrange

    def count(self):
        c = 1
        for key, range in self.ranges.items():
            assert range[1] >= range[0]
            c *= range[1] - range[0]

        return c

    def dedup_count(self, other):
        c = 1
        oranges = other.ranges
        for k, range in self.ranges.items():
            orange = oranges[k]
            result = min(orange[1], range[1]) - max(orange[0], range[0])
            result = max(result, 0)
            c *= result
        if c:
            print("Dedup", self.ranges, other.ranges, "duplicates are is {}/{}".format(c, self.count()))
        return c

    def __repr__(self):
        return str(self.ranges)


def part2(lines):
    workflows = {}
    morerules = True
    for l in lines:
        if l == "":
            break

        l = l.split('{')
        if morerules:
            workflows[l[0]] = Workflow(l[1][:-1])

    stack = [('in', Range())]
    finals = []
    count = 0
    while stack:
        key, range = stack.pop()
        #print('Next worflow', key, range.ranges)
        if key == 'A':
            finals.append(range)
            count += range.count()
            continue
        if key == 'R':
            continue
        wf = workflows[key]
        for rule in wf.rules:
            next = range.shrink(rule)
            if next:
                #print("Push", next)
                stack.append(next)
            #print("Update self", range)

    #print("Predup count", count / 10e9, 'vs', 167409079868000 / 10e9)

    for i, f in enumerate(finals):
        for o in finals[i + 1:]:
            count -= f.dedup_count(o)

    print("Dedup count", count, 'vs', 167409079868000 / 10e9)


def main(input):
    part1(input.strip().split('\n'))
    part2(input.strip().split('\n'))


input = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
main(input)

input = """
ttx{a>2952:R,x>3156:R,A}
mtl{s<2688:A,m>2764:A,m>2513:A,A}
xr{m>2905:rc,pm}
hxl{a<1867:jvl,x>2112:R,mjc}
rj{s>2173:A,a>1545:R,m<3290:A,R}
kdj{a<1508:sz,R}
ffs{s<2066:xsr,A}
ldc{s<2799:tfp,zc}
zqc{m>3028:R,R}
th{s>172:R,a>2933:A,x<3442:R,R}
gkf{x<154:A,m>471:A,R}
jnt{s<991:A,x>882:R,R}
qb{m<865:hj,s>1288:R,crr}
fjx{a>96:A,A}
dlf{a>892:jg,shm}
qp{x>1032:A,s>2654:gl,m>917:A,R}
xvr{s>1139:R,s<1012:R,a>1507:A,A}
hvt{s<3614:mhv,a<1048:pb,vgf}
sd{a<2455:A,x<3079:R,A}
tpq{x>3252:tl,x<3101:A,rzd}
tg{x>1907:A,a>2459:R,R}
dnn{m>3344:R,R}
xt{s>1861:jt,s>1697:R,s>1608:R,R}
pd{x>381:R,m<1438:R,a<3826:R,R}
dt{a>3206:gx,s>3630:ch,a>2717:krl,sgp}
hn{x>3764:A,x<3566:R,a<150:R,R}
zv{m<2971:A,R}
rjb{x<3515:R,x>3707:A,A}
dr{a<2942:R,m>2425:R,A}
bxx{x>1952:A,s>3110:R,s<2776:A,R}
bfr{m>3481:A,m>3357:A,R}
kh{m<655:R,s>1465:A,x<1376:R,A}
qhb{a>3508:xc,qcd}
glf{m>2749:R,a>2796:R,R}
cp{a<2342:R,A}
gg{x>2869:A,m>954:A,R}
xrq{a>1477:zzz,R}
dqb{s>1021:A,x<2223:A,sqg}
kft{s<2785:xr,a<2516:dss,qnc}
gb{s>1551:R,a<3568:R,R}
kq{x<58:R,x>101:A,m>3630:A,hqg}
hs{s>1423:fr,R}
tf{s>439:kgd,x<2122:vlx,pzp}
sxd{a<2877:R,R}
vc{s>2251:R,vhv}
sv{x<832:A,m<2745:R,x>1415:R,A}
ppn{m<3502:qx,zjh}
gx{x>573:R,a>3725:pd,A}
zzz{m<2669:R,x>2772:A,A}
dkt{m>3115:R,x>3592:R,R}
ghl{s>2544:A,x<410:A,m<3646:R,R}
jpj{s<2801:R,m>1728:R,R}
xld{m<3628:A,x>3145:R,x<2926:R,R}
fxz{a<2754:mvp,tgn}
xsr{x<2921:R,s>1911:A,A}
bnd{s<344:A,x<2429:R,s>503:R,A}
tgn{s>3589:R,R}
cr{a>1176:R,xlb}
gft{a<1943:hp,x>2731:jvb,s<1913:cmh,kv}
xv{m<3258:R,a<3081:dxh,qnp}
qgk{m>926:A,m<335:R,s>265:mr,A}
pkm{s<949:mtk,s>1358:A,bk}
hlg{a<308:A,m<3324:R,A}
qzv{x<364:A,R}
csg{s>489:R,m>3208:A,m<2712:R,A}
vf{s<2847:pcb,fjv}
xn{m>3627:R,a>2782:A,a<2733:A,A}
pb{s>3758:bx,s<3663:mb,lf}
rzh{m<1894:A,s>3310:hxt,m<2064:A,bdv}
kht{m>3639:ckg,gvv}
dlz{x>911:A,a>2989:A,A}
kkj{m>3195:A,R}
kf{s>1463:A,hm}
pvf{m>3390:jcd,qv}
hnz{a>1056:R,s>2709:R,A}
ssg{s>3489:bq,a>1382:rzh,pqf}
lth{m>1505:sb,x<2150:dch,m<1088:sl,rmz}
sfc{m<3919:R,m<3946:A,R}
bdv{s<3250:R,s<3277:A,R}
xdm{a<2948:R,m>3213:A,m>2636:A,A}
sxj{x>2398:A,a<3651:sv,bpd}
qh{x<255:R,x<511:R,a>1323:A,A}
hxt{s<3411:R,m<2082:R,s<3452:R,A}
smq{x<1742:gv,x>2951:tvf,m>3017:kht,xzl}
rr{x<1123:R,cvh}
rhf{a<1178:vpp,s>2907:A,kpq}
slr{x<1125:stt,x>1389:xdv,R}
vz{a<1633:ln,hd}
rzd{m<3020:R,x<3201:R,m>3361:R,A}
qcp{a<2916:sxd,m<2988:mvk,s>657:hbq,gld}
hlq{a>2991:R,s>2584:R,A}
cqn{m<3186:qf,a>1064:gd,qsp}
bg{x>1795:A,x<1646:A,A}
hb{m<3229:glf,s<2582:ffs,vf}
hqg{x>75:A,s>1097:R,A}
cl{m<1136:R,R}
kc{x>792:qp,kdj}
nvn{a>1200:A,x>301:A,A}
cjc{m>2356:A,x<1998:R,R}
qkp{x>2242:A,R}
qnc{x>1549:R,a<2582:A,m<2968:hgd,R}
qnq{m<3020:A,s<523:R,A}
xss{m>2523:R,x<578:R,R}
ntf{s<320:fqr,a>743:csg,R}
dm{m>1950:zld,pmh}
tzd{m>2469:A,A}
lm{a>1660:czz,s>714:R,m>3694:szj,dfq}
rf{a<703:A,m>591:R,R}
tz{a>1072:cnn,a<369:fl,s>2108:lp,sbr}
vrj{x>2206:lhn,m>2733:gsj,rbl}
nt{m<3734:A,A}
hgd{x<1014:R,A}
lps{m>2797:A,s<1055:A,R}
hpj{a<3775:A,A}
kff{a<3917:R,x>1813:R,s>2732:R,R}
xlb{a<782:R,a>1022:A,s<727:R,R}
mdd{m>1795:A,R}
vlx{a<1204:kn,s<238:gfr,vz}
dss{a>2397:R,x>2070:tr,A}
dv{m<3250:R,x>901:R,m>3613:R,jnt}
jlj{m>1123:mdd,s<181:rs,x>565:vst,rjr}
gmc{x<3362:R,A}
jvl{m<2535:A,A}
ml{a>1397:R,a>1210:R,a<1121:R,R}
xdn{x>791:A,R}
xb{s<693:R,m>3901:A,A}
qk{s>456:lb,a<1490:zrm,txc}
gz{s<2525:R,s>3422:xdm,ttx}
kpp{s<3542:A,x<470:A,R}
jk{m<3715:R,m>3826:A,A}
fjh{m<3681:A,A}
mb{a>546:R,a>250:A,m<2811:R,R}
pqf{m>1734:A,R}
jks{m>3630:bvv,a>3709:qsz,m<3402:A,jp}
msp{x>512:qpm,s>3718:ngb,x<291:xcd,jzh}
pls{s>459:ks,x<1668:jlj,a<3525:qgk,qnh}
vq{m<1755:R,s>2905:R,R}
zld{s<3811:R,vqt}
krl{x<811:A,bm}
gv{x>734:npb,s>919:dlf,a>1016:qk,lcg}
gnl{m<1814:A,m>2087:A,R}
nf{x<915:A,m<3238:R,A}
dqh{x<1801:cd,cb}
dkv{x<1394:knk,s<1270:A,x>1645:A,A}
lcz{s>474:A,a>2872:A,R}
mbf{a>2604:zxt,lhx}
bkv{s>3836:A,a<1509:R,A}
lnz{a>2180:A,a>2101:mkz,mq}
xl{a>3292:A,A}
zd{m<3724:A,cp}
xzl{a<1197:rkt,s>775:cnz,a>1692:qxx,jvt}
df{s>1223:R,A}
ns{m>2631:A,x>3304:A,A}
fz{a<2329:jkq,x>3264:hdt,pc}
sh{x<469:R,A}
fgh{s<1176:cj,m<3382:R,a>2530:R,nl}
ktx{x>1896:bqm,x<680:kpt,pcx}
bm{x<1087:R,A}
cj{m<3225:R,x<1134:R,a<2414:A,A}
xcd{m>1086:pcn,m>618:lg,m<256:A,gkf}
vjn{x<1078:hnf,fgh}
hvg{a>3048:xv,gbh}
bhf{x>1748:gdv,x<739:fn,m<3167:lnz,slr}
lcg{x>403:tbf,mll}
vgf{m<2626:A,a<1468:R,A}
xc{m>3206:gpk,a>3733:jtb,dl}
nv{s>616:R,a<898:R,R}
qx{x<494:jjs,a<879:hlg,s>3495:A,lbr}
hg{x>2311:A,x<2072:A,x<2225:A,R}
jcd{s>669:A,R}
rl{m>1230:R,A}
tjp{m>3258:A,m>2734:A,m>2473:ncv,A}
lhx{x<3542:kb,m>3249:fzr,fm}
zsb{x<986:R,A}
pk{m<2923:R,x<325:R,R}
hnf{a>2381:A,m>3006:R,rn}
vzz{m<2556:R,A}
qv{s>669:A,m>2885:zsl,s<325:R,fpl}
ddr{a<1562:R,a<1725:R,x<2224:A,A}
jpr{m<1413:rf,s<149:spz,m<1858:bgx,mbb}
vtk{x>302:fck,x>145:mcr,m>2954:kq,vqb}
qsz{x>3289:R,x>2886:R,x<2748:A,R}
br{m>3471:A,R}
xd{a>253:R,m<1273:R,R}
tfp{a>2307:R,x>3215:R,x<2902:A,A}
xx{x<2207:A,A}
kpq{x>3697:R,m>2602:R,R}
lsp{x<3275:R,a>2091:R,s<2171:R,R}
szk{m>2885:A,s>604:R,s<491:A,R}
xdv{m<3543:R,s>2970:A,A}
pcx{m>3083:qng,x>1253:dzc,sm}
nzd{x<2252:ngt,hpj}
ks{m>1405:bhm,x<2342:R,a<3495:ljf,A}
dgr{a<674:R,m<3710:R,A}
jkq{a<2204:A,s>904:R,a<2286:R,A}
cth{a>454:R,a<430:A,R}
crp{s<807:R,A}
zxt{s>1156:lnc,a<2857:tc,a<2952:qcp,hvg}
xms{a<3185:A,a<3222:R,R}
qjf{s<1410:hf,a<2837:tp,zv}
zmp{a>239:ns,x>3310:hn,A}
tk{a<504:R,x<3530:A,A}
kgd{m<1186:cr,s<756:ccv,m<1884:nmz,nj}
jvg{s<341:R,A}
tm{m<1324:A,A}
jh{m>3739:R,x>228:R,A}
nb{a>209:A,A}
sk{s<379:R,s>493:tbx,fth}
jhr{m>3828:R,a>1154:R,A}
jn{x>3372:A,m>3303:R,m>2952:A,A}
xhs{a>2073:R,bxx}
pzp{x>3016:qjj,x<2640:jpr,s>170:fmx,rl}
vqb{a>2408:A,m>2574:crp,x<89:R,jl}
qn{m<2135:A,a<917:A,R}
rks{m>2588:R,R}
fg{x<1739:hq,s<695:lz,brx}
zc{x>2953:A,R}
mcc{s<303:R,R}
pgq{a<1682:R,R}
xg{s>1101:R,R}
lv{x>3206:jn,kk}
jbk{a<1523:jxm,R}
ql{s>597:R,bbb}
mqt{a>678:A,m<3721:A,s<669:A,A}
hfk{a>2335:kft,bhf}
pcn{m>1709:R,x<193:A,x>253:A,R}
qsp{a>383:sr,tx}
hcc{m<2743:R,A}
nl{m<3655:A,s>1427:A,m<3779:R,R}
jjs{x>212:A,x<83:R,R}
gfr{m>945:R,s<139:tt,s>202:A,pz}
qjj{x<3465:A,s>286:R,tm}
pmh{m>1633:A,m<1516:A,x<2267:svg,gvj}
gc{s>138:A,m>3814:R,A}
fm{a<2320:sf,a>2500:rks,qbv}
ll{m>3255:R,R}
bt{a>1118:R,x<307:A,A}
sz{x<400:A,R}
bvh{x>3239:rjb,m<3108:A,A}
jrc{s>1467:svb,smq}
kk{s>1474:A,A}
ktf{x>3720:A,R}
zp{m>3515:R,A}
bph{a<2054:A,a>2139:A,s<323:gc,ph}
rhr{m>3077:R,R}
tl{a<967:A,x>3447:A,s>957:A,A}
zjh{m<3771:R,s>3513:R,A}
zk{a<1476:R,a<1756:R,x>2550:A,A}
jbm{x<393:R,A}
ngt{x>1229:A,x>518:R,R}
shm{s<1241:R,s>1363:tsz,a>522:R,A}
mbb{s>287:A,R}
vg{x<253:sq,zxg}
kn{s>236:A,a>459:R,xd}
gcb{s>3147:xn,m>3387:xdn,nf}
kd{a>541:zm,s<1221:R,s>1312:vd,cth}
npb{s<581:ntf,vr}
rxz{s<2143:R,R}
kmh{s>2920:qlx,kc}
sr{x<2598:A,x<3082:dgr,A}
lj{x>2551:hnz,m<2651:tvb,x>1987:mjn,A}
bp{a<3052:A,a>3081:A,m>2794:A,R}
bqm{a<3028:gz,rv}
pm{s<2141:A,A}
cz{x<700:vtk,x>966:vjn,a>2410:pvf,pqx}
ktm{m<3519:R,s>1737:R,R}
qj{x>1170:rqr,cz}
tvb{s>3127:A,m>2406:R,A}
pcg{s<373:A,x>423:R,m>3371:R,A}
cv{x>3590:fx,a<1421:tpq,bc}
sp{m<3060:R,a>3443:A,R}
jvt{x>2470:xrq,m>2536:jbk,pv}
ph{a<2110:A,A}
mll{x<170:A,x>305:qnq,x<234:A,R}
hj{m<400:R,A}
rxg{s>1547:xt,x<1050:qb,m<1048:fvz,dkv}
jhn{a>888:R,m<3302:hbs,A}
vb{m>2774:R,x<2730:A,A}
kxp{a>559:R,R}
lp{x<898:tgv,s>2600:vch,zsk}
qg{x>1542:A,a<1756:A,m>660:R,A}
frj{x>666:A,R}
fks{m>3207:cng,a<1413:R,mtl}
cf{a>1321:px,gm}
nr{x<2387:xhs,s>3042:nd,m>640:ldc,npm}
dch{x<1067:vt,s>467:km,x<1623:cvp,tg}
jm{m>2876:A,s>1418:A,x<1378:A,R}
vqm{x<945:R,s>3106:R,A}
vt{x>707:A,s<475:A,A}
vqt{s>3876:A,s>3854:R,m>2147:A,R}
smt{s<2585:A,x<862:A,R}
hl{x<1783:A,A}
km{s<832:R,R}
xgj{s<1484:R,A}
jrl{m>3067:A,s<2230:R,m<2772:A,R}
gp{x<1931:A,a<2204:A,R}
gdv{s>2871:kkj,x>2733:lsp,A}
zq{s>595:A,a>1712:A,a<1572:A,A}
nhs{m<3166:hvt,x<895:ppn,gnh}
gpl{m>3737:R,x>1121:R,x<1045:R,A}
srq{x>800:mv,m>3403:dd,R}
pl{x>1305:R,a>609:R,A}
vst{x<1083:R,m<502:A,a<3473:A,R}
jkn{m<1436:A,a>1521:R,R}
tc{a>2728:bvh,dxm}
kl{m<3670:R,A}
pc{s>929:A,s>537:A,s>351:A,A}
vs{m<2749:R,s<2625:R,m<2869:R,R}
rps{m<1369:nr,s<3165:kr,s<3715:ssg,dm}
vch{x>1144:R,a>793:R,s<2781:nh,zsb}
tsz{x>314:R,x>119:A,m>3173:R,A}
vgl{a>2941:A,A}
lnl{x<1144:R,a>582:pfh,a<274:jk,kl}
bpd{x>1569:R,A}
jvb{s>1745:R,A}
sx{a>3105:qhb,s>1779:ngc,x<2651:qj,mbf}
rqr{a<2344:fg,sn}
gr{a>1149:R,a>628:vq,x<3078:R,A}
vx{s>1319:A,a<2837:zqc,A}
gvj{s>3847:R,a>2133:R,s>3770:A,R}
vjv{m>3055:gcb,kpl}
ls{a<182:frj,s<2806:A,A}
kr{a>1748:qmc,gr}
mqp{m>3451:A,A}
frg{x>1348:rps,s>3393:zt,kmh}
rb{x>2668:nt,a>1738:R,hz}
kpt{s>2795:szf,a>3034:qpn,sqs}
kb{x<2948:vl,m>2858:fz,pkm}
gl{x>950:R,m<1491:A,m>1796:R,R}
ps{a>2009:R,x>1617:A,s<1167:A,A}
mjf{m<852:R,A}
szj{x>2454:R,A}
kbc{s>290:A,x>3743:A,R}
fck{s<1185:R,x<469:xgj,rh}
kt{s<2608:lps,m>2783:A,zf}
mv{a>2219:R,s>975:R,A}
vzc{x<1383:vjv,s<3153:hb,fxz}
bc{m>3023:tgq,m>2515:zq,a<1619:gmc,fmc}
mfs{a>3272:jm,a<3182:zfm,A}
mvp{m<3145:vb,s<3486:xk,s>3659:zp,A}
rs{x>1071:A,A}
gvv{x>2446:mg,s<726:vn,x>2040:vbz,fzt}
txc{x>321:R,s<224:R,A}
fpl{s>554:R,A}
fqr{a>953:A,A}
zx{a>3079:pls,m>864:lth,vrt}
vpp{s<2433:R,A}
mjn{s<2934:A,s<3477:R,R}
fb{x>2157:tn,mfs}
bx{s<3864:R,a>593:R,A}
sn{s>672:vx,tjp}
qt{a<113:td,x>3440:A,R}
jtj{s>1032:ptl,a>1863:zx,tf}
gm{x<2924:R,x>3394:A,A}
lbr{x<728:R,s<3226:R,x>800:R,R}
mcr{m<3379:fp,jh}
mhv{x>516:R,R}
cjj{s<381:A,m<2596:A,m<2759:A,szk}
spz{a>883:R,x>2363:R,R}
lnc{x>3546:qjf,a<2820:pdk,a<2991:lv,js}
rg{a>1638:R,R}
vhv{x>3097:A,s>1800:A,A}
vn{m>3352:kqn,x<2074:A,xx}
tp{a>2710:R,A}
mtk{a>2194:A,R}
qnh{s>186:R,R}
gsj{x<1366:R,s>2125:sp,bg}
zz{m>3244:ghl,s<2587:sgv,grh}
kpl{m>2551:vs,a>2807:R,smt}
fpq{m>3489:R,A}
jzh{x<425:R,m<948:A,m<1533:sh,R}
hx{x>3158:dnn,m>3319:ddr,s<3518:zk,bkv}
qst{m>3722:jhr,A}
sm{m>2732:hlq,s>2633:dlz,qfq}
jtb{a<3840:nzd,m<2623:hcp,m>2908:hs,kt}
sqg{a>1427:A,a>1297:A,s<932:R,A}
dfq{s>415:R,m>3671:A,x<2631:R,A}
vd{a<474:A,A}
mcf{m<3197:R,s<1284:R,R}
kgx{s>298:A,x>291:A,R}
jnl{s>1914:R,x>624:A,R}
js{s>1518:R,m<3123:bp,s<1334:df,R}
qcd{m>3247:jj,a<3373:fb,vrj}
sb{a<2347:A,A}
vcs{a<2138:A,gp}
svg{s<3834:A,R}
sgv{m<2895:R,s<2473:A,a>1394:A,A}
xgr{m>3281:R,a<1422:cvc,R}
zsl{a<2815:A,x<800:A,m>3162:A,A}
mdp{m>3335:R,m<2892:A,a<466:R,R}
pfh{s<3413:R,x>1359:A,m>3624:R,A}
npm{a<1469:A,s<2774:R,x<3375:A,A}
kgj{x<221:A,m>3118:R,x<299:A,R}
crr{m>1637:R,x>566:A,A}
ss{m<1062:A,s<332:A,m<1834:R,A}
rn{a>2202:R,a<2059:A,A}
kg{a>406:kd,m>2981:pds,zmp}
cnz{a>1616:xm,m<2758:dqb,s>1040:tsk,qkp}
hbs{s<1706:R,a>787:R,s>1974:R,R}
dl{a<3607:gb,sxj}
gpk{x<2590:jb,jks}
rh{m>3096:R,s<1434:R,x<603:A,A}
dzc{x<1682:A,s<2921:hl,s>3532:A,R}
tx{a<155:fjx,a>300:R,s<2342:R,A}
fn{x<348:kgj,A}
sqs{a>2974:jrl,R}
tt{m<316:A,s>51:A,a<1453:R,R}
dd{x<761:A,R}
hcp{s>2008:kff,R}
cng{x<1121:A,m>3633:R,A}
bxc{s<2479:jtj,frg}
jt{x<990:A,A}
ck{s>3593:rg,m>3270:A,R}
in{m<2249:bxc,a>1959:sx,jrc}
qmc{x<2760:A,a>2522:xl,a<2239:jpj,A}
cmh{s>1383:cl,m>793:hpk,R}
ntr{x<3466:R,a<83:kbc,m<3473:R,A}
lk{x<1645:A,s>719:R,R}
ngc{a<2679:hfk,a>2899:ktx,vzc}
vrt{a>2302:ql,m<542:dqh,vcs}
qf{x<3152:lj,rhf}
jg{x<320:mcf,xvr}
kqn{a<690:A,x<2132:A,R}
qlx{x>505:gqh,vg}
gd{s<2707:vc,m<3578:hx,a<1479:cf,rb}
qrd{x>3621:A,A}
px{s>3456:A,x<2952:R,s>3108:R,R}
cbm{a<1610:R,a<1751:R,a<1862:R,R}
xk{x>2520:A,x>2073:R,A}
fzt{s<989:jlr,a>983:R,R}
qnp{m>3646:R,x<3548:R,m<3406:A,A}
fzr{s>650:zd,a>2219:sk,m>3681:bph,mqp}
qpm{a<744:R,s<3651:A,xf}
xf{a>1408:A,A}
sgp{s>3481:kpp,m>889:A,m>583:A,A}
mjc{s<420:R,x>1966:A,R}
vbz{x<2273:A,R}
bvv{s<1955:R,x>3096:A,m>3778:R,R}
tbj{x<1423:R,x>1644:R,m<541:A,A}
mzz{a>3012:A,s<3248:A,s>3687:A,A}
kv{s<2264:A,R}
nmz{a<732:rgb,s>920:ztg,x<2045:R,A}
zf{a>3934:A,s<3518:R,a<3888:A,A}
mkz{x<1117:R,s>2574:R,x<1441:A,A}
zs{a>2125:A,s<1419:R,m<2676:R,A}
szf{a>2986:A,x<338:A,A}
gmx{x<964:jnl,s>1990:rj,R}
bn{x<950:A,s>381:R,m>2971:R,A}
fx{s>612:A,x>3756:R,m>2989:xsq,A}
vr{m<3306:cfp,fjh}
ccv{x<2626:A,nv}
rc{m<3483:A,a<2460:R,R}
zsk{s<2349:R,m>3395:pl,mz}
rv{x<3057:A,s>2578:A,dkt}
hc{a>676:A,a<420:R,A}
pcb{x<2322:R,R}
ckg{x<2191:cs,m>3779:xb,a<1264:mqt,lm}
td{s<437:R,A}
cvp{x<1299:R,a>2500:R,s<287:R,R}
lg{m>907:R,a>1314:R,R}
qrt{a>2218:A,s<3825:A,R}
hdt{m<3403:A,s>836:A,A}
qbv{x>3840:bcz,a>2402:ktf,a<2352:R,R}
tn{x<2952:R,x<3537:R,a<3266:R,R}
cvh{m>3801:R,x<1255:A,a<1750:A,A}
tbf{m>3023:jvg,s>478:rqb,xss}
pds{x>3503:A,m<3605:R,A}
hpk{m<1385:A,R}
ljf{a>3320:A,m>770:A,R}
tr{s>3319:R,R}
nj{m>2018:qn,hc}
dxh{m<3714:A,x<3224:R,R}
fth{m>3662:R,a>2358:A,A}
xm{m>2565:A,a<1741:pgq,A}
zfm{s<1693:R,a>3141:A,m>2700:A,A}
pz{a>1461:A,R}
cx{a>2212:A,s>779:ll,a<2047:bn,rp}
qs{a<3470:R,x<1144:R,m>2432:A,A}
lhn{m>2896:rhr,mlg}
fp{s>923:R,a>2529:R,x<245:A,A}
hbq{x>3102:br,R}
jxm{s<294:R,x<2066:R,A}
rgp{a<931:R,a<1225:A,R}
rp{s>452:R,a>2147:A,R}
zg{s<1656:A,m<3499:R,s<2890:R,R}
ptl{x<1980:rxg,gft}
jl{s<743:R,a>2158:A,m>2458:A,R}
xkt{m<2896:mvh,a<590:R,A}
rnn{a>655:A,s>790:R,mcc}
hm{m>3548:A,m<3408:R,m<3467:R,R}
cb{m>301:R,x<2685:R,m<113:A,R}
mlg{m>2603:R,x>3314:A,R}
cn{s<1725:A,m>3261:nb,A}
bgx{x>2324:R,m>1561:R,A}
mzd{a>332:tk,a>202:qrd,m<2875:qt,ntr}
tgq{a<1729:A,A}
tbx{x>3701:A,m>3509:R,A}
jb{s>1469:fpq,s>959:A,m<3720:A,A}
gld{s<339:th,m<3649:R,x>3308:R,A}
mr{s>393:A,R}
knk{s>1282:R,m<1459:A,m>1790:R,A}
fvz{s<1217:tbj,s<1347:qg,a<1941:kh,A}
xmf{x<695:zg,s>1993:vmc,m<3608:R,xms}
qng{x>1427:R,x<1126:cxc,m>3646:mzz,A}
bk{s>1161:R,x<3172:R,A}
cs{m>3799:sfc,a<779:A,A}
vxt{x>2842:R,A}
ngb{m<767:bt,s<3844:A,m<1396:scp,R}
pdk{m>3054:xld,m<2597:R,A}
qpn{m>3121:R,m>2585:pk,qzv}
bkp{a<1035:A,s<762:R,s>1215:A,A}
fmx{x>2831:R,a>775:ss,A}
mvk{a<2933:R,m>2637:vgl,s<459:dr,tzd}
fmc{s>933:R,s<401:A,A}
sl{a<2522:R,gg}
bhm{a>3481:R,m>1876:R,x>2330:R,R}
dxm{m<3215:R,bfr}
tvf{a>717:cv,s>746:kg,mzd}
ncv{a<2609:R,s<326:R,a<2932:R,A}
zhv{x<800:A,m<2945:R,m<3493:rxz,R}
svb{x>1516:cqn,s>3001:nhs,tz}
fjv{s>2998:A,x>2376:R,R}
jlr{a<696:A,R}
rkt{m<2643:jqt,rnn}
jj{x>1439:kf,a<3256:xmf,mt}
mg{x<2632:bkp,a<910:A,vxt}
tgv{s>2691:jbm,a<610:mdp,m>2940:A,A}
stt{m>3720:A,R}
scp{m<1151:R,s<3903:R,m>1271:A,R}
lz{m>3242:A,x>2271:A,A}
ztg{m>1629:R,a>1219:A,a<955:A,A}
xsq{s>244:R,x>3685:A,A}
sqh{m<2440:R,m>2483:A,R}
zxg{s>3163:A,m<1458:R,A}
vmc{x>967:R,a<3200:A,A}
hq{x<1544:R,a<2102:ps,lk}
hd{s<319:A,a<1743:R,m>828:R,R}
jqt{s>882:R,A}
mvh{m<2607:R,A}
hf{a>2909:A,x<3805:R,A}
brx{s<1112:A,m<3175:zs,a>2208:A,R}
gnh{a<880:lnl,a<1345:qst,m<3446:ck,rr}
qxx{x>2436:cjj,hxl}
vl{m<3280:tgt,s>910:R,R}
ln{m>956:A,s<331:R,R}
rbl{a>3435:qs,s<1982:A,x<1415:A,vzz}
zm{s>1197:R,A}
sq{s>3177:R,s>3086:A,a>1610:R,A}
cfp{a<1038:R,x>1264:R,x>1086:R,A}
gbh{a>3015:A,m<2856:R,A}
cd{a>2105:R,A}
sf{s<907:A,x<3819:R,hcc}
bbb{m>470:R,A}
cxc{s<2824:R,a>2995:R,a<2952:A,R}
fl{s>2463:ls,s>1902:zhv,cn}
jp{x>3479:R,m<3551:A,A}
hp{a>944:jkn,kxp}
zrm{s<154:nvn,s>318:pcg,s>259:kgx,qh}
cnn{s<2266:gmx,x>516:fks,x>307:zz,xgr}
rqb{x>564:R,x<486:A,x<530:R,R}
nh{a<610:R,m<2936:A,A}
bcz{x<3900:A,a<2416:A,A}
ch{a>2655:A,a<2299:qrt,mjf}
mz{a>696:R,m<2953:A,x>1246:R,A}
sbr{a<717:xkt,jhn}
cvc{a>1301:R,a<1191:R,m>2843:A,R}
qfq{a>3000:A,R}
gqh{a>2632:vqm,A}
nd{a>1530:sd,rgp}
czz{a>1854:R,R}
tgt{m>2726:A,s<888:A,m>2455:A,R}
lf{x<876:R,x>1147:A,x<1046:A,R}
fr{m>3086:R,R}
lb{s<690:A,m>3008:ml,cbm}
zt{a<2090:msp,dt}
rgb{m>1530:A,a<315:R,a<533:R,A}
hz{s<3270:R,s>3585:R,R}
tsk{s>1307:A,m<2890:hg,x>2515:R,R}
grh{a>1507:R,R}
rjr{a>3681:A,m<671:R,a>3303:A,R}
pv{x<2189:cjc,a>1439:sqh,x<2352:A,bnd}
bq{s>3578:R,gnl}
rmz{a>2569:lcz,R}
pqx{x<868:srq,x>925:cx,a>2240:xg,dv}
mt{x<942:ktm,a<3395:A,a<3445:R,gpl}
mq{a<2034:A,A}

{x=310,m=3257,a=1233,s=1596}
{x=1001,m=21,a=1647,s=695}
{x=1026,m=1219,a=1619,s=95}
{x=1726,m=409,a=2362,s=35}
{x=449,m=75,a=87,s=962}
{x=1123,m=152,a=823,s=483}
{x=1630,m=2919,a=185,s=501}
{x=971,m=1358,a=2558,s=1952}
{x=1888,m=2852,a=469,s=2309}
{x=476,m=1180,a=90,s=1810}
{x=214,m=2478,a=107,s=2972}
{x=1928,m=2294,a=113,s=529}
{x=176,m=59,a=661,s=1947}
{x=672,m=2225,a=1145,s=71}
{x=703,m=820,a=636,s=1189}
{x=106,m=1687,a=529,s=792}
{x=933,m=281,a=1439,s=608}
{x=677,m=885,a=413,s=930}
{x=823,m=1963,a=779,s=134}
{x=1766,m=630,a=1658,s=2914}
{x=1768,m=2273,a=104,s=2458}
{x=32,m=580,a=1622,s=547}
{x=1608,m=999,a=3105,s=857}
{x=1454,m=367,a=2203,s=599}
{x=1686,m=2431,a=1304,s=108}
{x=368,m=1586,a=1352,s=978}
{x=688,m=755,a=1063,s=3125}
{x=1497,m=1904,a=396,s=970}
{x=1242,m=589,a=2945,s=1615}
{x=569,m=1962,a=423,s=126}
{x=333,m=475,a=2847,s=137}
{x=1453,m=424,a=1338,s=248}
{x=426,m=1084,a=673,s=147}
{x=2833,m=1944,a=778,s=1620}
{x=936,m=1412,a=26,s=336}
{x=73,m=1805,a=270,s=398}
{x=240,m=1750,a=18,s=3443}
{x=1128,m=919,a=1353,s=29}
{x=1383,m=504,a=798,s=32}
{x=325,m=412,a=1616,s=635}
{x=3451,m=3595,a=1806,s=250}
{x=21,m=690,a=765,s=1256}
{x=426,m=810,a=254,s=116}
{x=161,m=614,a=61,s=433}
{x=340,m=627,a=612,s=2081}
{x=669,m=510,a=9,s=45}
{x=2032,m=1551,a=273,s=2073}
{x=794,m=30,a=1173,s=690}
{x=2657,m=146,a=1901,s=505}
{x=1098,m=3378,a=1,s=85}
{x=805,m=2385,a=1617,s=2338}
{x=1101,m=524,a=3372,s=579}
{x=73,m=256,a=143,s=27}
{x=1213,m=103,a=722,s=1036}
{x=1193,m=251,a=1828,s=161}
{x=441,m=1760,a=1406,s=378}
{x=657,m=432,a=702,s=867}
{x=1909,m=645,a=1614,s=48}
{x=1886,m=741,a=3134,s=2165}
{x=431,m=702,a=1006,s=3691}
{x=129,m=494,a=173,s=533}
{x=1519,m=1130,a=592,s=2963}
{x=1738,m=175,a=2046,s=218}
{x=1511,m=1259,a=1286,s=1241}
{x=858,m=2187,a=23,s=1223}
{x=231,m=1191,a=2461,s=842}
{x=494,m=2197,a=2812,s=2275}
{x=9,m=12,a=1121,s=597}
{x=696,m=1166,a=2123,s=356}
{x=334,m=1454,a=1444,s=841}
{x=673,m=3064,a=659,s=2392}
{x=2773,m=83,a=1340,s=2254}
{x=841,m=437,a=135,s=432}
{x=11,m=16,a=1336,s=810}
{x=816,m=1591,a=305,s=179}
{x=2118,m=817,a=619,s=508}
{x=2084,m=80,a=276,s=882}
{x=3511,m=11,a=2489,s=403}
{x=478,m=705,a=557,s=43}
{x=3635,m=97,a=3142,s=3796}
{x=165,m=298,a=4,s=692}
{x=979,m=2398,a=1073,s=293}
{x=455,m=437,a=1739,s=2834}
{x=2325,m=1529,a=697,s=886}
{x=2533,m=1258,a=270,s=111}
{x=1956,m=60,a=3408,s=1}
{x=1860,m=3228,a=1499,s=665}
{x=1801,m=79,a=464,s=1084}
{x=20,m=879,a=1211,s=1438}
{x=470,m=60,a=2468,s=1255}
{x=202,m=655,a=2373,s=380}
{x=3412,m=50,a=842,s=47}
{x=325,m=3119,a=1089,s=167}
{x=637,m=1440,a=44,s=1876}
{x=726,m=713,a=2591,s=587}
{x=3393,m=267,a=2138,s=763}
{x=570,m=385,a=440,s=1494}
{x=511,m=272,a=1850,s=1787}
{x=2754,m=1804,a=380,s=510}
{x=699,m=410,a=891,s=365}
{x=510,m=1689,a=148,s=1209}
{x=1396,m=188,a=143,s=1768}
{x=771,m=59,a=2449,s=249}
{x=395,m=556,a=1578,s=1604}
{x=280,m=1479,a=480,s=61}
{x=272,m=71,a=1363,s=1523}
{x=790,m=2915,a=3199,s=346}
{x=738,m=906,a=387,s=832}
{x=2187,m=2228,a=2531,s=1753}
{x=1459,m=207,a=279,s=256}
{x=42,m=349,a=2876,s=1154}
{x=577,m=1859,a=520,s=1675}
{x=26,m=1220,a=2591,s=1657}
{x=324,m=1116,a=647,s=195}
{x=430,m=76,a=1388,s=615}
{x=881,m=31,a=1059,s=1212}
{x=732,m=199,a=521,s=325}
{x=2934,m=333,a=1041,s=1780}
{x=83,m=1300,a=733,s=1813}
{x=330,m=531,a=703,s=1213}
{x=1699,m=581,a=125,s=416}
{x=971,m=1388,a=952,s=1051}
{x=240,m=1567,a=6,s=2777}
{x=2453,m=889,a=65,s=44}
{x=1141,m=578,a=749,s=892}
{x=1,m=373,a=544,s=586}
{x=2150,m=1325,a=669,s=692}
{x=744,m=1128,a=118,s=572}
{x=2437,m=1520,a=1084,s=78}
{x=1526,m=251,a=2007,s=1686}
{x=282,m=678,a=912,s=2186}
{x=1314,m=546,a=492,s=1191}
{x=528,m=2271,a=356,s=81}
{x=774,m=1247,a=539,s=39}
{x=2045,m=513,a=404,s=2720}
{x=24,m=2875,a=509,s=466}
{x=189,m=3040,a=1099,s=3572}
{x=1827,m=1091,a=544,s=510}
{x=781,m=241,a=55,s=298}
{x=1746,m=2166,a=218,s=1026}
{x=2062,m=238,a=1390,s=148}
{x=201,m=1212,a=733,s=219}
{x=3450,m=1477,a=911,s=463}
{x=1023,m=16,a=1889,s=336}
{x=1514,m=1357,a=526,s=2087}
{x=1978,m=559,a=2569,s=1499}
{x=465,m=804,a=1364,s=1057}
{x=76,m=1603,a=1393,s=145}
{x=136,m=1053,a=16,s=1777}
{x=992,m=860,a=2343,s=275}
{x=463,m=1834,a=2504,s=786}
{x=41,m=1973,a=1173,s=787}
{x=296,m=833,a=38,s=1968}
{x=1686,m=1458,a=437,s=1583}
{x=750,m=35,a=293,s=156}
{x=2384,m=50,a=516,s=2568}
{x=1023,m=2252,a=1295,s=1933}
{x=45,m=2922,a=600,s=2194}
{x=310,m=28,a=475,s=1359}
{x=845,m=439,a=435,s=2025}
{x=467,m=1390,a=320,s=558}
{x=1106,m=315,a=3285,s=260}
{x=833,m=314,a=950,s=528}
{x=54,m=3047,a=40,s=1116}
{x=230,m=119,a=887,s=514}
{x=6,m=428,a=14,s=62}
{x=336,m=328,a=316,s=90}
{x=3000,m=2576,a=641,s=1496}
{x=1776,m=1550,a=2392,s=3202}
{x=258,m=2128,a=1461,s=2472}
{x=1809,m=3126,a=229,s=1998}
{x=1276,m=1687,a=1011,s=370}
{x=1242,m=2380,a=441,s=568}
{x=1167,m=1268,a=2426,s=582}
{x=2297,m=530,a=3041,s=1552}
{x=1591,m=1077,a=2912,s=132}
{x=277,m=1836,a=1167,s=936}
{x=52,m=1460,a=583,s=695}
{x=430,m=1688,a=2448,s=3157}
{x=1081,m=472,a=226,s=848}
{x=47,m=433,a=2006,s=438}
{x=2480,m=835,a=1494,s=2003}
{x=2777,m=1473,a=1758,s=630}
{x=1891,m=2570,a=619,s=2146}
{x=174,m=694,a=2139,s=1763}
{x=18,m=510,a=2333,s=95}
{x=835,m=1516,a=337,s=1334}
{x=77,m=485,a=196,s=233}
{x=1256,m=229,a=812,s=914}
{x=1721,m=1056,a=499,s=4}
{x=923,m=779,a=189,s=119}
{x=204,m=434,a=449,s=131}
{x=1711,m=324,a=359,s=780}
{x=568,m=273,a=439,s=366}
{x=1311,m=284,a=1193,s=110}
{x=556,m=558,a=1829,s=2438}
{x=3526,m=1254,a=32,s=1720}
{x=361,m=632,a=932,s=436}
{x=1779,m=1496,a=2657,s=3344}
{x=74,m=133,a=2256,s=959}
"""
main(input)
