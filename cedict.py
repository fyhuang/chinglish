import collections
import itertools

trad_to_ent = collections.defaultdict(lambda: [])
simp_to_ent = collections.defaultdict(lambda: [])
eid_to_ent = {}

all_simp = []
all_simp_chars = set()
all_trad = []
all_trad_chars = set()
pinyin_ents = []

class DictEntry(object):
    def __init__(self, eid, simp, trad, pinyin, eng):
        self.eid = eid
        self.simp = simp
        self.trad = trad
        self.pinyin = pinyin
        self.eng = eng

        py_lst = self.pinyin.split()
        self.tones = [0 for p in py_lst]
        for i,p in enumerate(py_lst):
            if p[-1].isdigit():
                self.tones[i] = int(p[-1])

def load_dict(filename):
    def invalid_line(l):
        print("Invalid line: {}".format(l))

    with open(filename) as f:
        num_lines = 0
        for line in f:
            if line[0] == '#': continue
            num_lines += 1
            #if num_lines > 10: break
            if num_lines % 10000 == 0:
                print("Loaded", num_lines, "lines")

            lb_ix = line.find(' [')
            if lb_ix == -1:
                invalid_line(line)
                continue
            chinese = line[:lb_ix]

            chinese_sp = chinese.split(' ')
            if len(chinese_sp) != 2:
                invalid_line(line)
                continue
            trad = chinese_sp[0]
            simp = chinese_sp[1]

            if len(trad) != len(simp):
                invalid_line(line)
                continue

            #print("trad: {}, simp: {}".format(trad, simp))

            rb_ix = line.find(']')
            pinyin = line[lb_ix+2:rb_ix]

            sl_ix = line.find('/')
            if sl_ix == -1:
                invalid_line(line)
                continue
            english = line[sl_ix+1:]

            #print("def: ", first_def)

            # Add to dictionary
            eid = num_lines
            entry = DictEntry(eid, simp, trad, pinyin, english)
            trad_to_ent[trad].append(entry)
            simp_to_ent[simp].append(entry)
            eid_to_ent[eid] = entry

            pinyin_ents.append((pinyin, entry))

            all_trad.append(trad)
            all_simp.append(simp)

            for c in trad:
                all_trad_chars.add(c)
            for c in simp:
                all_simp_chars.add(c)

    all_trad.sort()
    all_simp.sort()
    pinyin_ents.sort(key=lambda x: x[0])


def get_entry_by_eid(eid):
    return eid_to_ent[eid]

def get_entries(chars):
    if chars in trad_to_ent:
        results = trad_to_ent[chars]
    results = simp_to_ent[chars]

    # TODO: proper ranking
    results.sort(key=lambda x: x.pinyin[0].isupper())
    return results

def entries_with_prefix(prefix):
    lst = all_simp
    for c in prefix:
        if c not in all_simp_chars:
            lst = all_trad
            print("Trad")
            break

    try:
        results = []
        ix = next(i for i,x in enumerate(lst) if x.startswith(prefix))
        while lst[ix].startswith(prefix):
            results += get_entries(lst[ix])
            ix += 1
        return results
    except StopIteration:
        return []

def entries_with_pinyin(in_pinyin):
    in_pinyin = in_pinyin.replace('v', 'u:').strip()
    if len(in_pinyin) == 0:
        return []

    in_py_list = in_pinyin.split()
    # TODO: handle more exotic input
    ch_max = 100 # TODO
    if len(in_py_list) == 1:
        ch_max = 1

    def py_matches(py):
        py_list = py.split()
        for i,p in enumerate(in_py_list):
            if i >= len(py_list):
                return False

            pp = py_list[i].lower()
            ipp = p.lower()
            if not (pp == ipp or ipp == pp[:-1]):
                return False
        return True

    # TODO: this is a crude optimization
    try:
        start = next(i for i,(py,e) in enumerate(pinyin_ents) if py[0] == in_pinyin[0])
    except StopIteration:
        return []

    results = []
    for ix in range(start, len(pinyin_ents)):
        (py,e) = pinyin_ents[ix]
        if py_matches(py) and len(e.simp) <= ch_max:
            results.append(e)
    return results
    #return [e for e in itertools.islice(results, 100)]

def get_compounds(chars):
    results = []
    for k,v in simp_to_ent.items():
        if chars in k:
            results += v
    return results



def old_entries_with_prefix(prefix):
    # binary search?
    def bs_prefix(begin, end):
        mid = int((begin + end)/2)
        entry = lst[mid]
        print("Searching {}-{}, mid={}, entry={}".format(begin,end,mid,entry))
        if entry.startswith(prefix):
            return mid
        if begin == end:
            return None

        ent_pf = entry[:len(prefix)]
        if ent_pf > prefix:
            return bs_prefix(begin, mid-1)
        else:
            return bs_prefix(mid+1, end)

    #ix = bs_prefix(0, len(lst)-1)
    #if ix is None: return []
    #return [lst[ix]]
    results = []
    for e in lst:
        if e.startswith(prefix):
            results.append(e)
    return results
