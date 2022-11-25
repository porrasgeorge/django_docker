
def str2bool(v):
    if v.lower() in ("true", "t", "1"):
        return 1
    elif v.lower() in ("false", "f", "0"):
        return 0
    else:
        return -1
