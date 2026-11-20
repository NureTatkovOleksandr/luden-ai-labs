# API-контракт Luden — чинний код і цільові уточнення

Редакція 20.11.2026. [Вимоги](requirements.md) — джерело правил. [Знімки й статуси](sources.md). Усі відповіді нижче виведено зі статичного коду; жоден HTTP-запит до працюючого сервісу не запускався. IMPLEMENTED означає наявну гілку коду, NOT VERIFIED — її виконання. Небезпечна наявна поведінка не стає нормативною вимогою.

## 1. Транспорт, сесія й помилки

Канонічний наявний префікс `/api`; ресурс гри називається Product, замовлення Bill. Старі `/games`, `/orders`, `/auth/*`, `/me/library` вилучені як несумісна вигадана альтернатива. URL середовища налаштовує frontend API_BASE_URL (localStorage apiBaseUrl → VITE_API_BASE_URL → /api). Публікація/доступність сервера NOT VERIFIED.

Authorization: `Bearer <JWT>`; JWT HS256, claims sub/NameIdentifier/Id/Role, issuer/audience/lifetime/signature перевіряються middleware. Тривалість береться з конфігурації, фіксованого числа тут не вигадано. Cookies/refresh tokens/session endpoint відсутні. UI зберігає authToken у localStorage; HTTP-клієнти читають також sessionStorage; ProfilePage guard читає лише localStorage. RegistrationPage робить register, потім login: автоматичний вхід залежить від двох запитів, register не повертає токен.

JSON поля API — camelCase, enum у відповідях — string через JsonStringEnumConverter; значення `Pending/Paid/...`, `User/Admin`. Числові enum-входи можуть десеріалізуватись; ціль — відхиляти невизначені enum PROPOSED. UTC/ISO-8601 є цільовим правилом, Bill create зараз змішує UtcNow і Now.

Уніфікованого error envelope у коді НЕМАЄ:

| Джерело | Чинна форма |
| --- | --- |
| Auth action | string (часто text/plain) Success, EmailBusy, IncorrectEmail тощо; JSON string можливий при negotiation |
| ApiController model binding / DataAnnotations | 400 ValidationProblemDetails: type, title, status, errors: map string→string[], traceId; фактичні dynamic поля NOT VERIFIED |
| Payment catch | 400 JSON {error:string} |
| Product/Bill/User catch | text/plain з текстом помилки, часто 500; можливе розкриття внутрішніх деталей |
| JWT challenge / Forbid | 401 / 403, зазвичай без body; це не JSON envelope |

Ціль: зберегти 400 для помилкових полів та {error:string} для платіжних бізнес-помилок; запропонувати 404 для відсутнього/чужого ресурсу, 409 для конфлікту/резервації/стану. Це PROPOSED, не чинні коди. 422 з попередньої роботи не підтверджено кодом і не використовується в цьому контракті.

## 1.1. Узгодження з початковими AC та UX-рішеннями

AC-02.4 — показ/приховування пароля на LoginPage; API для нього не потрібне. AC-06.3 — недоступний перехід порожнього кошика, AC-06.4 — його порожній стан. AC-07.1 відкриває форму оплати, не створює Bill за визначенням. AC-07.5 — скасування зі збереженням кошика, без нового HTTP cancel-маршруту. AC-08.1/08.4 — навігація profile→library→store. Retry same Bill, atomic price snapshot та JWT guards є окремими BR/EXT-гарантіями, не підміною цих початкових AC.

API-P01–API-P03 (server Cart) — необов’язковий архітектурний кандидат; наявний локальний Cart із перевіреним серверним checkout не суперечить сам по собі SRC-03. Strict PATCH API-P04 вимагає реальної зміни коду; чинний PUT не оголошується PATCH. Nullable releaseDate:null може очищати дату у target, інші nonnullable scalar null відхиляються; змішана помилка не зберігає жодного поля.

P-02 пропонує викликати POST Bill лише при першому confirm, а не при відкритті PaymentModal; поточний UI робить інакше. P-03 пропонує login→library, але source AC-02.2 і чинний UI — profile. Ці дві зміни PROPOSED, не приховано затверджені.

## 2. Wire-схеми

Синтаксис `T?` — допускає null у поточному DTO/мапінгу, `T[]` — масив; властивості наведено повністю. Вхідні missing/null/default та валідація визначені [контрактом даних](requirements.md); нижче зафіксовано саме wire-форму поточного коду.

### Схема UserRegisterDTO

| Field | Wire type / обмеження |
| --- | --- |
| name | string? |
| email | string?; email regex |
| password | string?; MinLength відсутній |
| googleJwtToken | string?; поза обсягом |

### Схема UserLoginDTO

| Field | Wire type / обмеження |
| --- | --- |
| email | string?; email regex |
| password | string? |
| googleJwtToken | string? |

### Схема ProductDto

| Field | Wire type / обмеження |
| --- | --- |
| name | string |
| description | string |
| price | decimal |
| stock | int |
| regionId | int? |
| discountPercentage | int |
| salesCount | int |
| developer | string |
| publisher | string |
| releaseDate | DateTime? |
| category | string |
| id | ulong |
| createdAt | DateTime |
| updatedAt | DateTime? |
| region | Region? (може бути null попри C# nonnullable) |
| coverUrl | string? |
| files | ProductFileDto[]; [] у ProductService |
| licenses | License[]; [] у ProductService |

### Схема ProductFileDto

| Field | Wire type / обмеження |
| --- | --- |
| path | string |
| fileName | string |
| mimeType | string |
| width | int? |
| height | int? |
| userId | ulong? |
| productId | ulong? |
| id | ulong |
| url | string? |

### Схема Region

| Field | Wire type / обмеження |
| --- | --- |
| id | ulong |
| name | string |
| code | string |
| createdAt | DateTime |
| updatedAt | DateTime? |

### Схема License

| Field | Wire type / обмеження |
| --- | --- |
| productId | ulong |
| billItemId | ulong |
| licenseKey | string |
| status | string |
| expiresAt | DateTime? |
| id | ulong |
| createdAt | DateTime |
| updatedAt | DateTime? |

### Схема BillDto

| Field | Wire type / обмеження |
| --- | --- |
| id | ulong |
| createdAt | DateTime |
| totalAmount | decimal |
| status | string |
| billItems | BillItemDto[]; [] коли не завантажено навігації |

### Схема BillItemDto

| Field | Wire type / обмеження |
| --- | --- |
| id | ulong |
| quantity | int |
| price | decimal; відповідає PriceAtPurchase |
| product | ProductDto; неповно заповнює BillService |
| licenseKeys | string[]; [] default |

### Схема UserDto

| Field | Wire type / обмеження |
| --- | --- |
| id | ulong |
| username | string |
| email | string |
| role | UserRole string |
| bonusPoints | decimal |
| createdAt | DateTime |
| updatedAt | DateTime? |

### Схема UserProfileDTO

| Field | Wire type / обмеження |
| --- | --- |
| username | string |
| email | string |
| role | UserRole string |
| bonusPoints | decimal |
| createdAt | DateTime |
| updatedAt | DateTime? |
| avatarUrl | string? |
| bills | BillDto[] |
| products | ProductDto[]; частковий мапінг із можливими null |

### Схема BillCreateDto

| Field | Wire type / обмеження |
| --- | --- |
| userId | ulong; missing →0 |
| totalAmount | decimal; missing →0 |
| status | BillStatus; missing →Pending |
| currency | string?; null/missing →UAH у controller |
| bonusPointsUsed | int; default0 |
| items | BillItemCreateDto[]?; null дозволено |

### Схема BillItemCreateDto

| Field | Wire type / обмеження |
| --- | --- |
| productId | ulong |
| quantity | int; default0, немає Range |
| price | decimal; default0, немає Range |

### Схема CreateProductDto

| Field | Wire type / обмеження |
| --- | --- |
| name | string; C=Y; Required create, ≤200; trim і відхилення whitespace PROPOSED; update зараз порожній рядок ігнорує |
| description | string; C=Y; ≤2000; explicit Required немає, nonnullable MVC може робити implicit required; trim PROPOSED; пустий опис PROPOSED дозволити |
| price | decimal; C=Y; ≥0.01; верхня межа CLR decimal, DTO double.MaxValue не уточнює бізнес-межі; 2 знаки й округлення OPEN; валюта на Product відсутня |
| stock | int; C=Y; 0..2147483647; цифрове значення запасу не доводить обмеження ліцензій |
| regionId | ulong; C=Y; &gt;0 і Region існує PROPOSED; перевірки існування у ProductService немає; DTO відповіді int? звужує ulong |
| discountPercentage | int; C=N; 0..100; точна участь у серверному розрахунку OPEN |
| developer | string; C=N; create null → empty; довжина OPEN; PATCH null відхилити PROPOSED |
| publisher | string; C=N; create null → empty; довжина OPEN; PATCH null відхилити PROPOSED |
| releaseDate | DateTime?; C=N; ISO date-time; цільовий null очищає дату; чинний PUT null ігнорує |
| category | string; C=N; один жанр; список жанрів у коді відсутній; мапа дозволених значень OPEN; trim PROPOSED |
| cover | IFormFile?; optional multipart, ≤10MiB, image/jpeg/jpg/png/gif/webp |

### Схема UpdateProductDto

| Field | Wire type / обмеження |
| --- | --- |
| name | string?; optional; null/missing ігноруються; Required create, ≤200; trim і відхилення whitespace PROPOSED; update зараз порожній рядок ігнорує |
| description | string?; optional; null/missing ігноруються; ≤2000; explicit Required немає, nonnullable MVC може робити implicit required; trim PROPOSED; пустий опис PROPOSED дозволити |
| price | decimal?; optional; null/missing ігноруються; ≥0.01; верхня межа CLR decimal, DTO double.MaxValue не уточнює бізнес-межі; 2 знаки й округлення OPEN; валюта на Product відсутня |
| stock | int?; optional; null/missing ігноруються; 0..2147483647; цифрове значення запасу не доводить обмеження ліцензій |
| regionId | ulong?; optional; null/missing ігноруються; &gt;0 і Region існує PROPOSED; перевірки існування у ProductService немає; DTO відповіді int? звужує ulong |
| discountPercentage | int?; optional; null/missing ігноруються; 0..100; точна участь у серверному розрахунку OPEN |
| developer | string?; optional; null/missing ігноруються; create null → empty; довжина OPEN; PATCH null відхилити PROPOSED |
| publisher | string?; optional; null/missing ігноруються; create null → empty; довжина OPEN; PATCH null відхилити PROPOSED |
| releaseDate | DateTime?; optional; null/missing ігноруються; ISO date-time; цільовий null очищає дату; чинний PUT null ігнорує |
| category | string?; optional; null/missing ігноруються; один жанр; список жанрів у коді відсутній; мапа дозволених значень OPEN; trim PROPOSED |

### Схема UpdatePaymentRequest

| Field | Wire type / обмеження |
| --- | --- |
| paymentIntentId | string; default empty |
| paymentMethod | string; default empty |
| action | string; default confirm |

ProductDto.regionId фактично int?, хоча модель Product.RegionId ulong; це окрема помилка звуження. Для ProductDto таблиця price описує значення decimal; у response немає власного currency. У BillDto НЕМАЄ userId, currency, updatedAt. BillDto ці поля не слід вигадувати в чинних прикладах. У запиті DTO називає ціну `price`, у збереженій BillItem — `PriceAtPurchase`.

У BillService.MapToDto і UserService.GetUserProfileAsync вкладені ProductDto заповнюються не повністю: невказані scalars мають CLR defaults, reference types можуть бути null; рівність із повним каталогом не гарантована. UserController.GetUserProducts дає повніший мапінг, але потенційно повертає чужі License. Ціль — один безпечний DTO-мапер, PROPOSED.

## 3. Контракти наявних операцій

В усіх операціях невказані query-параметри не мають задокументованої дії. Відповіді 500 не вважаються прийнятним бізнес-результатом. Чинне додавання/видалення кошика — локальні Redux-операції, HTTP-маршрутів немає.

### API-01: POST /api/Authorization/register

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-01 / AC-01 / BR-01–02 |
| Авторизація | публічно |
| Path / query / body / constraints | UserRegisterDTO: name?, email?, password?, googleJwtToken?; JSON. Для password-flow потрібні email/password, але DTO не має Required/MinLength. Regex email застосовується, якщо значення задано. Підтвердження в DTO відсутнє. |
| Успішна відповідь | 200 string Success; сесії немає |
| Помилки / error response | 400 string EmailBusy / UnknownOathProvider / InvalidToken; binding/regex →400 ValidationProblemDetails; неочікувана помилка →500 без стабільної схеми |
| Повтор | Повтор точного email →400 EmailBusy; race не закрито. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1) |

### API-02: POST /api/Authorization/login

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-01 / AC-02 / BR-03 |
| Авторизація | публічно |
| Path / query / body / constraints | UserLoginDTO: email?, password?, googleJwtToken?; JSON; password-flow email і password. |
| Успішна відповідь | 200 {token:string}; JWT HS256 |
| Помилки / error response | 400 string IncorrectEmail / IncorrectPassword / UnregisteredGoogle / UnknownOathProvider / InvalidToken; binding →400; можливий 500 |
| Повтор | Кожен правильний вхід генерує JWT; refresh/revoke/logout API немає. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/AuthorizationController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/AuthorizationController.cs#L1) |

### API-03: GET /api/Product

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-02 / AC-03–04 / BR-04 |
| Авторизація | публічно, AllowAnonymous |
| Path / query / body / constraints | Без body, path/query немає. query/genre у чинній action не приймаються й не фільтрують. |
| Успішна відповідь | 200 ProductDto[]; порожньо [] |
| Помилки / error response | 500 text: An error occurred while retrieving products: {message}; помилка Firebase може помилково дати [] |
| Повтор | Повторне читання без бізнес-мутацій; порядок не гарантований. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |

### API-04: GET /api/Product/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-02 / AC-05.1–2 / BR-04 |
| Авторизація | публічно, AllowAnonymous |
| Path / query / body / constraints | id: ulong, не UUID; body/query немає. |
| Успішна відповідь | 200 ProductDto |
| Помилки / error response | 404 text Product with ID {id} not found; тип id →400; 500 text |
| Повтор | Повторне читання; 404 не підмінюється першою грою. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |

### API-05: POST /api/Product

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-06 / AC-09.1–2 / BR-11 |
| Авторизація | JWT + роль Admin, перевірена через UserService |
| Path / query / body / constraints | multipart/form-data CreateProductDto; name/description/price/stock/regionId; optional discountPercentage/developer/publisher/releaseDate/category/cover. Поля й межі — schema нижче. |
| Успішна відповідь | 201 ProductDto + Location /api/Product/{id} |
| Помилки / error response | 401 порожній challenge; 403 Forbid; 400 ValidationProblemDetails або text file error; 415 неправильний media type; 500 text |
| Повтор | Неідемпотентний: дублює товар. Якщо cover upload впав, Product уже може бути записаний. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |

### API-06: PUT /api/Product/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-06 / AC-09 / BR-11; не повний PATCH-контракт |
| Авторизація | JWT + Admin |
| Path / query / body / constraints | id ulong; JSON UpdateProductDto, усі nullable/optional. Це фактично часткове оновлення під PUT. |
| Успішна відповідь | 200 ProductDto |
| Помилки / error response | 401/403; 404 text Product with ID {id} not found; 400 ValidationProblemDetails на Range/type; 500 text |
| Повтор | Ті самі значення переписуються, updatedAt змінюється. {} теж змінює updatedAt; null і missing нерозрізненні; unknown ігноруються за налаштуванням serializer. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |

### API-07: DELETE /api/Product/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-06 / AC-09; BR-10 ціль |
| Авторизація | JWT + Admin |
| Path / query / body / constraints | id ulong; без body/query. |
| Успішна відповідь | 204 без body |
| Помилки / error response | 401/403; 404 text; 500 text. 409 для історичних посилань зараз НЕ реалізовано. |
| Повтор | Повтор після успіху →404. Видаляє тільки Product, історичні посилання не перевіряє. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |

### API-08: GET /api/User/profile

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-01;SRC-05 / AC-02;AC-08 |
| Авторизація | JWT, поточний користувач |
| Path / query / body / constraints | Без body/query; UserId з перевіреного токена. |
| Успішна відповідь | 200 UserProfileDTO |
| Помилки / error response | 401; 500 text An error occurred: {message}, зокрема відсутній User/зіпсовані зв’язки |
| Повтор | Read; це агрегат, його ProductDto мапиться менш повно, ніж /User/products. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1) |

### API-09: GET /api/User/products

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-05 / AC-08 / BR-08 |
| Авторизація | JWT, поточний користувач |
| Path / query / body / constraints | Без body/query; userId із JWT. |
| Успішна відповідь | 200 ProductDto[] |
| Помилки / error response | 401; 500 text; repository може приховати помилку як [] |
| Повтор | Read; DISTINCT Product, тільки власні Paid/Completed Bill; licenses не обмежено до власного BillItem. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1) |

### API-10: GET /api/Bill/user

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04;SRC-05 / AC-07–08 |
| Авторизація | JWT, поточний користувач |
| Path / query / body / constraints | Без body/query; NameIdentifier із JWT парситься як ulong. |
| Успішна відповідь | 200 BillDto[], createdAt DESC |
| Помилки / error response | 401 text User ID not found in token; 400 text Invalid user ID format; 500 text, у т.ч. видалений Product |
| Повтор | Read; гідрує BillItems і Product вручну; tie-breaker відсутній. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |

### API-11: GET /api/Bill/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04;SRC-05;SRC-06 / BR-03 |
| Авторизація | будь-який JWT; ownership НЕ перевіряється |
| Path / query / body / constraints | id ulong; без body/query. |
| Успішна відповідь | 200 BillDto; BillItems часто [] через відсутнє завантаження навігацій |
| Помилки / error response | 401; 404 text Bill with ID {id} not found; 400 bad id; 500 text |
| Повтор | Read; витік чужих рахунків можливий за кодом; ціль власник/404. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |

### API-12: POST /api/Bill

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-03;SRC-04 / AC-06.4;AC-07 / BR-06 |
| Авторизація | будь-який JWT; body.UserId не звіряється з токеном |
| Path / query / body / constraints | JSON BillCreateDto з controller: userId ulong, totalAmount decimal, status BillStatus, currency string?, bonusPointsUsed int, items list?; item={productId ulong,quantity int,price decimal}. Немає Range/Required. Missing value-types →0/Pending; items null допускається. |
| Успішна відповідь | 201 BillDto + Location /api/Bill/{id}; currency у відповіді ВІДСУТНЯ |
| Помилки / error response | 401; 400 text InvalidOperationException (User не існує / недостатньо бонусів); 400 binding; 500 text; невідомий Product пропускається без помилки |
| Повтор | Новий Bill кожного разу; зменшення бонусів до Bill/Items; атомарність/дедуплікація/заборона повторної покупки відсутні. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |

### API-13: POST /api/Payment/stripe/create

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04 / AC-07 / BR-07 |
| Авторизація | JWT; сервіс перевіряє Bill.UserId |
| Path / query / body / constraints | JSON number billId (не {billId:...}); ulong; без path/query. |
| Успішна відповідь | 200 {success:true,paymentIntentId:string}; ВАЖЛИВО: поле фактично містить Stripe ClientSecret, не pi_* id |
| Помилки / error response | 401 text User ID claim not found; 400 text Invalid User ID format; 400 {error:string} для чужої/відсутньої/не Pending Bill та Stripe-помилок; binding 400 |
| Повтор | Кожен виклик створює новий PaymentIntent; Pending не змінюється; Stripe idempotency key не передається. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1) |

### API-14: POST /api/Payment/stripe/update-status

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04 / BR-07, небезпечна реалізаційна гілка |
| Авторизація | JWT; ownership PaymentIntent НЕ перевіряється |
| Path / query / body / constraints | JSON UpdatePaymentRequest: paymentIntentId string default empty, paymentMethod string default empty, action string default confirm; код приймає confirm/cancel, інший action не відхиляє явно. |
| Успішна відповідь | 200 {success:true,status:string,paymentId:ulong / null}; status succeeded якщо створено PaymentOrder, інакше updated |
| Помилки / error response | 401; 400 {error:string} зі Stripe/сервісу; binding 400 |
| Повтор | Зберігає charge через check-then-write, але UserId=0 і Bill не переводить у Paid. Може зірвати наступний complete як Payment already processed. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1) |

### API-15: POST /api/Payment/stripe/complete

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04;SRC-05 / AC-07–08 / BR-07–08 |
| Авторизація | JWT; UserId з claim Id; ownership Bill/metadata НЕ звірено |
| Path / query / body / constraints | JSON string pi_* paymentIntentId, не object; Stripe intent має succeeded. |
| Успішна відповідь | 200 {success:true,paymentId:ulong} |
| Помилки / error response | 401; 400 {error:string}, зокрема Payment already processed / Payment not succeeded; binding 400 |
| Повтор | Повтор завершеного charge →400, не ідемпотентний 200; Pending Bill →Paid та License/SalesCount/бонуси записуються окремо. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/PaymentController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/PaymentController.cs#L1) |

### API-16: GET /api/Bill

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-06 / BR-03: суперечність |
| Авторизація | будь-який JWT |
| Path / query / body / constraints | Без body/path/query. |
| Успішна відповідь | 200 BillDto[] усіх користувачів |
| Помилки / error response | 401; 500 text |
| Повтор | Read; Admin-only/owner-фільтра немає, не використовувати як власну історію. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |

### API-17: PUT /api/Bill/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-04;SRC-06 / BR-03;BR-07: суперечність |
| Авторизація | будь-який JWT; owner/Admin не перевірено |
| Path / query / body / constraints | id ulong; JSON повна Bill (id,userId,currency,totalAmount,status,createdAt,updatedAt); навігації JsonIgnore. |
| Успішна відповідь | 204 без body |
| Помилки / error response | 400 text Bill ID mismatch; 400 binding; 401; 404 без body; 500 text |
| Повтор | Дає змінити status/owner/amount без матриці; read-then-write, updatedAt не встановлює сервер. Ціль: прибрати з клієнтського API. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |

### API-18: DELETE /api/Bill/{id}

| Частина | Контракт |
| --- | --- |
| Призначення / вимоги | SRC-05;SRC-06 / BR-03;BR-08: суперечність |
| Авторизація | будь-який JWT; owner/Admin не перевірено |
| Path / query / body / constraints | id ulong; без body. |
| Успішна відповідь | 204 без body |
| Помилки / error response | 401; 404 без body; 500 text |
| Повтор | Повтор →404; видаляє Bill без цілісного видалення Items/License; paid-access може зникнути. Ціль: заборонити видалення історії. |
| Імплементація | IMPLEMENTED; виконання NOT VERIFIED; [LudenWebAPI/Controllers/BillController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/BillController.cs#L1) |


### Додаткові чинні маршрути та межа обсягу

| Операція | Контракт / ризик | Доказ |
| --- | --- | --- |
| GET /api/User; GET /api/User/{id} | JWT; 200 UserDto[] / UserDto, 404 для id, 500 catch. Немає Admin/owner-перевірки; privacy-ризик. GET profile/{id} повертає чужий UserProfileDTO без ownership-check. | IMPLEMENTED [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1) |
| DELETE /api/User/{id} | JWT, будь-який id; 204 /404/500, без owner/Admin-перевірки. Не потрібен для ЛР 1; закрити доступ до окремого рішення. | IMPLEMENTED [LudenWebAPI/Controllers/UserController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/UserController.cs#L1) |
| PUT /api/Product/{id}/cover/{coverFileId} | JWT+Admin; обидва ulong, без body; 200 ProductDto; 404/400 text/401/403/500; файл має належати Product; repeated write змінює updatedAt. | IMPLEMENTED [LudenWebAPI/Controllers/ProductController.cs:1](https://github.com/Ramseer24/Luden-Back-End/blob/fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff/LudenWebAPI/Controllers/ProductController.cs#L1) |
| PUT /api/User/update; Favorite/File/Image | профіль/обране/upload наявні; поза обсягом основних вимог; не заявлено виконання їхнього повного аудиту безпеки. | IMPLEMENTED / D,F; див. architecture.md |

## 4. Цільові доповнення в існуючому просторі API

Усе в цьому розділі PROPOSED / NOT IMPLEMENTED. Не створюється паралельний набір /games/orders. Наявні операції мають виправлятися в тих самих контролерах. Прийняття breaking input-обмежень потребує синхронної зміни frontend та погодження команди.

| ID / метод / endpoint | Авторизація, вхід | Успіх / повна схема | Помилки / повтор / зв’язок |
| --- | --- | --- | --- |
| API-P01 GET /api/Cart | JWT власника; без path/query/body | 200 Cart: {userId:ulong,items:[{productId:ulong,quantity:1,unitPrice:decimal}],totalAmount:decimal,currency:string} | 401; 503 недоступне сховище; read; BR-05 / AC-06 |
| API-P02 POST /api/Cart/items | JWT; JSON {productId:ulong}; &gt;0, існуючий непридбаний Product; інші поля заборонені | 200 Cart як P01; повтор того самого товару повертає той самий склад | 400 ValidationProblemDetails; 401; 404 {error:string}; 409 {error:string} для owned/резервації; BR-05 / AC-05.4,06.1 |
| API-P03 DELETE /api/Cart/items/{productId} | JWT; productId ulong; без body/query | 204 без body; сума змінюється в наступному GET | 401; 404 {error:string} для missing item, в т.ч. повтору; BR-05 / AC-06.2–3 |
| API-P04 PATCH /api/Product/{id} | JWT+Admin; id ulong; JSON object із presence-aware UpdateProductDto; дозволено name,description,price,stock,regionId,discountPercentage,developer,publisher,releaseDate,category; поля/межі у requirements | 200 повний ProductDto як API-04; змінено тільки передані поля. Одна валідація всього входу, потім один контрольований запис | 400 ValidationProblemDetails для {},unknown,immutable,null не nullable,невірних типів/меж; 401/403; 404 {error:string}; повтор значень без нових бізнес-ефектів, updatedAt може змінитись; BR-11 / AC-09 |
| API-12 виправлення POST /api/Bill | JWT власника; ціль JSON {items:[{productId:ulong}]} або серверний Cart за D-04; choice OPEN, не прийнятий другий контракт | 201 BillDto + PROPOSED currency:string; id/price/quantity/total/status/userId визначає сервер, старт Pending | 400/401/404/409; пусті позиції не допустимі; дубль покупки/активна резервація 409; BR-06/12; idempotency header і TTL OPEN |
| API-13 виправлення stripe/create | JWT власника; чинне JSON number billId збережено; Pending/Declined за матрицею | 200 чинний envelope, але назву paymentIntentId із clientSecret треба окремо погодити; зберігати attempt і Processing до виклику Stripe | 401; 404 hidden foreign; 409 state/reservation; provider400 {error:string}; BR-07; дубль start-key існуюча спроба |
| API-14/15 виправлення stripe/update-status і complete | JWT власника; чинні форми body збережено; звірити user/metadata/суму/валюту; заборонити використання ClientSecret як id | 200 чинні envelopes; перевірена відмова зберігає Declined; complete успішний тільки після перевірки provider; повтор event повертає попередній success | 401/404/409; provider400; один charge→одна доставка; durable recovery OPEN; BR-07/12 |
| API-07 виправлення DELETE /api/Product/{id} | JWT+Admin; чинний id/body збережено | 204 лише без будь-яких BillItem/License-посилань | 409 {error:string} якщо історія; repeated delete404; BR-10 / AC-09.1 |
| API-01 уточнення register | додати passwordConfirmation у той самий DTO, ≥8 на API; повна валідація до запису | 200 string Success і чинний наступний login UI залишити; атомарний register+session окремо OPEN | 400 binding/validation; дублікат 400 EmailBusy для сумісності; BR-01/02; не оголошувати 201/token чинним |

Для Catalog query/genre: frontend нині фільтрує завантажений список. Якщо команда вирішить перенести фільтрацію на сервер, розширити API-03 optional query:string, genre:string зі збереженням 200 ProductDto[] і BR-04; жодного другого маршруту. Це PROPOSED; чинний код їх не обробляє. Гарантований порядок — D-05 OPEN.

## 5. Приклади (синтетичні, NOT RUN)

Це перевірені на синтаксис JSON приклади форми, а не записи трафіку чи успішних тестів. Для PROPOSED-прикладів потрібного маршруту/поведінки немає. У реєстрації код повертає string; JSON-подання string наведено з `Accept: application/json`, переговори форматів runtime NOT VERIFIED. Типова text/plain-відповідь має тіло Success без лапок.

### EX-01 Успішна реєстрація

API-01 IMPLEMENTED; підтвердження на UI; сесія окремим API-02.

Request body:

```json
{
  "email": "buyer@example.test",
  "password": "ExamplePass8"
}
```

Response status: 200; body:

```json
"Success"
```

### EX-02 Помилка реєстрації

API-01 IMPLEMENTED: той самий email повторно; Accept application/json.

Request body:

```json
{
  "email": "buyer@example.test",
  "password": "ExamplePass8"
}
```

Response status: 400; body:

```json
"EmailBusy"
```

### EX-03 Каталог

API-03 IMPLEMENTED; GET без body, None нижче означає відсутність body.

Запит: без body.

Response status: 200; body:

```json
[
  {
    "id": 101,
    "name": "Приклад гри",
    "description": "Синтетичний опис",
    "price": 299.0,
    "stock": 10,
    "regionId": 1,
    "discountPercentage": 0,
    "salesCount": 0,
    "region": null,
    "createdAt": "2026-11-20T10:00:00Z",
    "updatedAt": null,
    "developer": "Навчальна студія",
    "publisher": "Навчальний видавець",
    "releaseDate": null,
    "category": "RPG",
    "coverUrl": null,
    "files": [],
    "licenses": []
  }
]
```

### EX-04 Додавання до кошика

API-P02 PROPOSED / NOT IMPLEMENTED.

Request body:

```json
{
  "productId": 101
}
```

Response status: 200; body:

```json
{
  "userId": 7,
  "items": [
    {
      "productId": 101,
      "quantity": 1,
      "unitPrice": 299.0
    }
  ],
  "totalAmount": 299.0,
  "currency": "UAH"
}
```

### EX-05 Створення Bill

API-12 IMPLEMENTED / НЕБЕЗПЕЧНИЙ чинний формат: значення клієнта; це не нормативне право задавати Paid/ціну; GetBillDtoById не гідрує Items.

Request body:

```json
{
  "userId": 7,
  "totalAmount": 299.0,
  "status": "Pending",
  "currency": "UAH",
  "bonusPointsUsed": 0,
  "items": [
    {
      "productId": 101,
      "quantity": 1,
      "price": 299.0
    }
  ]
}
```

Response status: 201; body:

```json
{
  "id": 201,
  "createdAt": "2026-11-20T10:05:00Z",
  "totalAmount": 299.0,
  "status": "Pending",
  "billItems": []
}
```

### EX-06 Перехід до Stripe

API-13 IMPLEMENTED: request JSON number; поле paymentIntentId фактично ClientSecret; Bill лишається Pending.

Request body:

```json
201
```

Response status: 200; body:

```json
{
  "success": true,
  "paymentIntentId": "pi_example_secret_example"
}
```

### EX-07 Відхилена оплата

API-14 IMPLEMENTED: приклад Stripe exception, не фіксація Declined; точний message залежить від провайдера.

Request body:

```json
{
  "paymentIntentId": "pi_example",
  "paymentMethod": "pm_card_chargeDeclined",
  "action": "confirm"
}
```

Response status: 400; body:

```json
{
  "error": "Приклад повідомлення Stripe про відхилену картку"
}
```

### EX-08 Бібліотека

API-09 IMPLEMENTED: GET без body, власний Paid Bill у тестовій передумові.

Запит: без body.

Response status: 200; body:

```json
[
  {
    "id": 101,
    "name": "Приклад гри",
    "description": "Синтетичний опис",
    "price": 299.0,
    "stock": 10,
    "regionId": 1,
    "discountPercentage": 0,
    "salesCount": 0,
    "region": null,
    "createdAt": "2026-11-20T10:00:00Z",
    "updatedAt": null,
    "developer": "Навчальна студія",
    "publisher": "Навчальний видавець",
    "releaseDate": null,
    "category": "RPG",
    "coverUrl": null,
    "files": [],
    "licenses": []
  }
]
```

### EX-09 Успішний Admin PATCH

API-P04 PROPOSED / NOT IMPLEMENTED; JWT Admin, id=101.

Request body:

```json
{
  "name": "Оновлена гра"
}
```

Response status: 200; body:

```json
{
  "id": 101,
  "name": "Оновлена гра",
  "description": "Синтетичний опис",
  "price": 299.0,
  "stock": 10,
  "regionId": 1,
  "discountPercentage": 0,
  "salesCount": 0,
  "region": null,
  "createdAt": "2026-11-20T10:00:00Z",
  "updatedAt": "2026-11-20T10:10:00Z",
  "developer": "Навчальна студія",
  "publisher": "Навчальний видавець",
  "releaseDate": null,
  "category": "RPG",
  "coverUrl": null,
  "files": [],
  "licenses": []
}
```

### EX-10 Помилковий Admin PATCH

API-P04 PROPOSED / NOT IMPLEMENTED; name після відповіді має лишитися Приклад гри; жодного запису.

Request body:

```json
{
  "name": "Не зберігати",
  "price": -1
}
```

Response status: 400; body:

```json
{
  "type": "about:blank",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "price": [
      "Price must be greater than 0"
    ]
  }
}
```

### EX-11 Успішний вхід

API-02 IMPLEMENTED; token синтетичний і не придатний для входу.

Request body:

```json
{
  "email": "buyer@example.test",
  "password": "ExamplePass8"
}
```

Response status: 200; body:

```json
{
  "token": "SYNTHETIC_JWT_NOT_A_CREDENTIAL"
}
```

### EX-12 Завершення оплати

API-15 IMPLEMENTED, передумова provider succeeded; body — JSON string.

Request body:

```json
"pi_example"
```

Response status: 200; body:

```json
{
  "success": true,
  "paymentId": 301
}
```

### EX-13 Помилковий чинний PUT

API-06 IMPLEMENTED; DataAnnotations відхиляє price до ProductService, name не записується; повний PATCH-policy при цьому відсутній.

Request body:

```json
{
  "name": "Не зберігати",
  "price": -1
}
```

Response status: 400; body:

```json
{
  "type": "about:blank",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "price": [
      "Price must be greater than 0"
    ]
  }
}
```

Після EX-10 перевіряють GET /api/Product/101 і знімок сховища: усі поля, включно з updatedAt, незмінні. Це очікуваний результат майбутнього тесту, а не виконаний тест. Справжнього PATCH у ProductController немає, тому приклад не можна відправити до чинного сервера й очікувати цей результат.

При відмові Stripe в чинному EX-07 Bill лишається Pending; відмову в DECLINED та retry того самого замовлення показано тільки в цільовій [матриці](requirements.md). Реальний Stripe SDK-код є, але працездатність конфігурації, sandbox і фінансова транзакція NOT VERIFIED.

## 6. Приклади для кожної суттєвої операції

Повний машиночитний набір для 18 наявних основних операцій і 4 пропозицій міститься в [api-examples.json](../verification/api-examples.json). Це синтетичні приклади NOT RUN, не трафік сервера. Для multipart create JSON у файлі лише представляє набір form-fields, media type лишається multipart/form-data. GET/DELETE без body мають request_body=null; це позначка відсутнього HTTP body, не literal JSON null у запиті. Success/error форми прив’язані до API-ID та описаних вище фактичних/цільових схем.

Register200 повертає string, login200 — token; payment create200 містить ClientSecret у misnamed paymentIntentId; BillDto досі без currency. Поточні 400 не замінено вигаданими 422. Повтор/ownership/state409 і foreign404 — target тільки там, де це явно PROPOSED. Невизначені money/quantity/destination рішення не можна видати за прийняті після review.
