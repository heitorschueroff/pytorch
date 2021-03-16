"""Define some common setup blocks which benchmarks can reuse.

Note that for `parse_stmts`:
  - Width for the left (Python) column MUST be 40 characters.
  - The column separator is " | ", not "|". Whitespace matters.
"""

import enum

from core.api import GroupedSetup
from core.utils import parse_stmts


_TRIVIAL_2D = GroupedSetup(
    r"x = torch.ones((4, 4))",
    r"auto x = torch::ones({4, 4});"
)


_TRIVIAL_4D = GroupedSetup(
    r"x = torch.ones((4, 4, 4, 4))",
    r"auto x = torch::ones({4, 4, 4, 4});"
)


_GENERIC = GroupedSetup(*parse_stmts(
    r"""
        Python                                   | C++
        ---------------------------------------- | ----------------------------------------
        torch.manual_seed(138_10_23)             | torch::manual_seed(1381023);
        x = torch.rand((4, 4))                   | auto x = torch::rand({4, 4});
        y_float = torch.ones((4, 4))             | auto y_float = torch::ones({4, 4});
        y_int = torch.ones(                      | auto y_int = torch::ones({4, 4}, at::kInt);
            (4, 4), dtype=torch.int32)           |
    """
))


_TRAINING = GroupedSetup(*parse_stmts(
    r"""
        Python                                   | C++
        ---------------------------------------- | ----------------------------------------
        # Inputs                                 | // Inputs
        x = torch.ones((1,))                     | auto x = torch::ones({1});
        y = torch.ones((1,))                     | auto y = torch::ones({1});
                                                 |
        # Weights                                | // Weights
        w0 = torch.ones(                         | auto w0 = torch::ones({1});
            (1,), requires_grad=True)            | w0.set_requires_grad(true);
        w1 = torch.ones(                         | auto w1 = torch::ones({1});
            (1,), requires_grad=True)            | w1.set_requires_grad(true);
        w2 = torch.ones(                         | auto w2 = torch::ones({2});
            (2,), requires_grad=True)            | w2.set_requires_grad(true);
    """
))


class Setup(enum.Enum):
    TRIVIAL_2D = _TRIVIAL_2D
    TRIVIAL_4D = _TRIVIAL_4D
    GENERIC = _GENERIC
    TRAINING = _TRAINING