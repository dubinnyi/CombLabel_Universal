from classes.constants import PatternClass, Constants
import copy


ITERATION_4_OUTPUT = 10000


class CLOptimizer:

    def __init__(self, parameters, logger):
        self.solution_found = False
        self.logger = logger
        self.samples = parameters["samples"]
        self.optimize_price = parameters["optimize_price"]
        self.iteration = 0
        self.residues2label = []
        self.final_depth = len(self.residues2label)
        self.solutions = 0
        self.solution = Solution(None)
        self.back_up_solutions = []
        self.counter = [0]
        self.depth = 0
        self.symmetry = [self.samples]

    def run(self):
        while not self.solution_found:
            self.find_solution()
            self.samples += 1

    def find_solution(self):
        self.back_up_solutions = []
        self.counter = [0]
        self.depth = 0
        self.generate_residues2label()
        self.create_patterns_codes()
        self.create_solution()
        self.main_cycle()

    def main_cycle(self):
        while True:
            self.next_iteration()

            if self.depth == 0 and self.counter[0] > self.solution.residues[0].patterns_number():
                break

            self.back_up_solutions.append(self.solution.copy())


            if not len(self.residues2label) and self.solution.good:

                if self.optimize_price:
                    pass
                else:
                    pass
                self.solutions += 1

            if self.solution.found and samples_number != self.solution.samples_num:
                break


    def next_iteration(self):
        self.iteration += 1
        # some output

    def go_deeper(self):
        # choose residue with smallest number of patterns
        # add counter
        # depth ++
        pass

    def go_parallel(self):
        # take back-upped scheme
        # pop back-upped scheme
        # counter ++
        pass

    def go_back(self):
        # depth --
        #

    def create_solution(self):
        pass

    def generate_residues2label(self):
        #make a set of residues
        #make residues after and before
        #check good or bad
        #cross out nitrogen patterns
        #if needed calculate prices
        #make labeling array
        #for each residue2label convert patterns to codes
        all_patterns = set().union(*[res.patterns_set for res is self.residues2label])
        all_patterns_list = list(all_patterns)


        self.label_list = sorted(self.label_set, key=lambda word: [alphabet[c] for c in word])


        patterns_codes = PatternsCodes(all_patterns_list)
        self.solution = Solution(patterns_codes)
        pass

    def create_patterns_codes(self):
        pass


class Residue2Label:

    def __init__(self, name, ncs, samples, label_options, residues_after, residues_before):
        self.name = name
        self.samples = samples
        self.pattern_price = dict()
        self.residues_after = residues_after
        self.residues_before = residues_before
        self.patterns_list = []
        self.patterns_codes = []
        self.label_options = label_options

        self.has_15n = False
        for label in label_options:
            if label in Constants.NITRO_TYPES:
                self.has_15n = True
                break

        self.labeling_prices = dict()
        self.patterns_set = self._generate_initial_set(self.samples)
        self._cross_out_N_power(ncs)


    def _generate_initial_set(self, samples):
        # recursive function, that generates all possible combinations
        # of labels given the number of samples for the given residue

        if samples == 0:
            new_set = set()
            new_set.add("")
            return new_set
        current_set = self._generate_initial_set(samples - 1)
        new_set = set()
        for item in current_set:
            for option in self.label_options:
                new_set.add(item + option)
        return new_set

    def _cross_out_N_power(self, ncs):
        if not self.has_15n:
            return
        cross_out_set = set()
        for pattern in self.patterns_set:
            if not self.check_N_power(pattern, ncs):
                cross_out_set.add(pattern)
        self.patterns_set = self.patterns_set.difference(cross_out_set)

    def check_N_power(self, pattern, ncs):
        max_pairs = 1
        got_nitro = False
        for label in pattern:
            max_pairs *= ncs.label_power[label]
            if label in Constants.NITRO_TYPES:
                got_nitro = True
        return got_nitro and max_pairs >= len(self.residues_after)


    def cross_out(self):
        pass

    def patterns_number(self):
        return len(self.patterns_list)

    def cross_out_symmetry(self, symmetry):
        for pattern_code


class PatternsCodes:

    def __init__(self, patterns, ncs):
        pattern_class = PatternClass()
        self.ncs = ncs
        self.pattern_strings = patterns
        self.code_strings = []
        self.simplified_strings = [pattern_class.simplify_pattern(pattern) for pattern in patterns]
        self.simplified_strings_unique = []
        self.map_code_to_int = {}
        self.map_pattern_to_int = {}
        self.map_simplified_to_int = {}
        self.codeint_2D = []
        self._create_codes_table()

        patternint=0
        for p in self.pattern_strings:
            self.map_pattern_to_int[p] = patternint
            patternint = patternint + 1

        simpleint=0
        for simpl in self.simplified_strings:
            if simpl not in self.map_simplified_to_int:
                self.map_simplified_to_int[simpl] = simpleint
                self.simplified_strings_unique.append(simpl)
                simpleint = simpleint + 1
        self.nsimple = simpleint

    # C-style
    def _create_codes_table(self):
        n = len(self.pattern_strings)
        self.codeint_2D = [[None in range(n)] in range(n)]
        codeint = 0
        for i in range(n):
            pattern1 = self.pattern_strings[i]
            for j in range(n):
                pattern2 = self.pattern_strings[j]
                code_string = self.ncs.calc_code(pattern1, pattern2)
                if code_string in self.map_code_to_int:
                    codeint = self.map_code_to_int[code_string]
                else:
                    codeint = codeint + 1
                    self.map_code_to_int[code_string] = codeint
                    self.code_strings.append(code_string)
                self.codeint_2D[i][j] = codeint

    def calc_code_fast(self, pattern_int1, pattern_int2):
        return self.codeint_2D[pattern_int1][pattern_int2]

    def convert_pattern_to_int(self, pattern_string):
        return self.map_pattern_to_int[pattern_string]

    def convert_int_to_pattern(self, pattern_int):
        return self.pattern_strings[pattern_int]

    def convert_int_to_simple(self, simple_int):
        return  self.simplified_strings_unique[simple_int]

    def convert_simple_to_int(self, simple_string):
        return  self.map_simplified_to_int[simple_string]

    def convert_int_to_code(self, code_int):
        return self.code_strings[code_int]

    def convert_code_to_int(self, code_string):
        return self.map_code_to_int[code_string]


class Solution:

    def __init__(self, patterns_codes):
        self.patterns_codes = patterns_codes
        self.patterns = []
        self.residues = []
        self.codes = set()
        self.price = 0
        self.new_codes = set()

    def try_label(self, pattern_code, residue):
        self.new_codes = set()
        if residue.name in residue.residues_after:
            self.new_codes.add(self.patterns_codes.codes[pattern_code][pattern_code])
        for i in range(len(self.residues)):
            res = self.residues[i]
            if res.name in residue.residues_after:
                new_code = self.patterns_codes.codes[pattern_code][self.patterns[i]]
                if new_code in self.codes or new_code in self.new_codes:
                    return False
                else:
                    self.new_codes.add(new_code)
            if res.name in residue.residues_before:
                new_code = self.patterns_codes.codes[self.patterns[i]][pattern_code]
                if new_code in self.codes or new_code in self.new_codes:
                    return False
                else:
                    self.new_codes.add(new_code)
        return True

    def add_label(self, pattern_code, residue):
        self.codes.update(self.new_codes)
        self.new_codes = set()
        self.patterns.append(pattern_code)
        self.residues.append(residue)
        self.price += residue.pattern_price[pattern_code]



