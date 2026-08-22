# Gate 2′ — environment and resource report

## Доступность

Пилот полностью локален. Не нужны:

- blockchain node;
- RPC;
- mainnet/testnet;
- внешний dataset;
- SMT/model-checking service;
- GPU;
- network access во время воспроизведения;
- third-party Python runtime packages.

## Зафиксированная среда

- CPython 3.13.5;
- Linux x86_64;
- `PYTHONHASHSEED=0` для документированной deterministic environment;
- uv 0.10.0 использован как вспомогательный environment tool;
- pytest 9.0.2 использован дополнительно;
- authoritative self-check написан только на Python standard library.

Machine-readable environment записан в `results/pilot/environment.json`.

## Upstream snapshot

Semantic extraction основана на `relab/hotstuff` branch head, зафиксированном официальной commit page как `3179c6e62929294961acbfd9bf8445769716a121` на дату проверки. Локальные source files имеют отдельные SHA-256 в `source_manifest.csv`.

## Воспроизведение

```bash
./scripts/reproduce.sh
```

Скрипт:

1. очищает `results/reproduction`;
2. заново исчерпывающе строит все языки;
3. запускает stdlib self-check;
4. при наличии запускает pytest;
5. побайтово сравнивает deterministic result core с baseline.
