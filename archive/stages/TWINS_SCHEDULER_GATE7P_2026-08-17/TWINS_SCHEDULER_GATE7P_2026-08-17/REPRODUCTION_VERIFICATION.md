# Gate 7′ clean-copy reproduction verification

**Дата проверки:** 17 августа 2026 года  
**Статус:** **PASS**

## Проверяемый сценарий

Исходное дерево было упаковано в ZIP, распаковано в новый каталог и запущено
только из распакованной копии. Перед упаковкой отсутствовали compiled Z3 loader,
Python caches и build directories. После распаковки выполнена команда:

```bash
./scripts/reproduce_gate7p.sh
```

Runner не использует package managers, Git, HTTP clients, RPC endpoints,
blockchain nodes или external datasets.

## Среда

```text
Linux 6.18.35 x86_64
CPython 3.13.5
Go 1.23.2
cc 14.2.0
Z3 runtime 4.13.3.0 via libz3.so.4
PYTHONHASHSEED=0
```

## Проверенные результаты

| Проверка | Результат |
|---|---:|
| Gate 6′ byte equivalence | 15/15 files |
| Positive SMT/CHC source files | 5 |
| Positive solver outcomes | 8 `UNSAT` |
| Damaged controls | 4/4 `SAT` |
| Unit tests | 17/17 PASS |
| Premise assignments | 128/128, 0 mismatches |
| Parameter cases | 512 PASS |
| Go big-integer cases | 1 028 PASS |
| Go/Python event-loop cases | 6/6 exact matches |
| Event-order case runs | 1 548, 0 classification changes |
| Generated paper assets | 24/24 |
| Core manifest | PASS |
| Full artifact manifest | PASS |
| Process exit status | 0 |

## Наблюдавшиеся ресурсы

GNU `time -v` для reference clean-copy run сообщил:

```text
elapsed wall clock: 0:06.48
user CPU: 8.16 s
system CPU: 1.28 s
maximum resident set: 113 372 KiB
major page faults: 12
minor page faults: 301 513
file-system outputs: 25 160
socket messages sent: 0
socket messages received: 0
swaps: 0
```

Эти числа описывают одну среду и не являются обещанием производительности.

## Выходные markers

```text
CORE EVIDENCE PASS
SMT PROOF MIGRATION PASS
PAPER ASSETS PASS
UNIT TESTS PASS (17)
GATE 7' SELF-CHECK PASS
CORE MANIFEST PASS
ARTIFACT MANIFEST PASS
GATE 7' REPRODUCTION PASS
```

## Ограничение проверки

Clean-copy reproduction подтверждает детерминированность и самодостаточность
пакета на указанной среде. Она не заменяет external human proof review, не
доказывает full-client refinement и не проверяет переносимость на произвольные
версии Python, Go, compiler или Z3.
