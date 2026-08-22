# Gate 7′ final ZIP reproduction verification

**Дата:** 17 августа 2026 года  
**Статус:** **PASS**

## Проверенный архив

- файл: `TWINS_SCHEDULER_GATE7P_2026-08-17.zip`;
- SHA-256: `43576dbb7f516e2aed6b4109a4ca0d44fe9b26653798f234f624b2af5f39a0ef`;
- compressed size: 233961 bytes;
- archive integrity: `unzip -t` — PASS;
- entries: 165.

## Метод

Архив распакован в новый пустой каталог. Из распакованной копии выполнена
команда:

```bash
./scripts/reproduce_gate7p.sh
```

После выполнения дополнительно проверены оба frozen manifests:

```bash
sha256sum -c CORE_RESULTS.sha256
sha256sum -c ARTIFACT_MANIFEST.sha256
```

## Итог

| Проверка | Результат |
|---|---:|
| Final ZIP extraction | PASS |
| Gate 6′ byte equivalence | 15/15 |
| Positive SMT/CHC outcomes | 8/8 `UNSAT` |
| Damaged negative controls | 4/4 `SAT` |
| Unit tests | 17/17 PASS |
| Premise assignments | 128/128, 0 mismatches |
| Parameter cases | 512 PASS |
| Go big-integer cases | 1 028 PASS |
| Go/Python event-loop conformance | 6/6 |
| Event-order runs | 1 548, 0 changes |
| Generated paper assets | 24/24 |
| Core manifest | PASS |
| Full artifact manifest | PASS |
| Exit status | 0 |

## Наблюдавшиеся ресурсы финального ZIP-run

```text
elapsed wall clock: 6.51 s
user CPU: 8.23 s
system CPU: 1.53 s
maximum resident set: 113 624 KiB
major page faults: 11
minor page faults: 301 543
swaps: 0
socket messages sent: 0
socket messages received: 0
```

Результаты подтверждают самодостаточность и детерминированность packaged route
на зафиксированной среде. Они не заменяют independent human proof review и не
являются full-client refinement proof.
