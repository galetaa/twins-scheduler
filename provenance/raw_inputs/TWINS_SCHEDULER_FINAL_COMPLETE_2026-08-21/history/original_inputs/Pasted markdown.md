Да. Если исходить именно из текущего текста, я бы **не переделывал работу с нуля**. Центральный результат уже есть. Сейчас задача — закрыть несколько мест, по которым сильный рецензент может ударить.

Я бы расставил приоритеты так.

## 1. Самое главное: привязать центральную теорему к одному реальному BFT-протоколу

Это сейчас главный недостаток статьи.

В работе уже прямо написано, что для natural protocol instantiation необходимо отдельно доказать:

- что `enable` и `repair` действительно оказываются на одном scheduler edge;
- что repair действительно выводит pivot из будущего конфликтующего quorum;
- что repair приходит до второй certificate opportunity;
- что pivot действительно является необходимым;
- что его нельзя заменить другим honest contribution.

И в limitations вы сами фактически признаёте, что mapping пока conditional.

### Что конкретно добавить

Выбрать **один** протокол. Я бы не пытался сразу делать Tendermint + HotStuff + CometBFT. Лучше один, но хорошо.

Например, CometBFT/Tendermint.

Нужен отдельный раздел примерно:

**“Instantiation / Conformance to Tendermint-style locking”**

И таблица соответствия:

| Abstract modelРеальный protocol mechanism |                                                           |
| ----------------------------------------- | --------------------------------------------------------- |
| (p)                                       | конкретный validator                                      |
| (E)                                       | конкретное сообщение / certificate                        |
| (R)                                       | конкретное repair/commit/lock evidence                    |
| (C\_0)                                    | конкретная certificate opportunity                        |
| (C\_1)                                    | следующая conflict opportunity                            |
| `enabled`                                 | конкретный protocol predicate                             |
| `disabled`                                | lock/decision/state condition                             |
| shared edge                               | почему scheduler действительно не различает два сообщения |

Причём не обязательно находить настоящий production bug.

Можно получить результат вида:

> «Если в Tendermint-style transition system присутствует mutation `MISSING_LOCK_UPDATE`, то abstract quorum-pivot construction refinement-equivalent данному bounded execution».

Это уже гораздо сильнее, чем просто искусственно написанный event loop.

**Если вы сделаете только одно большое дополнение — делайте это.**

---

## 2. Я бы добавил промежуточную теорему между абстрактной моделью и Theorem 2

Сейчас есть немного неприятный скачок.

Сначала очень общий relational theorem.

Потом специально сконструированный protocol schema.

А хотелось бы иметь theorem примерно такого содержания:

> Любая certificate-driven locking system, удовлетворяющая условиям A–F quorum-pivot mechanism, допускает strict separation между phase-specific и type-uniform scheduling.

То есть не:

> «Вот конкретно наша модель».

А:

> **«Вот структурный критерий, по которому можно узнать этот эффект в любом протоколе».**

Сейчас часть этой идеи спрятана в тексте после Theorem 2 и затем в семи Boolean flags.

Я бы поднял её на уровень отдельного proposition/theorem.

Например:

**Quorum-Pivot Separation Criterion.**

Предпосылки:

1. существуют два conflicting certificate opportunities;
2. их honest support пересекается в необходимом pivot (p);
3. без (p) второй certificate имеет (q-1);
4. (E) делает участие (p) возможным;
5. (R) до (C\_1) делает его невозможным;
6. (E,R) имеют одинаковые sender/receiver/view, но разные phase;
7. (G\_T) различает их, (G\_D) — нет.

Тогда phase/type erasure не сохраняет unsafe observation.

Вот такой theorem сильно уменьшит впечатление **“engineered toy example”**.

А ваш нынешний (3f+1) construction станет чистым corollary/instantiation.

---

# 3. Есть конкретная формальная проблема в replay section — её надо исправить

Вот это я бы исправил **обязательно до подачи**.

Для replay theorem вы требуете:

- projection congruence для состояния;
- duplicate stutter;
- silent output duplicate;
- observation factors through (\pi).

Теорема затем корректно утверждает сохранение **final relevant projection и state-based observations**.

Но в proof появляется утверждение:

> silent output prevents an erased duplicate from changing the relevant output trace.

Этого в текущих premises недостаточно, если вы хотите равенство **всего output trace**.

Почему?

Пусть

[
\pi(s)=\pi(t),
]

но hidden states разные.

Projection congruence гарантирует, что после следующего сообщения их **projected states** останутся одинаковыми.

Но она не гарантирует:

[
\mathsf{out}(s,m)=\mathsf{out}(t,m).
]

То есть будущий retained event теоретически может выдать разные outputs из двух hidden states, даже если projections одинаковы.

### Есть два простых варианта исправления

Либо вообще убрать claim про output-trace preservation и оставить только:

> final projection + state-based observations.

Это уже полностью соответствует theorem statement.

Либо добавить ещё одну premise:

[
\pi(s)=\pi(t)
\Longrightarrow
\mathsf{out}(s,m)=\mathsf{out}(t,m)
]

для protocol-relevant output каждого retained event.

Тогда можно честно доказывать equality relevant output traces.

**Я бы сделал второй вариант**, потому что theorem станет красивее и завершённее.

---

# 4. Надо почистить определение `UnsafeObs`

Здесь есть формальная неаккуратность.

Ранее:

[
\mathsf{Unsafe}(s)
]

определена как predicate над **state**.

Но затем:

[
\mathsf{UnsafeObs}\_G(P,B)=
{O\_s(\tau)\mid \tau\in L\_G(P,B)\land \mathsf{Unsafe}(O\_s(\tau))}.
]

То есть `Unsafe` внезапно применяется к observation.

Математически читатель поймёт, что имеется в виду, но в formal paper это лучше не оставлять.

Я бы сделал явно:

[
\operatorname{last}(\tau)
]

— terminal state execution,

[
\operatorname{Obs}(\tau)=O(\operatorname{last}(\tau)).
]

И либо:

# [ \mathsf{UnsafeObs}\_G(P,B)

{
O(\operatorname{last}(\tau))
\mid
\tau\in L\_G(P,B)
\land
\mathsf{Unsafe}(\operatorname{last}(\tau))
},
]

либо отдельно определить `UnsafeObsPredicate` на (\Omega).

Это маленькая правка, но reviewer по formal methods её увидит.

---

# 5. Сделать scheduler semantics более формальными

Сейчас описание (G\_D), (G\_T), (G\_M) интуитивно понятное, но центральный результат **целиком зависит от точной семантики scheduler grammar**.

Поэтому я бы формализовал их буквально как функции/отношения.

Например:

[
A\_D(v,s,r)\in{0,1}
]

для directed grammar и

[
A\_T(v,\lambda,s,r)\in{0,1}
]

для phase-specific grammar.

И тогда type closure:

# [ C\_{\mathrm{type}}(A\_T)(v,s,r)

\bigvee\_{\lambda\in\Lambda} A\_T(v,\lambda,s,r).
]

После этого надо явно написать:

**closure не создаёт сообщение, которого protocol execution никогда не emitted.**

Она только меняет admission/delivery для уже существующего controlled envelope.

И отдельно определить:

- меняет ли closure порядок;
- когда именно доставляется newly admitted message;
- можно ли message задержать внутри view;
- доставляется ли оно ровно один раз;
- какие edges вообще находятся под scheduler control.

Сейчас closure описан словами как admission всех controlled phases на использованном edge.

Для центрального результата я бы сделал это mathematically exact.

---

# 6. Усилить statement Theorem 2 — прямо указать protocol и bounded domain

Сейчас общая нотация была:

[
\mathsf{UnsafeObs}\_G(P,B).
]

Но Theorem 2 записан просто:

[
\mathsf{UnsafeObs}*{G\_D}=\varnothing,*
*\qquad*
*\mathsf{UnsafeObs}*{G\_T}\neq\varnothing.
]

А это немного маскирует очень важную часть theorem:

**результат относится к конкретно построенному (P\_f) и конкретному bounded domain.**

Лучше писать что-то вроде:

[
\mathsf{UnsafeObs}\_{G\_D}(P\_f,B\_f)=\varnothing,
]

[
\mathsf{UnsafeObs}\_{G\_T}(P\_f,B\_f)\neq\varnothing.
]

И очень точно определить (B\_f).

Особенно:

> все остальные edges, message productions и phase orders фиксированы; единственная scheduler-controlled degree of freedom для (G\_D) — Boolean admission shared edge.

Тогда фраза:

> “these two values exhaust all (G\_D) executions”

становится абсолютно железной, а не выглядит как следствие того, что автор просто решил рассмотреть два executions.

---

# 7. Theorem 1 надо немного усилить формулировочно

Relational closure theorem хороший, но надо явно включить в statement:

[
C(\tau)\in L\_{G\_{\text{coarse}}}(P,B).
]

Иными словами:

> closure не просто создаёт какую-то sequence of actions; она создаёт **legal execution target grammar**.

Сейчас merged trace описана как trace, которая сохраняет оригинальные actions и вставляет closure-required actions.

Для чистой theorem этого хватает интуитивно, но для заявленного result про language preservation лучше связать её прямо с:

[
L\_{G\_T}
\quad\text{и}\quad
L\_{G\_D}.
]

Я бы разделил результат на:

**Lemma — Merged-trace preservation**

и

**Corollary — Scheduler closure preserves unsafe observation whenever (C(\tau)) is an admissible target execution.**

Так будет математически чище.

---

# 8. Proof Theorem 3 сейчас слишком короткий для слова “exact characterization”

У вас заявляется точная equivalence по всем 128 assignments:

[
\mathsf{Strict}
\iff
S\_2\land D\land T\land E\_d\land X\land(S\_1\lor R\_q).
]

А proof фактически:

> substitute and simplify; exhaustive kernel confirms it.

Это правда может быть достаточно, но я бы добавил в paper **само Boolean simplification**, хотя бы 5–10 строк.

То есть показать:

[
U(1,0)=...
]

[
\neg U(0,0)=...
]

[
\neg U(1,1)=...
]

и затем conjunction → closed form.

Тогда theorem действительно будет выглядеть самостоятельно доказанной на бумаге, а enumeration станет **cross-check**, а не почти часть доказательства.

---

# 9. Убрать странное двойное именование T1/T2/T3/T6

Сейчас читатель встречает:

> Theorem 1 (...; T2)

потом

> Theorem 2 (...; T3)

потом

> Theorem 3 (...; T6)

а потом

> Theorem 4 (...; T1).

Это внутренне понятно как IDs proof obligations, но внешнему читателю выглядит довольно странно.

Я бы **полностью убрал T1/T2/T3/T6 из основного текста**.

Пусть будут:

- Theorem 1;
- Theorem 2;
- Theorem 3;
- Theorem 4.

А в artifact manifest:

> theorem 1 ↔ proof obligation T2.

Рецензенту ваши внутренние номера не нужны.

---

# 10. Сделать и реально собрать Lean или Coq proof

Вот это второй по важности большой engineering task после real-protocol bridge.

Сейчас работа очень честно говорит:

> Lean и Coq sources есть, но compiler отсутствовал, поэтому они **не считаются mature-prover evidence**.

И затем ещё раз:

> mature prover build остаётся assurance limitation.

Это означает, что автор уже сам поставил reviewer’у красную стрелочку:

**«Вот здесь работа ещё не закончена».**

Надо её убрать.

Не надо обязательно поддерживать одновременно Lean и Coq.

Лучше:

**один реально собранный Lean project**

или

**один реально собранный Coq project**

с:

- pinned compiler version;
- dependency lock;
- one-command build;
- CI;
- archived output/hash.

После этого фраза `mature-prover build remains...` исчезает вообще.

Это довольно сильно повысит perceived rigor.

---

# 11. Go/Python tests уже достаточно. Больше random executions почти не нужно

Вот здесь я бы **не тратил время**.

У вас уже есть:

- Go implementation;
- independent Python implementation;
- FIFO;
- LIFO;
- 256 seeded random orders;
- 1,548 executions;
- одинаковая safety classification.

Если сделать 10 000 или 100 000 random executions, paper практически не станет сильнее.

Reviewer всё равно скажет:

> bounded testing doesn't prove arbitrary asynchronous behavior.

И будет прав.

Поэтому вместо ещё тысячи тестов я бы вложил время в **protocol conformance и proof**.

---

# 12. Семь Boolean flags оставить, но понизить их статус относительно центрального результата

Theorem 3 хороший, однако paper должен очень явно говорить:

> это exact characterization **конкретной seven-flag operational abstraction**, а не universal necessary-and-sufficient characterization всех locking protocols.

Вы это уже говорите.

Я бы просто ещё сильнее структурно это показал:

**Main theorem:** quorum-pivot separation.

**Diagnostic characterization:** seven-premise model.

Тогда reviewer не сможет сказать:

> “Authors call an exhaustive truth table a major theorem.”

Сам exhaustive result полезен. Просто не надо заставлять его конкурировать по значимости с T2/T3.

---

# 13. Replay section либо сильнее привязать к основной истории, либо вынести часть в appendix

Сейчас central paper — про **phase erasure**.

Потом возникает отдельный replay theorem.

Он хороший, особенно `X,X,Y` counterexample.

Но это также второй самостоятельный story arc.

Если venue ограничивает страницы, я бы не резал quorum-pivot part ради replay.

Можно оставить в основном тексте:

> replay is a second closure dimension; immediate stutter is insufficient; theorem requires projection congruence.

А длинный proof/counterexamples/non-idempotent boundary частично отправить в appendix.

Если место позволяет — оставить.

Но **ядро paper должно считываться как phase-erasure paper**, а не как collection of scheduler facts.

---

# 14. Сократить повторяющиеся disclaimers

Сейчас осторожность у статьи хорошая, но её уже немного слишком много.

Nonclaims появляются:

- в introduction;
- в scope;
- после theorem;
- в related work;
- в external validity;
- в explicit nonclaims;
- в conclusion.

Например, отдельный список из семи вещей, которых paper не утверждает, уже достаточно сильный.

Я бы оставил:

**Introduction:** один короткий scope paragraph.

**Limitations:** подробное объяснение.

**Conclusion:** одна фраза.

А некоторые повторения вырезал.

Сейчас текст иногда звучит так, будто автор заранее отвечает на десяток рецензий. Это повышает доверие, но одновременно немного ослабляет уверенность presentation.

---

# 15. Сильно подчистить язык вокруг assurance

Например:

> “actually executed project-local proof-certificate kernel”

повторяется как защитная формулировка.

После появления reproducible artifact достаточно спокойно написать:

> “an independently implemented proof-certificate checker validates ...”

А факт execution будет в artifact evaluation.

То же с несколькими фразами типа:

> “real executed checks”

Это больше напоминает audit response, чем финальный paper.

Я подозреваю, что manuscript действительно прошёл через серию внутренних audits — и это хорошо. Но финальная версия должна **перестать выглядеть как ответ аудитору**.

---

# 16. Related Work надо сделать не шире, а острее

Сейчас related work достаточно хороший. Но перед submission я бы сделал одну очень полезную таблицу:

| WorkEndpoint partitionsDirectedPhase/type-specificReplayProperty-preserving closure theoremSeparation witness |
| ------------------------------------------------------------------------------------------------------------- |

И туда:

Twins, communication closure, Netrix, ByzzFuzz, ByzzBench, relevant message-adversary works и т. д.

Тогда novelty claim:

> мы не нашли работу, одновременно делающую четыре вещи...

становится визуально проверяемым.

Перед самой подачей literature search всё равно нужно обновить — manuscript сам это правильно требует.

---

# 17. Я бы чуть поменял hierarchy contributions

Сейчас я бы продавал paper вот так:

**Contribution 1 — главный:**
Phase erasure can destroy an agreement-violation witness because closure-added repair disables a unique honest quorum pivot.

**Contribution 2:**
General relational sufficient condition explaining when closure *does* preserve unsafety.

**Contribution 3:**
Parametric (3f+1) family + structural criterion / exact boundary.

**Contribution 4, secondary:**
Replay-erasure boundary.

**Evidence:**
SMT, prover, dual implementation, finite kernels.

То есть executable assurance — это не самостоятельная intellectual contribution такого же масштаба, а **evidence for contributions 1–4**.

Сейчас contributions уже в целом так устроены, но я бы ещё сильнее вывел quorum-pivot mechanism на первый план.

---

# 18. Artifact сделать максимально тупым для запуска

У вас уже очень хороший список evidence paths.

Финальная цель должна быть такая:

```text
git clone ...
cd ...
./reproduce.sh
```

И в конце:

```text
T1 PASS
T2 PASS
T3 PASS
T6 PASS
negative controls: 4/4 rejected
Go/Python canonical traces: match
128 premise assignments: match
```

Без ручного поиска по `gate7p`, `gate8p`, `proofs_checked`, `paper_data`.

Внутри проекта сложная структура может остаться. Reviewer должен видеть **одну кнопку**.

---

# Что я бы делал в первую очередь

Если ресурсов мало, мой порядок такой:

1. **Сделать real/natural protocol instantiation или conformance argument.**
2. **Исправить replay theorem/output issue.**
3. **Формализовать scheduler semantics и closure.**
4. **Усилить Theorem 2 явным (P\_f,B\_f) и completeness domain.**
5. **Собрать Lean или Coq реально.**
6. **Добавить structural quorum-pivot criterion между общей theorem и concrete construction.**
7. **Исправить** **`UnsafeObs`** **typing/notation.**
8. **Расписать Boolean proof T6 на бумаге.**
9. **Убрать внутренние T1/T2/T3/T6 IDs из основного текста.**
10. **Сократить повторы limitations/nonclaims и сделать narrative компактнее.**

Если выполнить **первые пять**, я бы считал, что статья изменилась качественно, а не косметически.

Самая большая прибавка будет не от новых экспериментов. Она будет от перехода:

> **“мы построили очень аккуратную абстрактную систему, где это происходит”**

к

> **“вот общий механизм, вот theorem, а вот формально проверенная связь этого механизма с естественной BFT semantics.”**

Именно это сейчас отделяет работу уровня «сильная» от работы, которую reviewer гораздо легче назвать **очень сильной**.