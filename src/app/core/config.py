import environ


@environ.config(prefix="")
class AppConfig:
    @environ.config(prefix="API")
    class API:
        host = environ.var()
        title = environ.var()
        version = environ.var()
        prefix = environ.var()
        debug = environ.bool_var()
        allowed_hosts = environ.var()

    @environ.config(prefix="DB")
    class DB:
        username = environ.var()
        password = environ.var()
        host = environ.var()
        port = environ.var(converter=int)
        name = environ.var()
        pool_size = environ.var(converter=int, default=100)
        max_overflow = environ.var(converter=int, default=20)
        echo = environ.bool_var(default=False)
        future = environ.bool_var(default=True)

        @property
        def url(self):
            return (
                f"postgresql://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}"
            )

        @property
        def async_url(self):
            return (
                f"postgresql+asyncpg://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}"
            )

    env = environ.var()
    adresse_api_url = environ.var()

    api: API = environ.group(API)
    db: DB = environ.group(DB)


CONFIG: AppConfig = AppConfig.from_environ()  # type: ignore
