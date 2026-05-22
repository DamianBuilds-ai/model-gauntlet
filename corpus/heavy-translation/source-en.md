# Northwind Stream - Developer Reference (Source, English)

Northwind Stream is a distributed message-streaming platform used by Acme, Globex,
Initech, and Umbra to move event data between services. This reference describes the
data model, the delivery guarantees, the client libraries, the operational tooling,
and the troubleshooting procedures. All product names, company names, and people in
this document are fictional.

This document is the SOURCE for a translation task. It is deliberately long and uses a
fixed technical vocabulary - the same terms recur in many sections and must be rendered
consistently throughout the whole translation. Code blocks, command-line examples,
configuration keys, field names, and identifiers must be preserved exactly and never
translated.

---

## 1. Concepts and data model

Northwind Stream organises data into **streams**. A stream is an append-only, ordered
log of **records**. Each record has a **key**, a **value**, a **timestamp**, and an
optional set of **headers**. Records are never modified once written; the log is
immutable.

A stream is divided into **partitions**. A partition is the unit of parallelism and
ordering: records within a single partition are strictly ordered, but there is no
ordering guarantee across partitions. The number of partitions in a stream is fixed at
creation time and is called the **partition count**.

Each record in a partition is assigned a monotonically increasing integer called the
**offset**. The offset uniquely identifies a record within its partition. The lowest
available offset in a partition is the **log-start offset**; the offset one past the
last written record is the **log-end offset**.

A **producer** is a client that writes records into a stream. A **consumer** is a
client that reads records from a stream. A group of cooperating consumers that share
the work of reading a stream is called a **consumer group**. Within a consumer group,
each partition is assigned to exactly one consumer; this assignment is called the
**partition assignment**, and the act of recomputing it is a **rebalance**.

A consumer tracks its progress by storing the offset of the next record it intends to
read. This stored position is the **committed offset**, and the act of saving it is a
**commit**. When a consumer restarts, it resumes from its committed offset. If no
committed offset exists, the consumer starts from the position dictated by its
**reset policy** (either the log-start offset or the log-end offset).

A **broker** is a server process that stores partitions and serves producers and
consumers. A set of brokers that work together is a **cluster**. One broker in the
cluster is elected the **controller**; the controller manages cluster-wide metadata and
coordinates rebalances.

Each partition is replicated across several brokers for durability. The broker that
owns the authoritative copy of a partition is the **leader** for that partition; the
other copies are **followers**. The set of followers that are sufficiently caught up to
the leader is the **in-sync replica set**. A write is considered **acknowledged** once
it is persisted on the required number of replicas, governed by the **acknowledgement
level** (see Section 3).

---

## 2. Stream lifecycle and administration

Streams are created, configured, and deleted through the **admin client** or the
command-line **administration tool**. The following example creates a stream named
`orders` with twelve partitions and a replication factor of three:

```
nwstream-admin create-stream \
  --name orders \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config cleanup.policy=delete
```

The **replication factor** is the number of copies of each partition the cluster
maintains. It must be less than or equal to the number of brokers. A replication factor
of three means one leader and two followers.

The **retention policy** controls how long records are kept. Two cleanup policies are
supported:

- `cleanup.policy=delete` - records older than `retention.ms` are deleted. This is the
  **time-based retention** mode.
- `cleanup.policy=compact` - the platform keeps only the latest record for each key and
  discards older records with the same key. This is the **log-compaction** mode, useful
  for changelog-style streams where only the latest value per key matters.

A stream can be reconfigured after creation, but the partition count can only be
increased, never decreased. Increasing the partition count changes how keys map to
partitions, so it can disturb ordering for in-flight keys; the documentation calls this
the **repartitioning hazard**.

To inspect a stream, use the describe command:

```
nwstream-admin describe-stream --name orders
```

This prints the partition count, the replication factor, the leader for each partition,
the in-sync replica set for each partition, and the configured retention policy.

---

## 3. Delivery guarantees

Northwind Stream offers three **delivery guarantees**, selected per producer and per
consumer-group configuration.

**At-most-once delivery** means each record is delivered zero or one times. A record may
be lost but is never duplicated. This is achieved by committing the offset before
processing the record. It has the lowest latency and the weakest guarantee.

**At-least-once delivery** means each record is delivered one or more times. A record is
never lost but may be duplicated if a consumer fails after processing but before
committing. This is achieved by committing the offset after processing the record. It is
the default guarantee.

**Exactly-once delivery** means each record is delivered and processed exactly once,
even across failures. This is achieved by combining an **idempotent producer** (which
de-duplicates retried writes using a producer identifier and a sequence number) with a
**transactional write** that atomically commits the produced records and the consumed
offsets together. Exactly-once delivery has the highest overhead and the strongest
guarantee.

The producer controls durability through the acknowledgement level:

- `acks=0` - the producer does not wait for any acknowledgement. Lowest latency, highest
  risk of loss.
- `acks=1` - the producer waits for the leader to persist the record. The record can
  still be lost if the leader fails before a follower replicates it.
- `acks=all` - the producer waits for every member of the in-sync replica set to
  persist the record. This is the **durable write** setting and the only one safe to
  combine with exactly-once delivery.

When `acks=all` is combined with a minimum in-sync replica setting, a write fails fast
if too few replicas are available rather than silently accepting a record that could be
lost. The documentation calls this **fail-fast durability**.

---

## 4. The producer client

A producer is created from a configuration object and is thread-safe. The minimal
configuration requires the cluster address (the **bootstrap address**) and the
serialisers for the key and the value.

```python
from nwstream import Producer

producer = Producer(
    bootstrap_address="broker1:9092,broker2:9092",
    key_serializer="string",
    value_serializer="json",
    acks="all",
    enable_idempotence=True,
)

producer.send(
    stream="orders",
    key="customer-1187",
    value={"order_id": 55012, "amount_cents": 4999},
    headers={"trace_id": "abc-123"},
)
producer.flush()
```

Records are buffered in the producer and sent in **batches** to improve throughput. The
`linger_ms` setting controls how long the producer waits to accumulate a batch before
sending; a higher value increases throughput at the cost of latency. The `batch_size`
setting caps the size of a single batch in bytes.

A producer assigns each record to a partition using a **partitioner**. The default
partitioner hashes the record key, so records with the same key always land in the same
partition and therefore preserve their relative order. A record with a null key is
distributed across partitions in a round-robin fashion. A custom partitioner can be
supplied to override this behaviour.

If a send fails with a retriable error - such as a leader election in progress - the
producer retries automatically up to `retries` times, with an exponential **backoff**
between attempts. A non-retriable error - such as a record larger than the maximum
message size - fails immediately and is surfaced to the caller.

When idempotence is enabled, the producer attaches a producer identifier and a
per-partition sequence number to every record, so the broker can detect and discard a
duplicate caused by a retry. This makes retries safe without producing duplicates.

---

## 5. The consumer client

A consumer subscribes to one or more streams and reads records in a poll loop. The
consumer belongs to a consumer group named by the `group_id` setting.

```python
from nwstream import Consumer

consumer = Consumer(
    bootstrap_address="broker1:9092,broker2:9092",
    group_id="order-processor",
    key_deserializer="string",
    value_deserializer="json",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)

consumer.subscribe(["orders"])

while True:
    records = consumer.poll(timeout_ms=1000)
    for record in records:
        handle(record.key, record.value)
    consumer.commit()
```

The `auto_offset_reset` setting is the reset policy: `earliest` resumes from the
log-start offset when no committed offset exists, `latest` resumes from the log-end
offset. It applies only when there is no committed offset; it never overrides an
existing committed offset.

Offset committing has two modes. With **automatic commit** (`enable_auto_commit=True`),
the consumer commits the latest polled offsets on a fixed interval in the background.
This is convenient but can lead to duplicate processing after a failure, because an
offset may be committed for a record that was not fully processed. With **manual
commit** (`enable_auto_commit=False`), the application commits explicitly after
processing, which is required for at-least-once and exactly-once delivery.

A consumer can commit synchronously or asynchronously. A **synchronous commit** blocks
until the broker confirms the commit and retries on failure; it is safe but slower. An
**asynchronous commit** returns immediately and does not retry, so it is faster but can
leave the committed offset behind after a transient failure. A common pattern is to use
asynchronous commits during normal operation and a single synchronous commit on
shutdown.

When a member joins or leaves a consumer group, the controller triggers a rebalance and
recomputes the partition assignment. During a rebalance, consumers stop reading until
the new assignment is in place. A long rebalance is a common cause of a consumer
appearing to stall.

---

## 6. Schema management

To keep producers and consumers compatible as data evolves, Northwind Stream integrates
with a **schema registry**. The schema registry stores a versioned schema for the key
and the value of each stream and enforces a **compatibility policy** when a new schema
version is registered.

Three compatibility policies are supported:

- **Backward compatibility** - a consumer using the new schema can read records written
  with the previous schema. This permits deleting a field or adding an optional field.
- **Forward compatibility** - a consumer using the previous schema can read records
  written with the new schema. This permits adding a field or deleting an optional
  field.
- **Full compatibility** - both backward and forward compatibility hold simultaneously.
  This permits only adding or deleting optional fields.

A schema change that violates the configured compatibility policy is rejected at
registration time, before any incompatible record can be written. The documentation
calls this a **breaking change** and recommends a two-phase rollout (deploy readers that
understand the new schema first, then deploy writers) to avoid one.

Each record carries a small **schema identifier** rather than the full schema, so the
serialised payload stays compact. The consumer fetches the schema by identifier from
the registry and caches it locally.

---

## 7. Operations and monitoring

Operators monitor a cluster through **metrics** exported by every broker. The most
important health signal is **replica lag**: the number of records by which a follower
trails its leader. A follower whose lag exceeds a threshold is removed from the in-sync
replica set and is then said to be an **out-of-sync replica**. Sustained lag indicates a
slow or overloaded broker.

The second key signal is **consumer lag**: the difference between the log-end offset of
a partition and the committed offset of a consumer group on that partition. Growing
consumer lag means the consumer group is falling behind the producers. Consumer lag is
the primary signal for deciding whether to scale out a consumer group.

When a broker fails, the controller detects the failure through a missed **heartbeat**
and triggers a **leader election** for every partition that broker led. A new leader is
chosen from the in-sync replica set. If the in-sync replica set is empty, the partition
becomes unavailable until a replica recovers, unless **unclean leader election** is
explicitly enabled - which allows an out-of-sync replica to become leader at the cost of
possibly losing records. Unclean leader election is disabled by default.

To rebalance load across brokers, an operator can trigger a **partition reassignment**,
which moves partition replicas from one broker to another. Reassignment copies data in
the background and is throttled to avoid saturating the network. The documentation warns
that an un-throttled reassignment is a frequent cause of a **cluster-wide slowdown**.

---

## 8. Security

Northwind Stream secures traffic with **transport encryption** and authenticates
clients with one of two mechanisms: **mutual TLS** (each client presents a certificate)
or a **token-based mechanism** (each client presents a signed token). Authentication
establishes the **principal** - the identity of the client.

Authorisation is governed by **access-control rules**. Each rule grants or denies a
principal a specific **operation** (read, write, create, delete, describe) on a specific
resource (a stream, a consumer group, or the whole cluster). By default, no principal
has any permission; every permission must be granted explicitly. The documentation calls
this the **deny-by-default posture**.

A common misconfiguration is granting write permission on a stream but forgetting to
grant the producer the **idempotent-write permission** required when idempotence is
enabled. The producer then fails at startup with an authorisation error rather than a
configuration error, which the troubleshooting section addresses.

---

## 9. Troubleshooting

**The producer hangs on send.** The most common cause is that `acks=all` is set but the
in-sync replica set is smaller than the minimum in-sync replica setting, so no write can
be acknowledged. Check the in-sync replica set for the target partition with the
describe command. Resolution: restore enough replicas, or, only if data loss is
acceptable, lower the minimum in-sync replica setting.

**The consumer processes the same record twice.** This is expected under at-least-once
delivery after a failure between processing and commit. If duplicates are unacceptable,
move to exactly-once delivery (idempotent producer plus transactional write) or make the
processing **idempotent** so that re-processing the same record has no additional effect.

**The consumer stalls and consumer lag grows.** Three frequent causes: a long rebalance
triggered by members joining and leaving repeatedly (a **rebalance storm**); a single
slow record-handler blocking the poll loop; or a partition whose leader is on an
overloaded broker. Inspect the rebalance history and the per-partition replica lag to
distinguish them.

**Records arrive out of order.** Ordering is only guaranteed within a partition. If
records that should be ordered land in different partitions, the cause is usually a null
key (round-robin distribution) or a partition-count increase that changed the key-to-
partition mapping (the repartitioning hazard). Resolution: ensure related records share
a non-null key and avoid changing the partition count on an ordered stream.

**The producer fails immediately with an authorisation error.** The principal lacks a
required permission. Recall the deny-by-default posture: every operation must be granted
explicitly, including the idempotent-write permission when idempotence is enabled. Grant
the missing access-control rule.

**A partition is unavailable after a broker failure.** Its in-sync replica set was empty
at the time of the leader election, so no in-sync replica could be promoted. The
partition stays unavailable until a replica recovers. Enabling unclean leader election
would restore availability at the risk of losing records; this is a deliberate
durability-versus-availability trade-off, not a default.

---

## 10. Summary of guarantees

Northwind Stream gives strict ordering within a partition, durability through
replication and the acknowledgement level, and a choice of three delivery guarantees.
The strongest configuration - `acks=all` with fail-fast durability, an idempotent
producer, a transactional write, and manual synchronous commits - provides exactly-once
delivery at the cost of latency and throughput. The default configuration -
at-least-once delivery with `acks=all` and manual commits - is the recommended starting
point for most services, with idempotent processing on the consumer to absorb the
occasional duplicate.
