from pyomo.environ import (
    AbstractModel,
    Binary,
    Constraint,
    Param,
    RangeSet,
    Var,
)
from pyomo.core.expr.relational_expr import EqualityExpression


def get_abstract_model() -> AbstractModel:
    model = AbstractModel(name='sudoku')

    # Parameters: Values that you know prior to solving the problem, and will not change
    # during the execution.
    model.n = Param(
        name='size',
        doc='Size of the problem, i.e. number of subgrids per dimension.',
        initialize=3,
    )

    n_value = 3

    # Sets: Indexes for parameters, variables and other sets.
    model.rows = RangeSet(
        0, n_value**2 - 1,
        name='rows',
        doc='Set of rows of the Sudoku grid.',
    )

    model.columns = RangeSet(
        0, n_value**2 - 1,
        name='columns',
        doc='Set of columns of the Sudoku grid.',
    )

    model.rows_subgrid = RangeSet(
        0, n_value - 1,
        name='rows_subgrid',
        doc='Group of rows taking into account the subgrids.',
    )

    model.columns_subgrid = RangeSet(
        0, n_value - 1,
        name='columns_subgrid',
        doc='Group of columns taking into account the subgrids.',
    )

    model.grid_values = RangeSet(
        1, n_value**2,
        name='values',
        doc='Allowed values in each square of the grid.',
    )

    # Variables: Values defined while solving the problem to get the best solution.
    model.place_value_square = Var(
        model.rows,
        model.columns,
        model.grid_values,
        name='place_value_square',
        doc='Binary variable: 1 if value is placed, 0 otherwise.',
        domain=Binary,
    )

    # Constraints: Requirements and forbidden actions to achieve a correct solution.
    model.constraint_value_used_once_per_row = Constraint(
        model.rows,
        model.grid_values,
        name='value_used_once_per_row',
        doc=constraint_value_used_once_per_row.__doc__,
        rule=constraint_value_used_once_per_row,
    )

    model.constraint_value_used_once_per_column = Constraint(
        model.columns,
        model.grid_values,
        name='value_used_once_per_column',
        doc=constraint_value_used_once_per_column.__doc__,
        rule=constraint_value_used_once_per_column,
    )

    model.constraint_values_used_once_per_subgrid = Constraint(
        model.rows_subgrid,
        model.columns_subgrid,
        model.grid_values,
        name='values_used_once_per_subgrid',
        doc=constraint_values_used_once_per_subgrid.__doc__,
        rule=constraint_values_used_once_per_subgrid,
    )

    model.constraint_one_value_per_square = Constraint(
        model.rows,
        model.columns,
        name='one_value_per_square',
        doc=constraint_one_value_per_square.__doc__,
        rule=constraint_one_value_per_square,
    )

    # Objective: Function of variables that returns a value to be maximized or minimized.
    # There is no function to maximize or minimize, as one solution is no “better” than
    # another. Each solution that fulfills all the constraints is equally valid/optimal.
    # model.objective_function = 0

    return model


# Constraints definition
def constraint_value_used_once_per_row(
        model: AbstractModel,
        row: int,
        value: int,
) -> EqualityExpression:
    """In a row, each value must be used exactly once."""
    values_per_row = (
        sum(model.place_value_square[row, column, value] for column in model.columns)
    )
    return values_per_row == 1


def constraint_value_used_once_per_column(
        model: AbstractModel,
        column: str,
        value: str,
) -> EqualityExpression:
    """In a column, each value must be used exactly once."""
    values_per_row = (
        sum(model.place_value_square[row, column, value] for row in model.rows)
    )
    return values_per_row == 1


def constraint_values_used_once_per_subgrid(
        model: AbstractModel,
        row_subgrid: int,
        column_subgrid: int,
        value: int,
) -> EqualityExpression:
    """In a subgrid, each value must be used exactly once."""
    n = model.n.value
    values_per_subgrid = (
        sum(
            model.place_value_square[i, j, value]
            for i in range(row_subgrid * n, (row_subgrid + 1) * n)
            for j in range(column_subgrid * n, (column_subgrid + 1) * n)
        )
    )
    return values_per_subgrid == 1


def constraint_one_value_per_square(
        model: AbstractModel,
        row: int,
        column: int
) -> EqualityExpression:
    """Each square must have exactly one value."""
    values_per_square = (
            sum(
                model.place_value_square[row, column, value]
                for value in model.grid_values
            )
    )
    return values_per_square == 1
