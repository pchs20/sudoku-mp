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
        grid_size = n ** 2

        for i in range(grid_size):
            if i % n == 0 and i != 0:
                print('-' * (2 * grid_size + n - 1))

            for j in range(grid_size):
                if j % n == 0 and j != 0:
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

        # Access the values of decision variables
        for i in self.concrete_model.rows:
            for j in self.concrete_model.columns:
                for k in self.concrete_model.grid_values:
                    if self.concrete_model.place_value_square[i, j, k].value:
                        print(f"Value {k} placed at row {i}, column {j}")
