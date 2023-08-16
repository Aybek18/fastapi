from re import sub


def pascal_case(value) -> str:
    value = sub(r"(_|-)+", " ", value).title().replace(" ", "")
    return ''.join([value[0:]])
