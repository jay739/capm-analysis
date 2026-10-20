# Contributing to capm-analysis

Thanks for considering a contribution. Issues, discussions and PRs are all
welcome.

## Getting set up

Python 3.10 or newer. `pip install -r requirements.txt`, then `jupyter notebook capm_analysis.ipynb` and run all cells.

## Running the checks

`pip install -r requirements.txt pytest` then `pytest -q tests`. The test runs every notebook cell offline against synthetic data. If you change the notebook, re-execute it so the committed outputs match the code.

## Ground rules

- Open an issue or discussion before large changes, so effort isn't wasted.
- Keep PRs focused: one change per PR.
- New behavior needs a test where the repo has a test suite.
- CI must pass before merge.

## Licensing

By contributing you agree your contributions are licensed under the repo's
MIT license.
