import quatro


# Pull all 'ord_no' records from 'order_header' table
def all_ord_nos(config):
    sql_exp = f'SELECT ord_no FROM order_header'
    result_set = quatro.sql_query(sql_exp, config.sigm_db_cursor)
    ord_nos = quatro.tabular_data(result_set)
    return ord_nos


def all_cli_nos(config):
    sql_exp = f'SELECT cli_no FROM client'
    result_set = quatro.sql_query(sql_exp, config.sigm_db_cursor)
    cli_nos = quatro.tabular_data(result_set)
    return cli_nos
