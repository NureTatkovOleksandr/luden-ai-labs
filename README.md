# Luden — лабораторні роботи з AI у програмній інженерії

Репозиторій команди для ЛР1–ЛР4. Поточний завершений комплект документації — **ЛР1 «Вимоги та проєктування з AI-асистентом»**. Наступні роботи продовжуються в цьому самому репозиторії.

## Здавання ЛР1

- [Короткий звіт](docs/lab-01.md) · [PDF, 2 сторінки](docs/lab-01.pdf)
- [Вимоги — канонічне джерело правил](docs/requirements.md)
- [Архітектура й ADR](docs/architecture.md) · [API-контракт](docs/api-contract.md)
- [Матриця простежуваності](docs/traceability.csv) · [Метрики покриття](docs/traceability-notes.md)
- [AI-журнал](docs/ai-log.md) · [56 майбутніх тестів](docs/test-cases.md)
- [Перевірка джерельних 33 AC](docs/ac-reconciliation.md) · [Журнал рішень](docs/decision-log.md)
- [Відповідність методичці](docs/methodology-compliance.md) · [Зіставлення з Mini Issue Tracker](docs/methodology-crosswalk.md)
- [Фактичні перевірки](docs/validation.md) · [Аудит коду](docs/implementation-audit.md) · [Результати виправлень](docs/review-report.md)

**Фіксована версія для перевірки:** [lab01-spec-published](https://github.com/NureTatkovOleksandr/luden-ai-labs/tree/lab01-spec-published). Tag lab01-spec також позначає цей публічний знімок для сумісності з методичкою. Повна історія попередніх локальних редакцій збережена окремо й не публікується разом із їхніми архівами. Дані версії — у [VERSION.txt](VERSION.txt).

## Структура

```text
docs/          вимоги, архітектура, API, звіт, AI-log, CSV і перевірки
sources/       мінімальний уже публічний Input Pack і запис про review
tools/         валідатор, рендер PDF і Mermaid-перевірка
verification/  машиночитні протоколи й прив’язка до версій коду
```

## Команда

Паламарчук Антон, Татьков Олександр, Сергєєва Таісія, Панковський Тимофій. Участь усіх чотирьох у колективному перехресному review підтверджена користувачем; деталі й межі підтвердження наведені у звіті. Історичні ролі попередньої UX-команди не видаються за нове персональне авторство файлів.

## Пов’язані реалізації й джерела

- [Попередня UX/UI-робота](https://github.com/NureTatkovOleksandr/luden-ux-ui)
- [Backend](https://github.com/Ramseer24/Luden-Back-End)
- [Frontend](https://github.com/Timbuhtuk/Luden-Front-End)
- [Знімки, джерела й статуси](docs/sources.md)

Це документація ЛР1 із урахуванням наявних ASP.NET Core/Firebase/Stripe та React/TypeScript. Реалізація застосунку в ЛР1 не потрібна. Дефекти коду й непогоджені P-рішення описані окремо; 56 продуктових тестів мають NOT RUN. Наявність GitHub-репозиторію не є результатом запуску цих тестів.

## Повторна перевірка

Python 3.10+:

```sh
python -m pip install -r tools/requirements-checks.txt
python tools/validate.py
```

Валідатор не звертається до живих платежів чи Firebase. Для повторного рендеру PDF додатково потрібні reportlab, Arial або DejaVu та pypdfium2 для PNG; для нового Mermaid parse — пакети з tools/package.json. Збережений Mermaid-протокол перевіряється за hash актуального architecture.md.

## Межа публікації

Це окремий публічний знімок для здавання. У ньому немає вкладених ZIP, Git bundle, оригінальних методичок DOCX/PDF або історії, що містить ці файли. Попередні редакції та всі джерела збережені локально. Внутрішні chat-ID вилучено з публічної AI-log копії; ключі чи токени доступу не додаються. Джерельні версії UX/UI доступні за відкритими посиланнями.
