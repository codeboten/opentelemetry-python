README
======

These files are basically the same example but mixing the storage mechanisms of
`threading` and `asyncio`.

Run all of these files. Notice that only `async_local.py` displays a different,
incorrect output. This happens because `threading.local` does not work
correctly with `asyncio`. That is why `contextvars` was created. Since the
opposite (`threading` with `contextvars`) does work, that means that
`contextvars` can be used in both situations, with `threading` and with
`asyncio` in the application code.

The original approach to this issue was to use `threading.local` as a fallback
option if `contextvars` was not available (`contextvars` was introduced in
3.7). This can be a problem for all the Python versions that came before 3.7
and support `asyncio`. This is the first problem. Can this be fixed with some
kind of backport of `contextvars` into the older versions? In the worst
scenario, can we at least raise a proper exception if a error of this kind
happens?

The second problem can come with other concurrency models, like Tornado (is
this statement true?). I think that this means that the Context itself needs to
be handled with entry points too. In this way a new package that introduces a
new concurrency model can introduce its own Context implementation. This
approach also makes it necessary to introduce some configuration capability to
context propagation so that the application user can let OpenTelemetry which
Context is necessary for the application code (can this detection be performed
automatically?).
