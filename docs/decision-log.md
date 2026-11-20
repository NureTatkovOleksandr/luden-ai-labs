# Журнал рішень і зіставлення з UX/UI

Ідентифікатори Q-06–Q-11 збережені. LR1-D-xx — локальні технічні питання (у тексті ранньої редакції також скорочені D-xx); UX:D-xx — історичні спостереження/рішення іншого документа. Вони не тотожні. Реєстр P-01–P-08 у поточному UX Decision Log має PROPOSED; reviewer/date/decision порожні. Командне review, підтверджене користувачем, не заповнює ці поля автоматично.

Джерело: [01_requirements/Decision_Log.md @ 9beb0fe](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/9beb0fe4a2b2734182ec233aa5084700f177491c/01_requirements/Decision_Log.md#L1).

| Питання | Зв’язок UX | Стан | Поведінка / кандидат | Що визначено й що справді лишилось |
| --- | --- | --- | --- | --- |
| Q-06 | P-01 | PROPOSED у HEAD; колись OPEN | Одна ліцензія, repeat add no-op, owned→library, quantity як текст. | Погодити звуження первинної quantity-гілки AC-06.2; duplicate-check/конкурентність BR-12 — технічна деталізація. |
| Q-07 | P-02 | PROPOSED | Pending→Processing→Declined/Paid→Completed; retry того самого Bill за незмінних items/sum; Paid прибирає куплене. | Відмова не видає нову гру й не забирає старе — вже SRC-04/05 CONFIRMED. Момент create/attempt/recovery і snapshot-політика потребують прийняття. |
| Q-08 | P-05 | PROPOSED | Admin також купує; зміни каталогу перевіряються окремо. | Admin-only CRUD уже SRC-06 CONFIRMED. Лише купівля Admin/суміщення прав є кандидатом. |
| Q-09 | P-03 | PROPOSED | Автосесія після register; library після login/register без перерваної дії. | Первинний AC-02.2 веде в profile; API register200 Success + окремий login. Немає доказу прийняття нового destination. |
| Q-10 | P-06 | PROPOSED | Keyboard, visible focus, focus trap/return, Escape, contrast4.5:1/large3:1. | Чотири NFR задані ЛР 1; конкретний розширений keyboard protocol — P-06. Runtime-аудит NOT RUN. |
| Q-11 | P-03 | PROPOSED | ≥8, email format, exact confirmation, inline errors. | Поля, duplicate rejection і mismatch без запиту вже AC-01 CONFIRMED; 7/8 та API confirmation — окреме уточнення. |
| Q-02 | P-02/P-08 частково | OPEN | Обсяг Present/середовище; в коді є Stripe, у Product Baseline провайдер не обраний. | Не плутати Figma sim із реальним платіжним sandbox; погодити середовище й adapter. |
| LR1-D-01 | P-01/P-02/P-07, SRC-04/05 | PROPOSED механізм | Не втрачати раніше придбаний доступ; заборонити DELETE з будь-якою BillItem/License:409. Soft delete — альтернатива. | Саме збереження старих прав CONFIRMED; OPEN тільки механізм збереження історії/доступу. |
| LR1-D-02 | P-02/P-07; AC-07.5 | CONFIRMED cancel; PROPOSED cleanup | «Скасувати» повертає той самий кошик. Після Paid прибирати тільки куплені позиції, не паралельно додані. | Cancel не залишено відкритим; момент cleanup й поведінка × під час processing — погодити. |
| LR1-D-03 | P-02; SRC-04 | PROPOSED | Ціну визначає сервер; snapshot зафіксовано; UAH як наявний default, decimal→minor boundary. | Фіксована валюта, правила discount/precision/rounding не задані джерелом. $24.99 у Figma — приклад, не правило всіх цін. |
| LR1-D-04 | P-01/P-02/P-04 | PROPOSED | За замовчуванням пропонується зберегти наявний локальний Cart і серверну валідацію checkout. Server Cart — необов’язковий варіант API-P01–03. | User-scoped storage, атомарна резервація й duplicate Bill захист потрібні для обраної single-copy політики; не вимагати нової DB-сутності лише за AI-порадою. |
| LR1-D-05 | немає P-джерела | PROPOSED | Catalog/library id ASC; Bill createdAt DESC,id DESC. | Гарантований порядок не задано; лишити явно кандидатом, не вимогою замовника. |
| LR1-D-06 | P-02 | PROPOSED | Durable attempt+charge/event dedup, локальний atomic claim/multi-location update та recovery після Stripe success. | Вибрати алгоритм доставки/відновлення; зовнішній Stripe не входить у Firebase ACID transaction. |
| LR1-D-07 | методичка с.5, не P-08 | PROPOSED реалізація | Presence-aware PATCH на тому самому Product/{id}, nullable releaseDate можна очистити; validate-all-before-write. | Чинний partial PUT задокументований; strict PATCH і migration клієнта ще відсутні. |
| LR1-D-08 | Input Pack/history | CLOSED: джерело отримано | 33 AC та 8 US відновлені з історії, усі порівняно з 0e0b1dd/HEAD і попередньою ЛР 1. | Не є затвердженням кожної історичної ревізії. Не ставити source NOT VERIFIED для доступного тексту. |
| LR1-D-09 | P-02 | PROPOSED | Bill створюється при першому confirm, не при простому відкритті форми; той самий snapshot→retry same Bill; зміна cart→new Bill. | AC-07.1 вимагає лише відкрити форму. Чинний PaymentModal створює Bill при ініціалізації; зміна тригера не виконана. |
| LR1-D-10 | P-03/P-04/P-07 | PROPOSED | Поки немає прийняття, вихідний login destination=profile. Library/guest resume — явні кандидати, не підміна AC-02.2. | Не виправляти frontend лише через наявність пізнішого P-03 у репозиторії. |
| LR1-D-11 | P-08 | PROPOSED; попередня UX-робота | Low-fidelity grayscale або виняток рецензента для кольорового Figma. | Не переносити як додаткову продуктову функцію чи безумовну вимогу ЛР 1. Погоджується окреме UX-приймання. |
| LR1-D-12 | користувач | CONFIRMED: колективне review | Усі четверо перевірили вимоги/AC/архітектуру/API/traceability. | Закрито твердження про відсутність review. Не підтверджено review-date/особисті findings/прийняття P/виправлення продуктового коду. |

## Усі P-01–P-08

| P | Відповідник ЛР 1 | Статус | Межа |
| --- | --- | --- | --- |
| P-01 | Q-06; BR-05/12; EXT-03 | PROPOSED | one-copy не прийнято за факт наявності рядка |
| P-02 | Q-07; LR1-D-02/03/06/09; BR-06–09 | PROPOSED | доступ Paid/Completed задано; точний життєвий цикл/створення — кандидат |
| P-03 | Q-09/Q-11; LR1-D-10; BR-01/02/17 | PROPOSED | поля/duplicate/mismatch задано; session/min8/destination окремо |
| P-04 | BR-03/17; EXT-09; TC-X17 | PROPOSED | guest read задано; context resume нове |
| P-05 | Q-08; BR-03/11; AC-09 | PROPOSED | Admin-only задано; Admin-buy кандидат |
| P-06 | Q-10; NFR-01 | PROPOSED | об’єктивні NFR у методичці; детальні focus-trap дії перевірити у UI |
| P-07 | BR-04/09/16; AC-04.3/05.3/07.5 | PROPOSED розширення | cancel та genre-preserving clear вже джерельні; повний контекст/× ширше |
| P-08 | LR1-D-11 | PROPOSED UX-процедура | не збільшує обсяг продукту ЛР 1 |

## Зіставлення просторів BR

| Зовнішній ID | Зміст UX-правила | Локальні BR ЛР 1 |
| --- | --- | --- |
| UX:BR-01 | Публічне читання / приватні профіль, library, оплата | BR-03 |
| UX:BR-02 | Admin-only зміни товару | BR-03;BR-11 |
| UX:BR-03 | Бонуси відкладені | BR-06 |
| UX:BR-04 | Ліцензії/статуси перевіряють у застосунку, не Figma | BR-07;BR-08 |

## Уже закриті невизначеності

Джерело 33 AC отримано; семантика видимості пароля, порядку AC-06.3/06.4, скасування й переходів профіль/library/store відновлена; дата review не вигадується, сам факт колективної перевірки підтверджено. Public read, no-bonus, owner Paid/Completed і збереження старих прав після відмови задані SRC/PDF, їх не треба питати повторно.

Відкритими лишаються конкретні непогоджені P-політики, історичний trigger card/details та quantity-політика, money precision/currency/discount, delete strategy, server duplicate/recovery механізм, первинний аналіз до AI й окремий захист ЛР 1. Відсутність runtime-тестів тут не маскує відсутність командного review.
