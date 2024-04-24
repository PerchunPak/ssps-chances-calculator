# ssps-chances-calculator

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://war.ukraine.ua/support-ukraine/)

Calculator for your chances to get into https://ssps.cz!

Smichov secondary technical school (SSPS) is secondary school in Prague with huge focus on IT. It is
a really good school, so it is hard to get there. In order to calculate my chances, I created this
website. You can also download underlying database and run your own scripts (e.g. to generate some
graphs or statistics). Feel free to share your conclusions with me!

## How does it work?

Everyone is able to look at exam results [here](https://www.ssps.cz/zajemci/kriteria-prijimaciho-rizeni-2/vysledky-prijimaciho-rizeni-pro-skolni-rok-2022-2023/).
However tables for results are as PDF tables, which is not readable for a robot at all.

In order to make results hackable, I transformed all tables to CSV format (see [here](#CSV-tables)
for a link) and then created a script, that transforms those CSV tables to SQLite database.

You can download SQLite database on the site - https://ssps-calc.perchun.it!

### CSV tables

If you want to get clean tables, without parsing done by me, here are CSV tables that I used as
a source of information:

- 2023
  - IT:
    [PDF](https://www.ssps.cz/wp-content/uploads/2023/05/IT_PR_23_v3.pdf)
    [CSV](https://files.perchun.it/ssps/2023it.csv)

    CSV sha256sum: f8e4a840b9a15306d5f37484e342d75f101f79a85c082650f132a74e229f909a

## Thanks

This project was generated with [svelte-template](https://github.com/PerchunPak/svelte-template).
