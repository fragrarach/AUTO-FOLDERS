from quatro import sql_query, tabular_data, configuration as c


# Pull all 'ord_no' records from 'order_header' table
def all_ord_nos():
    sql_exp = f'SELECT ord_no FROM order_header'
    result_set = sql_query(sql_exp, c.config.sigm_db_cursor)
    ord_nos = tabular_data(result_set)
    return ord_nos


def all_cli_nos():
    sql_exp = f'SELECT cli_no FROM client'
    result_set = sql_query(sql_exp, c.config.sigm_db_cursor)
    cli_nos = tabular_data(result_set)
    return cli_nos


def all_sup_nos():
    sql_exp = f'SELECT sup_no FROM supplier'
    result_set = sql_query(sql_exp, c.config.sigm_db_cursor)
    sup_nos = tabular_data(result_set)
    return sup_nos
