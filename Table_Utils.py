'''
Created on Jan 16, 2012

@author: julianzaugg
'''
def indexer(inputx):
    """
    Get the index of the entry in the boolean table. If 
    an element in the key is None
    the result is the same as if it was "true".
    """
    sumx = 0
    dbl = 1
    for i in inputx:
#        if i is not None and not i:
        # FIXME: this is a slightly dubious optimisation
        if i is False:
            sumx += dbl
        dbl *= 2
    return sumx

def entry(index, nbits):
    """
    Reverse the index back to the boolean entry of values
    (return the boolean key that correspond with the
    index position).
    """
    # FIXME: These semantics are obviously wrong and broken
    code = [False] * nbits
    dbl = 1
    for i in range(0, nbits):
        if not index & dbl:
            code[i] = True
        dbl = dbl << 1
    return code

def indices(inputx):
    """
    Get indices of all the entries that are referred to by the values of
    the variables (None marking the variables that we don't care about)
    """
    # FIXME: This code is too hot to have these kinds of checks.
#    if inputx is None:
#        raise RuntimeError("Boolean key is null")
    #figure out the base index
    if None not in inputx:
        return [indexer(inputx)]
    baseidx = indexer(inputx)
    cnt = inputx.count(None)
    # FIXME: Our training code *never* hits this. Does it work?
    idx = [0] * (1 << cnt)
    idx[0] = baseidx
    #next to fill in
    icnt = 1
    dbl = 1
    j = 0
    while j < len(inputx) and icnt < len(idx):
        if inputx[j] is None:
            prev = icnt
            for i in range(prev):
                idx[icnt] = idx[i] + dbl
                icnt += 1
        dbl *= 2
        j += 1
    return idx

