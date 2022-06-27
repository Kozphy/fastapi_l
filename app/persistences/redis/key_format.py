from constants import DEFAULT_KEY_PREFIX


def prefixed_key(f):
    """
    A method decorator that prefixes return values.
    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        key = f(*args, **kwargs)
        # print(self.prefix)
        # print(key)
        return f"{self.prefix}:{key}"

    return prefixed_method


class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    # @prefixed_key
    # def timeseries_sentiment_key(self) -> str:
    #     """A time series containing 30-second snapshots of BTC sentiment."""
    #     return f"sentiment:mean:30s"

    # @prefixed_key
    # def timeseries_price_key(self) -> str:
    #     """A time series containing 30-second snapshots of BTC price."""
    #     return f"price:mean:30s"

    @prefixed_key
    def product_key(self, *args, **kwargs) -> str:
        return f"product.{args}"

    @prefixed_key
    def cache_key(self) -> str:
        return f"cache"


def make_keys():
    return Keys()
