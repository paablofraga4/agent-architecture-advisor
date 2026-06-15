import nest_asyncio

# python run_chainlit.py run app.py --port 8081

def _noop_apply(*args, **kwargs):
    return None


# Chainlit CLI applies nest_asyncio unconditionally. On Python 3.14 this can
# break AnyIO backend detection, so we neutralize it before importing chainlit.cli.
nest_asyncio.apply = _noop_apply

from chainlit.cli import cli


if __name__ == "__main__":
    cli(prog_name="chainlit")
