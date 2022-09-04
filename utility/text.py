
def sanitize(txt: str | list[str]) -> str | list[str]:
    """
    Cleans up the provided text so that
    otherwise messy, unformatted text can
    be better-read by something like a nn
    """
    pass


def trim_stems(txt: str | list[str]) -> str | list[str]:
    """
    Trims the sometimes-unnecessary
    stems / endings off of words.

    This is really useful for NLPs

    Example:
    "application" -> "applic"
    "source code" -> "sourc cod"
    ...
    """
    pass
