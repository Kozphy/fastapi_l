from attrs import define


@define
class Base:
    url_schema: str
    username: str
    password: str
    host: str
    port: str

    @classmethod
    def from_config(cls, attris, **config):
        basic_config = {k: v for k, v in config.items() if k in attris}
        return cls(**basic_config)
