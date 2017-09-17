from .numeric import Numeric

class SHAUNPP(object):
    def __init__(self, shaun, indent_symbol='  '):
        self.shaun = shaun
        self.indent_symbol = indent_symbol
        self.indent_level = 0

    def print(self, to_print):
        lst = [ (lambda x: isinstance(x, (list, tuple)), self.print_list)
              , (lambda x: isinstance(x, dict), self.print_object)
              , (lambda x: isinstance(x, bool), self.print_bool)
              , (lambda x: isinstance(x, (int, float, Numeric)), self.print_numeric)
              , (lambda x: x is None, self.print_null)
              , (lambda x: isinstance(x, str), self.print_string) ]

        for (cond, f) in lst:
            if cond(to_print):
                return f(to_print)

    def indent(self):
        return self.indent_level * self.indent_symbol

    def print_list(self, lst):
        self.indent_level = self.indent_level + 1
        ret = ('\n' + self.indent()).join(map(lambda e: self.print(e), lst))
        self.indent_level = self.indent_level - 1
        return '[\n' + ret + ' ]'

    def print_object(self, obj):

        self.indent_level = self.indent_level + 1
        ret = []
        for k, v in obj.items():
            ret.append(self.indent() + k + ':' + self.print(v))
        self.indent_level = self.indent_level - 1

        return self.indent() + '{\n' + '\n'.join(ret) + '\n' + self.indent() + '}'

    def print_numeric(self, num):
        return str(num)

    def print_bool(self, b):
        if b:
            return 'true'
        else:
            return 'false'

    def print_null(self, n):
        return 'null'

    def print_string(self, string):
        return '"' + self.escape(string) + '"'

    def escape(self, s):
        ret = ''
        escape = { '\t' : '\\t'
                 , '\n' : '\\n'
                 , '\r' : '\\r'
                 , '\d' : '\\d'
                 , '\f' : '\\f'
                 , '"'  : '\\"'
                 , '\\' : '\\\\' }
        for c in s:
            try:
                ret += escape[c]
            except:
                ret += c
        return ret

    def dump(self):
        return self.print(self.shaun)
