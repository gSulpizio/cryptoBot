def sell_condition(df):
    """
    Checks if selling conditions are met for the SMA.

    Args:
        df (dataframe): containing long_avg and short_avg.

    Returns:
        Boolean.
    """
    n=len(df)-1
    short_avg = df["short_avg"][n]
    long_avg = df["long_avg"][n]
    pshort_avg = df["short_avg"][n - 1]
    plong_avg = df["long_avg"][n - 1]
    if short_avg < long_avg and pshort_avg > plong_avg:
        return True
    else:
        return False

if __name__ == "__main__":
    from initialize import initialize
    df=initialize()
    print(sell_condition(df))
