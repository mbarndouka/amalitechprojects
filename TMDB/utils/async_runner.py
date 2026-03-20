import asyncio
from concurrent.futures import ThreadPoolExecutor


# Shared executor used when bridging sync calls from an already-running event loop.
_ASYNC_BRIDGE_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tmdb-async-bridge")


def _run_coroutine_sync(coro):
    """Run a coroutine from sync code, even if an event loop is already active."""
    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    if running_loop.is_running():
        return _ASYNC_BRIDGE_EXECUTOR.submit(asyncio.run, coro).result()

    return running_loop.run_until_complete(coro)