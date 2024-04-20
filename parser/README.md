# parser

This is a quick script which tries to parse PDF tables from https://www.ssps.cz/zajemci/kriteria-prijimaciho-rizeni-2/vysledky-prijimaciho-rizeni-pro-skolni-rok-2022-2023/
to SQLite database that is then used by our backend.

How to use:

1. Download table you want to transform into machine-readable format.
2. Transform it into CSV format (for example with [this site](https://convertio.co/pdf-csv/))
3. Install dependencies with `poetry install --only main` (see https://python-poetry.org/docs/#installation)
4. Use `poetry run python -m src /path/to/csv/table tablename /path/to/result/db` (script will write result to table, name of which is provided as second argument)
5. Profit!
