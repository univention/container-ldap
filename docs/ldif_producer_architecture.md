# LDIF-Producer

The LDIF-Producer produces a provisioning message
for every LDAP write transaction (`ADD`, `DELETE`, `MODIFY`, `MODRDN`)
and pushes them into a NATS queue.

The messages are still in the LDAP Object representation.
A separate component is responsible for converting the Object
to it's UDM representation.

## High-level architecture

The LDIF-Producer combines two worlds.

The slapd-sock-server based on `socketserver`, which is itself `threading`-based.
And the official NATS python client library which is `asyncio`-based.

The socketserver main thread and the asyncio even loop
run in separate threads and are connected via the `outgoing_queue`
synchronous python queue.
The socketserver internally uses two additional python queues.
They will be explained later.

the ldif_producer.controller python module
configures and starts both components,
owns the `outgoing_queue` and initializes a graceful shutdown
via a `signal_handler`.

## slapd-sock-server

the LDIF-Producer hooks into the LDAP-Server
via the back-sock LDAP overlay module.
It provides Pre-Transaction and Post-Transaction hook capabilities
via a UNIX TCP Socket.
One problem with this approach is, that LDAP requests
can only be blocked in the Pre-hook (ADDRequset, DELETERequest, MODIFYRequest...)
and only the Post-hook (RESULTRequest)
provides the necessary LDAP object / LDIF data
to construct the provisioning message.

This leads to the requirements that:

1. the Post-hook must locally persist the message content as soon as possible.
2. The first action after startup must be to check the transaction journal
    and send any remaining messages to NATS.
3. A post-hook handler function must never be aborted before it persisted
    it's messages to the transaction journal.
4. modify requests need to be throtteled in the Pre-hook
    to not overload the downstream tasks.

Requirements one and two are not yet implemented
in the first alpha version of this component.
But it's already prepared in the `LDAPHandler.do_result()` function.
Requirement three is implemented via a signal_handler
that propagates an exit event to all threads and asyncio tasks
and careful tuning of the python queue and socket polling timeout
so that the exit event is evaluated with a reasonable frequency.
(about once per second)
Requirement four is implemented through a python `backpressure_queue`.
The pre-hooks add an object to the `backpressure_queue` for ever LDAP write request
and the post-hook removes an item after it has processed the request.
While processing the request, the message is added to the `outgoing_queue`.
That queue has a maximum size and blocks adding an item if it is reached.
Items are removed from the `outgoing_queue`
only after being successfully sent to NATS.
This way, a slow/unresponsive NATS
slows/stops the LDAP server from processing write requests.
The pre-hook waits for a configurable timeout
for a `backpressure_queue` seat to become available,
before cancelling the LDAP Request with a custom error:

```text
RESULT
code: 51
matched: <DN>
info: slapdsocklistener busy sending messages to the message queue\n
```

Code 51 = `LDAP_BUSY`

### Classes and threads

The LDIF-Producer acts as the UNIX Socket server
while the back-sock LDAP overlay module is the client.

The LdifProducerSlapdSockServer or rather it's parent classes
create and own the UNIX socket and the `requests` python queue.
It is instantiated in the main controller and executed
as a blocking and long-running process
in the socketserver main thread.
It listens for TCP requests on the socket and puts them into the `requests` queue.
The socketserver main thread also spawns worker threads
that consume the `requests` queue.

The logic for how to respond to back-sock hook requests
is defined in the LDAPHandler class and it's parents.
It is instantiated as a signleton,
owns and instantiates the `backpressure_queue`
and recieves a reference to the `outgoing_queue`
from the main controller.

## Performance Considerations

Multiple slapd-sock worker threads can and should be configured
to quickly respond to the LDAP-Server.

But the `backpressure_queue` is currently hard-coded to 1
This configuration means that many read requests
can be handeled concurrently, but only one write-request
can happen at a given time.
This choice was made because we currently don't know
how to preserve the message order
with multiple in-flight write transactions.

I expect that the bottleneck will be sending messages to NATS
but don't know how to parallelize this operation
without compromising the message order.

## Multi-Master LDAP-Server support

still under discussion.
We expect that queue deduplication by the NATS server
based on a unique transaction id
will do the heavy lifting.
