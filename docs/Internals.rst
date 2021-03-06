Internals
*********

This section contains some details about some CMS internals. They're
mostly meant for developers, not for users. However, if you're curious
about what's under the hood, you'll find something interesting here
(though without any pretension of completeness). Moreover, these are
not meant to be full specifications, but only useful notes for the
future.

RPC protocol
============

Different CMS processes communicate between them by mean of TCP
sockets. Once a service has established a socket with another, it can
write messages on the stream; each message is a JSON-encoded object,
terminated by a ``\r\n`` string (this, of course, means that ``\r\n``
cannot be used in the JSON encoding: this is not a problem, since new
lines inside string represented in the JSON have to be escaped
anyway).

An RPC request must be of the form::

  {
    "__method": <name of the requested method>,
    "__data": {
                <name of first arg>: <value of first arg>,
                ...
              },
    "__id": <random ID string>
  }

The arguments in ``__data`` are (of course) not ordered: they have to
be matched according to their names. In particular, this means that
our protocol enables us to use a ``kwargs``-like interface, but not a
``args``-like one. That's not so terrible, anyway.

The ``__id`` is a random string that will be returned in the response,
and it is useful (actually, it's the only way) to match requests with
responses.

The response is of the form::

  {
    "__data": <return value or null>,
    "__error": <null or error string>,
    "__id": <random ID string>
  }

The value of ``__id`` must of course be the same as in the request.
If ``__error`` is not null, then ``__data`` is expected to be null.

Historical notes
----------------

In the past the RPC protocol used to be a bit more powerful, having
the ability of complement the JSON message with a blob of binary
data. This feature has been removed now, both because it was unused
and because its implementation actually has a subtle bug that caused
messages of a specific length to mess around with the ``\r\n``
terminator.
