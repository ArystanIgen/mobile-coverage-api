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

    env = environ.var()

    api: API = environ.group(API)


CONFIG: AppConfig = AppConfig.from_environ()

