# Вимоги й контракт даних Luden — ЛР 1

Фінальна редакція 20.11.2026. Єдине джерело бізнес-правил цього пакета. [Походження і статуси](sources.md). CONFIRMED позначає перевірене джерело; нові P/EXT-рішення не стають погодженими через командне review. [Походження 33 AC](ac-reconciliation.md). IMPLEMENTED завжди стосується коду, не результату тесту.

## 1. Обсяг і простежувані вимоги

| ID | Потрібний результат | Джерело / стан |
| --- | --- | --- |
| SRC-01 | Email, пароль, підтвердження, відхилення дубліката; вхід і профіль. | PDF с.2–3 CONFIRMED; Q-09/Q-11 PROPOSED |
| SRC-02 | Публічний каталог, деталі обраної гри, пошук AND жанр; loading/error/empty окремо. | PDF с.2–3 CONFIRMED |
| SRC-03 | Додавання/вилучення, склад і сума; порожнє не оформлюється. | PDF с.2–3 CONFIRMED; одна копія Q-06 PROPOSED |
| SRC-04 | Сума, валюта, результат оплати, блокування повтору; відмова без нових прав. | PDF с.2–4 CONFIRMED; повтор у тій самій Bill Q-07 PROPOSED |
| SRC-05 | Власна бібліотека лише Paid/Completed; порожній стан. | PDF с.2–4 CONFIRMED |
| SRC-06 | Гість читає каталог; приватні дії потребують входу; товар змінює Admin. | PDF с.2–3 CONFIRMED; купівля Admin Q-08 PROPOSED |
| SRC-07 | Скидання пароля через email. | PDF с.2,4: відкладено; виключено з метрик |

Також відкладені Google OAuth, обране, редагування профілю, списання бонусів, перемикання валют, окремий Admin UI, Android/mobile web та AI-рекомендації (лише ЛР 4). Наявність коду цих функцій не розширює поточний навчальний обсяг; див. класи D/F у [аудиті](implementation-audit.md).

## 2. Початкові US-01–US-08 і 33 AC

Оригінал отримано з UX/UI-репозиторію, повну історію перевірено. У колонці «Джерельний AC» наведено точний текст першої версії Input Pack @822a688; канонічним джерелом правил ЛР 1 лишається цей requirements.md. Пізніші редакції @0e0b1dd та @9beb0fe зіставлені окремо для кожного AC. Їхні зміни не оголошено затвердженими: реєстр погодження P-01–P-08 порожній. Спільний сенс збережено, розбіжності trigger/quantity і статусу пропозицій не приховано. [Повне зіставлення](ac-reconciliation.md), [джерела](sources.md).

Кожний AC має джерело, SRC, BR, компонент/API і тест у traceability.csv. «NOT APPLICABLE» для API означає локальну UI-дію, а не відсутню вимогу. Позитивні, негативні та граничні підвипадки задані у test-cases.md. Додаткові серверні гарантії відокремлено у §2.10, без зміни первинних ідентифікаторів.

### US-01 — SRC-01

Як відвідувач, я хочу створити обліковий запис. Користь: отримати власний обліковий запис для покупок. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-01.1 | Форма містить email, пароль і підтвердження пароля. | Відкрити реєстрацію: є три поля email/password/confirmation; надсилання не потрібне. | BR-01 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L7) |
| AC-01.2 | Валідний запит створює обліковий запис. | Подати валідні дані з новим email: створено один акаунт. Автовхід — окремий P-03, не текст цього AC. | BR-01 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L7) |
| AC-01.3 | Якщо email уже зайнятий, API відхиляє повторну реєстрацію. | Повторити вже зайнятий email: API відхиляє; нового акаунта немає. Чинний HTTP400 EmailBusy, не вигаданий 409. | BR-01 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L7) |
| AC-01.4 | Якщо паролі різні, форма показує помилку і не надсилає запит | Різні password/confirmation: помилка на формі, register-запит не надсилається. Пряма перевірка confirmation API — EXT-02. | BR-02 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L7) |

### US-02 — SRC-01

Як покупець, я хочу увійти за паролем. Користь: відкрити власний профіль. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-02.1 | Вхід використовує email і пароль. | Заповнити email/password на формі входу; саме вони передаються password-гілці login. | BR-03 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L8) |
| AC-02.2 | Після успішного входу відкривається профіль. | За успішного входу відкривається профіль. Перенаправлення одразу в бібліотеку з P-03 лишається окремою непогодженою ревізією. | BR-03 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L8) |
| AC-02.3 | Помилка входу показується на формі без переходу у профіль. | Невірні облікові дані: помилка лишається на формі, перехід до профілю не виконується. | BR-03 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L8) |
| AC-02.4 | Пароль прихований на старті, користувач може показати і знову приховати його | Пароль на старті input type=password; натиснути показ/приховати двічі: type=text/password, значення незмінне. Це не перевірка JWT або ролі Admin. | BR-15 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L8) |

### US-03 — SRC-02

Як відвідувач, я хочу переглянути пропозиції магазину. Користь: порівняти пропозиції. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-03.1 | Каталог показує картки ігор з назвою та ціною. | Повернути список різних Product: кожна картка показує назву й ціну саме свого товару. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L9) |
| AC-03.2 | Під час завантаження є індикатор. | Затримати відповідь каталогу: до завершення показано індикатор, а не порожній список. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L9) |
| AC-03.3 | Помилка завантаження має окремий стан. | Змоделювати помилку запиту: показано окремий error-стан, відмінний від no matches. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L9) |
| AC-03.4 | Після успішного повторного запиту відображаються актуальні картки | Після помилки змінити відповідь сервера й повторити запит: показано нові картки, стару помилку прибрано. Це перевірюване уточнення без зміни сенсу. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L9) |

### US-04 — SRC-02

Як покупець, я хочу знайти гру за назвою чи фільтром. Користь: знайти потрібну гру. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-04.1 | Введення запиту звужує видимий список. | На dataset із збігами й незбігами ввести запит: видимий список звужується. Case/trim конкретизуються BR-04 як технічна пропозиція. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L10) |
| AC-04.2 | Нуль збігів показує порожній стан. | Ввести рядок без збігів: показано порожній стан, не server error. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L10) |
| AC-04.3 | Очищення запиту повертає ігри, які відповідають чинним фільтрам. | За активного жанру очистити текст: залишаються ігри чинного жанру. Це вже джерельне правило, його не лишено OPEN. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L10) |
| AC-04.4 | Вибір жанру обмежує результати цим жанром | Обрати жанр: усі результати належать йому; за тексту й жанру перевірити AND, задане SRC-02. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L10) |

### US-05 — SRC-02; SRC-03

Як покупець, я хочу відкрити деталі вибраної гри. Користь: перевірити товар перед додаванням. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-05.1 | Натискання картки відкриває деталі саме цієї гри. | Натиснути картку X: відкриті деталі X, не Y. Пізніший варіант «Деталі» на картці позначено в історії; прийняття заміни trigger не вигадано. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L11) |
| AC-05.2 | У деталях видно назву й ціну. | У відкритих деталях показано назву й ціну вибраної гри. | BR-04 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L11) |
| AC-05.3 | Закриття деталей повертає до каталогу. | Закрити деталі: повернення до каталогу. Збереження всього контексту — додаткова P-07, збереження жанру при очищенні — окремий AC-04.3. | BR-16 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L11) |
| AC-05.4 | Дія додавання в деталях передає до кошика саме вибрану гру | Додати X з його деталей: у кошик передано саме X. Кількість=1/owned-check — P-01/EXT-03, не підміна цього AC. | BR-05 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L11) |

### US-06 — SRC-03

Як покупець, я хочу перевірити склад кошика. Користь: контролювати склад і підсумок. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-06.1 | Додана гра відображається в кошику. | Додати X: X видно в кошику; коректність duplicate/no-op перевіряється окремо за кандидатом P-01. | BR-05 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L12) |
| AC-06.2 | Зміна кількості чи видалення оновлює склад і суму. | Видалити позицію: склад/сума змінюються відповідно. Якщо перевіряється первинна гілка quantity-update, нова кількість змінює суму; конфлікт цієї гілки з P-01 явно OPEN, до погодження не видаляти її й не заявляти прийняття single-copy. | BR-05 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L12) |
| AC-06.3 | У порожньому кошику перехід до оплати недоступний. | Порожній кошик: кнопка переходу до оплати недоступна. Серверний empty-check — додатковий BR-06, не підміна UX AC. | BR-05 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L12) |
| AC-06.4 | Після видалення останньої гри показується порожній стан | Видалити останню гру: відображений порожній стан. Не плутати із AC-06.3. | BR-05 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L12) |

### US-07 — SRC-03; SRC-04; SRC-05

Як покупець, я хочу оформити замовлення. Користь: придбати обрані ігри. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-07.1 | З непорожнього кошика можна відкрити форму оплати. | З непорожнього кошика відкрити форму оплати. Не прирівнювати відкриття форми до server Bill creation або успішної оплати. | BR-06 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L13) |
| AC-07.2 | Оформлення доступне без списання бонусів, зі значенням 0. | Оформити без списання бонусів, значення використаних бонусів 0; у поточному релізі списання відкладене за SRC-03. | BR-06 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L13) |
| AC-07.3 | Помилка оплати не відкриває придбану гру в бібліотеці. | Керована помилка оплати не надає нової гри. Збереження попередніх прав підтверджене SRC-04/PDF і деталізоване BR-08; це не нове припущення. | BR-07;BR-08 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L13) |
| AC-07.4 | Під час обробки повторне підтвердження недоступне. | Поки обробка триває, повторне підтвердження в UI недоступне. Серверний lock/idempotency — EXT-05. | BR-07 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L13) |
| AC-07.5 | Скасування повертає до кошика зі збереженими позиціями | Натиснути «Скасувати» до підтвердження або у формі після відмови: повернення до кошика, усі позиції збережені. Retry того самого Bill — окремий P-02, не цей AC. | BR-09;BR-16 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L13) |

### US-08 — SRC-05

Як покупець, я хочу бачити доступні мені ігри. Користь: дістатися власних покупок і повернутися до магазину. Формулювання користі додано редакційно; джерельна роль й дія збережені.

| AC | Джерельний AC (дослівно) | Операційна перевірка без підміни сенсу | BR | Походження |
| --- | --- | --- | --- | --- |
| AC-08.1 | Бібліотека доступна з профілю покупця. | Із профілю відкрити власну бібліотеку. Не підміняти цей навігаційний AC перевіркою Paid. | BR-16 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L14) |
| AC-08.2 | Гра із замовлення у статусі `Paid` або `Completed` входить до бібліотеки власника. | Власні Paid/Completed надають гру; source SRC-05/PDF додатково виключає чужі й неоплачені. Перевірити власника й статус, не наявність UI-кадру. | BR-03;BR-08 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L14) |
| AC-08.3 | Бібліотека без придбаних ігор має порожній стан. | За відсутності придбаних ігор видно порожній стан бібліотеки. | BR-08 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L14) |
| AC-08.4 | Із бібліотеки можна перейти до магазину | Із порожньої та непорожньої бібліотеки перейти до магазину. Збереження Paid→Completed/заборона повторної покупки — BR-07/08 і P-01, не заміна навігації. | BR-16 | CONFIRMED source; [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/822a688a04bce5167f44226efbec952069042b6c/01_requirements/01_Input_Pack_v0.1.md#L14) |

### US-09 — SRC-06 (PROPOSED)

Як Admin, я хочу створювати, змінювати й вилучати товар, щоб підтримувати каталог. Це запропоноване доповнення методички; командне review не є доказом прийняття замовником.

| AC | Критерій | BR | Походження |
| --- | --- | --- | --- |
| AC-09.1 | Admin створює, presence-aware PATCH змінює лише передані дозволені поля, видаляє непроданий товар. Null відхиляється лише для nonnullable полів; nullable releaseDate може очищатися. {}, unknown, immutable і змішані валідні/невалідні зміни відхиляються без жодного запису. | BR-11;BR-10 | PROPOSED; PDF с.4–6 |
| AC-09.2 | Гість отримує 401, User без Admin403 на створення/оновлення/видалення; каталог не змінюється. | BR-03;BR-11 | PROPOSED; PDF с.6 |

### 2.10. Збережені технічні уточнення (окремо від початкових AC)

| ID | Уточнення | Статус / джерело | BR | Майбутній тест |
| --- | --- | --- | --- | --- |
| EXT-01 | Сесія після реєстрації та 7/8 символів | Q-09/Q-11; P-03 PROPOSED | BR-01;BR-02 | TC-X16 |
| EXT-02 | Confirmation перевіряється також API, пароль не повертається | API-presence PROPOSED; безпечне зберігання задано PDF | BR-02 | TC-X16 |
| EXT-03 | Одна копія, duplicate-add no-op, owned-game → бібліотека | Q-06/P-01 PROPOSED; конфлікт із первинною quantity-гілкою AC-06.2 не прихований | BR-05;BR-12 | TC-X05 |
| EXT-04 | Server-owned Bill.userId/status/ціни й незмінний snapshot | PROPOSED технічне забезпечення SRC-04/05; ADR-03 | BR-06;BR-13 | TC-X04;TC-X09 |
| EXT-05 | Серверний lock, подія no-op, retry тієї самої Bill, не повторний charge | Матриця PDF; P-02 PROPOSED; atomic/dedup механізм OPEN | BR-07;BR-12 | TC-X01;TC-X06;TC-X07 |
| EXT-06 | Paid→Completed зберігає доступ; не видаляти історичний Product/Bill | Право з SRC-04/05 CONFIRMED; політика DELETE PROPOSED | BR-08;BR-10 | TC-X08 |
| EXT-07 | Кошик очищається після Paid лише для куплених позицій; паралельні додавання збережені | P-02 PROPOSED; «Скасувати» зберігає склад — уже AC-07.5 CONFIRMED | BR-09;BR-16 | TC-X14 |
| EXT-08 | Чужий/прострочений JWT не відкриває даних; Admin перевіряється окремо | SRC-06 CONFIRMED; Admin-купівля P-05 PROPOSED | BR-03;BR-11 | TC-X03;TC-X04 |
| EXT-09 | Зберігати контекст каталогу/гостьової дії; не скидати покупку після деталей | P-04/P-07 PROPOSED; очищення тексту зберігає жанр уже AC-04.3 CONFIRMED | BR-04;BR-16;BR-17 | TC-X12;TC-X17 |
| EXT-10 | Серверний кошик — необов’язкова архітектурна альтернатива; локальний checkout має валідуватися сервером | PROPOSED D-04; mandatory server Cart не виводиться з SRC-03 | BR-05;BR-06 | TC-X04;TC-X14 |

## 3. Бізнес-правила

| ID | Походження | Контракт |
| --- | --- | --- |
| BR-01 | CONFIRMED / Q-09 PROPOSED | Один акаунт на email; дублікат відхиляється; сесія після реєстрації — робоче Q-09. Поточний UI робить register → login, API register токена не повертає. |
| BR-02 | Q-11 PROPOSED; підтвердження CONFIRMED | Пароль ≥8 без обрізання чи зміни регістру; підтвердження не зберігати. Рекомендовано перевіряти обидва на API. Поведінка 7/8 символів явно тестується. |
| BR-03 | CONFIRMED; кошик PROPOSED | Каталог/деталі публічні. Профіль, оплата, бібліотека — лише власник із JWT; Admin-мутації — Admin. User відповідає бізнес-ролі покупець. Admin також купує — Q-08 PROPOSED. |
| BR-04 | CONFIRMED; деталі нормалізації PROPOSED | Текст і жанр AND; очищення тексту зберігає жанр; порожньо ≠ помилка ≠ loading. category є одним жанром у поточному коді. Пошук: trim запиту, case-insensitive substring; границі та множинні жанри OPEN. |
| BR-05 | CONFIRMED; Q-06 PROPOSED | Кошик: одна копія, повторне додавання no-op; видалення перераховує суму; придбану гру додавати/купувати не можна. Серверного кошика наразі немає; це архітектурна альтернатива, не окрема обов’язкова вимога SRC-03. |
| BR-06 | CONFIRMED; спосіб знімка PROPOSED | Створення лише з непорожнього кошика; власник, Pending, сума й ціни визначаються сервером; сума = Σ(quantity × priceAtPurchase). Не приймати від клієнта totalAmount/status/userId як джерело істини. Витрата бонусів відкладена. Відкриття форми за AC-07.1 не створює замовлення за визначенням; P-02 пропонує create Bill на першому confirm, D-09 PROPOSED. |
| BR-07 | CONFIRMED; технічні переходи PROPOSED | Повна матриця нижче: блокувати паралельне підтвердження; після відмови повтор у тій самій Bill; термінальний доступ не відкочувати. Точне фінансове виконання NOT VERIFIED. |
| BR-08 | CONFIRMED | Бібліотека = DISTINCT Product із BillItem власних Bill Paid/Completed. License — дані ключа, не незалежне джерело прав; ключі фільтрувати до власних BillItem. |
| BR-09 | AC-07.5 CONFIRMED; очищення після Paid P-02 PROPOSED | «Скасувати» повертає до кошика зі збереженим складом (AC-07.5). Кошик очищати після надійного серверного Paid — кандидат P-02; лише куплені позиції, не додані паралельно. При відмові зберігати. Поточний UI очищає весь локальний кошик після успіху complete. |
| BR-10 | PROPOSED / OPEN | До міграції soft delete заборонити фізичне вилучення товару, на який посилається будь-яка BillItem/License; 409. Зберігати історію і право покупця. Soft delete — альтернатива після погодження, не існуюче поле. |
| BR-11 | CONFIRMED; конкретна політика PROPOSED | Admin PATCH змінює тільки явно передані дозволені поля; усі перевірити до запису. Помилковий запит не зберігає жодної зміни. Порожня зміна й unknown заборонені. |
| BR-12 | PROPOSED / OPEN | Конкурентні покупки: атомарна резервація (userId,productId) і дедуплікація provider event/charge. Нове замовлення з активною резервацією повертає 409; оплата другого застарілого замовлення блокується до виклику провайдера. Самої UI-перевірки/Distinct недостатньо. |
| BR-13 | PROPOSED / OPEN | Ціни у decimal основних одиниць; одна валюта UAH для поточного контракту. priceAtPurchase — серверний знімок, згодом незмінний. Правила знижок/округлення — D-03, до прийняття не можна довести точну платіжну суму. |
| BR-14 | PROPOSED / OPEN | Для каталогу й бібліотеки пропонується id ASC; для власних рахунків createdAt DESC, id DESC як tie-breaker. Наразі каталог/бібліотека не мають гарантованого порядку; Bill/user сортується тільки createdAt DESC. |

| ID | Походження | Контракт |
| --- | --- | --- |
| BR-15 | CONFIRMED AC-02.4 @822a688; UX D-07 | Пароль прихований спочатку; показ/приховування не змінює введене значення і стан форми. |
| BR-16 | CONFIRMED AC-05.3/07.5/08.1/08.4; повний контекст P-07 PROPOSED | Закриття деталей повертає каталог; «Скасувати» — кошик із збереженими позиціями; бібліотека доступна з профілю; з бібліотеки є перехід до магазину. Повне збереження контексту після кожного × — додатковий кандидат. |
| BR-17 | P-03/P-04 PROPOSED; SRC-01/06 CONFIRMED | Базовий успішний login веде у профіль (AC-02.2); прямий перехід до бібліотеки й відновлення гостьової дії — кандидати, поки немає рішення. Гостьове читання вже дозволено, його не лишено відкритим. |

Увага до просторів ID: BR-01–BR-17 тут — локальні правила ЛР 1; UX:BR-01–04 із попередньої роботи мають інший зміст. Їх явне зіставлення наведено в decision-log.md, без прихованого перейменування.

Пов’язані сценарії конкурентності, зміни ціни, видалення й повторів конкретизовано у [тестах](test-cases.md), а питання вибору — у [журналі рішень](decision-log.md). Уточнення EXT-01–10 відокремлені від початкових AC; вони не є автоматично прийнятими замовником.

## 4. Єдиний контракт даних

Бізнес-акаунт = `User`, гра = `Product`, замовлення = `Bill`, позиція = `BillItem`. UUID і price_minor зі старої специфікації вилучено: код використовує `ulong` і `decimal`. JSON API має camelCase; Firebase серіалізує властивості C# у PascalCase (JsonOptions не задає naming policy). Це різні межі серіалізації.

C/U означають обов’язковість на create/update у ЦІЛЬОВОМУ контракті. S — сервер, Y — клієнт мусить передати, N — необов’язково, P — лише якщо поле включено в PATCH; «—» — операції немає. Таблиці містять усі скалярні поля сутностей поточного потоку й допоміжних сутностей, які входять у відповіді. Nullable у колонці — цільова політика; фактичні відхилення вказано поруч. Неявний CLR default не означає припустимість бізнес-значення.

### 4.1. Спільні поля IEntity

| Поле | Тип | C | U | Null | Default | Валідація / нормалізація | Змінність | Джерело / поле коду |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id | ulong → JSON integer | S | — | ні | серверний ID | &gt;0; uint64; клієнт не генерує. Для JS number безпечно ≤2^53−1, понад це OPEN міграція на string. | immutable | IMPLEMENTED: IEntity.Id; GenericRepository.GenerateIdAsync; атомарна унікальність NOT IMPLEMENTED |
| createdAt | DateTime → ISO 8601 | S | — | ні | UtcNow | UTC; недопустимий клієнтський час | immutable | IMPLEMENTED: IEntity.CreatedAt; установлюють сервіси, не generic repository |
| updatedAt | DateTime? → ISO 8601/null | S | S | так | null | UTC після зміни; у Bill create зараз DateTime.Now — розбіжність | server mutable | IMPLEMENTED: IEntity.UpdatedAt |

Спільна таблиця застосовується окремо до User, Product, Bill, BillItem, License, PaymentOrder, Region, ImageFile, Favorite. StripeOptions — конфігураційна модель, не ресурс бізнес-API; секрети не включено до специфікації та прикладів.

### 4.2. User

Джерело: [Entities/Models/User.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/User.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| username | string | S/N | — | ні | префікс email без @ | Name DTO → Username; whitespace Name замінюється префіксом; верхня межа OPEN | server / profile out of scope | IMPLEMENTED: User.Username; UserRegisterDTO.Name |
| email | string | Y | — | ні | немає | regex ^[^@\s]+@[^@\s]+\.[^@\s]+$; trim+lower для ключа унікальності PROPOSED; зараз точне == без нормалізації | immutable у ЛР 1 | CONFIRMED; IMPLEMENTED Email, але DTO nullable, Required немає |
| passwordHash | string? | S | — | так лише OAuth | null | не повертати; пароль не зберігати відкрито; зараз SHA-256 без salt; пароль ≥8 NOT IMPLEMENTED на API | server | IMPLEMENTED User.PasswordHash; Sha256PasswordHasher |
| googleId | string? | — | — | так | null | OAuth поза обсягом; не приймати як звичайний Id | server | IMPLEMENTED / F: User.GoogleId |
| role | UserRole | S | — | ні | User | User=0, Admin=1; JSON рядки; клієнт не призначає | server | IMPLEMENTED User.Role; Q-08 PROPOSED |
| bonusPoints | decimal | S | — | ні | 0 | нарахування є; списання відкладене; одиниця/округлення OPEN | server | IMPLEMENTED / D,F: User.BonusPoints |
| avatarFileId | ulong? | — | — | так | null | посилання на ImageFile; редагування профілю відкладене | server | IMPLEMENTED / F: User.AvatarFileId |

### 4.3. Product

Джерело: [Entities/Models/Product.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/Product.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| name | string | Y | P | ні | немає | Required create, ≤200; trim і відхилення whitespace PROPOSED; update зараз порожній рядок ігнорує | Admin mutable | IMPLEMENTED Product.Name / CreateProductDto / UpdateProductDto |
| description | string | Y | P | ні | немає | ≤2000; explicit Required немає, nonnullable MVC може робити implicit required; trim PROPOSED; пустий опис PROPOSED дозволити | Admin mutable | IMPLEMENTED Product.Description; DTO |
| price | decimal | Y | P | ні | CLR 0 — невалідно | ≥0.01; верхня межа CLR decimal, DTO double.MaxValue не уточнює бізнес-межі; 2 знаки й округлення OPEN; валюта на Product відсутня | Admin mutable | IMPLEMENTED Product.Price; Range DTO; BR-13 PROPOSED |
| stock | int | Y | P | ні | 0 | 0..2147483647; цифрове значення запасу не доводить обмеження ліцензій | Admin mutable | IMPLEMENTED Product.Stock; create Required для int не виявляє missing, 0 проходить |
| regionId | ulong | Y | P | ні | CLR 0 — цільово заборонено | &gt;0 і Region існує PROPOSED; перевірки існування у ProductService немає; DTO відповіді int? звужує ulong | Admin mutable | IMPLEMENTED Product.RegionId; ProductDto.RegionId int? |
| coverFileId | ulong? | S | S | так | null | лише файл цього товару; через окремий PUT cover; create cover ≤10MiB, JPEG/PNG/GIF/WebP за controller | server | IMPLEMENTED Product.CoverFileId; Cover IFormFile DTO |
| discountPercentage | int | N | P | ні | 0 | 0..100; точна участь у серверному розрахунку OPEN | Admin mutable | IMPLEMENTED Product.DiscountPercentage; DTO Range |
| salesCount | int | S | — | ні | 0 | на оплаті += quantity; конкурентне оновлення не атомарне | server | IMPLEMENTED Product.SalesCount |
| developer | string | N | P | ні | empty | create null → empty; довжина OPEN; PATCH null відхилити PROPOSED | Admin mutable | IMPLEMENTED Product.Developer |
| publisher | string | N | P | ні | empty | create null → empty; довжина OPEN; PATCH null відхилити PROPOSED | Admin mutable | IMPLEMENTED Product.Publisher |
| releaseDate | DateTime? | N | P | так | null | ISO date-time; цільовий null очищає дату; чинний PUT null ігнорує | Admin mutable | IMPLEMENTED Product.ReleaseDate; target clear PROPOSED |
| category | string | N | P | ні | empty | один жанр; список жанрів у коді відсутній; мапа дозволених значень OPEN; trim PROPOSED | Admin mutable | IMPLEMENTED Product.Category; StorePage maps genre |

### 4.4. Bill

Джерело: [Entities/Models/Bill.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/Bill.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| userId | ulong | S | — | ні | із перевіреного JWT | не body; FK User існує; чинний API бере body.UserId | immutable | IMPLEMENTED Bill.UserId; ціль BR-03/06 |
| currency | string | S | — | ні | UAH | для цього релізу UAH PROPOSED; код приймає довільний рядок; normalize upper; відсутня у BillDto | immutable після create | IMPLEMENTED Bill.Currency; response addition PROPOSED |
| totalAmount | decimal | S | — | ні | Σ позицій | серверна сума у валюті Bill; клієнтський total зараз довірений; точне округлення D-03 OPEN | immutable | IMPLEMENTED Bill.TotalAmount; target BR-06/13 |
| status | BillStatus | S | S | ні | Pending | лише матриця §5; чинний API приймає Status з body і довільний PUT | server | IMPLEMENTED Bill.Status; Declined NOT IMPLEMENTED |

### 4.5. BillItem

Джерело: [Entities/Models/BillItem.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/BillItem.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| billId | ulong | S | — | ні | створена Bill.Id | Bill існує; не змішувати позиції різних власників | immutable | IMPLEMENTED BillItem.BillId |
| productId | ulong | Y | — | ні | немає | Product існує; оплачений товар ще не належить власнику; зараз відсутній Product просто пропускається | immutable | IMPLEMENTED BillItem.ProductId |
| quantity | int | S | — | ні | 1 | рівно 1 за Q-06; зараз довільний int без Range | immutable | IMPLEMENTED BillItem.Quantity; target PROPOSED |
| priceAtPurchase | decimal | S | — | ні | серверна поточна ціна | знімок; DTO входу Price → PriceAtPurchase, DTO виходу Price; зараз клієнт задає | immutable | IMPLEMENTED BillItem.PriceAtPurchase; ADR-03 частково |

### 4.6. License

Джерело: [Entities/Models/License.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/License.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productId | ulong | S | — | ні | BillItem.ProductId | узгоджений із BillItem; наявний Product | immutable | IMPLEMENTED License.ProductId |
| billItemId | ulong | S | — | ні | оплачена позиція | лише власна Paid/Completed Bill; зараз у бібліотеку завантажуються всі License Product | immutable | IMPLEMENTED License.BillItemId; фільтрація E |
| licenseKey | string | S | — | ні | 4 групи по 4 hex | генерує StripeService; унікальність у сховищі не гарантована; не публікувати чужому користувачу | immutable | IMPLEMENTED License.LicenseKey |
| status | string | S | S | ні | Active | enum відсутній; інші значення/життєвий цикл OPEN | server | IMPLEMENTED License.Status |
| expiresAt | DateTime? | S | S | так | null | UTC; строк дії не погоджений, у потоці не встановлюється | server | IMPLEMENTED License.ExpiresAt |

### 4.7. PaymentOrder

Джерело: [Entities/Models/PaymentOrder.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/PaymentOrder.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| providerTransactionId | string | S | — | ні | Stripe charge.id | унікальний ключ дедуплікації PROPOSED; зараз check-then-write | immutable | IMPLEMENTED PaymentOrder.ProviderTransactionId |
| provider | string | S | — | ні | Stripe | не клієнтське поле | immutable | IMPLEMENTED PaymentOrder.Provider |
| success | bool | S | — | ні | true у success-path | лише підтверджений результат провайдера; false-path не записується | immutable | IMPLEMENTED PaymentOrder.Success |
| amountInMinorUnits | decimal | S | — | ні | charge.Amount | фактично integer minor units у decimal; звіряти з Bill/валютою PROPOSED | immutable | IMPLEMENTED PaymentOrder.AmountInMinorUnits |
| currency | string | S | — | ні | charge.Currency upper | перевірити збіг із Bill PROPOSED | immutable | IMPLEMENTED PaymentOrder.Currency |
| tokensAmount | int | S | — | ні | 0 у Capture | поле спадщини; не AI-токени, призначення OPEN | server | IMPLEMENTED PaymentOrder.TokensAmount |
| deliveredAt | DateTime | S | — | ні | UtcNow | UTC; не доказ атомарної доставки | server | IMPLEMENTED PaymentOrder.DeliveredAt |
| userId | ulong | S | — | ні | JWT User.Id у Capture | звіряти з Bill.UserId/Stripe metadata PROPOSED; update-status зараз лишає 0 | immutable | IMPLEMENTED PaymentOrder.UserId; розбіжність E |

### 4.8. Region

Джерело: [Entities/Models/Region.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/Region.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| name | string | — | — | ні | немає | межі й управління поза API ЛР 1; не трактувати як жанр | reference | IMPLEMENTED Region.Name |
| code | string | — | — | ні | немає | довжина/регістр/унікальність OPEN | reference | IMPLEMENTED Region.Code |

### 4.9. ImageFile

Джерело: [Entities/Models/ImageFile.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/ImageFile.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| path | string | S | — | ні | storage result | не приймати довільний шлях у Product PATCH; URL будує FileService | server | IMPLEMENTED ImageFile.Path |
| fileName | string | S | — | ні | ім’я upload | нормалізація FileService/storage; бізнес-межа довжини OPEN | server | IMPLEMENTED ImageFile.FileName |
| mimeType | string | S | — | ні | upload metadata | перевірка type/signature у файловому потоці; не доводить придбання | server | IMPLEMENTED ImageFile.MimeType |
| width | int? | S | — | так | null | якщо відома &gt;0 PROPOSED | server | IMPLEMENTED ImageFile.Width |
| height | int? | S | — | так | null | якщо відома &gt;0 PROPOSED | server | IMPLEMENTED ImageFile.Height |
| userId | ulong? | S | — | так | null | власник аватара; зв’язок без FK Firebase | server | IMPLEMENTED ImageFile.UserId |
| productId | ulong? | S | — | так | null | товар зображення; для avatar не Product | server | IMPLEMENTED ImageFile.ProductId |

### 4.10. Favorite

Джерело: [Entities/Models/Favorite.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Models/Favorite.cs#L1). Поля id/createdAt/updatedAt успадковують §4.1.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| userId | ulong | — | — | ні | із JWT у favorite-flow | обране відкладено для ЛР 1 | server / F | IMPLEMENTED Favorite.UserId |
| productId | ulong | — | — | ні | із path | обране відкладено; не право на придбання | server / F | IMPLEMENTED Favorite.ProductId |

### 4.10a. Навігаційні властивості (не wire-поля)

Усі мають JsonIgnore, null за CLR default; їх збирають вручну. Зміна в пам’яті не означає окреме збереження навігації.

| Field | Type | C | U | Nullable | Default | Validation / Normalization | Mutable | Source / implementation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| User.AvatarFile | ImageFile? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED User.cs: AvatarFile |
| User.Bills | ICollection&lt;Bill&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED User.cs: Bills |
| Product.Region | Region? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Product.cs: Region |
| Product.BillItems | ICollection&lt;BillItem&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Product.cs: BillItems |
| Product.Files | ICollection&lt;ImageFile&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Product.cs: Files |
| Product.CoverFile | ImageFile? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Product.cs: CoverFile |
| Product.Licenses | ICollection&lt;License&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Product.cs: Licenses |
| Bill.User | User? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Bill.cs: User |
| Bill.BillItems | ICollection&lt;BillItem&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Bill.cs: BillItems |
| BillItem.Bill | Bill? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED BillItem.cs: Bill |
| BillItem.Product | Product? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED BillItem.cs: Product |
| License.Product | Product? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED License.cs: Product |
| License.BillItem | BillItem? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED License.cs: BillItem |
| PaymentOrder.User | User? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED PaymentOrder.cs: User |
| Region.Products | ICollection&lt;Product&gt;? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Region.cs: Products |
| ImageFile.User | User? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED ImageFile.cs: User |
| ImageFile.Product | Product? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED ImageFile.cs: Product |
| Favorite.User | User? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Favorite.cs: User |
| Favorite.Product | Product? | S | S | так | null | Збирає сервіс із ID-посилань; не приймати в body; не серіалізувати сутність; FK не гарантований Firebase | server-only assembly | IMPLEMENTED Favorite.cs: Product |

### 4.11. Запити, DTO й незбережені поняття

| Поняття / поле | Тип / C / U / null / default | Валідація, нормалізація, змінність | Статус / відповідник |
| --- | --- | --- | --- |
| Registration.name | string? / N / — / так / null | create-only; якщо whitespace сервер бере префікс email | IMPLEMENTED UserRegisterDTO.Name → User.Username |
| Registration.email | string / Y / — / ні / немає | правило User.email; чинний DTO nullable | CONFIRMED / IMPLEMENTED частково |
| Registration.password | string / Y / — / ні / немає | ≥8; без trim; create-only, ніколи в response | Q-11 PROPOSED; поточний UserRegisterDTO.Password без MinLength |
| Registration.passwordConfirmation | string / Y / — / ні / немає | має збігатися, не зберігається, create-only | PROPOSED поле розширення того самого DTO; зараз тільки confirmPassword state UI |
| Login.email / password | string / Y / — / ні / немає | email як вище; пароль точне значення; відсутні/пусті відхилити | IMPLEMENTED DTO nullable; поточні винятки див. API |
| googleJwtToken | string? / N / — / так / null | лише окрема OAuth-гілка; поза обсягом | IMPLEMENTED / F у register/login DTO |
| Cart.items[].productId | ulong / Y / P / ні / немає | існуючий Product; незмінний ключ позиції; локально game.id | PROPOSED серверний CartItem; поточний Redux CartItem |
| Cart.items[].quantity | int / S / — / ні / 1 | рівно 1; поточний reducer збільшує кількість | PROPOSED / Q-06; поточне CartItem.quantity |
| Cart.userId | ulong / S / — / ні / JWT | власник; серверний ключ кошика; immutable | PROPOSED; поточний cartItems localStorage НЕ розділений за User |
| Cart.items[].unitPrice / Cart.totalAmount / Cart.currency | decimal / decimal / string; S / S / ні | обчислювані поточні ціни/сума; не право власності; UAH запропоновано | PROPOSED серверна відповідь; зараз calculateTotal в UI |
| PaymentUpdate.paymentIntentId | string / Y / — / ні / empty у DTO | справжній pi_* id, не client_secret; звіряти metadata з власником | IMPLEMENTED UpdatePaymentRequest.PaymentIntentId; ownership target PROPOSED |
| PaymentUpdate.paymentMethod | string / N / — / ні / empty | Stripe pm_* або empty; не номер картки; одноразовий запит | IMPLEMENTED UpdatePaymentRequest.PaymentMethod |
| PaymentUpdate.action | string / N / — / ні / confirm | тільки confirm/cancel PROPOSED; код інші значення ігнорує | IMPLEMENTED UpdatePaymentRequest.Action |
| Bill.attemptCount / attemptId / providerEventId | int / string / string; S / S / ні; 0 для count | серверні дані PROPOSED для блокування й дедуплікації; не в чинних DTO | NOT IMPLEMENTED; не додано вигаданої чинної сутності |
| Library | ProductDto[] / read-only | похідне подання BR-08, не таблиця Library | IMPLEMENTED UserRepository.GetUserProductsByIdAsync |
| Product.isDeleted | bool / S / S / ні / false | лише варіант soft delete після погодження, не поле поточного коду | PROPOSED альтернатива D-01; основний варіант — заборона DELETE |

Про повні wire-схеми ProductDto, BillDto, UserDto, UserProfileDTO, ProductFileDto, Create/UpdateProductDto див. [API §2](api-contract.md). Навігаційні User/Bills, Bill/BillItems, BillItem/Product, Product/Region/Files/Licenses і License/BillItem мають [JsonIgnore] у сутностях; їх читають/збирають сервіси явно. Це логічні посилання, не автоматично завантажені FK. Списки в DTO можуть бути [] або (у неповному мапінгу Bill/Profile) null; ціль — [] для колекцій PROPOSED.

### 4.12. Відсутність, null і помилкові значення

Цільова політика PROPOSED, крім джерельної заборони невалідних змін. Реальні винятки описані в API.

| Вхід | Create / обов’язкове | Create / optional | Admin PATCH |
| --- | --- | --- | --- |
| Поле відсутнє | 400 ValidationProblemDetails; без запису | взяти задокументований default | не змінювати |
| null | 400; без запису | лише nullable; інакше 400 | очистити тільки nullable releaseDate; інші scalar null →400 |
| Порожній / whitespace string | для name/email/password відхилити; пароль не trim | description/developer/publisher/category: empty дозволено PROPOSED | name/email whitespace відхилити; description може стати empty |
| Неправильний JSON type | 400 до сервісу | 400 до сервісу | 400 до будь-якого запису |
| Невалідний діапазон/значення | 400; відсутній referenced id →404 | так само | 400/404 відповідно, атомарно |
| Unknown / server-owned поле | 400 PROPOSED | 400 PROPOSED | 400 PROPOSED, жодна зміна не зберігається |
| {} | 400 для обов’язкових | лише якщо операція справді має defaults | 400 no changes |
| Порожнє HTTP body | 400 | не еквівалент {} | 400 |

## 5. Матриця станів

Навчальні стани: PENDING, PROCESSING, DECLINED, PAID, COMPLETED. Wire/код наявних еквівалентів: Pending, Processing, Paid, Completed. У чинному BillStatus також Cancelled і Refunded; Declined відсутній. Cancelled ≠ відмова платіжної спроби; Refunded — окремий майбутній сценарій, не прихований шлях PAID → DECLINED. Для цільового API пропонується додати Declined до існуючого enum без перейменування чотирьох наявних значень. Ця зміна NOT IMPLEMENTED.

Д — дозволений; Т — повтор тієї самої ідентифікованої події без повторних ефектів; Н — заборонений. Н не викликає провайдера, повертає 409, не змінює права.

| Звідки / куди | PENDING | PROCESSING | DECLINED | PAID | COMPLETED |
| --- | --- | --- | --- | --- | --- |
| PENDING | Т | Д | Н | Н | Н |
| PROCESSING | Н | Т | Д | Д | Н |
| DECLINED | Н | Д | Т | Н | Н |
| PAID | Н | Н | Н | Т | Д |
| COMPLETED | Н | Н | Н | Н | Т |


| Перехід | Подія / ініціатор | Передумова | Побічний ефект / бібліотека | Помилка / повтор |
| --- | --- | --- | --- | --- |
| створення → PENDING | checkout / власник через BillService | непорожньо, доступні товари, одна копія, немає активної резервації | серверний знімок Bill/Items; прав ще немає | 400/404/409; повтор create без idempotency key не гарантовано no-op; target key OPEN |
| PENDING → PROCESSING | start payment / власник | JWT власника, атомарно зайнята спроба, сума знімка | запис attempt до зовнішнього виклику; доступу немає | друге підтвердження 409; той самий start-key повертає існуючу спробу |
| DECLINED → PROCESSING | retry / власник | та сама Bill, новий attemptId, повторна перевірка належності/резервації | count+1, нова спроба без зміни суми; без доступу | не нова Bill; дублікат того самого retry-key no-op |
| PROCESSING → DECLINED | достовірна відмова / адаптер | подія відповідає активній спробі й власнику | покупка не видана; кошик/раніше придбані права лишаються | дубль тієї самої eventId → успішний no-op; stale подія іншої спроби →409 |
| PROCESSING → PAID | підтверджений результат / адаптер | провайдер succeeded, валюта/сума/власник збігаються, унікальний charge | Bill та право власника зафіксовані атомарно; потрібна відновлювана доставка License | дубль тієї самої події →200 без другого ключа/бонусу; частковий збій recovery OPEN |
| PAID → COMPLETED | завершення доставки / сервіс | оплата вже підтверджена; післяумови доставки виконані | доступ зберігається | повтор completion-event no-op; назад Н |
| X → X | повтор ідентичної події / сервіс | eventId/attemptId збігається з уже застосованим | жодних нових записів/списань/ключів | довільний новий confirm не є повтором події; для PROCESSING/PAID/COMPLETED →409 |

Ідемпотентна подія повідомляє вже встановлений факт; новий confirm є командою на фінансову дію. Діагональ Т не дозволяє знову списати кошти. Зовнішній платіж і Firebase не мають спільної ACID-транзакції: потрібні локальна атомарна зміна, durable attempt/dedup та recovery, а не вигадана розподілена транзакція.

Фактичний код: create intent лишає Bill Pending, capture ставить Pending → Paid; немає блокування Processing, збереженої Declined, attemptCount, webhook або completion-переходу. Update-status може записати PaymentOrder до capture й тим заблокувати capture як повтор. Повна відповідність матриці NOT IMPLEMENTED; деталі у [аудиті](implementation-audit.md).

## 6. Невирішені наскрізні випадки

| Випадок | Факт коду | Ціль / статус |
| --- | --- | --- |
| Вилучення придбаної гри | DELETE видаляє тільки Product у Firebase; BillItem/License лишаються; бібліотека фільтрує наявні Product, історія може впасти на bi.Product.Id | BR-10, D-01 OPEN: блокувати будь-яке історичне посилання; soft delete альтернатива |
| Кошик після оформлення | локальний cartItems; очищення всього кошика після onPaymentSuccess, відмова його не очищає | BR-09, D-02 OPEN: очищати лише оплачені позиції після серверного Paid; не після create |
| Декілька неоплачених Bill | кожне відкриття/перемонтування PaymentForm може створити нову Bill; сервер не забороняє | BR-12, D-04 OPEN: резервація та конфлікт 409; існуючі дублікати перевіряти перед оплатою |
| Конкурентна повторна купівля | немає unique/CAS/transact; .Distinct() лише приховує дублікати в поданні | BR-12: атомарний claim пари та charge/event; алгоритм recovery OPEN |
| Зміна ціни | PriceAtPurchase є, але приходить від клієнта; TotalAmount теж; пізніший Product.Price може змінитися | BR-13/ADR-03: серверний знімок, не перераховувати створену Bill; rounding D-03 OPEN |
| Порядок списків | Bill/user: CreatedAt DESC; каталог і бібліотека без OrderBy; frontend має опційні сортування | BR-14/D-05 OPEN; не стверджувати гарантований порядок чинного API |

## 7. Нефункціональні вимоги

Усі NFR — перевірювані цільові критерії з PDF с.2; виконання NOT VERIFIED. Числових performance-SLA без джерела не введено.

| ID | Критерій | Метод і об’єктивний oracle | Стан |
| --- | --- | --- | --- |
| NFR-01 | Усі дії основного потоку доступні клавіатурою, focus видимий; звичайний текст ≥4.5:1 | TC-NFR-01: пройти register→catalog→cart→payment→library без миші, облік кожної дії; вимір кожного text/background pair. Жодної недоступної дії/пари нижче 4.5:1. | NOT RUN |
| NFR-02 | Створені User і Bill/Items зберігаються після перезапуску | TC-NFR-02: прочитати ID/поля, перезапустити із тією самою тестовою Firebase, прочитати знов; рівність бізнес-полів. Наявність зовнішнього сховища не є результатом тесту. | NOT RUN |
| NFR-03 | Помилкові PATCH/оплата/неавторизовані операції не змінюють даних чи старих прав | TC-NFR-03: знімок усіх пов’язаних записів до/після; рівність для відхилених операцій, 1 purchase при конкуренції; fault injection між записами. | NOT RUN |
| NFR-04 | Паролі не повертаються/не зберігаються відкрито; секрети не у tracked-файлах чи клієнтських логах | TC-NFR-04: перевірити всі auth/profile/API responses, тестове сховище, git-tree й browser console. Статично знайдено unsalted SHA-256 та token log; це не повний runtime security test. | NOT RUN; статичні дефекти у аудиті |

## 8. Узгодження та команда

Input Pack, Product Baseline, Decision Log, TEAM і UX/UI QA тепер отримано й зіставлено. Первинні 33 AC мають перевірене походження; реконструкції попередньої редакції виправлено. Q-06–Q-11 у новому UX-репозиторії мають PROPOSED, а не колишній OPEN. Погодження конкретного P-рішення не зафіксовано: reviewer/date/decision порожні. Задані SRC/початкові AC не залишено штучно OPEN; відкриті тільки нові політики/конфлікти.

За прямим підтвердженням користувача всі четверо учасників ЛР 1 — Паламарчук Антон, Татьков Олександр, Сергєєва Таісія, Панковський Тимофій — виконали перехресну перевірку вимог, AC, архітектури, API та простежуваності. Персональних зауважень/дати/коміту не вигадано. [Підстава](../sources/team-review-confirmation.txt). Це не тотожне затвердженню P-01–P-08 або перевірці виправленого продуктового коду. Аналіз кожного до AI та захист ЛР 1 підтверджуються окремо.
