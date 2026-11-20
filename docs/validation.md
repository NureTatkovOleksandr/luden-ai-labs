# Фактично виконані перевірки фіналу

20.11.2026. Документаційні, джерельні та статичні перевірки; це не продуктове тестування. [Машинний протокол](../verification/validation-results.json), [валідатор](../tools/validate.py). Командне review чотирьох підтверджене користувачем; наведені перевірки — окрема робота AI, а не вигадане незалежне людське review.

| Перевірка | Результат | Підстава |
| --- | --- | --- |
| Primary 33 AC exact source meaning | PASS | {"count": 33, "missing": [], "changed": []} |
| Original 8 stories | PASS | ["US-01", "US-02", "US-03", "US-04", "US-05", "US-06", "US-07", "US-08"] |
| Per-AC historical provenance | PASS | {"initial": "822a688a04bce5167f44226efbec952069042b6c", "baseline": "0e0b1ddcfafb9ccaa455cbec8295ae757d7efd07", "current": "9beb0fe4a2b2734182ec233aa5084700f177491c"} |
| Semantic regressions and test oracles | PASS | {"errors": [], "scope": "source equality plus password toggle, cancel, empty/block and navigation; not a new human review"} |
| CSV syntax, references and status | PASS | {"rows": 64, "errors": []} |
| Original AC documentary coverage | PASS | {"original_ac": "33/33", "original_src": "5/6", "candidate_src": "6/6 with proposed US09", "code_coverage": "NOT MEASURED"} |
| 56 future tests all traced | PASS | {"defined": 56, "executed": 0, "status": "NOT RUN"} |
| Extensions not relabeled original AC | PASS | {"extensions": 10} |
| Moved Markdown links | PASS | {"checked": 93, "broken": []} |
| Pinned GitHub paths and lines | PASS | {"checked": 171, "invalid": []} |
| Markdown and JSON syntax | PASS | {"json_blocks": 24, "errors": []} |
| Per-operation API examples | PASS | 18 implemented +4 proposed; synthetic NOT RUN; multipart fields are a representation, not JSON wire |
| Actual model field coverage | PASS | {"entities": 9, "properties": 97, "missing": []} |
| Full state matrix | PASS | {"states": 5, "cells": 25} |
| PATCH null/missing and atomic rules | PASS | Nullable clear distinct from missing; nonnullable null/mixed invalid do not persist |
| P01-P08 and version conflicts explicit | PASS | No blanket acceptance of P proposals from team review |
| Confirmed four-person team review | PASS | {"participants": ["Паламарчук Антон", "Татьков Олександр", "Сергєєва Таісія", "Панковський Тимофій"], "basis": "direct user confirmation", "review_date": null, "individual_findings": "not fabricated"} |
| No obsolete active blockers | PASS | [] |
| Clean current repository snapshots | PASS | {"backend": "fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff", "frontend": "ea90e7f465012d78d2f0593ad745ffb0ea07106c", "ux_ui": "9beb0fe4a2b2734182ec233aa5084700f177491c"} |
| PDF matches current Markdown | PASS | Current source hash |
| Short Ukrainian report PDF | PASS | {"pages": 2, "Ukrainian_text": true} |
| Final PDF visual inspection | PASS | {"date": "2026-11-20", "reviewer": "AI assistant, visual inspection of final rendered PNGs; not a new human reviewer", "status": "PASS", "pages_reviewed": [1, 2], "pdf_sha256": "96f3866b15e2df0fd866490d1f50a501f708f426ef901f2897bd57197417535e", "observed": "Перевірено дві сторінки оновленого PDF для GitHub: посилання на версію здавання, українські символи, імена, абзаци й колонтитули читабельні; обрізання/накладання немає."} |
| Actual Mermaid parser | PASS | {"architecture_sha256": "4209096c4f2cb20dc24f0ebb3e3bd645f7522d86a78af43f1e6863f7f1283d26", "parser": "mermaid 11.17.2", "diagrams": [{"diagram": 1, "status": "PASS", "type": "flowchart LR"}, {"diagram": 2, "status": "PASS", "type": "erDiagram"}, {"diagram": 3, "status": "PASS", "type": "sequenceDiagram"}, {"diagram": 4, "status": "PASS", "type": "sequenceDiagram"}]} |

## Змістова перевірка й межі

Кожен із 33 первинних текстів порівняно окремим парсером із джерелом. Перевірено видимість пароля, cancel, empty/block, profile/library/store та quantity/destination/create-trigger конфлікти. Змістовий аналіз кожної версії — у [ac-reconciliation.md](ac-reconciliation.md). Евристика не є повною автоматичною перевіркою природної мови; рішення не приписано іншому рецензенту.

56 продуктових TC — NOT RUN. Backend/frontend/Android build, зовнішні Firebase/Stripe, runtime ownership/security/concurrency, restart та WCAG-вимірювання не запускались. F-T01–F-T07 — історичні записи UX Present, не нові тести агента. Повторний fetch та читання важливих code paths підтвердили незмінні актуальні BE/FE.

У двох Firebase config-файлах лишаються [потенційні секрети](../verification/secret-scan.json); значення й активність не перевіряли та не розкривали. Raw-token console log і unsalted SHA-256 — CONFIRMED факти коду. Жоден дефект продукту не закрито самим редагуванням документації.

Новий meaningful commit/tag, перевірка bundle й ZIP checksum фіксуються в [VERSION.txt](../VERSION.txt) та протоколі пакування після фінальної перевірки. Попередній commit/tag і архіви збережені. Версія GitHub-здавання — lab01-spec-published; факт публікації перевіряється окремим зовнішнім протоколом.
