# Джерела, історія й межі доказів

Фінальна редакція 20.11.2026. Пріоритет: методичка → підтверджені продуктові SRC/початкові AC → погоджені зміни (якщо є докази) → код як факт поточного стану → непогоджені P/EXT-пропозиції. Наявність файлу або командного review сама не змінює статус пропозиції на затверджену.

## Використані джерела

| Джерело | Версія й перевірка | Локальний доказ |
| --- | --- | --- |
| Головна методичка Luden | Прочитано всі 9 сторінок; результати зіставлені з пунктами здавання | PDF (оригінал збережено в локальному комплекті) |
| Первинний UX Input Pack | 822a688a04bce5167f44226efbec952069042b6c; 8 US/33 AC, точні тексти | [Текст](../sources/input-pack-initial.txt) · [Архів джерел](https://github.com/NureTatkovOleksandr/luden-ux-ui/tree/822a688a04bce5167f44226efbec952069042b6c) |
| Передревізійний UX-зріз | 0e0b1ddcfafb9ccaa455cbec8295ae757d7efd07; проаналізовано зміни від першої версії | [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/0e0b1ddcfafb9ccaa455cbec8295ae757d7efd07/01_requirements/01_Input_Pack_v0.1.md) · [Архів](https://github.com/NureTatkovOleksandr/luden-ux-ui/tree/0e0b1ddcfafb9ccaa455cbec8295ae757d7efd07) |
| Актуальні UX-матеріали | 9beb0fe4a2b2734182ec233aa5084700f177491c; main, full history16commits; P-01–P-08 PROPOSED | [Input Pack](https://github.com/NureTatkovOleksandr/luden-ux-ui/blob/9beb0fe4a2b2734182ec233aa5084700f177491c/01_requirements/01_Input_Pack_v0.1.md) · [Повний tracked-зріз](https://github.com/NureTatkovOleksandr/luden-ux-ui/tree/9beb0fe4a2b2734182ec233aa5084700f177491c) · [Історія](https://github.com/NureTatkovOleksandr/luden-ux-ui/commits/main/) |
| Backend | fb5ba5a66f4b3001b608e3e3999c3aa2f0ccaaff; main=origin/main після fetch; робоче дерево чисте | immutable code-links у [аудиті](implementation-audit.md) |
| Frontend | ea90e7f465012d78d2f0593ad745ffb0ea07106c; main=origin/main після fetch; робоче дерево чисте | immutable code-links у [архітектурі](architecture.md) |
| Підтвердження колективного review | Пряме повідомлення користувача для поточної ЛР 1; чотири названі учасники | [Запис підстави](../sources/team-review-confirmation.txt) |
| Попередні редакції ЛР 1 | Незмінні архіви; старі припущення відображають стан попередньої редакції, а не чинні факти | Попереднє допрацювання (оригінал збережено в локальному комплекті) · Початкова робота (оригінал збережено в локальному комплекті) |

## Що саме перевірено в UX/UI

Product Baseline, всі версії Input Pack і Decision Log, Screen Map/Contracts, Plan Review, Figma Brief, Review Report, Defect Change Log, Test Cases, AI log, TEAM та README. Джерельні 15 PNG/переходи доступні у snapshot-архівах; їхній опис використано як доказ UX-інвентаря. Figma Present у цій сесії не проходили. Історичні F-T PASS/FAIL належать записаному джерелом прогону, не новому продуктовому тесту.

Mini Issue Tracker DOCX тепер надано й перевірено як процедурний зразок; [зіставлення](methodology-crosswalk.md). Окремий методичний гід DOCX не надано. Предметну область Luden не замінено. Первинний Input Pack та командні UX-документи тепер доступні; старий blocker їх недоступності закрито.

## Статуси

CONFIRMED_SOURCE — текст є у перевіреній версії, не автоматичне підписане замовником приймання. PROPOSED — P/EXT/технічний кандидат. OPEN — потрібне конкретне рішення. IMPLEMENTED — є гілка коду; runtime окремо. Доказові статуси аудиту: CONFIRMED (підтверджений кодовий факт), POTENTIAL (обґрунтований вплив/ризик), FIXED (лише реально виправлене), NOT VERIFIED (бракує виконання/даних). Жодного виправлення backend/frontend не оголошено.

Командне перехресне review поточної ЛР 1 CONFIRMED BY USER: Паламарчук Антон, Татьков Олександр, Сергєєва Таісія, Панковський Тимофій. Персональні findings/дати не надані; не вигадані. UX TEAM історично включає також Кисельова Олександра; його з джерел не вилучено, до поточної четвірки ЛР 1 не додано.

## Навігація й версія

[Вимоги](requirements.md), [AC-порівняння](ac-reconciliation.md), [API](api-contract.md), [архітектура](architecture.md), [рішення](decision-log.md), [тести](test-cases.md), [CSV](traceability.csv), [покриття](traceability-notes.md), [аудит](implementation-audit.md), [AI-журнал](ai-log.md), [звіт](lab-01.md), [методична відповідність](methodology-compliance.md), [результат правок](review-report.md), [перевірки](validation.md). Точний локальний commit/tag і Git bundle — у [VERSION.txt](../VERSION.txt). Версію для GitHub-здавання позначає тег lab01-spec-published; адреса репозиторію й інструкції наведені в README. Факт публікації перевіряється окремо через GitHub API/Git refs.

## Межа публічного комплекту

У GitHub розміщено поточні академічні документи, згенерований PDF, інструменти й мінімальні метадані перевірок. Повні методички, історичні ZIP, Git bundle та попередня Git-історія не публікуються; їх збережено локально без видалення. Для UX/UI-версій наведено посилання на вже відкритий репозиторій. Один невеликий Input Pack @822a688 з цього відкритого джерела залишено для відтворюваної перевірки 33 AC.
