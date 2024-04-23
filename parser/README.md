# parser

This is a quick script which tries to parse PDF tables from https://www.ssps.cz/zajemci/kriteria-prijimaciho-rizeni-2/vysledky-prijimaciho-rizeni-pro-skolni-rok-2022-2023/
to SQLite database that is then used by our backend.

How to use:

1. Download table you want to transform into machine-readable format.
2. Transform it into CSV format (for example with [this site](https://convertio.co/pdf-csv/))
3. Go to backend and install its dependencies with `poetry install --only main` (see https://python-poetry.org/docs/#installation)
4. Run `poetry shell` to activate virtual environment.
5. Use `poetry run python -m src /path/to/csv/table YEAR FIELD_OF_STUDY /path/to/result/dir`

    `YEAR` must be an integer and `FIELD_OF_STUDY` must be also hardcoded to `backend/src/strawberry/scheme.py`.
    If you call script like this `poetry run python -m src data/IT_PR_23_v3.csv 2023 it ../backend/data`
    it will output all data to `../backend/data/database.db` to table `year2023it`.
6. Profit!
