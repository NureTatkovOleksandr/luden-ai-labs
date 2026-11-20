# Зіставлення вимог і реалізації

Фінальна повторна перевірка 20.11.2026: fetch підтвердив ті самі актуальні HEAD backend/frontend; критичні гілки коду перечитані. Аудит статичний. Класи A–F та значення IMPLEMENTED визначено у [джерелах](sources.md). Наявність коду не доводить проходження сценарію; всі runtime-висновки NOT VERIFIED. Зміни backend/frontend не вносились.

## Функції та класи розбіжностей

| Функція | Вимога | Backend | Frontend | Документація / розбіжність |
| --- | --- | --- | --- | --- |
| Акаунт і вхід | SRC-01 | IAuthorizationService → UserRepository; JWT; [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1) | register→login; [src/pages/RegistrationPage/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/RegistrationPage/index.tsx#L1) | A/B/E: механізм уточнено; ≥8/confirmation API відсутні |
| Каталог і деталі | SRC-02 | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); GetAll/GetById | StorePage + GameDetailsModal; [src/pages/StorePage/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/StorePage/index.tsx#L1) | A/B/C: API публічний, фільтрує UI; error/retry usability runtime не перевірено; AND може скидатися discount-гілкою |
| Кошик | SRC-03 | Серверної сутності/маршруту немає; це не самостійне порушення SRC-03 | [src/entities/Cart/model/cartSlice.ts:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/entities/Cart/model/cartSlice.ts#L1) | C/E: localStorage, quantity&gt;1, ключ не залежить від User |
| Оформлення | SRC-03/04 | [Application/Services/BillService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/BillService.cs#L1) | PaymentModal створює реальну Bill; [src/components/PaymentModal/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/components/PaymentModal/index.tsx#L1) | E: клієнт задає суму/owner/status; пусті/дубльовані позиції не відхиляються |
| Оплата | SRC-04 | [Application/Services/StripeService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/StripeService.cs#L1) | Stripe Elements → confirmCardPayment → complete; [src/services/PaymentService.ts:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/services/PaymentService.ts#L1) | B/E: Stripe-код є, фінансова працездатність NOT VERIFIED; матриця/повтори/атомарність відсутні |
| Бібліотека | SRC-05 | [Infrastructure/Repositories/UserRepository.cs:97](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Infrastructure/Repositories/UserRepository.cs#L97) | ProfilePage useGetUserProductsQuery; [src/pages/ProfilePage/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/ProfilePage/index.tsx#L1) | A для фільтра Paid/Completed; E для витоку License і обходу оплати через Bill |
| Admin | SRC-06 | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); перевірка User.Role.Admin | StorePage ProductModal викликає POST form/PUT JSON/DELETE | A для role-check; C для PATCH; контракт missing/null не виконано |
| OAuth/обране/профіль/бонуси/валюти/Android | відкладено | OAuth/Favorite/Bonus код є | Router, favorite hooks, currencySlice, android/ | D/F: наявні напрацювання збережено поза обсягом; не оголошено обов’язковими |
| Reset password / рекомендація | SRC-07 / ЛР 4 | Потрібного email reset/LLM service не знайдено | ForgotPasswordPage не доводить email-delivery; Recommendations navigation не доводить AI | F: не включено до поточного релізу |

## Реєстр суттєвих розбіжностей

### GAP-01 — Critical — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-03/06: власник і ціни/статус серверні |
| Факт / проблема | BillController POST приймає UserId/TotalAmount/Status, PUT дозволяє перезаписати Bill; немає звірки токена. User може задати Paid і вплинути на похідну бібліотеку без перевіреної оплати. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [Application/Services/BillService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/BillService.cs#L1) |
| Рекомендоване рішення | Не приймати ці поля як довірені; обмежити мутації матрицею та JWT-власником. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-02 — Critical — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-03: тільки власні покупки |
| Факт / проблема | GET Bill, GET Bill/{id}, PUT/DELETE Bill/{id} мають лише Authorize; User profile/{id}/delete також без owner/Admin-перевірок. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1) |
| Рекомендоване рішення | Закрити загальні маршрути ролями, приватні — перевіркою власника; foreign id →404. Додатковий доказ UserController. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-03 — Critical — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-03/07: власник платежу й замовлення збігаються |
| Факт / проблема | Stripe create перевіряє Bill.UserId, але update-status не отримує userId, capture не порівнює Bill.UserId/metadata user_id із JWT. |
| Код | [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1); [Application/Services/StripeService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/StripeService.cs#L1) |
| Рекомендоване рішення | Звіряти ownership і суму/валюту на всіх гілках, не лише create. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-04 — Critical — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-08: ключі лише власних покупок |
| Факт / проблема | UserRepository завантажує всі License з ProductId; UserController повертає їх у ProductDto. Користувач одного Product потенційно бачить ключі чужих BillItem того самого Product. |
| Код | [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1); [Infrastructure/Repositories/UserRepository.cs:159](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Infrastructure/Repositories/UserRepository.cs#L159) |
| Рекомендоване рішення | Фільтрувати License до BillItem власних Paid/Completed Bill або віддати окремий owner DTO. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-05 — Critical — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-07/12: атомарність і повтори |
| Факт / проблема | Capture спочатку ставить Paid, потім окремо пише SalesCount/License/bonus/PaymentOrder. Check transactionId і запис не атомарні; збій або race дає часткові ефекти/дублі. |
| Код | [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1); [Application/Services/StripeService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/StripeService.cs#L1) |
| Рекомендоване рішення | Durable payment attempt + atomic local claim/dedup + recovery; concurrency/fault-injection тести. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-06 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-05 / Q-06: одна копія |
| Факт / проблема | Redux addToCart збільшує quantity; BillService приймає будь-яку Quantity і не перевіряє вже придбане. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [src/entities/Cart/model/cartSlice.ts:35](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/entities/Cart/model/cartSlice.ts#L35) |
| Рекомендоване рішення | Узгодити Q-06, встановити quantity=1, серверну перевірку owned і резервацію. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-07 — Major — C/E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-07: п’ять станів, retry |
| Факт / проблема | BillStatus не має Declined; create intent лишає Pending, capture Pending→Paid; Processing/Completed не встановлюються цим потоком. |
| Код | [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1); [Entities/Enums/BillStatus.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Entities/Enums/BillStatus.cs#L1) |
| Рекомендоване рішення | Упровадити прийняту матрицю в BillService; не називати Cancelled відмовою. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-08 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-07: ідемпотентне завершення |
| Факт / проблема | UpdatePaymentStatusAsync записує PaymentOrder при succeeded без UserId/Bill Paid; Capture відхиляє існуючий transactionId. Дві гілки конфліктують. |
| Код | [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1); [Application/Services/StripeService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/StripeService.cs#L1) |
| Рекомендоване рішення | Єдина оркестрація фіналізації, збережений результат повтору; сумісно із наявним UI confirmCardPayment→complete. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-09 — Major — E/C

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-02: ≥8 і confirmation |
| Факт / проблема | Register DTO не має MinLength/confirmation; UI звіряє confirmation, але у JSX minLength і в handler length-check не знайдено. |
| Код | [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1); [Application/DTOs/UserDTOs/UserRegisterDTO.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/DTOs/UserDTOs/UserRegisterDTO.cs#L1); [src/pages/RegistrationPage/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/RegistrationPage/index.tsx#L1) |
| Рекомендоване рішення | Додати перевірку ≥8 до форми/API та presence-aware confirmation у DTO. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-10 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-10: не руйнувати історію/права |
| Факт / проблема | DELETE Product фізично видаляє запис, не перевіряє BillItem/License; бібліотека пропускає відсутній Product, Bill MapToDto може звернутися до null Product. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [Infrastructure/Repositories/GenericRepository.cs:96](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Infrastructure/Repositories/GenericRepository.cs#L96); [Infrastructure/Repositories/UserRepository.cs:137](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Infrastructure/Repositories/UserRepository.cs#L137) |
| Рекомендоване рішення | Заборона DELETE при історичних посиланнях як мінімальний варіант; soft delete після міграції. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-11 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | NFR-03: помилка сховища не успіх |
| Факт / проблема | GenericRepository логуює failed writes без throw; GetAllAsync перетворює помилку/десеріалізацію на empty. API може повернути успіх/[] після збою. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [Infrastructure/Repositories/GenericRepository.cs:63](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Infrastructure/Repositories/GenericRepository.cs#L63) |
| Рекомендоване рішення | Повертати явний failure, зупиняти бізнес-потік, 503 замість удаваного пустого каталогу. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-12 — Major — E/C

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-11: повний PATCH |
| Факт / проблема | ProductController має PUT, PATCH немає; missing/null нерозрізненні, {} змінює timestamp, unknown ігнорується; mixed invalid Range відхиляється до запису. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [Application/Services/ProductService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/ProductService.cs#L1); [Application/DTOs/ProductDTOs/UpdateProductDto.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/DTOs/ProductDTOs/UpdateProductDto.cs#L1) |
| Рекомендоване рішення | Presence-aware PATCH на тому самому /api/Product/{id}; валідація всього входу перед записом; існуючий PUT задокументувати. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-13 — Major — E (ізоляція/checkout); server Cart — OPTIONAL

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-05: власний серверний кошик |
| Факт / проблема | Є тільки Redux/localStorage cartItems, без ключа UserId; серверних Cart entity/controller/repository немає. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [src/entities/Cart/model/cartSlice.ts:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/entities/Cart/model/cartSlice.ts#L1) |
| Рекомендоване рішення | Прийняти D-04: зберегти локальний кошик із серверною перевіркою checkout або додати Cart; не вважати поточний кошик серверним. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-14 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-06/13: серверний знімок ціни |
| Факт / проблема | PriceAtPurchase зберігається, але копіює itemDto.Price, total із body; немає перевірки суми, позитивної quantity, пустого складу, пропущені missing Product. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [Application/Services/BillService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/BillService.cs#L1) |
| Рекомендоване рішення | Обчислити сервером за погодженим rounding/discount; усі Items валідні до одного атомарного запису. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-15 — Major — E/D/F

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Обсяг ЛР 1: бонуси/валюти відкладено |
| Факт / проблема | UI дозволяє bonusPointsUsed і перемикання валют, BillService списує бонуси до створення Bill; при відмові немає автоматичного відновлення. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [src/widgets/Cart/ui/Cart.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/widgets/Cart/ui/Cart.tsx#L1); [Application/Services/BillService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/BillService.cs#L1) |
| Рекомендоване рішення | У поточному релізі блокувати списання, не вважати наявність коду зміною вимог; D-03 узгодити валюту. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-16 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | NFR-04: захист облікових даних |
| Факт / проблема | Sha256PasswordHasher — один SHA-256 без salt/work factor; PaymentModal друкує Raw token у browser console. |
| Код | [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1); [Application/Services/Sha256PasswordHasher.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/Sha256PasswordHasher.cs#L1); [src/components/PaymentModal/index.tsx:99](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/components/PaymentModal/index.tsx#L99) |
| Рекомендоване рішення | Мігрувати парольний hash на password KDF окремою технічною зміною; прибрати token log. Відкритий пароль у response не знайдений статично. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-17 — Major — C/E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Доступність API незалежно від launch environment |
| Факт / проблема | UseAuthentication/Authorization/MapControllers/Run поміщені всередину IsDevelopment. Для Production гілки нормального запуску в цьому Program немає. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [LudenWebAPI/Program.cs:191](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Program.cs#L191) |
| Рекомендоване рішення | Винести загальний pipeline/Run за межі Development; фактичний запуск NOT VERIFIED. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-18 — Minor — B — FIXED у документації

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Документація враховує існуючий стек |
| Факт / проблема | Стара робота заявляє відсутній сервіс, UUID, Account/Game/Order, вигадані маршрути й 422. Реальний стек/сутності/коди інші. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [Application/Services/ProductService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/ProductService.cs#L1) |
| Рекомендоване рішення | Виправлено документами; джерела прив’язані до commit. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-19 — Minor — E/C

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | BR-04: AND і коректний жанр |
| Факт / проблема | StorePage text+genre послідовно filter, але Under 10€ гілка повторно бере games, скидаючи обидва фільтри; fallback region.name використовується як genre. На API фільтрів немає. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [src/pages/StorePage/index.tsx:318](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/StorePage/index.tsx#L318) |
| Рекомендоване рішення | Не скидувати filtered; category не підміняти Region; вирішити місце фільтрації. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-20 — Minor — C/E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Повнота DTO й money-контракту |
| Факт / проблема | BillDto без currency; GetBillDtoById не гідрує BillItems; різні мапери повертають неповний ProductDto; ProductDto.RegionId int? замість ulong. |
| Код | [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1); [Application/DTOs/BillDTOs/BillDto.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/DTOs/BillDTOs/BillDto.cs#L1); [Application/Services/BillService.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/Application/Services/BillService.cs#L1) |
| Рекомендоване рішення | Узгодити один безпечний мапер і явне currency; повертати persisted Items у create/get. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-21 — Minor — B/C

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Q-09: сесія після реєстрації |
| Факт / проблема | Backend register200 Success, UI виконує окремий login і зберігає JWT. Атомарного register+session немає; будь-який 400 UI може сприйняти як зайнятий email. |
| Код | [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1); [src/pages/RegistrationPage/index.tsx:1](https://github.com/Timbuhtuk/Luden-Front-End/blob/ea90e7f465012d78d2f0593ad745ffb0ea07106c/src/pages/RegistrationPage/index.tsx#L1) |
| Рекомендоване рішення | Задокументовано фактичні два запити; обробляти код причини, погодити гарантію при login failure. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |

### GAP-22 — Major — E

| Аспект | Зміст |
| --- | --- |
| Правило / твердження | Надійна версія/збірка |
| Факт / проблема | У LudenWebAPI вкладено дублікати Application/Entities/Infrastructure та LudenWebAPI/LudenWebAPI; Web csproj без явних Compile Remove для них. Можливі дублікати типів/entrypoint. |
| Код | [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1); [LudenWebAPI/LudenWebAPI.csproj:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/LudenWebAPI.csproj#L1); [LudenWebAPI/LudenWebAPI/Program.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/LudenWebAPI/Program.cs#L1) |
| Рекомендоване рішення | Окремо перевірити build і прибрати дублювання з compile items; це статичний ризик, build NOT RUN. |
| Перевірка | Статичний огляд IMPLEMENTED; відтворення на сервісі NOT RUN; виправлення коду не виконано |


## Сховище, FK і конкурентність

Program реєструє FirebaseService/FirebaseRepository і Firebase-backed GenericRepository. PostgreSQL/Npgsql, SQLite/EF Core та старі міграції є в packages/дереві, але active Program не реєструє DbContext чи UseSqlite/UseNpgsql. Не можна називати SQL FK або migration cascade активними гарантіями Firebase. Сервіси збирають зв’язки вручну; FirebaseService робить прості REST GET/PUT/DELETE без ETag/If-Match, Firebase transaction чи multi-location atomic update. Унікальність email, charge, пари User/Product не захищена атомарним записом. ID-генерація timestamp+random із попереднім GET також не є atomic unique constraint.

Невдала оплата на Stripe і невдале локальне збереження — різні події: після provider succeeded не можна просто повернути DECLINED і забути charge. Потрібний стан recovery/durable delivery, узгодження його представлення OPEN у D-06.

## Доказовий статус після повторного огляду

CONFIRMED тут означає кодовий факт, POTENTIAL — можливий вплив до runtime-відтворення. FIXED не використовується для невиправленого продукту. У source Git не з’явилося нового виправлення: BE/FE HEAD незмінні; робочі дерева чисті.



Зовнішню Firebase, Stripe, GitHub file storage та реальні акаунти не використовували для запусків. Не створювали фінансових операцій, користувачів або товарів. Секрети не копіюються у звіт; результати окремого статичного сканування — у [validation.md](validation.md). Це не security certification.
| Проблема | Статус доказу | Що підтверджено / практична межа |
| --- | --- | --- |
| GAP-01 | CONFIRMED | body задає userId/amount/status; немає server-owned захисту; надання доступу через підроблений Paid — POTENTIAL runtime-вплив |
| GAP-02 | CONFIRMED | Bill GET/PUT/DELETE й довільні User-маршрути без ownership-check; розкриття/видалення чужого — POTENTIAL до запуску |
| GAP-03 | CONFIRMED | create має owner-check, update-status/capture не перевіряють той самий owner на всіх гілках |
| GAP-04 | POTENTIAL | ProductId-only License-фільтр і передача до DTO CONFIRMED; реальний витік потребує набору чужих License/runtime |
| GAP-05 | CONFIRMED | окремі Paid/keys/bonus/payment writes, check-then-write; race/fault наслідки POTENTIAL |
| GAP-06 | CONFIRMED | qty+=1 і arbitrary quantity у Bill; невідповідність кандидату P-01, не доказ його прийняття |
| GAP-07/08 | CONFIRMED | Declined відсутній, update-status/capture гілки конфліктують статично |
| GAP-09 | CONFIRMED | DTO без MinLength/confirmation; ≥8 — робоче Q-11/P-03; source AC-01.4 вимагає лише UI mismatch block |
| GAP-10 | CONFIRMED | DELETE Product без історичних guards; втрата бібліотеки/падіння історії POTENTIAL |
| GAP-11/12 | CONFIRMED | hidden persistence failures; PUT без presence-aware PATCH; Range-negative блокується до service |
| GAP-13 | CONFIRMED / OPTIONAL | Cart локальний і не user-scoped; server Cart optional, server validation/security потрібні в будь-якому варіанті |
| GAP-14/15/16/17/19/20/21 | CONFIRMED | кодові гілки лишаються; масштаби runtime-впливу не тестувались |
| GAP-18 | FIXED | помилкові UUID/вигадані маршрути/відсутній backend виправлені документами; це не FIXED коду |
| GAP-22 | POTENTIAL | вкладені дублікати source/entrypoint; build не запускали, compile-failure не оголошено відтвореним |
| SCAN-01 | POTENTIAL | два config candidate SecretToken; значення/активність не перевіряли й не розкривали |

## Межі виконання

Продуктовий код не змінювали. Усі запропоновані виправлення backend/frontend — майбутня робота, а не результат цієї ЛР 1. Дані Figma QA використані як історичне UX-свідчення; не замінюють тести ownership/payment/license. Командне review поточної ЛР 1 підтверджене користувачем для чотирьох учасників, персональних findings чи результатів runtime-тестів не приписано.
