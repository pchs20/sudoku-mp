import itertools
from typing import Optional

from pyomo.environ import ConcreteModel, SolverFactory, SolverStatus
from pyomo.opt.results import SolverResults


class Solver:
    def __init__(self, concrete_model: ConcreteModel):
        self.concrete_model: ConcreteModel = concrete_model
        self._solution: Optional[SolverResults] = None

    def solve(self) -> None:
        solver = SolverFactory('scip')
        self._solution = solver.solve(self.concrete_model, tee=True)

    def solution_exists(self) -> bool:
        solution_found = (
            self._solution.solver.status == SolverStatus.ok or
            self._solution.solver.status == SolverStatus.warning
        )
        return solution_found

    def print_solution(self) -> None:
        assert self.solution_exists(), 'The solver did not find any solution!'

        n = int(self.concrete_model.n.value)
        grid_size = int(self.concrete_model.rows.last())

        for i in range(1, grid_size + 1):
            if i % n == 1 and i != 1:
                print('-' * (4 * grid_size + n + 1))

            for j in range(1, grid_size + 1):
                if j % n == 1 and j != 1:
                    print('|', end=' ')

                printed = False
                for v in range(1, grid_size + 1):
                    if self.concrete_model.place_value_square[i, j, v].value:
                        print(v, end=' ')
                        printed = True
                        break
                if not printed:
                    print(' ', end=' ')
            print()
