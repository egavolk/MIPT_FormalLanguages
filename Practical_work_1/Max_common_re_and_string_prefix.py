#ab+c.aba.*.bac.+.+* abacb
#ans = 5
#acb..bab.c.*.ab.ba.+.+*a. acbac
#ans = 5

class Edge:
    def __init__(self, to, symbol):
        self.to = to
        self.symbol = symbol

    def __repr__(self):
        return '(to : ' + str(self.to) + ', symbol : ' + str(self.symbol) + ' )'


class NFA:
    def __init__(self):
        self.g = {}
        self.counter = 0
        self.final = -1
        self.start = 0
        
    def __repr__(self):
        return str(g)


class SubNFA:
    def __init__(self, nfa, c):
        self.nfa = nfa
        self.start = self.nfa.counter
        self.nfa.g[self.nfa.counter] = [Edge(self.nfa.counter + 1, c)]
        self.nfa.g[self.nfa.counter + 1] = []
        self.final = self.nfa.counter + 1
        self.nfa.counter += 2

    def __iadd__(self, other):
        self.nfa.g[self.start].append(Edge(other.start, '-'))
        self.nfa.g[other.final].append(Edge(self.final, '-'))
        return self

    def __imul__(self, other):
        self.nfa.g[self.final].append(Edge(other.start, '-'))
        self.final = other.final
        return self

    def star(self):
        self.nfa.g[self.nfa.counter] = [Edge(self.start, '-'), Edge(self.nfa.counter + 1, '-')]
        self.nfa.g[self.final] += [Edge(self.nfa.counter + 1, '-'), Edge(self.start, '-')]
        self.nfa.g[self.nfa.counter + 1] = []
        self.start = self.nfa.counter
        self.final = self.nfa.counter + 1
        self.nfa.counter += 2
        return self


def make_nfa_from_re(a):
    st = []
    nfa = NFA();
    for symbol in a:
        if symbol in { 'a', 'b', 'c' }:
            st.append(SubNFA(nfa, symbol))
        elif symbol == '1':
            st.append(SubNFA(nfa, '-'))
        elif symbol == '+':
            if len(st) < 2:
                return None
            second = st.pop()
            first = st.pop()
            first += second
            st.append(first)
        elif symbol == '.':
            if len(st) < 2:
                return None
            second = st.pop()
            first = st.pop()
            first *= second
            st.append(first)
        elif symbol == '*':
            if len(st) < 1:
                return None
            first = st.pop()
            first = first.star()
            st.append(first)
        else:
            return None
    if len(st) > 1:
        return None
    nfa.start = st[0].start
    nfa.final = st[0].final
    return nfa


def dfs(g, used, v, symbol):
    if used[v]:
        return set()
    used[v] = True
    res = set()
    for edge in g[v]:
        if edge.symbol == '-':
            res |= dfs(g, used, edge.to, symbol)
        elif edge.symbol == symbol:
            res.add(edge.to)
    return res


def find_max_prefix_len(nfa, u):
    current_stages = [{ 0 }, set()]
    ans = 0
    for symbol in u:
        used = [False] * len(nfa.g)
        for stage in current_stages[0]:
            for edge in nfa.g[stage]:
                current_stages[1] |= dfs(nfa.g, used, stage, symbol)
        if not current_stages[1]:
            return ans
        ans += 1
        current_stages = [current_stages[1], set()]
    return ans


a, u = list(map(str, input().split()))
nfa = make_nfa_from_re(a)
if nfa is not None:
    print(find_max_prefix_len(nfa, u))
else:
    print('ERROR')
