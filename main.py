import random

from GA_utils import GA_utils


class Solver_8_queens:
    __pop_size = 0
    __cross_prob = 0.50
    __mut_prob = 0.25

    def __init__(self, pop_size=100, cross_prob=0.8, mut_prob=0.1):
        self.__pop_size = pop_size
        self.__cross_prob = cross_prob
        self.__mut_prob = mut_prob

    def solve(self, min_fitness=0.9, max_epochs=100):
        b_fit = 0
        e_num = 1
        vis = None
        GA_utils.cross_probability = self.__cross_prob
        GA_utils.mutation_probability = self.__mut_prob
        limit = max_epochs
        ds = GA_utils.generate_population(self.__pop_size)
        # for i in range(limit):
        i = 0
        while i < limit if limit is not None else True:
            ds = GA_utils.select_best_population(ds)
            random.shuffle(ds)
            ds = GA_utils.cross(ds)
            ds = GA_utils.mutate(ds)
            best = GA_utils.find_best(ds, min_fitness)
            f_f = GA_utils.fitness_func(best)
            if b_fit < f_f:
                b_fit = f_f
                e_num = i + 1
                vis = best.print_desk()
            if min_fitness is not None and f_f >= min_fitness:
                return b_fit, e_num, vis
            i += 1
        return b_fit, e_num, vis


if __name__ == "__main__":
    solver = Solver_8_queens(pop_size=100)
    best_fit, epoch_num, visualization = solver.solve(max_epochs=100, min_fitness=0.9)
    print("Best solution:")
    print("Fitness:", best_fit)
    print("Iterations: ", epoch_num)
    print(visualization)


