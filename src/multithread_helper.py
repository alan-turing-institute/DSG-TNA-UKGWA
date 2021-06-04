import concurrent.futures
import itertools


def grouper(iterable, n, fillvalue=None):
    """

    https://docs.python.org/3/library/itertools.html#itertools-recipes
    Collect data into fixed-length chunks or blocks
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def multi_threading(target, iterable, batch_size):
    """

    target - function to run
    iterable - iterable object to loop through
    batch_size - number of parallel threads to run
    """
    for batch in grouper(iterable, batch_size):
        # print(f'batch {batch}')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = (executor.submit(lambda arg: target(arg) if arg else None, item) for item in batch)
            for fut in concurrent.futures.as_completed(results):
                fut.result()
