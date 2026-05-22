# Terminology answer key - heavy-translation (English -> Spanish)

This is the canonical key the scoring Architect uses to score CONSISTENCY and FIDELITY
of the translation. It is NOT given to the variants. The variants receive only the
prompt (in the spec) plus `corpus/heavy-translation/source-en.md`.

The scoring axis is: did the model render each technical term the SAME way every time
it appears across all 10 sections (consistency), and did it choose a defensible
technical rendering (fidelity), while leaving every code block, command, configuration
key, field name, and identifier UNCHANGED?

Translation has more than one defensible rendering for many terms. The key therefore
lists, per term, the ACCEPTED renderings (any one is fine) and the requirement that
WHICHEVER rendering the model picks, it must use that SAME rendering on every
occurrence. A model that translates "partition" as "particion" in Section 1 and
"division" in Section 7 has failed consistency even if both words are individually
defensible. The occurrence counts below let the Architect verify a term was rendered
consistently across the whole document.

---

## A. Glossary terms - accepted renderings + occurrence count

Format: source term | accepted Spanish renderings (pick one, use it everywhere) | approx
occurrences in source.

| English source term | Accepted Spanish rendering(s) | ~occurrences |
|---------------------|-------------------------------|--------------|
| stream | flujo (preferred); "stream" left as-is also acceptable IF used consistently | many (15+) |
| record | registro | many (20+) |
| key | clave | many (10+) |
| value | valor | many (8+) |
| timestamp | marca de tiempo; "timestamp" acceptable if consistent | 2 |
| headers | encabezados; cabeceras | 3 |
| partition | particion | many (20+) |
| partition count | numero de particiones; recuento de particiones | 3 |
| offset | desplazamiento; "offset" acceptable if consistent | many (12+) |
| log-start offset | desplazamiento de inicio del registro | 4 |
| log-end offset | desplazamiento de fin del registro | 5 |
| producer | productor | many (15+) |
| consumer | consumidor | many (20+) |
| consumer group | grupo de consumidores | many (8+) |
| partition assignment | asignacion de particiones | 3 |
| rebalance | reequilibrio; rebalanceo | many (8+) |
| committed offset | desplazamiento confirmado | 5 |
| commit | confirmacion (noun) / confirmar (verb) | many (10+) |
| reset policy | politica de reinicio | 3 |
| broker | broker (left as-is, preferred - it is a product term); "agente"/"intermediario" acceptable if consistent | many (15+) |
| cluster | cluster (left as-is, preferred); "agrupacion" acceptable if consistent | many (10+) |
| controller | controlador | 4 |
| leader | lider | many (8+) |
| follower | seguidor; replica seguidora | many (6+) |
| in-sync replica set | conjunto de replicas sincronizadas | many (8+) |
| acknowledged / acknowledgement | confirmado / confirmacion (of a write); "reconocido"/"reconocimiento" acceptable if consistent | several |
| acknowledgement level | nivel de confirmacion; nivel de reconocimiento | 3 |
| replication factor | factor de replicacion | 4 |
| retention policy | politica de retencion | 3 |
| time-based retention | retencion basada en tiempo | 1 |
| log-compaction | compactacion de registro | 1 |
| repartitioning hazard | riesgo de reparticionamiento; peligro de reparticionamiento | 2 |
| delivery guarantee | garantia de entrega | several |
| at-most-once delivery | entrega como maximo una vez | 1 (+heading) |
| at-least-once delivery | entrega al menos una vez | 1 (+heading) |
| exactly-once delivery | entrega exactamente una vez | several |
| idempotent producer | productor idempotente | 3 |
| transactional write | escritura transaccional | 3 |
| durable write | escritura duradera | 1 |
| fail-fast durability | durabilidad de fallo rapido | 1 |
| bootstrap address | direccion de arranque; direccion de bootstrap | 1 |
| batches | lotes | several |
| partitioner | particionador | 3 |
| backoff | retroceso; "backoff" acceptable if consistent | 1 |
| schema registry | registro de esquemas | 3 |
| compatibility policy | politica de compatibilidad | 2 |
| backward compatibility | compatibilidad hacia atras | 2 |
| forward compatibility | compatibilidad hacia adelante | 2 |
| full compatibility | compatibilidad total | 1 |
| breaking change | cambio incompatible; cambio disruptivo | 1 |
| schema identifier | identificador de esquema | 1 |
| metrics | metricas | 2 |
| replica lag | retraso de replica; "lag de replica" acceptable if consistent | 3 |
| out-of-sync replica | replica desincronizada | 2 |
| consumer lag | retraso del consumidor; "lag del consumidor" acceptable if consistent | 4 |
| heartbeat | latido; "heartbeat" acceptable if consistent | 1 |
| leader election | eleccion de lider | 3 |
| unclean leader election | eleccion de lider sucia; eleccion de lider no limpia | 3 |
| partition reassignment | reasignacion de particiones | 2 |
| cluster-wide slowdown | ralentizacion de todo el cluster | 1 |
| transport encryption | cifrado de transporte; encriptacion de transporte | 1 |
| mutual TLS | TLS mutuo (TLS stays as-is) | 1 |
| token-based mechanism | mecanismo basado en tokens | 1 |
| principal | principal (identity term, left as-is preferred) | 3 |
| access-control rule | regla de control de acceso | 3 |
| operation | operacion | 2 |
| deny-by-default posture | postura de denegacion por defecto | 2 |
| idempotent-write permission | permiso de escritura idempotente | 2 |
| idempotent (processing) | idempotente | several |
| rebalance storm | tormenta de reequilibrio; tormenta de rebalanceo | 1 |

---

## B. STRUCTURAL INVARIANTS (these are scored as Format adherence + Correctness, hard requirements)

The model must preserve ALL of the following EXACTLY. Any change here is a fidelity
error, and changing a code identifier is the equivalent of breaking the document.

1. **Code blocks unchanged.** There are THREE fenced code blocks of commands/code:
   - the `nwstream-admin create-stream` command block (Section 2)
   - the `nwstream-admin describe-stream` command block (Section 2)
   - the Python `Producer` example (Section 4)
   - the Python `Consumer` example (Section 5)
   That is FOUR fenced code blocks total. Every line inside each MUST be byte-identical
   to the source. Comments, string literals, keyword arguments, and values are NOT
   translated. (E.g. `value_serializer="json"` stays exactly so; `group_id=
   "order-processor"` stays exactly so.)

2. **Inline code / identifiers unchanged.** Every backticked token stays verbatim:
   `cleanup.policy=delete`, `cleanup.policy=compact`, `retention.ms`, `acks=0`,
   `acks=1`, `acks=all`, `linger_ms`, `batch_size`, `retries`, `group_id`,
   `auto_offset_reset`, `earliest`, `latest`, `enable_auto_commit`, `timeout_ms`,
   `orders`, `nwstream`, `bootstrap_address`, `key_serializer`, `value_serializer`,
   `enable_idempotence`, `key_deserializer`, `value_deserializer`. None of these are
   translated.

3. **Section headings preserved in count and order.** 10 numbered top-level sections
   (## 1 through ## 10), in the same order, each present. Heading TEXT is translated;
   the NUMBER and the count are preserved. Sub-bullets within sections preserved.

4. **Stream/field names unchanged.** `orders`, `customer-1187`, `order_id`, `55012`,
   `amount_cents`, `4999`, `trace_id`, `abc-123`, `9092`, broker hostnames
   `broker1`/`broker2`, `604800000` - all unchanged.

5. **Fictional product name unchanged.** "Northwind Stream" stays "Northwind Stream"
   (it is a proper product name). The COMMON NOUN "stream" elsewhere is translated per
   the glossary; the PRODUCT NAME is not.

6. **No content dropped.** All 10 sections, all bullets, all paragraphs present in the
   translation. A model that summarises a section instead of translating it has failed
   Completeness. The output should be roughly the same length as the source (Spanish
   typically runs 15-25% longer than English prose - that expansion is expected and is
   NOT a fault).

7. **No content added.** The model must not insert translator notes, explanations, or
   extra sections inside the document body. (The output envelope appended at the very end
   is required and is separate from the document body.)

---

## C. Scoring shorthand for the Architect

- **Consistency check (the primary discriminator):** pick ~12 high-frequency terms from
  Section A (stream, record, partition, offset, producer, consumer, broker, leader,
  follower, commit, rebalance, in-sync replica set). For each, scan ALL occurrences in
  the translation and verify the SAME rendering is used every time. One term rendered
  two different ways across sections = a consistency miss. This is the eval-22 mechanism
  applied to translation: under the volume of a long document, weaker models drift in
  their term choices; a strong model locks a term once and reuses it.

- **Fidelity check:** are the chosen renderings defensible technical Spanish (Section A
  accepts a range), and are the four code blocks + all inline identifiers byte-identical?
  A model that translated a code keyword, a config key, or a field name has a Correctness
  miss (it broke the document).

- **Completeness check:** all 10 sections present, nothing summarised away, nothing
  added. Count missing or summarised sections explicitly.

- **Correctness (hard-fail eligible):** translating a code block / identifier / config
  key (breaks the document), OR rendering a load-bearing technical term with the WRONG
  meaning (e.g. translating "at-least-once" as "at-most-once", or "backward
  compatibility" as "forward compatibility" - a meaning inversion), is a Correctness
  failure. A meaning inversion on a delivery guarantee or a compatibility policy is the
  worst case and is confidently-wrong.

- **Hallucination (hard-fail eligible):** inventing a term, a section, or a code line
  that is not in the source.

Suggested numeric shorthand: consistency_score = (terms rendered consistently) / 12 on
the sampled high-frequency terms; identifier_integrity = (code blocks + inline
identifiers left verbatim) - any single broken identifier drops Correctness. An exemplary
5 on Correctness keeps every identifier verbatim, inverts no meaning, and locks every
high-frequency term to one rendering across all 10 sections.
