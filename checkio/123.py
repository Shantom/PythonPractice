def checkio(data)
    # type: (object) -> object
    """

    :type data: object
    """
    data.sort()
    print(len(data) // 2)
    if 1 == len(data) % 2:
        rsl = data[len(data) // 2]
    else:
        rsl = 0.5 * (data[len(data) // 2 - 1] + data[len(data) // 2])
    # replace this for solution
    return rsl


# These "asserts" using only for self-checking and not necessary for auto-testing

print(checkio([2, 1, 3, 4, 6, 5]))
