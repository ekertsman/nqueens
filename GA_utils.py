import random

from DeskSolution import DeskSolution


class GA_utils:
    cross_probability = 0.7
    mutation_probability = 0.05

    @classmethod
    def encode_dna(cls, desk):
        dna = ""
        for l in desk.lines:
            dna += "{0:0>3}".format(bin(l)[2:])
        return dna

    @classmethod
    def decode_dna(cls, dna):
        i = 0
        lines = []
        while i < len(dna):
            lines += [int(dna[i : i + 3], 2)]
            i += 3
        return DeskSolution(lines)

    @classmethod
    def generate_solution(cls):
        positions = list(range(8))
        random.shuffle(positions)
        lines = []
        for p in positions:
            lines += [p]
        ds = DeskSolution(lines)
        return ds

    @classmethod
    def select_best_population(cls, solutions):
        solutions_dict = dict()
        sum = 0
        for s in solutions:
            f_f = cls.fitness_func(s)
            sum += f_f
            solutions_dict.update({s: cls.fitness_func(s)})
        avg = sum / len(solutions)
        best_solutions = []
        result = []
        for s, f in solutions_dict.items():
            cnt = round(f / avg)
            best_solutions += [s] * cnt
        for i in range(len(solutions)):
            result += [random.choice(best_solutions)]
        return result

    @classmethod
    def generate_population(cls, cnt: int):
        ds = []
        for i in range(cnt):
            ds += [cls.generate_solution()]
        return ds

    @classmethod
    def fitness_func(cls, solution):
        no_intersections_count = 8
        for i in range(len(solution.lines)):
            if cls.count_intersections_vertical(solution, solution.lines[i], i) != 1:
                no_intersections_count -= 1
                continue
            # check diagonals
            if cls.count_intersections_diagonals(solution, solution.lines[i], i)  != 1:
                no_intersections_count -= 1
                continue
        return no_intersections_count / 8

    @classmethod
    def count_intersections_vertical(cls, solution, x, y):
        cnt = 0
        for i in range(len(solution.lines)):
            if x == solution.lines[i]:
                cnt += 1
        return cnt

    @classmethod
    def count_intersections_diagonals(cls, solution, x, y):
        cells = cls.get_diagonal_cells(x, y)
        cnt = 0
        for i in range(len(solution.lines)):
            if (solution.lines[i], i) in cells:
                cnt += 1
        return cnt

    @classmethod
    def get_diagonal_cells(cls, x, y):
        cells_to_check = set()
        for i in range(8):
            if x - i >= 0 and y - i >= 0:
                cells_to_check.update({(x - i, y - i)})
            if x + i < 8 and y + i < 8:
                cells_to_check.update({(x + i, y + i)})
            if x + i < 8 and y - i >= 0:
                cells_to_check.update({(x + i, y - i)})
            if x - i >= 0 and y + i < 8:
                cells_to_check.update({(x - i, y + i)})
        return cells_to_check

    @classmethod
    def cross(cls, ds):
        r = random.uniform(0, 1)
        random.shuffle(ds)
        new_gen = []
        for i in range(len(ds)//2):
            s1, s2 = ds[i], ds[0-i-1]
            if r < cls.cross_probability:
                dna1 = cls.encode_dna(s1)
                dna2 = cls.encode_dna(s2)
                cross_point = random.randrange(1, 8)
                res1 = "".join(dna1[:cross_point*3] + dna2[cross_point * 3:])
                res2 = "".join(dna2[:cross_point*3] + dna1[cross_point * 3:])
                new_gen += [cls.decode_dna(res1)]
                new_gen += [cls.decode_dna(res2)]
            else:
                new_gen += [s1]
                new_gen += [s2]
        return new_gen

    @classmethod
    def mutate(cls, ds):
        r = random.uniform(0, 1)
        new_gen = []
        for d in ds:
            rnd = r = random.uniform(0, 1)
            if rnd < cls.mutation_probability:
                dna = list(cls.encode_dna(d))
                k = int(random.randrange(len(dna)))
                dna[k] = str(1 - int(dna[k]))
                d = cls.decode_dna("".join(dna))
            new_gen += [d]
        return new_gen

    @classmethod
    def find_best(cls, ds, min_fitness: float):
        max_f = 0
        best = None
        for d in ds:
            f_f = cls.fitness_func(d)
            if max_f < cls.fitness_func(d):
                max_f = f_f
                best = d
            if min_fitness is not None and f_f >= min_fitness:
                return d
        return best