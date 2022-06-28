from constants import DEFAULT_KEY_PREFIX
import ulid


def prefixed_key(f):
    """
    A method decorator that prefixes return values.
    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        base_key: list = f(*args, **kwargs)
        for i, v in enumerate(args):
            if i == 0:
                continue
            base_key.append(f"-{v}")

        id = ulid.new().str
        base_key.append(f":{id}")
        key = "".join(base_key)

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
    def product_key(self, *args, **kwargs) -> list:
        return ["product"]

    @prefixed_key
    def cache_key(self, *args, **kwargs) -> list:
        return ["cache"]


def make_keys() -> Keys:
    return Keys()
