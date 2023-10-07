# ---------
# Usage: p
# ---------


def calc_basket_window_size_secs(the_start_date, the_end_date):
    """Calculates a Basket's (time) window size"""
    return (the_end_date - the_start_date).dt.total_seconds()


def calc_programming_duration(the_start_time: int, the_end_time: int):
    """ Calcs a Programming item's duration """
    return the_end_time - the_start_time


def calc_prog_as_percent_of_basket(the_prog_duration, the_basket_size):
    """ Calc Program percent of Basket """
    return the_prog_duration / the_basket_size * 100
