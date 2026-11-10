## RECON-P5CR2 | 2026-11-10 18:32:35 UTC

Ревизии: BASE `e17379ad660fca46859b403a6c3d33ec8d831a40`, FORK1 `9208dcf5a358f40afd95c99480e4e09f781ed566`, PORT `832c953a94a632d57872349013f7ed1a37434715`.

## 1. Участки HUD форка и места в PORT

Таблицы ниже сохраняют все строки и столбцы обязательных TSV-файлов.

### Дорожка 1

```tsv
путь в FORK1	строки участка в FORK1	функция или функции FORK1	что меняет участок	область	шаг	место в PORT	PORT отличается от BASE в этом месте
src/drawers/CreditsDrawer.cpp	src/drawers/CreditsDrawer.cpp@9208dcf:7-28	CreditsDrawer::CreditsDrawer, вне функций — подключения	Подключены локализация и текстовый контекст, а конструктор получает объект отрисовки текста.	полоса кредитов	П7	CreditsDrawer::CreditsDrawer: src/drawers/CreditsDrawer.cpp@832c953:50-76; подключения: src/drawers/CreditsDrawer.cpp@832c953:16	src/drawers/CreditsDrawer.cpp@832c953:1
src/drawers/CreditsDrawer.cpp	src/drawers/CreditsDrawer.cpp@9208dcf:37-43	CreditsDrawer::CreditsDrawer	Ширина полосы вычисляется по логическому размеру текстуры для HD-плотности.	полоса кредитов	П5в	CreditsDrawer::CreditsDrawer: src/drawers/CreditsDrawer.cpp@832c953:50-76	src/drawers/CreditsDrawer.cpp@832c953:1
src/drawers/CreditsDrawer.cpp	src/drawers/CreditsDrawer.cpp@9208dcf:185-248	CreditsDrawer::draw, CreditsDrawer::getXDrawingOffset (в FORK1 удалены: getXDrawingOffset)	Полоса кредитов перерисована как панель с подписью и текущей суммой; старый расчёт сдвига цифр удалён.	полоса кредитов	П5в	CreditsDrawer::draw: src/drawers/CreditsDrawer.cpp@832c953:209-218; CreditsDrawer::getXDrawingOffset: нет функции	src/drawers/CreditsDrawer.cpp@832c953:209
src/drawers/CreditsDrawer.cpp	src/drawers/CreditsDrawer.cpp@9208dcf:260 (только удаление)	CreditsDrawer::drawCurrentCredits, CreditsDrawer::drawPreviousCredits (в FORK1 удалены: drawCurrentCredits, drawPreviousCredits)	Удалены отдельные методы рисования текущей и предыдущей суммы с прокруткой цифр.	полоса кредитов	П5в	CreditsDrawer::drawCurrentCredits: src/drawers/CreditsDrawer.cpp@832c953:222-251; CreditsDrawer::drawPreviousCredits: src/drawers/CreditsDrawer.cpp@832c953:255-283	src/drawers/CreditsDrawer.cpp@832c953:209,src/drawers/CreditsDrawer.cpp@832c953:234,src/drawers/CreditsDrawer.cpp@832c953:254,src/drawers/CreditsDrawer.cpp@832c953:267
src/drawers/CreditsDrawer.h	src/drawers/CreditsDrawer.h@9208dcf:10-16	вне функций — объявление класса cTextDrawer	Добавлено предварительное объявление текстового drawer.	полоса кредитов	П5в	объявление класса cTextDrawer: нет	—
src/drawers/CreditsDrawer.h	src/drawers/CreditsDrawer.h@9208dcf:31-40	вне функций — объявление класса и его полей	Добавлен указатель на объект отрисовки текста и удалены объявления старых методов прокрутки цифр.	полоса кредитов	П5в	объявление класса и его полей: src/drawers/CreditsDrawer.h@832c953:38	src/drawers/CreditsDrawer.h@832c953:23
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:5-71	removeLastUtf8CodePoint, fitWithEllipsis, compactCardName, cBuildingListDrawer::cBuildingListDrawer, вне функций — подключения	Добавлены обрезка UTF-8 текста и компактные подписи карточек, а метка готовности локализована.	список построек	П7	removeLastUtf8CodePoint: нет функции; fitWithEllipsis: нет функции; compactCardName: нет функции; cBuildingListDrawer::cBuildingListDrawer: src/drawers/cBuildingListDrawer.cpp@832c953:43-53; подключения: src/drawers/cBuildingListDrawer.cpp@832c953:16	src/drawers/cBuildingListDrawer.cpp@832c953:1
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:97-104	cBuildingListDrawer::drawButtonHoverRectangle	Размер рамки наведения берётся из геометрии кнопки списка.	боковая панель, список построек	П5в	cBuildingListDrawer::drawButtonHoverRectangle: src/drawers/cBuildingListDrawer.cpp@832c953:83-98	src/drawers/cBuildingListDrawer.cpp@832c953:82
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:125-201	cBuildingListDrawer::drawButton, cBuildingListDrawer::getDrawX, cBuildingListDrawer::getDrawY	Кнопки категорий получили новую рамку и состояния доступности, а их координаты берутся из HudLayout.	боковая панель, список построек	П5в	cBuildingListDrawer::drawButton: src/drawers/cBuildingListDrawer.cpp@832c953:100-149; cBuildingListDrawer::getDrawX: src/drawers/cBuildingListDrawer.cpp@832c953:152-155; cBuildingListDrawer::getDrawY: src/drawers/cBuildingListDrawer.cpp@832c953:157-160	src/drawers/cBuildingListDrawer.cpp@832c953:82,src/drawers/cBuildingListDrawer.cpp@832c953:111,src/drawers/cBuildingListDrawer.cpp@832c953:134,src/drawers/cBuildingListDrawer.cpp@832c953:151
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:205-213	cBuildingListDrawer::drawList	Для списка вычисляются раскладка карточек и текущая строка прокрутки.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:220-237	cBuildingListDrawer::drawList	Рисование списка ограничено областью карточек, размеры и вертикальная раскладка взяты из HudLayout.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:239-252	cBuildingListDrawer::drawList	Карточки размещаются по раскладке с учётом прокрутки и пропускаются за видимой областью.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:256-262	cBuildingListDrawer::drawList	Вместо текстуры элемента вызывается новый отрисовщик HD-карточек.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:267-318	cBuildingListDrawer::drawList	Прогресс строительства показывается заполнением полосы, а готовность — текстовой меткой с цветом действия.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:335-350	cBuildingListDrawer::drawList	Недоступность элемента обозначается затемнённой областью карточки.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:354-360	cBuildingListDrawer::drawList	Строка «Upgrading» заменена вызовом локализации для ключа «Upgrade» с русской подписью «Улучшение».	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:365-378	cBuildingListDrawer::drawList	Три строки Building in progress заменены одной надписью OCCUPIED.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:380-395	cBuildingListDrawer::drawList	Состояние занятости вместо текстуры затемняет область карточки.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:417-440	cBuildingListDrawer::drawList	Подписи и цена карточки размещаются внутри её нижней части на тёмной подложке.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:461-470	cBuildingListDrawer::drawList	Удалён ручной переход по сетке; после цикла снимается clipping и рисуется полоса прокрутки.	список построек	П5в	cBuildingListDrawer::drawList: src/drawers/cBuildingListDrawer.cpp@832c953:165-377	src/drawers/cBuildingListDrawer.cpp@832c953:161,src/drawers/cBuildingListDrawer.cpp@832c953:179,src/drawers/cBuildingListDrawer.cpp@832c953:194,src/drawers/cBuildingListDrawer.cpp@832c953:211,src/drawers/cBuildingListDrawer.cpp@832c953:225,src/drawers/cBuildingListDrawer.cpp@832c953:234,src/drawers/cBuildingListDrawer.cpp@832c953:261,src/drawers/cBuildingListDrawer.cpp@832c953:341,src/drawers/cBuildingListDrawer.cpp@832c953:351,src/drawers/cBuildingListDrawer.cpp@832c953:376
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:494-512	cBuildingListDrawer::drawStructureSize, cBuildingListDrawer::isOverItemCoordinates_Boolean	Значок размера структуры перенесён в правый верхний угол карточки, а область попадания использует её размеры из раскладки.	список построек, мышь	П5в	cBuildingListDrawer::drawStructureSize: src/drawers/cBuildingListDrawer.cpp@832c953:403-425; cBuildingListDrawer::isOverItemCoordinates_Boolean: src/drawers/cBuildingListDrawer.cpp@832c953:427-433	src/drawers/cBuildingListDrawer.cpp@832c953:403,src/drawers/cBuildingListDrawer.cpp@832c953:419
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:515-718	cBuildingListDrawer::isOverItemCoordinates, cBuildingListDrawer::getCardWidth, cBuildingListDrawer::getCardHeight, cBuildingListDrawer::drawHdCard	Добавлены проверка попадания по карточкам с прокруткой, HD-отрисовка и перенос/обрезка названий и цены.	список построек, мышь	П5в	cBuildingListDrawer::isOverItemCoordinates: src/drawers/cBuildingListDrawer.cpp@832c953:435-465; cBuildingListDrawer::getCardWidth: нет функции; cBuildingListDrawer::getCardHeight: нет функции; cBuildingListDrawer::drawHdCard: нет функции	src/drawers/cBuildingListDrawer.cpp@832c953:434
src/drawers/cBuildingListDrawer.cpp	src/drawers/cBuildingListDrawer.cpp@9208dcf:720-866	cBuildingListDrawer::getLayout, cBuildingListDrawer::getScrollRow, cBuildingListDrawer::setScrollRow, cBuildingListDrawer::scrollSelectedList, cBuildingListDrawer::drawHdScrollbar, cBuildingListDrawer::onNotifyMouseEvent	Добавлены состояние и полоса прокрутки списка, обработка колеса мыши и кликов по полосе; старый пустой обработчик заменён.	список построек, мышь	П5в	cBuildingListDrawer::getLayout: нет функции; cBuildingListDrawer::getScrollRow: нет функции; cBuildingListDrawer::setScrollRow: нет функции; cBuildingListDrawer::scrollSelectedList: нет функции; cBuildingListDrawer::drawHdScrollbar: нет функции; cBuildingListDrawer::onNotifyMouseEvent: src/drawers/cBuildingListDrawer.cpp@832c953:472-475	нет
src/drawers/cBuildingListDrawer.h	src/drawers/cBuildingListDrawer.h@9208dcf:3-19	вне функций — подключения; объявление класса	Подключён HudLayout и добавлен доступ UiAuditAccess к приватным данным drawer.	список построек, другое — доступ UI-аудита	П5г	подключения: src/drawers/cBuildingListDrawer.h@832c953:20; объявление класса: src/drawers/cBuildingListDrawer.h@832c953:32	src/drawers/cBuildingListDrawer.h@832c953:1
src/drawers/cBuildingListDrawer.h	src/drawers/cBuildingListDrawer.h@9208dcf:43-50	вне функций — объявление класса и его полей	Добавлено состояние строк прокрутки и локализованная метка готовности.	список построек	П5в	объявление класса и его полей: src/drawers/cBuildingListDrawer.h@832c953:32	src/drawers/cBuildingListDrawer.h@832c953:1
src/drawers/cBuildingListDrawer.h	src/drawers/cBuildingListDrawer.h@9208dcf:52-65	вне функций — объявление класса и его методов	Объявлены методы HD-карточек, scrollbar, раскладки, прокрутки и hit testing.	список построек, мышь	П5в	объявление класса и его методов: src/drawers/cBuildingListDrawer.h@832c953:32	src/drawers/cBuildingListDrawer.h@832c953:1
src/drawers/cMessageDrawer.cpp	src/drawers/cMessageDrawer.cpp@9208dcf:3-16	вне функций — подключения	Добавлены зависимости раскладки строки сообщений и музыкального блока.	строка сообщений, верхняя строка	П9	подключения: src/drawers/cMessageDrawer.cpp@832c953:16	src/drawers/cMessageDrawer.cpp@832c953:1
src/drawers/cMessageDrawer.cpp	src/drawers/cMessageDrawer.cpp@9208dcf:39-125	cMessageDrawer::draw	В боевом режиме сообщения занимают место рядом с музыкальным блоком и автоматически масштабируются по доступной ширине.	строка сообщений, верхняя строка	П9	cMessageDrawer::draw: src/drawers/cMessageDrawer.cpp@832c953:58-69	src/drawers/cMessageDrawer.cpp@832c953:58
src/drawers/cMessageDrawer.cpp	src/drawers/cMessageDrawer.cpp@9208dcf:233-266	cMessageDrawer::createMessageBarBmp	Поверхность фона полосы сообщений создаётся с учётом плотности HD и текстура повторяется с масштабированными шагами.	строка сообщений	П5в	cMessageDrawer::createMessageBarBmp: src/drawers/cMessageDrawer.cpp@832c953:173-195	src/drawers/cMessageDrawer.cpp@832c953:172
src/drawers/cMessageDrawer.h	src/drawers/cMessageDrawer.h@9208dcf:39-45	cMessageDrawer::getMessage	Геттер сообщения помечен как константный.	строка сообщений	П5в	cMessageDrawer::getMessage: нет функции	—
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:2-8	вне функций — подключения	Подключён инструмент аудита интерфейса для регистрации области мини-карты.	мини-карта, другое — аудит интерфейса	П5г	подключения: src/drawers/cMiniMapDrawer.cpp@832c953:16	src/drawers/cMiniMapDrawer.cpp@832c953:1
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:11-17	вне функций — подключения	Подключена общая раскладка HUD для геометрии мини-карты.	мини-карта	П5в	подключения: src/drawers/cMiniMapDrawer.cpp@832c953:16	src/drawers/cMiniMapDrawer.cpp@832c953:1
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:26-62	cMiniMapDrawer::cMiniMapDrawer	Геометрия мини-карты вычисляется по области радара из HudLayout.	мини-карта	П5в	cMiniMapDrawer::cMiniMapDrawer: src/drawers/cMiniMapDrawer.cpp@832c953:48-90	src/drawers/cMiniMapDrawer.cpp@832c953:1
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:70-78	cMiniMapDrawer::draw	Добавлена регистрация области клика по мини-карте при наличии радара.	мини-карта, мышь	П5в	cMiniMapDrawer::draw: src/drawers/cMiniMapDrawer.cpp@832c953:108-133	src/drawers/cMiniMapDrawer.cpp@832c953:97,src/drawers/cMiniMapDrawer.cpp@832c953:115,src/drawers/cMiniMapDrawer.cpp@832c953:126
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:81-89	cMiniMapDrawer::draw	Отрисованная область мини-карты регистрируется в UI-аудите.	мини-карта, другое — аудит интерфейса	П5в	cMiniMapDrawer::draw: src/drawers/cMiniMapDrawer.cpp@832c953:108-133	src/drawers/cMiniMapDrawer.cpp@832c953:97,src/drawers/cMiniMapDrawer.cpp@832c953:115,src/drawers/cMiniMapDrawer.cpp@832c953:126
src/drawers/cMiniMapDrawer.cpp	src/drawers/cMiniMapDrawer.cpp@9208dcf:97 (только удаление)	cMiniMapDrawer::draw, cMiniMapDrawer::drawStaticFrame (в FORK1 удалены: drawStaticFrame)	Удалены вызов и реализация анимации статических помех на мини-карте.	мини-карта	П5в	cMiniMapDrawer::draw: src/drawers/cMiniMapDrawer.cpp@832c953:108-133; cMiniMapDrawer::drawStaticFrame: src/drawers/cMiniMapDrawer.cpp@832c953:135-158	src/drawers/cMiniMapDrawer.cpp@832c953:97,src/drawers/cMiniMapDrawer.cpp@832c953:115,src/drawers/cMiniMapDrawer.cpp@832c953:126,src/drawers/cMiniMapDrawer.cpp@832c953:139,src/drawers/cMiniMapDrawer.cpp@832c953:153
src/drawers/cMiniMapDrawer.h	src/drawers/cMiniMapDrawer.h@9208dcf:34 (только удаление)	вне функций — объявление класса и метода	Удалено объявление метода рисования статических помех.	мини-карта	П5в	объявление класса и метода: src/drawers/cMiniMapDrawer.h@832c953:56	src/drawers/cMiniMapDrawer.h@832c953:55
src/drawers/cMiniMapDrawer.h	src/drawers/cMiniMapDrawer.h@9208dcf:76 (только удаление)	вне функций — объявление класса и поля	Удалено поле прозрачности кадров статических помех.	мини-карта	П5в	объявление класса и поля: src/drawers/cMiniMapDrawer.h@832c953:56	src/drawers/cMiniMapDrawer.h@832c953:55
src/drawers/cSideBarDrawer.cpp	src/drawers/cSideBarDrawer.cpp@9208dcf:1-56	cSideBarDrawer::cSideBarDrawer, cSideBarDrawer::~cSideBarDrawer, вне функций — подключения	Загружаются HD-гербы Домов и освобождаются при уничтожении drawer; Candybar-текстуры больше не создаются.	боковая панель, герб Дома	П5г,П7	cSideBarDrawer::cSideBarDrawer: src/drawers/cSideBarDrawer.cpp@832c953:36-44; cSideBarDrawer::~cSideBarDrawer: src/drawers/cSideBarDrawer.cpp@832c953:54-61; подключения: src/drawers/cSideBarDrawer.cpp@832c953:16	src/drawers/cSideBarDrawer.cpp@832c953:1
src/drawers/cSideBarDrawer.cpp	src/drawers/cSideBarDrawer.cpp@9208dcf:66-410	cSideBarDrawer::draw, cSideBarDrawer::drawHdSidebar, cSideBarDrawer::getHouseCrest, cSideBarDrawer::getHouseDisplayName, cSideBarDrawer::drawHdRadarPanel, cSideBarDrawer::drawHdMeter, cSideBarDrawer::drawHdCapacities, cSideBarDrawer::drawHdBuildingLists, cSideBarDrawer::setPlayer	Боковая панель заменена HD-оформлением: показаны радарная область, герб и Дом, счётчики ресурсов, категории построек и их список.	боковая панель, список построек, мини-карта, герб Дома	П5г	cSideBarDrawer::draw: src/drawers/cSideBarDrawer.cpp@832c953:81-91; cSideBarDrawer::drawHdSidebar: нет функции; cSideBarDrawer::getHouseCrest: нет функции; cSideBarDrawer::getHouseDisplayName: нет функции; cSideBarDrawer::drawHdRadarPanel: нет функции; cSideBarDrawer::drawHdMeter: нет функции; cSideBarDrawer::drawHdCapacities: нет функции; cSideBarDrawer::drawHdBuildingLists: нет функции; cSideBarDrawer::setPlayer: src/drawers/cSideBarDrawer.cpp@832c953:93-101	src/drawers/cSideBarDrawer.cpp@832c953:81,src/drawers/cSideBarDrawer.cpp@832c953:92
src/drawers/cSideBarDrawer.h	src/drawers/cSideBarDrawer.h@9208dcf:6-20	вне функций — объявление класса и полей	Добавлены UiAuditAccess и массив HD-текстур гербов, удалено состояние Candybar.	боковая панель, герб Дома, другое — доступ UI-аудита	П5г	объявление класса и полей: src/drawers/cSideBarDrawer.h@832c953:35	src/drawers/cSideBarDrawer.h@832c953:1
src/drawers/cSideBarDrawer.h	src/drawers/cSideBarDrawer.h@9208dcf:30-54	вне функций — объявление класса и методов	Старые методы и поля Candybar/вертикальных индикаторов заменены приватными методами HD-панели.	боковая панель	П5в	объявление класса и методов: src/drawers/cSideBarDrawer.h@832c953:35	src/drawers/cSideBarDrawer.h@832c953:1
```
### Дорожка 2

```tsv
путь в FORK1	строки участка в FORK1	функция или функции FORK1	что меняет участок	область	шаг	место в PORT	PORT отличается от BASE в этом месте
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:2-8	вне функций — подключения	Подключает средства аудита интерфейса.	другое — подключения	П5г	нет	—
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:10-28	cDrawManager	Подключает локализацию и компоновщики верхней строки и музыкальных элементов управления, а также добавляет командную строку в состав менеджера отрисовки.	верхняя строка, другое — командная строка	П7,П9,П10	cDrawManager — src/managers/cDrawManager.cpp@832c953:59-87	src/managers/cDrawManager.cpp@832c953:1
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:31-48	cDrawManager, cDrawManager::~cDrawManager	Добавляет малый шрифт и менеджер скорости игры; удаляет хранение и освобождение старой текстуры кнопки параметров.	верхняя строка, мышь	П5в	cDrawManager — src/managers/cDrawManager.cpp@832c953:59-87; cDrawManager::~cDrawManager — src/managers/cDrawManager.cpp@832c953:116-118	src/managers/cDrawManager.cpp@832c953:1
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:77-82	cDrawManager::drawCombatState	Убирает вызов старой панели параметров из отрисовки боевого состояния.	верхняя строка	П5в	cDrawManager::drawCombatState — src/managers/cDrawManager.cpp@832c953:120-178	src/managers/cDrawManager.cpp@832c953:1, src/managers/cDrawManager.cpp@832c953:170
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:86-97	cDrawManager::drawCombatState	Добавляет музыкальные элементы верхней строки и командную строку; удаляет старую отрисовку полосы параметров.	строка сообщений, верхняя строка, другое — командная строка	П9,П10	cDrawManager::drawCombatState — src/managers/cDrawManager.cpp@832c953:120-178	src/managers/cDrawManager.cpp@832c953:1, src/managers/cDrawManager.cpp@832c953:170
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:135-147	cDrawManager::drawDebugInfoUsages	Локализует подписи отладочного счётчика объектов.	другое — отладочная статистика	П5в	cDrawManager::drawDebugInfoUsages — src/managers/cDrawManager.cpp@832c953:180-218	src/managers/cDrawManager.cpp@832c953:170
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:161-178	cDrawManager::drawRallyPoint	Берёт логический размер указателя перемещения вместо размера SDL-поверхности.	поле боя и камера	П5в	cDrawManager::drawRallyPoint — src/managers/cDrawManager.cpp@832c953:225-254	src/managers/cDrawManager.cpp@832c953:170
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:231-442	cDrawManager::drawTopBarBackground, cDrawManager::drawTopBarMusicControls, cDrawManager::drawMusicControls, cDrawManager::setPlayerToDraw, cDrawManager::drawNotifications	Перерисовывает верхнюю строку, добавляет музыкальные кнопки и регулятор скорости, привязывает уведомления к командной строке и обновляет её игрока.	строка сообщений, верхняя строка, мышь, другое — командная строка	П9,П10	cDrawManager::drawTopBarBackground — src/managers/cDrawManager.cpp@832c953:301-315; cDrawManager::drawTopBarMusicControls — нет функции; cDrawManager::drawMusicControls — нет функции; cDrawManager::setPlayerToDraw — src/managers/cDrawManager.cpp@832c953:317-331; cDrawManager::drawNotifications — нет функции	src/managers/cDrawManager.cpp@832c953:301
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:456-462	cDrawManager::onNotifyMouseEvent	Передаёт события мыши командной строке.	мышь, другое — командная строка	П10	cDrawManager::onNotifyMouseEvent — src/managers/cDrawManager.cpp@832c953:354-357	src/managers/cDrawManager.cpp@832c953:301
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:527-537	cDrawManager::getMessage	Предоставляет текущий текст сообщения.	строка сообщений	П5в	cDrawManager::getMessage — src/managers/cDrawManager.cpp@832c953:433-436	src/managers/cDrawManager.cpp@832c953:374
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:2-8	вне функций — подключения	Подключает класс командной строки.	другое — подключения	П10	нет	—
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:22-28	вне функций — объявление класса	Объявляет тип менеджера скорости игры.	другое — объявление класса	П5в	нет	—
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:47-56	cDrawManager::getCommandBarDrawer	Открывает доступ к объекту командной строки.	другое — командная строка	П10	cDrawManager::getCommandBarDrawer — нет функции	—
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:82-88	вне функций — объявление класса	Объявляет получение текущего сообщения.	строка сообщений	П5в	src/managers/cDrawManager.h@832c953:106	src/managers/cDrawManager.h@832c953:103
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:102-118	вне функций — объявление класса	Объявляет отрисовку музыкальных элементов, удаляет метод старой полосы параметров и добавляет поле командной строки.	верхняя строка, другое — командная строка	П9,П10	нет	—
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:121-135	вне функций — объявление класса	Добавляет поля малого шрифта, менеджера скорости и состояния перетаскивания регулятора.	верхняя строка, мышь	П5в	нет	—
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:1-9	вне функций — подключения	Подключает контекст управления и данные игрока для обновления наведения мыши.	другое — подключения	П5в	нет	—
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:11-37	findTileIndex	Добавляет двоичный поиск клетки по её экранному интервалу.	поле боя и камера	П5в	findTileIndex — нет функции	—
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:41-47	cMapCamera::cMapCamera	Инициализирует масштаб камеры мировым масштабом и учитывает размеры панели и верхней строки.	поле боя и камера, боковая панель, верхняя строка	П5в	cMapCamera::cMapCamera — src/gameobjects/map/cMapCamera.cpp@832c953:32-65	src/gameobjects/map/cMapCamera.cpp@832c953:1
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:67-87	cMapCamera::resetZoom, cMapCamera::zoomIn	Добавляет сброс масштаба к мировому значению и обновляет наведение мыши после масштабирования.	поле боя и камера, мышь	П5в	cMapCamera::resetZoom — src/gameobjects/map/cMapCamera.cpp@832c953:71-74; cMapCamera::zoomIn — src/gameobjects/map/cMapCamera.cpp@832c953:103-109	src/gameobjects/map/cMapCamera.cpp@832c953:1
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:110-116	cMapCamera::zoomOut	Обновляет наведение мыши после уменьшения масштаба.	поле боя и камера, мышь	П5в	cMapCamera::zoomOut — src/gameobjects/map/cMapCamera.cpp@832c953:130-136	src/gameobjects/map/cMapCamera.cpp@832c953:1
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:169-190	cMapCamera::centerAndJumpViewPortToCell, cMapCamera::thinkFast	Переносит ограничение камеры в общий переход и обновляет наведение после перемещения.	поле боя и камера, мышь	П5в	cMapCamera::centerAndJumpViewPortToCell — src/gameobjects/map/cMapCamera.cpp@832c953:171-197; cMapCamera::thinkFast — src/gameobjects/map/cMapCamera.cpp@832c953:199-207	src/gameobjects/map/cMapCamera.cpp@832c953:1
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:192-204	cMapCamera::jumpTo, cMapCamera::setViewportPosition	Ограничивает координаты при переходе камеры и обновляет наведение мыши.	поле боя и камера, мышь	П5в	cMapCamera::jumpTo — src/gameobjects/map/cMapCamera.cpp@832c953:209-214; cMapCamera::setViewportPosition — src/gameobjects/map/cMapCamera.cpp@832c953:216-220	src/gameobjects/map/cMapCamera.cpp@832c953:1
src/map/cMapCamera.cpp	src/map/cMapCamera.cpp@9208dcf:206-231	cMapCamera::getCellFromWindowPosition, cMapCamera::refreshMouseHover	Преобразует экранные координаты в клетку и пересчитывает наведение после изменения камеры.	поле боя и камера, мышь	П5в	cMapCamera::getCellFromWindowPosition — нет функции; cMapCamera::refreshMouseHover — нет функции	—
src/map/cMapCamera.h	src/map/cMapCamera.h@9208dcf:29-35	вне функций — объявление класса	Выносит реализацию сброса масштаба из заголовка.	поле боя и камера	П5в	src/gameobjects/map/cMapCamera.h@832c953:53	src/gameobjects/map/cMapCamera.h@832c953:1
src/map/cMapCamera.h	src/map/cMapCamera.h@9208dcf:89-105	cMapCamera::getAbsMapMouseX, cMapCamera::getAbsMapMouseY	Корректирует перевод экранного пикселя в координаты карты с учётом округления на границе клетки.	поле боя и камера, мышь	П5в	cMapCamera::getAbsMapMouseX — нет функции; cMapCamera::getAbsMapMouseY — нет функции	—
src/map/cMapCamera.h	src/map/cMapCamera.h@9208dcf:142-156	cMapCamera::getTileDrawWidth, cMapCamera::getTileDrawHeight	Добавляет ширину и высоту прямоугольника отрисовки клетки с запасом в один пиксель.	поле боя и камера	П5в	cMapCamera::getTileDrawWidth — нет функции; cMapCamera::getTileDrawHeight — нет функции	—
src/map/cMapCamera.h	src/map/cMapCamera.h@9208dcf:218-225	вне функций — объявление класса	Объявляет обновление наведения мыши.	мышь, поле боя и камера	П5в	нет	—
src/map/cMapCamera.h	src/map/cMapCamera.h@9208dcf:238-243	вне функций — объявление класса	Предоставляет аудитору интерфейса доступ к приватным полям камеры.	другое — доступ аудита интерфейса	П5г	нет	—
src/sidebar/cBuildingList.cpp	src/sidebar/cBuildingList.cpp@9208dcf:253-266	cBuildingList::isOverButton	Использует фактическую ширину и высоту кнопки при проверке попадания мышью.	список построек, мышь	П5в	cBuildingList::isOverButton — src/sidebar/cBuildingList.cpp@832c953:272-275	нет
src/sidebar/cBuildingList.cpp	src/sidebar/cBuildingList.cpp@9208dcf:476-479	cBuildingList::startFlashing	Добавляет завершающий перевод строки после функции.	другое — оформление файла	П5в	cBuildingList::startFlashing — src/sidebar/cBuildingList.cpp@832c953:502-505	src/sidebar/cBuildingList.cpp@832c953:496
src/sidebar/cBuildingList.h	src/sidebar/cBuildingList.h@9208dcf:79-100	cBuildingList::getButtonWidth, cBuildingList::getButtonHeight, cBuildingList::getItemCount	Добавляет получение размеров кнопки и числа пунктов списка.	список построек	П5в	cBuildingList::getButtonWidth — нет функции; cBuildingList::getButtonHeight — нет функции; cBuildingList::getItemCount — нет функции	—
src/sidebar/cBuildingListFactory.cpp	src/sidebar/cBuildingListFactory.cpp@9208dcf:2-8	вне функций — подключения	Подключает компоновщик HUD.	другое — подключения	П5в	нет	—
src/sidebar/cBuildingListFactory.cpp	src/sidebar/cBuildingListFactory.cpp@9208dcf:21-38	cBuildingListFactory::getButtonDrawY, cBuildingListFactory::getButtonDrawXStart	Берёт координаты вкладок из компоновщика HUD.	список построек	П5в	cBuildingListFactory::getButtonDrawY — src/sidebar/cBuildingListFactory.cpp@832c953:23-28; cBuildingListFactory::getButtonDrawXStart — src/sidebar/cBuildingListFactory.cpp@832c953:30-33	src/sidebar/cBuildingListFactory.cpp@832c953:1, src/sidebar/cBuildingListFactory.cpp@832c953:29
src/sidebar/cBuildingListFactory.cpp	src/sidebar/cBuildingListFactory.cpp@9208dcf:46-59	cBuildingListFactory::initializeList	Задаёт вкладкам списка ширину и высоту из области вкладок HUD.	список построек	П5в	cBuildingListFactory::initializeList — src/sidebar/cBuildingListFactory.cpp@832c953:36-105	src/sidebar/cBuildingListFactory.cpp@832c953:29
src/sidebar/cBuildingListItem.cpp	src/sidebar/cBuildingListItem.cpp@9208dcf:2-8	вне функций — подключения	Подключает локализацию описаний пунктов списка.	список построек	П7	нет	—
src/sidebar/cBuildingListItem.cpp	src/sidebar/cBuildingListItem.cpp@9208dcf:384-410	cBuildingListItem::getInfo	Переводит описания стоимости, энергии, времени и неизвестного типа пункта списка.	список построек	П5в	cBuildingListItem::getInfo — src/sidebar/cBuildingListItem.cpp@832c953:397-431	src/sidebar/cBuildingListItem.cpp@832c953:391, src/sidebar/cBuildingListItem.cpp@832c953:413
src/sidebar/cBuildingListItem.cpp	src/sidebar/cBuildingListItem.cpp@9208dcf:443-447	cBuildingListItem::getNameString	Локализует имя неизвестного типа пункта списка.	список построек	П5в	cBuildingListItem::getNameString — src/sidebar/cBuildingListItem.cpp@832c953:448-468	src/sidebar/cBuildingListItem.cpp@832c953:432
src/sidebar/cBuildingListItem.h	src/sidebar/cBuildingListItem.h@9208dcf:12-18	вне функций — объявление класса	Объявляет менеджер сохранения.	другое — объявление класса	П8	нет	—
src/sidebar/cBuildingListItem.h	src/sidebar/cBuildingListItem.h@9208dcf:253-259	вне функций — объявление класса	Разрешает менеджеру сохранения доступ к полям элемента списка построек.	список построек, другое — сохранение игры	П8	нет	—
src/sidebar/cBuildingListUpdater.cpp	src/sidebar/cBuildingListUpdater.cpp@9208dcf:2-8	вне функций — подключения	Подключает очередь заказов космопорта.	список построек	П10	нет	—
src/sidebar/cBuildingListUpdater.cpp	src/sidebar/cBuildingListUpdater.cpp@9208dcf:436-450	cBuildingListUpdater::onStructureDestroyed	При утрате последнего космопорта удаляет его пункты и передаёт выбор другой вкладке через событие недоступности списка.	список построек, боковая панель	П10	cBuildingListUpdater::onStructureDestroyed — src/sidebar/cBuildingListUpdater.cpp@832c953:494-543	src/sidebar/cBuildingListUpdater.cpp@832c953:486, src/sidebar/cBuildingListUpdater.cpp@832c953:538
src/sidebar/cSideBar.cpp	src/sidebar/cSideBar.cpp@9208dcf:302-309	cSideBar::onNotifyMouseEvent	Передаёт события мыши от боковой панели списку построек.	список построек, боковая панель, мышь	П5в	cSideBar::onNotifyMouseEvent — src/sidebar/cSideBar.cpp@832c953:343-369	src/sidebar/cSideBar.cpp@832c953:342, src/sidebar/cSideBar.cpp@832c953:357
src/sidebar/cSideBar.cpp	src/sidebar/cSideBar.cpp@9208dcf:314-322	cSideBar::onNotifyMouseEvent	Игнорирует события прокрутки после передачи их списку построек.	список построек, боковая панель, мышь	П5в	cSideBar::onNotifyMouseEvent — src/sidebar/cSideBar.cpp@832c953:343-369	src/sidebar/cSideBar.cpp@832c953:342, src/sidebar/cSideBar.cpp@832c953:357
src/sidebar/cSideBar.cpp	src/sidebar/cSideBar.cpp@9208dcf:408-422	cSideBar::configureLayout	Настраивает ширину боковой панели по режиму HD и логической ширине экрана.	боковая панель	П5в	cSideBar::configureLayout — нет функции	—
src/sidebar/cSideBar.h	src/sidebar/cSideBar.h@9208dcf:79-87	вне функций — объявление класса	Делает ширину боковой панели изменяемой при настройке HD.	боковая панель	П5в	src/sidebar/cSideBar.h@832c953:103	src/sidebar/cSideBar.h@832c953:102
src/sidebar/cSideBar.h	src/sidebar/cSideBar.h@9208dcf:95-102	вне функций — объявление класса	Объявляет настройку размеров боковой панели.	боковая панель	П5в	нет	—
```
### Сверка количества участков по файлам

Команда подсчёта: `/srv/dune/venv/bin/python .tmp/p5cr2/summarize_tables.py`. Вывод успешного запуска:

fork-hunks-1.tsv: 42 строк
  файл src/drawers/CreditsDrawer.cpp: 4
  файл src/drawers/CreditsDrawer.h: 2
  файл src/drawers/cBuildingListDrawer.cpp: 17
  файл src/drawers/cBuildingListDrawer.h: 3
  файл src/drawers/cMessageDrawer.cpp: 3
  файл src/drawers/cMessageDrawer.h: 1
  файл src/drawers/cMiniMapDrawer.cpp: 6
  файл src/drawers/cMiniMapDrawer.h: 2
  файл src/drawers/cSideBarDrawer.cpp: 2
  файл src/drawers/cSideBarDrawer.h: 2
  шаг П5в: 33
  шаг П5г: 5
  шаг П7: 3
  шаг П8: 0
  шаг П9: 2
  шаг П10: 0
fork-hunks-2.tsv: 47 строк
  файл src/managers/cDrawManager.cpp: 10
  файл src/managers/cDrawManager.h: 6
  файл src/map/cMapCamera.cpp: 8
  файл src/map/cMapCamera.h: 5
  файл src/sidebar/cBuildingList.cpp: 2
  файл src/sidebar/cBuildingList.h: 1
  файл src/sidebar/cBuildingListFactory.cpp: 3
  файл src/sidebar/cBuildingListItem.cpp: 3
  файл src/sidebar/cBuildingListItem.h: 2
  файл src/sidebar/cBuildingListUpdater.cpp: 2
  файл src/sidebar/cSideBar.cpp: 3
  файл src/sidebar/cSideBar.h: 2
  шаг П5в: 33
  шаг П5г: 2
  шаг П7: 2
  шаг П8: 2
  шаг П9: 4
  шаг П10: 9


Первый запуск этого вспомогательного подсчёта завершился `KeyError: 'путь'` из-за неверного имени ключа TSV; заголовок таблицы прочитан как `путь в FORK1`, ключ исправлен, успешный повторный вывод приведён выше. Полный вывод первого запуска: см. `summary-counts.txt`.

### Команды и выводы для дорожек 1 и 2

# Доказательства: P5CR2, дорожка 1

Все чтения Git выполнялись с явными ревизиями. Для чтения и сверки использовались `BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566` и `PORT=832c953a94a632d57872349013f7ed1a37434715`.

## Наличие файлов в PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python - <<'PY'
import subprocess
rev='832c953a94a632d57872349013f7ed1a37434715'
files='src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h'.split()
for path in files:
 subprocess.run(['git','cat-file','-e',rev+':'+path],check=True)
 print(path+': файл присутствует в PORT')
PY
```

Вывод:

```text
src/drawers/CreditsDrawer.cpp: файл присутствует в PORT
src/drawers/CreditsDrawer.h: файл присутствует в PORT
src/drawers/cBuildingListDrawer.cpp: файл присутствует в PORT
src/drawers/cBuildingListDrawer.h: файл присутствует в PORT
src/drawers/cMessageDrawer.cpp: файл присутствует в PORT
src/drawers/cMessageDrawer.h: файл присутствует в PORT
src/drawers/cMiniMapDrawer.cpp: файл присутствует в PORT
src/drawers/cMiniMapDrawer.h: файл присутствует в PORT
src/drawers/cSideBarDrawer.cpp: файл присутствует в PORT
src/drawers/cSideBarDrawer.h: файл присутствует в PORT
```

## Построение таблицы и сверка

Таблица формируется скриптом `build_fork_hunks_1.py`. Он читает участки `git diff --unified=3 BASE FORK1 -- <путь>`, сопоставляет функции и диапазоны в `PORT` через `git show PORT:<путь>` и проверяет пересечения по участкам `git diff --unified=3 BASE PORT -- <путь>`. Строки словаря шагов проверяются на всех строках добавления, удаления и контекста каждого участка.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/build_fork_hunks_1.py
```

Вывод:

```text
Создана таблица: .tmp/p5cr2/fork-hunks-1.tsv (42 строк данных).
src/drawers/CreditsDrawer.cpp: таблица=4; @@=4; OK
src/drawers/CreditsDrawer.h: таблица=2; @@=2; OK
src/drawers/cBuildingListDrawer.cpp: таблица=17; @@=17; OK
src/drawers/cBuildingListDrawer.h: таблица=3; @@=3; OK
src/drawers/cMessageDrawer.cpp: таблица=3; @@=3; OK
src/drawers/cMessageDrawer.h: таблица=1; @@=1; OK
src/drawers/cMiniMapDrawer.cpp: таблица=6; @@=6; OK
src/drawers/cMiniMapDrawer.h: таблица=2; @@=2; OK
src/drawers/cSideBarDrawer.cpp: таблица=2; @@=2; OK
src/drawers/cSideBarDrawer.h: таблица=2; @@=2; OK
```

Отдельная команда сверки, которая пересчитывает строки таблицы по каждому файлу и число строк `@@` в соответствующем diff:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/verify_fork_hunks_1.py
```

Её stdout:

```text
src/drawers/CreditsDrawer.cpp: строки таблицы=4; участки @@=4; OK
src/drawers/CreditsDrawer.h: строки таблицы=2; участки @@=2; OK
src/drawers/cBuildingListDrawer.cpp: строки таблицы=17; участки @@=17; OK
src/drawers/cBuildingListDrawer.h: строки таблицы=3; участки @@=3; OK
src/drawers/cMessageDrawer.cpp: строки таблицы=3; участки @@=3; OK
src/drawers/cMessageDrawer.h: строки таблицы=1; участки @@=1; OK
src/drawers/cMiniMapDrawer.cpp: строки таблицы=6; участки @@=6; OK
src/drawers/cMiniMapDrawer.h: строки таблицы=2; участки @@=2; OK
src/drawers/cSideBarDrawer.cpp: строки таблицы=2; участки @@=2; OK
src/drawers/cSideBarDrawer.h: строки таблицы=2; участки @@=2; OK
ИТОГО: 42 строк данных; число строк совпадает с числом @@ во всех 10 файлах.
```

В таблице находятся строки FORK1 по новой стороне заголовков `@@`; для участков без добавленных строк указана начальная строка и пометка «только удаление». Скрипты, таблица и этот отчёт находятся в `.tmp/p5cr2/`.

## Точность описания участка cBuildingListDrawer.cpp@9208dcf:354-360

Спот-проверка показала, что этот участок заменяет строку `Upgrading` локализованным вызовом с ключом `Upgrade` и русским текстом `Улучшение`. Описание соответствующей ячейки таблицы и запись в скрипте-генераторе уточнены; остальные ячейки таблицы не менялись.

Команда проверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp | rg -n -C 3 'localization::text\("Upgrade"'
```

Вывод:

```text
337- 
338-                     Color red = Color{255, 0, 0,255};
339--                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
340:+                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
341-                 }
342- 
343-                 // Pending building (ie: a build is progressing, blocking the upgrade)
```

Полный stdout исходной команды `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp` находится в разделе `src/drawers/cBuildingListDrawer.cpp: BASE → FORK1` файла `.tmp/p5cr2/track1-source-outputs.md`.

# Точные stdout diff-команд для дорожки 1

Ревизии: BASE `e17379ad660fca46859b403a6c3d33ec8d831a40`, FORK1 `9208dcf5a358f40afd95c99480e4e09f781ed566`, PORT `832c953a94a632d57872349013f7ed1a37434715`.
Команды выполнены с контекстом Git по умолчанию (3 строки). В каждом блоке сохранён полный stdout соответствующей команды без фильтрации.

## src/drawers/CreditsDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp
```

stdout (6253 байт):

````text
diff --git a/src/drawers/CreditsDrawer.cpp b/src/drawers/CreditsDrawer.cpp
index da5a87ab..119e8466 100644
--- a/src/drawers/CreditsDrawer.cpp
+++ b/src/drawers/CreditsDrawer.cpp
@@ -7,16 +7,22 @@
 #include "utils/cSoundPlayer.h"
 #include "drawers/SDLDrawer.hpp"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/TextContext.hpp"
+#include "sidebar/HudLayout.hpp"
 #include <SDL2/SDL.h>
+#include <algorithm>
+#include <format>
 
 #include "data/gfxaudio.h"
 
 CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
     m_player(player),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer())
 {
     assert(player);
 
@@ -31,7 +37,7 @@ CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
     previousCredits = 0;
 
     // center credits bar within sidebar
-    int widthCreditsBar = (m_gfxinter->getSurface(CREDITS_BAR))->w;
+    int widthCreditsBar = m_gfxinter->getLogicalWidth(CREDITS_BAR);
     drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
     drawY = 0;
 }
@@ -179,25 +185,64 @@ void CreditsDrawer::thinkAboutIndividualCreditOffsets()
  */
 void CreditsDrawer::draw()
 {
-    auto *tex = m_gfxinter->getTexture(CREDITS_BAR);
-    renderDrawer->renderSprite(tex, drawX, drawY);
-    renderDrawer->setClippingFor(drawX+1, drawY+5, drawX+tex->w-1, drawY+tex->h-5);
-    drawCurrentCredits(drawX, drawY);
-    drawPreviousCredits(drawX, drawY);
-    renderDrawer->resetClippingFor();
-
-}
-
-int CreditsDrawer::getXDrawingOffset(int amount)
-{
-    int offset = 1;
-    if (amount > 0)		offset =  4;
-    if (amount < 10)	offset =  5;
-    if (amount > 99)	offset =  3;
-    if (amount > 999)	offset =  2;
-    if (amount > 9999) 	offset =  1;
-    if (amount > 99999) offset =  0;
-    return offset;
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const cRectangle &rect = layout.credits;
+    const Color panel{15, 19, 21, 255};
+    const Color border{155, 116, 43, 255};
+    const Color label{208, 196, 157, 255};
+    const Color amount{255, 210, 82, 255};
+
+    renderDrawer->renderRectFillColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        panel
+    );
+    renderDrawer->renderRectColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        border
+    );
+    renderDrawer->renderRectFillColor(
+        rect.getX() + 7,
+        rect.getY() + 10,
+        12,
+        14,
+        Color{205, 133, 35, 255}
+    );
+    renderDrawer->renderRectColor(
+        rect.getX() + 7,
+        rect.getY() + 10,
+        12,
+        14,
+        Color{255, 215, 103, 255}
+    );
+    m_gameTextDrawer->drawText(
+        rect.getX() + 26,
+        rect.getY() + 10,
+        label,
+        localization::text("CREDITS", "КРЕДИТЫ"),
+        false
+    );
+
+    const std::string credits = std::format(
+        "{}",
+        std::max(0, currentCredits)
+    );
+    const int amountWidth = m_gameTextDrawer->getTextLength(credits);
+    m_gameTextDrawer->drawText(
+        rect.getEndX() - amountWidth - 9,
+        rect.getY() + 10,
+        amount,
+        credits,
+        false
+    );
 }
 
 int CreditsDrawer::getCreditDrawId(char c)
@@ -215,75 +260,6 @@ int CreditsDrawer::getCreditDrawId(char c)
     return CREDITS_NONE;
 }
 
-// current credits are either drawn from 'above' or from below. (depending on direction)
-// the offset pushes them more up or down.
-void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
-{
-    if (currentCredits < 0) currentCredits = 0;
-
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", currentCredits);
-
-    int offset = getXDrawingOffset(currentCredits);
-
-    for (int i=0; i < 6; i++) {
-        // the actual position to draw on is: ((game.m_screenX - 120) +
-        //        screen        -  14 + (6 digits (each 20 pixels due borders))
-        int dx = ((offset + i) * 20);
-        int dy = 0;
-
-        // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = 20 - (int)offset_credit[i];
-        }
-        else if (offset_direction[i] == 2) {
-            dy = -20 + (int)offset_credit[i];
-        }
-
-        int nr = getCreditDrawId(credits[i]);
-
-        if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
-        }
-    }
-}
-
-// current credits are either drawn from 'above' or from below. (depending on direction)
-// the offset pushes them more up or down.
-void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
-{
-    if (previousCredits < 0) previousCredits = 0;
-
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", previousCredits);
-
-    int offset = getXDrawingOffset(previousCredits);
-
-    for (int i=0; i < 6; i++) {
-        // the actual position to draw on is: ((game.m_screenX - 120) +
-        //        screen        -  14 + (6 digits (each 20 pixels due borders))
-        int dx = ((offset + i) * 20);
-        int dy = 0;
-
-        // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = (int)offset_credit[i] * -1;
-        }
-        else if (offset_direction[i] == 2) {
-            dy = (int)offset_credit[i];
-        }
-        int nr = getCreditDrawId(credits[i]);
-
-        if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
-        }
-    }
-}
-
 // the think method will gradually update the currentCredits array so that it is 'the same'
 bool CreditsDrawer::hasDrawnCurrentCredits()
 {
````

## src/drawers/CreditsDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/CreditsDrawer.cpp
```

stdout (16086 байт):

````text
diff --git a/src/drawers/CreditsDrawer.cpp b/src/drawers/CreditsDrawer.cpp
index da5a87ab..daa24388 100644
--- a/src/drawers/CreditsDrawer.cpp
+++ b/src/drawers/CreditsDrawer.cpp
@@ -1,39 +1,85 @@
-#include "CreditsDrawer.h"
+/**
+ * @file CreditsDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
-#include "d2tmc.h"
+#include "CreditsDrawer.h"
+#include "CreditsMath.hpp"
+#include "include/sGameServices.h"
+#include "utils/common.h"
+#include "context/AudioContext.hpp"
+#include "game/cGameSettings.h"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
+#include "sidebar/cSideBar.h"
 #include "utils/cSoundPlayer.h"
 #include "drawers/SDLDrawer.hpp"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
-#include <SDL2/SDL.h>
-
 #include "data/gfxaudio.h"
 
-CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
+#include <SDL3/SDL.h>
+#include "include/cAssert.h"
+#include "include/Texture.hpp"
+#include <algorithm>
+#include <cstdlib>
+#include <string>
+
+namespace {
+// digits of the credits, cut off / padded with '\0' to 8 characters (what the old char[9] buffers held)
+std::string creditsToDigits(int credits)
+{
+    std::string digits = std::to_string(credits);
+    digits.resize(8, '\0');
+    return digits;
+}
+}
+
+CreditsDrawer::CreditsDrawer(GameContext* ctx, cGameSettings *settings, cPlayer *player) :
     m_player(player),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_gfxdata(ctx->getGraphicsContext()->gfxdata.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_playCreditsSound(settings->isPlayCreditsSound())
 {
-    assert(player);
-
-    memset(offset_credit, 0, sizeof(offset_credit));
-    memset(offset_direction, 0, sizeof(offset_direction));
-    initial = true;
-    soundType = -1;
-    rollSpeed = 0.0F;
-    rolled = 0;
-    soundsMade = 0;
-    currentCredits = 0;
-    previousCredits = 0;
+    d2tm_assert(player!= nullptr);
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(settings != nullptr);
+
+    std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+    std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
+    m_initial = true;
+    m_soundType = -1;
+    m_rollSpeed = 0.0F;
+    m_rolled = 0;
+    m_soundsMade = 0;
+    m_currentCredits = 0;
+    m_previousCredits = 0;
 
     // center credits bar within sidebar
-    int widthCreditsBar = (m_gfxinter->getSurface(CREDITS_BAR))->w;
-    drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
-    drawY = 0;
+    int widthCreditsBar = m_gfxinter->getTexture(CREDITS_BAR)->w;
+    m_drawX = settings->getScreenW() - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
+    m_drawY = 0;
+}
+
+void CreditsDrawer::serviceInit(sGameServices* services)
+{
+    m_audioContext = services->ctx->getAudioContext();
+    m_mapCamera = services->mapCamera;
+    m_objects = services->objects;
 }
 
 CreditsDrawer::~CreditsDrawer()
@@ -48,71 +94,58 @@ void CreditsDrawer::setCredits()
 
 void CreditsDrawer::setCredits(int amount)
 {
-    initial = true;
-    previousCredits = amount;
-    currentCredits = amount;
-    memset(offset_credit, 0, sizeof(offset_credit));
-    memset(offset_direction, 0, sizeof(offset_direction));
+    m_initial = true;
+    m_previousCredits = amount;
+    m_currentCredits = amount;
+    std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+    std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
 }
 
 // timer based method
 void CreditsDrawer::thinkFast()
 {
 
-    if (hasDrawnCurrentCredits() || initial) {
-        soundsMade = 0;
+    if (hasDrawnCurrentCredits() || m_initial) {
+        m_soundsMade = 0;
 
-        memset(offset_credit, 0, sizeof(offset_credit));
-        memset(offset_direction, 0, sizeof(offset_direction));
+        std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+        std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
 
-        // determine new currentCredits
+        // determine new m_currentCredits
         // TODO: make it 'roll' instead of 'jump' to the newest credits?
-        previousCredits = currentCredits;
+        m_previousCredits = m_currentCredits;
         auto newCurrentCredits = m_player->getCredits();
 
-        if (newCurrentCredits != previousCredits) {
-            int diff = newCurrentCredits - previousCredits;
-            // when big difference, slice it up in pieces so we
-            // have a more fluent transition
-            if (diff > 200) {
-                currentCredits = previousCredits + (diff / 8);
-            }
-            else if (diff > 20) {
-                currentCredits = previousCredits + (diff / 4);
-            }
-            else {
-                currentCredits = newCurrentCredits;
-            }
-        }
+        m_currentCredits = CreditsMath::nextDisplayedCredits(m_previousCredits, newCurrentCredits);
 
         // decide what sound to play when done
-        if (currentCredits > previousCredits) {
-            soundType = SOUND_CREDITUP;
+        if (m_currentCredits > m_previousCredits) {
+            m_soundType = SOUND_CREDITUP;
         }
-        else if (currentCredits < previousCredits) {
-            soundType = SOUND_CREDITDOWN;
+        else if (m_currentCredits < m_previousCredits) {
+            m_soundType = SOUND_CREDITDOWN;
         }
         else {
-            soundType = -1;
+            m_soundType = -1;
         }
 
-        TIMER_money++;
-        if (TIMER_money > 20) {
-            if (rollSpeed > 0.0F) {
-                rollSpeed -= 0.005;
+        m_TIMER_money++;
+        if (m_TIMER_money > 20) {
+            if (m_rollSpeed > 0.0F) {
+                m_rollSpeed -= 0.005;
             }
-            if (rollSpeed < 0.0F) {
-                rollSpeed = 0.0F;
-                TIMER_money = 0;
+            if (m_rollSpeed < 0.0F) {
+                m_rollSpeed = 0.0F;
+                m_TIMER_money = 0;
             }
         }
 
-        initial = false;
+        m_initial = false;
     }
     else {
-        TIMER_money = 0;
-        if (rollSpeed < 3.0F) {
-            rollSpeed += 0.005;
+        m_TIMER_money = 0;
+        if (m_rollSpeed < 3.0F) {
+            m_rollSpeed += 0.005;
         }
         thinkAboutIndividualCreditOffsets();
     }
@@ -122,54 +155,50 @@ void CreditsDrawer::thinkFast()
 // it has to go 'up' or 'down'
 void CreditsDrawer::thinkAboutIndividualCreditOffsets()
 {
-    char current_credits[9];
-    char previous_credits[9];
-    memset(current_credits, 0, sizeof(current_credits));
-    memset(previous_credits, 0, sizeof(previous_credits));
-    snprintf(current_credits, sizeof(current_credits), "%d", currentCredits);
-    snprintf(previous_credits, sizeof(previous_credits), "%d", previousCredits);
+    std::string current_credits = creditsToDigits(m_currentCredits);
+    std::string previous_credits = creditsToDigits(m_previousCredits);
 
     for (int i = 0; i < 6; i++) {
-        int currentId = getCreditDrawId(current_credits[i]);
-        int previousId = getCreditDrawId(previous_credits[i]);
+        int currentId = CreditsMath::getCreditDrawId(current_credits[i]);
+        int previousId = CreditsMath::getCreditDrawId(previous_credits[i]);
 
-        if (offset_direction[i] == 0) {
+        if (m_offset_direction[i] == 0) {
             if (currentId == CREDITS_NONE || previousId == CREDITS_NONE) {
                 // either of the 2 is unidentifiable. Do nothing
-                offset_direction[i] = 3;
+                m_offset_direction[i] = 3;
                 continue; // next
             }
 
             // UP/DOWN ANIMATION: Is over the entire sum of money, so all 'credits' move the same
             // way.
-            if (currentCredits > previousCredits) {
-                offset_direction[i] = 1;
+            if (m_currentCredits > m_previousCredits) {
+                m_offset_direction[i] = 1;
             }
-            else if (previousCredits > currentCredits) {
-                offset_direction[i] = 2;
+            else if (m_previousCredits > m_currentCredits) {
+                m_offset_direction[i] = 2;
             }
 
             // when the same, do not animate
             if (currentId == previousId) {
-                offset_direction[i] = 3;
+                m_offset_direction[i] = 3;
             }
 
         }
 
         // always 'add' here, the draw routine knows how to handle this for up/down movement.
-        if (offset_credit[i] > 18.0F) {
-            //offset_credit[i] = 18.1F; // so we do not keep matching our IF :)
-            offset_credit[i] = 0.0F; // so we do not keep matching our IF :)
-            if (soundsMade < 7) {
-                game.playSound(soundType, 32);
-                soundsMade++;
+        if (m_offset_credit[i] > 18.0F) {
+            //m_offset_credit[i] = 18.1F; // so we do not keep matching our IF :)
+            m_offset_credit[i] = 0.0F; // so we do not keep matching our IF :)
+            if (m_playCreditsSound && m_soundsMade < 7) {
+                playSoundWithDistance(m_audioContext, m_mapCamera, m_objects, m_soundType, 32);
+                m_soundsMade++;
             }
             // it is fully 'moved'. Now update the array.
             previous_credits[i] = current_credits[i];
-            previousCredits = atoi(previous_credits);
+            m_previousCredits = std::atoi(previous_credits.c_str());
         }
         else {
-            offset_credit[i] += 1.0F * rollSpeed;
+            m_offset_credit[i] += 1.0F * m_rollSpeed;
         }
     }
 }
@@ -180,52 +209,23 @@ void CreditsDrawer::thinkAboutIndividualCreditOffsets()
 void CreditsDrawer::draw()
 {
     auto *tex = m_gfxinter->getTexture(CREDITS_BAR);
-    renderDrawer->renderSprite(tex, drawX, drawY);
-    renderDrawer->setClippingFor(drawX+1, drawY+5, drawX+tex->w-1, drawY+tex->h-5);
-    drawCurrentCredits(drawX, drawY);
-    drawPreviousCredits(drawX, drawY);
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->renderSprite(tex, m_drawX, m_drawY);
+    m_sdlDrawer->setClippingFor(m_drawX+1, m_drawY+5, m_drawX+tex->w-1, m_drawY+tex->h-5);
+    drawCurrentCredits(m_drawX, m_drawY);
+    drawPreviousCredits(m_drawX, m_drawY);
+    m_sdlDrawer->resetClippingFor();
 
 }
 
-int CreditsDrawer::getXDrawingOffset(int amount)
-{
-    int offset = 1;
-    if (amount > 0)		offset =  4;
-    if (amount < 10)	offset =  5;
-    if (amount > 99)	offset =  3;
-    if (amount > 999)	offset =  2;
-    if (amount > 9999) 	offset =  1;
-    if (amount > 99999) offset =  0;
-    return offset;
-}
-
-int CreditsDrawer::getCreditDrawId(char c)
-{
-    if (c == '0') return CREDITS_0;
-    if (c == '1') return CREDITS_1;
-    if (c == '2') return CREDITS_2;
-    if (c == '3') return CREDITS_3;
-    if (c == '4') return CREDITS_4;
-    if (c == '5') return CREDITS_5;
-    if (c == '6') return CREDITS_6;
-    if (c == '7') return CREDITS_7;
-    if (c == '8') return CREDITS_8;
-    if (c == '9') return CREDITS_9;
-    return CREDITS_NONE;
-}
-
 // current credits are either drawn from 'above' or from below. (depending on direction)
 // the offset pushes them more up or down.
 void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
 {
-    if (currentCredits < 0) currentCredits = 0;
+    if (m_currentCredits < 0) m_currentCredits = 0;
 
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", currentCredits);
+    std::string credits = creditsToDigits(m_currentCredits);
 
-    int offset = getXDrawingOffset(currentCredits);
+    int offset = CreditsMath::getXDrawingOffset(m_currentCredits);
 
     for (int i=0; i < 6; i++) {
         // the actual position to draw on is: ((game.m_screenX - 120) +
@@ -234,18 +234,18 @@ void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
         int dy = 0;
 
         // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = 20 - (int)offset_credit[i];
+        if (m_offset_direction[i] == 1) {
+            // up, means it comes from 'below' and the m_offset_credit is the 'coming up' part.
+            dy = 20 - static_cast<int>(m_offset_credit[i]);
         }
-        else if (offset_direction[i] == 2) {
-            dy = -20 + (int)offset_credit[i];
+        else if (m_offset_direction[i] == 2) {
+            dy = -20 + static_cast<int>(m_offset_credit[i]);
         }
 
-        int nr = getCreditDrawId(credits[i]);
+        int nr = CreditsMath::getCreditDrawId(credits[i]);
 
         if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
+            m_sdlDrawer->renderSprite(m_gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
         }
     }
 }
@@ -254,13 +254,11 @@ void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
 // the offset pushes them more up or down.
 void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
 {
-    if (previousCredits < 0) previousCredits = 0;
+    if (m_previousCredits < 0) m_previousCredits = 0;
 
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", previousCredits);
+    std::string credits = creditsToDigits(m_previousCredits);
 
-    int offset = getXDrawingOffset(previousCredits);
+    int offset = CreditsMath::getXDrawingOffset(m_previousCredits);
 
     for (int i=0; i < 6; i++) {
         // the actual position to draw on is: ((game.m_screenX - 120) +
@@ -269,25 +267,25 @@ void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
         int dy = 0;
 
         // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = (int)offset_credit[i] * -1;
+        if (m_offset_direction[i] == 1) {
+            // up, means it comes from 'below' and the m_offset_credit is the 'coming up' part.
+            dy = static_cast<int>(m_offset_credit[i]) * -1;
         }
-        else if (offset_direction[i] == 2) {
-            dy = (int)offset_credit[i];
+        else if (m_offset_direction[i] == 2) {
+            dy = static_cast<int>(m_offset_credit[i]);
         }
-        int nr = getCreditDrawId(credits[i]);
+        int nr = CreditsMath::getCreditDrawId(credits[i]);
 
         if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
+            m_sdlDrawer->renderSprite(m_gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
         }
     }
 }
 
-// the think method will gradually update the currentCredits array so that it is 'the same'
+// the think method will gradually update the m_currentCredits array so that it is 'the same'
 bool CreditsDrawer::hasDrawnCurrentCredits()
 {
-    return previousCredits == currentCredits;
+    return m_previousCredits == m_currentCredits;
 }
 
 void CreditsDrawer::setPlayer(cPlayer *thePlayer)
@@ -300,7 +298,7 @@ void CreditsDrawer::setPlayer(cPlayer *thePlayer)
 // thinkAboutIndividualCreditOffsets
 //
 //			if (currentId > previousId) {
-//				offset_direction[i] = 1; // UP
+//				m_offset_direction[i] = 1; // UP
 //			} else if (currentId < previousId) {
-//				offset_direction[i] = 2; // DOWN
+//				m_offset_direction[i] = 2; // DOWN
 //			}
````

## src/drawers/CreditsDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.h
```

stdout (794 байт):

````text
diff --git a/src/drawers/CreditsDrawer.h b/src/drawers/CreditsDrawer.h
index 76f39a43..9b9d6498 100644
--- a/src/drawers/CreditsDrawer.h
+++ b/src/drawers/CreditsDrawer.h
@@ -10,6 +10,7 @@
 class GameContext;
 class Graphics;
 class cPlayer;
+class cTextDrawer;
 struct SDL_Surface;
 
 // the credits drawer takes state of a player, and draws the credits accordingly
@@ -30,12 +31,10 @@ private:
     cPlayer *m_player;  //
     GameContext* m_ctx;
     Graphics* m_gfxinter;
+    cTextDrawer *m_gameTextDrawer;
 
     void thinkAboutIndividualCreditOffsets();
-    void drawCurrentCredits(int drawX, int drawY);
-    void drawPreviousCredits(int drawX, int drawY);
     int getCreditDrawId(char c);
-    int getXDrawingOffset(int amount);
 
     int TIMER_money;	// timer needed to do logic
 
````

## src/drawers/CreditsDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/CreditsDrawer.h
```

stdout (3443 байт):

````text
diff --git a/src/drawers/CreditsDrawer.h b/src/drawers/CreditsDrawer.h
index 76f39a43..689811ff 100644
--- a/src/drawers/CreditsDrawer.h
+++ b/src/drawers/CreditsDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file CreditsDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /*
  * CreditsDrawer.h
  *
@@ -8,17 +23,25 @@
 #pragma once
 
 class GameContext;
+class cGameSettings;
 class Graphics;
 class cPlayer;
 struct SDL_Surface;
+class SDLDrawer;
+class AudioContext;
+class cMapCamera;
+class cGameObjectContext;
+struct sGameServices;
 
 // the credits drawer takes state of a player, and draws the credits accordingly
 
 class CreditsDrawer {
 public:
-    explicit CreditsDrawer(GameContext* ctx, cPlayer *player);
+    explicit CreditsDrawer(GameContext* ctx, cGameSettings *settings, cPlayer *player);
     virtual ~CreditsDrawer();
 
+    void serviceInit(sGameServices* services);
+
     void thinkFast(); // set animation counters and such, time based. Also make sound when needed.
 
     void draw();
@@ -29,34 +52,38 @@ public:
 private:
     cPlayer *m_player;  //
     GameContext* m_ctx;
+    AudioContext* m_audioContext = nullptr;
+    cMapCamera* m_mapCamera = nullptr;
+    cGameObjectContext* m_objects = nullptr;
     Graphics* m_gfxinter;
+    Graphics* m_gfxdata;
+    SDLDrawer* m_sdlDrawer = nullptr;
+    bool m_playCreditsSound = true;
 
     void thinkAboutIndividualCreditOffsets();
     void drawCurrentCredits(int drawX, int drawY);
     void drawPreviousCredits(int drawX, int drawY);
-    int getCreditDrawId(char c);
-    int getXDrawingOffset(int amount);
 
-    int TIMER_money;	// timer needed to do logic
+    int m_TIMER_money;	// timer needed to do logic
 
-    float rollingSpeed;	// the 'rolling speed' of the credits. Need to be sped up when just starting
+    float m_rollingSpeed;	// the 'rolling speed' of the credits. Need to be sped up when just starting
     // to withdrawn money.
 
-    int currentCredits;		// current credits we want to draw
-    int previousCredits;	// previous credits we wanted to draw
+    int m_currentCredits;		// current credits we want to draw
+    int m_previousCredits;	// previous credits we wanted to draw
 
     // the offset of the current 'credit' being drawn (the Y offset)
-    float offset_credit[7];
-    int offset_direction[7]; // direction (0 = not yet determined / finished, 1 = UP, 2 = DOWN , 3 = DO NOTHING
+    float m_offset_credit[7];
+    int m_offset_direction[7]; // direction (0 = not yet determined / finished, 1 = UP, 2 = DOWN , 3 = DO NOTHING
 
     bool hasDrawnCurrentCredits();	// returns true whenever the new state has been finalized.
 
-    bool initial;
-    int soundType;
-    float rollSpeed;
-    int rolled; // how many credits did get rolled over?
-    int soundsMade; // sounds made per time frame
+    bool m_initial;
+    int m_soundType;
+    float m_rollSpeed;
+    int m_rolled; // how many credits did get rolled over?
+    int m_soundsMade; // sounds made per time frame
 
     // topleft position of credits-bar bmp
-    int drawX, drawY;
+    int m_drawX, m_drawY;
 };
````

## src/drawers/cBuildingListDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp
```

stdout (28207 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.cpp b/src/drawers/cBuildingListDrawer.cpp
index eb979610..8b935d08 100644
--- a/src/drawers/cBuildingListDrawer.cpp
+++ b/src/drawers/cBuildingListDrawer.cpp
@@ -5,18 +5,67 @@
 #include "data/gfxinter.h"
 #include "player/cPlayer.h"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
+#include "utils/common.h"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 
 #include <SDL2/SDL.h>
+#include <algorithm>
 #include <format>
+#include <sstream>
+#include <vector>
+
+namespace {
+void removeLastUtf8CodePoint(std::string &text)
+{
+    if (text.empty()) {
+        return;
+    }
+    std::size_t position = text.size() - 1;
+    while (position > 0 &&
+           (static_cast<unsigned char>(text[position]) & 0xC0U) == 0x80U) {
+        --position;
+    }
+    text.erase(position);
+}
+
+std::string fitWithEllipsis(
+    const cTextDrawer *drawer,
+    std::string text,
+    int maximumWidth)
+{
+    if (drawer->getTextLength(text) <= maximumWidth) {
+        return text;
+    }
+    constexpr const char *ellipsis = "…";
+    while (!text.empty() &&
+           drawer->getTextLength(text + ellipsis) > maximumWidth) {
+        removeLastUtf8CodePoint(text);
+    }
+    return text + ellipsis;
+}
+
+std::string compactCardName(const std::string &name)
+{
+    // Keep canonical names in status messages and save-independent game data,
+    // but use familiar short forms in the narrow construction cards.
+    if (name == localization::text("Hi-Tech", "Авиазавод")) return localization::text("Hi-Tech", "Авиазавод");
+    if (name == localization::text("Spice Refinery", "Переработчик пряности")) return localization::text("Refinery", "Переработчик");
+    if (name == localization::text("MCV", "Мобильная база")) return localization::text("MCV", "Мобильная база");
+    if (name == localization::text("Light Infantry", "Отряд пехоты")) return localization::text("Infantry", "Пехота");
+    if (name == localization::text("Troopers", "Отряд ракетчиков")) return localization::text("Troopers", "Ракетчики");
+    return name;
+}
+}
 
 cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
     m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
     m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_player(player),
-    m_renderListIds(false)
+    m_renderListIds(false),
+    m_readyLabel(localization::text("READY", "ГОТОВО"))
 {
 }
 
@@ -48,8 +97,8 @@ void cBuildingListDrawer::drawButtonHoverRectangle(cBuildingList *list)
     int y = list->getButtonDrawY();
     int id = list->getButtonIconIdUnpressed();
 
-    int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int width = list->getButtonWidth();
+    int height = list->getButtonHeight();
 
     Color color = m_player->getSelectFadingColor();
 
@@ -76,47 +125,77 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
     }
 
 //	int width = (gfxinter->getSurface(id))->w;
-    int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
-
-    // clear
-    renderDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
-
-    // set blender
-    renderDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
-
+    int width = list->getButtonWidth();
+    int height = list->getButtonHeight();
+
+    const Color panel{18, 22, 25, 255};
+    const Color border{93, 78, 49, 255};
+    const Color active{217, 164, 54, 255};
+    renderDrawer->renderRectFillColor(x, y, width, height, panel);
+
+    Texture *icon = m_gfxinter->getTexture(id);
+    const int availableWidth = std::max(1, width - 8);
+    const int availableHeight = std::max(1, height - 6);
+    const float scale = std::min(
+        static_cast<float>(availableWidth) / icon->w,
+        static_cast<float>(availableHeight) / icon->h
+    );
+    const int iconWidth = std::max(1, static_cast<int>(icon->w * scale));
+    const int iconHeight = std::max(1, static_cast<int>(icon->h * scale));
+    const cRectangle iconRect(
+        x + (width - iconWidth) / 2,
+        y + (height - iconHeight) / 2,
+        iconWidth,
+        iconHeight
+    );
+    renderDrawer->renderStrechFullSprite(
+        icon,
+        iconRect,
+        list->isAvailable() ? 255 : 96
+    );
     if (!list->isAvailable()) {
-        renderDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
+        renderDrawer->renderRectFillColor(
+            iconRect,
+            Color{20, 22, 23, 255},
+            138
+        );
     }
-
+    renderDrawer->renderRectColor(
+        x,
+        y,
+        width,
+        height,
+        pressed ? active : border
+    );
     if (pressed) {
+        renderDrawer->renderRectFillColor(
+            x + 2,
+            y + height - 3,
+            width - 4,
+            2,
+            active
+        );
         list->stopFlashing();
-
-        Color color = m_player->getHouseFadingColor();
-
-        renderDrawer->renderRectColor(x, y, width, height, color);
-        renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
     }
-    else {
-        if (list->isFlashing()) {
-            Color color = list->getFlashingColor();
-
-            renderDrawer->renderRectColor(x, y, width, height, color);
-            renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
-            renderDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
-        }
+    else if (list->isFlashing()) {
+        renderDrawer->renderRectColor(
+            x + 1,
+            y + 1,
+            width - 2,
+            height - 2,
+            list->getFlashingColor()
+        );
     }
 }
 
-
 int cBuildingListDrawer::getDrawX()
 {
-    return (game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar) + 2;
+    return getLayout().cards.getX();
 }
 
 int cBuildingListDrawer::getDrawY()
 {
-    return cSideBar::TopBarHeight + 230 + 30;
+    return getLayout().cards.getY();
 }
 
 /**
@@ -126,6 +205,9 @@ int cBuildingListDrawer::getDrawY()
  */
 void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)
 {
+    const HudLayout layout = getLayout(list);
+    const int scrollRow = getScrollRow(list);
+
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
@@ -138,11 +220,18 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     std::array<int, 6> isBuildingItemInList = list->isBuildingItem();
 
     // Start drawing the 'icons grid'
-    int withOfIcon = 63;
-    int heightOfIcon = 47;
-
-    // draw the icons, in rows of 3
-    int rowNr = 0;
+    int withOfIcon = getCardWidth();
+    int heightOfIcon = getCardHeight();
+
+    renderDrawer->setClippingFor(
+        layout.cards.getX(),
+        layout.cards.getY(),
+        layout.cards.getEndX(),
+        layout.cards.getEndY()
+    );
+
+    // Draw the visible icon rows. HD positions come from HudLayout so drawing
+    // and hit testing cannot drift apart.
     for (int i = 0; i < end; i++) {
         cBuildingListItem *item = list->getItem(i);
 
@@ -150,6 +239,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             continue; // allow gaps in the list data structure (just not with rendering)
         }
 
+        const cRectangle card = layout.cardRect(i, scrollRow);
+        if (card.getEndY() <= layout.cards.getY() ||
+            card.getY() >= layout.cards.getEndY()) {
+            continue;
+        }
+        iDrawX = card.getX();
+        iDrawY = card.getY();
+
         int iDrawXEnd = iDrawX + withOfIcon;
         int iDrawYEnd = iDrawY + heightOfIcon;
 
@@ -159,7 +256,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         // icon id must be set , assert it.
         assert(item->getIconId() > -1);
 
-        renderDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
+        drawHdCard(item, iDrawX, iDrawY);
 
         if (shouldDrawStructureSize) {
             drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
@@ -170,27 +267,52 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             int iFrame = item->getBuildProgressFrame();
 
             if (!item->isDoneBuilding() || iFrame < 31) {
-                // draw the other progress stuff
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+                const int progressWidth = std::clamp(
+                    (withOfIcon - 4) * iFrame / 31,
+                    0,
+                    withOfIcon - 4
+                );
+                const int progressY = iDrawY + heightOfIcon - 36;
+                renderDrawer->renderRectFillColor(
+                    iDrawX + 2,
+                    progressY,
+                    withOfIcon - 4,
+                    4,
+                    15,
+                    18,
+                    20,
+                    230
+                );
+                renderDrawer->renderRectFillColor(
+                    iDrawX + 2,
+                    progressY,
+                    progressWidth,
+                    4,
+                    selectFadingColor
+                );
             }
             else {
                 if (item->shouldPlaceIt()) {
-                    // TODO: draw white/red (flicker)
-                    int icon = READY01;
-                    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) {
-                        icon = READY02;
-                    }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    const Color readyColor = m_player->isContextMouseState(
+                        eMouseState::MOUSESTATE_PLACE
+                    ) ? Color{225, 48, 42, 255} : Color::white();
+                    m_smallTextDrawer->drawTextScaledCenteredInBox(
+                        m_readyLabel,
+                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
+                        1.0F,
+                        readyColor
+                    );
                 }
                 else if (item->shouldDeployIt()) {
-                    // TODO: draw white/red (flicker)
-                    // TODO: draw DEPLOY
-                    int icon = READY01;
-                    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) {
-                        icon = READY02;
-                    }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    const Color readyColor = m_player->isContextMouseState(
+                        eMouseState::MOUSESTATE_DEPLOY
+                    ) ? Color{225, 48, 42, 255} : Color::white();
+                    m_smallTextDrawer->drawTextScaledCenteredInBox(
+                        m_readyLabel,
+                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
+                        1.0F,
+                        readyColor
+                    );
                 }
             }
         }
@@ -213,7 +335,16 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             }
 
             if (!item->isAvailable() || isBuildingSameSubListItem) {
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                renderDrawer->renderRectFillColor(
+                    iDrawX,
+                    iDrawY,
+                    withOfIcon,
+                    heightOfIcon - 32,
+                    0,
+                    0,
+                    0,
+                    128
+                );
 
                 // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
                 if (item->isPendingUpgrading()) {
@@ -223,7 +354,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
                     Color red = Color{255, 0, 0,255};
-                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
+                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
                 }
 
                 // Pending building (ie: a build is progressing, blocking the upgrade)
@@ -234,10 +365,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
                     Color red = Color{255, 0, 0, 255};
-                    int height = heightOfIcon / 3;
-                    m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, red);
+                    m_smallTextDrawer->drawTextCenteredInBox(
+                        localization::text("OCCUPIED", "ЗАНЯТО"),
+                        iDrawX,
+                        iDrawY,
+                        withOfIcon,
+                        heightOfIcon,
+                        red
+                    );
                 }
             }
 
@@ -245,7 +380,16 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 // only for starport show you can't pay it, as we allow building units when you cannot pay it (ie partial
                 // payment/progress)
                 if (cannotPayIt) {
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                    renderDrawer->renderRectFillColor(
+                        iDrawX,
+                        iDrawY,
+                        withOfIcon,
+                        heightOfIcon - 32,
+                        0,
+                        0,
+                        0,
+                        128
+                    );
                     Color errorFadingColor = m_player->getErrorFadingColor();
                     renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
                     renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
@@ -273,13 +417,24 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 
         if (showAmount) {
             // draw number of times to build this thing (queueing)
-            int textX = iDrawX + 41;
-            int textY = iDrawY + 16;
+            int textX = iDrawX + withOfIcon - 20;
+            int textY = iDrawY + heightOfIcon - 51;
 
             if (amountToShow < 10) {
-                textX += 10;
+                textX += 6;
             }
 
+            renderDrawer->renderRectFillColor(
+                textX - 3,
+                textY - 1,
+                withOfIcon - (textX - iDrawX) - 1,
+                16,
+                8,
+                10,
+                12,
+                220
+            );
+
             // draw
             m_gameTextDrawer->drawText(textX, textY, std::format("{}",amountToShow));
         }
@@ -306,18 +461,10 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
             }
         }
-
-        // update coordinates, 3 icons in a row
-        if (rowNr < 2) {
-            iDrawX+=66;
-            rowNr++;
-        }
-        else {
-            rowNr = 0;
-            iDrawX=getDrawX();
-            iDrawY+=50;
-        }
     }
+
+    renderDrawer->resetClippingFor();
+    drawHdScrollbar(list, layout);
 }
 
 /**
@@ -347,14 +494,19 @@ void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
         iTile = GRID_3X3;
     }
 
-    renderDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
+    const int gridX = x + getCardWidth() - 22;
+    const int gridY = y + 3;
+    renderDrawer->renderRectFillColor(gridX, gridY,19,19,8,10,12,220);
+    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), gridX, gridY);
+    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), gridX, gridY);
 }
 
 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
 {
-    if (x >= drawX && x <= (drawX + 64) && y >= drawY && y < (drawY + 48)) {
+    if (x >= drawX &&
+        x <= drawX + getCardWidth() &&
+        y >= drawY &&
+        y < drawY + getCardHeight()) {
         return true;
     }
     return false;
@@ -363,33 +515,204 @@ bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX,
 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
 {
     assert(list != nullptr);
-    // starting draw coordinates
-    int iDrawX=getDrawX();
-    int iDrawY=getDrawY();
-
-    int end = MAX_ITEMS;
 
-    int rowNr = 0;
-    for (int i = 0; i < end; i++) {
+    const HudLayout layout = getLayout(list);
+    if (!layout.cards.isPointWithin(x, y)) {
+        return nullptr;
+    }
+    const int scrollRow = getScrollRow(list);
+    for (int i = 0; i < list->getItemCount(); ++i) {
         cBuildingListItem *item = list->getItem(i);
-        if (item == nullptr) break;
-
-        if (isOverItemCoordinates_Boolean(x, y, iDrawX, iDrawY)) {
+        if (item == nullptr) {
+            continue;
+        }
+        const cRectangle card = layout.cardRect(i, scrollRow);
+        if (card.getY() < layout.cards.getY() ||
+            card.getEndY() > layout.cards.getEndY()) {
+            continue;
+        }
+        if (card.isPointWithin(x, y)) {
             return item;
         }
+    }
+    return nullptr;
+}
+
+int cBuildingListDrawer::getCardWidth() const
+{
+    return getLayout().cardWidth;
+}
 
-        if (rowNr < 2) {
-            rowNr++;
-            iDrawX+=66;
+int cBuildingListDrawer::getCardHeight() const
+{
+    return getLayout().cardHeight;
+}
+
+void cBuildingListDrawer::drawHdCard(
+    cBuildingListItem *item,
+    int x,
+    int y)
+{
+    const int cardWidth = getCardWidth();
+    const int cardHeight = getCardHeight();
+    const int labelHeight = 32;
+    const int imageHeight = cardHeight - labelHeight;
+    const Color panelColor{18, 22, 25, 255};
+    const Color borderColor{142, 111, 51, 255};
+    const Color innerBorder{56, 61, 62, 255};
+    const Color labelColor{232, 225, 196, 255};
+    const Color priceColor{255, 205, 73, 255};
+
+    renderDrawer->renderRectFillColor(
+        x,
+        y,
+        cardWidth,
+        cardHeight,
+        panelColor
+    );
+
+    Texture *icon = m_gfxinter->getTexture(item->getIconId());
+    renderDrawer->renderStrechSprite(
+        icon,
+        cRectangle(0, 0, icon->w, icon->h),
+        cRectangle(x + 3, y + 3, cardWidth - 6, imageHeight - 5)
+    );
+
+    renderDrawer->renderRectFillColor(
+        x + 1,
+        y + imageHeight,
+        cardWidth - 2,
+        labelHeight - 1,
+        panelColor
+    );
+    renderDrawer->renderRectColor(
+        x,
+        y,
+        cardWidth,
+        cardHeight,
+        borderColor
+    );
+    renderDrawer->renderRectColor(
+        x + 1,
+        y + 1,
+        cardWidth - 2,
+        cardHeight - 2,
+        innerBorder
+    );
+    renderDrawer->renderLine(
+        x + 2,
+        y + imageHeight,
+        x + cardWidth - 3,
+        y + imageHeight,
+        borderColor
+    );
+
+    const std::string name = compactCardName(item->getNameString());
+    const int textWidth = cardWidth - 6;
+    if (m_smallTextDrawer->getTextLength(name) <= textWidth) {
+        m_smallTextDrawer->drawTextCenteredInBox(
+            name,
+            x + 3,
+            y + imageHeight,
+            textWidth,
+            labelHeight,
+            labelColor
+        );
+    }
+    else {
+        std::istringstream stream(name);
+        std::vector<std::string> words;
+        std::string word;
+        while (stream >> word) {
+            words.push_back(word);
+        }
+
+        std::string firstLine;
+        std::string secondLine;
+        for (const auto &candidateWord : words) {
+            const std::string candidate = firstLine.empty()
+                ? candidateWord
+                : firstLine + " " + candidateWord;
+            if (secondLine.empty() &&
+                m_smallTextDrawer->getTextLength(candidate) <= textWidth) {
+                firstLine = candidate;
+            }
+            else {
+                secondLine += secondLine.empty()
+                    ? candidateWord
+                    : " " + candidateWord;
+            }
+        }
+
+        firstLine = fitWithEllipsis(
+            m_smallTextDrawer,
+            firstLine.empty() ? name : firstLine,
+            textWidth
+        );
+        secondLine = fitWithEllipsis(
+            m_smallTextDrawer,
+            secondLine,
+            textWidth
+        );
+
+        if (secondLine.empty()) {
+            m_smallTextDrawer->drawTextCenteredInBox(
+                firstLine,
+                x + 3,
+                y + imageHeight,
+                textWidth,
+                labelHeight,
+                labelColor
+            );
         }
         else {
-            iDrawY += 50;
-            iDrawX=getDrawX();
-            rowNr = 0;
+            const int firstLineY = y + imageHeight + 2;
+            m_smallTextDrawer->drawTextCentered(
+                firstLine,
+                x + 3,
+                textWidth,
+                firstLineY,
+                labelColor
+            );
+            m_smallTextDrawer->drawTextCentered(
+                secondLine,
+                x + 3,
+                textWidth,
+                firstLineY + m_smallTextDrawer->getFontHeight(),
+                labelColor
+            );
         }
     }
 
-    return nullptr;
+    if (item->getBuildCost() > 0) {
+        const std::string price = std::format("${}", item->getBuildCost());
+        const int priceWidth = m_smallTextDrawer->getTextLength(price);
+        const int priceX = x + 6;
+        renderDrawer->renderRectFillColor(
+            priceX - 3,
+            y + 3,
+            priceWidth + 4,
+            17,
+            8,
+            10,
+            12,
+            220
+        );
+        renderDrawer->renderRectColor(
+            priceX - 3,
+            y + 3,
+            priceWidth + 4,
+            17,
+            Color{126, 94, 35, 255}
+        );
+        m_smallTextDrawer->drawText(
+            priceX,
+            y + 4,
+            priceColor,
+            price,
+            false
+        );
+    }
 }
 
 void cBuildingListDrawer::setPlayer(cPlayer *player)
@@ -397,9 +720,147 @@ void cBuildingListDrawer::setPlayer(cPlayer *player)
     this->m_player = player;
 }
 
-void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &)
+HudLayout cBuildingListDrawer::getLayout(cBuildingList *list) const
 {
-    // NOOP
+    const bool reserveOrderArea =
+        list != nullptr &&
+        list->getType() == eListType::LIST_STARPORT;
+    return HudLayout::create(
+        game.m_screenW,
+        game.m_screenH,
+        reserveOrderArea
+    );
+}
+
+int cBuildingListDrawer::getScrollRow(cBuildingList *list) const
+{
+    if (list == nullptr) {
+        return 0;
+    }
+    const int listId = eListTypeAsInt(list->getType());
+    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
+        return 0;
+    }
+    return std::clamp(
+        m_scrollRows[listId],
+        0,
+        getLayout(list).maxScrollRow(list->getItemCount())
+    );
+}
+
+void cBuildingListDrawer::setScrollRow(cBuildingList *list, int row)
+{
+    if (list == nullptr) {
+        return;
+    }
+    const int listId = eListTypeAsInt(list->getType());
+    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
+        return;
+    }
+    m_scrollRows[listId] = std::clamp(
+        row,
+        0,
+        getLayout(list).maxScrollRow(list->getItemCount())
+    );
+}
+
+void cBuildingListDrawer::scrollSelectedList(int rowDelta)
+{
+    if (m_player == nullptr || m_player->getSideBar() == nullptr) {
+        return;
+    }
+    cSideBar *sidebar = m_player->getSideBar();
+    const int selectedId = sidebar->getSelectedListID();
+    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
+        return;
+    }
+    cBuildingList *list = sidebar->getList(selectedId);
+    setScrollRow(list, getScrollRow(list) + rowDelta);
+}
+
+void cBuildingListDrawer::drawHdScrollbar(
+    cBuildingList *list,
+    const HudLayout &layout)
+{
+    const Color track{10, 13, 15, 245};
+    const Color border{83, 69, 43, 255};
+    const Color thumb{181, 135, 44, 255};
+    renderDrawer->renderRectFillColor(
+        layout.scrollbar.getX(),
+        layout.scrollbar.getY(),
+        layout.scrollbar.getWidth(),
+        layout.scrollbar.getHeight(),
+        track
+    );
+    renderDrawer->renderRectColor(
+        layout.scrollbar.getX(),
+        layout.scrollbar.getY(),
+        layout.scrollbar.getWidth(),
+        layout.scrollbar.getHeight(),
+        border
+    );
+
+    if (layout.maxScrollRow(list->getItemCount()) <= 0) {
+        return;
+    }
+    const cRectangle thumbRect = layout.scrollbarThumb(
+        list->getItemCount(),
+        getScrollRow(list)
+    );
+    renderDrawer->renderRectFillColor(
+        thumbRect.getX() + 2,
+        thumbRect.getY() + 2,
+        thumbRect.getWidth() - 4,
+        thumbRect.getHeight() - 4,
+        thumb
+    );
+}
+
+void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
+{
+    if (m_player == nullptr ||
+        m_player->getSideBar() == nullptr) {
+        return;
+    }
+
+    cSideBar *sidebar = m_player->getSideBar();
+    const int selectedId = sidebar->getSelectedListID();
+    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
+        return;
+    }
+    cBuildingList *list = sidebar->getList(selectedId);
+    if (list == nullptr) {
+        return;
+    }
+
+    const HudLayout layout = getLayout(list);
+    if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
+        return;
+    }
+
+    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_UP) {
+        scrollSelectedList(-1);
+        return;
+    }
+    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN) {
+        scrollSelectedList(1);
+        return;
+    }
+    if (event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED ||
+        !layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) {
+        return;
+    }
+
+    const cRectangle thumb = layout.scrollbarThumb(
+        list->getItemCount(),
+        getScrollRow(list)
+    );
+    if (event.coords.y < thumb.getY()) {
+        scrollSelectedList(-layout.visibleRows());
+    }
+    else if (event.coords.y > thumb.getEndY()) {
+        scrollSelectedList(layout.visibleRows());
+    }
 }
 
 void cBuildingListDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
````

## src/drawers/cBuildingListDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cBuildingListDrawer.cpp
```

stdout (22221 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.cpp b/src/drawers/cBuildingListDrawer.cpp
index eb979610..529e15c5 100644
--- a/src/drawers/cBuildingListDrawer.cpp
+++ b/src/drawers/cBuildingListDrawer.cpp
@@ -1,23 +1,63 @@
-#include "cBuildingListDrawer.h"
+/**
+ * @file cBuildingListDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cBuildingListDrawer.h"
+#include "include/sGameServices.h"
 #include "drawers/SDLDrawer.hpp"
-#include "d2tmc.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/structures/cOrderProcesser.h"
+#include "gameobjects/players/cPlayer.h"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "controls/cMouse.h"
+#include "utils/common.h"
+#include "utils/Log.h"
 
-#include <SDL2/SDL.h>
+#include <SDL3/SDL.h>
 #include <format>
 
+#include "gameobjects/structures/cStructureFactory.h"
+#include "gameobjects/units/cUnits.h"
+#include "include/cAssert.h"
+#include "include/Texture.hpp"
+#include "context/TextContext.hpp"
+#include "drawers/cTextDrawer.h"
+#include "game/cGameSettings.h"
+#include "gameobjects/structures/cStructureInfo.h"
+
 cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
     m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
     m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_player(player),
     m_renderListIds(false)
 {
+    d2tm_assert(player != nullptr);
+    d2tm_assert(ctx != nullptr);
+}
+
+void cBuildingListDrawer::serviceInit(sGameServices* services)
+{
+    m_infos = services->info;
+    m_settings = services->settings;
+    m_mouse = services->mouse;
+    m_objects = services->objects;
 }
 
 void cBuildingListDrawer::drawList(cBuildingList *list, int listIDToDraw)
@@ -42,24 +82,24 @@ void cBuildingListDrawer::drawListWithUnitsOrAbilities(cBuildingList *list)
 
 void cBuildingListDrawer::drawButtonHoverRectangle(cBuildingList *list)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
 
     int x = list->getButtonDrawX();
     int y = list->getButtonDrawY();
     int id = list->getButtonIconIdUnpressed();
 
     int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int height = m_gfxinter->getTexture(id)->h;
 
     Color color = m_player->getSelectFadingColor();
 
-    renderDrawer->renderRectColor(x, y, width, height, color);
-    renderDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
+    m_sdlDrawer->renderRectColor(x, y, width, height, color);
+    m_sdlDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
 }
 
 void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
 
     int x = list->getButtonDrawX();
     int y = list->getButtonDrawY();
@@ -71,22 +111,22 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
     if (id < 0) {
         // this is not good
-        logbook("ERROR UNABLE TO DRAW LIST BECAUSE ID IS NOT VALID!?");
+        Logger::error(COMP_GAME, "cBuildingListDrawer::drawButton","unable to draw list because id is not valid!? id={}", id);
         return;
     }
 
 //	int width = (gfxinter->getSurface(id))->w;
     int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int height = m_gfxinter->getTexture(id)->h;
 
     // clear
-    renderDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
 
     // set blender
-    renderDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
 
     if (!list->isAvailable()) {
-        renderDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
+        m_sdlDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
     }
 
     if (pressed) {
@@ -94,16 +134,16 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
         Color color = m_player->getHouseFadingColor();
 
-        renderDrawer->renderRectColor(x, y, width, height, color);
-        renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
+        m_sdlDrawer->renderRectColor(x, y, width, height, color);
+        m_sdlDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
     }
     else {
         if (list->isFlashing()) {
             Color color = list->getFlashingColor();
 
-            renderDrawer->renderRectColor(x, y, width, height, color);
-            renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
-            renderDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
+            m_sdlDrawer->renderRectColor(x, y, width, height, color);
+            m_sdlDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
+            m_sdlDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
         }
     }
 }
@@ -111,7 +151,7 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
 int cBuildingListDrawer::getDrawX()
 {
-    return (game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar) + 2;
+    return (m_settings->getScreenW() - cSideBar::SidebarWidthWithoutCandyBar) + 2;
 }
 
 int cBuildingListDrawer::getDrawY()
@@ -121,18 +161,16 @@ int cBuildingListDrawer::getDrawY()
 
 /**
  * Draw the list, start from startId, until the max icons in the list to be drawn.
- *
- * @param startId
  */
-void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)
+void cBuildingListDrawer::drawList(cBuildingList *list, const bool shouldDrawStructureSize)
 {
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
 
-    Color selectFadingColor = m_player->getSelectFadingColor();
+    const Color selectFadingColor = m_player->getSelectFadingColor();
 
-    int end = MAX_ITEMS;
+    constexpr int end = MAX_ITEMS;
 
     // is building an item in the list?
     std::array<int, 6> isBuildingItemInList = list->isBuildingItem();
@@ -141,6 +179,9 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     int withOfIcon = 63;
     int heightOfIcon = 47;
 
+    bool structureLimitReached = list->isType(eListType::LIST_CONSTYARD) && m_objects->getStructureFactory()->isStructureLimitReached();
+    bool unitLimitReached = (list->isType(eListType::LIST_FOOT_UNITS) || list->isType(eListType::LIST_UNITS)) && m_objects->getUnits()->isUnitLimitReached();
+
     // draw the icons, in rows of 3
     int rowNr = 0;
     for (int i = 0; i < end; i++) {
@@ -153,13 +194,12 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         int iDrawXEnd = iDrawX + withOfIcon;
         int iDrawYEnd = iDrawY + heightOfIcon;
 
-        // asumes drawing for human player
         bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());
 
         // icon id must be set , assert it.
-        assert(item->getIconId() > -1);
+        d2tm_assert(item->getIconId() > -1);
 
-        renderDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
 
         if (shouldDrawStructureSize) {
             drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
@@ -171,8 +211,12 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 
             if (!item->isDoneBuilding() || iFrame < 31) {
                 // draw the other progress stuff
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+                m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
+                m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+
+                if (item->isPaused()) {
+                    m_smallTextDrawer->drawTextCenteredInBox("Paused", iDrawX, iDrawY, withOfIcon, heightOfIcon, Color::Yellow);
+                }
             }
             else {
                 if (item->shouldPlaceIt()) {
@@ -181,7 +225,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     if (m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) {
                         icon = READY02;
                     }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
                 }
                 else if (item->shouldDeployIt()) {
                     // TODO: draw white/red (flicker)
@@ -190,9 +234,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) {
                         icon = READY02;
                     }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
                 }
             }
+
+            // units being built (or queued) while no unit slot is left: they can only wait
+            if (unitLimitReached && item->isTypeUnit()) {
+                drawMaxBuilt(iDrawX, iDrawY, withOfIcon, heightOfIcon);
+            }
         }
         else {   // not building
             // this item is not being built. So we do not draw a progress indicator.
@@ -212,51 +261,59 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 }
             }
 
-            if (!item->isAvailable() || isBuildingSameSubListItem) {
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+            bool cannotBuildDueStructureLimit = structureLimitReached && !cStructureFactory::isModifyingTerrain(item->getBuildId());
+            bool cannotBuildDueUnitLimit = unitLimitReached && item->isTypeUnit();
+            bool cannotBuildDueLimit = cannotBuildDueStructureLimit || cannotBuildDueUnitLimit;
 
-                // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
-                if (item->isPendingUpgrading()) {
-                    Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+            if (!item->isAvailable() || isBuildingSameSubListItem || cannotBuildDueLimit) {
 
-                    Color red = Color{255, 0, 0,255};
-                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
-                }
+                if (!cannotBuildDueLimit) {
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                    // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
+                    if (item->isPendingUpgrading()) {
+                        Color errorFadingColor = m_player->getErrorFadingColor();
+                        m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
-                // Pending building (ie: a build is progressing, blocking the upgrade)
-                if (item->isPendingBuilding()) {
-                    Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
-
-                    Color red = Color{255, 0, 0, 255};
-                    int height = heightOfIcon / 3;
-                    m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, red);
+                        m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, Color::Red);
+                    }
+
+                    // Pending building (ie: a build is progressing, blocking the upgrade)
+                    if (item->isPendingBuilding()) {
+                        Color errorFadingColor = m_player->getErrorFadingColor();
+                        m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+
+                        int height = heightOfIcon / 3;
+                        m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, Color::Red);
+                        m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, Color::Red);
+                        m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, Color::Red);
+                    }
+                } else {
+                    drawMaxBuilt(iDrawX, iDrawY, withOfIcon, heightOfIcon);
                 }
             }
 
             if (list->getType() == eListType::LIST_STARPORT) {
                 // only for starport show you can't pay it, as we allow building units when you cannot pay it (ie partial
                 // payment/progress)
-                if (cannotPayIt) {
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                cOrderProcesser *orderProcesser = m_player->getOrderProcesser();
+                bool orderIsAwaitingFrigate = orderProcesser->isOrderPlaced() || orderProcesser->isFrigateSent();
+                if (cannotPayIt || orderIsAwaitingFrigate) {
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
                     Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+                    m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                    m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                    m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
                 }
             }
 
             // last built id
             if (list->getLastClickedId() == i) {
-                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
-                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
+                m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
+                m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
             }
         }
 
@@ -284,7 +341,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             m_gameTextDrawer->drawText(textX, textY, std::format("{}",amountToShow));
         }
 
-        if (game.isDebugMode()) {
+        if (m_settings->isDebugMode()) {
             if (m_renderListIds) {
                 int textX = iDrawX + 41;
                 int textY = iDrawY + 40;
@@ -294,16 +351,15 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         }
 
         // draw rectangle when mouse hovers over icon
-        auto m_mouse = game.getMouse();
         if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
-            renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
-            renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
+            m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
+            m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
         }
         else {
             Color color = list->getFlashingColor();
             if (item->isFlashing()) {
-                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
-                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
+                m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
+                m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
             }
         }
 
@@ -320,6 +376,22 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     }
 }
 
+/**
+ * Draws the red cross with "Max built" over an icon, when its item can not be built because a limit is reached.
+ */
+void cBuildingListDrawer::drawMaxBuilt(int x, int y, int width, int height)
+{
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), x, y, 64);
+    Color errorFadingColor = m_player->getErrorFadingColor();
+    m_sdlDrawer->renderRectColor(x, y, width, height, errorFadingColor);
+    m_sdlDrawer->renderLine(x, y, x + width, y + height, errorFadingColor);
+    m_sdlDrawer->renderLine(x, y + height, x + width, y, errorFadingColor);
+
+    int halfHeight = height / 2;
+    m_smallTextDrawer->drawTextCenteredInBox("Max", x, y, width, halfHeight, Color::Red);
+    m_smallTextDrawer->drawTextCenteredInBox("built", x, y + halfHeight, width, halfHeight, Color::Red);
+}
+
 /**
  * Draw the amount of squares a structure would take. The X and Y coordinates are the top
  * left coordinates of an icon.
@@ -331,8 +403,8 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
 {
     // figure out size
-    int iW= sStructureInfo[structureId].bmp_width / 32;
-    int iH= sStructureInfo[structureId].bmp_height / 32;
+    int iW= m_infos->getStructureInfo(structureId).bmp_width / 32;
+    int iH= m_infos->getStructureInfo(structureId).bmp_height / 32;
     int iTile = GRID_1X1;
 
     if (iW == 2 && iH == 2) {
@@ -347,9 +419,9 @@ void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
         iTile = GRID_3X3;
     }
 
-    renderDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
+    m_sdlDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
 }
 
 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
@@ -362,7 +434,7 @@ bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX,
 
 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
@@ -404,7 +476,7 @@ void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &)
 
 void cBuildingListDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 {
-    switch (event.eventType) {
+    switch (event.getType()) {
         case eKeyEventType::HOLD:
             onKeyHold(event);
             break;
````

## src/drawers/cBuildingListDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.h
```

stdout (1636 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.h b/src/drawers/cBuildingListDrawer.h
index 7a5a52cd..b4f9928d 100644
--- a/src/drawers/cBuildingListDrawer.h
+++ b/src/drawers/cBuildingListDrawer.h
@@ -3,12 +3,17 @@
 #include "cTextDrawer.h"
 #include "observers/cInputObserver.h"
 #include "sidebar/cBuildingList.h"
+#include "sidebar/HudLayout.hpp"
+
+#include <array>
+#include <string>
 
 class cPlayer;
 class GameContext;
 class Graphics;
 
 class cBuildingListDrawer : cInputObserver {
+    friend class UiAuditAccess;
 
 public:
     explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);
@@ -38,6 +43,8 @@ private:
     cPlayer *m_player;
 
     bool m_renderListIds;
+    std::array<int, cSideBar::LIST_MAX> m_scrollRows{};
+    std::string m_readyLabel;
 
     void drawStructureSize(int structureId, int x, int y);
     void drawList(cBuildingList *list, bool shouldDrawStructureSize);
@@ -45,6 +52,14 @@ private:
     void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport
 
     bool isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY);
+    [[nodiscard]] int getCardWidth() const;
+    [[nodiscard]] int getCardHeight() const;
+    void drawHdCard(cBuildingListItem *item, int x, int y);
+    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
+    [[nodiscard]] HudLayout getLayout(cBuildingList *list = nullptr) const;
+    [[nodiscard]] int getScrollRow(cBuildingList *list) const;
+    void setScrollRow(cBuildingList *list, int row);
+    void scrollSelectedList(int rowDelta);
 
     void onKeyHold(const cKeyboardEvent &event);
 
````

## src/drawers/cBuildingListDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cBuildingListDrawer.h
```

stdout (2216 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.h b/src/drawers/cBuildingListDrawer.h
index 7a5a52cd..f4458f61 100644
--- a/src/drawers/cBuildingListDrawer.h
+++ b/src/drawers/cBuildingListDrawer.h
@@ -1,18 +1,41 @@
+/**
+ * @file cBuildingListDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
-#include "cTextDrawer.h"
+class cTextDrawer;
+class cGameObjectContext;
 #include "observers/cInputObserver.h"
 #include "sidebar/cBuildingList.h"
 
 class cPlayer;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+class cInfoContext;
+class cGameSettings;
+class cMouse;
+struct sGameServices;
 
 class cBuildingListDrawer : cInputObserver {
 
 public:
     explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);
 
+    void serviceInit(sGameServices* services);
+
     void onNotifyMouseEvent(const s_MouseEvent &event) override;
     void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
 
@@ -31,15 +54,21 @@ protected:
 
 private:
     // the list to draw
-    cTextDrawer* m_gameTextDrawer;
-    cTextDrawer* m_smallTextDrawer;
-    Graphics* m_gfxinter;
+    cTextDrawer* m_gameTextDrawer = nullptr;
+    cTextDrawer* m_smallTextDrawer = nullptr;
+    Graphics* m_gfxinter = nullptr;
+    SDLDrawer* m_sdlDrawer = nullptr;
 
     cPlayer *m_player;
+    cInfoContext* m_infos = nullptr;
+    cGameSettings* m_settings = nullptr;
+    cMouse* m_mouse = nullptr;
+    cGameObjectContext *m_objects = nullptr;
 
     bool m_renderListIds;
 
     void drawStructureSize(int structureId, int x, int y);
+    void drawMaxBuilt(int x, int y, int width, int height);
     void drawList(cBuildingList *list, bool shouldDrawStructureSize);
     void drawListWithStructures(cBuildingList *list);		// used for const yard
     void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport
````

## src/drawers/cMessageDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMessageDrawer.cpp
```

stdout (5393 байт):

````text
diff --git a/src/drawers/cMessageDrawer.cpp b/src/drawers/cMessageDrawer.cpp
index da9d02fe..feb84567 100644
--- a/src/drawers/cMessageDrawer.cpp
+++ b/src/drawers/cMessageDrawer.cpp
@@ -3,11 +3,14 @@
 #include "d2tmc.h"
 #include "drawers/SDLDrawer.hpp"
 #include "sidebar/cSideBar.h"
+#include "sidebar/HudLayout.hpp"
+#include "sidebar/MusicControlsLayout.hpp"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 
 #include <SDL2/SDL.h>
+#include <algorithm>
 
 // Game Playing State and SelectYourNextConquestState have their own version
 // this class has to be abstracted in such a way so it is used in both those states, yet without the wonky init
@@ -36,11 +39,87 @@ cMessageDrawer::~cMessageDrawer()
 void cMessageDrawer::draw()
 {
     if (m_state == messages::eMessageDrawerState::COMBAT) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y);
+        const HudLayout layout = HudLayout::create(
+            game.m_screenW,
+            game.m_screenH
+        );
+        const int left = 143;
+        const int right = layout.battlefield.getEndX() - 8;
+        const int reservedMessageWidth = m_message.empty()
+            ? 0
+            : m_textDrawer->getTextLength(m_message) + 16;
+        const MusicControlsLayout music = MusicControlsLayout::create(
+            left,
+            right,
+            reservedMessageWidth
+        );
+        const int messageX = music.visible
+            ? music.panel.getEndX() + 8
+            : left;
+        const cRectangle messageRect(
+            messageX,
+            4,
+            std::max(0, right - messageX),
+            33
+        );
+        renderDrawer->renderRectFillColor(
+            messageRect.getX(),
+            messageRect.getY(),
+            messageRect.getWidth(),
+            messageRect.getHeight(),
+            Color{20, 24, 26, 255}
+        );
+        renderDrawer->renderRectColor(
+            messageRect.getX(),
+            messageRect.getY(),
+            messageRect.getWidth(),
+            messageRect.getHeight(),
+            Color{112, 87, 42, 255}
+        );
+        const int messageTextWidth = m_message.empty()
+            ? 0
+            : m_textDrawer->getTextLength(m_message);
+        const int messageContentWidth = messageRect.getWidth() - 16;
+        if (m_alpha > -1 && messageTextWidth > 0 && messageContentWidth > 0) {
+            const Color messageColor{232, 225, 196, Uint8(m_alpha)};
+            if (messageTextWidth <= messageContentWidth) {
+                m_textDrawer->drawText(
+                    messageRect.getX() + 8,
+                    messageRect.getY() + 10,
+                    messageColor,
+                    m_message,
+                    false
+                );
+            } else {
+                const float scale = static_cast<float>(messageContentWidth) /
+                    static_cast<float>(messageTextWidth);
+                if (scale >= 0.5F) {
+                    m_textDrawer->drawTextScaledOpticallyCenteredInBox(
+                        m_message,
+                        cRectangle(
+                            messageRect.getX() + 8,
+                            messageRect.getY(),
+                            messageContentWidth,
+                            messageRect.getHeight()
+                        ),
+                        scale,
+                        messageColor,
+                        false
+                    );
+                }
+            }
+        }
+        return;
     }
 
     if (m_alpha > -1) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha);
+        renderDrawer->renderFromSurface(
+            m_bmpBar,
+            m_position.x,
+            m_position.y,
+            m_alpha,
+            m_gfxinter->getDensity()
+        );
         // draw message
         m_textDrawer->drawText(m_position.x+13, m_position.y+6, Color{0, 0, 0,Uint8(m_alpha)}, m_message, false);
     }
@@ -154,19 +233,34 @@ void cMessageDrawer::createMessageBarBmp(int desiredWidth)
         SDL_FreeSurface(m_bmpBar);
     }
 
-    m_bmpBar = SDL_CreateRGBSurface(0,desiredWidth, 30,32,0,0,0,255);
+    const int density = m_gfxinter->getDensity();
+    m_bmpBar = SDL_CreateRGBSurfaceWithFormat(
+        0,
+        desiredWidth * density,
+        30 * density,
+        32,
+        SDL_PIXELFORMAT_RGBA8888
+    );
     auto color = SDL_MapRGBA(m_bmpBar->format,255,0,255,255);
     SDL_FillRect(m_bmpBar, nullptr, color);
     SDL_BlitSurface(m_gfxinter->getSurface(MESSAGE_LEFT), nullptr, m_bmpBar, nullptr);
 
-    for (int drawX = 11; drawX < m_bmpBar->w; drawX+= 55) {
+    for (
+        int drawX = 11 * density;
+        drawX < m_bmpBar->w;
+        drawX += 55 * density) {
         auto src = m_gfxinter->getSurface(MESSAGE_MIDDLE);
         auto tmp = cRectangle{drawX, 0,src->w,src->h};
         SDL_Rect destRect = tmp.toSDL();
         SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
     }
     auto src = m_gfxinter->getSurface(MESSAGE_RIGHT);
-    auto tmp = cRectangle{m_bmpBar->w - 11, 0,src->w,src->h};
+    auto tmp = cRectangle{
+        m_bmpBar->w - 11 * density,
+        0,
+        src->w,
+        src->h
+    };
     SDL_Rect destRect = tmp.toSDL();
     SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
 }
````

## src/drawers/cMessageDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMessageDrawer.cpp
```

stdout (4906 байт):

````text
diff --git a/src/drawers/cMessageDrawer.cpp b/src/drawers/cMessageDrawer.cpp
index da9d02fe..a69f8d9d 100644
--- a/src/drawers/cMessageDrawer.cpp
+++ b/src/drawers/cMessageDrawer.cpp
@@ -1,27 +1,49 @@
+/**
+ * @file cMessageDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #include "cMessageDrawer.h"
 #include "data/gfxinter.h"
-#include "d2tmc.h"
 #include "drawers/SDLDrawer.hpp"
 #include "sidebar/cSideBar.h"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "game/cGameSettings.h"
+#include "include/sGameServices.h"
 
-#include <SDL2/SDL.h>
+#include <SDL3/SDL.h>
+#include "include/cAssert.h"
+#include "context/TextContext.hpp"
 
 // Game Playing State and SelectYourNextConquestState have their own version
 // this class has to be abstracted in such a way so it is used in both those states, yet without the wonky init
 // functions
 
-cMessageDrawer::cMessageDrawer(GameContext* ctx) :
+cMessageDrawer::cMessageDrawer(GameContext* ctx, sGameServices* services) :
     m_TIMER_message(0),
     m_alpha(0),
     m_state(messages::eMessageDrawerState::COMBAT),
     m_fadeState(messages::eMessageDrawerFadingState::FADE_IN),
     m_textDrawer(ctx->getTextContext()->getGameTextDrawer()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_services(services)
 {
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(services != nullptr);
     m_bmpBar = nullptr;
     m_keepMessage = false;
     m_timeMessageIsVisible = 10;
@@ -36,11 +58,11 @@ cMessageDrawer::~cMessageDrawer()
 void cMessageDrawer::draw()
 {
     if (m_state == messages::eMessageDrawerState::COMBAT) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y);
+        m_sdlDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, 255, m_gfxinter->getDensity());
     }
 
     if (m_alpha > -1) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha);
+        m_sdlDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha, m_gfxinter->getDensity());
         // draw message
         m_textDrawer->drawText(m_position.x+13, m_position.y+6, Color{0, 0, 0,Uint8(m_alpha)}, m_message, false);
     }
@@ -94,7 +116,7 @@ void cMessageDrawer::destroy()
     m_alpha = -1;
     m_TIMER_message = 0;
     if (m_bmpBar != nullptr) {
-        SDL_FreeSurface(m_bmpBar);
+        SDL_DestroySurface(m_bmpBar);
     }
 }
 
@@ -126,7 +148,7 @@ void cMessageDrawer::initCombatPosition()
 
     int margin = 4;
     int widthOfOptionsButton = 160 + margin;
-    int desiredWidth = game.m_screenW - (cSideBar::SidebarWidth + widthOfOptionsButton);
+    int desiredWidth = m_services->settings->getScreenW() - (cSideBar::SidebarWidth + widthOfOptionsButton);
     createMessageBarBmp(desiredWidth);
     // default positions in-game (battle mode)
     m_position.x = widthOfOptionsButton;
@@ -150,23 +172,24 @@ void cMessageDrawer::setMessage(const std::string &msg, bool keepMessage)
 
 void cMessageDrawer::createMessageBarBmp(int desiredWidth)
 {
+    const int density = m_gfxinter->getDensity();
     if (m_bmpBar) {
-        SDL_FreeSurface(m_bmpBar);
+        SDL_DestroySurface(m_bmpBar);
     }
 
-    m_bmpBar = SDL_CreateRGBSurface(0,desiredWidth, 30,32,0,0,0,255);
-    auto color = SDL_MapRGBA(m_bmpBar->format,255,0,255,255);
-    SDL_FillRect(m_bmpBar, nullptr, color);
+    m_bmpBar = SDL_CreateSurface(desiredWidth * density, 30 * density, SDL_PIXELFORMAT_RGBA32);
+    auto color = SDL_MapRGBA(SDL_GetPixelFormatDetails(m_bmpBar->format), SDL_GetSurfacePalette(m_bmpBar), 255, 0, 255, 255);
+    SDL_FillSurfaceRect(m_bmpBar, nullptr, color);
     SDL_BlitSurface(m_gfxinter->getSurface(MESSAGE_LEFT), nullptr, m_bmpBar, nullptr);
 
-    for (int drawX = 11; drawX < m_bmpBar->w; drawX+= 55) {
+    for (int drawX = 11 * density; drawX < m_bmpBar->w; drawX += 55 * density) {
         auto src = m_gfxinter->getSurface(MESSAGE_MIDDLE);
         auto tmp = cRectangle{drawX, 0,src->w,src->h};
         SDL_Rect destRect = tmp.toSDL();
         SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
     }
     auto src = m_gfxinter->getSurface(MESSAGE_RIGHT);
-    auto tmp = cRectangle{m_bmpBar->w - 11, 0,src->w,src->h};
+    auto tmp = cRectangle{m_bmpBar->w - 11 * density, 0,src->w,src->h};
     SDL_Rect destRect = tmp.toSDL();
     SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
 }
````

## src/drawers/cMessageDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMessageDrawer.h
```

stdout (436 байт):

````text
diff --git a/src/drawers/cMessageDrawer.h b/src/drawers/cMessageDrawer.h
index fb9584c1..1bfc420a 100644
--- a/src/drawers/cMessageDrawer.h
+++ b/src/drawers/cMessageDrawer.h
@@ -39,7 +39,7 @@ public:
     void initCombatPosition();
 
     void setMessage(const std::string &msg, bool keepMessage = false);
-    std::string getMessage() {
+    std::string getMessage() const {
         return m_message;
     }
     bool hasMessage() {
````

## src/drawers/cMessageDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMessageDrawer.h
```

stdout (1543 байт):

````text
diff --git a/src/drawers/cMessageDrawer.h b/src/drawers/cMessageDrawer.h
index fb9584c1..89edd6bb 100644
--- a/src/drawers/cMessageDrawer.h
+++ b/src/drawers/cMessageDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file cMessageDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
 #include "utils/cPoint.h"
@@ -7,6 +22,8 @@
 struct SDL_Surface;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+struct sGameServices;
 
 namespace messages {
 enum eMessageDrawerState {
@@ -22,9 +39,11 @@ enum eMessageDrawerFadingState {
 
 class cMessageDrawer {
 public:
-    explicit cMessageDrawer(GameContext* ctx);
+    explicit cMessageDrawer(GameContext* ctx, sGameServices* services);
     ~cMessageDrawer();
 
+    void serviceInit(sGameServices*) {}
+
     void draw();
 
     void thinkFast(); // timer based thinking to fade in/out message
@@ -61,8 +80,10 @@ private:
     messages::eMessageDrawerState m_state;
     messages::eMessageDrawerFadingState m_fadeState;
     cTextDrawer* m_textDrawer=nullptr;
+    SDLDrawer* m_sdlDrawer=nullptr;
     GameContext* m_ctx;
     Graphics* m_gfxinter;
+    sGameServices* m_services;
 
     void createMessageBarBmp(int desiredWidth);
 };
````

## src/drawers/cMiniMapDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMiniMapDrawer.cpp
```

stdout (4764 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.cpp b/src/drawers/cMiniMapDrawer.cpp
index 9ca08ea4..58fbb91a 100644
--- a/src/drawers/cMiniMapDrawer.cpp
+++ b/src/drawers/cMiniMapDrawer.cpp
@@ -2,6 +2,7 @@
 
 #include "drawers/SDLDrawer.hpp"
 #include "d2tmc.h"
+#include "debug/UiAudit.hpp"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
 #include "player/cPlayer.h"
@@ -10,6 +11,7 @@
 #include "utils/Graphics.hpp"
 #include <SDL2/SDL.h>
 #include "map/MapGeometry.hpp"
+#include "sidebar/HudLayout.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 #include <cassert>
@@ -24,32 +26,37 @@ cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMa
     m_mapCamera(mapCamera),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_status(eMinimapStatus::NOTAVAILABLE),
-    m_iStaticFrame(STAT14),
-    m_iTrans(0)
+    m_iStaticFrame(STAT14)
 {
     assert(map);
     assert(player);
     assert(mapCamera);
 
-    int reportX = cSideBar::WidthOfMinimap / getMapWidthInPixels();
-    int reportY = cSideBar::HeightOfMinimap / getMapHeightInPixels();
-    factorZoom = std::min(reportX, reportY);
+    const HudLayout hud = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const cRectangle minimapArea = hud.radarViewport;
 
-    int halfWidthOfMinimap = cSideBar::WidthOfMinimap / 2;
+    int reportX = minimapArea.getWidth() / getMapWidthInPixels();
+    int reportY = minimapArea.getHeight() / getMapHeightInPixels();
+    factorZoom = std::max(1, std::min(reportX, reportY));
+
+    int halfWidthOfMinimap = minimapArea.getWidth() / 2;
     int halfWidthOfMap = getMapWidthInPixels() / 2;
-    int topLeftX = game.m_screenW - cSideBar::WidthOfMinimap;
+    int topLeftX = minimapArea.getX();
     drawX = topLeftX + (halfWidthOfMinimap - factorZoom*halfWidthOfMap);
 
-    int halfHeightOfMinimap = cSideBar::HeightOfMinimap / 2;
+    int halfHeightOfMinimap = minimapArea.getHeight() / 2;
     int halfHeightOfMap = getMapHeightInPixels() / 2;
-    int topLeftY = cSideBar::TopBarHeight;
+    int topLeftY = minimapArea.getY();
     drawY = topLeftY + (halfHeightOfMinimap - factorZoom*halfHeightOfMap);
 
     centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
     centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
 
     m_RectMinimap = cRectangle(drawX, drawY, factorZoom*getMapWidthInPixels(), factorZoom * getMapHeightInPixels());
-    m_RectFullMinimap = cRectangle(topLeftX, topLeftY, cSideBar::WidthOfMinimap, cSideBar::HeightOfMinimap);
+    m_RectFullMinimap = minimapArea;
     mipMapTex = renderDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
 }
 
@@ -63,6 +70,9 @@ cMiniMapDrawer::~cMiniMapDrawer()
 
 void cMiniMapDrawer::draw()
 {
+    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
+        uiaudit::recordClick("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
+    }
     if (!m_map) {
         return;
     }
@@ -71,6 +81,9 @@ void cMiniMapDrawer::draw()
         return;
     }
 
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
+    }
     renderDrawer->renderRectFillColor(m_RectFullMinimap, Color::black());
 
     if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
@@ -84,40 +97,13 @@ void cMiniMapDrawer::draw()
     }
     renderDrawer->renderStrechFullSprite(mipMapTex, m_RectMinimap);
 
-    drawStaticFrame();
     drawViewPortRectangle();
 }
 
-void cMiniMapDrawer::drawStaticFrame()
-{
-    if (m_status == eMinimapStatus::NOTAVAILABLE) return;
-    if (m_status == eMinimapStatus::RENDERMAP) return;
-    if (m_status == eMinimapStatus::LOWPOWER) return;
-
-    if (m_status == eMinimapStatus::POWERDOWN) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
-        return;
-    }
-
-    // Draw static info
-    // < STAT01 frames are going from very transparent to opaque
-    if (m_iStaticFrame < STAT10) {
-        m_iTrans = 255 - healthBar(192, (STAT12 - m_iStaticFrame), 12);
-    } else {
-        m_iTrans = 255;
-    }
-
-    // non-stat01 frames are drawn transparent
-    if (m_iStaticFrame != STAT01) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
-    }
-}
-
 void cMiniMapDrawer::init()
 {
     m_status = eMinimapStatus::NOTAVAILABLE;
     m_iStaticFrame = STAT14;
-    m_iTrans = 0;
     m_isMouseOver = false;
 }
 
````

## src/drawers/cMiniMapDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMiniMapDrawer.cpp
```

stdout (20791 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.cpp b/src/drawers/cMiniMapDrawer.cpp
index 9ca08ea4..62d94b32 100644
--- a/src/drawers/cMiniMapDrawer.cpp
+++ b/src/drawers/cMiniMapDrawer.cpp
@@ -1,56 +1,92 @@
-#include "cMiniMapDrawer.h"
+/**
+ * @file cMiniMapDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cMiniMapDrawer.h"
+#include "include/sGameServices.h"
 #include "drawers/SDLDrawer.hpp"
-#include "d2tmc.h"
+#include "gameobjects/structures/cStructures.h"
+#include "gameobjects/units/cUnits.h"
+#include "gameobjects/map/cMapCamera.h"
+#include "game/cGameSettings.h"
+#include "controls/cMouse.h"
+#include "context/AudioContext.hpp"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
+#include "gameobjects/players/cPlayers.h"
 #include "sidebar/cSideBar.h"
 #include "utils/cSoundPlayer.h"
 #include "utils/Graphics.hpp"
-#include <SDL2/SDL.h>
-#include "map/MapGeometry.hpp"
+#include <SDL3/SDL.h>
+#include "gameobjects/map/MapGeometry.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
-#include <cassert>
-#include <iostream>
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "gameobjects/map/cMap.h"
+#include "include/cAssert.h"
+#include <algorithm>
+#include <cmath>
+//#include <iostream>
 
 #include "data/gfxaudio.h"
+#include "gameobjects/particles/cParticle.h"
+#include "utils/RNG.hpp"
 
-cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMapCamera *mapCamera) :
+cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cGameSettings *settings, cMap *map, cPlayer *player, cMapCamera *mapCamera) :
     m_isMouseOver(false),
     m_map(map),
+    m_mapGeometry(map ? map->getGeometry() : nullptr),
     m_player(player),
     m_mapCamera(mapCamera),
+    m_ctx(ctx),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_status(eMinimapStatus::NOTAVAILABLE),
     m_iStaticFrame(STAT14),
     m_iTrans(0)
 {
-    assert(map);
-    assert(player);
-    assert(mapCamera);
+    d2tm_assert(map!=nullptr);
+    d2tm_assert(m_mapGeometry != nullptr);
+    d2tm_assert(player!=nullptr);
+    d2tm_assert(mapCamera!=nullptr);
+    d2tm_assert(settings!=nullptr);
 
-    int reportX = cSideBar::WidthOfMinimap / getMapWidthInPixels();
-    int reportY = cSideBar::HeightOfMinimap / getMapHeightInPixels();
-    factorZoom = std::min(reportX, reportY);
+    float reportX = cSideBar::WidthOfMinimap*1.f / getMapWidthInPixels();
+    float reportY = cSideBar::HeightOfMinimap*1.f / getMapHeightInPixels();
+    m_factorZoom = std::min(reportX, reportY);
+    //std::cout << "Minimap zoom factor: " << m_factorZoom << std::endl;
 
     int halfWidthOfMinimap = cSideBar::WidthOfMinimap / 2;
     int halfWidthOfMap = getMapWidthInPixels() / 2;
-    int topLeftX = game.m_screenW - cSideBar::WidthOfMinimap;
-    drawX = topLeftX + (halfWidthOfMinimap - factorZoom*halfWidthOfMap);
+    int topLeftX = settings->getScreenW() - cSideBar::WidthOfMinimap;
+    m_drawX = topLeftX + (halfWidthOfMinimap - m_factorZoom*halfWidthOfMap);
 
     int halfHeightOfMinimap = cSideBar::HeightOfMinimap / 2;
     int halfHeightOfMap = getMapHeightInPixels() / 2;
     int topLeftY = cSideBar::TopBarHeight;
-    drawY = topLeftY + (halfHeightOfMinimap - factorZoom*halfHeightOfMap);
+    m_drawY = topLeftY + (halfHeightOfMinimap - m_factorZoom*halfHeightOfMap);
 
-    centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
-    centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
+    m_centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
+    m_centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
 
-    m_RectMinimap = cRectangle(drawX, drawY, factorZoom*getMapWidthInPixels(), factorZoom * getMapHeightInPixels());
+    m_RectMinimap = cRectangle(m_drawX, m_drawY, m_factorZoom*getMapWidthInPixels(), m_factorZoom * getMapHeightInPixels());
     m_RectFullMinimap = cRectangle(topLeftX, topLeftY, cSideBar::WidthOfMinimap, cSideBar::HeightOfMinimap);
-    mipMapTex = renderDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
+    //std::cout << "Minimap top left corner: (" << m_RectMinimap.getX() << ", " << m_RectMinimap.getY() << ", " << m_RectMinimap.getWidth() << ", " << m_RectMinimap.getHeight() << ")" << std::endl;
+    //std::cout << "RectFullMinimap: (" << m_RectFullMinimap.getX() << ", " << m_RectFullMinimap.getY() << ", " << m_RectFullMinimap.getWidth() << ", " << m_RectFullMinimap.getHeight() << ")" << std::endl;
+    m_mipMapTex = m_sdlDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
 }
 
 cMiniMapDrawer::~cMiniMapDrawer()
@@ -61,6 +97,14 @@ cMiniMapDrawer::~cMiniMapDrawer()
     m_status = eMinimapStatus::NOTAVAILABLE;
 }
 
+void cMiniMapDrawer::serviceInit(sGameServices* services)
+{
+    m_objects = services->objects;
+    m_infos = services->info;
+    m_mouse = services->mouse;
+    m_audioContext = services->ctx->getAudioContext();
+}
+
 void cMiniMapDrawer::draw()
 {
     if (!m_map) {
@@ -71,7 +115,7 @@ void cMiniMapDrawer::draw()
         return;
     }
 
-    renderDrawer->renderRectFillColor(m_RectFullMinimap, Color::black());
+    m_sdlDrawer->renderRectFillColor(m_RectFullMinimap, Color::Black);
 
     if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
         drawTerrain();
@@ -82,7 +126,7 @@ void cMiniMapDrawer::draw()
         cleanDrawTerrain();
         drawUnitsAndStructures(true);
     }
-    renderDrawer->renderStrechFullSprite(mipMapTex, m_RectMinimap);
+    m_sdlDrawer->renderStrechFullSprite(m_mipMapTex, m_RectMinimap);
 
     drawStaticFrame();
     drawViewPortRectangle();
@@ -95,7 +139,7 @@ void cMiniMapDrawer::drawStaticFrame()
     if (m_status == eMinimapStatus::LOWPOWER) return;
 
     if (m_status == eMinimapStatus::POWERDOWN) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
+        m_sdlDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
         return;
     }
 
@@ -109,7 +153,7 @@ void cMiniMapDrawer::drawStaticFrame()
 
     // non-stat01 frames are drawn transparent
     if (m_iStaticFrame != STAT01) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
+        m_sdlDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
     }
 }
 
@@ -126,7 +170,10 @@ void cMiniMapDrawer::think()
 {
     if (m_player->hasAtleastOneStructure(RADAR)) {
         if (m_status == eMinimapStatus::NOTAVAILABLE) {
-            m_status = eMinimapStatus::POWERUP;
+            // Route through POWERDOWN instead of jumping straight to POWERUP, so the
+            // power check below (which plays SOUND_RADAR) always gets a chance to run,
+            // even when power is already sufficient the instant the radar completes.
+            m_status = eMinimapStatus::POWERDOWN;
         }
     }
     else {
@@ -143,7 +190,7 @@ void cMiniMapDrawer::think()
             // go to state power down (not enough power)
             m_status = eMinimapStatus::POWERDOWN;
             // "Radar de-activated""
-            game.playVoice(SOUND_VOICE_04_ATR, m_player->getId());
+            m_audioContext->playVoice(SOUND_VOICE_04_ATR, m_player->getHouse());
         }
     }
 
@@ -152,9 +199,9 @@ void cMiniMapDrawer::think()
         if (hasRadarAndEnoughPower) {
             // go to state power up (enough power)
             m_status = eMinimapStatus::POWERUP;
-            game.playSound(SOUND_RADAR);
+            m_audioContext->playSound(SOUND_RADAR);
             // "Radar activated"
-            game.playVoice(SOUND_VOICE_03_ATR, m_player->getId());
+            m_audioContext->playVoice(SOUND_VOICE_03_ATR, m_player->getHouse());
         }
     }
 
@@ -196,27 +243,31 @@ void cMiniMapDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
             onMouseAt(event);
             return;
         case eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED:
-            onMousePressedLeft(event); // click has same behavior as 'press'
-            return;
+            onMouseClickedLeft(event);
+            break;
         case eMouseEventType::MOUSE_LEFT_BUTTON_PRESSED:
             onMousePressedLeft(event);
-            return;
+            break;
+        case eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED:
+            onMousePressedRight(event);
+            break;
         default:
             return;
     }
 
+    updateMouseCursor();
 }
 
 void cMiniMapDrawer::drawTerrain()
 {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
     Color iColor = Color{0, 0, 0,255};
 
-    for (int x = 0; x < (m_map->getWidth()); x++) {
-        for (int y = 0; y < (m_map->getHeight()); y++) {
+    for (int x = 0; x < m_mapGeometry->getWidth(); x++) {
+        for (int y = 0; y < m_mapGeometry->getHeight(); y++) {
             iColor = Color{0, 0, 0,255};
             //@mira where is map ?
-            int iCll = m_map->getGeometry().makeCell(x, y);
+            int iCll = m_mapGeometry->makeCell(x, y);
 
             if (m_map->isVisible(iCll, m_player->getId())) {
                 iColor = getRGBColorForTerrainType(m_map->getCellType(iCll));
@@ -224,14 +275,14 @@ void cMiniMapDrawer::drawTerrain()
 
             // TODO: make flexible map borders
             // do not show the helper border
-            if (!m_map->isWithinBoundaries(x, y)) {
+            if (!m_mapGeometry->isWithinBoundaries(x, y)) {
                 iColor = Color{0, 0, 0,255};
             }
 
-            renderDrawer->renderDot(x, y, iColor, 1);
+            m_sdlDrawer->renderDot(x, y, iColor, 1);
         }
     }
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 void cMiniMapDrawer::drawViewPortRectangle()
@@ -242,13 +293,16 @@ void cMiniMapDrawer::drawViewPortRectangle()
     iWidth--;
     iHeight--;
 
-    int pixelSize = factorZoom;
+    const float pixelSize = std::max(m_factorZoom, 0.001f);
+
+    const float startXf = m_drawX + ((m_mapCamera->getViewportStartX() / TILESIZE_WIDTH_PIXELS) * pixelSize);
+    const float startYf = m_drawY + ((m_mapCamera->getViewportStartY() / TILESIZE_HEIGHT_PIXELS) * pixelSize);
 
-    int startX = drawX + ((m_mapCamera->getViewportStartX() / TILESIZE_WIDTH_PIXELS) * pixelSize);
-    int startY = drawY + ((m_mapCamera->getViewportStartY() / TILESIZE_HEIGHT_PIXELS) * pixelSize);
+    int startX = static_cast<int>(std::floor(startXf));
+    int startY = static_cast<int>(std::floor(startYf));
 
-    int minimapWidth = iWidth * (pixelSize) + 1;
-    int minimapHeight = iHeight * (pixelSize) + 1;
+    int minimapWidth = std::max(1, static_cast<int>(std::ceil(iWidth * pixelSize + 1.0f)));
+    int minimapHeight = std::max(1, static_cast<int>(std::ceil(iHeight * pixelSize + 1.0f)));
 
     //cap the rectangle to the minimap size
     if (startX < m_RectFullMinimap.getX()) {
@@ -265,7 +319,7 @@ void cMiniMapDrawer::drawViewPortRectangle()
     if (startY + minimapHeight > m_RectFullMinimap.getEndY()) {
         minimapHeight = m_RectFullMinimap.getEndY() - startY;
     }
-    renderDrawer->renderRectColor(startX, startY, minimapWidth, minimapHeight, Color{255, 255, 255,255});
+    m_sdlDrawer->renderRectColor(startX, startY, minimapWidth, minimapHeight, Color{255, 255, 255,255});
 }
 
 /**
@@ -274,14 +328,14 @@ void cMiniMapDrawer::drawViewPortRectangle()
  * @param playerOnly (if false, draws all other players than player)
  */
 void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
-    const Color black = Color::black();
-    for (int x = 0; x < m_map->getWidth(); x++) {
-        for (int y = 0; y < m_map->getHeight(); y++) {
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
+    const Color black = Color::Black;
+    for (int x = 0; x < m_mapGeometry->getWidth(); x++) {
+        for (int y = 0; y < m_mapGeometry->getHeight(); y++) {
             // do not show the helper border
-            if (!m_map->isWithinBoundaries(x, y)) continue;
+            if (!m_mapGeometry->isWithinBoundaries(x, y)) continue;
 
-            int iCll = m_map->getGeometry().makeCell(x, y);
+            int iCll = m_mapGeometry->makeCell(x, y);
 
             if (!m_map->isVisible(iCll, m_player->getId())) {
                 // invisible cell
@@ -293,29 +347,33 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
 
             int idOfStructureAtCell = m_map->getCellIdStructuresLayer(iCll);
             if (idOfStructureAtCell > -1) {
-                int iPlr = structure[idOfStructureAtCell]->getOwner();
+                int iPlr = m_objects->getStructures()[idOfStructureAtCell]->getOwner();
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfUnitAtCell = m_map->getCellIdUnitLayer(iCll);
             if (idOfUnitAtCell > -1) {
-                int iPlr = unit[idOfUnitAtCell].iPlayer;
+                cUnit *pUnit = m_objects->getUnit(idOfUnitAtCell);
+                if (m_map->isHiddenByFogOfWar(pUnit)) continue; // hidden in the fog of war
+                int iPlr = pUnit->iPlayer;
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfAirUnitAtCell = m_map->getCellIdAirUnitLayer(iCll);
             if (idOfAirUnitAtCell > -1) {
-                int iPlr = unit[idOfAirUnitAtCell].iPlayer;
+                cUnit *pUnit = m_objects->getUnit(idOfAirUnitAtCell);
+                if (m_map->isHiddenByFogOfWar(pUnit)) continue; // hidden in the fog of war
+                int iPlr = pUnit->iPlayer;
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfWormAtCell = m_map->getCellIdWormsLayer(iCll);
@@ -323,6 +381,7 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
                 if (playerOnly) {
                     continue; // skip sandworms
                 }
+                if (m_map->isHiddenByFogOfWar(m_objects->getUnit(idOfWormAtCell))) continue;
                 iColor = m_player->getSelectFadingColor();
             }
 
@@ -330,10 +389,10 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
             if (iColor.r == black.r && iColor.g == black.g && iColor.b == black.b) {
                 continue;
             }
-            renderDrawer->renderDot(x, y, iColor, 1);
+            m_sdlDrawer->renderDot(x, y, iColor, 1);
         }
     }
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 Color cMiniMapDrawer::getRGBColorForTerrainType(int terrainType)
@@ -366,45 +425,98 @@ Color cMiniMapDrawer::getRGBColorForTerrainType(int terrainType)
 }
 
 int cMiniMapDrawer::getMapHeightInPixels() const {
-    return m_map->getHeight();
+    return m_mapGeometry->getHeight();
 }
 
 int cMiniMapDrawer::getMapWidthInPixels() const {
-    return m_map->getWidth();
+    return m_mapGeometry->getWidth();
 }
 
 void cMiniMapDrawer::onMouseAt(const s_MouseEvent &event)
 {
     m_isMouseOver = m_RectMinimap.isPointWithin(event.coords.x, event.coords.y);
+    updateMouseCursor();
 }
 
-void cMiniMapDrawer::onMousePressedLeft(const s_MouseEvent &event)
+void cMiniMapDrawer::updateMouseCursor()
 {
+    if (m_isMouseOver &&
+        m_status != NOTAVAILABLE) {
+        if (m_player->hasAnyUnitSelected()) {
+            m_mouse->setTile(MOUSE_MOVE);
+        } else {
+            m_mouse->setTile(MOUSE_NORMAL);
+        }
+    }
+}
+
+void cMiniMapDrawer::onMouseClickedLeft(const s_MouseEvent &event) {
     if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
-        !game.getMouse()->isBoxSelecting() // pressed the mouse and not boxing anything..
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
     ) {
+        // left mouse *click* will move any units if selected
+        if (m_player->hasAnyUnitSelected()) {
+            int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
+            cUnits *units = m_objects->getUnits();
+            units->move_to(mouseCellOnMinimap);
+
+            auto absPoint = m_map->getGeometry()->getAbsolutePositionFromCell(mouseCellOnMinimap);
+            cParticle::create(absPoint.x, absPoint.y, D2TM_PARTICLE_MOVE, -1, -1, m_objects, m_infos);
+
+            sSelectedUnitTypes selectedUnitTypes = m_player->getSelectedUnitTypes();
+            if (selectedUnitTypes.hasInfantry) {
+                m_audioContext->playSound(SOUND_MOVINGOUT + RNG::rnd(2));
+            }
+            if (selectedUnitTypes.hasVehicles) {
+                m_audioContext->playSound(SOUND_ACKNOWLEDGED + RNG::rnd(3));
+            }
+        }
+    }
+}
 
-        if (m_player->hasAtleastOneStructure(RADAR)) {
-            auto m_mouse = game.getMouse();
+void cMiniMapDrawer::onMousePressedLeft(const s_MouseEvent &event)
+{
+    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
+    ) {
+        // left-mouse button press only moves viewport if no units are selected
+        if (!m_player->hasAnyUnitSelected()) {
             int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
             m_mapCamera->centerAndJumpViewPortToCell(mouseCellOnMinimap);
         }
     }
 }
 
+void cMiniMapDrawer::onMousePressedRight(const s_MouseEvent &event)
+{
+    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
+    ) {
+        // right-mouse button press will always move viewport
+        int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
+        m_mapCamera->centerAndJumpViewPortToCell(mouseCellOnMinimap);
+    }
+}
+
 void cMiniMapDrawer::cleanDrawTerrain() const {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
-    renderDrawer->renderClearToColor(Color::black());
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
+    m_sdlDrawer->renderClearToColor(Color::Black);
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 int cMiniMapDrawer::getMouseCell(int mouseX, int mouseY)
 {
-    int mouseMiniMapX = mouseX - drawX;
-    int mouseMiniMapY = mouseY - drawY;
-    mouseMiniMapX /= factorZoom;
-    mouseMiniMapY /= factorZoom;
-    auto mouseMiniMapPoint = m_map->fixCoordinatesToBeWithinPlayableMap(mouseMiniMapX, mouseMiniMapY);
+    const float safeZoom = std::max(m_factorZoom, 0.001f);
+    const float mouseMiniMapXf = (mouseX - m_drawX) / safeZoom;
+    const float mouseMiniMapYf = (mouseY - m_drawY) / safeZoom;
+
+    int mouseMiniMapX = static_cast<int>(std::floor(mouseMiniMapXf));
+    int mouseMiniMapY = static_cast<int>(std::floor(mouseMiniMapYf));
+
+    auto mouseMiniMapPoint = m_mapGeometry->fixCoordinatesToBeWithinPlayableMap(mouseMiniMapX, mouseMiniMapY);
 
-    return m_map->getGeometry().getCellWithMapBorders(mouseMiniMapPoint.x, mouseMiniMapPoint.y);
+    return m_mapGeometry->getCellWithMapBorders(mouseMiniMapPoint.x, mouseMiniMapPoint.y);
 }
````

## src/drawers/cMiniMapDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMiniMapDrawer.h
```

stdout (544 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.h b/src/drawers/cMiniMapDrawer.h
index 858c9515..ceaaec57 100644
--- a/src/drawers/cMiniMapDrawer.h
+++ b/src/drawers/cMiniMapDrawer.h
@@ -34,8 +34,6 @@ public:
 
     void draw();
 
-    void drawStaticFrame();
-
     // in-between solution until we have a proper combat state object
     void init();
 
@@ -78,7 +76,6 @@ private:
     eMinimapStatus m_status;
 
     int m_iStaticFrame;
-    int m_iTrans;							// transparancy
 
     // the top left coordinates for the minimap
     int drawX, drawY;
````

## src/drawers/cMiniMapDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMiniMapDrawer.h
```

stdout (3708 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.h b/src/drawers/cMiniMapDrawer.h
index 858c9515..f4cb3ca7 100644
--- a/src/drawers/cMiniMapDrawer.h
+++ b/src/drawers/cMiniMapDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file cMiniMapDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /*
  * cMiniMapDrawer.h
  *
@@ -7,15 +22,27 @@
 
 #pragma once
 
-#include "map/cMap.h"
-#include "map/cMapCamera.h"
+// #include "gameobjects/map/cMap.h"
+// #include "gameobjects/map/cMapCamera.h"
 #include "utils/cRectangle.h"
 #include "utils/Color.hpp"
+#include "controls/sMouseEvent.h"
 
+
+class cMap;
+class MapGeometry;
+class cMapCamera;
 class cPlayer;
 class Texture;
 class GameContext;
+class cGameSettings;
 class Graphics;
+class SDLDrawer;
+class cGameObjectContext;
+class cInfoContext;
+class cMouse;
+class AudioContext;
+struct sGameServices;
 
 // the BuildingListItemState
 enum eMinimapStatus {
@@ -28,7 +55,7 @@ enum eMinimapStatus {
 
 class cMiniMapDrawer {
 public:
-    explicit cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMapCamera *mapCamera);
+    explicit cMiniMapDrawer(GameContext *ctx, cGameSettings *settings, cMap *map, cPlayer *player, cMapCamera *mapCamera);
     cMiniMapDrawer() = delete;
     ~cMiniMapDrawer();
 
@@ -47,6 +74,8 @@ public:
 
     void onNotifyMouseEvent(const s_MouseEvent &event);
 
+    void serviceInit(sGameServices* services);
+
 protected:
 
     void drawTerrain();
@@ -61,19 +90,29 @@ protected:
 private:
     void onMouseAt(const s_MouseEvent &event);
     void onMousePressedLeft(const s_MouseEvent &event);
+    void onMousePressedRight(const s_MouseEvent &event);
+    void onMouseClickedLeft(const s_MouseEvent &event);
+    void updateMouseCursor();
     void cleanDrawTerrain() const;
     int getMouseCell(int mouseX, int mouseY);
 
     bool m_isMouseOver;
 
     //@mira : where is map ? Where is this initialisation ?
-    cMap *m_map;	// the minimap drawer reads data from here
-    cPlayer *m_player;	// the player used as 'context' (ie, for drawing the rectangle / viewport on the minimap)
-    cMapCamera *m_mapCamera;
+    cMap *m_map = nullptr;	// the minimap drawer reads data from here
+    MapGeometry *m_mapGeometry = nullptr;
+    cPlayer *m_player = nullptr;	// the player used as 'context' (ie, for drawing the rectangle / viewport on the minimap)
+    cMapCamera *m_mapCamera = nullptr;
+    GameContext* m_ctx = nullptr;
+    cGameObjectContext* m_objects = nullptr;
+    cInfoContext* m_infos = nullptr;
+    cMouse* m_mouse = nullptr;
+    AudioContext* m_audioContext = nullptr;
     cRectangle m_RectMinimap; // the minimap (map) itself
     cRectangle m_RectFullMinimap; // the total space it could take
-    Texture *mipMapTex;
+    Texture *m_mipMapTex;
     Graphics *m_gfxinter;
+    SDLDrawer *m_sdlDrawer;
 
     eMinimapStatus m_status;
 
@@ -81,9 +120,9 @@ private:
     int m_iTrans;							// transparancy
 
     // the top left coordinates for the minimap
-    int drawX, drawY;
-    int centerX, centerY; // the center of the minimap
+    int m_drawX, m_drawY;
+    int m_centerX, m_centerY; // the center of the minimap
 
     // bool isBigMap;
-    int factorZoom = 1; // factor to zoom the minimap, based on the map size and the minimap size
+    float m_factorZoom = 1.f; // factor to zoom the minimap, based on the map size and the minimap size
 };
````

## src/drawers/cSideBarDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cSideBarDrawer.cpp
```

stdout (27651 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.cpp b/src/drawers/cSideBarDrawer.cpp
index 009617be..22c7fa1a 100644
--- a/src/drawers/cSideBarDrawer.cpp
+++ b/src/drawers/cSideBarDrawer.cpp
@@ -1,50 +1,56 @@
 #include "cSideBarDrawer.h"
 
 #include "d2tmc.h"
+#include "debug/UiAudit.hpp"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
 #include "drawers/cOrderDrawer.h"
 #include "managers/cDrawManager.h"
 #include "player/cPlayer.h"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
 #include <SDL2/SDL.h>
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/TextContext.hpp"
+#include "sidebar/HudLayout.hpp"
+#include "utils/HdUiTextureLoader.hpp"
 #include <algorithm>
+#include <format>
 
 cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :
     m_player(player),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_buildingListDrawer(ctx, player),
     m_sidebar(nullptr),
-    m_sidebarColor(Color{214, 149, 20,255})
+    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer())
 {
     assert(player);
 
-    candyBarBall = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex);
-    candyBarPiece = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex);
-    candyHorizonBar = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex);
-
-    candiBarRenderer = renderDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, game.m_screenH-40);
-    renderDrawer->beginDrawingToTexture(candiBarRenderer);
-    createCandyBar();
-    renderDrawer->endDrawingToTexture();
+    const int density = game.getGraphicsDensity();
+    m_houseCrests[0] = loadHdUiTexture(
+        "hud_house_atreides.png",
+        density,
+        "HD HUD Atreides crest"
+    );
+    m_houseCrests[1] = loadHdUiTexture(
+        "hud_house_harkonnen.png",
+        density,
+        "HD HUD Harkonnen crest"
+    );
+    m_houseCrests[2] = loadHdUiTexture(
+        "hud_house_ordos.png",
+        density,
+        "HD HUD Ordos crest"
+    );
 }
 
 cSideBarDrawer::~cSideBarDrawer()
 {
-    if (candyBarBall)
-        delete candyBarBall;
-    if (candyBarPiece)
-        delete candyBarPiece;
-    if (candyHorizonBar)
-        delete candyHorizonBar;
-
-    if (candiBarRenderer)
-        delete candiBarRenderer;
+    for (Texture *&crest : m_houseCrests) {
+        delete crest;
+        crest = nullptr;
+    }
 }
 
 void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
@@ -60,340 +66,345 @@ void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 // draws the sidebar on screen
 void cSideBarDrawer::draw()
 {
-    // black out sidebar
-    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, game.m_screenH, Color{0, 0, 0,255});
-
-    drawCandybar();
-
-    drawMinimap();
-    drawCapacities();
-    drawBuildingLists();
+    if (uiaudit::isEnabled()) {
+        UiAuditAccess::recordSidebarClicks(*this);
+    }
+    drawHdSidebar();
 }
 
-void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
+void cSideBarDrawer::drawHdSidebar()
 {
-    m_player = pPlayer;
-    m_buildingListDrawer.setPlayer(pPlayer);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
+    }
+    renderDrawer->renderRectFillColor(
+        layout.sidebar.getX(),
+        layout.sidebar.getY(),
+        layout.sidebar.getWidth(),
+        layout.sidebar.getHeight(),
+        Color{12, 15, 17, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        layout.sidebar.getX(),
+        cSideBar::TopBarHeight,
+        5,
+        game.m_screenH - cSideBar::TopBarHeight,
+        Color{32, 36, 38, 255}
+    );
+    renderDrawer->renderLine(
+        layout.sidebar.getX() + 5,
+        cSideBar::TopBarHeight,
+        layout.sidebar.getX() + 5,
+        game.m_screenH,
+        Color{166, 124, 44, 255}
+    );
+
+    drawHdRadarPanel();
+    drawHdCapacities();
+    drawHdBuildingLists();
 }
 
-void cSideBarDrawer::drawBuildingLists()
+Texture *cSideBarDrawer::getHouseCrest() const
 {
-    // draw the sidebar itself (the backgrounds, borders, etc)
-
-    // !??! sidebar is not set earlier...but can be re-set, so keep doing this :(
-    // This basically means the allocation goes wrong somewhere! :(
-    m_sidebar = m_player->getSideBar();
-
-    // draw the buildlist icons
-    int selectedListId = m_sidebar->getSelectedListID();
-
-    int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
-    for (int listId = startPos; listId < cSideBar::LIST_MAX; listId++) {
-        cBuildingList *list = m_sidebar->getList(listId);
-        bool isListIdSelectedList = (selectedListId == listId);
-        m_buildingListDrawer.drawButton(list, isListIdSelectedList);
+    if (m_player->isHouse(ATREIDES)) {
+        return m_houseCrests[0];
     }
-
-    // draw background of buildlist
-    Texture *backgroundSprite = m_gfxinter->getTexture(BMP_GERALD_ICONLIST_BACKGROUND);
-
-    int drawX = game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar + 1;
-
-    int startY = cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight +
-                 cSideBar::HeightOfListButton;
-
-    for (; drawX < game.m_screenW; drawX += backgroundSprite->w) {
-        for (int drawY=startY; drawY < game.m_screenH; drawY += backgroundSprite->h) {
-            renderDrawer->renderSprite(backgroundSprite, drawX, drawY);
-        }
-    }
-
-    // draw the 'lines' between the icons    // draw the buildlist itself (take scrolling into account)
-    cBuildingList *selectedList = nullptr;
-
-    int iDrawX = m_buildingListDrawer.getDrawX();
-    int iDrawY = m_buildingListDrawer.getDrawY();
-
-    Texture *horBar = m_gfxinter->getTexture(BMP_GERALD_SIDEBAR_PIECE);
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
-
-    if (selectedListId > -1) {
-        selectedList = m_sidebar->getList(selectedListId);
+    if (m_player->isHouse(HARKONNEN)) {
+        return m_houseCrests[1];
     }
-
-    int endY = game.m_screenH;
-    int rows = 6;
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        rows = 5;
-        endY = game.m_screenH - 50;
+    if (m_player->isHouse(ORDOS)) {
+        return m_houseCrests[2];
     }
+    return nullptr;
+}
 
-    for (int i = 1; i < 3; i++) {
-        int barX = (iDrawX - 1) + (i * 66);
-        Color darker = Color{89, 56, 0,255};
-        Color veryDark = Color{48, 28, 0,255};
-        renderDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
-        renderDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
-
-        // horizontal lines
-        for (int j = 1; j < rows; j++) {
-            int barY = iDrawY - 1 + (j * 50);
-            renderDrawer->renderLine( iDrawX, barY-1, game.m_screenW, barY - 1, darker);
-            renderDrawer->renderLine( iDrawX, barY, game.m_screenW, barY, veryDark);
-        }
+std::string cSideBarDrawer::getHouseDisplayName() const
+{
+    if (m_player->isHouse(ATREIDES)) {
+        return localization::text("HOUSE ATREIDES", "ДОМ АТРЕЙДЕС");
     }
-
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        renderDrawer->renderRectFillColor(iDrawX, endY, game.m_screenW-iDrawX, game.m_screenH-endY, m_sidebarColor);
-        renderDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
+    if (m_player->isHouse(HARKONNEN)) {
+        return localization::text("HOUSE HARKONNEN", "ДОМ ХАРКОННЕН");
     }
-
-    // vertical lines at the side
-    renderDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, game.m_screenH, Color{255, 211, 125,255}); // left
-    renderDrawer->renderLine( game.m_screenW - 1, iDrawY - 38, game.m_screenW - 1, endY, Color{209, 150, 28,255}); // right
-
-    // END drawing icons grid
-
-    if (selectedList) {
-        m_buildingListDrawer.drawList(selectedList, selectedListId);
+    if (m_player->isHouse(ORDOS)) {
+        return localization::text("HOUSE ORDOS", "ДОМ ОРДОС");
     }
+    return localization::text("UNKNOWN HOUSE", "НЕИЗВЕСТНЫЙ ДОМ");
+}
 
-    // button interaction
-    for (int i = startPos; i < cSideBar::LIST_MAX; i++) {
-        if (i == selectedListId) continue; // skip selected list for button interaction
-        cBuildingList *list = m_sidebar->getList(i);
-
-        if (list->isAvailable() == false) continue; // not available, so no interaction possible
-
-        // render hover over border
-        auto m_mouse = game.getMouse();
-        if (list->isOverButton(m_mouse->getX(), m_mouse->getX())) {
-            m_buildingListDrawer.drawButtonHoverRectangle(list);
-        }
+void cSideBarDrawer::drawHdRadarPanel()
+{
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const Color panel{16, 20, 22, 255};
+    const Color panelInner{7, 10, 11, 255};
+    const Color brass{151, 113, 43, 255};
+    const Color text{235, 225, 191, 255};
+    const Color accent = m_player->getSelectFadingColor();
+
+    renderDrawer->renderRectFillColor(
+        layout.radarPanel.getX(),
+        layout.radarPanel.getY(),
+        layout.radarPanel.getWidth(),
+        layout.radarPanel.getHeight(),
+        panel
+    );
+    renderDrawer->renderRectColor(
+        layout.radarPanel.getX(),
+        layout.radarPanel.getY(),
+        layout.radarPanel.getWidth(),
+        layout.radarPanel.getHeight(),
+        brass
+    );
+    renderDrawer->renderRectFillColor(
+        layout.houseHeader.getX(),
+        layout.houseHeader.getY(),
+        layout.houseHeader.getWidth(),
+        layout.houseHeader.getHeight(),
+        Color{25, 29, 30, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        layout.houseHeader.getX(),
+        layout.houseHeader.getEndY() - 2,
+        layout.houseHeader.getWidth(),
+        2,
+        accent
+    );
+
+    Texture *crest = getHouseCrest();
+    const int headerCrestSize = 24;
+    if (crest != nullptr) {
+        renderDrawer->renderStrechFullSprite(
+            crest,
+            cRectangle(
+                layout.houseHeader.getX() + 3,
+                layout.houseHeader.getY() + 2,
+                headerCrestSize,
+                headerCrestSize
+            )
+        );
     }
-
-    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();
-
-    // allow clicking on the order button
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        orderDrawer->drawOrderButton(m_player);
+    m_smallTextDrawer->drawText(
+        layout.houseHeader.getX() + headerCrestSize + 10,
+        layout.houseHeader.getY() + 7,
+        text,
+        getHouseDisplayName(),
+        false
+    );
+
+    renderDrawer->renderRectFillColor(
+        layout.radarViewport.getX(),
+        layout.radarViewport.getY(),
+        layout.radarViewport.getWidth(),
+        layout.radarViewport.getHeight(),
+        panelInner
+    );
+    renderDrawer->renderRectColor(
+        layout.radarViewport.getX(),
+        layout.radarViewport.getY(),
+        layout.radarViewport.getWidth(),
+        layout.radarViewport.getHeight(),
+        Color{62, 68, 67, 255}
+    );
+
+    if (!m_player->hasRadarAndEnoughPower() && crest != nullptr) {
+        const int crestSize = std::min(
+            96,
+            layout.radarViewport.getHeight() - 18
+        );
+        renderDrawer->renderStrechFullSprite(
+            crest,
+            cRectangle(
+                layout.radarViewport.getX() +
+                    (layout.radarViewport.getWidth() - crestSize) / 2,
+                layout.radarViewport.getY() +
+                    (layout.radarViewport.getHeight() - crestSize) / 2,
+                crestSize,
+                crestSize
+            ),
+            210
+        );
     }
 }
 
-void cSideBarDrawer::drawCapacities()
+void cSideBarDrawer::drawHdMeter(
+    const cRectangle &rect,
+    const std::string &label,
+    int value,
+    int maximum,
+    Color fill,
+    bool warning) const
 {
-    drawPowerUsage();
-    drawCreditsUsage();
+    const int safeMaximum = std::max(1, maximum);
+    const float ratio = std::clamp(
+        static_cast<float>(value) / static_cast<float>(safeMaximum),
+        0.0f,
+        1.0f
+    );
+    const Color border{104, 82, 43, 255};
+    const Color text{225, 218, 190, 255};
+    const Color warningColor = warning
+        ? m_player->getErrorFadingColor()
+        : fill;
+
+    renderDrawer->renderRectFillColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        Color{10, 13, 15, 255}
+    );
+    renderDrawer->renderRectColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        border
+    );
+    m_smallTextDrawer->drawText(
+        rect.getX() + 4,
+        rect.getY() + 2,
+        text,
+        label,
+        false
+    );
+    const std::string amount = std::format("{}/{}", value, maximum);
+    const int amountWidth = m_smallTextDrawer->getTextLength(amount);
+    m_smallTextDrawer->drawText(
+        rect.getEndX() - amountWidth - 4,
+        rect.getY() + 2,
+        text,
+        amount,
+        false
+    );
+
+    const int barX = rect.getX() + 4;
+    const int barY = rect.getEndY() - 7;
+    const int barWidth = rect.getWidth() - 8;
+    renderDrawer->renderRectFillColor(
+        barX,
+        barY,
+        barWidth,
+        4,
+        Color{31, 35, 36, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        barX,
+        barY,
+        static_cast<int>(barWidth * ratio),
+        4,
+        warningColor
+    );
 }
 
-void cSideBarDrawer::drawCandybar()
+void cSideBarDrawer::drawHdCapacities()
 {
-    renderDrawer->renderSprite(candiBarRenderer,game.m_screenW - cSideBar::SidebarWidth,40);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const int produced = std::max(0, m_player->getPowerProduced());
+    const int used = std::max(0, m_player->getPowerUsage());
+    drawHdMeter(
+        layout.powerMeter,
+        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
+        used,
+        produced,
+        Color{72, 202, 103, 255},
+        !m_player->bEnoughPower()
+    );
+
+    drawHdMeter(
+        layout.spiceMeter,
+        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
+        std::max(0, m_player->getCredits()),
+        std::max(1, static_cast<int>(m_player->getMaxCredits())),
+        Color{218, 139, 47, 255},
+        !m_player->bEnoughSpiceCapacityToStoreCredits()
+    );
 }
 
-void cSideBarDrawer::drawMinimap()
+void cSideBarDrawer::drawHdBuildingLists()
 {
-    Texture *sprite = candyHorizonBar;
-    int drawX = (game.m_screenW - sprite->w) + 1;
-    // 128 pixels (each pixel is a cell) + 8 margin
-    int heightMinimap = cSideBar::HeightOfMinimap;
-    int drawY = cSideBar::TopBarHeight + heightMinimap;
-    renderDrawer->renderSprite(sprite, drawX, drawY);
-
-    // 11, 10
-    // 78, 60
-    // ------
-    // 67, 50 (width/height)
-
-    bool hasRadarAndEnoughPower = m_player->hasRadarAndEnoughPower();
-
-    if (hasRadarAndEnoughPower) {
-        return; // bail, because we render the minimap
+    m_sidebar = m_player->getSideBar();
+    const int selectedListId = m_sidebar->getSelectedListID();
+    cBuildingList *selectedList = nullptr;
+    if (selectedListId >= 0 && selectedListId < cSideBar::LIST_MAX) {
+        selectedList = m_sidebar->getList(selectedListId);
     }
 
-    // else, we render the house emblem
-    renderDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,game.m_screenW-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
-                                      m_player->getEmblemBackgroundColor());
-
-    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS)) {
-        int bitmapId = BMP_SELECT_HOUSE_ATREIDES;
-
-        int srcX = 11;
-        int srcY = 10;
-
-        // draw house emblem, which is the same as the 'select house x' picture, but partially
-        int emblemWidth = 68;
-        int emblemHeight = 50;
-
-        if (m_player->isHouse(HARKONNEN)) {
-            bitmapId = BMP_SELECT_HOUSE_HARKONNEN;
-        }
-
-        if (m_player->isHouse(ORDOS)) {
-            bitmapId = BMP_SELECT_HOUSE_ORDOS;
-            emblemHeight = 49;
-            srcY = 11;
-        }
-
-        int emblemDesiredWidth = (emblemWidth * 2);
-        int emblemDesiredHeight = (emblemHeight * 2);
-
-        drawX += (sprite->w / 2) - (emblemDesiredWidth / 2);
-        drawY = cSideBar::TopBarHeight + ((heightMinimap / 2) - (emblemDesiredHeight / 2));
-
-        cRectangle src = {srcX, srcY, emblemWidth,emblemHeight};
-        cRectangle dest = {drawX, drawY, emblemDesiredWidth, emblemDesiredHeight};
-        renderDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH,
+        selectedList != nullptr &&
+            selectedList->getType() == eListType::LIST_STARPORT
+    );
+
+    renderDrawer->renderRectFillColor(
+        layout.tabs.getX(),
+        layout.tabs.getY(),
+        layout.tabs.getWidth(),
+        layout.tabs.getHeight(),
+        Color{13, 16, 18, 255}
+    );
+
+    const int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
+    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
+        cBuildingList *list = m_sidebar->getList(listId);
+        m_buildingListDrawer.drawButton(
+            list,
+            selectedListId == listId
+        );
     }
-}
 
-void cSideBarDrawer::createCandyBar()
-{
-    int heightInPixels = (game.m_screenH - cSideBar::TopBarHeight);
-    // ball first
-    renderDrawer->renderSprite(candyBarBall, 0,0); // height of ball = 25
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
-    // now draw pieces untill the end (height of piece is 23 pixels)
-    int startY = 26 + 10; // end of ball (26) + height of top m_candybar (=10) , makes 36
-    int heightMinimap = cSideBar::HeightOfMinimap;
-    // auto tmp = cRectangle{0,0,24, heightMinimap - (6 + 1)};  // (add 1 pixel for room between ball and bar)
-    for (int y = startY; y < (heightMinimap); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("build-list", layout.catalog.getX(), layout.catalog.getY(), layout.catalog.getWidth(), layout.catalog.getHeight());
     }
-    // note: no need to take top bar into account because 'm_candybar' is a separate bitmap so coords start at 0,0
-    // ball is 6 pixels higher than horizontal m_candybar
-    int ballY = (heightMinimap) - 6;
-
-    // draw bottom m_candybar
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
-
-    // draw ball
-    renderDrawer->renderSprite(candyBarBall, 0, ballY); // height of ball = 25
-
-    // draw top m_candybar again
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
-
-    startY = ballY + 26 + 10;
-    for (int y = startY; y < (heightInPixels + 23); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+    renderDrawer->renderRectFillColor(
+        layout.catalog.getX(),
+        layout.catalog.getY(),
+        layout.catalog.getWidth(),
+        layout.catalog.getHeight(),
+        Color{12, 15, 17, 255}
+    );
+    renderDrawer->renderRectColor(
+        layout.catalog.getX(),
+        layout.catalog.getY(),
+        layout.catalog.getWidth(),
+        layout.catalog.getHeight(),
+        Color{93, 75, 40, 255}
+    );
+
+    if (selectedList != nullptr) {
+        m_buildingListDrawer.drawList(selectedList, selectedListId);
     }
-    // draw bottom
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
-}
-
-void cSideBarDrawer::drawPowerUsage() const
-{
-    int arbitraryMargin = 6;
-    int barTotalHeight = game.m_screenH - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
-    int barY = cSideBar::TotalHeightBeforePowerBarStarts + arbitraryMargin;
-    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
-    //cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::black()); //renderDrawer->getColor_BLACK());
-
-    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxPowerOutageOfWindtrap = sStructureInfo[WINDTRAP].power_give;
-    float totalPowerOutput = (1 + (m_player->getAmountOfStructuresForType(WINDTRAP))) * maxPowerOutageOfWindtrap;
-    float powerIn = (float)m_player->getPowerProduced() / totalPowerOutput;
-    float powerUse = (float)m_player->getPowerUsage() / totalPowerOutput;
-
-    float barHeightToDraw = barTotalHeight * powerIn;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerInY = barY + (barTotalHeight - barHeightToDraw);
-
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
-
-    barHeightToDraw = barTotalHeight * powerUse;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerOutY = barY + (barTotalHeight - barHeightToDraw);
-
-    float powerUsageRatio = ((float)m_player->getPowerUsage() + 1) / ((float)m_player->getPowerProduced() + 1);
-    int r = powerUsageRatio * 255;
-    int g = (1.1 - powerUsageRatio) * 255;
-
-    if (r > 255) r = 255;
-    if (g > 255) g = 255;
 
-    if (m_player->bEnoughPower()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{(Uint8)r, (Uint8)g, 32,255});
-    }
-    else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
+    auto mouse = game.getMouse();
+    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
+        if (listId == selectedListId) {
+            continue;
+        }
+        cBuildingList *list = m_sidebar->getList(listId);
+        if (list->isAvailable() &&
+            list->isOverButton(mouse->getX(), mouse->getY())) {
+            m_buildingListDrawer.drawButtonHoverRectangle(list);
+        }
     }
 
-    renderDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
-
-    renderDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
-
-    // draw darker 'sides' at the left and top
-    Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
-    if (m_player->bEnoughPower()) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
-    }
-    else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
+    if (selectedList != nullptr &&
+        selectedList->getType() == eListType::LIST_STARPORT) {
+        drawManager->getOrderDrawer()->drawOrderButton(m_player);
     }
 }
 
-void cSideBarDrawer::drawCreditsUsage()
+void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
 {
-    int barTotalHeight = (cSideBar::HeightOfMinimap - 76);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
-    int barY = cSideBar::TopBarHeight + 48;
-    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
-    // cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
-
-    // STEFAN: 01/05/2021 -> looks like a lot of this code can be moved to the player class to retrieve max spice capacity
-    // and so forth.
-
-    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxSpiceCapacity = 1000; // this is still hard coded, need to move to INI file
-    int structuresWithSpice = m_player->getAmountOfStructuresForType(REFINERY) + m_player->getAmountOfStructuresForType(SILO);
-    float totalSpiceCapacity = (1 + structuresWithSpice) * maxSpiceCapacity;
-    float maxSpice = m_player->getMaxCredits() / totalSpiceCapacity;
-    float spiceStored = static_cast<float>(m_player->getCredits()) / totalSpiceCapacity;
-
-    float barHeightToDraw = barTotalHeight * maxSpice;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerInY = barY + (barTotalHeight - barHeightToDraw);
-
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
-
-    barHeightToDraw = barTotalHeight * spiceStored;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerOutY = barY + (barTotalHeight - barHeightToDraw);
-
-    auto spiceCapacityRatio = static_cast<float>(m_player->getCredits() + 1) / (m_player->getMaxCredits() + 1);
-    spiceCapacityRatio = std::clamp(spiceCapacityRatio, 0.0f, 1.0f);
-    int r = spiceCapacityRatio * 255;
-    int g = (1.1 - spiceCapacityRatio) * 255;
-
-    if (r > 255) r = 255;
-    if (g > 255) g = 255;
-
-    if (m_player->bEnoughSpiceCapacityToStoreCredits()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, (Uint8)r,(Uint8)g, 32,255);
-    }
-    else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
-    }
-
-    renderDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
-
-    // draw darker 'sides' at the left and top
-    Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
-
-    if (spiceCapacityRatio>0.95) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
-    } else  if (spiceCapacityRatio<0.05) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
-    } else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
-    }
+    m_player = pPlayer;
+    m_buildingListDrawer.setPlayer(pPlayer);
 }
````

## src/drawers/cSideBarDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cSideBarDrawer.cpp
```

stdout (23830 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.cpp b/src/drawers/cSideBarDrawer.cpp
index 009617be..0fd34e64 100644
--- a/src/drawers/cSideBarDrawer.cpp
+++ b/src/drawers/cSideBarDrawer.cpp
@@ -1,50 +1,70 @@
-#include "cSideBarDrawer.h"
+/**
+ * @file cSideBarDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
-#include "d2tmc.h"
+#include "cSideBarDrawer.h"
+#include "include/sGameServices.h"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
 #include "drawers/cOrderDrawer.h"
 #include "managers/cDrawManager.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
 #include "utils/Graphics.hpp"
-#include <SDL2/SDL.h>
+#include "utils/texture_utils.h"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "controls/cMouse.h"
+#include <SDL3/SDL.h>
 #include <algorithm>
+#include "include/cAssert.h"
+#include "game/cGameSettings.h"
+#include "include/Texture.hpp"
 
-cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :
+cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :
     m_player(player),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_ctx(ctx),
+    m_services(services),
     m_buildingListDrawer(ctx, player),
     m_sidebar(nullptr),
     m_sidebarColor(Color{214, 149, 20,255})
 {
-    assert(player);
-
-    candyBarBall = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex);
-    candyBarPiece = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex);
-    candyHorizonBar = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex);
+    d2tm_assert(player!= nullptr);
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(services != nullptr);
 
-    candiBarRenderer = renderDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, game.m_screenH-40);
-    renderDrawer->beginDrawingToTexture(candiBarRenderer);
-    createCandyBar();
-    renderDrawer->endDrawingToTexture();
+    m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());
+    createPlayerCandyBar();
 }
 
 cSideBarDrawer::~cSideBarDrawer()
 {
-    if (candyBarBall)
-        delete candyBarBall;
-    if (candyBarPiece)
-        delete candyBarPiece;
-    if (candyHorizonBar)
-        delete candyHorizonBar;
-
-    if (candiBarRenderer)
-        delete candiBarRenderer;
+    // smart pointers handle cleanup
+    // delete m_candyBarBall; --- IGNORE ---
+    // delete m_candyBarPiece; --- IGNORE ---
+    // delete m_candyHorizonBar; --- IGNORE ---
+    // delete m_candiBarRenderer; --- IGNORE ---
+}
+
+void cSideBarDrawer::serviceInit(sGameServices* services)
+{
+    m_infos = services->info;
+    m_mouse = services->mouse;
+    m_buildingListDrawer.serviceInit(services);
 }
 
 void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
@@ -61,7 +81,7 @@ void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 void cSideBarDrawer::draw()
 {
     // black out sidebar
-    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, game.m_screenH, Color{0, 0, 0,255});
+    m_sdlDrawer->renderRectFillColor((m_services->settings->getScreenW() - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, m_services->settings->getScreenH(), Color{0, 0, 0,255});
 
     drawCandybar();
 
@@ -72,8 +92,31 @@ void cSideBarDrawer::draw()
 
 void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
 {
+    const bool houseChanged = m_player->getHouse() != pPlayer->getHouse();
     m_player = pPlayer;
     m_buildingListDrawer.setPlayer(pPlayer);
+    if (houseChanged) {
+        createPlayerCandyBar();
+    }
+}
+
+// (re)creates the house-colored candybar textures and renders them into the candybar texture
+void cSideBarDrawer::createPlayerCandyBar()
+{
+    m_candyBarBall.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex, m_gfxinter->getDensity()));
+    m_candyBarPiece.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex, m_gfxinter->getDensity()));
+    m_candyHorizonBar.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex, m_gfxinter->getDensity()));
+
+    if (m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()) {
+        delete m_candiBarRenderer;
+        m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());
+    }
+    m_sdlDrawer->beginDrawingToTexture(m_candiBarRenderer);
+    createCandyBar();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 void cSideBarDrawer::drawBuildingLists()
@@ -97,14 +140,14 @@ void cSideBarDrawer::drawBuildingLists()
     // draw background of buildlist
     Texture *backgroundSprite = m_gfxinter->getTexture(BMP_GERALD_ICONLIST_BACKGROUND);
 
-    int drawX = game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar + 1;
+    int drawX = m_services->settings->getScreenW() - cSideBar::SidebarWidthWithoutCandyBar + 1;
 
     int startY = cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight +
                  cSideBar::HeightOfListButton;
 
-    for (; drawX < game.m_screenW; drawX += backgroundSprite->w) {
-        for (int drawY=startY; drawY < game.m_screenH; drawY += backgroundSprite->h) {
-            renderDrawer->renderSprite(backgroundSprite, drawX, drawY);
+    for (; drawX < m_services->settings->getScreenW(); drawX += backgroundSprite->w) {
+        for (int drawY=startY; drawY < m_services->settings->getScreenH(); drawY += backgroundSprite->h) {
+            m_sdlDrawer->renderSprite(backgroundSprite, drawX, drawY);
         }
     }
 
@@ -115,43 +158,43 @@ void cSideBarDrawer::drawBuildingLists()
     int iDrawY = m_buildingListDrawer.getDrawY();
 
     Texture *horBar = m_gfxinter->getTexture(BMP_GERALD_SIDEBAR_PIECE);
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
+    m_sdlDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
+    m_sdlDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
 
     if (selectedListId > -1) {
         selectedList = m_sidebar->getList(selectedListId);
     }
 
-    int endY = game.m_screenH;
+    int endY = m_services->settings->getScreenH();
     int rows = 6;
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
         rows = 5;
-        endY = game.m_screenH - 50;
+        endY = m_services->settings->getScreenH() - 50; // leave room for button "order" at bottom sidebar
     }
 
     for (int i = 1; i < 3; i++) {
         int barX = (iDrawX - 1) + (i * 66);
         Color darker = Color{89, 56, 0,255};
         Color veryDark = Color{48, 28, 0,255};
-        renderDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
-        renderDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
+        m_sdlDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
+        m_sdlDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
 
         // horizontal lines
         for (int j = 1; j < rows; j++) {
             int barY = iDrawY - 1 + (j * 50);
-            renderDrawer->renderLine( iDrawX, barY-1, game.m_screenW, barY - 1, darker);
-            renderDrawer->renderLine( iDrawX, barY, game.m_screenW, barY, veryDark);
+            m_sdlDrawer->renderLine( iDrawX, barY-1, m_services->settings->getScreenW(), barY - 1, darker);
+            m_sdlDrawer->renderLine( iDrawX, barY, m_services->settings->getScreenW(), barY, veryDark);
         }
     }
 
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        renderDrawer->renderRectFillColor(iDrawX, endY, game.m_screenW-iDrawX, game.m_screenH-endY, m_sidebarColor);
-        renderDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
+        m_sdlDrawer->renderRectFillColor(iDrawX, endY, m_services->settings->getScreenW()-iDrawX, m_services->settings->getScreenH()-endY, m_sidebarColor);
+        m_sdlDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
     }
 
     // vertical lines at the side
-    renderDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, game.m_screenH, Color{255, 211, 125,255}); // left
-    renderDrawer->renderLine( game.m_screenW - 1, iDrawY - 38, game.m_screenW - 1, endY, Color{209, 150, 28,255}); // right
+    m_sdlDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, m_services->settings->getScreenH(), Color{255, 211, 125,255}); // left
+    m_sdlDrawer->renderLine( m_services->settings->getScreenW() - 1, iDrawY - 38, m_services->settings->getScreenW() - 1, endY, Color{209, 150, 28,255}); // right
 
     // END drawing icons grid
 
@@ -167,13 +210,12 @@ void cSideBarDrawer::drawBuildingLists()
         if (list->isAvailable() == false) continue; // not available, so no interaction possible
 
         // render hover over border
-        auto m_mouse = game.getMouse();
-        if (list->isOverButton(m_mouse->getX(), m_mouse->getX())) {
+        if (list->isOverButton(m_mouse->getX(), m_mouse->getY())) {
             m_buildingListDrawer.drawButtonHoverRectangle(list);
         }
     }
 
-    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();
+    cOrderDrawer *orderDrawer = m_services->drawManager->getOrderDrawer();
 
     // allow clicking on the order button
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
@@ -189,17 +231,21 @@ void cSideBarDrawer::drawCapacities()
 
 void cSideBarDrawer::drawCandybar()
 {
-    renderDrawer->renderSprite(candiBarRenderer,game.m_screenW - cSideBar::SidebarWidth,40);
+    if (m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()) {
+        createPlayerCandyBar();
+    }
+
+    m_sdlDrawer->renderSprite(m_candiBarRenderer,m_services->settings->getScreenW() - cSideBar::SidebarWidth,40);
 }
 
 void cSideBarDrawer::drawMinimap()
 {
-    Texture *sprite = candyHorizonBar;
-    int drawX = (game.m_screenW - sprite->w) + 1;
+    Texture *sprite = m_candyHorizonBar.get();
+    int drawX = (m_services->settings->getScreenW() - sprite->w) + 1;
     // 128 pixels (each pixel is a cell) + 8 margin
     int heightMinimap = cSideBar::HeightOfMinimap;
     int drawY = cSideBar::TopBarHeight + heightMinimap;
-    renderDrawer->renderSprite(sprite, drawX, drawY);
+    m_sdlDrawer->renderSprite(sprite, drawX, drawY);
 
     // 11, 10
     // 78, 60
@@ -213,10 +259,10 @@ void cSideBarDrawer::drawMinimap()
     }
 
     // else, we render the house emblem
-    renderDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,game.m_screenW-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
+    m_sdlDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,m_services->settings->getScreenW()-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
                                       m_player->getEmblemBackgroundColor());
 
-    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS)) {
+    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS) || m_player->isHouse(SARDAUKAR)) {
         int bitmapId = BMP_SELECT_HOUSE_ATREIDES;
 
         int srcX = 11;
@@ -236,6 +282,12 @@ void cSideBarDrawer::drawMinimap()
             srcY = 11;
         }
 
+        if (m_player->isHouse(SARDAUKAR)) {
+            bitmapId = BMP_SELECT_HOUSE_SARDAUKAR;
+            //emblemHeight = 49;
+            //srcY = 11;
+        }
+
         int emblemDesiredWidth = (emblemWidth * 2);
         int emblemDesiredHeight = (emblemHeight * 2);
 
@@ -244,71 +296,71 @@ void cSideBarDrawer::drawMinimap()
 
         cRectangle src = {srcX, srcY, emblemWidth,emblemHeight};
         cRectangle dest = {drawX, drawY, emblemDesiredWidth, emblemDesiredHeight};
-        renderDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
+        m_sdlDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
     }
 }
 
 void cSideBarDrawer::createCandyBar()
 {
-    int heightInPixels = (game.m_screenH - cSideBar::TopBarHeight);
+    int heightInPixels = (m_services->settings->getScreenH() - cSideBar::TopBarHeight);
     // ball first
-    renderDrawer->renderSprite(candyBarBall, 0,0); // height of ball = 25
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
+    m_sdlDrawer->renderSprite(m_candyBarBall.get(), 0,0); // height of ball = 25
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
     // now draw pieces untill the end (height of piece is 23 pixels)
     int startY = 26 + 10; // end of ball (26) + height of top m_candybar (=10) , makes 36
     int heightMinimap = cSideBar::HeightOfMinimap;
     // auto tmp = cRectangle{0,0,24, heightMinimap - (6 + 1)};  // (add 1 pixel for room between ball and bar)
     for (int y = startY; y < (heightMinimap); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+        m_sdlDrawer->renderSprite(m_candyBarPiece.get(), 0, y);
     }
     // note: no need to take top bar into account because 'm_candybar' is a separate bitmap so coords start at 0,0
     // ball is 6 pixels higher than horizontal m_candybar
     int ballY = (heightMinimap) - 6;
 
     // draw bottom m_candybar
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
 
     // draw ball
-    renderDrawer->renderSprite(candyBarBall, 0, ballY); // height of ball = 25
+    m_sdlDrawer->renderSprite(m_candyBarBall.get(), 0, ballY); // height of ball = 25
 
     // draw top m_candybar again
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
 
     startY = ballY + 26 + 10;
     for (int y = startY; y < (heightInPixels + 23); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+        m_sdlDrawer->renderSprite(m_candyBarPiece.get(), 0, y);
     }
     // draw bottom
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
 }
 
 void cSideBarDrawer::drawPowerUsage() const
 {
     int arbitraryMargin = 6;
-    int barTotalHeight = game.m_screenH - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
+    int barTotalHeight = m_services->settings->getScreenH() - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
+    int barX = (m_services->settings->getScreenW() - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
     int barY = cSideBar::TotalHeightBeforePowerBarStarts + arbitraryMargin;
     int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
     //cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::black()); //renderDrawer->getColor_BLACK());
+    m_sdlDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::Black); //sdlDrawer->getColor_BLACK());
 
     // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxPowerOutageOfWindtrap = sStructureInfo[WINDTRAP].power_give;
+    int maxPowerOutageOfWindtrap = m_infos->getStructureInfo(WINDTRAP).power_give;
     float totalPowerOutput = (1 + (m_player->getAmountOfStructuresForType(WINDTRAP))) * maxPowerOutageOfWindtrap;
-    float powerIn = (float)m_player->getPowerProduced() / totalPowerOutput;
-    float powerUse = (float)m_player->getPowerUsage() / totalPowerOutput;
+    float powerIn = static_cast<float>(m_player->getPowerProduced()) / totalPowerOutput;
+    float powerUse = static_cast<float>(m_player->getPowerUsage()) / totalPowerOutput;
 
     float barHeightToDraw = barTotalHeight * powerIn;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerInY = barY + (barTotalHeight - barHeightToDraw);
 
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
+    m_sdlDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
 
     barHeightToDraw = barTotalHeight * powerUse;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerOutY = barY + (barTotalHeight - barHeightToDraw);
 
-    float powerUsageRatio = ((float)m_player->getPowerUsage() + 1) / ((float)m_player->getPowerProduced() + 1);
+    float powerUsageRatio = (static_cast<float>(m_player->getPowerUsage()) + 1) / (static_cast<float>(m_player->getPowerProduced()) + 1);
     int r = powerUsageRatio * 255;
     int g = (1.1 - powerUsageRatio) * 255;
 
@@ -316,36 +368,36 @@ void cSideBarDrawer::drawPowerUsage() const
     if (g > 255) g = 255;
 
     if (m_player->bEnoughPower()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{(Uint8)r, (Uint8)g, 32,255});
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{static_cast<Uint8>(r), static_cast<Uint8>(g), 32,255});
     }
     else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
     }
 
-    renderDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
+    m_sdlDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
 
-    renderDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
+    m_sdlDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
 
     // draw darker 'sides' at the left and top
     Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
+    m_sdlDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
+    m_sdlDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
     if (m_player->bEnoughPower()) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
     }
     else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
     }
 }
 
 void cSideBarDrawer::drawCreditsUsage()
 {
     int barTotalHeight = (cSideBar::HeightOfMinimap - 76);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
+    int barX = (m_services->settings->getScreenW() - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
     int barY = cSideBar::TopBarHeight + 48;
     int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
     // cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
+    m_sdlDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
 
     // STEFAN: 01/05/2021 -> looks like a lot of this code can be moved to the player class to retrieve max spice capacity
     // and so forth.
@@ -361,7 +413,7 @@ void cSideBarDrawer::drawCreditsUsage()
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerInY = barY + (barTotalHeight - barHeightToDraw);
 
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
+    m_sdlDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
 
     barHeightToDraw = barTotalHeight * spiceStored;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
@@ -376,24 +428,24 @@ void cSideBarDrawer::drawCreditsUsage()
     if (g > 255) g = 255;
 
     if (m_player->bEnoughSpiceCapacityToStoreCredits()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, (Uint8)r,(Uint8)g, 32,255);
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, static_cast<Uint8>(r),static_cast<Uint8>(g), 32,255);
     }
     else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
     }
 
-    renderDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
+    m_sdlDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
 
     // draw darker 'sides' at the left and top
     Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
+    m_sdlDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
+    m_sdlDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
 
     if (spiceCapacityRatio>0.95) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
     } else  if (spiceCapacityRatio<0.05) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
     } else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
     }
 }
````

## src/drawers/cSideBarDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cSideBarDrawer.h
```

stdout (1646 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.h b/src/drawers/cSideBarDrawer.h
index 3e246239..2dc9925b 100644
--- a/src/drawers/cSideBarDrawer.h
+++ b/src/drawers/cSideBarDrawer.h
@@ -6,12 +6,15 @@
 #include "observers/cInputObserver.h"
 #include "sMouseEvent.h"
 
+#include <array>
+
 class Texture;
 class cPlayer;
 class GameContext;
 class Graphics;
 
 class cSideBarDrawer : cInputObserver {
+    friend class UiAuditAccess;
 public:
     explicit cSideBarDrawer(GameContext *ctx, cPlayer *player);
     ~cSideBarDrawer() override;
@@ -27,27 +30,25 @@ public:
 
     void setPlayer(cPlayer *pPlayer);
 
-protected:
-    void drawBuildingLists();
-    void drawCapacities();
-
-    void drawCandybar();
-
-    void drawMinimap();
-
 private:
     cPlayer *m_player;
     Graphics *m_gfxinter;
     cBuildingListDrawer m_buildingListDrawer;
     cSideBar *m_sidebar;
-    Color m_sidebarColor;
-
-    void createCandyBar();
-
-    void drawPowerUsage() const;
-    void drawCreditsUsage();
-    Texture *candyBarBall=nullptr;
-    Texture *candyBarPiece=nullptr;
-    Texture *candyHorizonBar=nullptr;
-    Texture *candiBarRenderer= nullptr;
+    cTextDrawer *m_smallTextDrawer;
+    std::array<Texture *, 3> m_houseCrests{};
+
+    void drawHdSidebar();
+    void drawHdBuildingLists();
+    void drawHdRadarPanel();
+    void drawHdCapacities();
+    void drawHdMeter(
+        const cRectangle &rect,
+        const std::string &label,
+        int value,
+        int maximum,
+        Color fill,
+        bool warning) const;
+    [[nodiscard]] Texture *getHouseCrest() const;
+    [[nodiscard]] std::string getHouseDisplayName() const;
 };
````

## src/drawers/cSideBarDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cSideBarDrawer.h
```

stdout (2288 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.h b/src/drawers/cSideBarDrawer.h
index 3e246239..9f01b645 100644
--- a/src/drawers/cSideBarDrawer.h
+++ b/src/drawers/cSideBarDrawer.h
@@ -1,21 +1,44 @@
+/**
+ * @file cSideBarDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
 #include "cBuildingListDrawer.h"
 #include "cTextDrawer.h"
-#include "controls/cKeyboardEvent.h"
+class cKeyboardEvent;
 #include "observers/cInputObserver.h"
-#include "sMouseEvent.h"
+struct s_MouseEvent;
+
+#include <memory>
 
 class Texture;
 class cPlayer;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+class cInfoContext;
+class cMouse;
+struct sGameServices;
 
 class cSideBarDrawer : cInputObserver {
 public:
-    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player);
+    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
     ~cSideBarDrawer() override;
 
+    void serviceInit(sGameServices* services);
+
     void onNotifyMouseEvent(const s_MouseEvent &event) override;
     void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
 
@@ -38,16 +61,22 @@ protected:
 private:
     cPlayer *m_player;
     Graphics *m_gfxinter;
+    SDLDrawer* m_sdlDrawer;
+    GameContext* m_ctx = nullptr;
+    cInfoContext* m_infos = nullptr;
+    cMouse* m_mouse = nullptr;
+    sGameServices* m_services = nullptr;
     cBuildingListDrawer m_buildingListDrawer;
     cSideBar *m_sidebar;
     Color m_sidebarColor;
 
     void createCandyBar();
+    void createPlayerCandyBar();
 
     void drawPowerUsage() const;
     void drawCreditsUsage();
-    Texture *candyBarBall=nullptr;
-    Texture *candyBarPiece=nullptr;
-    Texture *candyHorizonBar=nullptr;
-    Texture *candiBarRenderer= nullptr;
+    std::unique_ptr<Texture> m_candyBarBall;
+    std::unique_ptr<Texture> m_candyBarPiece;
+    std::unique_ptr<Texture> m_candyHorizonBar;
+    Texture *m_candiBarRenderer= nullptr;
 };
````

# Дорожка 2, пункт 1 задания P5CR2

Таблица находится в `fork-hunks-2.tsv`. Скрипт `assemble.py` собрал участки командами `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <путь>`, определил шаг по строкам hunk и проверил места в `PORT`. Исходные diff-фрагменты, выгруженные через `git show`, вспомогательные скрипты и результаты работы сохранены только в `.tmp/p5cr2/`.

Для трёх файлов с фильтром применялись буквальные подстроки `HudLayout`, `sidebarWidth`, `TopBarHeight`, `battlefield`, `Battlefield` к добавленным, удалённым и контекстным строкам hunk. В `src/cGame_logic.cpp`, `src/controls/cGameControlsContext.cpp` и `src/controls/cMouse.cpp` совпадений нет; поэтому в таблице по ним 0 строк.

Для файлов камеры, отсутствующих по исходному пути в `PORT`, выполнены `git grep -n -F '<Класс>::<функция>(' 832c953a94a632d57872349013f7ed1a37434715 -- src`; полные команды и вывод лежат в `git-grep-port.txt`. Методы камеры нашлись в перемещённом `src/gameobjects/map/cMapCamera.cpp`; отсутствующие совпадения отмечены в таблице. Пересечения рассчитаны по новым сторонам hunks вывода `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- <путь в PORT>`.

## Проверка количества строк

Команда:

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/verify_counts.py
```

Вывод:

```text
src/managers/cDrawManager.cpp	TSV=10	diff=10	OK
src/managers/cDrawManager.h	TSV=6	diff=6	OK
src/map/cMapCamera.cpp	TSV=8	diff=8	OK
src/map/cMapCamera.h	TSV=5	diff=5	OK
src/sidebar/cBuildingList.cpp	TSV=2	diff=2	OK
src/sidebar/cBuildingList.h	TSV=1	diff=1	OK
src/sidebar/cBuildingListFactory.cpp	TSV=3	diff=3	OK
src/sidebar/cBuildingListItem.cpp	TSV=3	diff=3	OK
src/sidebar/cBuildingListItem.h	TSV=2	diff=2	OK
src/sidebar/cBuildingListUpdater.cpp	TSV=2	diff=2	OK
src/sidebar/cSideBar.cpp	TSV=3	diff=3	OK
src/sidebar/cSideBar.h	TSV=2	diff=2	OK
src/cGame_logic.cpp	TSV=0	diff=0	OK
src/controls/cGameControlsContext.cpp	TSV=0	diff=0	OK
src/controls/cMouse.cpp	TSV=0	diff=0	OK
Всего строк данных TSV: 47
Итог: OK
```

Полный stdout также сохранён в `verify-output.txt`. Сборки, CTest и запуск игры не выполнялись.

## Дополнительная проверка hunk `cDrawManager.cpp@9208dcf:77-82`

Команда:

```text
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/managers/cDrawManager.cpp
```

В её stdout есть hunk:

```diff
@@ -76,8 +77,6 @@ void cDrawManager::drawCombatState()
     // GUI
     drawSidebar();
 
-    drawOptionBar();
-
     renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
     drawStructurePlacing();
     renderDrawer->resetClippingFor();
```

Удаление `drawOptionBar()` подтверждает описание в таблице. Диапазон `77-82` относится к новой стороне hunk; удалённая строка поэтому показана со знаком `-` в выводе diff. Ячейку TSV не менял. Полный stdout команды находится в `track2-source-outputs.txt` и `source-outputs/fork__src__managers__cDrawManager.cpp.diff`.

Полные stdout 15 команд `git diff BASE FORK1`, результаты фильтра по трём файлам и 17 команд `git diff BASE PORT` сохранены в `track2-source-outputs.txt`; отдельные raw diff находятся в `source-outputs/`. Результаты поиска перенесённых методов камеры сохранены в `git-grep-port.txt`.

P5CR2, пункт 1, дорожка 2 — исходные команды и stdout
Ревизии: BASE=e17379ad660fca46859b403a6c3d33ec8d831a40; FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566; PORT=832c953a94a632d57872349013f7ed1a37434715.
Каждый блок ниже содержит точную команду git diff и полный stdout. Перед вызовами установлен PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH.


=== FORK1: src/managers/cDrawManager.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/managers/cDrawManager.cpp
stdout:
diff --git a/src/managers/cDrawManager.cpp b/src/managers/cDrawManager.cpp
index 7c0e45a9..3f6572c3 100644
--- a/src/managers/cDrawManager.cpp
+++ b/src/managers/cDrawManager.cpp
@@ -2,6 +2,7 @@
 
 #include "controls/cGameControlsContext.h"
 #include "d2tmc.h"
+#include "debug/UiAudit.hpp"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
@@ -9,14 +10,19 @@
 #include "gameobjects/projectiles/bullet.h"
 #include "player/cPlayer.h"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
+#include "sidebar/HudLayout.hpp"
+#include "sidebar/MusicControlsLayout.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "utils/cTimeManager.h"
 
 #include <SDL2/SDL.h>
 #include <cassert>
 
 cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer) :
     m_sidebarDrawer(ctx, thePlayer),
+    m_commandBarDrawer(ctx, thePlayer),
     m_creditsDrawer(ctx, thePlayer),
     m_orderDrawer(ctx, thePlayer),
     m_mapDrawer(&global_map, thePlayer, mapCamera),
@@ -25,23 +31,18 @@ cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer) :
     m_messageDrawer(ctx),
     m_placeitDrawer(thePlayer),
     m_structureDrawer(ctx),
-    m_sidebarColor(Color{214, 149, 20,255}),
     m_player(thePlayer),
     m_textDrawer(ctx->getTextContext()->getGameTextDrawer()),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_timeManager(ctx->getTimeManager())
 {
     assert(thePlayer);
-    btnOptions = thePlayer->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BTN_OPTIONS), TransparentColorIndex
-    );
     m_mouseDrawer = new cMouseDrawer(thePlayer, ctx->getTextContext()->getSmallTextDrawer());
 }
 
 cDrawManager::~cDrawManager()
 {
-    if (btnOptions) {
-        delete btnOptions;
-    }
 }
 
 void cDrawManager::drawCombatState()
@@ -76,8 +77,6 @@ void cDrawManager::drawCombatState()
     // GUI
     drawSidebar();
 
-    drawOptionBar();
-
     renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
     drawStructurePlacing();
     renderDrawer->resetClippingFor();
@@ -87,9 +86,12 @@ void cDrawManager::drawCombatState()
 
     // THE MESSAGE
     drawMessage();
+    drawTopBarMusicControls();
 
     drawNotifications();
 
+    m_commandBarDrawer.draw();
+
     renderDrawer->resetClippingFor();
 
     if (game.m_drawUsages) {
@@ -133,10 +135,13 @@ void cDrawManager::drawDebugInfoUsages() const
 
     int startY = 74;
     int height = 14;
-    m_textDrawer->drawText(0, startY, std::format("Units {}/{}", unitsUsed, MAX_UNITS));
-    m_textDrawer->drawText(0, startY + 1*height, std::format("Structures %d/%d", structuresUsed, MAX_STRUCTURES));
-    m_textDrawer->drawText(0, startY + 2*height, std::format("Bullets %d/%d", bulletsUsed, MAX_BULLETS));
-    m_textDrawer->drawText(0, startY + 3*height, std::format("Particles %d/%d", particlesUsed, MAX_PARTICLES));
+    m_textDrawer->drawText(0, startY, localization::format("Units {}/{}", "Юниты {}/{}", unitsUsed, MAX_UNITS));
+    m_textDrawer->drawText(0, startY + 1*height,
+                           localization::format("Structures {}/{}", "Здания {}/{}", structuresUsed, MAX_STRUCTURES));
+    m_textDrawer->drawText(0, startY + 2*height,
+                           localization::format("Projectiles {}/{}", "Снаряды {}/{}", bulletsUsed, MAX_BULLETS));
+    m_textDrawer->drawText(0, startY + 3*height,
+                           localization::format("Particles {}/{}", "Частицы {}/{}", particlesUsed, MAX_PARTICLES));
 }
 
 void cDrawManager::drawCredits()
@@ -156,17 +161,18 @@ void cDrawManager::drawRallyPoint()
     int drawX = mapCamera->getWindowXPositionFromCell(rallyPointCell);
     int drawY = mapCamera->getWindowYPositionFromCell(rallyPointCell);
 
-    SDL_Surface *mouseMoveBitmap = gfxdata->getSurface(MOUSE_MOVE);
+    const int mouseMoveWidth = gfxdata->getLogicalWidth(MOUSE_MOVE);
+    const int mouseMoveHeight = gfxdata->getLogicalHeight(MOUSE_MOVE);
 
-    int rallyPointWidthScaled = mapCamera->factorZoomLevel(mouseMoveBitmap->w);
-    int rallyPointHeightScaled = mapCamera->factorZoomLevel(mouseMoveBitmap->h);
+    int rallyPointWidthScaled = mapCamera->factorZoomLevel(mouseMoveWidth);
+    int rallyPointHeightScaled = mapCamera->factorZoomLevel(mouseMoveHeight);
     cRectangle dest = {drawX, drawY, rallyPointWidthScaled, rallyPointHeightScaled};
     renderDrawer->renderStrechFullSprite(gfxdata->getTexture(MOUSE_MOVE), dest);
 
     int startX = theStructure->iDrawX() + mapCamera->factorZoomLevel(theStructure->getWidthInPixels() / 2);
     int startY = theStructure->iDrawY() + mapCamera->factorZoomLevel(theStructure->getHeightInPixels() / 2);
 
-    int offset = (mouseMoveBitmap->w/2);
+    int offset = (mouseMoveWidth/2);
     drawX = mapCamera->getWindowXPositionFromCellWithOffset(rallyPointCell, offset);
     drawY = mapCamera->getWindowYPositionFromCellWithOffset(rallyPointCell, offset);
 
@@ -225,46 +231,212 @@ void cDrawManager::drawMouse()
 
 void cDrawManager::drawTopBarBackground()
 {
-    Texture *topbarPiece = m_gfxinter->getTexture(BMP_TOPBAR_BACKGROUND);
-    for (int x = 0; x < game.m_screenW; x+= topbarPiece->w) {
-        renderDrawer->renderSprite(topbarPiece, x, 0);
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("top-panel", 0, 0, game.m_screenW, cSideBar::TopBarHeight);
     }
+    const Color panel{17, 21, 23, 255};
+    const Color border{151, 113, 43, 255};
+    const Color text{232, 222, 188, 255};
+    renderDrawer->renderRectFillColor(
+        0,
+        0,
+        game.m_screenW,
+        cSideBar::TopBarHeight,
+        panel
+    );
+    renderDrawer->renderLine(
+        0,
+        cSideBar::TopBarHeight - 2,
+        game.m_screenW,
+        cSideBar::TopBarHeight - 2,
+        border
+    );
 
-    renderDrawer->renderSprite(btnOptions, 1, 0);
-
-    //HACK HACK: for now do it like this, instead of using an actual GUI object here
-    cRectangle optionsRect = cRectangle(0,0, 162, 30);
-    if (game.getMouse()->isLeftButtonClicked() && game.getMouse()->isOverRectangle(&optionsRect)) {
+    const cRectangle optionsRect(7, 4, 126, 33);
+    renderDrawer->renderRectFillColor(
+        optionsRect.getX(),
+        optionsRect.getY(),
+        optionsRect.getWidth(),
+        optionsRect.getHeight(),
+        Color{27, 31, 33, 255}
+    );
+    renderDrawer->renderRectColor(
+        optionsRect.getX(),
+        optionsRect.getY(),
+        optionsRect.getWidth(),
+        optionsRect.getHeight(),
+        border
+    );
+    m_textDrawer->drawTextCenteredInBox(
+        localization::text("OPTIONS", "НАСТРОЙКИ"),
+        optionsRect,
+        text
+    );
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordClick("top-options", optionsRect.getX(), optionsRect.getY(), optionsRect.getWidth(), optionsRect.getHeight());
+    }
+    if (game.getMouse()->isLeftButtonClicked() &&
+        game.getMouse()->isOverRectangle(
+            optionsRect.getX(),
+            optionsRect.getY(),
+            optionsRect.getWidth(),
+            optionsRect.getHeight())) {
         game.setNextStateToTransitionTo(GAME_OPTIONS);
     }
 }
 
+void cDrawManager::drawTopBarMusicControls()
+{
+    const HudLayout layout = HudLayout::create(game.m_screenW, game.m_screenH);
+    const int left = 143;
+    const int right = layout.battlefield.getEndX() - 8;
+    drawMusicControls(left, right);
+}
+
+void cDrawManager::drawMusicControls(int left, int right)
+{
+    const std::string message = m_messageDrawer.getMessage();
+    const int reservedMessageWidth = message.empty()
+        ? 0
+        : m_textDrawer->getTextLength(message) + 16;
+    const MusicControlsLayout layout = MusicControlsLayout::create(
+        left,
+        right,
+        reservedMessageWidth
+    );
+    if (!layout.visible) {
+        return;
+    }
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordClick("music-previous", layout.previous.getX(), layout.previous.getY(), layout.previous.getWidth(), layout.previous.getHeight());
+        uiaudit::recordClick("music-next", layout.next.getX(), layout.next.getY(), layout.next.getWidth(), layout.next.getHeight());
+        uiaudit::recordClick("music-speed-slider", layout.speedSlider.getX(), layout.speedSlider.getY(), layout.speedSlider.getWidth(), layout.speedSlider.getHeight());
+    }
+
+    const Color panel{35, 32, 25, 255};
+    const Color border{188, 139, 47, 255};
+    const Color borderDark{71, 50, 24, 255};
+    const Color text{232, 222, 188, 255};
+
+    for (const cRectangle *rect : {&layout.previous, &layout.next}) {
+        renderDrawer->renderRectFillColor(rect->getX(), rect->getY(), rect->getWidth(), rect->getHeight(), panel);
+        renderDrawer->renderRectColor(rect->getX(), rect->getY(), rect->getWidth(), rect->getHeight(), border);
+    }
+    m_textDrawer->drawTextCenteredInBox("<", layout.previous, text);
+    m_textDrawer->drawTextCenteredInBox(">", layout.next, text);
+
+    if (layout.showsLabel()) {
+        std::string name = game.getCurrentMusicTrackName();
+        bool truncated = false;
+        const std::string ellipsis = "...";
+        while (!name.empty() &&
+               m_smallTextDrawer->getTextLength(name + (truncated ? ellipsis : std::string{})) > layout.label.getWidth() - 10) {
+            std::size_t characterStart = name.size() - 1U;
+            while (characterStart > 0U &&
+                   (static_cast<unsigned char>(name[characterStart]) & 0xC0U) == 0x80U) {
+                --characterStart;
+            }
+            name.erase(characterStart);
+            truncated = true;
+        }
+        while (!name.empty() && truncated &&
+               m_smallTextDrawer->getTextLength(name + ellipsis) > layout.label.getWidth() - 10) {
+            std::size_t characterStart = name.size() - 1U;
+            while (characterStart > 0U &&
+                   (static_cast<unsigned char>(name[characterStart]) & 0xC0U) == 0x80U) {
+                --characterStart;
+            }
+            name.erase(characterStart);
+        }
+        if (!name.empty() && truncated) {
+            name += ellipsis;
+        }
+        renderDrawer->renderRectFillColor(layout.label.getX(), layout.label.getY(), layout.label.getWidth(), layout.label.getHeight(), panel);
+        renderDrawer->renderRectColor(layout.label.getX(), layout.label.getY(), layout.label.getWidth(), layout.label.getHeight(), border);
+        m_smallTextDrawer->drawTextCenteredInBox(name, layout.label, text);
+    }
+
+    renderDrawer->renderRectFillColor(layout.speedLabel, panel);
+    renderDrawer->gui_DrawRectBorder(layout.speedLabel, border, borderDark);
+    m_smallTextDrawer->drawTextCenteredInBox(
+        localization::text("SPEED", "СКОРОСТЬ"),
+        layout.speedLabel,
+        text
+    );
+
+    renderDrawer->renderRectFillColor(layout.speedSlider, panel);
+    renderDrawer->gui_DrawRectBorder(layout.speedSlider, border, borderDark);
+
+    constexpr int MinSliderValue = 2;
+    constexpr int MaxSliderValue = 10;
+    constexpr int SliderKnobWidth = 12;
+    const int globalSpeed = std::clamp<int>(m_timeManager->getGlobalSpeed(), 2, 10);
+    int sliderValue = 12 - globalSpeed;
+
+    cMouse *mouse = game.getMouse();
+    const bool mouseOverSlider = mouse->isOverRectangle(
+        layout.speedSlider.getX(),
+        layout.speedSlider.getY(),
+        layout.speedSlider.getWidth(),
+        layout.speedSlider.getHeight()
+    );
+    if ((mouse->isLeftButtonPressed() || mouse->isLeftButtonClicked()) && mouseOverSlider) {
+        m_speedSliderDragging = true;
+    }
+    if (!mouse->isLeftButtonPressed() && !mouse->isLeftButtonClicked()) {
+        m_speedSliderDragging = false;
+    }
+    if (m_speedSliderDragging) {
+        const int position = std::clamp(
+            mouse->getX() - layout.speedSlider.getX(),
+            0,
+            layout.speedSlider.getWidth()
+        );
+        sliderValue = MinSliderValue +
+            position * (MaxSliderValue - MinSliderValue) /
+            std::max(1, layout.speedSlider.getWidth());
+        const int requestedGlobalSpeed = 12 - sliderValue;
+        if (requestedGlobalSpeed != globalSpeed) {
+            m_timeManager->setGlobalSpeed(requestedGlobalSpeed);
+        }
+    }
+
+    const int knobTravel = std::max(0, layout.speedSlider.getWidth() - SliderKnobWidth);
+    const int knobX = layout.speedSlider.getX() +
+        (sliderValue - MinSliderValue) * knobTravel /
+        (MaxSliderValue - MinSliderValue);
+    const cRectangle knob(knobX, layout.speedSlider.getY(), SliderKnobWidth, layout.speedSlider.getHeight());
+    renderDrawer->renderRectFillColor(knob, borderDark);
+    renderDrawer->gui_DrawRectBorder(knob, border, borderDark);
+
+    if (mouse->isLeftButtonClicked()) {
+        if (mouse->isOverRectangle(
+                layout.previous.getX(), layout.previous.getY(), layout.previous.getWidth(), layout.previous.getHeight())) {
+            game.playPreviousGameplayTrack();
+        }
+        else if (mouse->isOverRectangle(
+                     layout.next.getX(), layout.next.getY(), layout.next.getWidth(), layout.next.getHeight())) {
+            game.playNextGameplayTrack();
+        }
+    }
+}
+
 void cDrawManager::setPlayerToDraw(cPlayer *playerToDraw)
 {
     m_player = playerToDraw;
     m_creditsDrawer.setPlayer(playerToDraw);
     m_sidebarDrawer.setPlayer(playerToDraw);
+    m_commandBarDrawer.setPlayer(playerToDraw);
     m_orderDrawer.setPlayer(playerToDraw);
     miniMapDrawer.setPlayer(playerToDraw);
     m_mapDrawer.setPlayer(playerToDraw);
 }
 
-void cDrawManager::drawOptionBar()
-{
-    // upper bar
-    renderDrawer->renderRectFillColor(0, 0, game.m_screenW, cSideBar::TopBarHeight, Color{0, 0, 0,255});
-    renderDrawer->renderRectFillColor(0,game.m_screenW, 40,32, Color{214,149,20,255});
-
-    for (int w = 0; w < (game.m_screenW + 800); w += 789) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_TOP_BAR), w, 31);
-    }
-}
-
 void cDrawManager::drawNotifications()
 {
     std::vector<cPlayerNotification> &notifications = m_player->getNotifications();
 //    int y = cSideBar::TopBarHeight + 14; // 12 pixels
-    int y = game.m_screenH - 44;
+    int y = m_commandBarDrawer.getTopY() - 18;
     for (auto &notification : notifications) {
         m_textDrawer->drawText(4, y, notification.getColor(), notification.getMessage().c_str());
         y-=15;
@@ -284,6 +456,7 @@ void cDrawManager::init()
 void cDrawManager::onNotifyMouseEvent(const s_MouseEvent &event)
 {
     m_sidebarDrawer.onNotifyMouseEvent(event);
+    m_commandBarDrawer.onNotifyMouseEvent(event);
 }
 
 void cDrawManager::onNotifyKeyboardEvent(const cKeyboardEvent &event)
@@ -354,6 +527,11 @@ void cDrawManager::setMessage(std::string msg, bool keepMessage)
     m_messageDrawer.setMessage(msg, keepMessage);
 }
 
+std::string cDrawManager::getMessage() const
+{
+    return m_messageDrawer.getMessage();
+}
+
 void cDrawManager::setKeepMessage(bool value)
 {
     m_messageDrawer.setKeepMessage(value);


=== FORK1: src/managers/cDrawManager.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/managers/cDrawManager.h
stdout:
diff --git a/src/managers/cDrawManager.h b/src/managers/cDrawManager.h
index 247baca4..8e3bb12b 100644
--- a/src/managers/cDrawManager.h
+++ b/src/managers/cDrawManager.h
@@ -2,6 +2,7 @@
 
 #include "controls/cKeyboardEvent.h"
 #include "drawers/cBuildingListDrawer.h"
+#include "drawers/cCommandBarDrawer.h"
 #include "drawers/cMapDrawer.h"
 #include "drawers/cMessageDrawer.h"
 #include "drawers/cMiniMapDrawer.h"
@@ -21,6 +22,7 @@ struct SDL_Surface;
 class Texture;
 class GameContext;
 class Graphics;
+class cTimeManager;
 
 /**
  * Candidate class for PlayingMissionState (draw function?), but also for SelectYourNextConquestState (drawing
@@ -45,6 +47,10 @@ public:
         return &m_orderDrawer;
     }
 
+    cCommandBarDrawer *getCommandBarDrawer() {
+        return &m_commandBarDrawer;
+    }
+
     cMouseDrawer *getMouseDrawer() {
         return m_mouseDrawer;
     }
@@ -76,6 +82,7 @@ public:
     void drawMessageBar();
 
     void setMessage(std::string msg, bool keepMessage = false);
+    [[nodiscard]] std::string getMessage() const;
 
     void setKeepMessage(bool value);
 
@@ -95,16 +102,17 @@ protected:
     void drawRallyPoint();
 
     void drawTopBarBackground();
+    void drawTopBarMusicControls();
+    void drawMusicControls(int left, int right);
 
 private:
-    void drawOptionBar();
-
     void drawDebugInfoUsages() const;
 
     void drawNotifications();
 
     // Properties:
     cSideBarDrawer m_sidebarDrawer;
+    cCommandBarDrawer m_commandBarDrawer;
     CreditsDrawer m_creditsDrawer;
     cOrderDrawer m_orderDrawer;
     cMapDrawer m_mapDrawer;
@@ -113,14 +121,15 @@ private:
     cMessageDrawer m_messageDrawer;
     cPlaceItDrawer m_placeitDrawer;
     cStructureDrawer m_structureDrawer;
-    Color m_sidebarColor;
-    Texture *btnOptions;
 
     // TODO: bullet/projectile drawer
     cPlayer *m_player;
     cTextDrawer *m_textDrawer = nullptr;
+    cTextDrawer *m_smallTextDrawer = nullptr;
     Graphics* m_gfxinter;
     cMouseDrawer* m_mouseDrawer = nullptr;
+    cTimeManager *m_timeManager = nullptr;
+    bool m_speedSliderDragging = false;
 
     void onKeyDown(const cKeyboardEvent &event);
 


=== FORK1: src/map/cMapCamera.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/map/cMapCamera.cpp
stdout:
diff --git a/src/map/cMapCamera.cpp b/src/map/cMapCamera.cpp
index f9c24a52..21f6da12 100644
--- a/src/map/cMapCamera.cpp
+++ b/src/map/cMapCamera.cpp
@@ -1,7 +1,9 @@
 #include "cMapCamera.h"
 
+#include "controls/cGameControlsContext.h"
 #include "data/gfxdata.h"
 #include "d2tmc.h"
+#include "player/cPlayer.h"
 #include "sidebar/cSideBar.h"
 #include "map/MapGeometry.hpp"
 
@@ -9,6 +11,27 @@
 
 namespace {
 constexpr auto kMapBoundaryScrollSpeed = 5.0f;
+
+template <typename WindowPosition>
+int findTileIndex(int pixel, int tileCount, int tileSize, WindowPosition windowPosition)
+{
+    if (tileCount <= 0 || pixel < windowPosition(0)) {
+        return -1;
+    }
+
+    int low = 0;
+    int high = tileCount - 1;
+    while (low < high) {
+        int mid = (low + high + 1) / 2;
+        if (windowPosition(mid * tileSize) <= pixel) {
+            low = mid;
+        }
+        else {
+            high = mid - 1;
+        }
+    }
+    return pixel < windowPosition((low + 1) * tileSize) ? low : -1;
+}
 }
 
 cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
@@ -18,7 +41,7 @@ cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderO
     m_pMap(theMap)
 {
     m_viewportStartX = m_viewportStartY = 32;
-    m_zoomLevel = 1.0f;
+    m_zoomLevel = game.getWorldScaleFactor();
 
     int widthOfSidebar = cSideBar::SidebarWidth;
     m_heightOfTopBar = cSideBar::TopBarHeight;
@@ -44,12 +67,21 @@ cMapCamera::~cMapCamera()
 {
 }
 
+void cMapCamera::resetZoom()
+{
+    m_zoomLevel = game.getWorldScaleFactor();
+    calibrate();
+    keepViewportWithinReasonableBounds();
+    refreshMouseHover();
+}
+
 void cMapCamera::zoomIn()
 {
     if (m_zoomLevel < 4.0) {
         m_zoomLevel += 0.1;
         auto m_mouse = game.getMouse();
         adjustViewport(m_mouse->getX(), m_mouse->getY());
+        refreshMouseHover();
     }
 }
 
@@ -78,6 +110,7 @@ void cMapCamera::zoomOut()
         m_zoomLevel -= 0.1;
         auto m_mouse = game.getMouse();
         adjustViewport(m_mouse->getX(), m_mouse->getY());
+        refreshMouseHover();
     }
 }
 
@@ -136,20 +169,22 @@ void cMapCamera::centerAndJumpViewPortToCell(int cell)
     newViewPortY = (newViewPortY / 32) * 32;
 
     jumpTo(newViewPortX, newViewPortY);
-
-    calibrate();
-
-    keepViewportWithinReasonableBounds();
 }
 
 void cMapCamera::thinkFast()
 {
+    const float previousViewportStartX = m_viewportStartX;
+    const float previousViewportStartY = m_viewportStartY;
+
     // update viewport coordinates
     m_viewportStartX = m_viewportStartX + m_moveX;
     m_viewportStartY = m_viewportStartY + m_moveY;
 
     keepViewportWithinReasonableBounds();
 
+    if (m_viewportStartX != previousViewportStartX || m_viewportStartY != previousViewportStartY) {
+        refreshMouseHover();
+    }
 }
 
 void cMapCamera::jumpTo(int theX, int theY)
@@ -157,12 +192,13 @@ void cMapCamera::jumpTo(int theX, int theY)
     m_viewportStartX = theX;
     m_viewportStartY = theY;
     calibrate();
+    keepViewportWithinReasonableBounds();
+    refreshMouseHover();
 }
 
 void cMapCamera::setViewportPosition(int x, int y)
 {
     jumpTo(x, y);
-    keepViewportWithinReasonableBounds();
 }
 
 int cMapCamera::getCellFromAbsolutePosition(int x, int y)
@@ -170,6 +206,26 @@ int cMapCamera::getCellFromAbsolutePosition(int x, int y)
     return global_map.getGeometry().getCellWithMapDimensions((x / 32), (y / 32));
 }
 
+int cMapCamera::getCellFromWindowPosition(int windowX, int windowY)
+{
+    int cellX = findTileIndex(windowX, global_map.getWidth(), TILESIZE_WIDTH_PIXELS, [this](int absoluteX) {
+        return getWindowXPosition(absoluteX);
+    });
+    int cellY = findTileIndex(windowY, global_map.getHeight(), TILESIZE_HEIGHT_PIXELS, [this](int absoluteY) {
+        return getWindowYPosition(absoluteY);
+    });
+    return global_map.getGeometry().getCellWithMapDimensions(cellX, cellY);
+}
+
+void cMapCamera::refreshMouseHover()
+{
+    cGameControlsContext *controls = players[HUMAN].getGameControlsContext();
+    if (controls == nullptr || drawManager == nullptr) {
+        return;
+    }
+    controls->refreshMouseHover();
+}
+
 void cMapCamera::onNotifyMouseEvent(const s_MouseEvent &event)
 {
     // MOUSE WHEEL scrolling causes zooming in/out


=== FORK1: src/map/cMapCamera.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/map/cMapCamera.h
stdout:
diff --git a/src/map/cMapCamera.h b/src/map/cMapCamera.h
index a76f36e5..cb05b3c2 100644
--- a/src/map/cMapCamera.h
+++ b/src/map/cMapCamera.h
@@ -29,11 +29,7 @@ public:
 
     void thinkFast();
 
-    void resetZoom() {
-        m_zoomLevel = 1.0f;
-        calibrate();
-        keepViewportWithinReasonableBounds();
-    }
+    void resetZoom();
 
     void jumpTo(int theX, int theY);
 
@@ -93,17 +89,17 @@ public:
         return std::round(factorZoomLevel((absoluteYPosition - m_viewportStartY) + offset) + m_heightOfTopBar);
     }
 
-    // These methods need to use zoomfactor to properly calculate the position on the map
+    // A sample exactly on a cell border belongs to the cell before it, as the drawn rectangles are half-open on the right
     int getAbsMapMouseX(int mouseX) {
-        int iMouseX = divideByZoomLevel(mouseX);
-        return iMouseX + getViewportStartX();
+        return static_cast<int>(std::ceil((mouseX + 0.5) / m_zoomLevel + m_viewportStartX)) - 1;
     }
 
     int getAbsMapMouseY(int mouseY) {
-        int iMouseY = divideByZoomLevel(mouseY - m_heightOfTopBar);
-        return iMouseY + getViewportStartY();
+        return static_cast<int>(std::ceil((mouseY - m_heightOfTopBar + 0.5) / m_zoomLevel + m_viewportStartY)) - 1;
     }
 
+    int getCellFromWindowPosition(int windowX, int windowY);
+
     int getViewportStartX() {
         return m_viewportStartX;
     }
@@ -146,6 +142,15 @@ public:
         return m_tileHeight;
     }
 
+    // Reaches one pixel into the next tile so rounding never leaves a gap between tiles.
+    int getTileDrawWidth(int absoluteXPosition) {
+        return getWindowXPosition(absoluteXPosition + TILESIZE_WIDTH_PIXELS) - getWindowXPosition(absoluteXPosition) + 1;
+    }
+
+    int getTileDrawHeight(int absoluteYPosition) {
+        return getWindowYPosition(absoluteYPosition + TILESIZE_HEIGHT_PIXELS) - getWindowYPosition(absoluteYPosition) + 1;
+    }
+
     float factorZoomLevel(int value) {
         return value * m_zoomLevel;
     }
@@ -213,6 +218,8 @@ private:
 
     void adjustViewport(float screenX, float screenY);
 
+    void refreshMouseHover();
+
     // Calculates viewport and tile width/height
     void calibrate();
 
@@ -231,4 +238,6 @@ private:
 
     void onKeyHold(const cKeyboardEvent &event);
     void onKeyPressed(const cKeyboardEvent &event);
+
+    friend class UiAuditAccess;
 };


=== FORK1: src/sidebar/cBuildingList.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingList.cpp
stdout:
diff --git a/src/sidebar/cBuildingList.cpp b/src/sidebar/cBuildingList.cpp
index 3410b9cd..20f61923 100644
--- a/src/sidebar/cBuildingList.cpp
+++ b/src/sidebar/cBuildingList.cpp
@@ -253,7 +253,14 @@ bool cBuildingList::removeItemFromList(int position)
  */
 bool cBuildingList::isOverButton(int x, int y)
 {
-    return cRectangle::isWithin(x, y, getButtonDrawX(), getButtonDrawY(), 33, 27);
+    return cRectangle::isWithin(
+        x,
+        y,
+        getButtonDrawX(),
+        getButtonDrawY(),
+        buttonWidth,
+        buttonHeight
+    );
 }
 
 /**
@@ -469,4 +476,4 @@ void cBuildingList::stopFlashing()
 void cBuildingList::startFlashing()
 {
     TIMER_flashing = 2500;
-}
\ No newline at end of file
+}


=== FORK1: src/sidebar/cBuildingList.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingList.h
stdout:
diff --git a/src/sidebar/cBuildingList.h b/src/sidebar/cBuildingList.h
index d3323d8d..dc8584b9 100644
--- a/src/sidebar/cBuildingList.h
+++ b/src/sidebar/cBuildingList.h
@@ -79,10 +79,22 @@ public:
         return buttonDrawY;
     }
 
+    int getButtonWidth() const {
+        return buttonWidth;
+    }
+
+    int getButtonHeight() const {
+        return buttonHeight;
+    }
+
     bool isAvailable() {
         return maxItems > 0;
     }
 
+    int getItemCount() const {
+        return maxItems;
+    }
+
     std::array<int, 6> isBuildingItem();
 
     cBuildingListItem *getItemByBuildId(int buildId);


=== FORK1: src/sidebar/cBuildingListFactory.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingListFactory.cpp
stdout:
diff --git a/src/sidebar/cBuildingListFactory.cpp b/src/sidebar/cBuildingListFactory.cpp
index cf6e0573..e6d61531 100644
--- a/src/sidebar/cBuildingListFactory.cpp
+++ b/src/sidebar/cBuildingListFactory.cpp
@@ -2,6 +2,7 @@
 
 #include "d2tmc.h"
 #include "data/gfxinter.h"
+#include "sidebar/HudLayout.hpp"
 
 cBuildingListFactory *cBuildingListFactory::instance = NULL;
 
@@ -20,14 +21,18 @@ cBuildingListFactory *cBuildingListFactory::getInstance()
 
 int cBuildingListFactory::getButtonDrawY()
 {
-    // 6 pixels margin below horizontal candybar, so it lines up nice horizontally with the sphere
-    // of the vertical candybar at the left of the building list icons
-    return cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight + 6;
+    return HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    ).tabs.getY();
 }
 
 int cBuildingListFactory::getButtonDrawXStart()
 {
-    return (game.m_screenW - 200) + 2;
+    return HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    ).tabs.getX();
 }
 
 
@@ -41,9 +46,14 @@ void cBuildingListFactory::initializeList(cBuildingList *list, eListType listTyp
     // Y is the same for all list buttons
     list->setButtonDrawY(getButtonDrawY());
 
-    int widthOfButtonIncludingMargin = 33;
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const int widthOfButtonIncludingMargin = layout.tabs.getWidth() / 6;
+    const int buttonHeight = layout.tabs.getHeight();
     list->setButtonWidth(widthOfButtonIncludingMargin);
-//    list->setButtonHeight()
+    list->setButtonHeight(buttonHeight);
 
     int startX = getButtonDrawXStart();
 


=== FORK1: src/sidebar/cBuildingListItem.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingListItem.cpp
stdout:
diff --git a/src/sidebar/cBuildingListItem.cpp b/src/sidebar/cBuildingListItem.cpp
index ea84a91b..e81bdcd7 100644
--- a/src/sidebar/cBuildingListItem.cpp
+++ b/src/sidebar/cBuildingListItem.cpp
@@ -2,6 +2,7 @@
 
 #include "d2tmc.h"
 #include "sidebar/cBuildingList.h"
+#include "utils/Localization.hpp"
 
 #include <format>
 
@@ -383,27 +384,27 @@ std::string cBuildingListItem::getInfo()
 
     if (isTypeStructure()) {
         s_StructureInfo structureType = getStructureInfo();
-        msg = std::format("${} | {} | {} Power | {} Secs", getBuildCost(), structureType.name, (structureType.power_give - structureType.power_drain), seconds);
+        msg = localization::format("${} | {} | power {} | {} s", "${} | {} | энергия {} | {} с", getBuildCost(), structureType.name, (structureType.power_give - structureType.power_drain), seconds);
     }
     else if (isTypeUnit()) {
         s_UnitInfo unitType = getUnitInfo();
         if (getBuildCost() > 0) {
-            msg = std::format("${} | {} | {} Secs", getBuildCost(), unitType.name, seconds);
+            msg = localization::format("${} | {} | {} s", "${} | {} | {} с", getBuildCost(), unitType.name, seconds);
         }
         else {
-            msg = std::format("{} | {} Secs", sUnitInfo[getBuildId()].name, seconds);
+            msg = localization::format("{} | {} s", "{} | {} с", sUnitInfo[getBuildId()].name, seconds);
         }
     }
     else if (isTypeUpgrade()) {
         s_UpgradeInfo upgrade = getUpgradeInfo();
-        msg = std::format("UPGRADE: ${} | {} | {} Secs", getBuildCost(), upgrade.description, seconds);
+        msg = localization::format("UPGRADE: ${} | {} | {} s", "УЛУЧШЕНИЕ: ${} | {} | {} с", getBuildCost(), upgrade.description, seconds);
     }
     else if (isTypeSpecial()) {
         s_SpecialInfo special = getSpecialInfo();
-        msg = std::format("${} | {} | {} Secs", getBuildCost(), special.description, seconds);
+        msg = localization::format("${} | {} | {} s", "${} | {} | {} с", getBuildCost(), special.description, seconds);
     }
     else {
-        msg = "ERROR: UNKNOWN BUILD TYPE";
+        msg = localization::text("ERROR: UNKNOWN TYPE", "ОШИБКА: НЕИЗВЕСТНЫЙ ТИП");
     }
     return msg;
 }
@@ -442,5 +443,5 @@ std::string cBuildingListItem::getNameString()
         return std::string(special.description);
     }
 
-    return std::string("Unknown type.");
+    return std::string(localization::text("Unknown type.", "Неизвестный тип."));
 }


=== FORK1: src/sidebar/cBuildingListItem.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingListItem.h
stdout:
diff --git a/src/sidebar/cBuildingListItem.h b/src/sidebar/cBuildingListItem.h
index dae2191b..23a4dabf 100644
--- a/src/sidebar/cBuildingListItem.h
+++ b/src/sidebar/cBuildingListItem.h
@@ -12,6 +12,7 @@
 #include <string>
 
 class cBuildingList;
+class SaveGameManager;
 
 class cBuildingListItem {
 
@@ -252,6 +253,7 @@ public:
     void decreaseFlashingTimer();
 
 private:
+    friend class SaveGameManager;
     void setProgress(int value) {
         progress = value;
     }


=== FORK1: src/sidebar/cBuildingListUpdater.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cBuildingListUpdater.cpp
stdout:
diff --git a/src/sidebar/cBuildingListUpdater.cpp b/src/sidebar/cBuildingListUpdater.cpp
index 61ab9147..b339726b 100644
--- a/src/sidebar/cBuildingListUpdater.cpp
+++ b/src/sidebar/cBuildingListUpdater.cpp
@@ -2,6 +2,7 @@
 
 #include "building/cItemBuilder.h"
 #include "d2tmc.h"
+#include "gameobjects/structures/StarportOrderQueue.hpp"
 #include "player/cPlayer.h"
 #include "utils/cLog.h"
 
@@ -435,12 +436,15 @@ void cBuildingListUpdater::onStructureDestroyed(int structureType)
     cBuildingList *listConstYard = sideBar->getList(eListType::LIST_CONSTYARD);
 
     if (structureType == STARPORT) {
-        if (!player->hasAtleastOneStructure(STARPORT)) {
+        if (!isStarportCatalogAvailable(player->hasAtleastOneStructure(STARPORT))) {
             listConstYard->removeItemFromListByBuildId(IX);
             cOrderProcesser *pProcesser = player->getOrderProcesser();
             pProcesser->clear();
             cBuildingList *listStarport = sideBar->getList(eListType::LIST_STARPORT);
-            listStarport->resetTimesOrderedForAllItems();
+            while (listStarport->removeItemFromList(0)) {
+                // Removing the final entry emits the unavailable-list event,
+                // which also moves selection away from the Starport tab.
+            }
         }
     }
 


=== FORK1: src/sidebar/cSideBar.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cSideBar.cpp
stdout:
diff --git a/src/sidebar/cSideBar.cpp b/src/sidebar/cSideBar.cpp
index 843fd3b8..30c8ff39 100644
--- a/src/sidebar/cSideBar.cpp
+++ b/src/sidebar/cSideBar.cpp
@@ -302,6 +302,8 @@ void cSideBar::onNotifyMouseEvent(const s_MouseEvent &event)
         return;
     }
 
+    drawManager->getBuildingListDrawer()->onNotifyMouseEvent(event);
+
     switch (event.eventType) {
         case eMouseEventType::MOUSE_MOVED_TO:
             onMouseAt(event);
@@ -312,6 +314,9 @@ void cSideBar::onNotifyMouseEvent(const s_MouseEvent &event)
         case eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED:
             onMouseClickedRight(event);
             return;
+        case eMouseEventType::MOUSE_SCROLLED_UP:
+        case eMouseEventType::MOUSE_SCROLLED_DOWN:
+            return;
         default:
             return;
     }
@@ -403,3 +408,15 @@ void cSideBar::setSelectedListId(eListType value)
         lists[selectedListID]->setSelected(true);
     }
 }
+void cSideBar::configureLayout(bool hdMode, int logicalWidth)
+{
+    if (!hdMode) {
+        SidebarWidthWithoutCandyBar = 200;
+        SidebarWidth = SidebarWidthWithoutCandyBar + VerticalCandyBarWidth;
+        return;
+    }
+
+    SidebarWidth = logicalWidth < 960 ? 280 : 360;
+    // HD uses a narrow graphite divider instead of the 24 px candybar.
+    SidebarWidthWithoutCandyBar = SidebarWidth - 8;
+}


=== FORK1: src/sidebar/cSideBar.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/sidebar/cSideBar.h
stdout:
diff --git a/src/sidebar/cSideBar.h b/src/sidebar/cSideBar.h
index c2d9ad53..cae35ddd 100644
--- a/src/sidebar/cSideBar.h
+++ b/src/sidebar/cSideBar.h
@@ -79,9 +79,9 @@ public:
 
     static const int LIST_MAX = 7;
 
-    static const int VerticalCandyBarWidth = 24;
-    static const int SidebarWidthWithoutCandyBar = 200;
-    static const int SidebarWidth = SidebarWidthWithoutCandyBar + VerticalCandyBarWidth; // including vertical candy bar
+    static constexpr int VerticalCandyBarWidth = 24;
+    inline static int SidebarWidthWithoutCandyBar = 200;
+    inline static int SidebarWidth = 224;
     static const int TopBarHeight = 42;
     static const int HeightOfMinimap = 200 + 8;
     static const int WidthOfMinimap = 200;
@@ -95,6 +95,8 @@ public:
     static const int TotalHeightBeforePowerBarStarts =
         TopBarHeight + HeightOfMinimap + HorizontalCandyBarHeight + PowerBarMarginHeight;
 
+    static void configureLayout(bool hdMode, int logicalWidth);
+
     void onNotifyMouseEvent(const s_MouseEvent &event);
 
     void cancelBuildingListItem(cBuildingListItem *item);


=== FORK1: src/cGame_logic.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/cGame_logic.cpp
stdout:
diff --git a/src/cGame_logic.cpp b/src/cGame_logic.cpp
index 45505256..db1c6b43 100644
--- a/src/cGame_logic.cpp
+++ b/src/cGame_logic.cpp
@@ -9,7 +9,10 @@
   2001 - 2022 (c) code by Stefan Hendriks
 
 */
+#include "debug/UiAudit.hpp"
 #include "cGame.h"
+#include "audio/MusicController.h"
+#include "audio/MusicTransitionPolicy.hpp"
 #include "include/Texture.hpp"
 #include "building/cItemBuilder.h"
 #include "d2tmc.h"
@@ -44,6 +47,7 @@
 #include "sidebar/cBuildingListFactory.h"
 #include "sidebar/cSideBarFactory.h"
 #include "utils/RNG.hpp"
+#include "utils/SoundDistance.hpp"
 #include "utils/cLog.h"
 #include "utils/cPlatformLayerInit.h"
 #include "utils/cSoundPlayer.h"
@@ -58,6 +62,13 @@
 #include "player/cHousesInfo.h"
 #include "utils/Graphics.hpp"
 #include "utils/GameSettings.hpp"
+#include "utils/Localization.hpp"
+#include "utils/HdPresentation.hpp"
+#include "utils/HdUiTextureLoader.hpp"
+#include "utils/OutcomeScreenLayout.hpp"
+#include "utils/RenderScale.hpp"
+#include "utils/WorldScale.hpp"
+#include "save/SaveGameManager.hpp"
 #include <format>
 #include "context/GameContext.hpp"
 #include "context/ContextCreator.hpp"
@@ -68,7 +79,10 @@
 #include "utils/cFocusManager.h"
 
 #include <algorithm>
+#include <array>
+#include <filesystem>
 #include <random>
+#include <string_view>
 #include <vector>
 #include <iostream>
 
@@ -79,6 +93,55 @@ namespace {
 constexpr auto kMinAlpha = 0;
 constexpr auto kMaxAlpha = 255;
 
+MusicCategory musicCategoryFor(int musicType, int house)
+{
+    switch (musicType) {
+        case MUSIC_PEACE:
+        case MUSIC_ATTACK:
+            return MusicCategory::Gameplay;
+        case MUSIC_MENU:
+            return MusicCategory::Menu;
+        case MUSIC_CONQUEST:
+            return MusicCategory::Conquest;
+        case MUSIC_WIN:
+            return MusicCategory::Victory;
+        case MUSIC_LOSE:
+            return MusicCategory::Defeat;
+        case MUSIC_BRIEFING:
+            if (house == HARKONNEN) return MusicCategory::BriefingHarkonnen;
+            if (house == ORDOS) return MusicCategory::BriefingOrdos;
+            return MusicCategory::BriefingAtreides;
+        default:
+            return MusicCategory::Menu;
+    }
+}
+
+std::string defaultHdDataFileName(
+    std::string_view key,
+    int density)
+{
+    static_cast<void>(density);
+    const std::string suffix = "_hd4.dat";
+    if (key == "GFXDATA") return "sdl_data" + suffix;
+    if (key == "GFXINTER") return "sdl_inter" + suffix;
+    if (key == "GFXWORLD") return "sdl_world" + suffix;
+    if (key == "GFXMENTAT") return "sdl_mentat" + suffix;
+    return "";
+}
+
+std::string graphicsDataFileName(
+    const cIniFile &settings,
+    const std::string &section,
+    std::string_view key,
+    int density)
+{
+    const std::string configured =
+        settings.getStringValue(section, std::string(key));
+    return configured.empty()
+        ? defaultHdDataFileName(key, density)
+        : configured;
+}
+
 }
 
 cGame::cGame()
@@ -91,6 +154,9 @@ cGame::cGame()
     m_currentState = nullptr;
     m_screenW = -1;
     m_screenH = -1;
+    m_renderScalePercent = 0;
+    m_worldScalePercent = 0;
+    m_effectiveWorldScalePercent = 100;
     m_windowed = false;
     m_allowRepeatingReinforcements = false;
     m_playSound = true;
@@ -118,8 +184,16 @@ cGame::cGame()
 
 void cGame::applySettings(GameSettings *gs)
 {
+    localization::setLanguage(gs->language);
     m_screenW = gs->screenW;
     m_screenH = gs->screenH;
+    m_renderScalePercent = gs->renderScalePercent;
+    m_worldScalePercent = gs->worldScalePercent;
+    m_effectiveWorldScalePercent = resolveWorldScalePercent(
+        m_worldScalePercent,
+        gs->screenH
+    );
+    m_commandBindings = gs->commandBindings;
     m_cameraDragMoveSpeed = gs->cameraDragMoveSpeed;
     m_cameraBorderOrKeyMoveSpeed = gs->cameraBorderOrKeyMoveSpeed;
     m_cameraEdgeMove = gs->cameraEdgeMove;
@@ -491,27 +565,8 @@ void cGame::think_audio()
     if (!game.m_playMusic) // no music enabled, so no need to think
         return;
 
-    // all this does is repeating music in the same theme.
-    if (m_musicType < 0)
-        return;
-
-    if (m_newMusicCountdown > 0) {
-        m_newMusicCountdown--;
-    }
-
-    if (m_newMusicCountdown == 0) {
-        m_soundPlayer->playMusic(m_newMusicSample);
-        m_newMusicCountdown--; // so we don't keep re-starting music
-    }
-
-    if (m_newMusicCountdown < 0) {
-        if (!m_soundPlayer->isMusicPlaying()) {
-            int desiredMusicType = m_musicType;
-            if (m_musicType == MUSIC_ATTACK) {
-                desiredMusicType = MUSIC_PEACE; // set back to peace
-            }
-            playMusicByType(desiredMusicType);
-        }
+    if (m_musicController) {
+        m_musicController->update();
     }
 }
 
@@ -598,8 +653,25 @@ void cGame::fadeOutOrBlitScreenBuffer() const
 void cGame::drawState()
 {
     if (m_fadeAction == eFadeAction::FADE_OUT) {
-        if (screenTexture) {
-            renderDrawer->renderSprite(screenTexture,0,0,(Uint8)m_fadeAlpha);
+        Texture *fadeTexture = m_hdPresentationFadeCaptureActive
+            ? m_hdPresentationTargets.fade.texture
+            : screenTexture;
+        if (fadeTexture) {
+            if (m_hdPresentationFadeCaptureActive) {
+                renderDrawer->renderStrechFullSprite(
+                    fadeTexture,
+                    cRectangle(0, 0, m_screenW, m_screenH),
+                    static_cast<Uint8>(m_fadeAlpha)
+                );
+            }
+            else {
+                renderDrawer->renderSprite(
+                    fadeTexture,
+                    0,
+                    0,
+                    static_cast<Uint8>(m_fadeAlpha)
+                );
+            }
         }
         return;
     }
@@ -612,6 +684,7 @@ void cGame::drawState()
     if (m_fadeAction == eFadeAction::FADE_IN && m_fadeAlpha>250) {
         m_fadeAlpha = kMaxAlpha;
         m_fadeAction = eFadeAction::FADE_NONE;
+        m_hdPresentationFadeCaptureActive = false;
     }
 
     switch (m_state) {
@@ -664,6 +737,11 @@ void cGame::run()
                 case SDL_KEYUP:
                     m_keyboard->handleEvent(event);
                     break;
+                case SDL_TEXTINPUT:
+                    if (m_currentState) {
+                        m_currentState->onTextInput(event.text.text);
+                    }
+                    break;
 
                 case SDL_MOUSEBUTTONDOWN:
                 case SDL_MOUSEBUTTONUP:
@@ -683,19 +761,151 @@ void cGame::run()
         updateMouseAndKeyboardState();
         updateGamePlaying();
 
-        renderDrawer->beginDrawingToTexture(actualRenderer);
+        const bool hdPresentationFrame = useHdPresentation();
+        Texture *frameTarget = hdPresentationFrame
+            ? ensureHdPresentationRenderTarget(false)
+            : actualRenderer;
+        renderDrawer->beginDrawingToTexture(frameTarget);
+        SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
         renderDrawer->renderClearToColor();
+        if (uiaudit::isEnabled()) {
+            uiaudit::beginFrame(*this);
+        }
         drawState(); // run game state, includes interaction + drawing
         transitionStateIfRequired();
         shakeScreenAndBlitBuffer();
 
         renderDrawer->endDrawingToTexture();
-        renderDrawer->renderSprite(actualRenderer, m_screenShake->getX(), m_screenShake->getY());
+        presentFrame(frameTarget, hdPresentationFrame);
+        if (uiaudit::isEnabled()) {
+            uiaudit::onFramePresented(*this);
+        }
         SDL_RenderPresent(renderer);
         m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
     }
 }
 
+bool cGame::useHdPresentation() const
+{
+    HdPresentationScene scene = HdPresentationScene::Legacy;
+    if (m_currentState != nullptr) {
+        scene = HdPresentationScene::Menu;
+    }
+    else if (m_state == GAME_PLAYING) {
+        scene = HdPresentationScene::Gameplay;
+    }
+    else if (
+        m_state == GAME_TELLHOUSE ||
+        m_state == GAME_BRIEFING ||
+        m_state == GAME_WINBRIEF ||
+        m_state == GAME_LOSEBRIEF
+    ) {
+        scene = HdPresentationScene::Mentat;
+    }
+    return shouldUsePhysicalHdPresentation(scene);
+}
+
+Texture *cGame::ensureHdPresentationRenderTarget(bool fadeTarget)
+{
+    int outputWidth = m_screenW;
+    int outputHeight = m_screenH;
+    if (SDL_GetRendererOutputSize(
+            renderer,
+            &outputWidth,
+            &outputHeight) < 0) {
+        outputWidth = m_screenW;
+        outputHeight = m_screenH;
+    }
+    outputWidth = std::max(1, outputWidth);
+    outputHeight = std::max(1, outputHeight);
+
+    auto &targetSlot = m_hdPresentationTargets.select(fadeTarget);
+    if (targetSlot.needsResize(outputWidth, outputHeight)) {
+        delete targetSlot.texture;
+        targetSlot.texture = nullptr;
+        targetSlot.setSize(outputWidth, outputHeight);
+        cLogger::getInstance()->log(
+            LOG_INFO,
+            COMP_SDL2,
+            "HD presentation renderer",
+            std::format(
+                "Presentation target : {}x{}",
+                outputWidth,
+                outputHeight
+            )
+        );
+    }
+
+    if (!targetSlot.texture) {
+        targetSlot.texture = renderDrawer->createRenderTargetTexture(
+            outputWidth,
+            outputHeight
+        );
+        SDL_SetTextureScaleMode(
+            targetSlot.texture->tex,
+            SDL_ScaleModeLinear
+        );
+    }
+    return targetSlot.texture;
+}
+
+void cGame::presentFrame(Texture *frameTarget, bool hdPresentationFrame)
+{
+    SDL_RenderSetLogicalSize(renderer, 0, 0);
+    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
+    SDL_RenderClear(renderer);
+    SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
+
+    if (hdPresentationFrame) {
+        const int shakeX = m_state == GAME_PLAYING
+            ? m_screenShake->getX()
+            : 0;
+        const int shakeY = m_state == GAME_PLAYING
+            ? m_screenShake->getY()
+            : 0;
+        const SDL_Rect destination = {
+            shakeX,
+            shakeY,
+            m_screenW,
+            m_screenH
+        };
+        SDL_SetTextureScaleMode(frameTarget->tex, SDL_ScaleModeLinear);
+        SDL_RenderCopy(renderer, frameTarget->tex, nullptr, &destination);
+        return;
+    }
+
+    renderDrawer->renderSprite(
+        frameTarget,
+        m_screenShake->getX(),
+        m_screenShake->getY()
+    );
+}
+
+void cGame::captureCurrentFrameForFade()
+{
+    Texture *frameTarget = m_hdPresentationTargets.frame.texture;
+    if (useHdPresentation() && frameTarget) {
+        Texture *fadeTarget = ensureHdPresentationRenderTarget(true);
+        renderDrawer->beginDrawingToTexture(fadeTarget);
+        SDL_RenderSetLogicalSize(renderer, 0, 0);
+        SDL_RenderCopy(
+            renderer,
+            frameTarget->tex,
+            nullptr,
+            nullptr
+        );
+        renderDrawer->endDrawingToTexture();
+        SDL_RenderSetLogicalSize(renderer, m_screenW, m_screenH);
+        m_hdPresentationFadeCaptureActive = true;
+        return;
+    }
+
+    renderDrawer->beginDrawingToTexture(screenTexture);
+    SDL_RenderCopy(renderer, actualRenderer->tex, nullptr, nullptr);
+    renderDrawer->endDrawingToTexture();
+    m_hdPresentationFadeCaptureActive = false;
+}
+
 void cGame::shakeScreen(int duration)
 {
     m_screenShake->shake(duration);
@@ -759,6 +969,23 @@ void cGame::shutdown()
         players[i].destroyAllegroBitmaps();
     }
 
+    delete m_hdPresentationTargets.fade.texture;
+    m_hdPresentationTargets.fade.texture = nullptr;
+    delete m_hdPresentationTargets.frame.texture;
+    m_hdPresentationTargets.frame.texture = nullptr;
+    delete m_hdVictoryRu;
+    m_hdVictoryRu = nullptr;
+    delete m_hdVictoryEn;
+    m_hdVictoryEn = nullptr;
+    delete m_hdDefeatRu;
+    m_hdDefeatRu = nullptr;
+    delete m_hdDefeatEn;
+    m_hdDefeatEn = nullptr;
+    delete screenTexture;
+    screenTexture = nullptr;
+    delete actualRenderer;
+    actualRenderer = nullptr;
+
     delete renderDrawer;
     delete m_mouse;
     delete m_keyboard;
@@ -798,6 +1025,18 @@ bool cGame::setupGame()
     game.init(); // Must be first! (loads game.ini file at the end, which is required before going on...)
 
     const std::string &gameDir = settings->getStringValue(SECTION_SETTINGS, "GameDir");
+    const std::string graphicsSection = "HD4_DATAFILE";
+    logger->log(
+        LOG_INFO,
+        COMP_INIT,
+        "Graphics",
+        std::format(
+            "{}x assets, section [{}]",
+            cGame::kHdAssetDensity,
+            graphicsSection
+        )
+    );
+
     std::unique_ptr<cFileValidator> settingsValidator = std::make_unique<cFileValidator>(gameDir);
     {
         std::map<eGameDirFileName, std::string> m_transfertMap;
@@ -805,10 +1044,14 @@ bool cGame::setupGame()
         m_transfertMap[eGameDirFileName::BENEGESS] = settings->getStringValue("FONT", "BENEGESS");
         m_transfertMap[eGameDirFileName::SMALL] = settings->getStringValue("FONT", "SMALL");
 
-        m_transfertMap[eGameDirFileName::GFXDATA] = settings->getStringValue("DATAFILE", "GFXDATA");
-        m_transfertMap[eGameDirFileName::GFXINTER] = settings->getStringValue("DATAFILE", "GFXINTER");
-        m_transfertMap[eGameDirFileName::GFXWORLD] = settings->getStringValue("DATAFILE", "GFXWORLD");
-        m_transfertMap[eGameDirFileName::GFXMENTAT] = settings->getStringValue("DATAFILE", "GFXMENTAT");
+        m_transfertMap[eGameDirFileName::GFXDATA] =
+            graphicsDataFileName(*settings, graphicsSection, "GFXDATA", kHdAssetDensity);
+        m_transfertMap[eGameDirFileName::GFXINTER] =
+            graphicsDataFileName(*settings, graphicsSection, "GFXINTER", kHdAssetDensity);
+        m_transfertMap[eGameDirFileName::GFXWORLD] =
+            graphicsDataFileName(*settings, graphicsSection, "GFXWORLD", kHdAssetDensity);
+        m_transfertMap[eGameDirFileName::GFXMENTAT] =
+            graphicsDataFileName(*settings, graphicsSection, "GFXMENTAT", kHdAssetDensity);
         m_transfertMap[eGameDirFileName::GFXAUDIO] = settings->getStringValue("DATAFILE", "GFXAUDIO");
         settingsValidator->addResources(std::move(m_transfertMap));
     }
@@ -829,18 +1072,28 @@ bool cGame::setupGame()
     m_keyboard = new cKeyboard();
     logger->log(LOG_INFO, COMP_INIT, "Initializing Keyboard", "install_keyboard()", OUTC_SUCCESS);
 
-    m_Screen = std::make_unique<cScreenInit>(m_screenW, m_screenH, title);
+    m_Screen = std::make_unique<cScreenInit>(
+        m_screenW,
+        m_screenH,
+        m_renderScalePercent,
+        title
+    );
     if (!m_windowed) {
         m_Screen->setFullScreenMode();
     }
 
     m_screenW = m_Screen->Width();
     m_screenH = m_Screen->Height();
+    cSideBar::configureLayout(true, m_screenW);
     window = m_Screen->getWindows();
     renderer = m_Screen->getRenderer();
 
     // create ressources from scratch
-    context = std::make_unique<ContextCreator>(renderer, settingsValidator.get());
+    context = std::make_unique<ContextCreator>(
+        renderer,
+        settingsValidator.get(),
+        kHdAssetDensity
+    );
     // share Graphics to all class what use ctx !
     ctx->setGraphicsContext(context->createGraphicsContext());
     // share Text to all class what use ctx !
@@ -860,6 +1113,45 @@ bool cGame::setupGame()
         m_soundPlayer->setMusicEnabled(false);
     }
 
+    // main() switches the working directory to the executable directory before
+    // settings are loaded. GameDir points at the data pack directory, while
+    // user-owned music lives next to d2tm.exe.
+    const std::filesystem::path resolvedGameDirectory = std::filesystem::current_path();
+    const std::array<std::filesystem::path, 8> musicDirectories{
+        "music/gameplay",
+        "music/menu",
+        "music/conquest",
+        "music/briefing/atreides",
+        "music/briefing/harkonnen",
+        "music/briefing/ordos",
+        "music/victory",
+        "music/defeat"
+    };
+    for (const auto &directory : musicDirectories) {
+        std::error_code createError;
+        std::filesystem::create_directories(resolvedGameDirectory / directory, createError);
+        if (createError) {
+            logger->log(
+                LOG_WARN,
+                COMP_SOUND,
+                "Music directory",
+                std::format("Could not create {}: {}", (resolvedGameDirectory / directory).string(), createError.message()));
+        }
+    }
+    m_musicController = std::make_unique<MusicController>(m_soundPlayer, resolvedGameDirectory);
+    m_musicController->configure(
+        MusicCategory::Gameplay,
+        "music/gameplay",
+        {MIDI_BUILDING01, MIDI_BUILDING02, MIDI_BUILDING03, MIDI_BUILDING04, MIDI_BUILDING05,
+         MIDI_BUILDING06, MIDI_BUILDING07, MIDI_BUILDING08, MIDI_BUILDING09});
+    m_musicController->configure(MusicCategory::Menu, "music/menu", {MIDI_MENU});
+    m_musicController->configure(MusicCategory::Conquest, "music/conquest", {MIDI_SCENARIO});
+    m_musicController->configure(MusicCategory::BriefingAtreides, "music/briefing/atreides", {MIDI_MENTAT_ATR});
+    m_musicController->configure(MusicCategory::BriefingHarkonnen, "music/briefing/harkonnen", {MIDI_MENTAT_HAR});
+    m_musicController->configure(MusicCategory::BriefingOrdos, "music/briefing/ordos", {MIDI_MENTAT_ORD});
+    m_musicController->configure(MusicCategory::Victory, "music/victory", {MIDI_WIN01, MIDI_WIN02, MIDI_WIN03});
+    m_musicController->configure(MusicCategory::Defeat, "music/defeat", {MIDI_LOSE01, MIDI_LOSE02, MIDI_LOSE03});
+
     // do it here, because it depends on fonts to be loaded
     m_mouse = new cMouse(ctx.get());
 
@@ -877,7 +1169,11 @@ bool cGame::setupGame()
     /*** Data files ***/
 
     // load datafiles
-    gfxdata = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXDATA));
+    gfxdata = std::make_shared<Graphics>(
+        renderer,
+        settingsValidator->getFullName(eGameDirFileName::GFXDATA),
+        getGraphicsDensity()
+    );
     if (gfxdata == nullptr) {
         logger->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXDATA), OUTC_FAILED);
         return false;
@@ -1145,6 +1441,7 @@ void cGame::setState(int newState)
                 newStatePtr = new cOptionsState(*this, ctx.get(), m_state);
             }
             else if (newState == GAME_PLAYING) {
+                playMusicByTypeForStateTransition(MUSIC_PEACE);
                 if (m_state == GAME_OPTIONS) {
                     m_timeManager->restartTimer();
                     takeBackGroundScreen();
@@ -1663,7 +1960,7 @@ void cGame::saveBmpScreenToDisk()
     // shows a message in-game, would be even better to have this 'globally' (not depending on state), kind of like
     // a Quake console perhaps?
     cPlayer &humanPlayer = players[HUMAN];
-    humanPlayer.addNotification(std::format("Screenshot saved {}.", filename), eNotificationType::NEUTRAL);
+    humanPlayer.addNotification(localization::format("Screenshot saved: {}.", "Снимок экрана сохранён: {}.", filename), eNotificationType::NEUTRAL);
 
     m_screenshot++;
 }
@@ -1742,6 +2039,34 @@ void cGame::onKeyPressedGamePlaying(const cKeyboardEvent &event)
 {
     cPlayer &humanPlayer = players[HUMAN];
 
+    if (event.hasKey(SDL_SCANCODE_F5) &&
+            !event.hasKey(SDL_SCANCODE_LSHIFT) &&
+            !event.hasKey(SDL_SCANCODE_RSHIFT)) {
+        std::string error;
+        if (saveQuickGame(error)) {
+            humanPlayer.addNotification(
+                localization::text("Game saved.", "Игра сохранена."),
+                eNotificationType::NEUTRAL
+            );
+        }
+        else {
+            humanPlayer.addNotification(error, eNotificationType::BAD);
+        }
+    }
+
+    if (event.hasKey(SDL_SCANCODE_F9)) {
+        std::string error;
+        if (loadQuickGame(error)) {
+            players[HUMAN].addNotification(
+                localization::text("Game loaded.", "Игра загружена."),
+                eNotificationType::NEUTRAL
+            );
+        }
+        else {
+            humanPlayer.addNotification(error, eNotificationType::BAD);
+        }
+    }
+
     if (event.hasKey(SDL_SCANCODE_F)) {
         m_drawFps = false;
     }
@@ -1750,7 +2075,7 @@ void cGame::onKeyPressedGamePlaying(const cKeyboardEvent &event)
         m_drawTime = ! m_drawTime;
     }
 
-    if (event.hasKey(SDL_SCANCODE_D)) {
+    if (event.hasAssignedKey(m_commandBindings.deploy)) {
         for (int i = 0; i < MAX_UNITS; i++) {
             cUnit &u = unit[i];
             if (u.bSelected && u.iType == MCV && u.getPlayer()->isHuman()) {
@@ -1766,16 +2091,25 @@ void cGame::onKeyPressedGamePlaying(const cKeyboardEvent &event)
 
     if (event.hasKey(SDL_SCANCODE_M) || event.hasKey(SDL_SCANCODE_MUTE)) {
         game.m_playMusic = !game.m_playMusic;
+        m_soundPlayer->setMusicEnabled(game.m_playMusic);
         if (!game.m_playMusic) {
-            m_soundPlayer->stopMusic();
-            humanPlayer.addNotification("Music muted", eNotificationType::NEUTRAL);
+            if (m_musicController) m_musicController->stop();
+            humanPlayer.addNotification(localization::text("Music off", "Музыка выключена"), eNotificationType::NEUTRAL);
         }
         else {
-            m_soundPlayer->playMusic(m_newMusicSample);
-            humanPlayer.addNotification("Music enabled", eNotificationType::NEUTRAL);
+            if (m_musicController) m_musicController->replayCurrent();
+            humanPlayer.addNotification(localization::text("Music on", "Музыка включена"), eNotificationType::NEUTRAL);
         }
     }
 
+    if (event.hasKey(SDL_SCANCODE_LEFTBRACKET)) {
+        playPreviousGameplayTrack();
+    }
+
+    if (event.hasKey(SDL_SCANCODE_RIGHTBRACKET)) {
+        playNextGameplayTrack();
+    }
+
     if (event.hasKey(SDL_SCANCODE_O) || event.hasKey(SDL_SCANCODE_VOLUMEDOWN)) {
         m_soundPlayer->changeMusicVolume(-10);
     }
@@ -1820,7 +2154,7 @@ void cGame::onKeyPressedGamePlaying(const cKeyboardEvent &event)
         // depending on type of structure, a key could mean a different thing?
         // so, kind of like event.hasKey(selectedStructure->KeyForDeploying()) ?
         // and then perform?
-        if (event.hasKey(SDL_SCANCODE_D)) {
+        if (event.hasAssignedKey(m_commandBindings.release)) {
             if (selectedStructure->getType() == REPAIR) { // this should be done differently?
                 s_GameEvent e{
                     .eventType = eGameEventType::GAME_EVENT_DEPLOY_UNIT,
@@ -1855,13 +2189,13 @@ void cGame::playSoundWithDistance(int sampleId, int iDistance)
 
     // zoom factor influences distance we can 'hear'. The closer up, the less max distance. Unzoomed, this is half the map.
     // where when unit is at half map, we can hear it only a bit.
-    float maxDistance = mapCamera->divideByZoomLevel(global_map.getMaxDistanceInPixels() / 2);
+    float maxDistance = soundMaxDistance(global_map.getMaxDistanceInPixels(), mapCamera->getZoomLevel(), getWorldScaleFactor());
     float distanceNormalized = 1.0 - (iDistance / maxDistance);
 
     float volume = m_soundPlayer->getMaxVolume() * distanceNormalized;
 
     // zoom factor influences volume (more zoomed in means louder)
-    float volumeFactor = mapCamera->factorZoomLevel(0.7f);
+    float volumeFactor = soundVolumeFactor(mapCamera->getZoomLevel(), getWorldScaleFactor());
     int iVolFactored = volumeFactor * volume;
 
     if (game.isDebugMode()) {
@@ -1880,10 +2214,7 @@ void cGame::playVoice(int sampleId, int playerId)
 
 void cGame::playMusicByTypeForStateTransition(int iType)
 {
-    if (m_musicType != iType) {
-        m_newMusicCountdown = 0;
-        playMusicByType(iType, HUMAN, false);
-    }
+    playMusicByType(iType, HUMAN, false);
 }
 
 bool cGame::playMusicByType(int iType, int playerId, bool triggerWithVoice)
@@ -1895,13 +2226,12 @@ bool cGame::playMusicByType(int iType, int playerId, bool triggerWithVoice)
 
     logbook(std::format("cGame::playMusicByType - iType = {}. playerId = {}, triggerWithVoice = {}", iType, playerId, triggerWithVoice));
 
-    if (triggerWithVoice) {
-        if (iType == m_musicType) {
-            logbook(std::format("m_musicType = {}, iType is {}, so bailing", m_musicType, iType));
-            return false;
-        }
+    // Attack detection no longer owns the music state. Legacy callers are folded
+    // into the gameplay pool and cannot interrupt the current composition.
+    if (iType == MUSIC_ATTACK) {
+        iType = MUSIC_PEACE;
     }
-
+    const bool repeatedCategory = m_musicType == iType;
     m_musicType = iType;
     logbook(std::format("m_musicType = {}", m_musicType));
 
@@ -1909,67 +2239,37 @@ bool cGame::playMusicByType(int iType, int playerId, bool triggerWithVoice)
         return false; // todo: have a 'no-sound soundplayer' instead of doing this :/
     }
 
-    if (m_newMusicCountdown > 0) {
-        // do not interfere with previous 'change to music' thing?
-        return false;
+    if (m_musicController) {
+        const MusicCategory category = musicCategoryFor(iType, players[HUMAN].getHouse());
+        // Keep the current track when adjacent screens use the same category.
+        m_musicController->activate(
+            category,
+            shouldAdvanceRepeatedMusicCategory(
+                repeatedCategory,
+                isState(GAME_PLAYING)
+            )
+        );
     }
+    return true;
+}
 
-
-    int sampleId = MIDI_MENU;
-    if (iType == MUSIC_WIN) {
-        sampleId = MIDI_WIN01 + RNG::rnd(3);
-    }
-    else if (iType == MUSIC_LOSE) {
-        sampleId = MIDI_LOSE01 + RNG::rnd(6);
-    }
-    else if (iType == MUSIC_ATTACK) {
-        sampleId = MIDI_ATTACK01 + RNG::rnd(6);
-    }
-    else if (iType == MUSIC_PEACE) {
-        sampleId = MIDI_BUILDING01 + RNG::rnd(9);
-    }
-    else if (iType == MUSIC_MENU) {
-        sampleId = MIDI_MENU;
-    }
-    else if (iType == MUSIC_CONQUEST) {
-        sampleId = MIDI_SCENARIO;
-    }
-    else if (iType == MUSIC_BRIEFING) {
-        int houseIndex = players[HUMAN].getHouse();
-        if (houseIndex == ATREIDES) {
-            sampleId = MIDI_MENTAT_ATR;
-        }
-        else if (houseIndex == HARKONNEN) {
-            sampleId = MIDI_MENTAT_HAR;
-        }
-        else if (houseIndex == ORDOS) {
-            sampleId = MIDI_MENTAT_ORD;
-        }
-        else {
-            assert(false && "Undefined house.");
-        }
-    }
-    else {
-        assert(false && "Undefined music type.");
+void cGame::playPreviousGameplayTrack()
+{
+    if (m_playMusic && isState(GAME_PLAYING) && m_musicController) {
+        m_musicController->previous();
     }
+}
 
-    if (triggerWithVoice) {
-        // voice triggered music (ie "Enemy unit approaching"), so have music stop a bit
-        if (isState(GAME_PLAYING)) {
-            m_newMusicCountdown = 400; // wait a bit longer
-        }
-        else {
-            m_newMusicCountdown = 0;
-        }
-        m_soundPlayer->stopMusic();
-    }
-    else {
-        // instant switch
-        m_newMusicCountdown = 0;
+void cGame::playNextGameplayTrack()
+{
+    if (m_playMusic && isState(GAME_PLAYING) && m_musicController) {
+        m_musicController->next();
     }
+}
 
-    m_newMusicSample = sampleId;
-    return true;
+std::string cGame::getCurrentMusicTrackName() const
+{
+    return m_musicController ? m_musicController->currentDisplayName() : std::string{};
 }
 
 int cGame::getMaxVolume()
@@ -2136,7 +2436,7 @@ void cGame::onKeyDownDebugMode(const cKeyboardEvent &event)
     }
     else {
         // REVEAL MAP
-        if (event.hasKey(SDL_SCANCODE_F5)) {
+        if (event.hasKey(SDL_SCANCODE_F7)) {
             for (int i = 0; i < AI_WORM; i++) {
                 global_map.clear_all(i);
             }
@@ -2227,22 +2527,79 @@ void cGame::initiateFadingOut()
     m_fadeAction = eFadeAction::FADE_OUT; // fade out
     m_fadeAlpha = 250;
 
-    renderDrawer->beginDrawingToTexture(screenTexture);
-    SDL_RenderCopy(renderer, actualRenderer->tex,nullptr, nullptr);
-    renderDrawer->endDrawingToTexture();
+    captureCurrentFrameForFade();
+}
+
+Texture *cGame::getHdOutcomeTexture(bool victory)
+{
+    const bool english = localization::isEnglish();
+    Texture *&texture = victory
+        ? (english ? m_hdVictoryEn : m_hdVictoryRu)
+        : (english ? m_hdDefeatEn : m_hdDefeatRu);
+    if (!texture) {
+        const char *fileName = victory
+            ? localization::text(
+                "outcome_victory_en.png",
+                "outcome_victory_ru.png"
+            )
+            : localization::text(
+                "outcome_defeat_en.png",
+                "outcome_defeat_ru.png"
+            );
+        texture = loadHdUiTexture(
+            fileName,
+            getGraphicsDensity(),
+            victory ? "Victory screen" : "Defeat screen"
+        );
+    }
+    return texture;
 }
 
-// this shows the you have lost bmp at screen, after mouse press the mentat debriefing state will begin
-void cGame::drawStateLosing()
+void cGame::drawOutcomeScreen(bool victory)
 {
-    if (screenTexture)
-        renderDrawer->renderSprite(screenTexture,0,0);
+    Texture *texture = getHdOutcomeTexture(victory);
+
+    if (texture) {
+        auto *textDrawer = ctx->getTextContext()->getMenuTextDrawer();
+        const std::string prompt = localization::text(
+            "Click to continue",
+            "Нажмите, чтобы продолжить"
+        );
+        const OutcomeScreenLayout layout = calculateOutcomeScreenLayout(
+            m_screenW,
+            m_screenH,
+            texture->pixelW,
+            texture->pixelH,
+            textDrawer->getTextLength(prompt)
+        );
+        renderDrawer->renderStrechFullSprite(texture, layout.image);
+        const Color textColor{255, 224, 164, 255};
+        textDrawer->drawTextScaledCenteredInBox(
+            prompt,
+            layout.prompt,
+            layout.promptTextScale,
+            textColor
+        );
+    }
+    else {
+        if (screenTexture) {
+            renderDrawer->renderSprite(screenTexture, 0, 0);
+        }
+        Texture *fallback = ctx->getGraphicsContext()->gfxinter->getTexture(
+            victory ? BMP_WINNING : BMP_LOSING
+        );
+        const int x = (m_screenW - fallback->w) / 2;
+        const int y = (m_screenH - fallback->h) / 2;
+        renderDrawer->renderSprite(fallback, x, y);
+    }
 
-    auto tex = ctx->getGraphicsContext()->gfxinter->getTexture(BMP_LOSING);
-    int posW = (m_screenW-tex->w)/2;
-    int posH = (m_screenH-tex->h)/2;
-    renderDrawer->renderSprite(tex,posW, posH);
     renderDrawer->renderSprite(gfxdata->getTexture(MOUSE_NORMAL), m_mouse->getX(), m_mouse->getY());
+}
+
+// this shows the you have lost bmp at screen, after mouse press the mentat debriefing state will begin
+void cGame::drawStateLosing()
+{
+    drawOutcomeScreen(false);
 
     if (m_mouse->isLeftButtonClicked()) {
         m_state = GAME_LOSEBRIEF;
@@ -2257,14 +2614,7 @@ void cGame::drawStateLosing()
 // this shows the you have won bmp at screen, after mouse press the mentat debriefing state will begin
 void cGame::drawStateWinning()
 {
-    if (screenTexture)
-        renderDrawer->renderSprite(screenTexture,0,0);
-        
-    auto tex = ctx->getGraphicsContext()->gfxinter->getTexture(BMP_WINNING);
-    int posW = (m_screenW-tex->w)/2;
-    int posH = (m_screenH-tex->h)/2;
-    renderDrawer->renderSprite(tex,posW, posH);
-    renderDrawer->renderSprite(gfxdata->getTexture(MOUSE_NORMAL), m_mouse->getX(), m_mouse->getY());
+    drawOutcomeScreen(true);
 
     if (m_mouse->isLeftButtonClicked()) {
         // Mentat will be happy, after that enter "Select your next Conquest"
@@ -2279,12 +2629,25 @@ void cGame::drawStateWinning()
 
 void cGame::takeBackGroundScreen()
 {
-    renderDrawer->beginDrawingToTexture(screenTexture);
-    SDL_RenderCopy(renderer, actualRenderer->tex,nullptr, nullptr);
-    renderDrawer->endDrawingToTexture();
+    captureCurrentFrameForFade();
+}
+
+bool cGame::saveQuickGame(std::string &errorMessage)
+{
+    return SaveGameManager::saveQuickGame(*this, errorMessage);
+}
+
+bool cGame::loadQuickGame(std::string &errorMessage)
+{
+    return SaveGameManager::loadQuickGame(*this, errorMessage);
+}
+
+bool cGame::hasQuickSave() const
+{
+    return SaveGameManager::hasQuickSave();
 }
 
 std::shared_ptr<s_TerrainInfo> cGame::getTerrainInfo() const
 {
     return m_TerrainInfo;
-}
\ No newline at end of file
+}


=== FORK1: src/controls/cGameControlsContext.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/cGameControlsContext.cpp
stdout:
diff --git a/src/controls/cGameControlsContext.cpp b/src/controls/cGameControlsContext.cpp
index b7479ffd..daa03e14 100644
--- a/src/controls/cGameControlsContext.cpp
+++ b/src/controls/cGameControlsContext.cpp
@@ -1,5 +1,7 @@
 #include "cGameControlsContext.h"
 
+#include "player/cPlayer.h"
+
 #include "data/gfxdata.h"
 #include "d2tmc.h"
 #include "managers/cDrawManager.h"
@@ -49,6 +51,12 @@ void cGameControlsContext::updateMouseCell(const cPoint &coords)
         return;
     }
 
+    if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
+        m_mouseCell = MOUSECELL_COMMAND_BAR;
+        m_mouseOnBattleField = false;
+        return;
+    }
+
     if (drawManager->getMiniMapDrawer()->isMouseOver()) {
         m_mouseCell = MOUSECELL_MINIMAP; // on minimap
         m_mouseOnBattleField = false;
@@ -64,11 +72,31 @@ void cGameControlsContext::updateMouseCell(const cPoint &coords)
     m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
 }
 
+void cGameControlsContext::activateMoveCommand()
+{
+    if (m_player->getSelectedUnits().empty()) return;
+    setMouseState(MOUSESTATE_UNITS_SELECTED);
+    m_mouseUnitsSelectedState->setCommandState(SELECTED_STATE_MOVE);
+}
+
+void cGameControlsContext::activateAttackCommand()
+{
+    if (m_player->getSelectedUnits().empty()) return;
+    setMouseState(MOUSESTATE_UNITS_SELECTED);
+    m_mouseUnitsSelectedState->setCommandState(SELECTED_STATE_FORCE_ATTACK);
+}
+
+void cGameControlsContext::activateRallyPointCommand()
+{
+    cAbstractStructure *selected = m_player->getSelectedStructure();
+    if (!selected || !selected->belongsTo(m_player) || !selected->canSpawnUnits()) return;
+    setMouseState(MOUSESTATE_SELECT);
+    m_mouseNormalState->setRallyPointCommandMode();
+}
+
 int cGameControlsContext::getMouseCellFromScreen(int mouseX, int mouseY) const
 {
-    int absMapX = mapCamera->getAbsMapMouseX(mouseX);
-    int absMapY = mapCamera->getAbsMapMouseY(mouseY);
-    return mapCamera->getCellFromAbsolutePosition(absMapX, absMapY);
+    return mapCamera->getCellFromWindowPosition(mouseX, mouseY);
 }
 
 void cGameControlsContext::determineToolTip()
@@ -164,6 +192,14 @@ void cGameControlsContext::onMouseMovedTo(const s_MouseEvent &event)
     m_prevTickMouseAtBattleField = mouseOnBattleField;
 }
 
+void cGameControlsContext::refreshMouseHover()
+{
+    s_MouseEvent event;
+    event.eventType = eMouseEventType::MOUSE_MOVED_TO;
+    event.coords = cPoint(m_mouse->getX(), m_mouse->getY());
+    onNotifyMouseEvent(event);
+}
+
 void cGameControlsContext::onNotifyMouseEvent(const s_MouseEvent &event)
 {
     if (event.eventType == eMouseEventType::MOUSE_MOVED_TO) {


=== FORK1: src/controls/cMouse.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/cMouse.cpp
stdout:
(пустой stdout)


=== Точные результаты фильтрации трёх файлов ===
Фильтр проверяет только строки hunk с префиксом пробела, + или -; заголовки @@ и служебные строки diff не проверяются. Сопоставление буквальное, с учётом регистра. Подстроки: HudLayout, sidebarWidth, TopBarHeight, battlefield, Battlefield. Для каждого файла полный исходный stdout находится в его блоке FORK1 выше.

Файл: src/cGame_logic.cpp
Команда фильтрации: `/srv/dune/venv/bin/python .tmp/p5cr2/collect_source_outputs.py` (функция `selected_hunks`; вход — полный stdout git diff выше).
Выбрано участков @@: 0
stdout выбранных участков:
(пустой stdout)

Файл: src/controls/cGameControlsContext.cpp
Команда фильтрации: `/srv/dune/venv/bin/python .tmp/p5cr2/collect_source_outputs.py` (функция `selected_hunks`; вход — полный stdout git diff выше).
Выбрано участков @@: 0
stdout выбранных участков:
(пустой stdout)

Файл: src/controls/cMouse.cpp
Команда фильтрации: `/srv/dune/venv/bin/python .tmp/p5cr2/collect_source_outputs.py` (функция `selected_hunks`; вход — полный stdout git diff выше).
Выбрано участков @@: 0
stdout выбранных участков:
(пустой stdout)


=== PORT относительно BASE: полные diff для исходных путей и перемещённой камеры ===
Эти полные stdout позволяют проверить строки таблицы о пересечениях и отсутствии пересечений. Для камеры включены исходные пути `src/map/...` и перемещённые пути `src/gameobjects/map/...`.


=== PORT: src/managers/cDrawManager.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/managers/cDrawManager.cpp
stdout:
diff --git a/src/managers/cDrawManager.cpp b/src/managers/cDrawManager.cpp
index 7c0e45a9..78225e92 100644
--- a/src/managers/cDrawManager.cpp
+++ b/src/managers/cDrawManager.cpp
@@ -1,86 +1,168 @@
+/**
+ * @file cDrawManager.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #include "cDrawManager.h"
 
 #include "controls/cGameControlsContext.h"
-#include "d2tmc.h"
+#include "gameobjects/particles/cParticles.h"
+#include "gameobjects/structures/cStructures.h"
+#include "game/GameStateTransition.hpp"
+#include "controls/cMouse.h"
+#include "utils/cRectangle.h"
+#include "include/eGameState.h"
+#include "include/sGameServices.h"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
 #include "gameobjects/particles/cParticle.h"
 #include "gameobjects/projectiles/bullet.h"
-#include "player/cPlayer.h"
+#include "gameobjects/projectiles/cBullets.h"
+#include "gameobjects/players/cPlayer.h"
+#include "gameobjects/players/cPlayers.h"
+#include "gameobjects/units/cUnits.h"
 #include "utils/Graphics.hpp"
+#include "utils/texture_utils.h"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
-
-#include <SDL2/SDL.h>
-#include <cassert>
-
-cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer) :
-    m_sidebarDrawer(ctx, thePlayer),
-    m_creditsDrawer(ctx, thePlayer),
-    m_orderDrawer(ctx, thePlayer),
-    m_mapDrawer(&global_map, thePlayer, mapCamera),
-    miniMapDrawer(ctx, &global_map, thePlayer, mapCamera),
-    m_particleDrawer(),
-    m_messageDrawer(ctx),
-    m_placeitDrawer(thePlayer),
-    m_structureDrawer(ctx),
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "gameobjects/map/cMapCamera.h"
+#include "gameobjects/map/cMap.h"
+#include "drawers/cSideBarDrawer.h"
+
+#include <SDL3/SDL.h>
+#include "include/cAssert.h"
+#include "context/TextContext.hpp"
+#include "drawers/CreditsDrawer.h"
+#include "drawers/cMapDrawer.h"
+#include "drawers/cMessageDrawer.h"
+#include "drawers/cMiniMapDrawer.h"
+#include "drawers/cMouseDrawer.h"
+#include "drawers/cOrderDrawer.h"
+#include "drawers/cParticleDrawer.h"
+#include "drawers/cPlaceItDrawer.h"
+#include "game/cGameSettings.h"
+#include "include/Texture.hpp"
+
+cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer, sGameServices *services) :
     m_sidebarColor(Color{214, 149, 20,255}),
     m_player(thePlayer),
+    m_ctx(ctx),
     m_textDrawer(ctx->getTextContext()->getGameTextDrawer()),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_gfxdata(ctx->getGraphicsContext()->gfxdata.get()),
+    m_stateTransitions(services->stateTransitions),
+    m_mouse(services->mouse),
+    m_mapViewport(services->mapViewport),
+    m_objects(services->objects),
+    m_mapCamera(services->mapCamera),
+    m_gameSettings(services->settings),
+    m_structureUtils(services->structureUtils),
+    m_services(services)
+{
+    d2tm_assert(m_player!=nullptr);
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(m_textDrawer != nullptr);
+    d2tm_assert(m_sdlDrawer != nullptr);
+    d2tm_assert(m_gfxdata != nullptr);
+    d2tm_assert(m_gfxinter != nullptr);
+    d2tm_assert(m_stateTransitions != nullptr);
+    d2tm_assert(m_objects != nullptr);
+    d2tm_assert(m_mapCamera != nullptr);
+    d2tm_assert(m_gameSettings != nullptr);
+    this->reset();
+}
+
+void cDrawManager::reset()
 {
-    assert(thePlayer);
-    btnOptions = thePlayer->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BTN_OPTIONS), TransparentColorIndex
-    );
-    m_mouseDrawer = new cMouseDrawer(thePlayer, ctx->getTextContext()->getSmallTextDrawer());
+    m_sidebarColor = Color{214, 149, 20,255};
+    m_sidebarDrawer = std::make_unique<cSideBarDrawer>(m_ctx, m_player, m_services);
+    m_creditsDrawer = std::make_unique<CreditsDrawer>(m_ctx, m_gameSettings, m_player);
+    m_orderDrawer = std::make_unique<cOrderDrawer>(m_ctx, m_player, m_services);
+    m_mapDrawer = std::make_unique<cMapDrawer>(m_ctx, m_objects->getMap(), m_player, m_mapCamera, m_services);
+    m_miniMapDrawer = std::make_unique<cMiniMapDrawer>(m_ctx, m_gameSettings, m_objects->getMap(), m_player, m_mapCamera);
+    m_particleDrawer = std::make_unique<cParticleDrawer>();
+    m_messageDrawer = std::make_unique<cMessageDrawer>(m_ctx, m_services);
+    m_placeitDrawer = std::make_unique<cPlaceItDrawer>(m_ctx, m_player, m_structureUtils);
+    m_structureDrawer = std::make_unique<cStructureDrawer>(m_ctx, m_player, m_structureUtils);
+    m_btnOptions.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_ctx->getSDLDrawer(),m_player, m_gfxinter->getSurface(BTN_OPTIONS), TransparentColorIndex, m_gfxinter->getDensity()));
+    m_mouseDrawer = std::make_unique<cMouseDrawer>(m_player, m_ctx->getTextContext()->getSmallTextDrawer());
+
+    m_sidebarDrawer->serviceInit(m_services);
+    m_creditsDrawer->serviceInit(m_services);
+    m_orderDrawer->serviceInit(m_services);
+    m_mapDrawer->serviceInit(m_services);
+    m_miniMapDrawer->serviceInit(m_services);
+    m_particleDrawer->serviceInit(m_services);
+    m_messageDrawer->serviceInit(m_services);
+    m_placeitDrawer->serviceInit(m_services);
+    m_structureDrawer->serviceInit(m_services);
+    m_mouseDrawer->serviceInit(m_services);
 }
 
 cDrawManager::~cDrawManager()
 {
-    if (btnOptions) {
-        delete btnOptions;
-    }
 }
 
 void cDrawManager::drawCombatState()
 {
     // MAP
-    renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), game.m_screenH);
-    m_mapDrawer.drawTerrain();
+    m_sdlDrawer->setClippingFor(0, cSideBar::TopBarHeight, m_mapCamera->getWindowWidth(), m_gameSettings->getScreenH());
+    m_mapDrawer->drawTerrain();
 
-    m_structureDrawer.drawStructuresFirstLayer();
+    m_structureDrawer->drawStructuresFirstLayer();
 
     // draw layer 1 (beneath units, on top of terrain)
-    m_particleDrawer.determineParticlesToDraw(*game.m_mapViewport);
-    m_particleDrawer.drawLowerLayer();
+    m_particleDrawer->determineParticlesToDraw(*m_mapViewport);
+    m_particleDrawer->drawLowerLayer();
+
+    m_objects->getMap()->draw_units();
+
+    m_objects->getMap()->draw_bullets();
 
-    global_map.draw_units();
+    m_structureDrawer->drawStructuresSecondLayer();
 
-    global_map.draw_bullets();
+    m_objects->getMap()->draw_units_2nd();
 
-    m_structureDrawer.drawStructuresSecondLayer();
+    m_particleDrawer->drawTopLayer();
 
-    global_map.draw_units_2nd();
+    // what was last seen of fogged cells covers anything live in the fog
+    m_mapDrawer->drawRememberedTerrain();
+    m_structureDrawer->drawRememberedStructures();
+    m_objects->getMap()->drawRememberedUnits();
 
-    m_particleDrawer.drawTopLayer();
-    m_structureDrawer.drawStructuresHealthBars();
+    m_structureDrawer->drawStructuresHealthBars();
 
-    m_mapDrawer.drawShroud();
+    m_mapDrawer->drawShroud();
+
+    // after the shroud: an attacker on a never explored cell would otherwise be painted over in black
+    m_objects->getMap()->drawRevealedUnitsInFog();
 
     drawRallyPoint();
 
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->resetClippingFor();
 
     // GUI
     drawSidebar();
 
     drawOptionBar();
 
-    renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
+    m_sdlDrawer->setClippingFor(0, cSideBar::TopBarHeight, m_mapCamera->getWindowWidth(), m_mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
     drawStructurePlacing();
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->resetClippingFor();
 
     drawTopBarBackground();
     drawCredits();
@@ -88,100 +170,95 @@ void cDrawManager::drawCombatState()
     // THE MESSAGE
     drawMessage();
 
-    drawNotifications();
-
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->resetClippingFor();
 
-    if (game.m_drawUsages) {
+    if (m_gameSettings->isDrawUsages()) {
         drawDebugInfoUsages();
-        m_particleDrawer.drawDebugInfo(m_textDrawer);
     }
 }
 
 void cDrawManager::drawDebugInfoUsages() const
 {
     int unitsUsed = 0;
-    for (int i = 0; i < MAX_UNITS; i++) {
-        if (unit[i].isValid()) {
+    for (int i = 0; i < m_objects->getUnitsSize(); i++) {
+        if (m_objects->getUnit(i)->isValid()) {
             unitsUsed++;
         }
     }
 
     int structuresUsed = 0;
     for (int i = 0; i < MAX_STRUCTURES; i++) {
-        cAbstractStructure *pStructure = structure[i];
+        cAbstractStructure *pStructure = m_objects->getStructures()[i];
         if (pStructure) {
             structuresUsed++;
         }
     }
 
     int bulletsUsed = 0;
-    for (int i = 0; i < MAX_BULLETS; i++) {
-        cBullet &pBullet = bullet[i];
-        if (pBullet.bAlive) {
+    for (const auto& bullet : m_objects->getBullets()) {
+        if (bullet.bAlive) {
             bulletsUsed++;
         }
     }
 
     int particlesUsed = 0;
-    for (int i = 0; i < MAX_PARTICLES; i++) {
-        cParticle &pParticle = particle[i];
-        if (pParticle.isValid()) {
+    for (const auto& particle : m_objects->getParticles()) {
+        if (particle.isValid()) {
             particlesUsed++;
         }
     }
 
     int startY = 74;
     int height = 14;
-    m_textDrawer->drawText(0, startY, std::format("Units {}/{}", unitsUsed, MAX_UNITS));
-    m_textDrawer->drawText(0, startY + 1*height, std::format("Structures %d/%d", structuresUsed, MAX_STRUCTURES));
-    m_textDrawer->drawText(0, startY + 2*height, std::format("Bullets %d/%d", bulletsUsed, MAX_BULLETS));
-    m_textDrawer->drawText(0, startY + 3*height, std::format("Particles %d/%d", particlesUsed, MAX_PARTICLES));
+    m_textDrawer->drawText(0, startY, std::format("Units {}/{}", unitsUsed, m_objects->getUnitsSize()));
+    m_textDrawer->drawText(0, startY + (1*height), std::format("Structures {}/{}", structuresUsed, MAX_STRUCTURES));
+    m_textDrawer->drawText(0, startY + (2*height), std::format("Bullets {}/{}", bulletsUsed, m_objects->getBullets().size()));
+    m_textDrawer->drawText(0, startY + (3*height), std::format("Particles {}/{}", particlesUsed, cParticles::size()));
+    m_textDrawer->drawText(0, startY + (4*height), std::format("Visible particles BOTTOM: {}/ TOP: {}", m_particleDrawer->getParticlesLowerLayerAmount(), m_particleDrawer->getParticlesTopLayerAmount()));
 }
 
 void cDrawManager::drawCredits()
 {
-    m_creditsDrawer.draw();
+    m_creditsDrawer->draw();
 }
 
 void cDrawManager::drawRallyPoint()
 {
-    cPlayer &humanPlayer = players[HUMAN];
-    if (humanPlayer.selected_structure < 0) return;
-    cAbstractStructure *theStructure = structure[humanPlayer.selected_structure];
+    if (m_player->selected_structure < 0) return;
+    cAbstractStructure *theStructure = m_objects->getStructures()[m_player->selected_structure];
     if (!theStructure) return;
     int rallyPointCell = theStructure->getRallyPoint();
     if (rallyPointCell < 0) return;
 
-    int drawX = mapCamera->getWindowXPositionFromCell(rallyPointCell);
-    int drawY = mapCamera->getWindowYPositionFromCell(rallyPointCell);
+    int drawX = m_mapCamera->getWindowXPositionFromCell(rallyPointCell);
+    int drawY = m_mapCamera->getWindowYPositionFromCell(rallyPointCell);
 
-    SDL_Surface *mouseMoveBitmap = gfxdata->getSurface(MOUSE_MOVE);
+    Texture *mouseMoveBitmap = m_gfxdata->getTexture(MOUSE_MOVE);
 
-    int rallyPointWidthScaled = mapCamera->factorZoomLevel(mouseMoveBitmap->w);
-    int rallyPointHeightScaled = mapCamera->factorZoomLevel(mouseMoveBitmap->h);
+    int rallyPointWidthScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->w);
+    int rallyPointHeightScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->h);
     cRectangle dest = {drawX, drawY, rallyPointWidthScaled, rallyPointHeightScaled};
-    renderDrawer->renderStrechFullSprite(gfxdata->getTexture(MOUSE_MOVE), dest);
+    m_sdlDrawer->renderStrechFullSprite(m_gfxdata->getTexture(MOUSE_MOVE), dest);
 
-    int startX = theStructure->iDrawX() + mapCamera->factorZoomLevel(theStructure->getWidthInPixels() / 2);
-    int startY = theStructure->iDrawY() + mapCamera->factorZoomLevel(theStructure->getHeightInPixels() / 2);
+    int startX = theStructure->iDrawX() + m_mapCamera->factorZoomLevel(theStructure->getWidthInPixels() / 2);
+    int startY = theStructure->iDrawY() + m_mapCamera->factorZoomLevel(theStructure->getHeightInPixels() / 2);
 
     int offset = (mouseMoveBitmap->w/2);
-    drawX = mapCamera->getWindowXPositionFromCellWithOffset(rallyPointCell, offset);
-    drawY = mapCamera->getWindowYPositionFromCellWithOffset(rallyPointCell, offset);
+    drawX = m_mapCamera->getWindowXPositionFromCellWithOffset(rallyPointCell, offset);
+    drawY = m_mapCamera->getWindowYPositionFromCellWithOffset(rallyPointCell, offset);
 
     int endX = drawX;
     int endY = drawY;
 
-    renderDrawer->renderLine( startX, startY, endX, endY, players[HUMAN].getMinimapColor());
+    m_sdlDrawer->renderLine( startX, startY, endX, endY, m_player->getMinimapColor());
 }
 
 void cDrawManager::drawSidebar()
 {
-    renderDrawer->setClippingFor(game.m_screenW - cSideBar::SidebarWidth, 0, game.m_screenW, game.m_screenH);
-    m_sidebarDrawer.draw();
-    miniMapDrawer.draw();
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->setClippingFor(m_gameSettings->getScreenW() - cSideBar::SidebarWidth, 0, m_gameSettings->getScreenW(), m_gameSettings->getScreenH());
+    m_sidebarDrawer->draw();
+    m_miniMapDrawer->draw();
+    m_sdlDrawer->resetClippingFor();
 }
 
 /**
@@ -196,13 +273,12 @@ void cDrawManager::drawStructurePlacing()
     cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();
     if (itemToPlace == nullptr) return;
 
-    m_placeitDrawer.draw(itemToPlace, m_player->getGameControlsContext()->getMouseCell());
+    m_placeitDrawer->draw(itemToPlace, m_player->getGameControlsContext()->getMouseCell());
 }
 
 void cDrawManager::drawMessage()
 {
-    m_messageDrawer.draw();
-
+    m_messageDrawer->draw();
     // TODO: replace messageDrawer with drawMessageBar?
     // messageBarDrawer->drawMessageBar();
 }
@@ -212,8 +288,7 @@ void cDrawManager::drawCombatMouse()
     drawMouse();
 
     cGameControlsContext *context = m_player->getGameControlsContext();
-    //context->isMouseRightButtonPressed()
-    if (context->shouldDrawToolTip()) {
+    if (m_drawToolTip && context->isMouseOnBattleField() ) {
         m_mouseDrawer->drawToolTip();
     }
 }
@@ -226,71 +301,66 @@ void cDrawManager::drawMouse()
 void cDrawManager::drawTopBarBackground()
 {
     Texture *topbarPiece = m_gfxinter->getTexture(BMP_TOPBAR_BACKGROUND);
-    for (int x = 0; x < game.m_screenW; x+= topbarPiece->w) {
-        renderDrawer->renderSprite(topbarPiece, x, 0);
+    for (int x = 0; x < m_gameSettings->getScreenW(); x+= topbarPiece->w) {
+        m_sdlDrawer->renderSprite(topbarPiece, x, 0);
     }
 
-    renderDrawer->renderSprite(btnOptions, 1, 0);
+    m_sdlDrawer->renderSprite(m_btnOptions.get(), 1, 0);
 
     //HACK HACK: for now do it like this, instead of using an actual GUI object here
     cRectangle optionsRect = cRectangle(0,0, 162, 30);
-    if (game.getMouse()->isLeftButtonClicked() && game.getMouse()->isOverRectangle(&optionsRect)) {
-        game.setNextStateToTransitionTo(GAME_OPTIONS);
+    if (m_mouse->isLeftButtonClicked() && m_mouse->isOverRectangle(&optionsRect)) {
+        m_stateTransitions->setNextState(GAME_OPTIONS);
     }
 }
 
 void cDrawManager::setPlayerToDraw(cPlayer *playerToDraw)
 {
+    const bool houseChanged = m_player->getHouse() != playerToDraw->getHouse();
     m_player = playerToDraw;
-    m_creditsDrawer.setPlayer(playerToDraw);
-    m_sidebarDrawer.setPlayer(playerToDraw);
-    m_orderDrawer.setPlayer(playerToDraw);
-    miniMapDrawer.setPlayer(playerToDraw);
-    m_mapDrawer.setPlayer(playerToDraw);
+    if (houseChanged) {
+        m_btnOptions.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_ctx->getSDLDrawer(), m_player, m_gfxinter->getSurface(BTN_OPTIONS), TransparentColorIndex, m_gfxinter->getDensity()));
+    }
+    m_creditsDrawer->setPlayer(playerToDraw);
+    m_sidebarDrawer->setPlayer(playerToDraw);
+    m_orderDrawer->setPlayer(playerToDraw);
+    m_miniMapDrawer->setPlayer(playerToDraw);
+    m_mapDrawer->setPlayer(playerToDraw);
+    m_structureDrawer->setPlayer(playerToDraw);
+    m_placeitDrawer->setPlayer(playerToDraw);
 }
 
 void cDrawManager::drawOptionBar()
 {
     // upper bar
-    renderDrawer->renderRectFillColor(0, 0, game.m_screenW, cSideBar::TopBarHeight, Color{0, 0, 0,255});
-    renderDrawer->renderRectFillColor(0,game.m_screenW, 40,32, Color{214,149,20,255});
-
-    for (int w = 0; w < (game.m_screenW + 800); w += 789) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_TOP_BAR), w, 31);
-    }
-}
+    m_sdlDrawer->renderRectFillColor(0, 0, m_gameSettings->getScreenW(), cSideBar::TopBarHeight, Color{0, 0, 0,255});
+    m_sdlDrawer->renderRectFillColor(0,m_gameSettings->getScreenW(), 40,32, Color{214,149,20,255});
 
-void cDrawManager::drawNotifications()
-{
-    std::vector<cPlayerNotification> &notifications = m_player->getNotifications();
-//    int y = cSideBar::TopBarHeight + 14; // 12 pixels
-    int y = game.m_screenH - 44;
-    for (auto &notification : notifications) {
-        m_textDrawer->drawText(4, y, notification.getColor(), notification.getMessage().c_str());
-        y-=15;
+    for (int w = 0; w < (m_gameSettings->getScreenW() + 800); w += 789) {
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_TOP_BAR), w, 31);
     }
 }
 
 void cDrawManager::think()
 {
-    miniMapDrawer.think();
+    m_miniMapDrawer->think();
 }
 
 void cDrawManager::init()
 {
-    miniMapDrawer.init();
+    m_miniMapDrawer->init();
 }
 
 void cDrawManager::onNotifyMouseEvent(const s_MouseEvent &event)
 {
-    m_sidebarDrawer.onNotifyMouseEvent(event);
+    m_sidebarDrawer->onNotifyMouseEvent(event);
 }
 
 void cDrawManager::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 {
-    m_sidebarDrawer.onNotifyKeyboardEvent(event);
+    m_sidebarDrawer->onNotifyKeyboardEvent(event);
 
-    switch (event.eventType) {
+    switch (event.getType()) {
         case eKeyEventType::HOLD:
             onKeyDown(event);
             break;
@@ -304,67 +374,82 @@ void cDrawManager::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 
 void cDrawManager::onKeyDown(const cKeyboardEvent &event)
 {
-    if (game.isDebugMode()) {
+    if (m_gameSettings->isDebugMode()) {
         if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
-            m_mapDrawer.setDrawWithoutShroudTiles(true);
+            m_mapDrawer->setDrawWithoutShroudTiles(true);
         }
         if (event.hasKey(SDL_SCANCODE_G)) {
-            m_mapDrawer.setDrawGrid(true);
+            m_mapDrawer->setDrawGrid(true);
         }
     }
+    if (event.hasKey(SDL_SCANCODE_T)) {
+        m_drawToolTip = true;
+    }
 }
 
 void cDrawManager::onKeyPressed(const cKeyboardEvent &event)
 {
-    if (game.isDebugMode()) {
+    if (m_gameSettings->isDebugMode()) {
         // one of these we're pressed, that's enough info to revert back as it breaks the
         // mandatory 'both keys must be pressed' state:
         if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
-            m_mapDrawer.setDrawWithoutShroudTiles(false);
+            m_mapDrawer->setDrawWithoutShroudTiles(false);
         }
         if (event.hasKey(SDL_SCANCODE_G)) {
-            m_mapDrawer.setDrawGrid(false);
+            m_mapDrawer->setDrawGrid(false);
         }
     }
+    if (event.hasKey(SDL_SCANCODE_T)) {
+        m_drawToolTip = false;
+    }
 }
 
 void cDrawManager::missionInit()
 {
-    m_creditsDrawer.setCredits();
-    m_messageDrawer.initCombatPosition();
+    m_creditsDrawer->setCredits();
+    m_messageDrawer->initCombatPosition();
 }
 
 void cDrawManager::thinkFast_statePlaying()
 {
-    m_creditsDrawer.thinkFast();
+    m_creditsDrawer->thinkFast();
 }
 
 void cDrawManager::thinkFast()
 {
-    m_messageDrawer.thinkFast();
+    m_messageDrawer->thinkFast();
 }
 
 void cDrawManager::drawMessageBar()
 {
-    m_messageDrawer.draw();
+    m_messageDrawer->draw();
 }
 
 void cDrawManager::setMessage(std::string msg, bool keepMessage)
 {
-    m_messageDrawer.setMessage(msg, keepMessage);
+    m_messageDrawer->setMessage(msg, keepMessage);
+}
+
+std::string cDrawManager::getMessage() const
+{
+    return m_messageDrawer->getMessage();
 }
 
 void cDrawManager::setKeepMessage(bool value)
 {
-    m_messageDrawer.setKeepMessage(value);
+    m_messageDrawer->setKeepMessage(value);
 }
 
 void cDrawManager::regionInit(int offsetX, int offsetY)
 {
-    m_messageDrawer.initRegionPosition(offsetX, offsetY);
+    m_messageDrawer->initRegionPosition(offsetX, offsetY);
 }
 
 bool cDrawManager::hasMessage()
 {
-    return m_messageDrawer.hasMessage();
+    return m_messageDrawer->hasMessage();
+}
+
+cBuildingListDrawer *cDrawManager::getBuildingListDrawer() {
+    return m_sidebarDrawer->getBuildingListDrawer();
 }


=== PORT: src/managers/cDrawManager.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/managers/cDrawManager.h
stdout:
diff --git a/src/managers/cDrawManager.h b/src/managers/cDrawManager.h
index 247baca4..f01f93e8 100644
--- a/src/managers/cDrawManager.h
+++ b/src/managers/cDrawManager.h
@@ -1,26 +1,54 @@
+/**
+ * @file cDrawManager.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
-#include "controls/cKeyboardEvent.h"
-#include "drawers/cBuildingListDrawer.h"
-#include "drawers/cMapDrawer.h"
-#include "drawers/cMessageDrawer.h"
-#include "drawers/cMiniMapDrawer.h"
-#include "drawers/cMouseDrawer.h"
-#include "drawers/cOrderDrawer.h"
-#include "drawers/cParticleDrawer.h"
-#include "drawers/cPlaceItDrawer.h"
-#include "drawers/CreditsDrawer.h"
-#include "drawers/cSideBarDrawer.h"
+class cKeyboardEvent;
+class cBuildingListDrawer;
+class cMapDrawer;
+class cMessageDrawer;
+class cMiniMapDrawer;
+class cMouseDrawer;
+class cOrderDrawer;
+class cParticleDrawer;
+class cPlaceItDrawer;
+class CreditsDrawer;
+//#include "drawers/cSideBarDrawer.h"
 #include "drawers/cStructureDrawer.h"
 
 #include "observers/cInputObserver.h"
-#include "sMouseEvent.h"
+struct s_MouseEvent;
+
+#include <memory>
 
 class cPlayer;
 struct SDL_Surface;
 class Texture;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+class cSideBarDrawer;
+class GameContext;
+class GameStateTransition;
+class cGameObjectContext;
+class cMapCamera;
+class cMouse;
+class cRectangle;
+class cGameSettings;
+class cStructureUtils;
+struct sGameServices;
 
 /**
  * Candidate class for PlayingMissionState (draw function?), but also for SelectYourNextConquestState (drawing
@@ -29,7 +57,7 @@ class Graphics;
 class cDrawManager : cInputObserver {
 
 public:
-    explicit cDrawManager(GameContext *ctx, cPlayer *thePlayer);
+    explicit cDrawManager(GameContext *ctx, cPlayer *thePlayer, sGameServices *services);
     ~cDrawManager();
 
     void drawCombatState();
@@ -38,24 +66,22 @@ public:
     void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
 
     cMiniMapDrawer *getMiniMapDrawer() {
-        return &miniMapDrawer;
+        return m_miniMapDrawer.get();
     }
 
     cOrderDrawer *getOrderDrawer() {
-        return &m_orderDrawer;
+        return m_orderDrawer.get();
     }
 
     cMouseDrawer *getMouseDrawer() {
-        return m_mouseDrawer;
+        return m_mouseDrawer.get();
     }
 
     cPlaceItDrawer *getPlaceItDrawer() {
-        return &m_placeitDrawer;
+        return m_placeitDrawer.get();
     }
 
-    cBuildingListDrawer *getBuildingListDrawer() {
-        return m_sidebarDrawer.getBuildingListDrawer();
-    }
+    cBuildingListDrawer *getBuildingListDrawer();
 
     void drawMouse();
 
@@ -77,12 +103,15 @@ public:
 
     void setMessage(std::string msg, bool keepMessage = false);
 
+    [[nodiscard]] std::string getMessage() const;
+
     void setKeepMessage(bool value);
 
     void regionInit(int offsetX, int offsetY);
 
     bool hasMessage();
 
+    void reset();
 protected:
     void drawSidebar();
 
@@ -101,26 +130,37 @@ private:
 
     void drawDebugInfoUsages() const;
 
-    void drawNotifications();
+    // void drawNotifications();
 
     // Properties:
-    cSideBarDrawer m_sidebarDrawer;
-    CreditsDrawer m_creditsDrawer;
-    cOrderDrawer m_orderDrawer;
-    cMapDrawer m_mapDrawer;
-    cMiniMapDrawer miniMapDrawer;
-    cParticleDrawer m_particleDrawer;
-    cMessageDrawer m_messageDrawer;
-    cPlaceItDrawer m_placeitDrawer;
-    cStructureDrawer m_structureDrawer;
+    std::unique_ptr<cSideBarDrawer> m_sidebarDrawer;
+    std::unique_ptr<CreditsDrawer> m_creditsDrawer;
+    std::unique_ptr<cOrderDrawer> m_orderDrawer;
+    std::unique_ptr<cMapDrawer> m_mapDrawer;
+    std::unique_ptr<cMiniMapDrawer> m_miniMapDrawer;
+    std::unique_ptr<cParticleDrawer> m_particleDrawer;
+    std::unique_ptr<cMessageDrawer> m_messageDrawer;
+    std::unique_ptr<cPlaceItDrawer> m_placeitDrawer;
+    std::unique_ptr<cStructureDrawer> m_structureDrawer;
     Color m_sidebarColor;
-    Texture *btnOptions;
-
+    std::unique_ptr<Texture> m_btnOptions;
+    bool m_drawToolTip = false;
     // TODO: bullet/projectile drawer
-    cPlayer *m_player;
+    cPlayer *m_player = nullptr;
+    GameContext *m_ctx = nullptr;
     cTextDrawer *m_textDrawer = nullptr;
-    Graphics* m_gfxinter;
-    cMouseDrawer* m_mouseDrawer = nullptr;
+    SDLDrawer* m_sdlDrawer = nullptr;
+    Graphics* m_gfxinter = nullptr;
+    Graphics* m_gfxdata = nullptr;
+    std::unique_ptr<cMouseDrawer> m_mouseDrawer;
+    GameStateTransition* m_stateTransitions = nullptr;
+    cMouse* m_mouse = nullptr;
+    cRectangle* m_mapViewport = nullptr;
+    cGameObjectContext* m_objects = nullptr;
+    cMapCamera* m_mapCamera = nullptr;
+    cGameSettings* m_gameSettings = nullptr;
+    cStructureUtils* m_structureUtils = nullptr;
+    sGameServices* m_services = nullptr;
 
     void onKeyDown(const cKeyboardEvent &event);
 


=== PORT: src/map/cMapCamera.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/map/cMapCamera.cpp
stdout:
diff --git a/src/map/cMapCamera.cpp b/src/map/cMapCamera.cpp
deleted file mode 100644
index f9c24a52..00000000
--- a/src/map/cMapCamera.cpp
+++ /dev/null
@@ -1,361 +0,0 @@
-#include "cMapCamera.h"
-
-#include "data/gfxdata.h"
-#include "d2tmc.h"
-#include "sidebar/cSideBar.h"
-#include "map/MapGeometry.hpp"
-
-#include <algorithm>
-
-namespace {
-constexpr auto kMapBoundaryScrollSpeed = 5.0f;
-}
-
-cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
-    m_moveSpeedDrag(moveSpeedDrag),
-    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
-    m_cameraEdgeMove(cameraEdgeMove),
-    m_pMap(theMap)
-{
-    m_viewportStartX = m_viewportStartY = 32;
-    m_zoomLevel = 1.0f;
-
-    int widthOfSidebar = cSideBar::SidebarWidth;
-    m_heightOfTopBar = cSideBar::TopBarHeight;
-
-    m_windowWidth= game.m_screenW - widthOfSidebar;
-    m_windowHeight= game.m_screenH - m_heightOfTopBar;
-
-    m_viewportWidth=m_windowWidth;
-    m_viewportHeight=m_windowHeight;
-
-    m_moveX = 0.0f;
-    m_moveY = 0.0f;
-
-    m_keyPressedDown = false;
-    m_keyPressedUp = false;
-    m_keyPressedLeft = false;
-    m_keyPressedRight = false;
-
-    calibrate();
-}
-
-cMapCamera::~cMapCamera()
-{
-}
-
-void cMapCamera::zoomIn()
-{
-    if (m_zoomLevel < 4.0) {
-        m_zoomLevel += 0.1;
-        auto m_mouse = game.getMouse();
-        adjustViewport(m_mouse->getX(), m_mouse->getY());
-    }
-}
-
-void cMapCamera::adjustViewport(float screenX, float screenY)
-{
-    int oldViewportWidth = m_viewportWidth;
-    int oldViewportHeight = m_viewportHeight;
-
-    calibrate();
-
-    int diffViewportWidth = oldViewportWidth - m_viewportWidth;
-    int diffViewportHeight = oldViewportHeight - m_viewportHeight;
-
-    float nMouseX = screenX / m_windowWidth;
-    float nMouseY = (screenY - m_heightOfTopBar) / m_windowHeight;
-
-    m_viewportStartX += diffViewportWidth * nMouseX;
-    m_viewportStartY += diffViewportHeight * nMouseY;
-
-    keepViewportWithinReasonableBounds();
-}
-
-void cMapCamera::zoomOut()
-{
-    if (m_zoomLevel > 0.25) {
-        m_zoomLevel -= 0.1;
-        auto m_mouse = game.getMouse();
-        adjustViewport(m_mouse->getX(), m_mouse->getY());
-    }
-}
-
-void cMapCamera::calibrate()
-{
-    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
-    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
-
-    m_viewportWidth = divideByZoomLevel(m_windowWidth);
-    m_viewportHeight = divideByZoomLevel(m_windowHeight);
-}
-
-void cMapCamera::keepViewportWithinReasonableBounds()
-{
-    int halfViewportWidth = m_viewportWidth / 2;
-    int halfViewportHeight = m_viewportHeight / 2;
-
-    if (m_viewportStartX < -halfViewportWidth) {
-        m_viewportStartX = -halfViewportWidth;
-    }
-
-    if (m_viewportStartY < -halfViewportHeight) {
-        m_viewportStartY = -halfViewportHeight;
-    }
-
-    int maxWidth = (global_map.getWidth() * TILESIZE_WIDTH_PIXELS) + halfViewportWidth;
-    if (getViewportEndX() > maxWidth) {
-        m_viewportStartX = maxWidth - m_viewportWidth;
-    }
-
-    int maxHeight = (global_map.getHeight() * TILESIZE_HEIGHT_PIXELS) + halfViewportHeight;
-    if ((getViewportEndY()) > maxHeight) {
-        m_viewportStartY = maxHeight - m_viewportHeight;
-    }
-}
-
-void cMapCamera::centerAndJumpViewPortToCell(int cell)
-{
-    // fix any boundaries
-    if (cell < 0) cell = 0;
-    if (cell >= global_map.getMaxCells()) cell = (global_map.getMaxCells()-1);
-
-    int mapCellX = m_pMap->getAbsoluteXPositionFromCell(cell);
-    int mapCellY = m_pMap->getAbsoluteYPositionFromCell(cell);
-
-    // determine the half of our screen
-    int halfViewportWidth = m_viewportWidth / 2;
-    int halfViewportHeight = m_viewportHeight / 2;
-
-    // determine the new X and Y position, absolute map coordinates
-    int newViewPortX = mapCellX - halfViewportWidth;
-    int newViewPortY = mapCellY - halfViewportHeight;
-
-    // for now, snap it to 32x32 grid
-    newViewPortX = (newViewPortX / 32) * 32;
-    newViewPortY = (newViewPortY / 32) * 32;
-
-    jumpTo(newViewPortX, newViewPortY);
-
-    calibrate();
-
-    keepViewportWithinReasonableBounds();
-}
-
-void cMapCamera::thinkFast()
-{
-    // update viewport coordinates
-    m_viewportStartX = m_viewportStartX + m_moveX;
-    m_viewportStartY = m_viewportStartY + m_moveY;
-
-    keepViewportWithinReasonableBounds();
-
-}
-
-void cMapCamera::jumpTo(int theX, int theY)
-{
-    m_viewportStartX = theX;
-    m_viewportStartY = theY;
-    calibrate();
-}
-
-void cMapCamera::setViewportPosition(int x, int y)
-{
-    jumpTo(x, y);
-    keepViewportWithinReasonableBounds();
-}
-
-int cMapCamera::getCellFromAbsolutePosition(int x, int y)
-{
-    return global_map.getGeometry().getCellWithMapDimensions((x / 32), (y / 32));
-}
-
-void cMapCamera::onNotifyMouseEvent(const s_MouseEvent &event)
-{
-    // MOUSE WHEEL scrolling causes zooming in/out
-    switch (event.eventType) {
-        case eMouseEventType::MOUSE_MOVED_TO:
-            onMouseMovedTo(event);
-            break;
-        case eMouseEventType::MOUSE_SCROLLED_DOWN:
-            mapCamera->zoomOut();
-            break;
-        case eMouseEventType::MOUSE_SCROLLED_UP:
-            mapCamera->zoomIn();
-            break;
-        case eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED:
-            onMouseRightButtonPressed(event);
-            break;
-        case eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED:
-            onMouseRightButtonClicked(event);
-            break;
-        default:
-            break;
-    }
-}
-
-void cMapCamera::onMouseMovedTo(const s_MouseEvent &event)
-{
-    cMouse *pMouse = game.getMouse();
-
-    // mouse is 'moving by pressing right mouse button', this supersedes behavior with edges
-    if (!pMouse->isMapScrolling() && m_cameraEdgeMove) {
-
-        int mouseX = event.coords.x;
-        int mouseY = event.coords.y;
-
-        if (mouseX <= 2) {
-            setMoveX(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_LEFT);
-        }
-        else if (mouseX >= (game.m_screenW - 2)) {
-            setMoveX(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_RIGHT);
-        }
-        else {
-            if (!m_keyPressedLeft && !m_keyPressedRight) {
-                setMoveX(0.0f, m_moveSpeedBorderOrKeys);
-            }
-        }
-
-        if (mouseY <= 2) {
-            setMoveY(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_UP);
-        }
-        else if (mouseY >= (game.m_screenH - 2)) {
-            setMoveY(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_DOWN);
-        }
-        else {
-            if (!m_keyPressedUp && !m_keyPressedDown) {
-                setMoveY(0.0f, m_moveSpeedBorderOrKeys);
-            }
-        }
-    }
-}
-
-void cMapCamera::onNotifyKeyboardEvent(const cKeyboardEvent &event)
-{
-    switch (event.eventType) {
-        case eKeyEventType::HOLD:
-            onKeyHold(event);
-            break;
-        case eKeyEventType::PRESSED:
-            onKeyPressed(event);
-            break;
-        default:
-            break;
-    }
-}
-
-void cMapCamera::onMouseRightButtonPressed(const s_MouseEvent &)
-{
-    m_moveX = 0.0f;
-    m_moveY = 0.0f;
-
-    cMouse *pMouse = game.getMouse();
-
-    // mouse is 'moving by pressing right mouse button', this supersedes behavior with borders
-    if (pMouse->isMapScrolling()) {
-        // difference in pixels (- means up/left, + means down/right)
-        int diffX = pMouse->getMouseDragDeltaX();
-        int diffY = pMouse->getMouseDragDeltaY();
-
-        // now calculate the speed in which we want to do this, the further
-        // away (greater distance) the faster.
-        float factorX = (float)abs(diffX) / (m_windowWidth / 2);
-        float factorY = (float)abs(diffY) / (m_windowHeight / 2);
-
-        // now we know factor, we only want to move so fast in pixels, so clamp/keep the diffX/Y between sane
-        // values. If we don't do this, the scrolling is too fast. Also take m_zoomLevel into account so when we
-        // zoom in, it won't go faster. And if we have zoomed out, it will be faster, but relatively the same speed as
-        // zoom factor 1.0
-        diffX = divideByZoomLevel(std::clamp(diffX, -24, 24));
-        diffY = divideByZoomLevel(std::clamp(diffY, -24, 24));
-
-        float resultX = diffX * factorX;
-        float resultY = diffY * factorY;
-
-        setMoveX(resultX, m_moveSpeedDrag);
-        setMoveY(resultY, m_moveSpeedDrag);
-
-        // reset keyboard state, as this supersedes keyboard movement
-        m_keyPressedDown = false;
-        m_keyPressedUp = false;
-        m_keyPressedLeft = false;
-        m_keyPressedRight = false;
-
-        return;
-    }
-}
-
-void cMapCamera::setMoveX(float x, float moveSpeed)
-{
-    m_moveX = x * moveSpeed;
-}
-
-void cMapCamera::setMoveY(float y, float moveSpeed)
-{
-    m_moveY = y * moveSpeed;
-}
-
-void cMapCamera::onKeyHold(const cKeyboardEvent &event)
-{
-    cMouse *pMouse = game.getMouse();
-
-    // mouse is 'moving by pressing right mouse button', this supersedes reacting to keypress
-    if (!pMouse->isMapScrolling()) {
-        if (event.hasKey(SDL_SCANCODE_LEFT)) {
-            setMoveX(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_LEFT);
-            m_keyPressedLeft = true;
-        }
-
-        if (event.hasKey(SDL_SCANCODE_UP)) {
-            setMoveY(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_UP);
-            m_keyPressedUp = true;
-        }
-
-        if (event.hasKey(SDL_SCANCODE_RIGHT)) {
-            setMoveX(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_RIGHT);
-            m_keyPressedRight = true;
-        }
-
-        if (event.hasKey(SDL_SCANCODE_DOWN)) {
-            setMoveY(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
-            pMouse->setTile(MOUSE_DOWN);
-            m_keyPressedDown = true;
-        }
-    }
-}
-
-void cMapCamera::onKeyPressed(const cKeyboardEvent &event)
-{
-    if (event.hasKey(SDL_SCANCODE_LEFT)) {
-        setMoveX(0.0f, m_moveSpeedBorderOrKeys);
-        m_keyPressedLeft = false;
-    }
-
-    if (event.hasKey(SDL_SCANCODE_UP)) {
-        setMoveY(0.0f, m_moveSpeedBorderOrKeys);
-        m_keyPressedUp = false;
-    }
-
-    if (event.hasKey(SDL_SCANCODE_RIGHT)) {
-        setMoveX(0.0f, m_moveSpeedBorderOrKeys);
-        m_keyPressedRight = false;
-    }
-
-    if (event.hasKey(SDL_SCANCODE_DOWN)) {
-        setMoveY(0.0f, m_moveSpeedBorderOrKeys);
-        m_keyPressedDown = false;
-    }
-}
-
-void cMapCamera::onMouseRightButtonClicked(const s_MouseEvent &)
-{
-    m_moveX = 0.0f;
-    m_moveY = 0.0f;
-}


=== PORT: src/map/cMapCamera.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/map/cMapCamera.h
stdout:
diff --git a/src/map/cMapCamera.h b/src/map/cMapCamera.h
deleted file mode 100644
index a76f36e5..00000000
--- a/src/map/cMapCamera.h
+++ /dev/null
@@ -1,234 +0,0 @@
-/*
- * cMapCamera.h
- *
- *  A map camera is 'looking' at the map. Using this camera (or viewport) we can determine
- *  what to draw, how big, etc.
- *
- *  Using a camera technique we can easily adjust the drawing logic whenever the resolution
- *  of the game changes.
- *
- */
-
-#pragma once
-
-#include "cMap.h"
-
-#include "observers/cInputObserver.h"
-
-#include <cmath>
-
-class cMapCamera : cInputObserver {
-
-public:
-    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove);
-
-    ~cMapCamera();
-
-    void onNotifyMouseEvent(const s_MouseEvent &event) override;
-    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
-
-    void thinkFast();
-
-    void resetZoom() {
-        m_zoomLevel = 1.0f;
-        calibrate();
-        keepViewportWithinReasonableBounds();
-    }
-
-    void jumpTo(int theX, int theY);
-
-    void moveTo(int theX, int theY);
-
-    /**
-     * Returns the pixel coordinate on the window to draw onto. Use this function to convert absolute
-     * coordinates into window coordinates so you can draw something.
-     * @param absoluteXPosition
-     * @return
-     */
-    int getWindowXPosition(int absoluteXPosition) {
-        return getWindowXPositionWithOffset(absoluteXPosition, 0);
-    }
-
-    int getWindowYPosition(int absoluteYPosition) {
-        return getWindowYPositionWithOffset(absoluteYPosition, 0);
-    }
-
-    int getWindowXPositionFromCell(int cell) {
-        return getWindowXPositionFromCellWithOffset(cell, 0);
-    }
-
-    int getWindowYPositionFromCell(int cell) {
-        return getWindowYPositionFromCellWithOffset(cell, 0);
-    }
-
-    int getWindowXPositionFromCellWithOffset(int cell, int offset) {
-        int absoluteXPosition = m_pMap->getAbsoluteXPositionFromCell(cell);
-        return getWindowXPositionWithOffset(absoluteXPosition, offset);
-    }
-
-    int getWindowYPositionFromCellWithOffset(int cell, int offset) {
-        int absoluteYPosition = m_pMap->getAbsoluteYPositionFromCell(cell);
-        return getWindowYPositionWithOffset(absoluteYPosition, offset);
-    }
-
-    /**
-     * Translates an absolute X position into a position on the window. The offset is added after translating
-     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
-     * @param absoluteXPosition
-     * @param offset
-     * @return
-     */
-    int getWindowXPositionWithOffset(int absoluteXPosition, int offset) {
-        return std::round(factorZoomLevel((absoluteXPosition - m_viewportStartX) + offset));
-    }
-
-    /**
-     * Translates an absolute Y position into a position on the window. The offset is added after translating
-     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
-     * @param absoluteYPosition
-     * @param offset
-     * @return
-     */
-    int getWindowYPositionWithOffset(int absoluteYPosition, int offset) {
-        return std::round(factorZoomLevel((absoluteYPosition - m_viewportStartY) + offset) + m_heightOfTopBar);
-    }
-
-    // These methods need to use zoomfactor to properly calculate the position on the map
-    int getAbsMapMouseX(int mouseX) {
-        int iMouseX = divideByZoomLevel(mouseX);
-        return iMouseX + getViewportStartX();
-    }
-
-    int getAbsMapMouseY(int mouseY) {
-        int iMouseY = divideByZoomLevel(mouseY - m_heightOfTopBar);
-        return iMouseY + getViewportStartY();
-    }
-
-    int getViewportStartX() {
-        return m_viewportStartX;
-    }
-
-    int getViewportStartY() {
-        return m_viewportStartY;
-    }
-
-    int getViewportEndX() {
-        return m_viewportStartX + m_viewportWidth;
-    }
-
-    int getViewportEndY() {
-        return m_viewportStartY + m_viewportHeight;
-    }
-
-    int getViewportWidth() {
-        return m_viewportWidth;
-    }
-
-    int getViewportHeight() {
-        return m_viewportHeight;
-    }
-
-    int getViewportCenterX() {
-        return m_viewportStartX + (m_viewportWidth / 2);
-    }
-
-    int getViewportCenterY() {
-        return m_viewportStartY + (m_viewportHeight / 2);
-    }
-
-    void centerAndJumpViewPortToCell(int cell);
-
-    float getZoomedTileWidth() const {
-        return m_tileWidth;
-    }
-
-    float getZoomedTileHeight() const {
-        return m_tileHeight;
-    }
-
-    float factorZoomLevel(int value) {
-        return value * m_zoomLevel;
-    }
-
-    float factorZoomLevel(float value) {
-        return value * m_zoomLevel;
-    }
-
-    float divideByZoomLevel(int value) {
-        return value / m_zoomLevel;
-    }
-
-    float divideByZoomLevel(float value) {
-        return value / m_zoomLevel;
-    }
-
-    int getWindowWidth() {
-        return m_windowWidth;
-    }
-
-    int getWindowHeight() {
-        return m_windowHeight;
-    }
-
-    float getZoomLevel() {
-        return m_zoomLevel;
-    }
-
-    int getCellFromAbsolutePosition(int x, int y);
-
-    void setViewportPosition(int x, int y);
-
-private:
-    // rendering coordinates, they are manipulated by zooming
-    float m_viewportStartX;
-    float m_viewportStartY;
-    int m_viewportWidth;
-    int m_viewportHeight;
-
-    // used for moving
-    float m_moveX;
-    float m_moveY;
-    float m_moveSpeedDrag;
-    float m_moveSpeedBorderOrKeys;
-    bool m_cameraEdgeMove;
-
-    bool m_keyPressedUp;
-    bool m_keyPressedDown;
-    bool m_keyPressedLeft;
-    bool m_keyPressedRight;
-
-    int m_heightOfTopBar;
-    int m_windowWidth;
-    int m_windowHeight;
-
-    // Zoom level, 1 == normal, > 1 is zooming in. < 1 is zooming out.
-    float m_zoomLevel;
-
-    // the calculated width and height, taking zoomlevel into account
-    float m_tileHeight;
-    float m_tileWidth;
-
-    // the map this camera is viewing
-    cMap *m_pMap;
-
-    void adjustViewport(float screenX, float screenY);
-
-    // Calculates viewport and tile width/height
-    void calibrate();
-
-    void keepViewportWithinReasonableBounds();
-
-    void zoomIn();
-    void zoomOut();
-
-    void onMouseMovedTo(const s_MouseEvent &event);
-
-    void onMouseRightButtonClicked(const s_MouseEvent &event);
-    void onMouseRightButtonPressed(const s_MouseEvent &event);
-
-    void setMoveX(float x, float moveSpeed);
-    void setMoveY(float y, float moveSpeed);
-
-    void onKeyHold(const cKeyboardEvent &event);
-    void onKeyPressed(const cKeyboardEvent &event);
-};


=== PORT: src/sidebar/cBuildingList.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingList.cpp
stdout:
diff --git a/src/sidebar/cBuildingList.cpp b/src/sidebar/cBuildingList.cpp
index 3410b9cd..a130f15f 100644
--- a/src/sidebar/cBuildingList.cpp
+++ b/src/sidebar/cBuildingList.cpp
@@ -1,22 +1,48 @@
-#include "cBuildingList.h"
+/**
+ * @file cBuildingList.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cBuildingList.h"
+#include "context/cInfoContext.h"
 #include "building/cItemBuilder.h"
-#include "d2tmc.h"
+#include "context/GameContext.hpp"
+#include "game/cEventEmitter.h"
+#include "game/cScreenFader.h"
+#include "include/sGameServices.h"
+#include "utils/common.h"
+#include "utils/cRectangle.h"
+#include "utils/Log.h"
+#include "gameobjects/cSpecialInfos.h"
+#include "gameobjects/cUpgradeInfo.h"
+#include "gameobjects/structures/cStructureInfo.h"
+#include "gameobjects/units/cUnitInfos.h"
 
 #include <vector>
+#include <algorithm>
 
 cBuildingList::cBuildingList(eListType listType)
 {
-    TIMER_flashing = 0;
-    lastClickedId = 0;
-    buttonIconIdPressed = 0;	// the button to draw at the left of the list
-    buttonDrawX = 0;
-    buttonDrawY = 0;
-    memset(items, 0, sizeof(items));
-    typeOfList = listType;
-    maxItems = 0;
+    m_TIMER_flashing = 0;
+    m_lastClickedId = 0;
+    m_buttonIconIdPressed = 0;	// the button to draw at the left of the list
+    m_buttonDrawX = 0;
+    m_buttonDrawY = 0;
+    std::fill(std::begin(m_items), std::end(m_items), nullptr);
+    m_listType = listType;
+    m_maxItems = 0;
     m_itemBuilder = nullptr;
-    selected = false;
+    m_selected = false;
 }
 
 cBuildingList::~cBuildingList()
@@ -28,7 +54,7 @@ cBuildingListItem *cBuildingList::getItem(int i)
 {
     if (i < 0) return nullptr;
     if (i >= MAX_ICONS) return nullptr;
-    return items[i];
+    return m_items[i];
 }
 
 /**
@@ -39,7 +65,7 @@ cBuildingListItem *cBuildingList::getItem(int i)
 int cBuildingList::getFreeSlot()
 {
     for (int i = 0; i < MAX_ICONS; i++) {
-        if (items[i] == nullptr) {
+        if (m_items[i] == nullptr) {
             return i; // return free slot
         }
     }
@@ -50,8 +76,8 @@ int cBuildingList::getFreeSlot()
 void cBuildingList::removeAllItems()
 {
     for (int i =0 ; i < MAX_ICONS; i++) {
-        delete items[i];
-        items[i] = nullptr;
+        delete m_items[i];
+        m_items[i] = nullptr;
     }
 }
 
@@ -77,8 +103,12 @@ cBuildingListItem *cBuildingList::getItemByBuildId(int buildId)
 
 void cBuildingList::addUpgradeToList(int upgradeType)
 {
-    cBuildingListItem *item = new cBuildingListItem(upgradeType, sUpgradeInfo[upgradeType],
-            sUpgradeInfo[upgradeType].providesTypeSubList);
+    auto upgradeInfo = m_info->getUpgradeInfo(upgradeType);
+    cBuildingListItem *item = new cBuildingListItem(
+        upgradeType,
+        upgradeInfo
+    );
+
     if (!addItemToList(item)) {
         delete item;
     }
@@ -86,7 +116,7 @@ void cBuildingList::addUpgradeToList(int upgradeType)
 
 void cBuildingList::addStructureToList(int structureType, int subList)
 {
-    cBuildingListItem *item = new cBuildingListItem(structureType, sStructureInfo[structureType], subList);
+    cBuildingListItem *item = new cBuildingListItem(structureType, m_info->getStructureInfo(structureType), subList);
     if (!addItemToList(item)) {
         delete item;
     }
@@ -94,7 +124,7 @@ void cBuildingList::addStructureToList(int structureType, int subList)
 
 void cBuildingList::addUnitToList(int unitType, int subList)
 {
-    cBuildingListItem *item = new cBuildingListItem(unitType, sUnitInfo[unitType], subList);
+    cBuildingListItem *item = new cBuildingListItem(unitType, m_info->getUnitInfo(unitType), subList);
     if (!addItemToList(item)) {
         delete item;
     }
@@ -102,7 +132,7 @@ void cBuildingList::addUnitToList(int unitType, int subList)
 
 void cBuildingList::addSpecialToList(int specialType, int subList)
 {
-    s_SpecialInfo &special = sSpecialInfo[specialType];
+    s_SpecialInfo &special = m_info->getSpecialInfo(specialType);
     cBuildingListItem *item = new cBuildingListItem(specialType, special, subList);
     if (!addItemToList(item)) {
         delete item;
@@ -112,61 +142,52 @@ void cBuildingList::addSpecialToList(int specialType, int subList)
 bool cBuildingList::addItemToList(cBuildingListItem *item)
 {
     if (isItemInList(item)) {
-//		logbook("Will not add, item is already in list.");
-        // item is already in list, do not add
         return false;
     }
 
     int slotId = getFreeSlot();
     if (slotId < 0 ) {
-        logbook("Failed to add icon to cBuildingList, no free slot left in list");
+        Logger::warn(COMP_SIDEBAR, "cBuildingList", "Failed to add icon to cBuildingList, no free slot left in list");
         return false;
     }
 
     bool beforeAddingAvailable = isAvailable();
 
     // add
-    items[slotId] = item;
+    m_items[slotId] = item;
     item->setSlotId(slotId);
     item->setList(this);
-    maxItems = slotId + 1;
-//	char msg[355];
-//	sprintf(msg, "Icon added with id [%d] added to cBuilding list, put in slot[%d], set maxItems to [%d]", item->getBuildId(), slot, maxItems);
-//	logbook(msg);
+    item->serviceInit(m_info, m_settings);
+    m_maxItems = slotId + 1;
 
     // notify game that the item just has been added!
     cPlayer *pPlayer = m_itemBuilder->getPlayer();
     int buildId = item->getBuildId();
     eBuildType buildType = item->getBuildType();
-
-    s_GameEvent event {
+    const s_GameEvent event {
         .eventType = eGameEventType::GAME_EVENT_LIST_ITEM_ADDED,
-        .entityType = buildType,
-        .entityID = -1,
-        .player = pPlayer,
-        .entitySpecificType = buildId,
-        .atCell = -1,
-        .isReinforce = false,
-        .buildingListItem = item
+        .data = BuildingEvent {
+            .entityType = buildType,
+            .player = pPlayer,
+            .entitySpecificType = buildId,
+            .buildingListItem = item
+        }
     };
-
-    game.onNotifyGameEvent(event);
+    m_eventEmitter->emit(event);
 
     if (isAvailable() != beforeAddingAvailable) {
         // emit another event that this list became available! (so that sidebar can animate things)
-        s_GameEvent event {
+        const s_GameEvent event {
             .eventType = eGameEventType::GAME_EVENT_LIST_BECAME_AVAILABLE,
-            .entityType = buildType,
-            .entityID = -1,
-            .player = pPlayer,
-            .entitySpecificType = buildId,
-            .atCell = -1,
-            .isReinforce = false,
-            .buildingListItem = item,
-            .buildingList = this
+            .data = BuildingEvent {
+                .entityType = buildType,
+                .player = pPlayer,
+                .entitySpecificType = buildId,
+                .buildingListItem = item,
+                .buildingList = this
+            }
         };
-
-        game.onNotifyGameEvent(event);
+        m_eventEmitter->emit(event);
     }
 
     startFlashing();
@@ -209,36 +230,33 @@ bool cBuildingList::removeItemFromList(int position)
     bool beforeRemovingAvailable = isAvailable();
 
     delete item;
-    items[position] = nullptr;
+    m_items[position] = nullptr;
 
     // starting from 'position' which became NULL, make sure everything
     // after that slotIndex is moved. So we don't get gaps.
-    for (int i = (position + 1); i < maxItems; i++) {
-        items[i-1] = items[i];
-        items[i-1]->setSlotId(i-1);
+    for (int i = (position + 1); i < m_maxItems; i++) {
+        m_items[i-1] = m_items[i];
+        m_items[i-1]->setSlotId(i-1);
 
         // and clear it out, which in the next loop will be filled
         // if there is any other pointer. If not, the 'last' item is NULL now.
-        items[i] = nullptr;
+        m_items[i] = nullptr;
     }
 
-    maxItems--; // now we can do this
+    m_maxItems--; // now we can do this
 
     if (isAvailable() != beforeRemovingAvailable) {
         // emit another event that this list became un-available!
-        s_GameEvent event {
+        const s_GameEvent event {
             .eventType = eGameEventType::GAME_EVENT_LIST_BECAME_UNAVAILABLE,
-            .entityType = eBuildType::UNIT, // BOGUS
-            .entityID = -1,
-            .player = this->m_itemBuilder->getPlayer(),
-            .entitySpecificType = -1, // BOGUS
-            .atCell = -1,
-            .isReinforce = false,
-            .buildingListItem = nullptr,
-            .buildingList = this
+            .data = BuildingEvent {
+                .entityType = eBuildType::UNIT,
+                .player = this->m_itemBuilder->getPlayer(),
+                .entitySpecificType = -1,
+                .buildingList = this
+            }
         };
-
-        game.onNotifyGameEvent(event);
+        m_eventEmitter->emit(event);
     }
     return true;
 }
@@ -301,7 +319,7 @@ cBuildingListItem *cBuildingList::getItemToPlace()
             }
         }
     }
-    return NULL;
+    return nullptr;
 }
 
 // TODO: This should be set, not looked up. Ie, the item to place should be set somewhere (instead of setting
@@ -319,7 +337,7 @@ cBuildingListItem *cBuildingList::getItemToDeploy()
             }
         }
     }
-    return NULL;
+    return nullptr;
 }
 
 void cBuildingList::setStatusPendingUpgrade(int subListId)
@@ -401,6 +419,13 @@ void cBuildingList::removeAllSublistItems(int sublistId)
     }
 }
 
+void cBuildingList::clearList()
+{
+    while (m_maxItems > 0) {
+        removeItemFromList(m_maxItems - 1);
+    }
+}
+
 void cBuildingList::resetTimesOrderedForAllItems()
 {
     for (int i = 0; i < MAX_ITEMS; i++) {
@@ -423,19 +448,27 @@ cBuildingListItem *cBuildingList::getFirstItemInSubList(int sublistId)
 
 void cBuildingList::setItemBuilder(cItemBuilder *value)
 {
-    assert(value && "cBuildingList::setItemBuilder - Expected to set to a non-null value");
+    d2tm_assert(value && "cBuildingList::setItemBuilder - Expected to set to a non-null value");
     m_itemBuilder = value;
 }
 
+void cBuildingList::serviceInit(sGameServices* services)
+{
+    m_info = services->info;
+    m_settings = services->settings;
+    m_eventEmitter = services->eventEmitter;
+    m_screenFader = services->screenFader;
+}
+
 Color cBuildingList::getFlashingColor()
 {
-    return game.getColorFadeSelected(255, 209, 64);
+    return m_screenFader->getColorFadeSelected(255, 209, 64);
 }
 
 void cBuildingList::think()
 {
-    if (TIMER_flashing > 0) {
-        TIMER_flashing--;
+    if (m_TIMER_flashing > 0) {
+        m_TIMER_flashing--;
     }
     for (int i = 0; i < MAX_ITEMS; i++) {
         cBuildingListItem *pItem = getItem(i);
@@ -463,10 +496,10 @@ void cBuildingList::think()
 
 void cBuildingList::stopFlashing()
 {
-    TIMER_flashing = 0;
+    m_TIMER_flashing = 0;
 }
 
 void cBuildingList::startFlashing()
 {
-    TIMER_flashing = 2500;
+    m_TIMER_flashing = 2500;
 }
\ No newline at end of file


=== PORT: src/sidebar/cBuildingList.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingList.h
stdout:
diff --git a/src/sidebar/cBuildingList.h b/src/sidebar/cBuildingList.h
index d3323d8d..5ce65777 100644
--- a/src/sidebar/cBuildingList.h
+++ b/src/sidebar/cBuildingList.h
@@ -1,3 +1,18 @@
+/**
+ * @file cBuildingList.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
 #include "cSideBar.h"
@@ -9,6 +24,11 @@
 #include "utils/Color.hpp"
 
 class cItemBuilder;
+class cInfoContext;
+class cGameSettings;
+class cEventEmitter;
+class cScreenFader;
+struct sGameServices;
 
 /**
  *
@@ -56,31 +76,31 @@ public:
 
     // get
     bool isSelected() {
-        return selected;
+        return m_selected;
     }
 
     int getLastClickedId() {
-        return lastClickedId;
+        return m_lastClickedId;
     }
 
     int getButtonIconIdPressed() {
-        return buttonIconIdPressed;
+        return m_buttonIconIdPressed;
     }
 
     int getButtonIconIdUnpressed() {
-        return buttonIconIdUnpressed;
+        return m_buttonIconIdUnpressed;
     }
 
     int getButtonDrawX() {
-        return buttonDrawX;
+        return m_buttonDrawX;
     }
 
     int getButtonDrawY() {
-        return buttonDrawY;
+        return m_buttonDrawY;
     }
 
     bool isAvailable() {
-        return maxItems > 0;
+        return m_maxItems > 0;
     }
 
     std::array<int, 6> isBuildingItem();
@@ -89,7 +109,7 @@ public:
 
     // set
     void setSelected(bool value) {
-        selected = value;
+        m_selected = value;
     }
 
     void setStatusPendingUpgrade(int subListId);
@@ -99,31 +119,31 @@ public:
     void setStatusAvailable(int subListId);
 
     void setButtonIconIdPressed(int iconId) {
-        buttonIconIdPressed = iconId;
+        m_buttonIconIdPressed = iconId;
     }
 
     void setButtonIconIdUnpressed(int iconId) {
-        buttonIconIdUnpressed = iconId;
+        m_buttonIconIdUnpressed = iconId;
     }
 
     void setButtonWidth(int value) {
-        buttonWidth = value;
+        m_buttonWidth = value;
     }
 
     void setButtonHeight(int value) {
-        buttonHeight = value;
+        m_buttonHeight = value;
     }
 
     void setButtonDrawX(int value) {
-        buttonDrawX = value;
+        m_buttonDrawX = value;
     }
 
     void setButtonDrawY(int value) {
-        buttonDrawY = value;
+        m_buttonDrawY = value;
     }
 
     void setLastClickedId(int value) {
-        lastClickedId = value;
+        m_lastClickedId = value;
     }
 
     /**
@@ -131,19 +151,27 @@ public:
     * @param value
     */
     eListType getType() {
-        return typeOfList;
+        return m_listType;
+    }
+
+    [[nodiscard]] bool isType(const eListType type) const
+    {
+        return m_listType == type;
     }
 
     void removeAllSublistItems(int sublistId);
 
+    void clearList();
+
     void resetTimesOrderedForAllItems();
 
     void setItemBuilder(cItemBuilder *value);
+    void serviceInit(sGameServices* services);
 
     void startFlashing();
 
     bool isFlashing() {
-        return TIMER_flashing > 0;
+        return m_TIMER_flashing > 0;
     }
 
     Color getFlashingColor();
@@ -156,26 +184,30 @@ protected:
     // nothing
 
 private:
-    int lastClickedId;    // last clicked item id
-    int buttonIconIdPressed;    // the button to draw at the left of the list when pressed (selected)
-    int buttonIconIdUnpressed;    // the button to draw at the left of the list when unpressed
-    int buttonDrawX;
-    int buttonDrawY;
-    int buttonWidth;
-    int buttonHeight;
+    int m_lastClickedId;    // last clicked item id
+    int m_buttonIconIdPressed;    // the button to draw at the left of the list when pressed (selected)
+    int m_buttonIconIdUnpressed;    // the button to draw at the left of the list when unpressed
+    int m_buttonDrawX;
+    int m_buttonDrawY;
+    int m_buttonWidth;
+    int m_buttonHeight;
 
-    int TIMER_flashing;
+    int m_TIMER_flashing;
 
-    int maxItems;         // how many items have been set in the list?
+    int m_maxItems;         // how many items have been set in the list?
 
-    bool selected;          // is this list selected at sidebar or not?
+    bool m_selected;          // is this list selected at sidebar or not?
 
     // the list of icons
-    cBuildingListItem *items[MAX_ITEMS];
+    cBuildingListItem *m_items[MAX_ITEMS];
 
     cItemBuilder *m_itemBuilder;
+    cInfoContext* m_info = nullptr;
+    cGameSettings* m_settings = nullptr;
+    cEventEmitter* m_eventEmitter = nullptr;
+    cScreenFader* m_screenFader = nullptr;
 
     int getFreeSlot();
 
-    eListType typeOfList;
+    eListType m_listType;
 };


=== PORT: src/sidebar/cBuildingListFactory.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingListFactory.cpp
stdout:
diff --git a/src/sidebar/cBuildingListFactory.cpp b/src/sidebar/cBuildingListFactory.cpp
index cf6e0573..600a1b4a 100644
--- a/src/sidebar/cBuildingListFactory.cpp
+++ b/src/sidebar/cBuildingListFactory.cpp
@@ -1,22 +1,24 @@
-#include "cBuildingListFactory.h"
+/**
+ * @file cBuildingListFactory.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
-#include "d2tmc.h"
+#include "cBuildingListFactory.h"
+#include "game/cGameSettings.h"
 #include "data/gfxinter.h"
 
-cBuildingListFactory *cBuildingListFactory::instance = NULL;
-
-cBuildingListFactory::cBuildingListFactory()
-{
-}
-
-cBuildingListFactory *cBuildingListFactory::getInstance()
-{
-    if (instance == nullptr) {
-        instance = new cBuildingListFactory();
-    }
-
-    return instance;
-}
+cBuildingListFactory::cBuildingListFactory(cGameSettings* settings) : m_settings(settings)
+{}
 
 int cBuildingListFactory::getButtonDrawY()
 {
@@ -27,13 +29,13 @@ int cBuildingListFactory::getButtonDrawY()
 
 int cBuildingListFactory::getButtonDrawXStart()
 {
-    return (game.m_screenW - 200) + 2;
+    return (m_settings->getScreenW() - 200) + 2;
 }
 
 
 void cBuildingListFactory::initializeList(cBuildingList *list, eListType listType)
 {
-    assert(list != NULL);
+    d2tm_assert(list != nullptr);
 
     // first clear the list
     list->removeAllItems();
@@ -115,10 +117,3 @@ cBuildingList *cBuildingListFactory::createList(eListType listType)
     initializeList(list, listType);
     return list;
 }
-
-void cBuildingListFactory::destroy()
-{
-    if (instance) {
-        delete instance;
-    }
-}


=== PORT: src/sidebar/cBuildingListItem.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingListItem.cpp
stdout:
diff --git a/src/sidebar/cBuildingListItem.cpp b/src/sidebar/cBuildingListItem.cpp
index ea84a91b..0ba04f36 100644
--- a/src/sidebar/cBuildingListItem.cpp
+++ b/src/sidebar/cBuildingListItem.cpp
@@ -1,56 +1,79 @@
+/**
+ * @file cBuildingListItem.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #include "cBuildingListItem.h"
 
-#include "d2tmc.h"
+#include "utils/Log.h"
+#include "utils/common.h"
 #include "sidebar/cBuildingList.h"
-
+#include "context/cInfoContext.h"
+#include "game/cGameSettings.h"
 #include <format>
+#include "include/cAssert.h"
+#include "gameobjects/cSpecialInfos.h"
+#include "gameobjects/cUpgradeInfo.h"
+#include "gameobjects/structures/cStructureInfo.h"
+#include "gameobjects/units/cUnitInfos.h"
 
 cBuildingListItem::cBuildingListItem(eBuildType type, int buildId, int cost, int icon, cBuildingList *list, int subList, bool queuable)
 {
-    assert(buildId >= 0);
-    this->icon = icon;
-    this->buildId = buildId;
-    this->type = type;
-    this->cost = cost;
-    building = false;
-    state = AVAILABLE;
-    progress = 0;
-    buildFrameToDraw = 0;
-    timesToBuild = 0;
-    timesOrdered  = 0;
-    slotId = -1; // is set later
-
-    creditsPerProgressTime = 0;
-    placeIt = false;
-    deployIt = false;
-    this->queuable = queuable;
+    d2tm_assert(buildId >= 0);
+    m_icon = icon;
+    m_buildId = buildId;
+    m_type = type;
+    m_cost = cost;
+    m_state = AVAILABLE;
+    m_progress = 0;
+    m_buildFrameToDraw = 0;
+    m_timesToBuild = 0;
+    m_timesOrdered  = 0;
+    m_slotId = -1; // is set later
+
+    m_creditsPerProgressTime = 0;
+    m_placeIt = false;
+    m_waitingForUnitSlot = false;
+    m_deployIt = false;
+    m_queuable = queuable;
 
 //    this->totalBuildTime = totalBuildTime;
-    this->subList = subList;
+    m_subList = subList;
 
-    TIMER_progressFrame = 0.0f;
-    TIMER_flashing = 500;
+    m_TIMER_progressFrame = 0.0f;
+    m_TIMER_flashing = 500;
 
-    timerCap = game.isDebugMode() ? cBuildingListItem::DebugTimerCap : cBuildingListItem::DefaultTimerCap;
+    m_timerCap = DefaultTimerCap;
 
-    myList = list; // this can be nullptr! (it will be set from the outside by cBuildingList convenience methods)
-
-    int totalBuildTime = getTotalBuildTime();
-    if (cost > 0 && totalBuildTime > 0) {
-        creditsPerProgressTime = (float)this->cost / (float)totalBuildTime;
-    }
-
-    if (game.isDebugMode()) {
-        logbook(std::format("cBuildingListItem constructor [{}], cost = {}, totalBuildTime = {}, creditsPerProgressTime = {}",
-                            getNameString().c_str(), cost, totalBuildTime, creditsPerProgressTime));
-
-    }
+    m_myList = list; // this can be nullptr! (it will be set from the outside by cBuildingList convenience methods)
 
+    Logger::debug(COMP_STRUCTURES, "cBuildingListItem", "constructor [type={}, id={}], cost = {}", eBuildTypeString(m_type), m_buildId, m_cost);
 }
 
 cBuildingListItem::~cBuildingListItem()
 {
-    myList = NULL;
+    m_myList = nullptr;
+}
+
+void cBuildingListItem::serviceInit(cInfoContext* info, cGameSettings* settings)
+{
+    m_info = info;
+    m_settings = settings;
+    m_timerCap = m_settings->isCheatMode() ? DebugTimerCap : DefaultTimerCap;
+    int totalBuildTime = getTotalBuildTime();
+    if (m_cost > 0 && totalBuildTime > 0) {
+        m_creditsPerProgressTime = static_cast<float>(m_cost) / static_cast<float>(totalBuildTime);
+    }
 }
 
 /**
@@ -113,6 +136,10 @@ cBuildingListItem::cBuildingListItem(int theID, s_UnitInfo entry, int subList) :
 {
 }
 
+cBuildingListItem::cBuildingListItem(int theID, s_UpgradeInfo entry) : cBuildingListItem(theID, entry, entry.providesTypeSubList)
+{
+}
+
 cBuildingListItem::cBuildingListItem(int theID, s_UpgradeInfo entry, int subList) : cBuildingListItem(theID, entry, nullptr, subList)
 {
 }
@@ -123,16 +150,11 @@ cBuildingListItem::cBuildingListItem(int theID, s_UpgradeInfo entry, int subList
  */
 float cBuildingListItem::getRefundAmount()
 {
-    float fProgress = progress;
+    float fProgress = m_progress;
     if (fProgress < 1.0F) {
         return 0.0F;
     }
-    return (fProgress * creditsPerProgressTime);
-}
-
-void cBuildingListItem::decreaseTimesToBuild()
-{
-    timesToBuild--;
+    return (fProgress * m_creditsPerProgressTime);
 }
 
 void cBuildingListItem::increaseProgress(int byAmount)
@@ -147,17 +169,17 @@ void cBuildingListItem::increaseProgress(int byAmount)
  */
 int cBuildingListItem::getTotalBuildTime() const
 {
-    if (type == STRUCTURE) {
-        return sStructureInfo[buildId].buildTime;
+    if (m_type == STRUCTURE) {
+        return m_info->getStructureInfo(m_buildId).buildTime;
     }
-    if (type == UPGRADE) {
-        return sUpgradeInfo[buildId].buildTime;
+    if (m_type == UPGRADE) {
+        return m_info->getUpgradeInfo(m_buildId).buildTime;
     }
-    if (type == SPECIAL) {
-        return sSpecialInfo[buildId].buildTime;
+    if (m_type == SPECIAL) {
+        return m_info->getSpecialInfo(m_buildId).buildTime;
     }
     // assumes units by default
-    return sUnitInfo[buildId].buildTime;
+    return m_info->getUnitInfo(m_buildId).buildTime;
 }
 
 bool cBuildingListItem::isDoneBuilding()
@@ -194,51 +216,51 @@ s_UpgradeInfo &cBuildingListItem::getUpgradeInfo()
 {
     int buildId = getBuildId();
     if (getBuildType() != eBuildType::UPGRADE) {
-        logbook("ERROR!!! - calling getUpgradeInfo while type is not UPGRADE! - falling back to buildId 1 as safety");
+        Logger::error(COMP_STRUCTURES, "cBuildingListItem::getUpgradeInfo", "type is not UPGRADE - falling back to buildId 1 as safety");
         buildId = 1;
     }
-    return sUpgradeInfo[buildId];
+    return m_info->getUpgradeInfo(buildId);
 }
 
 s_SpecialInfo &cBuildingListItem::getSpecialInfo()
 {
     int buildId = getBuildId();
     if (getBuildType() != eBuildType::SPECIAL) {
-        logbook("ERROR!!! - calling gets_Special while type is not SPECIAL! - falling back to buildId 1 as safety");
+        Logger::error(COMP_STRUCTURES, "cBuildingListItem::getSpecialInfo", "type is not SPECIAL - falling back to buildId 1 as safety");
         buildId = 1;
     }
-    return sSpecialInfo[buildId];
+    return m_info->getSpecialInfo(buildId);
 }
 
 s_UnitInfo &cBuildingListItem::getUnitInfo()
 {
     int buildId = getBuildId();
     if (getBuildType() != eBuildType::UNIT) {
-        logbook("ERROR!!! - calling getUnitInfo while type is not UNIT! - falling back to buildId 1 as safety");
+        Logger::error(COMP_STRUCTURES, "cBuildingListItem::getUnitInfo", "type is not UNIT - falling back to buildId 1 as safety");
         buildId = 1;
     }
-    return sUnitInfo[buildId];
+    return m_info->getUnitInfo(buildId);
 }
 
 s_StructureInfo &cBuildingListItem::getStructureInfo()
 {
     int buildId = getBuildId();
     if (getBuildType() != eBuildType::STRUCTURE) {
-        logbook("ERROR!!! - calling getStructureInfo while type is not STRUCTURE! - falling back to buildId 1 as safety");
+        Logger::error(COMP_STRUCTURES, "cBuildingListItem::getStructureInfo", "type is not STRUCTURE - falling back to buildId 1 as safety");
         buildId = 1;
     }
-    return sStructureInfo[buildId];
+    return m_info->getStructureInfo(buildId);
 }
 
 void cBuildingListItem::resetTimesOrdered()
 {
-    timesOrdered = 0;
+    m_timesOrdered = 0;
 }
 
 eListType cBuildingListItem::getListType()
 {
-    if (myList) {
-        return myList->getType();
+    if (m_myList) {
+        return m_myList->getType();
     }
     return eListType::LIST_NONE;
 }
@@ -246,8 +268,8 @@ eListType cBuildingListItem::getListType()
 int cBuildingListItem::calculateBuildProgressFrameBasedOnBuildProgress()
 {
     // frame to draw (for building in progress)
-//    int iFrame = health_bar(31, progress, getTotalBuildTime());
-    int iFrame = healthBar(31, progress, getTotalBuildTime());
+//    int iFrame = health_bar(31, m_progress, getTotalBuildTime());
+    int iFrame = healthBar(31, m_progress, getTotalBuildTime());
 
     if (iFrame > 31) {
         iFrame = 31;
@@ -258,12 +280,12 @@ int cBuildingListItem::calculateBuildProgressFrameBasedOnBuildProgress()
 
 void cBuildingListItem::decreaseProgressFrameTimer()
 {
-    TIMER_progressFrame--;
+    m_TIMER_progressFrame--;
 }
 
 float cBuildingListItem::getProgressFrameTimer()
 {
-    return TIMER_progressFrame;
+    return m_TIMER_progressFrame;
 }
 
 void cBuildingListItem::resetProgressFrameTimer()
@@ -272,10 +294,10 @@ void cBuildingListItem::resetProgressFrameTimer()
     // divide that by frames (31), and get the time between frames!
     int buildTimeInTicks = getTotalBuildTimeInTicks();
     if (buildTimeInTicks > 0) {
-        TIMER_progressFrame = buildTimeInTicks / 31;
+        m_TIMER_progressFrame = buildTimeInTicks / 31;
     }
     else {
-        TIMER_progressFrame = 0;
+        m_TIMER_progressFrame = 0;
     }
 }
 
@@ -286,12 +308,12 @@ int cBuildingListItem::getTotalBuildTimeInTicks() const
 
 int cBuildingListItem::getInTicks(int getTimeInTicks) const
 {
-    return timerCap * getTimeInTicks;
+    return m_timerCap * getTimeInTicks;
 }
 
 void cBuildingListItem::setTimerCap(int value)
 {
-    timerCap = value;
+    m_timerCap = value;
 }
 
 /**
@@ -311,24 +333,24 @@ int cBuildingListItem::getTotalBuildTimeInMs()
  */
 int cBuildingListItem::getProgressBuildTimeInMs()
 {
-    return getInTicks(progress) * 5; // 5 = ms for every time we call the itemBuilder
+    return getInTicks(m_progress) * 5; // 5 = ms for every time we call the itemBuilder
 }
 
-int cBuildingListItem::getTotalBuildTimeInTicks(eBuildType type, int buildId)
+int cBuildingListItem::getTotalBuildTimeInTicks(eBuildType type, int buildId, cInfoContext* info)
 {
     int buildTime = 0;
     switch (type) {
         case UNIT:
-            buildTime = sUnitInfo[buildId].buildTime;
+            buildTime = info->getUnitInfo(buildId).buildTime;
             break;
         case STRUCTURE:
-            buildTime = sStructureInfo[buildId].buildTime;
+            buildTime = info->getStructureInfo(buildId).buildTime;
             break;
         case SPECIAL:
-            buildTime = sSpecialInfo[buildId].buildTime;
+            buildTime = info->getSpecialInfo(buildId).buildTime;
             break;
         case UPGRADE:
-            buildTime = sUpgradeInfo[buildId].buildTime;
+            buildTime = info->getUpgradeInfo(buildId).buildTime;
             break;
         case BULLET:
         default:
@@ -338,18 +360,18 @@ int cBuildingListItem::getTotalBuildTimeInTicks(eBuildType type, int buildId)
     return buildTime * 35;
 }
 
-int cBuildingListItem::getListId(eBuildType type, int buildId)
+int cBuildingListItem::getListId(eBuildType type, int buildId, cInfoContext* info)
 {
     switch (type) {
         case UNIT:
-            return eListTypeAsInt(sUnitInfo[buildId].listType);
+            return eListTypeAsInt(info->getUnitInfo(buildId).listType);
         case STRUCTURE:
-            return sStructureInfo[buildId].list;
+            return info->getStructureInfo(buildId).list;
         case SPECIAL:
-            return eListTypeAsInt(sSpecialInfo[buildId].listType);
+            return eListTypeAsInt(info->getSpecialInfo(buildId).listType);
             break;
         case UPGRADE:
-//            return sUpgradeInfo[buildId].;
+//            return info->getUpgradeInfo(buildId).;
             return eListTypeAsInt(eListType::LIST_UPGRADES);
             break;
         default:
@@ -357,11 +379,11 @@ int cBuildingListItem::getListId(eBuildType type, int buildId)
     }
 }
 
-bool cBuildingListItem::isAutoBuild(eBuildType type, int buildId)
+bool cBuildingListItem::isAutoBuild(eBuildType type, int buildId, cInfoContext* info)
 {
     switch (type) {
         case SPECIAL:
-            return sSpecialInfo[buildId].autoBuild;
+            return info->getSpecialInfo(buildId).autoBuild;
         default:
             return false;
     }
@@ -369,7 +391,7 @@ bool cBuildingListItem::isAutoBuild(eBuildType type, int buildId)
 
 bool cBuildingListItem::isAutoBuild()
 {
-    return cBuildingListItem::isAutoBuild(type, buildId);
+    return cBuildingListItem::isAutoBuild(m_type, m_buildId, m_info);
 }
 
 std::string cBuildingListItem::getInfo()
@@ -391,7 +413,7 @@ std::string cBuildingListItem::getInfo()
             msg = std::format("${} | {} | {} Secs", getBuildCost(), unitType.name, seconds);
         }
         else {
-            msg = std::format("{} | {} Secs", sUnitInfo[getBuildId()].name, seconds);
+            msg = std::format("{} | {} Secs", m_info->getUnitInfo(getBuildId()).name, seconds);
         }
     }
     else if (isTypeUpgrade()) {
@@ -410,17 +432,17 @@ std::string cBuildingListItem::getInfo()
 
 bool cBuildingListItem::isFlashing()
 {
-    return TIMER_flashing > 0;
+    return m_TIMER_flashing > 0;
 }
 
 void cBuildingListItem::decreaseFlashingTimer()
 {
-    if (TIMER_flashing > 0) TIMER_flashing--;
+    if (m_TIMER_flashing > 0) m_TIMER_flashing--;
 }
 
 std::string cBuildingListItem::getTypeString()
 {
-    return std::string(eBuildTypeString(this->type));
+    return std::string(eBuildTypeString(m_type));
 }
 
 std::string cBuildingListItem::getNameString()


=== PORT: src/sidebar/cBuildingListItem.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingListItem.h
stdout:
diff --git a/src/sidebar/cBuildingListItem.h b/src/sidebar/cBuildingListItem.h
index dae2191b..d7a670e3 100644
--- a/src/sidebar/cBuildingListItem.h
+++ b/src/sidebar/cBuildingListItem.h
@@ -1,3 +1,18 @@
+/**
+ * @file cBuildingListItem.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /**
  * a cListItem is  used within a BuildingList , it has a picture and any unit or
  * structure ID attached. At the same time this item is responsible for 'building'
@@ -7,11 +22,18 @@
  */
 #pragma once
 
-#include "structs.h"
-
 #include <string>
+#include "include/enums/BuildEnums.h"
+#include "include/enums/ListEnums.h"
 
 class cBuildingList;
+class cInfoContext;
+class cGameSettings;
+struct s_SpecialInfo;
+struct s_UpgradeInfo;
+struct s_UnitInfo;
+struct s_StructureInfo;
+struct s_TerrainInfo;
 
 class cBuildingListItem {
 
@@ -25,7 +47,9 @@ public:
     cBuildingListItem(int theID, s_StructureInfo entry, int subList);
     cBuildingListItem(int theID, s_SpecialInfo entry, int subList);
     cBuildingListItem(int theID, s_UnitInfo entry, int subList);
-    cBuildingListItem(int theID, s_UpgradeInfo entry, int subList);
+    cBuildingListItem(int theID, s_UpgradeInfo entry);
+
+    void serviceInit(cInfoContext* info, cGameSettings* settings);
 
     static const int DefaultTimerCap = 35;
     static const int DebugTimerCap = 2;
@@ -34,7 +58,7 @@ public:
     int getTotalBuildTimeInMs();
     int getProgressBuildTimeInMs(); // how much time has passed for build item
     int getIconId() {
-        return icon;
+        return m_icon;
     }
     std::string getInfo();
 
@@ -48,7 +72,7 @@ public:
      * @return
      */
     int getBuildId() {
-        return buildId;
+        return m_buildId;
     }
 
     /**
@@ -56,23 +80,26 @@ public:
      * @return
      */
     int getSubList() {
-        return subList;
+        return m_subList;
     }
 
     eBuildType getBuildType() {
-        return type;
+        return m_type;
     }
     int getBuildCost() const {
-        return cost;
+        return m_cost;
     }
     int getProgress() {
-        return progress;
+        return m_progress;
     }
     bool isBuilding() {
-        return building;
+        return isState(eBuildingListItemState::BUILDING) || isState(eBuildingListItemState::PAUSED);
+    }
+    bool isPaused() {
+        return isState(eBuildingListItemState::PAUSED);
     }
     bool isState(eBuildingListItemState value) {
-        return state == value;
+        return m_state == value;
     }
 
     /**
@@ -80,7 +107,7 @@ public:
      * @return
      */
     bool isAvailable() {
-        return isState(eBuildingListItemState::AVAILABLE);
+        return isState(eBuildingListItemState::AVAILABLE) || isState(eBuildingListItemState::BUILDING);
     }
 
     /**
@@ -100,13 +127,13 @@ public:
     }
 
     int getTimesToBuild() {
-        return timesToBuild;
+        return m_timesToBuild;
     }
     int getSlotId() {
-        return slotId;    // return index of items[] array (set after adding item to list, default is < 0)
+        return m_slotId;    // return index of items[] array (set after adding item to list, default is < 0)
     }
     int getTimesOrdered() {
-        return timesOrdered;
+        return m_timesOrdered;
     }
 
     s_SpecialInfo &getSpecialInfo();
@@ -115,86 +142,93 @@ public:
     s_StructureInfo &getStructureInfo();
 
     float getCreditsPerProgressTime() {
-        return creditsPerProgressTime;
+        return m_creditsPerProgressTime;
     }
 
     float getRefundAmount();
 
     bool shouldPlaceIt() {
-        return placeIt;
+        return m_placeIt;
     }
     bool shouldDeployIt() {
-        return deployIt;
+        return m_deployIt;
     }
     bool isQueuable() {
-        return queuable;
+        return m_queuable;
+    }
+
+    void pauseBuilding() {
+        m_state = eBuildingListItemState::PAUSED;
+    }
+    void resumeBuilding() {
+        m_state = eBuildingListItemState::BUILDING;
+    }
+    void cancelBuilding() {
+        m_state = eBuildingListItemState::AVAILABLE;
+        m_waitingForUnitSlot = false;
+        resetProgress();
+    }
+    void startBuilding() {
+        m_state = eBuildingListItemState::BUILDING;
     }
 
     // setters
     void setIconId(int value) {
-        icon = value;
+        m_icon = value;
     }
     void setBuildCost(int value) {
-        cost = value;
-    }
-    void setIsBuilding(bool value) {
-        building = value;
-    }
-    void stopBuilding() {
-        setIsBuilding(false);
-        resetProgress();
+        m_cost = value;
     }
     void setStatusPendingUpgrade() {
-        state = eBuildingListItemState::PENDING_UPGRADE;
+        m_state = eBuildingListItemState::PENDING_UPGRADE;
     }
     void setStatusAvailable() {
-        state = eBuildingListItemState::AVAILABLE;
+        m_state = eBuildingListItemState::AVAILABLE;
     }
     void setStatusPendingBuilding() {
-        state = eBuildingListItemState::PENDING_BUILDING;
-    }
-    void setIsAvailable(bool value) {
-        value ? state = eBuildingListItemState::AVAILABLE : eBuildingListItemState::UNAVAILABLE;
-    }
-    void setTimesToBuild(int value) {
-        timesToBuild = value;
-    }
-    void setTimesOrdered(int value) {
-        timesOrdered = value;
+        m_state = eBuildingListItemState::PENDING_BUILDING;
     }
     void increaseTimesToBuild() {
-        timesToBuild++;
+        m_timesToBuild++;
     }
     void increaseTimesToBuildNTimes(int amount) {
-        if (queuable) {
-            timesToBuild += amount;
+        if (m_queuable) {
+            m_timesToBuild += amount;
         }
         else {
-            timesToBuild = 1; // not queueable always means 1
+            m_timesToBuild = 1; // not queueable always means 1
         }
     }
-    void decreaseTimesToBuild();
+    void decreaseTimesToBuild() {
+        m_timesToBuild--;
+    }
     void increaseTimesOrdered() {
-        timesOrdered++;
+        m_timesOrdered++;
     }
     void decreaseTimesOrdered() {
-        timesOrdered--;
+        m_timesOrdered--;
     }
     void setSlotId(int value) {
-        slotId = value;
+        m_slotId = value;
     }
     void setPlaceIt(bool value) {
-        placeIt = value;
+        m_placeIt = value;
+    }
+    void setWaitingForUnitSlot(bool value) {
+        m_waitingForUnitSlot = value;
+    }
+    bool isWaitingForUnitSlot() const {
+        return m_waitingForUnitSlot;
     }
     void setDeployIt(bool value) {
-        deployIt = value;
+        m_deployIt = value;
     }
     void setList(cBuildingList *theList) {
-        myList = theList;
+        m_myList = theList;
     }
 
     cBuildingList *getList() {
-        return myList;    // returns the list it belongs to
+        return m_myList;    // returns the list it belongs to
     }
 
     /**
@@ -206,9 +240,9 @@ public:
     void increaseProgress(int byAmount);
 
     void resetProgress() {
-        progress = 0;
-        buildFrameToDraw = 0;
-        TIMER_progressFrame = 0.0f;
+        m_progress = 0;
+        m_buildFrameToDraw = 0;
+        m_TIMER_progressFrame = 0.0f;
     }
 
     int getTotalBuildTime() const;
@@ -223,10 +257,10 @@ public:
     void resetTimesOrdered();
 
     void increaseBuildProgressFrame() {
-        buildFrameToDraw++;
+        m_buildFrameToDraw++;
     }
     int getBuildProgressFrame() {
-        return buildFrameToDraw;
+        return m_buildFrameToDraw;
     }
 
     int calculateBuildProgressFrameBasedOnBuildProgress();
@@ -241,9 +275,9 @@ public:
 
     int getTotalBuildTimeInTicks() const;
 
-    static int getTotalBuildTimeInTicks(eBuildType type, int buildId);
-    static int getListId(eBuildType type, int buildId);
-    static bool isAutoBuild(eBuildType type, int buildId);
+    static int getTotalBuildTimeInTicks(eBuildType type, int buildId, cInfoContext* info);
+    static int getListId(eBuildType type, int buildId, cInfoContext* info);
+    static bool isAutoBuild(eBuildType type, int buildId, cInfoContext* info);
 
     bool isAutoBuild();
 
@@ -252,34 +286,38 @@ public:
     void decreaseFlashingTimer();
 
 private:
-    void setProgress(int value) {
-        progress = value;
-    }
-
-    int icon;				// the icon ID to draw (from datafile)
-    int buildId;			// the ID to build .. (ie TRIKE, or CONSTYARD)
-    eBuildType type;		// .. of this type of thing (ie, UNIT or STRUCTURE)
-    int cost;				// price
-    bool building;			// building this item? (default = false)
-    eBuildingListItemState state;
-    int progress;			// progress building this item
-    int buildFrameToDraw;   // for the progress drawing
-    int timesToBuild;		// the amount of times to build this item (queueing) (meaning, when building = true, this should be 1...)
-    int timesOrdered;		// the amount of times this item has been ordered (starport related)
-    int slotId;			 	// return index of items[] array (set after adding item to list, default is < 0)
-
-    float creditsPerProgressTime; // credits to pay for each progress point. (calculated at creation)
-    bool placeIt;			// when true, this item is ready for placement
-    bool deployIt;			// when true, this item is ready for deployment (FYI, super weapons)
-    bool queuable;			// when true, this item can be ordered multiple times to build
-
-    int subList;            // subList id's allow us to distinguish built items within the same buildingList.
-
-    float TIMER_progressFrame; // timer used for progress drawing animation
-    int TIMER_flashing;        // if > 0 then this item is 'flashing'
-    int timerCap;           // passed in by item builder (determined by power outage, etc)
+    cBuildingListItem(int theID, s_UpgradeInfo entry, int subList);
 
-    cBuildingList *myList;
+    void setProgress(int value) {
+        m_progress = value;
+    }
+
+    int m_icon;				// the icon ID to draw (from datafile)
+    int m_buildId;			// the ID to build .. (ie TRIKE, or CONSTYARD)
+    eBuildType m_type;		// .. of this type of thing (ie, UNIT or STRUCTURE)
+    int m_cost;				// price
+    eBuildingListItemState m_state;
+    int m_progress;			// progress building this item
+    int m_buildFrameToDraw;   // for the progress drawing
+    int m_timesToBuild;		// the amount of times to build this item (queueing) (meaning, when building = true, this should be 1...)
+    int m_timesOrdered;		// the amount of times this item has been ordered (starport related)
+    int m_slotId;			 	// return index of items[] array (set after adding item to list, default is < 0)
+
+    float m_creditsPerProgressTime; // credits to pay for each progress point. (calculated at creation)
+    bool m_placeIt;			// when true, this item is ready for placement
+    bool m_waitingForUnitSlot;	// when true, this unit is done building but waits for a free unit slot
+    bool m_deployIt;			// when true, this item is ready for deployment (FYI, super weapons)
+    bool m_queuable;			// when true, this item can be ordered multiple times to build
+
+    int m_subList;            // subList id's allow us to distinguish built items within the same buildingList.
+
+    float m_TIMER_progressFrame; // timer used for progress drawing animation
+    int m_TIMER_flashing;        // if > 0 then this item is 'flashing'
+    int m_timerCap;           // passed in by item builder (determined by power outage, etc)
+
+    cBuildingList *m_myList;
+    cInfoContext* m_info = nullptr;
+    cGameSettings* m_settings = nullptr;
 
     cBuildingListItem(int theID, s_StructureInfo entry, cBuildingList *list, int subList);
     cBuildingListItem(int theID, s_UnitInfo entry, cBuildingList *list, int subList);


=== PORT: src/sidebar/cBuildingListUpdater.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cBuildingListUpdater.cpp
stdout:
diff --git a/src/sidebar/cBuildingListUpdater.cpp b/src/sidebar/cBuildingListUpdater.cpp
index 61ab9147..4d071f5d 100644
--- a/src/sidebar/cBuildingListUpdater.cpp
+++ b/src/sidebar/cBuildingListUpdater.cpp
@@ -1,34 +1,58 @@
-#include "cBuildingListUpdater.h"
+/**
+ * @file cBuildingListUpdater.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cBuildingListUpdater.h"
 #include "building/cItemBuilder.h"
-#include "d2tmc.h"
-#include "player/cPlayer.h"
-#include "utils/cLog.h"
+#include "gameobjects/players/cPlayer.h"
+#include "utils/Log.h"
+#include "sidebar/cSideBar.h"
+#include "gameobjects/structures/cOrderProcesser.h"
+#include "context/cInfoContext.h"
+#include "game/cGameSettings.h"
+#include "include/sGameServices.h"
 
 #include <format>
-
-#include <cassert>
+#include "include/cAssert.h"
+#include "gameobjects/structures/cStructureInfo.h"
 
 cBuildingListUpdater::cBuildingListUpdater(cPlayer *thePlayer)
 {
-    assert(thePlayer);
-    player = thePlayer;
+    d2tm_assert(thePlayer!=nullptr);
+    m_player = thePlayer;
+}
+
+void cBuildingListUpdater::serviceInit(sGameServices* services)
+{
+    m_info = services->info;
+    m_settings = services->settings;
 }
 
 void cBuildingListUpdater::onStructureCreated(int structureType)
 {
-    player->log("onStructureCreated - begin");
+    m_player->log("onStructureCreated - begin");
 
-    if (player->isHuman()) {
+    if (m_player->isHuman()) {
         // always strict (skirmish) mode. Which means, do not cheat...
         onStructureCreatedSkirmishMode(structureType);
         evaluateUpgrades();
     }
     else {
-        // AI players...
+        // AI m_players...
 
-        if (game.m_skirmish) {
-            // on skirmish mode use the 'strict' / no cheating mode (same as human players)
+        if (m_settings->isSkirmish()) {
+            // on skirmish mode use the 'strict' / no cheating mode (same as human m_players)
             onStructureCreatedSkirmishMode(structureType);
             evaluateUpgrades();
         }
@@ -39,37 +63,36 @@ void cBuildingListUpdater::onStructureCreated(int structureType)
         }
     }
 
-    player->logStructures();
-    player->log("onStructureCreated - end");
+    m_player->logStructures();
+    m_player->log("onStructureCreated - end");
 }
 
 void cBuildingListUpdater::onStructureCreatedCampaignMode(int structureType) const
 {
 
     // this is (should be) only called by the AI and in Campaign mode.
-    // there the AI only re-builds things. The tech-tree used for players makes no sense if you compare it
+    // there the AI only re-builds things. The tech-tree used for m_players makes no sense if you compare it
     // with the AI. The AI can build anything, even with low power. For example, mission 9 has AI's with low
     // power (yet their turrets should work), but also they don't have all structures to have others (ie, there
-    // is a PALACE, but AI players do not have the prerequisites for such a structure).
+    // is a PALACE, but AI m_players do not have the prerequisites for such a structure).
     //
     // long story short: we give the AI the ability to build *any* structure (and *any* unit, though that is
-    // limited to techLevel so the AI can't build things that the player cant unit-wise).
+    // limited to techLevel so the AI can't build things that the m_player cant unit-wise).
 
     // activate/deactivate any lists if needed
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listConstYard = sideBar->getList(eListType::LIST_CONSTYARD);
     cBuildingList *listFootUnits = sideBar->getList(eListType::LIST_FOOT_UNITS);
     cBuildingList *listUnits = sideBar->getList(eListType::LIST_UNITS);
 
-    int house = player->getHouse();
-    int techLevel = player->getTechLevel();
+    int house = m_player->getHouse();
+    int techLevel = m_player->getTechLevel();
 
-    cLogger::getInstance()->log(LOG_TRACE, COMP_STRUCTURES, "onStructureCreatedCampaignMode",
-                                std::format("For player [{}], structureType [{}], techlevel [{}], house [{}]", player->getId(), structureType, techLevel, house));
+    Logger::trace(COMP_STRUCTURES, "cBuildingListUpdater::onStructureCreatedCampaignMode", "For m_player [{}], structureType [{}], techlevel [{}], house [{}]", m_player->getId(), structureType, techLevel, house);
 
-    assert(listConstYard);
-    assert(listFootUnits);
-    assert(listConstYard);
+    d2tm_assert(listConstYard);
+    d2tm_assert(listFootUnits);
+    d2tm_assert(listConstYard);
 
     if (structureType == CONSTYARD) {
         // add items
@@ -147,17 +170,28 @@ void cBuildingListUpdater::onStructureCreatedCampaignMode(int structureType) con
         if (house == ATREIDES) {
             listUnits->addUnitToList(SONICTANK, SUBLIST_HEAVYFCTRY);
         }
-        else if (house == HARKONNEN || house == SARDAUKAR) {
+        else if (house == HARKONNEN) {
             listUnits->addUnitToList(DEVASTATOR, SUBLIST_HEAVYFCTRY);
         }
         else if (house == ORDOS) {
             listUnits->addUnitToList(DEVIATOR, SUBLIST_HEAVYFCTRY);
         }
+        else if (house == SARDAUKAR) {
+            if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_SONICTANK)) {
+                listUnits->addUnitToList(SONICTANK, SUBLIST_HEAVYFCTRY);
+            }
+            if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVASTATOR)) {
+                listUnits->addUnitToList(DEVASTATOR, SUBLIST_HEAVYFCTRY);
+            }
+            if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVIATOR)) {
+                listUnits->addUnitToList(DEVIATOR, SUBLIST_HEAVYFCTRY);
+            }
+        }
     }
 
     if (structureType == HIGHTECH) {
         listUnits->addUnitToList(CARRYALL, SUBLIST_HIGHTECH);
-        if (house == ATREIDES || house == ORDOS) {
+        if (house != HARKONNEN) {
             listUnits->addUnitToList(ORNITHOPTER, SUBLIST_HIGHTECH);
         }
     }
@@ -172,12 +206,13 @@ void cBuildingListUpdater::onStructureCreatedCampaignMode(int structureType) con
         list->addUnitToList(MCV, 0);
         list->addUnitToList(HARVESTER, 0);
         list->addUnitToList(LAUNCHER, 0);
+		list->addUnitToList(CARRYALL, 0);
 
         if (techLevel > 6) {
             list->addUnitToList(SIEGETANK, 0);
         }
 
-        if (techLevel > 7 && (house != HARKONNEN && house != SARDAUKAR)) {
+        if (techLevel > 7 && (house != HARKONNEN)) {
             list->addUnitToList(ORNITHOPTER, 0);
         }
     }
@@ -205,42 +240,58 @@ void cBuildingListUpdater::onStructureCreatedCampaignMode(int structureType) con
 void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) const
 {
     // activate/deactivate any lists if needed
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listConstYard = sideBar->getList(eListType::LIST_CONSTYARD);
     cBuildingList *listFootUnits = sideBar->getList(eListType::LIST_FOOT_UNITS);
     cBuildingList *listUnits = sideBar->getList(eListType::LIST_UNITS);
 
-    int house = player->getHouse();
-    int techLevel = player->getTechLevel();
+    int house = m_player->getHouse();
+    int techLevel = m_player->getTechLevel();
 
-    assert(listConstYard);
-    assert(listFootUnits);
-    assert(listConstYard);
+    d2tm_assert(listConstYard);
+    d2tm_assert(listFootUnits);
+    d2tm_assert(listConstYard);
 
     if (structureType == CONSTYARD) {
         // add items
         listConstYard->addStructureToList(SLAB1, 0);
-        player->log("onStructureCreated - added SLAB1 to list");
+        m_player->log("onStructureCreated - added SLAB1 to list");
 
         if (techLevel >= 2) {
-            if (house == ATREIDES || house == ORDOS) {
+            if (house != HARKONNEN) {
                 listConstYard->addStructureToList(BARRACKS, 0);
-                player->log("onStructureCreated - added BARRACKS to list");
+                m_player->log("onStructureCreated - added BARRACKS to list");
             }
             if (house == HARKONNEN) {
                 listConstYard->addStructureToList(WOR, 0);
-                player->log("onStructureCreated - added WOR to list");
+                m_player->log("onStructureCreated - added WOR to list");
             }
         }
 
         if (techLevel >= 4) {
             //list->addItemToList(new cBuildingListItem(SLAB4, structures[SLAB4])); // only available after upgrading
             listConstYard->addStructureToList(WALL, 0);
-            player->log("onStructureCreated - added WALL to list");
+            m_player->log("onStructureCreated - added WALL to list");
         }
 
         listConstYard->addStructureToList(WINDTRAP, 0);
-        player->log("onStructureCreated - added WINDTRAP to list");
+        m_player->log("onStructureCreated - added WINDTRAP to list");
+
+        // a rebuilt ConstYard: re-add what the structures we still own make available
+        for (int type = 0; type < MAX_STRUCTURETYPES; type++) {
+            if (type == CONSTYARD) continue;
+            if (!m_player->hasAtleastOneStructure(type)) continue;
+            onStructureCreatedSkirmishMode(type);
+        }
+    }
+
+	if (structureType == BARRACKS) {
+		if (techLevel >= 4) {
+			if (house == SARDAUKAR) {
+				listConstYard->addStructureToList(WOR, 0);
+				m_player->log("onStructureCreated - added WOR to list");
+			}
+		}
     }
 
     if (structureType == WINDTRAP) {
@@ -257,17 +308,18 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
         list->addUnitToList(MCV, 0);
         list->addUnitToList(HARVESTER, 0);
         list->addUnitToList(LAUNCHER, 0);
+		list->addUnitToList(CARRYALL, 0);
 
         if (techLevel > 6) {
             list->addUnitToList(SIEGETANK, 0);
         }
 
-        if (techLevel > 7 && (house != HARKONNEN && house != SARDAUKAR)) {
+        if (techLevel > 7 && house != HARKONNEN) {
             list->addUnitToList(ORNITHOPTER, 0);
         }
 
         // TODO: use events for this
-        player->getOrderProcesser()->updatePricesForStarport();
+        m_player->getOrderProcesser()->updatePricesForStarport();
     }
 
     if (structureType == REFINERY) {
@@ -280,13 +332,13 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
                     house == FREMEN) {
                 listConstYard->addStructureToList(BARRACKS, 0);
 
-                if (house == ORDOS && techLevel >= 5) {
+                if (house == ORDOS && techLevel >= 4) {
                     listConstYard->addStructureToList(WOR, 0);
                 }
             }
             else if (
                 house == HARKONNEN ||
-                house == SARDAUKAR ||
+                // house == SARDAUKAR ||
                 house == FREMEN ||
                 house == MERCENARY) {
                 listConstYard->addStructureToList(WOR, 0);
@@ -303,15 +355,15 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
         if (techLevel >= 5) {
             listConstYard->addStructureToList(TURRET, 0);
         }
-
-        if (techLevel >= 8) {
-            listConstYard->addStructureToList(PALACE, 0);
-        }
     }
 
+	if (structureType == IX) { //already techlevel 7, but we want to add palace only when IX is built, not when techlevel is 7 (since the player might not have built IX yet)
+				listConstYard->addStructureToList(PALACE, 0);
+	}
+
     if (structureType == STARPORT) {
         // House of IX is available if Starport is built
-        if (techLevel >= 8) {
+        if (techLevel >= 7) {
             listConstYard->addStructureToList(IX, 0);
         }
     }
@@ -330,7 +382,7 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
             listConstYard->addStructureToList(STARPORT, 0);
         }
 
-        if (house == ATREIDES) {
+        if (house == ATREIDES || house == SARDAUKAR) {
             listUnits->addUnitToList(TRIKE, SUBLIST_LIGHTFCTRY);
         }
         else if (house == ORDOS) {
@@ -341,7 +393,6 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
         }
         else {
             listUnits->addUnitToList(TRIKE, SUBLIST_LIGHTFCTRY);
-            listUnits->addUnitToList(RAIDER, SUBLIST_LIGHTFCTRY);
             listUnits->addUnitToList(QUAD, SUBLIST_LIGHTFCTRY);
         }
     }
@@ -368,26 +419,41 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
 
     // Heavyfactory
     if (techLevel >= 7) {
-        if (player->hasAtleastOneStructure(HEAVYFACTORY) &&
-                player->hasAtleastOneStructure(IX)) {
-            if (player->getHouse() == ATREIDES) {
+        if (m_player->hasAtleastOneStructure(HEAVYFACTORY) &&
+            m_player->hasAtleastOneStructure(IX)) {
+
+            if (m_player->getHouse() == ATREIDES) {
                 listUnits->addUnitToList(SONICTANK, SUBLIST_HEAVYFCTRY);
             }
-            else if (player->getHouse() == HARKONNEN) {
+            else if (m_player->getHouse() == HARKONNEN) {
                 listUnits->addUnitToList(DEVASTATOR, SUBLIST_HEAVYFCTRY);
             }
-            else if (player->getHouse() == ORDOS) {
+            else if (m_player->getHouse() == ORDOS) {
                 listUnits->addUnitToList(DEVIATOR, SUBLIST_HEAVYFCTRY);
+            } else if (m_player->getHouse() == SARDAUKAR) {
+                if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_SONICTANK)) {
+                    listUnits->addUnitToList(SONICTANK, SUBLIST_HEAVYFCTRY);
+                }
+                if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVASTATOR)) {
+                    listUnits->addUnitToList(DEVASTATOR, SUBLIST_HEAVYFCTRY);
+                }
+                if (m_player->isUpgradeApplied(UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVIATOR)) {
+                    listUnits->addUnitToList(DEVIATOR, SUBLIST_HEAVYFCTRY);
+                }
             }
         }
         else {
-            if (player->getHouse() == ATREIDES) {
+            if (m_player->getHouse() == ATREIDES) {
                 listUnits->removeItemFromListByBuildId(SONICTANK);
             }
-            else if (player->getHouse() == HARKONNEN) {
+            else if (m_player->getHouse() == HARKONNEN) {
                 listUnits->removeItemFromListByBuildId(DEVASTATOR);
             }
-            else if (player->getHouse() == ORDOS) {
+            else if (m_player->getHouse() == ORDOS) {
+                listUnits->removeItemFromListByBuildId(DEVIATOR);
+            } else if (m_player->getHouse() == SARDAUKAR) {
+                listUnits->removeItemFromListByBuildId(SONICTANK);
+                listUnits->removeItemFromListByBuildId(DEVASTATOR);
                 listUnits->removeItemFromListByBuildId(DEVIATOR);
             }
         }
@@ -420,45 +486,48 @@ void cBuildingListUpdater::onStructureCreatedSkirmishMode(int structureType) con
 /**
  * A structure of *structureType* got destroyed...
  *
- * This is called *after* the structure count has been updated. Ie you can use player->hasAtleastOneStructure() because
+ * This is called *after* the structure count has been updated. Ie you can use m_player->hasAtleastOneStructure() because
  * it already is updated to the new state.
  *
  * @param structureType
  */
 void cBuildingListUpdater::onStructureDestroyed(int structureType)
 {
-    player->log("onStructureDestroyed - begin");
+    m_player->log("onStructureDestroyed - begin");
 
     // activate/deactivate any lists if needed
-    cSideBar *sideBar = player->getSideBar();
-    cItemBuilder *pItemBuilder = player->getItemBuilder();
+    cSideBar *sideBar = m_player->getSideBar();
+    cItemBuilder *pItemBuilder = m_player->getItemBuilder();
     cBuildingList *listConstYard = sideBar->getList(eListType::LIST_CONSTYARD);
 
     if (structureType == STARPORT) {
-        if (!player->hasAtleastOneStructure(STARPORT)) {
+        if (!m_player->hasAtleastOneStructure(STARPORT)) {
             listConstYard->removeItemFromListByBuildId(IX);
-            cOrderProcesser *pProcesser = player->getOrderProcesser();
+            cOrderProcesser *pProcesser = m_player->getOrderProcesser();
             pProcesser->clear();
             cBuildingList *listStarport = sideBar->getList(eListType::LIST_STARPORT);
-            listStarport->resetTimesOrderedForAllItems();
+            listStarport->clearList();
+            if (sideBar->getSelectedListID() == eListTypeAsInt(eListType::LIST_STARPORT)) {
+                sideBar->findFirstActiveListAndSelectIt();
+            }
         }
     }
 
-    if (!player->hasAtleastOneStructure(CONSTYARD)) {
+    if (!m_player->hasAtleastOneStructure(CONSTYARD)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_CONSTYARD, SUBLIST_CONSTYARD);
         listConstYard->removeAllSublistItems(SUBLIST_CONSTYARD);
     }
 
-    if (player->isHuman()) {
+    if (m_player->isHuman()) {
         // always strict (skirmish) mode. Which means, do not cheat...
         onStructureDestroyedSkirmishMode();
         evaluateUpgrades();
     }
     else {
-        // AI players...
+        // AI m_players...
 
-        if (game.m_skirmish) {
-            // on skirmish mode use the 'strict' / no cheating mode (same as human players)
+        if (m_settings->isSkirmish()) {
+            // on skirmish mode use the 'strict' / no cheating mode (same as human m_players)
             onStructureDestroyedSkirmishMode();
             evaluateUpgrades();
         }
@@ -469,74 +538,85 @@ void cBuildingListUpdater::onStructureDestroyed(int structureType)
         }
     }
 
-    player->logStructures();
-    player->log("onStructureDestroyed - end");
+    m_player->logStructures();
+    m_player->log("onStructureDestroyed - end");
 }
 
 
 void cBuildingListUpdater::evaluateUpgrades()
 {
-    player->log("evaluateUpgrades - start");
-    cSideBar *sideBar = player->getSideBar();
+    m_player->log("evaluateUpgrades - start");
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listUpgrades = sideBar->getList(eListType::LIST_UPGRADES);
 
     for (int i = 0; i < MAX_UPGRADETYPES; i++) {
-        s_UpgradeInfo &upgradeInfo = sUpgradeInfo[i];
+        s_UpgradeInfo &upgradeInfo = m_info->getUpgradeInfo(i);
         if (!upgradeInfo.enabled) continue;
         // check techlevel (this is a non-changing value per mission, usually coupled with mission nr, ie
         // mission 1 = techlevel 1. Mission 9 = techlevel 9. Skirmish is usually techlevel 9.
-        if (player->getTechLevel() < upgradeInfo.techLevel) continue;
+        if (m_player->getTechLevel() < upgradeInfo.techLevel) continue;
 
-        if (!(upgradeInfo.house & player->getHouseBitFlag())) {
-            // house specific upgradeInfo, player house does not match
-            player->log(std::format("Upgrade [{}] has not same house.", upgradeInfo.description));
+        if (!(upgradeInfo.house & m_player->getHouseBitFlag())) {
+            // house specific upgradeInfo, m_player house does not match
+            m_player->log(std::format("Upgrade [{}] has not same house.", upgradeInfo.description));
             continue;
         }
 
         bool addToUpgradesList = true;
 
-        // check if player has structure to upgrade
-        bool hasRequiredStructureType = player->hasAtleastOneStructure(upgradeInfo.structureType);
+        // check if m_player has structure to upgrade
+        bool hasRequiredStructureType = m_player->hasAtleastOneStructure(upgradeInfo.structureType);
         if (!hasRequiredStructureType) {
             addToUpgradesList = false;
-            player->log(std::format("Upgrade [{}] has not required structureType (upgradeInfo.structureType) #1 [{}].",
-                                    upgradeInfo.description, sStructureInfo[upgradeInfo.structureType].name));
+            m_player->log(std::format("Upgrade [{}] has not required structureType (upgradeInfo.structureType) #1 [{}].",
+                                    upgradeInfo.description, m_info->getStructureInfo(upgradeInfo.structureType).name));
         }
 
-        // check if player has the additional structure (if required)
+        // check if m_player has the additional structure (if required)
         if (upgradeInfo.needsStructureType > -1) {
-            hasRequiredStructureType = player->hasAtleastOneStructure(upgradeInfo.needsStructureType);
-            if (!hasRequiredStructureType) {
+            if (!m_player->hasAtleastOneStructure(upgradeInfo.needsStructureType)) {
+                // do not overwrite: a missing upgradeInfo.structureType (ie the ConstYard) must stay missing
+                hasRequiredStructureType = false;
                 addToUpgradesList = false;
-                player->log(std::format("Upgrade [{}] has not required additional structureType (upgradeInfo.needsStructureType) [{}].",
-                                        upgradeInfo.description, sStructureInfo[upgradeInfo.needsStructureType].name));
+                m_player->log(std::format("Upgrade [{}] has not required additional structureType (upgradeInfo.needsStructureType) [{}].",
+                                        upgradeInfo.description, m_info->getStructureInfo(upgradeInfo.needsStructureType).name));
             }
         }
 
-        // check if the structure to upgradeInfo is at the expected level
-        int structureUpgradeLevel = player->getStructureUpgradeLevel(upgradeInfo.structureType);
-
-        if (structureUpgradeLevel != upgradeInfo.atUpgradeLevel) {
-            // already at correct upgradeInfo level, no = comparison because that means it should be offered
-            if (structureUpgradeLevel > upgradeInfo.atUpgradeLevel) {
-                // this upgradeInfo has been executed already, so apply again,
-                // but only if we have the required structure(s)
+        // check if the upgrade has been done already / is at the expected level
+        if (upgradeInfo.dependsOnStructureLevel) {
+            int structureUpgradeLevel = m_player->getStructureUpgradeLevel(upgradeInfo.structureType);
+
+            if (structureUpgradeLevel != upgradeInfo.atUpgradeLevel) {
+                // already at correct upgradeInfo level, no = comparison because that means it should be offered
+                if (structureUpgradeLevel > upgradeInfo.atUpgradeLevel) {
+                    // this upgradeInfo has been executed already, so apply again,
+                    // but only if we have the required structure(s)
+                    if (hasRequiredStructureType) {
+                        applyUpgrade(upgradeInfo);
+                        m_player->log(std::format(
+                                        "Upgrade [{}] has already been achieved, so re-apply. StructureUpgradeLevel={} and upgradeInfo.atUpgradeLevel={}.",
+                                        upgradeInfo.description, structureUpgradeLevel, upgradeInfo.atUpgradeLevel));
+                    }
+                    else {
+                        m_player->log(std::format(
+                                        "Upgrade [{}] has already been achieved, But will not be re-applied because required (additional) structure type is/are present.",
+                                        upgradeInfo.description));
+                    }
+                }
+                addToUpgradesList = false;
+                m_player->log(std::format(
+                                "Upgrade [{}] will not be offered because it has a different atUpgradeLevel. StructureUpgradeLevel={} and upgradeInfo.atUpgradeLevel={} not required additional structureType (upgradeInfo.needsStructureType).",
+                                upgradeInfo.description, structureUpgradeLevel, upgradeInfo.atUpgradeLevel));
+            }
+        } else {
+            if (m_player->isUpgradeApplied(i)) {
                 if (hasRequiredStructureType) {
                     applyUpgrade(upgradeInfo);
-                    player->log(std::format(
-                                    "Upgrade [{}] has already been achieved, so re-apply. StructureUpgradeLevel={} and upgradeInfo.atUpgradeLevel={}.",
-                                    upgradeInfo.description, structureUpgradeLevel, upgradeInfo.atUpgradeLevel));
-                }
-                else {
-                    player->log(std::format(
-                                    "Upgrade [{}] has already been achieved, But will not be re-applied because required (additional) structure type is/are present.",
-                                    upgradeInfo.description));
+                    m_player->log(std::format("Upgrade [{}] has already been applied independently, so re-apply.", upgradeInfo.description));
                 }
+                addToUpgradesList = false;
             }
-            addToUpgradesList = false;
-            player->log(std::format(
-                            "Upgrade [{}] will not be offered because it has a different atUpgradeLevel. StructureUpgradeLevel={} and upgradeInfo.atUpgradeLevel={} not required additional structureType (upgradeInfo.needsStructureType).",
-                            upgradeInfo.description, structureUpgradeLevel, upgradeInfo.atUpgradeLevel));
         }
 
         if (addToUpgradesList) {
@@ -548,15 +628,14 @@ void cBuildingListUpdater::evaluateUpgrades()
             if (item) {
                 if (item->isBuilding() && !item->isDoneBuilding()) {
                     // DUPLICATION OF cSidebar::thinkInteraction, line ~ 195!
-                    cLogger::getInstance()->log(LOG_INFO, COMP_BUILDING_LIST_UPDATER, "Cancel upgrading", "Upgrade no longer available, aborted mid-way upgrading so refunding.");
+                    Logger::info(COMP_BUILDING_LIST_UPDATER, "Cancel upgrading", "Upgrade no longer available, aborted mid-way upgrading so refunding.");
                     // only give money back for item that is being built
                     if (item->isBuilding()) {
                         // calculate the amount of money back:
-                        player->giveCredits(item->getRefundAmount());
+                        m_player->giveCredits(item->getRefundAmount());
                     }
-                    item->setIsBuilding(false);
-                    item->resetProgress();
-                    cItemBuilder *itemBuilder = player->getItemBuilder();
+                    item->cancelBuilding();
+                    cItemBuilder *itemBuilder = m_player->getItemBuilder();
                     itemBuilder->removeItemFromList(item);
                 }
             }
@@ -566,7 +645,7 @@ void cBuildingListUpdater::evaluateUpgrades()
         }
     }
 
-    player->log("evaluateUpgrades - end");
+    m_player->log("evaluateUpgrades - end");
 }
 
 /**
@@ -574,17 +653,21 @@ void cBuildingListUpdater::evaluateUpgrades()
  */
 void cBuildingListUpdater::onUpgradeCompleted(cBuildingListItem *item)
 {
-    assert(item);
+    d2tm_assert(item);
     if (!item->isTypeUpgrade()) {
-        player->log("ERROR ERROR ERROR! -> the provided item is NOT an upgrade type!");
-        assert(false && "the provided item is NOT an upgrade type!");
+        m_player->log("ERROR ERROR ERROR! -> the provided item is NOT an upgrade type!");
+        d2tm_assert(false && "the provided item is NOT an upgrade type!");
         return;
     }
 
     const s_UpgradeInfo &upgradeType = item->getUpgradeInfo();
 
     // Upgrade structure + provide any unit or structure
-    player->increaseStructureUpgradeLevel(upgradeType.structureType);
+    if (upgradeType.dependsOnStructureLevel) {
+        m_player->increaseStructureUpgradeLevel(upgradeType.structureType);
+    } else {
+        m_player->setUpgradeApplied(item->getBuildId());
+    }
 
     applyUpgrade(upgradeType);
 
@@ -600,14 +683,20 @@ void cBuildingListUpdater::onUpgradeCompleted(cBuildingListItem *item)
  */
 void cBuildingListUpdater::applyUpgrade(const s_UpgradeInfo &upgradeInfo)
 {
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     eListType listType = upgradeInfo.providesTypeList;
     int subListType = upgradeInfo.providesTypeSubList;
 
-    cBuildingList *listBeingUpgraded = sideBar->getList(listType);
-    listBeingUpgraded->setStatusAvailable(subListType);
+    // when re-applying an earlier upgrade while the next upgrade of the same list is still in progress,
+    // keep the list blocked until that upgrade is done (#1048). When the upgrade itself just completed,
+    // cItemBuilder calls onUpgradeCompleted only after its progress reached the build time, so it counts as done.
+    cBuildingListItem *upgradeInProgress = m_player->isUpgradingList(listType, subListType);
+    if (upgradeInProgress == nullptr || upgradeInProgress->isDoneBuilding()) {
+        cBuildingList *listBeingUpgraded = sideBar->getList(listType);
+        listBeingUpgraded->setStatusAvailable(subListType);
+    }
 
-    assert(upgradeInfo.providesTypeId > -1);
+    d2tm_assert(upgradeInfo.providesTypeId > -1);
 
     cBuildingList *list = sideBar->getList(listType);
     if (upgradeInfo.providesType == UNIT) {
@@ -627,9 +716,9 @@ void cBuildingListUpdater::applyUpgrade(const s_UpgradeInfo &upgradeInfo)
  */
 void cBuildingListUpdater::onUpgradeStarted(cBuildingListItem *pItem)
 {
-    assert(pItem);
-    assert(pItem->isTypeUpgrade() && "Expected type upgrade");
-    cSideBar *sideBar = player->getSideBar();
+    d2tm_assert(pItem);
+    d2tm_assert(pItem->isTypeUpgrade() && "Expected type upgrade");
+    cSideBar *sideBar = m_player->getSideBar();
 
     // get the structure type it is upgrading
     const s_UpgradeInfo &upgrade = pItem->getUpgradeInfo();
@@ -647,11 +736,11 @@ void cBuildingListUpdater::onUpgradeStarted(cBuildingListItem *pItem)
  */
 void cBuildingListUpdater::onUpgradeCancelled(cBuildingListItem *pItem)
 {
-    player->log("onUpgradeCancelled - start");
-    assert(pItem);
-    assert(pItem->isTypeUpgrade() && "Expected type Upgrade for onUpgradeCancelled");
+    m_player->log("onUpgradeCancelled - start");
+    d2tm_assert(pItem);
+    d2tm_assert(pItem->isTypeUpgrade() && "Expected type Upgrade for onUpgradeCancelled");
 
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
 
     // get the structure type it is upgrading
     const s_UpgradeInfo &upgrade = pItem->getUpgradeInfo();
@@ -661,12 +750,12 @@ void cBuildingListUpdater::onUpgradeCancelled(cBuildingListItem *pItem)
     cBuildingList *listBeingUpgraded = sideBar->getList(listType);
     listBeingUpgraded->setStatusAvailable(subListType);
 
-    player->log("onUpgradeCancelled - end");
+    m_player->log("onUpgradeCancelled - end");
 }
 
 void cBuildingListUpdater::onBuildItemCancelled(cBuildingListItem *pItem)
 {
-    player->log("onBuildItemCancelled - start");
+    m_player->log("onBuildItemCancelled - start");
     if (pItem == nullptr) return;
     if (pItem->isTypeUpgrade()) {
         onUpgradeCancelled(pItem);
@@ -674,11 +763,11 @@ void cBuildingListUpdater::onBuildItemCancelled(cBuildingListItem *pItem)
     }
 
     // it is a unit/structure/special
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listUpgrades = sideBar->getList(eListType::LIST_UPGRADES);
     listUpgrades->setStatusAvailable(pItem->getSubList());
 
-    player->log("onBuildItemCancelled - end");
+    m_player->log("onBuildItemCancelled - end");
 }
 
 /**
@@ -699,7 +788,7 @@ void cBuildingListUpdater::onBuildItemStarted(cBuildingListItem *pItem)
     }
 
     // it is a unit/structure/special
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listUpgrades = sideBar->getList(eListType::LIST_UPGRADES);
     listUpgrades->setStatusPendingBuilding(pItem->getSubList());
 }
@@ -713,7 +802,7 @@ void cBuildingListUpdater::onBuildItemCompleted(cBuildingListItem *pItem)
     if (pItem == nullptr) return;
     if (pItem->isTypeUpgrade()) {
         // do nothing, this is normally called via OnUpgradeCompleted, see method above.
-        player->log("Wrongfully called onBuildItemCompleted when OnUpgradeCompleted was expected.");
+        m_player->log("Wrongfully called onBuildItemCompleted when OnUpgradeCompleted was expected.");
         return;
     }
 
@@ -724,62 +813,62 @@ void cBuildingListUpdater::onBuildItemCompleted(cBuildingListItem *pItem)
     }
 
     // it is a unit/structure/special
-    cSideBar *sideBar = player->getSideBar();
+    cSideBar *sideBar = m_player->getSideBar();
     cBuildingList *listUpgrades = sideBar->getList(eListType::LIST_UPGRADES);
     listUpgrades->setStatusAvailable(pItem->getSubList());
 }
 
 void cBuildingListUpdater::onStructureDestroyedSkirmishMode() const
 {
-    cSideBar *sideBar = player->getSideBar();
-    cItemBuilder *pItemBuilder = player->getItemBuilder();
+    cSideBar *sideBar = m_player->getSideBar();
+    cItemBuilder *pItemBuilder = m_player->getItemBuilder();
     cBuildingList *listUnits = sideBar->getList(eListType::LIST_UNITS);
     cBuildingList *listFootUnits = sideBar->getList(eListType::LIST_FOOT_UNITS);
 
-    if (player->getTechLevel() >= 7) {
-        if (!player->hasAtleastOneStructure(HEAVYFACTORY) ||
-                !player->hasAtleastOneStructure(IX)) {
-            if (player->getHouse() == ATREIDES) {
+    if (m_player->getTechLevel() >= 7) {
+        if (!m_player->hasAtleastOneStructure(HEAVYFACTORY) ||
+                !m_player->hasAtleastOneStructure(IX)) {
+            if (m_player->getHouse() == ATREIDES) {
                 pItemBuilder->removeItemsByBuildId(UNIT, SONICTANK);
                 listUnits->removeItemFromListByBuildId(SONICTANK);
             }
-            else if (player->getHouse() == HARKONNEN) {
+            else if (m_player->getHouse() == HARKONNEN) {
                 pItemBuilder->removeItemsByBuildId(UNIT, DEVASTATOR);
                 listUnits->removeItemFromListByBuildId(DEVASTATOR);
             }
-            else if (player->getHouse() == ORDOS) {
+            else if (m_player->getHouse() == ORDOS) {
                 pItemBuilder->removeItemsByBuildId(UNIT, DEVIATOR);
                 listUnits->removeItemFromListByBuildId(DEVIATOR);
             }
         }
     }
 
-    if (!player->hasAtleastOneStructure(HIGHTECH)) {
+    if (!m_player->hasAtleastOneStructure(HIGHTECH)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_HIGHTECH);
         listUnits->removeAllSublistItems(SUBLIST_HIGHTECH);
     }
 
-    if (!player->hasAtleastOneStructure(WOR)) {
+    if (!m_player->hasAtleastOneStructure(WOR)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_FOOT_UNITS, SUBLIST_TROOPERS);
         listFootUnits->removeAllSublistItems(SUBLIST_TROOPERS);
     }
 
-    if (!player->hasAtleastOneStructure(BARRACKS)) {
+    if (!m_player->hasAtleastOneStructure(BARRACKS)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_FOOT_UNITS, SUBLIST_INFANTRY);
         listFootUnits->removeAllSublistItems(SUBLIST_INFANTRY);
     }
 
-    if (!player->hasAtleastOneStructure(LIGHTFACTORY)) {
+    if (!m_player->hasAtleastOneStructure(LIGHTFACTORY)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_LIGHTFCTRY);
         listUnits->removeAllSublistItems(SUBLIST_LIGHTFCTRY);
     }
 
-    if (!player->hasAtleastOneStructure(HEAVYFACTORY)) {
+    if (!m_player->hasAtleastOneStructure(HEAVYFACTORY)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_HEAVYFCTRY);
         listUnits->removeAllSublistItems(SUBLIST_HEAVYFCTRY);
     }
 
-    if (!player->hasAtleastOneStructure(PALACE)) {
+    if (!m_player->hasAtleastOneStructure(PALACE)) {
         cBuildingList *listPalace = sideBar->getList(eListType::LIST_PALACE);
         pItemBuilder->removeItemsFromListType(eListType::LIST_PALACE, 0);
         listPalace->removeAllSublistItems(0);
@@ -788,26 +877,26 @@ void cBuildingListUpdater::onStructureDestroyedSkirmishMode() const
 
 void cBuildingListUpdater::onStructureDestroyedCampaignMode() const
 {
-    cSideBar *sideBar = player->getSideBar();
-    cItemBuilder *pItemBuilder = player->getItemBuilder();
+    cSideBar *sideBar = m_player->getSideBar();
+    cItemBuilder *pItemBuilder = m_player->getItemBuilder();
     cBuildingList *listUnits = sideBar->getList(eListType::LIST_UNITS);
 
-    if (!player->hasAtleastOneStructure(HIGHTECH)) {
+    if (!m_player->hasAtleastOneStructure(HIGHTECH)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_HIGHTECH);
         listUnits->removeAllSublistItems(SUBLIST_HIGHTECH);
     }
 
-    if (!player->hasAtleastOneStructure(LIGHTFACTORY)) {
+    if (!m_player->hasAtleastOneStructure(LIGHTFACTORY)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_LIGHTFCTRY);
         listUnits->removeAllSublistItems(SUBLIST_LIGHTFCTRY);
     }
 
-    if (!player->hasAtleastOneStructure(HEAVYFACTORY)) {
+    if (!m_player->hasAtleastOneStructure(HEAVYFACTORY)) {
         pItemBuilder->removeItemsFromListType(eListType::LIST_UNITS, SUBLIST_HEAVYFCTRY);
         listUnits->removeAllSublistItems(SUBLIST_HEAVYFCTRY);
     }
 
-    if (!player->hasAtleastOneStructure(PALACE)) {
+    if (!m_player->hasAtleastOneStructure(PALACE)) {
         cBuildingList *listPalace = sideBar->getList(eListType::LIST_PALACE);
         pItemBuilder->removeItemsFromListType(eListType::LIST_PALACE, 0);
         listPalace->removeAllSublistItems(0);


=== PORT: src/sidebar/cSideBar.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cSideBar.cpp
stdout:
diff --git a/src/sidebar/cSideBar.cpp b/src/sidebar/cSideBar.cpp
index 843fd3b8..55659ade 100644
--- a/src/sidebar/cSideBar.cpp
+++ b/src/sidebar/cSideBar.cpp
@@ -1,34 +1,60 @@
-#include "cSideBar.h"
+/**
+ * @file cSideBar.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cSideBar.h"
+#include "game/cGameSettings.h"
 #include "building/cItemBuilder.h"
-#include "d2tmc.h"
 #include "managers/cDrawManager.h"
-#include "player/cPlayer.h"
-#include "utils/cLog.h"
-#include "utils/cSoundPlayer.h"
+#include "gameobjects/players/cPlayer.h"
+#include "utils/Log.h"
+#include "controls/cGameControlsContext.h"
+#include "gameobjects/structures/cOrderProcesser.h"
+#include "data/gfxaudio.h"
+#include "context/AudioContext.hpp"
+#include "game/cEventEmitter.h"
+#include "context/GameContext.hpp"
+#include "include/sGameServices.h"
 
 #include <format>
 
-#include <cassert>
+#include "gameobjects/structures/cStructureFactory.h"
+#include "gameobjects/units/cUnits.h"
+#include "include/cAssert.h"
+#include "context/cGameObjectContext.h"
+#include "drawers/cBuildingListDrawer.h"
+#include "drawers/cOrderDrawer.h"
+#include <algorithm>
+
 
-#include "data/gfxaudio.h"
 
-cSideBar::cSideBar(cPlayer *thePlayer) : player(thePlayer)
+cSideBar::cSideBar(cPlayer *thePlayer) : m_player(thePlayer)
 {
-    assert(thePlayer != nullptr && "Expected player to be not null!");
-    selectedListID = -1; // nothing is selected
-    isMouseOverSidebarValue = false;
-    memset(lists, 0, sizeof(lists));
+    d2tm_assert(thePlayer != nullptr && "Expected player to be not null!");
+    m_selectedListID = -1; // nothing is selected
+    m_isMouseOverSidebarValue = false;
+    std::fill(std::begin(m_lists), std::end(m_lists), nullptr);
 }
 
 cSideBar::~cSideBar()
 {
     for (int i = 0; i < LIST_MAX; i++) {
-        cBuildingList *pList = lists[i];
+        cBuildingList *pList = m_lists[i];
         if (pList) {
             pList->removeAllItems();
             delete pList; // delete list (also removes pointers within the list)
-            lists[i] = nullptr;
+            m_lists[i] = nullptr;
         }
     }
 }
@@ -36,12 +62,12 @@ cSideBar::~cSideBar()
 void cSideBar::setList(eListType listType, cBuildingList *list)
 {
     int listId = eListTypeAsInt(listType);
-    if (lists[listId]) {
-        logbook("WARNING: Setting list, while list already set. Deleting old entry before assigning new.");
-        delete lists[listId];
+    if (m_lists[listId]) {
+        Logger::warn(COMP_SIDEBAR, "cSideBar::setList", "Setting list while list already set. Deleting old entry before assigning new.");
+        delete m_lists[listId];
     }
 
-    lists[listId] = list;
+    m_lists[listId] = list;
 }
 
 /**
@@ -52,9 +78,17 @@ void cSideBar::think()
     thinkProgressAnimation();
 }
 
+void cSideBar::serviceInit(sGameServices* services)
+{
+    m_drawManager = services->drawManager;
+    m_settings = services->settings;
+    m_audioContext = services->ctx->getAudioContext();
+    m_eventEmitter = services->eventEmitter;
+}
+
 void cSideBar::drawMessageBarWithItemInfo(cBuildingListItem *item) const
 {
-    drawManager->setMessage(item->getInfo());
+    m_drawManager->setMessage(item->getInfo());
 }
 
 bool cSideBar::startBuildingItemIfOk(cBuildingListItem *item) const
@@ -64,14 +98,25 @@ bool cSideBar::startBuildingItemIfOk(cBuildingListItem *item) const
     }
 
     if (item->shouldPlaceIt()) {
-        logbook("Attempting to build an item that is in the \"Place it\" mode - which should not happen - ignoring!");
+        Logger::warn(COMP_SIDEBAR, "cSideBar::startBuildingItemIfOk", "Attempting to build an item that is in Place it mode - which should not happen - ignoring!");
+        return false;
+    }
+
+    if (item->isTypeStructure() &&
+        m_player->getObjects()->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(item->getBuildId())) {
+        m_drawManager->setMessage("Unable to create more.");
+        return false;
+    }
+
+    if (item->isTypeUnit() && !item->getList()->isType(eListType::LIST_STARPORT) && m_player->getObjects()->getUnits()->isUnitLimitReached()) {
+        m_drawManager->setMessage("Unable to create more.");
         return false;
     }
 
     cBuildingList *list = item->getList();
     if (item->isAvailable()) {
         // Item should not be placed, so it can be built
-        cItemBuilder *itemBuilder = player->getItemBuilder();
+        cItemBuilder *itemBuilder = m_player->getItemBuilder();
         bool firstOfItsListType = itemBuilder->isBuildListItemTheFirstOfItsListType(item);
 
         if (item->isQueuable()) {
@@ -104,8 +149,8 @@ bool cSideBar::startBuildingItemIfOk(eListType listType, int buildId) const
         return startBuildingItemIfOk(pItem);
     }
     else {
-        logbook(std::format("ERROR: startBuildingItemIfOk with listType[{}] and buildId[{}] did not find an item to build!",
-                            eListTypeAsInt(listType), buildId ));
+        Logger::error(COMP_SIDEBAR, "cSideBar::startBuildingItemIfOk", "listType[{}] and buildId[{}] did not find an item to build!",
+                      eListTypeAsInt(listType), buildId);
     }
     return false;
 }
@@ -114,7 +159,7 @@ cBuildingListItem *cSideBar::getBuildingListItem(eListType listType, int buildId
 {
     int listId = eListTypeAsInt(listType);
 
-    cBuildingList *pList = lists[listId];
+    cBuildingList *pList = m_lists[listId];
     if (pList == nullptr) return nullptr;
 
     return pList->getItemByBuildId(buildId);
@@ -134,14 +179,14 @@ void cSideBar::thinkProgressAnimation()
 
 void cSideBar::onMouseAt(const s_MouseEvent &event)
 {
-    isMouseOverSidebarValue = event.coords.x > (game.m_screenW - cSideBar::SidebarWidth);
-    drawManager->setKeepMessage(isMouseOverSidebarValue);
+    m_isMouseOverSidebarValue = event.coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth);
+    m_drawManager->setKeepMessage(m_isMouseOverSidebarValue);
 
-    if (selectedListID < 0) return;
+    if (m_selectedListID < 0) return;
 
     // when mouse is selecting a list, and over an item, then draw message bar...!?
-    cBuildingList *list = getList(selectedListID);
-    cBuildingListDrawer *buildingListDrawer = drawManager->getBuildingListDrawer();
+    cBuildingList *list = getList(m_selectedListID);
+    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
     cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
     if (item == nullptr) return;
 
@@ -156,7 +201,7 @@ void cSideBar::onMouseClickedLeft(const s_MouseEvent &event)
 
     // button interaction
     for (int i = startPos; i < LIST_MAX; i++) {
-        if (i == selectedListID) continue; // skip selected list for button interaction
+        if (i == m_selectedListID) continue; // skip selected list for button interaction
         cBuildingList *list = getList(i);
         if (list == nullptr) continue;
         if (!list->isAvailable()) continue; // not available, so no interaction possible
@@ -165,32 +210,32 @@ void cSideBar::onMouseClickedLeft(const s_MouseEvent &event)
         if (list->isOverButton(event.coords.x, event.coords.y)) {
             // clicked on it. Set focus on this one
             setSelectedListId(eListTypeFromInt(i));
-            game.playSound(SOUND_BUTTON, 64); // click sound
+            m_audioContext->playSound(SOUND_BUTTON); // click sound
             break;
         }
     }
 
-    if (selectedListID < 0) return;
+    if (m_selectedListID < 0) return;
 
     // when mouse pressed, build item if over item
-    cBuildingList *list = getList(selectedListID);
+    cBuildingList *list = getList(m_selectedListID);
 
     if (list == nullptr) return;
 
     if (!list->isAvailable()) {
         // unselect this list
-        player->getSideBar()->setSelectedListId(eListType::LIST_NONE);
+        m_player->getSideBar()->setSelectedListId(eListType::LIST_NONE);
         return;
     }
 
-    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();
+    cOrderDrawer *orderDrawer = m_drawManager->getOrderDrawer();
 
     // allow clicking on the order button, send event through...
     if (list->getType() == eListType::LIST_STARPORT) {
         orderDrawer->onNotify(event);
     }
 
-    cBuildingListDrawer *buildingListDrawer = drawManager->getBuildingListDrawer();
+    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
     cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
     if (item == nullptr) return;
 
@@ -200,24 +245,27 @@ void cSideBar::onMouseClickedLeft(const s_MouseEvent &event)
     if (list->getType() != eListType::LIST_STARPORT) {
         // icon is in "Place it" mode, meaning if clicked the "place the thing" state should be set
         if (item->shouldPlaceIt()) {
-            player->setContextMouseState(eMouseState::MOUSESTATE_PLACE);
+            m_player->setContextMouseState(eMouseState::MOUSESTATE_PLACE);
         }
         else if (item->shouldDeployIt()) {
-            player->setContextMouseState(eMouseState::MOUSESTATE_DEPLOY);
+            m_player->setContextMouseState(eMouseState::MOUSESTATE_DEPLOY);
+        }
+        else if (item->isPaused()) {
+            item->startBuilding();
         }
         else {
             startBuildingItemIfOk(item);
         }
     }
     else {
-        cOrderProcesser *orderProcesser = player->getOrderProcesser();
+        cOrderProcesser *orderProcesser = m_player->getOrderProcesser();
 
         // add orders
         if (orderProcesser->acceptsOrders()) {
-            if (player->hasEnoughCreditsFor(item->getBuildCost())) {
+            if (m_player->hasEnoughCreditsFor(item->getBuildCost())) {
                 item->increaseTimesOrdered();
                 orderProcesser->addOrder(item);
-                player->substractCredits(item->getBuildCost());
+                m_player->substractCredits(item->getBuildCost());
             }
         }
     }
@@ -225,23 +273,28 @@ void cSideBar::onMouseClickedLeft(const s_MouseEvent &event)
 
 void cSideBar::onMouseClickedRight(const s_MouseEvent &event)
 {
-    if (selectedListID < 0) return;
+    if (m_selectedListID < 0) return;
 
     // when mouse pressed, build item if over item
-    cBuildingList *list = getList(selectedListID);
+    cBuildingList *list = getList(m_selectedListID);
 
-    cBuildingListDrawer *buildingListDrawer = drawManager->getBuildingListDrawer();
+    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
     cBuildingListItem *item = buildingListDrawer->isOverItemCoordinates(list, event.coords.x, event.coords.y);
     if (item == nullptr) return;
 
     // anything but the starport can 'build' things
     if (list->getType() != eListType::LIST_STARPORT) {
-        cancelBuildingListItem(item);
-    }
-    else {
-        cOrderProcesser *orderProcesser = player->getOrderProcesser();
+        if (!item->isPaused() &&
+            item->isBuilding()) {
+            item->pauseBuilding();
+        }
+        else {
+            cancelBuildingListItem(item);
+        }
+    } else {
+        cOrderProcesser *orderProcesser = m_player->getOrderProcesser();
 
-        assert(orderProcesser);
+        d2tm_assert(orderProcesser);
         if (!orderProcesser->isOrderPlaced()) {
             if (item->getTimesOrdered() > 0) {
                 item->decreaseTimesOrdered();
@@ -259,32 +312,29 @@ void cSideBar::cancelBuildingListItem(cBuildingListItem *item)
         item->setDeployIt(false);
 
         if (item->getTimesToBuild() == 0) {
-            cLogger::getInstance()->log(LOG_TRACE, COMP_SIDEBAR, "Cancel construction", "Item is last item in queue, will give money back.");
+            Logger::trace(COMP_SIDEBAR, "Cancel construction", "Item is last item in queue, will give money back.");
             // only give money back for item that is being built
             if (item->isBuilding()) {
                 // calculate the amount of money back:
-                player->giveCredits(item->getRefundAmount());
-                player->getBuildingListUpdater()->onBuildItemCancelled(item);
+                m_player->giveCredits(item->getRefundAmount());
+                m_player->getBuildingListUpdater()->onBuildItemCancelled(item);
             }
-            item->setIsBuilding(false);
-            item->resetProgress();
+            item->cancelBuilding();
 
             // notify game that the item just has been cancelled, just before the actual removal
-            s_GameEvent newEvent {
+            const s_GameEvent event {
                 .eventType = eGameEventType::GAME_EVENT_LIST_ITEM_CANCELLED,
-                .entityType = item->getBuildType(),
-                .entityID = -1,
-                .player = player,
-                .entitySpecificType = item->getBuildId(),
-                .atCell = -1,
-                .isReinforce = false,
-                .buildingListItem = item
+                .data = BuildingEvent {
+                    .entityType = item->getBuildType(),
+                    .player = m_player,
+                    .entitySpecificType = item->getBuildId(),
+                    .buildingListItem = item
+                }
             };
-
-            game.onNotifyGameEvent(newEvent);
+            m_eventEmitter->emit(event);
             // else, only the number is decreased (used for queueing)
 
-            cItemBuilder *itemBuilder = player->getItemBuilder();
+            cItemBuilder *itemBuilder = m_player->getItemBuilder();
             itemBuilder->removeItemFromList(item);
         }
     }
@@ -292,7 +342,7 @@ void cSideBar::cancelBuildingListItem(cBuildingListItem *item)
 
 void cSideBar::onNotifyMouseEvent(const s_MouseEvent &event)
 {
-    cGameControlsContext *pContext = player->getGameControlsContext();
+    cGameControlsContext *pContext = m_player->getGameControlsContext();
 
     if (!pContext->isMouseOnSidebarOrMinimap()) {
         // we're only interested in mouse movement
@@ -307,6 +357,7 @@ void cSideBar::onNotifyMouseEvent(const s_MouseEvent &event)
             onMouseAt(event);
             return;
         case eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED:
+        case eMouseEventType::MOUSE_LEFT_BUTTON_DOUBLE_CLICKED:
             onMouseClickedLeft(event);
             return;
         case eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED:
@@ -319,87 +370,88 @@ void cSideBar::onNotifyMouseEvent(const s_MouseEvent &event)
 
 void cSideBar::onNotify(const s_GameEvent &event)
 {
-    // event is for specific player, and we are not that player...
-    if (event.player != nullptr && event.player != player) {
-        return;
-    }
-
-    // for us, or for no player in particular
-    switch(event.eventType) {
-        case eGameEventType::GAME_EVENT_SPECIAL_SELECT_TARGET:
-            onSpecialReadyToDeployEvent(event);
-            break;
-        case eGameEventType::GAME_EVENT_LIST_ITEM_PLACE_IT:
-            onListItemReadyToPlaceEvent(event);
-            break;
-        case eGameEventType::GAME_EVENT_LIST_BECAME_AVAILABLE:
-            onListBecameAvailableEvent(event);
-            break;
-        case eGameEventType::GAME_EVENT_LIST_BECAME_UNAVAILABLE:
-            onListBecameUnavailableEvent(event);
-            break;
-        case eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN:
-            findFirstActiveListAndSelectIt();
-            break;
-        default:
-            break;
+    if (const auto *buildEvent = std::get_if<BuildingEvent>(&event.data)) {
+        // event is for specific player, and we are not that player...
+        if (buildEvent->player != nullptr && buildEvent->player != m_player) {
+            return;
+        }
+        // for us, or for no player in particular
+        switch(event.eventType) {
+            case eGameEventType::GAME_EVENT_SPECIAL_SELECT_TARGET:
+                onSpecialReadyToDeployEvent(buildEvent);
+                break;
+            case eGameEventType::GAME_EVENT_LIST_ITEM_PLACE_IT:
+                onListItemReadyToPlaceEvent(buildEvent);
+                break;
+            case eGameEventType::GAME_EVENT_LIST_BECAME_AVAILABLE:
+                onListBecameAvailableEvent(buildEvent);
+                break;
+            case eGameEventType::GAME_EVENT_LIST_BECAME_UNAVAILABLE:
+                onListBecameUnavailableEvent(buildEvent);
+                break;
+            case eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN:
+                findFirstActiveListAndSelectIt();
+                break;
+            default:
+                break;
+        }
     }
 }
 
-void cSideBar::onListItemReadyToPlaceEvent(const s_GameEvent &event) const
+void cSideBar::onListItemReadyToPlaceEvent(const BuildingEvent *event) const
 {
-    event.buildingListItem->getList()->startFlashing();
+    event->buildingListItem->getList()->startFlashing();
 }
 
-void cSideBar::onSpecialReadyToDeployEvent(const s_GameEvent &event) const
+void cSideBar::onSpecialReadyToDeployEvent(const BuildingEvent *event) const
 {
-    event.buildingListItem->getList()->startFlashing();
+    event->buildingListItem->getList()->startFlashing();
 }
 
-void cSideBar::onListBecameAvailableEvent(const s_GameEvent &event)
+void cSideBar::onListBecameAvailableEvent(const BuildingEvent *event)
 {
-    event.buildingList->startFlashing();
+    event->buildingList->startFlashing();
 }
 
-void cSideBar::onListBecameUnavailableEvent(const s_GameEvent &event)
+void cSideBar::onListBecameUnavailableEvent(const BuildingEvent *event)
 {
     cBuildingList *pList = getSelectedList();
-    if (pList == event.buildingList) {
+    if (pList == event->buildingList) {
         findFirstActiveListAndSelectIt();
     }
 }
 
 cBuildingList *cSideBar::getSelectedList() const
 {
-    if (selectedListID < 0) return nullptr;
-    return lists[selectedListID];
+    if (m_selectedListID < 0) return nullptr;
+    return m_lists[m_selectedListID];
 }
 
 void cSideBar::findFirstActiveListAndSelectIt()
 {
-    logbook(std::format("cSideBar::findFirstActiveListAndSelectIt - current selectedListID is [{}]", selectedListID));
+    Logger::info(COMP_SIDEBAR, "cSideBar::findFirstActiveListAndSelectIt", "current m_selectedListID is [{}]", m_selectedListID);
     for (int i = 0; i < LIST_MAX; i++) {
-        cBuildingList *pList = lists[i];
+        cBuildingList *pList = m_lists[i];
         if (pList && pList->isAvailable()) {
             setSelectedListId(eListTypeFromInt(i));
             break;
         }
     }
-    logbook(std::format("cSideBar::findFirstActiveListAndSelectIt - new selectedListID is [{}]", selectedListID));
+    Logger::info(COMP_SIDEBAR, "cSideBar::findFirstActiveListAndSelectIt", "new m_selectedListID is [{}]", m_selectedListID);
 }
 
 void cSideBar::setSelectedListId(eListType value)
 {
-    logbook(std::format("cSideBar::setSelectedListId -  m_PlayerId = [{}] - old value [{}], new [{}]",
-                        player->getId(), selectedListID, eListTypeAsInt(value)));
+    Logger::info(COMP_SIDEBAR, "cSideBar::setSelectedListId", "m_PlayerId = [{}] - old value [{}], new [{}]",
+                 m_player->getId(), m_selectedListID, eListTypeAsInt(value));
 
-    int oldListId = selectedListID;
-    selectedListID = eListTypeAsInt(value);
+    int oldListId = m_selectedListID;
+    m_selectedListID = eListTypeAsInt(value);
     if (oldListId > -1 && oldListId < LIST_MAX) {
-        lists[oldListId]->setSelected(false);
+        m_lists[oldListId]->setSelected(false);
     }
 
-    if (selectedListID > -1 && selectedListID < LIST_MAX) {
-        lists[selectedListID]->setSelected(true);
+    if (m_selectedListID > -1 && m_selectedListID < LIST_MAX) {
+        m_lists[m_selectedListID]->setSelected(true);
     }
 }


=== PORT: src/sidebar/cSideBar.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/sidebar/cSideBar.h
stdout:
diff --git a/src/sidebar/cSideBar.h b/src/sidebar/cSideBar.h
index c2d9ad53..7c5b819e 100644
--- a/src/sidebar/cSideBar.h
+++ b/src/sidebar/cSideBar.h
@@ -1,3 +1,18 @@
+/**
+ * @file cSideBar.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /*
  * cSideBar.h
  *
@@ -16,9 +31,14 @@
 #include "cBuildingList.h"
 #include "cBuildingListItem.h"
 #include "sGameEvent.h"
-#include "sMouseEvent.h"
+#include "controls/sMouseEvent.h"
 
 class cPlayer;
+class cDrawManager;
+class cGameSettings;
+class AudioContext;
+class cEventEmitter;
+struct sGameServices;
 
 //// List ID's corresponding buttons
 //#define LIST_NONE        0
@@ -30,13 +50,13 @@ class cPlayer;
 //#define LIST_UPGRADES    6 // possible upgrades
 //#define LIST_MAX        7 // max amount of lists
 
-#define SUBLIST_CONSTYARD  0  // structures
-#define SUBLIST_LIGHTFCTRY 1 // quad, trike, etc
-#define SUBLIST_HEAVYFCTRY 2 // tanks
-#define SUBLIST_HIGHTECH   3 // orni, carry-all
+inline constexpr int SUBLIST_CONSTYARD = 0;  // structures
+inline constexpr int SUBLIST_LIGHTFCTRY = 1; // quad, trike, etc
+inline constexpr int SUBLIST_HEAVYFCTRY = 2; // tanks
+inline constexpr int SUBLIST_HIGHTECH = 3; // orni, carry-all
 
-#define SUBLIST_INFANTRY   4 // soldier, infantry
-#define SUBLIST_TROOPERS   5 // trooper, troopers
+inline constexpr int SUBLIST_INFANTRY = 4; // soldier, infantry
+inline constexpr int SUBLIST_TROOPERS = 5; // trooper, troopers
 
 /**
  * Basically a container:
@@ -55,7 +75,7 @@ public:
     ~cSideBar();
 
     cBuildingList *getList(int listId) {
-        return lists[listId];
+        return m_lists[listId];
     }
 
     cBuildingList *getList(eListType listType) {
@@ -67,7 +87,7 @@ public:
     void setList(eListType listType, cBuildingList *list);
 
     int getSelectedListID() {
-        return selectedListID;
+        return m_selectedListID;
     }
     cBuildingListItem *getBuildingListItem(eListType listType, int buildId) const;
 
@@ -82,7 +102,7 @@ public:
     static const int VerticalCandyBarWidth = 24;
     static const int SidebarWidthWithoutCandyBar = 200;
     static const int SidebarWidth = SidebarWidthWithoutCandyBar + VerticalCandyBarWidth; // including vertical candy bar
-    static const int TopBarHeight = 42;
+    static constexpr int TopBarHeight = 42;
     static const int HeightOfMinimap = 200 + 8;
     static const int WidthOfMinimap = 200;
     static const int PowerBarMarginHeight = 32; // for a power icon
@@ -95,6 +115,8 @@ public:
     static const int TotalHeightBeforePowerBarStarts =
         TopBarHeight + HeightOfMinimap + HorizontalCandyBarHeight + PowerBarMarginHeight;
 
+    void serviceInit(sGameServices* services);
+
     void onNotifyMouseEvent(const s_MouseEvent &event);
 
     void cancelBuildingListItem(cBuildingListItem *item);
@@ -109,12 +131,16 @@ private:
     void onMouseClickedRight(const s_MouseEvent &event);
 
     // the lists:
-    cBuildingList *lists[LIST_MAX];
-    cPlayer *player;
+    cBuildingList *m_lists[LIST_MAX];
+    cPlayer *m_player;
+    cDrawManager* m_drawManager = nullptr;
+    cGameSettings* m_settings = nullptr;
+    AudioContext* m_audioContext = nullptr;
+    cEventEmitter* m_eventEmitter = nullptr;
 
-    bool isMouseOverSidebarValue;
+    bool m_isMouseOverSidebarValue;
 
-    int selectedListID;
+    int m_selectedListID;
 
     bool startBuildingItemIfOk(cBuildingListItem *item) const;
 
@@ -124,11 +150,11 @@ private:
 
     cBuildingList *getSelectedList() const;
 
-    void onListBecameUnavailableEvent(const s_GameEvent &event);
+    void onListBecameUnavailableEvent(const BuildingEvent *event);
 
-    void onListBecameAvailableEvent(const s_GameEvent &event);
+    void onListBecameAvailableEvent(const BuildingEvent *event);
 
-    void onSpecialReadyToDeployEvent(const s_GameEvent &event) const;
+    void onSpecialReadyToDeployEvent(const BuildingEvent *event) const;
 
-    void onListItemReadyToPlaceEvent(const s_GameEvent &event) const;
+    void onListItemReadyToPlaceEvent(const BuildingEvent *event) const;
 };


=== PORT: src/cGame_logic.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/cGame_logic.cpp
stdout:
diff --git a/src/cGame_logic.cpp b/src/cGame_logic.cpp
deleted file mode 100644
index 45505256..00000000
--- a/src/cGame_logic.cpp
+++ /dev/null
@@ -1,2290 +0,0 @@
-/*
-
-  Dune II - The Maker
-
-  Author : Stefan Hendriks
-  Contact: stefan@fundynamic.com
-  Website: http://dune2themaker.fundynamic.com
-
-  2001 - 2022 (c) code by Stefan Hendriks
-
-*/
-#include "cGame.h"
-#include "include/Texture.hpp"
-#include "building/cItemBuilder.h"
-#include "d2tmc.h"
-#include "config.h"
-#include "data/gfxdata.h"
-#include "data/gfxinter.h"
-#include "drawers/SDLDrawer.hpp"
-#include "gameobjects/particles/cParticle.h"
-#include "gameobjects/projectiles/bullet.h"
-#include "gameobjects/structures/cStructureFactory.h"
-#include "gameobjects/units/cReinforcements.h"
-#include "gamestates/cChooseHouseState.h"
-#include "gamestates/cCreditsState.h"
-#include "gamestates/cMainMenuState.h"
-#include "gamestates/cSelectMissionState.h"
-#include "gamestates/cOptionsState.h"
-#include "gamestates/cSelectYourNextConquestState.h"
-#include "gamestates/cSetupSkirmishState.h"
-#include "ini.h"
-#include "iniDefine.h"
-#include "managers/cDrawManager.h"
-#include "managers/cInteractionManager.h"
-#include "mentat/AtreidesMentat.h"
-#include "mentat/BeneMentat.h"
-#include "mentat/HarkonnenMentat.h"
-#include "mentat/OrdosMentat.h"
-#include "player/cPlayer.h"
-#include "player/brains/cPlayerBrainCampaign.h"
-#include "player/brains/cPlayerBrainSandworm.h"
-#include "player/brains/cPlayerBrainSkirmish.h"
-#include "player/brains/superweapon/cPlayerBrainFremenSuperWeapon.h"
-#include "sidebar/cBuildingListFactory.h"
-#include "sidebar/cSideBarFactory.h"
-#include "utils/RNG.hpp"
-#include "utils/cLog.h"
-#include "utils/cPlatformLayerInit.h"
-#include "utils/cSoundPlayer.h"
-#include "utils/cScreenInit.h"
-#include "utils/d2tm_math.h"
-#include "map/cPreviewMaps.h"
-#include "map/MapGeometry.hpp"
-#include "utils/Color.hpp"
-
-#include "utils/cFileValidator.h"
-#include "utils/cIniFile.h"
-#include "player/cHousesInfo.h"
-#include "utils/Graphics.hpp"
-#include "utils/GameSettings.hpp"
-#include <format>
-#include "context/GameContext.hpp"
-#include "context/ContextCreator.hpp"
-#include "utils/cIniGameRessouces.h"
-
-#include "utils/cScreenShake.h"
-#include "utils/cTimeCounter.h"
-#include "utils/cFocusManager.h"
-
-#include <algorithm>
-#include <random>
-#include <vector>
-#include <iostream>
-
-#include "data/gfxaudio.h"
-
-namespace {
-
-constexpr auto kMinAlpha = 0;
-constexpr auto kMaxAlpha = 255;
-
-}
-
-cGame::cGame()
-{
-    memset(m_states, 0, sizeof(cGameState *));
-
-    m_drawFps = false;
-    m_drawTime = false;
-    m_nextState = -1;
-    m_currentState = nullptr;
-    m_screenW = -1;
-    m_screenH = -1;
-    m_windowed = false;
-    m_allowRepeatingReinforcements = false;
-    m_playSound = true;
-    m_playMusic = true;
-    context = nullptr;
-    ctx = nullptr;
-    m_mentat = nullptr;
-    m_pauseWhenLosingFocus = false;
-
-    // create GameContext
-    ctx = std::make_unique<GameContext>();
-    // create TimeManager
-    std::unique_ptr<cTimeManager> timeManager = std::make_unique<cTimeManager>(this);
-    // local usage
-    m_timeManager = timeManager.get();
-    // send to GameContext
-    ctx->setTimeManager(std::move(timeManager));
-    // focus manager
-    m_focusManager = std::make_unique<cFocusManager>(m_timeManager);
-    // initialisation terrainInfo
-    m_TerrainInfo = std::make_shared<s_TerrainInfo>();
-
-    m_screenShake = std::make_unique<cScreenShake>();
-}
-
-void cGame::applySettings(GameSettings *gs)
-{
-    m_screenW = gs->screenW;
-    m_screenH = gs->screenH;
-    m_cameraDragMoveSpeed = gs->cameraDragMoveSpeed;
-    m_cameraBorderOrKeyMoveSpeed = gs->cameraBorderOrKeyMoveSpeed;
-    m_cameraEdgeMove = gs->cameraEdgeMove;
-    m_windowed = gs->windowed;
-    m_allowRepeatingReinforcements = gs->allowRepeatingReinforcements;
-    m_turretsDownOnLowPower = gs->turretsDownOnLowPower;
-    m_rocketTurretsDownOnLowPower = gs->rocketTurretsDownOnLowPower;
-    m_playMusic = gs->playMusic;
-    m_playSound = gs->playSound;
-    m_debugMode = gs->debugMode;
-    m_drawUnitDebug = gs->drawUnitDebug;
-    m_pauseWhenLosingFocus = gs->pauseWhenLosingFocus;
-    m_disableAI = gs->disableAI;
-    m_oneAi = gs->oneAi;
-    m_disableWormAi = gs->disableWormAi;
-    m_disableReinforcements = gs->disableReinforcements;
-    m_noAiRest = gs->noAiRest;
-    m_drawUsages = gs->drawUsages;
-    m_gameFilename = gs->gameFilename;
-}
-
-void cGame::init()
-{
-    global_map.setTerrainInfo(m_TerrainInfo);
-    m_newMusicSample = MUSIC_MENU;
-    m_newMusicCountdown = 0;
-
-    m_drawFps = false;
-    m_nextState = -1;
-    m_missionWasWon = false;
-    m_currentState = nullptr;
-    m_screenshot = 0;
-    m_playing = true;
-
-    m_TIMER_evaluatePlayerStatus = 5;
-
-    m_skirmish = false;
-    m_PreviewMaps = std::make_shared<cPreviewMaps>(m_debugMode);
-
-    // Alpha (for fading in/out)
-    m_fadeAlpha = kMinAlpha;             // 255 = opaque , anything else
-    m_fadeAction = eFadeAction::FADE_IN; // 0 = NONE, 1 = fade out (go to 0), 2 = fade in (go to 255)
-
-    m_musicVolume = 96; // volume is 0...
-
-    m_pathsCreated = 0;
-
-    setState(GAME_INITIALIZE);
-
-    // mentat
-    delete m_mentat;
-    m_mentat = nullptr;
-
-    m_fadeSelect = 1.0f;
-
-    m_fadeSelectDir = true;    // fade select direction
-
-    m_region = 1;          // what region ? (calumative, from player perspective, NOT the actual region number)
-    m_mission = 0;         // calculated by mission loading (region -> mission calculation)
-
-    m_screenShake->reset();
-
-    m_musicType = -1;
-
-    m_cameraDragMoveSpeed=0.5f;
-    m_cameraBorderOrKeyMoveSpeed=0.5;
-    m_cameraEdgeMove = true;
-
-    global_map.init(64, 64);
-
-    initPlayers(false);
-
-    for (int i = 0; i < MAX_UNITS; i++) {
-        unit[i].init(i);
-    }
-
-    for (int i = 0; i < MAX_PARTICLES; i++) {
-        particle[i].init();
-    }
-
-    // Units & Structures are already initialized in map.init()
-    // Load properties
-    cIni::installGame(m_gameFilename);
-}
-
-// TODO: Bad smell (duplicate code)
-// initialize for missions
-void cGame::missionInit()
-{
-    mapCamera->resetZoom();
-
-    // first 15 seconds, do not evaluate player alive status
-    m_TIMER_evaluatePlayerStatus = 5;
-
-    m_winFlags = 0;
-    m_loseFlags = 0;
-
-    m_musicVolume = 96; // volume is 0...
-
-    m_pathsCreated = 0;
-
-    m_fadeSelect = 1.0f;
-
-    m_fadeSelectDir = true;    // fade select direction
-
-    m_screenShake->reset();
-
-    global_map.init(64, 64);
-
-    initPlayers(true);
-
-    drawManager->missionInit();
-}
-
-void cGame::initPlayers(bool rememberHouse) const
-{
-    int maxThinkingAIs = MAX_PLAYERS;
-    if (m_oneAi) {
-        maxThinkingAIs = 1;
-    }
-
-    for (int i = 0; i < MAX_PLAYERS; i++) {
-        cPlayer &pPlayer = players[i];
-
-        int h = pPlayer.getHouse();
-
-        brains::cPlayerBrain *brain = nullptr;
-        bool autoSlabStructures = false;
-
-        if (i > HUMAN && i < AI_CPU5) {
-            // TODO: playing attribute? (from ai player class?)
-            if (!game.m_disableAI) {
-                if (maxThinkingAIs > 0) {
-                    if (game.m_skirmish) {
-                        brain = new brains::cPlayerBrainSkirmish(&pPlayer);
-                    }
-                    else {
-                        brain = new brains::cPlayerBrainCampaign(&pPlayer);
-                        autoSlabStructures = true;  // campaign based AI's autoslab structures...
-                    }
-                }
-            }
-            maxThinkingAIs--;
-        }
-        else if (i == AI_CPU5) {
-            brain = new brains::cPlayerBrainFremenSuperWeapon(&pPlayer);
-        }
-        else if (i == AI_CPU6) {
-            if (!game.m_disableWormAi) {
-                brain = new brains::cPlayerBrainSandworm(&pPlayer);
-            }
-        }
-
-        pPlayer.init(i, brain);
-        pPlayer.setAutoSlabStructures(autoSlabStructures);
-        if (rememberHouse) {
-            pPlayer.setHouse(h);
-        }
-
-        if (m_skirmish) {
-            pPlayer.setCredits(2500);
-        }
-    }
-}
-
-/**
- * Thinking every second while in combat
- */
-void cGame::thinkSlow_stateCombat_evaluatePlayerStatus()
-{
-    if (m_TIMER_evaluatePlayerStatus > 0) {
-        m_TIMER_evaluatePlayerStatus--;
-    }
-    else {
-        // TODO: Better way is with events (ie created/destroyed). However, there is no such
-        // bookkeeping per player *yet*. So instead, for now, we "poll" for this data.
-        for (int i = 0; i < MAX_PLAYERS; i++) {
-            cPlayer &player = players[i];
-            bool isAlive = player.isAlive();
-            // evaluate all players regardless if they are alive or not (who knows, they became alive?)
-            player.evaluateStillAlive();
-
-            if (isAlive && !player.isAlive()) {
-                s_GameEvent event{
-                    .eventType = eGameEventType::GAME_EVENT_PLAYER_DEFEATED,
-                    .entityType = eBuildType::SPECIAL,
-                    .entityID = -1,
-                    .player = &player
-                };
-
-                game.onNotifyGameEvent(event);
-            }
-            // TODO: event : Player joined/became alive, etc?
-        }
-        m_TIMER_evaluatePlayerStatus = 2;
-    }
-
-    if (isMissionFailed()) {
-        setMissionLost();
-        return;
-    }
-
-    if (isMissionWon()) {
-        setMissionWon();
-        return;
-    }
-}
-
-void cGame::setMissionWon()
-{
-    m_missionWasWon = true;
-    setState(GAME_WINNING);
-
-    m_screenShake->reset();
-    m_mouse->setTile(MOUSE_NORMAL);
-
-    m_soundPlayer->playVoice(SOUND_VOICE_07_ATR, players[HUMAN].getHouse());
-
-    playMusicByType(MUSIC_WIN);
-
-    takeBackGroundScreen();
-}
-
-void cGame::setMissionLost()
-{
-    m_missionWasWon = false;
-    setState(GAME_LOSING);
-
-    m_screenShake->reset();
-    m_mouse->setTile(MOUSE_NORMAL);
-
-    m_soundPlayer->playVoice(SOUND_VOICE_08_ATR, players[HUMAN].getHouse());
-
-    playMusicByType(MUSIC_LOSE);
-
-    takeBackGroundScreen();
-}
-
-bool cGame::isMissionFailed() const
-{
-    if (hasGameOverConditionHarvestForSpiceQuota()) {
-        // check for non-human players if they have met spice quota, if so, they win (and thus human player loses)
-        for (int i = 1; i < MAX_PLAYERS; i++) {
-            cPlayer &player = players[i];
-            if (player.isAlive() && player.hasMetQuota()) {
-                return true;
-            }
-        }
-    }
-
-    if (hasGameOverConditionPlayerHasNoBuildings()) {
-        cPlayer &humanPlayer = players[HUMAN];
-        if (!humanPlayer.isAlive()) {
-            /**
-             * If any of the bits in “LoseFlags” is set and the corresponding condition holds true
-             * the player has won (and the computer has lost)
-             */
-            if (hasWinConditionHumanMustLoseAllBuildings()) {
-                // this means, if any other player has lost all, that player wins, this is not (yet)
-                // supported. Mainly because we can't distinguish yet between 'active' and non-active players
-                // since we have a fixed list of players.
-
-                // so for now just do this:
-                return false; // it is meant to win the game by drawStateLosing all...
-            }
-            else {
-                return true; // nope, it should lose mission now
-            }
-        }
-    }
-
-    return false;
-}
-
-bool cGame::isMissionWon() const
-{
-    cPlayer &humanPlayer = players[HUMAN];
-    if (hasGameOverConditionHarvestForSpiceQuota()) {
-        if (humanPlayer.hasMetQuota()) {
-            return true;
-        }
-    }
-
-    if (hasGameOverConditionPlayerHasNoBuildings()) {
-        if (hasWinConditionHumanMustLoseAllBuildings()) {
-            if (!humanPlayer.isAlive()) {
-                return true;
-            }
-        }
-
-        if (hasWinConditionAIShouldLoseEverything()) {
-            if (allEnemyAIPlayersAreDestroyed()) {
-                return true;
-            }
-        }
-    }
-    else if (hasGameOverConditionAIHasNoBuildings()) {
-        if (hasWinConditionAIShouldLoseEverything()) {
-            if (allEnemyAIPlayersAreDestroyed()) {
-                return true;
-            }
-        }
-    }
-    return false;
-}
-
-bool cGame::allEnemyAIPlayersAreDestroyed() const
-{
-    cPlayer &humanPlayer = players[HUMAN];
-    for (int i = 0; i < MAX_PLAYERS; i++) {
-        if (i == HUMAN || i == AI_WORM || i == AI_CPU5) continue; // do not evaluate these players
-        cPlayer *player = &players[i];
-        if (!player->isAlive()) continue;
-        if (humanPlayer.isSameTeamAs(player)) continue; // skip allied AI players
-        return false;
-    }
-    return true;
-}
-
-
-/**
- * Remember, the 'm_winFlags' are used to determine when the game is "over". Only then the lose flags are evaluated
- * and used to determine who has won. (According to the SCEN specification).
- * @return
- */
-bool cGame::hasWinConditionHumanMustLoseAllBuildings() const
-{
-    return (m_loseFlags & WINLOSEFLAGS_HUMAN_HAS_BUILDINGS) != 0;
-}
-
-bool cGame::hasWinConditionAIShouldLoseEverything() const
-{
-    return (m_loseFlags & WINLOSEFLAGS_AI_NO_BUILDINGS) != 0;
-}
-
-/**
- * Game over condition: player has no buildings (WinFlags)
- * @return
- */
-bool cGame::hasGameOverConditionPlayerHasNoBuildings() const
-{
-    return (m_winFlags & WINLOSEFLAGS_HUMAN_HAS_BUILDINGS) != 0;
-}
-
-/**
- * Game over condition: Spice quota reached by player
- * @return
- */
-bool cGame::hasGameOverConditionHarvestForSpiceQuota() const
-{
-    return (m_winFlags & WINLOSEFLAGS_QUOTA) != 0;
-}
-
-bool cGame::hasGameOverConditionAIHasNoBuildings() const
-{
-    return (m_winFlags & WINLOSEFLAGS_AI_NO_BUILDINGS) != 0;
-}
-
-void cGame::think_mentat()
-{
-    if (m_mentat) {
-        m_mentat->think();
-    }
-}
-
-// think function belongs to combat state (tbd)
-void cGame::think_audio()
-{
-    if (!game.m_playMusic) // no music enabled, so no need to think
-        return;
-
-    // all this does is repeating music in the same theme.
-    if (m_musicType < 0)
-        return;
-
-    if (m_newMusicCountdown > 0) {
-        m_newMusicCountdown--;
-    }
-
-    if (m_newMusicCountdown == 0) {
-        m_soundPlayer->playMusic(m_newMusicSample);
-        m_newMusicCountdown--; // so we don't keep re-starting music
-    }
-
-    if (m_newMusicCountdown < 0) {
-        if (!m_soundPlayer->isMusicPlaying()) {
-            int desiredMusicType = m_musicType;
-            if (m_musicType == MUSIC_ATTACK) {
-                desiredMusicType = MUSIC_PEACE; // set back to peace
-            }
-            playMusicByType(desiredMusicType);
-        }
-    }
-}
-
-void cGame::updateMouseAndKeyboardState()
-{
-    m_mouse->updateState(); // calls observers that are interested in mouse input
-    m_keyboard->updateState(); // calls observers that are interested in keyboard input
-}
-
-void cGame::updateGamePlaying()
-{
-    if (m_state != GAME_PLAYING) {
-        return;
-    }
-    // Mission playing state logic
-    // TODO: Move this to combat state object
-    for (auto &pPlayer : players) {
-        pPlayer.update();
-    }
-}
-
-void cGame::drawStateCombat()
-{
-    drawManager->drawCombatState();
-    if (m_drawFps) {
-        m_textDrawer->drawText(180,8, Color::black(), std::format("FPS/REST: {}/{}", m_timeManager->getFps(), m_timeManager->getWaitingTime()), false);
-    }
-
-    // for now, call this on game class.
-    // TODO: move this "combat" state into own game state class
-    drawCombatMouse();
-
-    if (m_drawTime) {
-        auto time = m_timeManager->getCurrentTime();
-        m_textDrawer->drawText(game.m_screenW- cSideBar::SidebarWidth-75, cSideBar::TopBarHeight + 1, Color::white(), time);
-        time = m_timeManager->getCurrentTimer();
-        m_textDrawer->drawText(game.m_screenW- cSideBar::SidebarWidth-75, cSideBar::TopBarHeight + 1+15, Color::white(), time);
-    }
-    // MOUSE
-    drawManager->drawCombatMouse();
-}
-
-// drawStateMentat logic + drawing mouth/eyes
-void cGame::drawStateMentat(AbstractMentat *mentat)
-{
-    m_mouse->setTile(MOUSE_NORMAL);
-    mentat->draw();
-    m_mouse->draw();
-}
-
-// draw menu
-// void cGame::drawStateMenu()
-// {
-//     m_currentState->draw();
-// }
-
-void cGame::initSkirmish() const
-{
-    game.missionInit();
-}
-
-void cGame::loadSkirmishMaps() const
-{
-    m_PreviewMaps->loadSkirmishMaps();
-}
-
-void cGame::shakeScreenAndBlitBuffer()
-{
-    m_screenShake->update(m_state, GAME_PLAYING, mapCamera);
-    fadeOutOrBlitScreenBuffer();
-}
-
-void cGame::fadeOutOrBlitScreenBuffer() const
-{
-    if (m_fadeAction == FADE_NONE) {
-        return;
-    }
-
-    // Fading
-    assert(m_fadeAlpha >= kMinAlpha);
-    assert(m_fadeAlpha <= kMaxAlpha);
-}
-
-void cGame::drawState()
-{
-    if (m_fadeAction == eFadeAction::FADE_OUT) {
-        if (screenTexture) {
-            renderDrawer->renderSprite(screenTexture,0,0,(Uint8)m_fadeAlpha);
-        }
-        return;
-    }
-
-    // this makes fade-in happen after fade-out automatically
-    if (m_fadeAlpha == kMinAlpha) {
-        m_fadeAction = eFadeAction::FADE_IN;
-    }
-
-    if (m_fadeAction == eFadeAction::FADE_IN && m_fadeAlpha>250) {
-        m_fadeAlpha = kMaxAlpha;
-        m_fadeAction = eFadeAction::FADE_NONE;
-    }
-
-    switch (m_state) {
-        case GAME_BRIEFING:
-        case GAME_LOSEBRIEF:
-        case GAME_TELLHOUSE:
-        case GAME_WINBRIEF:
-            drawStateMentat(m_mentat);
-            break;
-        case GAME_PLAYING:
-            drawStateCombat();
-            break;
-        // case GAME_MENU:
-        //     drawStateMenu();
-        //     break;
-        case GAME_WINNING:
-            drawStateWinning();
-            break;
-        case GAME_LOSING:
-            drawStateLosing();
-            break;
-        default:
-            // std::cout << "m_state registered in drawState() " << m_state << std::endl;
-            m_currentState->draw();
-            // TODO: GAME_STATISTICS, ETC
-    }
-}
-
-/**
-	Main game loop
-*/
-void cGame::run()
-{
-    actualRenderer = renderDrawer->createRenderTargetTexture(m_screenW, m_screenH);
-    screenTexture = renderDrawer->createRenderTargetTexture(m_screenW, m_screenH);
-    SDL_Event event;
-    while (m_playing) {
-        if (m_focusManager->isGameWindowActive()) {
-            m_timeManager->processTime();
-        }
-        while (SDL_PollEvent(&event)) {
-            switch (event.type) {
-                case SDL_QUIT:
-                    m_playing = false;
-                    break;
-                case SDL_WINDOWEVENT:
-                    m_focusManager->onWindowsFocus(event.window);
-                    break;
-                case SDL_KEYDOWN:
-                case SDL_KEYUP:
-                    m_keyboard->handleEvent(event);
-                    break;
-
-                case SDL_MOUSEBUTTONDOWN:
-                case SDL_MOUSEBUTTONUP:
-                case SDL_MOUSEMOTION:
-                case SDL_MOUSEWHEEL:
-                    m_mouse->handleEvent(event);
-                default:
-                    break;
-            }
-        }
-
-        if (!m_focusManager->isGameWindowActive()) {
-            m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
-            continue; // skip the rest of the loop when we don't have focus
-        }
-
-        updateMouseAndKeyboardState();
-        updateGamePlaying();
-
-        renderDrawer->beginDrawingToTexture(actualRenderer);
-        renderDrawer->renderClearToColor();
-        drawState(); // run game state, includes interaction + drawing
-        transitionStateIfRequired();
-        shakeScreenAndBlitBuffer();
-
-        renderDrawer->endDrawingToTexture();
-        renderDrawer->renderSprite(actualRenderer, m_screenShake->getX(), m_screenShake->getY());
-        SDL_RenderPresent(renderer);
-        m_timeManager->waitForCPU(); // wait for CPU to catch up, so we don't run too fast
-    }
-}
-
-void cGame::shakeScreen(int duration)
-{
-    m_screenShake->shake(duration);
-}
-
-/**
-	Shutdown the game
-*/
-void cGame::shutdown()
-{
-    cParticle::reset();
-    cLogger *logger = cLogger::getInstance();
-    logger->logHeader("SHUTDOWN");
-
-    for (int i = 0; i < GAME_MAX_STATES; i++) {
-        cGameState *pState = m_states[i];
-        if (pState) {
-            if (pState->getType() != eGameStateType::GAMESTATE_SELECT_YOUR_NEXT_CONQUEST) {
-                if (m_currentState == pState) {
-                    m_currentState = nullptr; // reset
-                }
-                delete pState;
-                m_states[i] = nullptr;
-            }
-            else {
-                if (m_currentState == pState) {
-                    m_currentState = nullptr; // reset
-                }
-                m_states[i] = nullptr;
-            }
-        }
-    }
-
-    if (m_currentState != nullptr) {
-        assert(false);
-        if (m_currentState->getType() != eGameStateType::GAMESTATE_SELECT_YOUR_NEXT_CONQUEST) {
-            // destroy game state object, unless we talk about the region select
-            delete m_currentState;
-        }
-        else {
-            m_currentState = nullptr;
-        }
-    }
-
-    if (m_PreviewMaps != nullptr) {
-        m_PreviewMaps->destroy();
-    }
-
-    delete m_mentat;
-    delete m_mapViewport;
-
-    delete drawManager;
-
-    delete mapCamera;
-
-    cStructureFactory::destroy();
-    cSideBarFactory::destroy();
-    cBuildingListFactory::destroy();
-
-    for (int i = 0; i < MAX_PLAYERS; i++) {
-        players[i].destroyAllegroBitmaps();
-    }
-
-    delete renderDrawer;
-    delete m_mouse;
-    delete m_keyboard;
-
-    logbook("Allegro FONT library shut down.");
-
-    // Release the game dev framework, so that it can do cleanup
-    //m_PLInit.reset();
-}
-
-
-/**
-	Setup the game
-
-	Should not be called twice.
-*/
-bool cGame::setupGame()
-{
-    cLogger *logger = cLogger::getInstance();
-    logger->setDebugMode(m_debugMode);
-    logger->logHeader("Dune II - The Maker");
-    logger->logCommentLine(""); // whitespace
-
-    logger->logHeader("Version information");
-    logger->log(LOG_INFO, COMP_VERSION, "Initializing",
-                std::format("Version {}, Compiled at {} , {}", D2TM_VERSION, __DATE__, __TIME__));
-
-    // SETTINGS.INI
-    std::shared_ptr<cIniFile> settings = std::make_shared<cIniFile>("settings.ini", m_debugMode);
-
-    // TODO(SETTINGS) -> The game rules file is loaded via here, but *also* via `INSTALL_GAME()`!
-    std::shared_ptr<cIniFile> gamesCfg = std::make_shared<cIniFile>(m_gameFilename, m_debugMode);
-
-    m_reinforcements = std::make_shared<cReinforcements>();
-    global_map.setReinforcements(m_reinforcements);
-
-    game.init(); // Must be first! (loads game.ini file at the end, which is required before going on...)
-
-    const std::string &gameDir = settings->getStringValue(SECTION_SETTINGS, "GameDir");
-    std::unique_ptr<cFileValidator> settingsValidator = std::make_unique<cFileValidator>(gameDir);
-    {
-        std::map<eGameDirFileName, std::string> m_transfertMap;
-        m_transfertMap[eGameDirFileName::ARRAKEEN] = settings->getStringValue("FONT", "ARRAKEEN");
-        m_transfertMap[eGameDirFileName::BENEGESS] = settings->getStringValue("FONT", "BENEGESS");
-        m_transfertMap[eGameDirFileName::SMALL] = settings->getStringValue("FONT", "SMALL");
-
-        m_transfertMap[eGameDirFileName::GFXDATA] = settings->getStringValue("DATAFILE", "GFXDATA");
-        m_transfertMap[eGameDirFileName::GFXINTER] = settings->getStringValue("DATAFILE", "GFXINTER");
-        m_transfertMap[eGameDirFileName::GFXWORLD] = settings->getStringValue("DATAFILE", "GFXWORLD");
-        m_transfertMap[eGameDirFileName::GFXMENTAT] = settings->getStringValue("DATAFILE", "GFXMENTAT");
-        m_transfertMap[eGameDirFileName::GFXAUDIO] = settings->getStringValue("DATAFILE", "GFXAUDIO");
-        settingsValidator->addResources(std::move(m_transfertMap));
-    }
-
-    if (!settingsValidator->fileExists()) {
-        logger->log(LOG_INFO, COMP_INIT, "Loading settings.ini", "Validation of files within settings.ini failed", OUTC_FAILED);
-        std::cerr << "One or more validations failed with resources defined in settings.ini" << std::endl;
-        return false;
-    }
-
-    // GAME.INI
-    const auto title = std::format("Dune II - The Maker [{}] - (by Stefan Hendriks)", D2TM_VERSION);
-
-    // FIXME: eventually, we will want to grab this object in the constructor. But then cGame cannot be a
-    // global anymore, because it needs to be destructed before main exits.
-    m_PLInit = std::make_unique<cPlatformLayerInit>();
-
-    m_keyboard = new cKeyboard();
-    logger->log(LOG_INFO, COMP_INIT, "Initializing Keyboard", "install_keyboard()", OUTC_SUCCESS);
-
-    m_Screen = std::make_unique<cScreenInit>(m_screenW, m_screenH, title);
-    if (!m_windowed) {
-        m_Screen->setFullScreenMode();
-    }
-
-    m_screenW = m_Screen->Width();
-    m_screenH = m_Screen->Height();
-    window = m_Screen->getWindows();
-    renderer = m_Screen->getRenderer();
-
-    // create ressources from scratch
-    context = std::make_unique<ContextCreator>(renderer, settingsValidator.get());
-    // share Graphics to all class what use ctx !
-    ctx->setGraphicsContext(context->createGraphicsContext());
-    // share Text to all class what use ctx !
-    ctx->setTextContext(context->createTextContext());
-    global_map.setGameContext(ctx.get());
-
-    m_textDrawer = ctx->getTextContext()->getGameTextDrawer();
-    //m_textDrawer->setApplyShadow(false);
-
-    std::unique_ptr<cSoundPlayer> soundPlayer = std::make_unique<cSoundPlayer>(settingsValidator->getFullName(eGameDirFileName::GFXAUDIO));
-    m_soundPlayer = soundPlayer.get();
-    ctx->setSoundPlayer(std::move(soundPlayer));
-    if (!m_playSound) {
-        m_soundPlayer->setSoundEnabled(false);
-    }
-    if (!m_playMusic) {
-        m_soundPlayer->setMusicEnabled(false);
-    }
-
-    // do it here, because it depends on fonts to be loaded
-    m_mouse = new cMouse(ctx.get());
-
-    /***
-     * Viewport(s)
-     */
-    m_mapViewport = new cRectangle(0, cSideBar::TopBarHeight, game.m_screenW - cSideBar::SidebarWidth, game.m_screenH - cSideBar::TopBarHeight);
-
-    logbook("Color conversion method set");
-
-    logbook("MOUSE: Mouse speed set");
-
-    logger->logHeader("GAME");
-
-    /*** Data files ***/
-
-    // load datafiles
-    gfxdata = std::make_shared<Graphics>(renderer,settingsValidator->getFullName(eGameDirFileName::GFXDATA));
-    if (gfxdata == nullptr) {
-        logger->log(LOG_ERROR, COMP_INIT, "Load data", "Could not hook/load datafile:" + settingsValidator->getName(eGameDirFileName::GFXDATA), OUTC_FAILED);
-        return false;
-    }
-    else {
-        logger->log(LOG_INFO, COMP_INIT, "Load data", "Hooked datafile: " + settingsValidator->getName(eGameDirFileName::GFXDATA), OUTC_SUCCESS);
-    }
-
-    renderDrawer = new SDLDrawer(renderer);
-
-    // randomize timer
-    auto t = static_cast<unsigned int>(time(nullptr));
-    logbook(std::format("Seed is {}", t));
-    srand(t);
-
-    game.m_playing = true;
-    game.m_screenshot = 0;
-    game.m_state = GAME_INITIALIZE;
-
-    logbook("Setup:  HOUSES");
-    m_Houses = std::make_shared<cHousesInfo>();
-    m_Houses->INSTALL_HOUSES(gamesCfg);
-    // A few messages for the player
-    logbook("Initializing:  PLAYERS");
-    for (int i = 0; i < MAX_PLAYERS; i++) {
-        players[i].init(i, nullptr);
-        players[i].setHousesInfo(m_Houses);
-    }
-    logbook("Setup:  STRUCTURES");
-    IniGameRessources::install_structures();
-    logbook("Setup:  PROJECTILES");
-    IniGameRessources::install_bullets();
-    logbook("Setup:  UNITS");
-    IniGameRessources::install_units();
-    logbook("Setup:  SPECIALS");
-    IniGameRessources::install_specials();
-    logbook("Setup:  PARTICLES");
-    IniGameRessources::install_particles();
-    logbook("Setup:  TERRAINS");
-    IniGameRessources::install_terrain(m_TerrainInfo);
-
-    delete mapCamera;
-    mapCamera = new cMapCamera(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove);
-
-    cIni::installGame(m_gameFilename);
-    // Now we are ready for the menu state
-    game.setState(GAME_MENU);
-
-    m_focusManager->setEnabled(m_pauseWhenLosingFocus);
-
-    // do install_upgrades after game.init, because game.init loads the INI file and then has the very latest
-    // unit/structures catalog loaded - which the install_upgrades depends on.
-    IniGameRessources::install_upgrades();
-    cPlayer *humanPlayer = &players[HUMAN];
-
-    delete drawManager;
-    drawManager = new cDrawManager(ctx.get(), humanPlayer);
-
-    // Must be after drawManager, because the cInteractionManager constructor depends on drawManager
-    m_interactionManager = std::make_unique<cInteractionManager>(humanPlayer);
-
-    game.setupPlayers();
-
-    playMusicByTypeForStateTransition(MUSIC_MENU);
-
-    m_mouse->setMouseObserver(m_interactionManager.get());
-    m_keyboard->setKeyboardObserver(m_interactionManager.get());
-
-    // all has installed well. Let's rock and roll.
-    SDL_ShowCursor(false);
-    return true;
-}
-
-/**
- * Set up players
- * (Elegible for combat state object initialization)
- */
-void cGame::setupPlayers()
-{
-    // make sure each player has an own item builder
-    for (int i = HUMAN; i < MAX_PLAYERS; i++) {
-        cPlayer *thePlayer = &players[i];
-
-        auto *buildingListUpdater = new cBuildingListUpdater(thePlayer);
-        thePlayer->setBuildingListUpdater(buildingListUpdater);
-
-        auto *itemBuilder = new cItemBuilder(thePlayer, buildingListUpdater);
-        thePlayer->setItemBuilder(itemBuilder);
-
-        auto *sidebar = cSideBarFactory::getInstance()->createSideBar(thePlayer);
-        thePlayer->setSideBar(sidebar);
-
-        auto *orderProcesser = new cOrderProcesser(thePlayer);
-        thePlayer->setOrderProcesser(orderProcesser);
-
-        auto *gameControlsContext = new cGameControlsContext(thePlayer, this->m_mouse);
-        thePlayer->setGameControlsContext(gameControlsContext);
-
-        // set tech level
-        thePlayer->setTechLevel(game.m_mission);
-    }
-    setPlayerToInteractFor(&players[0]);
-}
-
-bool cGame::isState(int thisState) const
-{
-    return (m_state == thisState);
-}
-
-void cGame::jumpToSelectYourNextConquestMission(int missionNr)
-{
-    cGameState *existingStatePtr = m_states[GAME_REGION];
-    if (existingStatePtr) {
-        delete existingStatePtr;
-        m_states[GAME_REGION] = nullptr;
-    }
-
-    cSelectYourNextConquestState *pState = new cSelectYourNextConquestState(game, ctx.get());
-    m_states[GAME_REGION] = pState;
-
-    pState->calculateOffset();
-    pState->installWorld();
-
-    cPlayer &humanPlayer = players[HUMAN];
-    int missionZeroBased = missionNr - 1;
-    m_mission = missionZeroBased;
-
-    // a 'missionX.ini' file is from 1 til (including) 8
-    // to play mission 2 (passed as missionNr param), we have to load up mission1.ini
-    // meaning we have to use the 'zero based' value here
-    pState->fastForwardUntilMission(missionZeroBased, humanPlayer.getHouse());
-    pState->regionSetupNextMission(missionZeroBased, humanPlayer.getHouse());
-}
-
-void cGame::setState(int newState)
-{
-    if (newState == m_state) {
-        // ignore
-        return;
-    }
-
-    logbook(std::format("Setting state from {}(={}) to {}(={})", m_state, stateString(m_state), newState, stateString(newState)));
-
-    if (newState > -1) {
-        bool deleteOldState = (newState != GAME_REGION &&
-                               newState != GAME_PLAYING &&
-                               newState != GAME_OPTIONS); // don't delete these m_states, but re-use!
-
-        if (newState == GAME_PLAYING) {
-            // make sure to delete options menu now
-            delete m_states[GAME_OPTIONS];
-            m_states[GAME_OPTIONS] = nullptr;
-        }
-
-        if (newState == GAME_REGION) {
-            // make sure to delete options menu now
-            delete m_states[GAME_OPTIONS];
-            m_states[GAME_OPTIONS] = nullptr;
-        }
-
-        if (newState == GAME_MISSIONSELECT) {
-            deleteOldState = true; // delete old options state everytime
-        }
-
-        if (deleteOldState) {
-            delete m_states[newState];
-            m_states[newState] = nullptr;
-        }
-
-        cPlayer &humanPlayer = players[HUMAN];
-
-        cGameState *existingStatePtr = m_states[newState];
-
-        if (existingStatePtr) {
-            // no need for re-creating state
-            if (newState == GAME_REGION) {
-                playMusicByTypeForStateTransition(MUSIC_CONQUEST);
-
-                // came from a win/lose brief state, so make sure to set up the next state
-                if (m_state == GAME_WINBRIEF || m_state == GAME_LOSEBRIEF) {
-                    // because `GAME_REGION` == if (existingStatePtr->getType() == GAMESTATE_SELECT_YOUR_NEXT_CONQUEST ||
-                    auto *pState = dynamic_cast<cSelectYourNextConquestState *>(existingStatePtr);
-
-                    if (game.m_mission > 1) {
-                        pState->conquerRegions();
-                    }
-
-                    if (m_missionWasWon) {
-                        // we won
-                        pState->regionSetupNextMission(game.m_mission, humanPlayer.getHouse());
-                    }
-                    else {
-                        // OR: did not win
-                        pState->regionSetupLostMission();
-                    }
-                }
-            }
-            else if (newState == GAME_OPTIONS) {
-                // This feels awkward. For now, I'll keep it (if it works), but this will change
-                // once we have a proper game playing state and we need to transition properly between
-                // states
-                takeBackGroundScreen();
-                auto *pState = dynamic_cast<cOptionsState *>(existingStatePtr);
-                // you cannot 'go back' to mission select
-                if (m_state != GAME_MISSIONSELECT) {
-                    pState->setPrevState(m_state);
-                }
-                else {
-                    pState->refresh(); // rebuilds UI windows, but keeps background
-                }
-            }
-
-            m_currentState = existingStatePtr;
-        }
-        else {
-            cGameState *newStatePtr = nullptr;
-
-            if (newState == GAME_REGION) {
-                cSelectYourNextConquestState *pState = new cSelectYourNextConquestState(game, ctx.get());
-
-                pState->calculateOffset();
-                logbook("Setup:  WORLD");
-                pState->installWorld();
-                if (game.m_mission > 1) {
-                    pState->conquerRegions();
-                }
-                // first creation
-                pState->regionSetupNextMission(game.m_mission, humanPlayer.getHouse());
-
-                playMusicByTypeForStateTransition(MUSIC_CONQUEST);
-
-                newStatePtr = pState;
-            }
-            else if (newState == GAME_SETUPSKIRMISH) {
-                initPlayers(false);
-                newStatePtr = new cSetupSkirmishState(*this, ctx.get(), m_PreviewMaps);
-                playMusicByTypeForStateTransition(MUSIC_MENU);
-            }
-            else if (newState == GAME_CREDITS) {
-                newStatePtr = new cCreditsState(*this, ctx.get());
-            }
-            else if (newState == GAME_MENU) {
-                newStatePtr = new cMainMenuState(*this, ctx.get());
-                playMusicByTypeForStateTransition(MUSIC_MENU);
-            }
-            else if (newState == GAME_SELECT_HOUSE) {
-                newStatePtr = new cChooseHouseState(*this, ctx.get());
-            }
-            else if (newState == GAME_MISSIONSELECT) {
-                m_mouse->setTile(MOUSE_NORMAL);
-                newStatePtr = new cSelectMissionState(*this, ctx.get(), m_state);
-            }
-            else if (newState == GAME_OPTIONS) {
-                takeBackGroundScreen();
-                m_mouse->setTile(MOUSE_NORMAL);
-                if (m_state == GAME_PLAYING) {
-                    // so we don't draw mouse cursor
-                    drawManager->drawCombatState();
-                    m_timeManager->pauseTimer();
-                }
-                else {
-                    // we fall back what was on screen, (which includes mouse cursor for now)
-                }
-
-                newStatePtr = new cOptionsState(*this, ctx.get(), m_state);
-            }
-            else if (newState == GAME_PLAYING) {
-                if (m_state == GAME_OPTIONS) {
-                    m_timeManager->restartTimer();
-                    takeBackGroundScreen();
-                    // we came from options menu, notify mouse
-                    humanPlayer.getGameControlsContext()->onFocusMouseStateEvent();
-                }
-                else {
-                    // re-create drawManager
-                    delete drawManager;
-                    drawManager = new cDrawManager(ctx.get(), &humanPlayer);
-
-                    // evaluate all players, so we have initial 'alive' values set properly
-                    for (int i = 1; i < MAX_PLAYERS; i++) {
-                        cPlayer &player = players[i];
-                        player.evaluateStillAlive();
-                    }
-                    cParticle::reset();
-                    // in-between solution until we have a proper combat state object
-                    drawManager->init();
-
-                    // handle update
-                    s_GameEvent event{
-                        .eventType = eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN,
-                    };
-                    // the game is about to begin!
-                    game.onNotifyGameEvent(event);
-                    m_timeManager->startTimer();
-                }
-            }
-
-            m_states[newState] = newStatePtr;
-            m_currentState = newStatePtr;
-        }
-    }
-    m_state = newState;
-}
-
-void cGame::think_fading()
-{
-    // Fading of the entire screen
-    if (m_fadeAction == eFadeAction::FADE_OUT) {
-        m_fadeAlpha -= 2;
-        if (m_fadeAlpha < kMinAlpha) {
-            m_fadeAlpha = kMinAlpha;
-            m_fadeAction = eFadeAction::FADE_NONE;
-        }
-    }
-    else if (m_fadeAction == eFadeAction::FADE_IN) {
-        m_fadeAlpha += 2;
-        if (m_fadeAlpha > kMaxAlpha) {
-            m_fadeAlpha = kMaxAlpha;
-            m_fadeAction = eFadeAction::FADE_NONE;
-        }
-    }
-
-    // Fading / pulsating of selected stuff
-    static constexpr float fadeSelectIncrement = 1 / 256.0f;
-    if (m_fadeSelectDir) {
-        m_fadeSelect += fadeSelectIncrement;
-        // when 255, then fade back
-        if (m_fadeSelect > 0.99) {
-            m_fadeSelect = 1.0f;
-            m_fadeSelectDir = false;
-        }
-
-        return;
-    }
-
-    m_fadeSelect -= fadeSelectIncrement;
-    // not too dark, 0.03125
-    if (m_fadeSelect < 0.3125f) {
-        m_fadeSelectDir = true;
-    }
-}
-
-cGame::~cGame()
-{
-}
-
-void cGame::prepareMentatForPlayer()
-{
-    int house = players[HUMAN].getHouse();
-    if (m_state == GAME_BRIEFING) {
-        game.missionInit();
-        game.setupPlayers();
-        cIni::loadScenario(house, m_region, m_mentat, m_reinforcements.get());
-        cIni::loadBriefing(house, m_region, INI_BRIEFING, m_mentat);
-    }
-    else if (m_state == GAME_WINBRIEF) {
-        if (RNG::rnd(100) < 50) {
-            m_mentat->loadScene("win01");
-        }
-        else {
-            m_mentat->loadScene("win02");
-        }
-        cIni::loadBriefing(house, m_region, INI_WIN, m_mentat);
-    }
-    else if (m_state == GAME_LOSEBRIEF) {
-        if (RNG::rnd(100) < 50) {
-            m_mentat->loadScene("lose01");
-        }
-        else {
-            m_mentat->loadScene("lose02");
-        }
-        cIni::loadBriefing(house, m_region, INI_LOSE, m_mentat);
-    }
-}
-
-void cGame::createAndPrepareMentatForHumanPlayer(bool allowMissionSelect)
-{
-    delete m_mentat;
-    int houseIndex = players[HUMAN].getHouse();
-    if (houseIndex == ATREIDES) {
-        m_mentat = new AtreidesMentat(ctx.get(), allowMissionSelect);
-    }
-    else if (houseIndex == HARKONNEN) {
-        m_mentat = new HarkonnenMentat(ctx.get(), allowMissionSelect);
-    }
-    else if (houseIndex == ORDOS) {
-        m_mentat = new OrdosMentat(ctx.get(), allowMissionSelect);
-    }
-    else {
-        // fallback
-        m_mentat = new BeneMentat(ctx.get());
-    }
-    prepareMentatForPlayer();
-    m_mentat->speak();
-}
-
-void cGame::prepareMentatToTellAboutHouse(int house)
-{
-    delete m_mentat;
-    m_mentat = new BeneMentat(ctx.get());
-    m_mentat->setHouse(house);
-    // create new drawStateMentat
-    if (house == ATREIDES) {
-        cIni::loadBriefing(ATREIDES, 0, INI_DESCRIPTION, m_mentat);
-        m_mentat->loadScene("platr"); // load planet of atreides
-    }
-    else if (house == HARKONNEN) {
-        cIni::loadBriefing(HARKONNEN, 0, INI_DESCRIPTION, m_mentat);
-        m_mentat->loadScene("plhar"); // load planet of harkonnen
-    }
-    else if (house == ORDOS) {
-        cIni::loadBriefing(ORDOS, 0, INI_DESCRIPTION, m_mentat);
-        m_mentat->loadScene("plord"); // load planet of ordos
-    }
-    else {
-        m_mentat->setSentence(0, "Looks like you choose an unknown house");
-    }
-    // todo: Sardaukar, etc? (Super Dune 2 features)
-    m_mentat->speak();
-}
-
-void cGame::loadScenario()
-{
-    int iHouse = players[HUMAN].getHouse();
-    cIni::loadScenario(iHouse, game.m_region, m_mentat, m_reinforcements.get());
-}
-
-void cGame::thinkFast_state()
-{
-    think_audio();
-    think_mentat();
-
-    if (m_currentState) {
-        m_currentState->thinkFast();
-    }
-
-    // THINKING ONLY WHEN PLAYING / COMBAT (no state object yet)
-    if (isState(GAME_PLAYING)) {
-        drawManager->thinkFast_statePlaying();
-        thinkFast_combat();
-    }
-
-    if (drawManager) {
-        drawManager->thinkFast();
-    }
-}
-
-void cGame::thinkFast_combat()
-{
-    mapCamera->thinkFast();
-
-    for (cPlayer &pPlayer : players) {
-        pPlayer.thinkFast();
-    }
-
-    // structures think
-    for (cAbstractStructure *pStructure : structure) {
-        if (pStructure == nullptr) continue;
-        if (pStructure->isValid()) {
-            pStructure->thinkFast();       // think about actions going on
-            pStructure->think_animation(); // think about animating
-            pStructure->think_guard();     // think about 'guarding' the area (turrets only)
-        }
-
-        if (pStructure->isDead()) {
-            cStructureFactory::getInstance()->deleteStructureInstance(pStructure);
-        }
-    }
-
-    for (cPlayer &pPlayer : players) {
-        cItemBuilder *itemBuilder = pPlayer.getItemBuilder();
-        if (itemBuilder) {
-            itemBuilder->thinkFast();
-        }
-    }
-
-    global_map.thinkFast();
-
-    game.reduceShaking();
-
-    // units think (move only)
-    for (cUnit &cUnit : unit) {
-        if (!cUnit.isValid()) continue;
-        cUnit.thinkFast();
-    }
-
-    for (cParticle &pParticle : particle) {
-        if (!pParticle.isValid()) continue;
-        pParticle.thinkFast();
-    }
-
-    // when not drawing the options, the game does all it needs to do
-    // bullets think
-    for (cBullet &cBullet : bullet) {
-        if (!cBullet.bAlive) continue;
-        cBullet.thinkFast();
-    }
-}
-
-void cGame::setPlayerToInteractFor(cPlayer *pPlayer)
-{
-    m_interactionManager->setPlayerToInteractFor(pPlayer);
-}
-
-void cGame::onNotifyGameEvent(const s_GameEvent &event)
-{
-    logbook(s_GameEvent::toString(event));
-
-    global_map.onNotifyGameEvent(event);
-
-    // game itself handles events
-    switch (event.eventType) {
-        case eGameEventType::GAME_EVENT_SPECIAL_LAUNCH:
-            onEventSpecialLaunch(event);
-            break;
-        case eGameEventType::GAME_EVENT_DESTROYED:
-            onEventEntityDestroyed(event);
-            break;
-        default:
-            break;
-    }
-
-    // players handle events
-    for (int i = 0; i < MAX_PLAYERS; i++) {
-        players[i].onNotifyGameEvent(event);
-    }
-}
-
-void cGame::onEventEntityDestroyed(const s_GameEvent &event) {
-    if (event.entityType != eBuildType::STRUCTURE) {
-        return;
-    }
-    // TODO(https://github.com/stefanhendriks/Dune-II---The-Maker/issues/755) - Make this configurable via game.ini
-
-    int minAmountOfSoldiersToSpawnPotentially = 1;
-    int maxAmountOfSoldiersToSpawnPotentially = 3;
-
-    // bigger structures, can spawn a bigger range of
-    if (event.entitySpecificType == PALACE || event.entitySpecificType == STARPORT) {
-        maxAmountOfSoldiersToSpawnPotentially = 5;
-    }
-
-    if (event.entitySpecificType == TURRET || event.entitySpecificType == RTURRET || event.entitySpecificType == WALL) {
-        minAmountOfSoldiersToSpawnPotentially = 0;
-        maxAmountOfSoldiersToSpawnPotentially = 0;
-    }
-
-    int amountOfSoldiersToSpawn = RNG::genInt(minAmountOfSoldiersToSpawnPotentially, maxAmountOfSoldiersToSpawnPotentially);
-
-
-    int widthInCells = sStructureInfo[event.entitySpecificType].bmp_width / 32;
-    int heightInCells = sStructureInfo[event.entitySpecificType].bmp_height / 32;
-
-    int cellX = global_map.getGeometry().getCellX(event.atCell);
-    int cellY = global_map.getGeometry().getCellY(event.atCell);
-
-    for (int i = 0; i < amountOfSoldiersToSpawn; i++) {
-        int randomX = cellX + RNG::genIntMaxExcl(0, widthInCells);
-        int randomY = cellY + RNG::genIntMaxExcl(0, heightInCells);
-        UNIT_CREATE(
-            global_map.getGeometry().makeCell(randomX, randomY),
-            SOLDIER,
-            event.player->getId(),
-            false,
-            false,
-            RNG::genDouble(0.3, 0.8)
-        );
-    }
-}
-
-void cGame::onEventSpecialLaunch(const s_GameEvent &event) const {
-    cBuildingListItem *itemToDeploy = event.buildingListItem;
-    int iMouseCell = event.atCell;
-    cPlayer *player = event.player;
-    if (itemToDeploy->isTypeSpecial()) {
-        const s_SpecialInfo &special = itemToDeploy->getSpecialInfo();
-
-        int deployCell = -1;
-        if (special.deployTargetType == eDeployTargetType::TARGET_SPECIFIC_CELL) {
-            deployCell = iMouseCell;
-        }
-        else if (special.deployTargetType == eDeployTargetType::TARGET_INACCURATE_CELL) {
-            int precision = special.deployTargetPrecision;
-            int mouseCellX = global_map.getCellX(iMouseCell) - precision;
-            int mouseCellY = global_map.getCellY(iMouseCell) - precision;
-
-            int posX = mouseCellX + RNG::rnd((precision * 2) + 1);
-            int posY = mouseCellY + RNG::rnd((precision * 2) + 1);
-            cPoint::split(posX, posY) = global_map.fixCoordinatesToBeWithinPlayableMap(posX, posY);
-
-            logbook(std::format(
-                        "eDeployTargetType::TARGET_INACCURATE_CELL, mouse cell X,Y = {},{} - target pos ={},{} - precision {}",
-                        mouseCellY, mouseCellY, posX, posY,precision)
-                   );
-
-            deployCell = global_map.getGeometry().makeCell(posX, posY);
-        }
-
-
-        if (special.providesType == eBuildType::BULLET) {
-            // from where
-            int structureId = structureUtils.findStructureBy(player->getId(), special.deployAtStructure, false);
-            if (structureId > -1) {
-                cAbstractStructure *pStructure = structure[structureId];
-                if (pStructure && pStructure->isValid()) {
-                    m_soundPlayer->playSound(SOUND_PLACE);
-                    createBullet(special.providesTypeId, pStructure->getCell(), deployCell, -1, structureId);
-
-                    // notify game that the item just has been finished!
-                    s_GameEvent newEvent{
-                        .eventType = eGameEventType::GAME_EVENT_SPECIAL_LAUNCHED,
-                        .entityType = itemToDeploy->getBuildType(),
-                        .entityID = -1,
-                        .player = pStructure->getPlayer(),
-                        .entitySpecificType = itemToDeploy->getBuildId(),
-                        .atCell = -1,
-                        .isReinforce = false,
-                        .buildingListItem = itemToDeploy
-                    };
-
-                    game.onNotifyGameEvent(newEvent);
-                }
-            }
-        }
-    }
-
-    itemToDeploy->decreaseTimesToBuild();
-    itemToDeploy->setDeployIt(false);
-    itemToDeploy->setIsBuilding(false);
-    itemToDeploy->resetProgress();
-    if (itemToDeploy->getTimesToBuild() < 1) {
-        player->getItemBuilder()->removeItemFromList(itemToDeploy);
-    }
-
-    if (player) {
-        player->getGameControlsContext()->toPreviousState();
-    }
-
-    // notify game that the item just has been finished!
-    s_GameEvent newEvent{
-        .eventType = eGameEventType::GAME_EVENT_LIST_ITEM_FINISHED,
-        .entityType = itemToDeploy->getBuildType(),
-        .entityID = -1,
-        .player = player,
-        .entitySpecificType = itemToDeploy->getBuildId(),
-        .atCell = -1,
-        .isReinforce = false,
-        .buildingListItem = nullptr
-    };
-
-    game.onNotifyGameEvent(newEvent);
-}
-
-void cGame::reduceShaking() const {
-    m_screenShake->reduce();
-}
-
-// void cGame::install_bitmaps()
-// {
-//     //Mira rip this function
-// }
-
-Color cGame::getColorFadeSelected(int r, int g, int b, bool rFlag, bool gFlag, bool bFlag)
-{
-    unsigned char desiredRed = rFlag ? r * m_fadeSelect : r;
-    unsigned char desiredGreen = gFlag ? g * m_fadeSelect : g;
-    unsigned char desiredBlue = bFlag ? b * m_fadeSelect : b;
-    return Color{desiredRed, desiredGreen, desiredBlue,255};
-}
-
-Color cGame::getColorPlaceNeutral()
-{
-    return Color{242, 174, 36,64};
-}
-
-Color cGame::getColorPlaceBad()
-{
-    return Color{160, 0, 0,64};
-}
-
-Color cGame::getColorPlaceGood()
-{
-    return Color{64, 255, 64,64};
-}
-
-void cGame::setWinFlags(int value)
-{
-    if (game.isDebugMode()) {
-        logbook(std::format("Changing m_winFlags from {} to {}", m_winFlags, value));
-    }
-    m_winFlags = value;
-}
-
-void cGame::setLoseFlags(int value)
-{
-    if (game.isDebugMode()) {
-        logbook(std::format("Changing m_loseFlags from {} to {}", m_loseFlags, value));
-    }
-    m_loseFlags = value;
-}
-
-void cGame::onNotifyMouseEvent(const s_MouseEvent &event)
-{
-    // pass through any classes that are interested
-    if (m_currentState) {
-        m_currentState->onNotifyMouseEvent(event);
-    }
-    if (m_mentat) {
-        m_mentat->onNotifyMouseEvent(event);
-    }
-}
-
-void cGame::onNotifyKeyboardEvent(const cKeyboardEvent &event)
-{
-    // pass through any classes that are interested
-    if (m_currentState) {
-        m_currentState->onNotifyKeyboardEvent(event);
-    }
-
-    // take screenshot
-    if (event.isType(eKeyEventType::PRESSED) && event.hasKey(SDL_SCANCODE_F11)) {
-        saveBmpScreenToDisk();
-    }
-
-    // TODO: this has to be its own state class. Then this if is no longer needed.
-    if (m_state == GAME_PLAYING) {
-        onNotifyKeyboardEventGamePlaying(event);
-    }
-}
-
-void cGame::transitionStateIfRequired()
-{
-    if (m_nextState > -1) {
-        setState(m_nextState);
-
-        if (m_nextState == GAME_BRIEFING) {
-            playMusicByType(MUSIC_BRIEFING);
-            game.createAndPrepareMentatForHumanPlayer();
-        }
-
-        m_nextState = -1;
-    }
-}
-
-void cGame::setNextStateToTransitionTo(int newState)
-{
-    m_nextState = newState;
-}
-
-void cGame::drawCombatMouse()
-{
-    if (m_mouse->isBoxSelecting()) {
-        renderDrawer->renderRectColor(m_mouse->getBoxSelectRectangle(),255,255,255,255);
-    }
-
-    if (m_mouse->isMapScrolling()) {
-        cPoint startPoint = m_mouse->getDragLineStartPoint();
-        cPoint endPoint = m_mouse->getDragLineEndPoint();
-        renderDrawer->renderLine( startPoint.x, startPoint.y, endPoint.x, endPoint.y, Color{255,255,255,255});
-    }
-
-    m_mouse->draw();
-}
-
-void cGame::saveBmpScreenToDisk()
-{
-    std::string filename = std::format("{}x{}_{:0>4}.bmp", m_screenW, m_screenH, m_screenshot);
-    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, m_screenW, m_screenH, 32, SDL_PIXELFORMAT_RGBA32);
-    if (!surface) {
-        std::cerr << "Erreur lors de la création de la surface: " << SDL_GetError() << std::endl;
-        return;
-    }
-    // Lire les pixels depuis le framebuffer
-    if (SDL_RenderReadPixels(renderer, NULL, SDL_PIXELFORMAT_RGBA32, surface->pixels, surface->pitch) != 0) {
-        std::cerr << "Erreur lors de la lecture des pixels: " << SDL_GetError() << std::endl;
-        SDL_FreeSurface(surface);
-        return;
-    }
-    std::string name = std::format("screenshot{}.bmp",m_screenshot);
-    SDL_SaveBMP(surface, filename.c_str());
-    SDL_FreeSurface(surface);
-
-    // shows a message in-game, would be even better to have this 'globally' (not depending on state), kind of like
-    // a Quake console perhaps?
-    cPlayer &humanPlayer = players[HUMAN];
-    humanPlayer.addNotification(std::format("Screenshot saved {}.", filename), eNotificationType::NEUTRAL);
-
-    m_screenshot++;
-}
-
-void cGame::onNotifyKeyboardEventGamePlaying(const cKeyboardEvent &event)
-{
-    logbook(event.toString());
-
-    drawManager->onNotifyKeyboardEvent(event);
-
-    switch (event.eventType) {
-        case eKeyEventType::HOLD:
-            onKeyDownGamePlaying(event);
-            break;
-        case eKeyEventType::PRESSED:
-            onKeyPressedGamePlaying(event);
-            break;
-        default:
-            break;
-    }
-}
-
-void cGame::onKeyDownGamePlaying(const cKeyboardEvent &event)
-{
-    const cPlayer &humanPlayer = players[HUMAN];
-
-    bool createGroup = event.hasKey(SDL_SCANCODE_LCTRL) || event.hasKey(SDL_SCANCODE_RCTRL);
-    if (createGroup) {
-        int iGroup = event.getGroupNumber();
-
-        if (iGroup > 0) {
-            humanPlayer.markUnitsForGroup(iGroup);
-        }
-    }
-
-    if (isDebugMode()) { // debug mode has additional keys
-        if (event.hasKey(SDL_SCANCODE_TAB)) {
-            onKeyDownDebugMode(event);
-        }
-
-        if (event.hasKey(SDL_SCANCODE_F4)) {
-            int mouseCell = humanPlayer.getGameControlsContext()->getMouseCell();
-            if (mouseCell > -1) {
-                global_map.clearShroud(mouseCell, 6, HUMAN);
-            }
-        }
-
-    }
-
-    if (event.hasKey(SDL_SCANCODE_Z)) {
-        mapCamera->resetZoom();
-    }
-
-    if (event.hasKey(SDL_SCANCODE_H)) {
-        mapCamera->centerAndJumpViewPortToCell(humanPlayer.getFocusCell());
-    }
-
-    // Center on the selected structure
-    if (event.hasKey(SDL_SCANCODE_C)) {
-        cAbstractStructure *selectedStructure = humanPlayer.getSelectedStructure();
-        if (selectedStructure) {
-            mapCamera->centerAndJumpViewPortToCell(selectedStructure->getCell());
-        }
-    }
-
-    if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
-        game.setNextStateToTransitionTo(GAME_OPTIONS);
-    }
-
-    if (event.hasKey(SDL_SCANCODE_F)) {
-        m_drawFps = true;
-    }
-}
-
-void cGame::onKeyPressedGamePlaying(const cKeyboardEvent &event)
-{
-    cPlayer &humanPlayer = players[HUMAN];
-
-    if (event.hasKey(SDL_SCANCODE_F)) {
-        m_drawFps = false;
-    }
-
-    if (event.hasKey(SDL_SCANCODE_BACKSLASH)) {
-        m_drawTime = ! m_drawTime;
-    }
-
-    if (event.hasKey(SDL_SCANCODE_D)) {
-        for (int i = 0; i < MAX_UNITS; i++) {
-            cUnit &u = unit[i];
-            if (u.bSelected && u.iType == MCV && u.getPlayer()->isHuman()) {
-                bool canPlace = u.getPlayer()->canPlaceStructureAt(u.getCell(), CONSTYARD, u.iID).success;
-                if (canPlace) {
-                    int iLocation = u.getCell();
-                    u.die(false, false);
-                    humanPlayer.placeStructure(iLocation, CONSTYARD, 100);
-                }
-            }
-        }
-    }
-
-    if (event.hasKey(SDL_SCANCODE_M) || event.hasKey(SDL_SCANCODE_MUTE)) {
-        game.m_playMusic = !game.m_playMusic;
-        if (!game.m_playMusic) {
-            m_soundPlayer->stopMusic();
-            humanPlayer.addNotification("Music muted", eNotificationType::NEUTRAL);
-        }
-        else {
-            m_soundPlayer->playMusic(m_newMusicSample);
-            humanPlayer.addNotification("Music enabled", eNotificationType::NEUTRAL);
-        }
-    }
-
-    if (event.hasKey(SDL_SCANCODE_O) || event.hasKey(SDL_SCANCODE_VOLUMEDOWN)) {
-        m_soundPlayer->changeMusicVolume(-10);
-    }
-
-    if (event.hasKey(SDL_SCANCODE_P) || event.hasKey(SDL_SCANCODE_VOLUMEUP) ) {
-        m_soundPlayer->changeMusicVolume(10);
-    }
-
-    if (event.hasKey(SDL_SCANCODE_H)) {
-        mapCamera->centerAndJumpViewPortToCell(humanPlayer.getFocusCell());
-    }
-
-    if (event.hasKey(SDL_SCANCODE_KP_PLUS)) {
-        auto timerManager = ctx->getTimeManager();
-        timerManager->setGlobalSpeedVariation(-1);
-    }
-    if (event.hasKey(SDL_SCANCODE_KP_MINUS)) {
-        auto timerManager = ctx->getTimeManager();
-        timerManager->setGlobalSpeedVariation(1);
-    }
-
-    // Center on the selected structure
-    if (event.hasKey(SDL_SCANCODE_C)) {
-        cAbstractStructure *selectedStructure = humanPlayer.getSelectedStructure();
-        if (selectedStructure) {
-            mapCamera->centerAndJumpViewPortToCell(selectedStructure->getCell());
-        }
-    }
-
-    if (event.hasKeys(SDL_SCANCODE_LALT,SDL_SCANCODE_RETURN)) {
-        if (m_windowed) {
-            m_Screen->setFullScreenMode();
-            m_windowed = false;
-        } else {
-            m_Screen->setWindowMode();
-            m_windowed = true;
-        }
-    }
-
-    cAbstractStructure *selectedStructure = humanPlayer.getSelectedStructure();
-    if (selectedStructure) {
-        // depending on type of structure, a key could mean a different thing?
-        // so, kind of like event.hasKey(selectedStructure->KeyForDeploying()) ?
-        // and then perform?
-        if (event.hasKey(SDL_SCANCODE_D)) {
-            if (selectedStructure->getType() == REPAIR) { // this should be done differently?
-                s_GameEvent e{
-                    .eventType = eGameEventType::GAME_EVENT_DEPLOY_UNIT,
-                    .entityType = eBuildType::UNKNOWN,
-                    .entityID = -1,
-                    .player = &humanPlayer
-                };
-                selectedStructure->onNotifyGameEvent(e);
-            }
-        }
-        // other keys for other structures?
-        // like: repair/stop repairing?
-    }
-}
-
-void cGame::playSound(int sampleId)
-{
-    m_soundPlayer->playSound(sampleId);
-}
-
-void cGame::playSound(int sampleId, int vol)
-{
-    m_soundPlayer->playSound(sampleId, vol);
-}
-
-void cGame::playSoundWithDistance(int sampleId, int iDistance)
-{
-    if (iDistance <= 1) { // means "on screen" (meaning fixed volume, and no need for panning)
-        playSound(sampleId);
-        return;
-    }
-
-    // zoom factor influences distance we can 'hear'. The closer up, the less max distance. Unzoomed, this is half the map.
-    // where when unit is at half map, we can hear it only a bit.
-    float maxDistance = mapCamera->divideByZoomLevel(global_map.getMaxDistanceInPixels() / 2);
-    float distanceNormalized = 1.0 - (iDistance / maxDistance);
-
-    float volume = m_soundPlayer->getMaxVolume() * distanceNormalized;
-
-    // zoom factor influences volume (more zoomed in means louder)
-    float volumeFactor = mapCamera->factorZoomLevel(0.7f);
-    int iVolFactored = volumeFactor * volume;
-
-    if (game.isDebugMode()) {
-        logbook(std::format("iDistance [{}], distanceNormalized [{}] maxDistance [{}], m_zoomLevel [{}], volumeFactor [{}], volume [{}], iVolFactored [{}]",
-                            iDistance, distanceNormalized, maxDistance, mapCamera->getZoomLevel(), volumeFactor, volume, iVolFactored));
-    }
-
-    playSound(sampleId, iVolFactored);
-}
-
-
-void cGame::playVoice(int sampleId, int playerId)
-{
-    m_soundPlayer->playVoice(sampleId, players[playerId].getHouse());
-}
-
-void cGame::playMusicByTypeForStateTransition(int iType)
-{
-    if (m_musicType != iType) {
-        m_newMusicCountdown = 0;
-        playMusicByType(iType, HUMAN, false);
-    }
-}
-
-bool cGame::playMusicByType(int iType, int playerId, bool triggerWithVoice)
-{
-    if (playerId != HUMAN) {
-        // skip music we want to play for non human player
-        return false;
-    }
-
-    logbook(std::format("cGame::playMusicByType - iType = {}. playerId = {}, triggerWithVoice = {}", iType, playerId, triggerWithVoice));
-
-    if (triggerWithVoice) {
-        if (iType == m_musicType) {
-            logbook(std::format("m_musicType = {}, iType is {}, so bailing", m_musicType, iType));
-            return false;
-        }
-    }
-
-    m_musicType = iType;
-    logbook(std::format("m_musicType = {}", m_musicType));
-
-    if (!m_playMusic) {
-        return false; // todo: have a 'no-sound soundplayer' instead of doing this :/
-    }
-
-    if (m_newMusicCountdown > 0) {
-        // do not interfere with previous 'change to music' thing?
-        return false;
-    }
-
-
-    int sampleId = MIDI_MENU;
-    if (iType == MUSIC_WIN) {
-        sampleId = MIDI_WIN01 + RNG::rnd(3);
-    }
-    else if (iType == MUSIC_LOSE) {
-        sampleId = MIDI_LOSE01 + RNG::rnd(6);
-    }
-    else if (iType == MUSIC_ATTACK) {
-        sampleId = MIDI_ATTACK01 + RNG::rnd(6);
-    }
-    else if (iType == MUSIC_PEACE) {
-        sampleId = MIDI_BUILDING01 + RNG::rnd(9);
-    }
-    else if (iType == MUSIC_MENU) {
-        sampleId = MIDI_MENU;
-    }
-    else if (iType == MUSIC_CONQUEST) {
-        sampleId = MIDI_SCENARIO;
-    }
-    else if (iType == MUSIC_BRIEFING) {
-        int houseIndex = players[HUMAN].getHouse();
-        if (houseIndex == ATREIDES) {
-            sampleId = MIDI_MENTAT_ATR;
-        }
-        else if (houseIndex == HARKONNEN) {
-            sampleId = MIDI_MENTAT_HAR;
-        }
-        else if (houseIndex == ORDOS) {
-            sampleId = MIDI_MENTAT_ORD;
-        }
-        else {
-            assert(false && "Undefined house.");
-        }
-    }
-    else {
-        assert(false && "Undefined music type.");
-    }
-
-    if (triggerWithVoice) {
-        // voice triggered music (ie "Enemy unit approaching"), so have music stop a bit
-        if (isState(GAME_PLAYING)) {
-            m_newMusicCountdown = 400; // wait a bit longer
-        }
-        else {
-            m_newMusicCountdown = 0;
-        }
-        m_soundPlayer->stopMusic();
-    }
-    else {
-        // instant switch
-        m_newMusicCountdown = 0;
-    }
-
-    m_newMusicSample = sampleId;
-    return true;
-}
-
-int cGame::getMaxVolume()
-{
-    return m_soundPlayer->getMaxVolume();
-}
-
-/**
- * Called every 100ms
- */
-void cGame::think_state()
-{
-    if (game.isState(GAME_PLAYING)) {
-        // units think
-        for (int i = 0; i < MAX_UNITS; i++) {
-            cUnit &cUnit = unit[i];
-            if (cUnit.isValid()) {
-                cUnit.think();
-            }
-        }
-
-        drawManager->think();
-
-        for (int i = 0; i < MAX_PLAYERS; i++) {
-            players[i].think();
-        }
-
-    }
-}
-
-/**
- * Called every second
- */
-void cGame::thinkSlow()
-{
-    thinkSlow_state();
-
-    m_timeManager->capFps();
-    m_timeManager->adaptWaitingTime();
-}
-
-void cGame::think_minute()
-{
-    ctx->resetCache();
-}
-
-void cGame::thinkSlow_state()
-{
-    if (isState(GAME_PLAYING)) {
-        thinkSlow_stateCombat_evaluatePlayerStatus(); // so we can call non-const from a const :S
-
-        m_pathsCreated = 0;
-
-        if (!m_disableReinforcements) {
-            m_reinforcements->thinkSlow();
-        }
-
-        // starports think per second for deployment (if any)
-        for (int i = 0; i < MAX_STRUCTURES; i++) {
-            cAbstractStructure *pStructure = structure[i];
-            if (pStructure && pStructure->isValid()) {
-                pStructure->thinkSlow();
-            }
-        }
-
-        for (int i = 0; i < MAX_PLAYERS; i++) {
-            cPlayer &player = players[i];
-            player.thinkSlow();
-        }
-
-    } // game specific stuff
-
-}
-
-void cGame::onKeyDownDebugMode(const cKeyboardEvent &event)
-{
-    const cPlayer &humanPlayer = players[HUMAN];
-
-    if (event.hasKey(SDL_SCANCODE_0)) {
-        drawManager->setPlayerToDraw(&players[0]);
-        game.setPlayerToInteractFor(&players[0]);
-    }
-    else if (event.hasKey(SDL_SCANCODE_1)) {
-        drawManager->setPlayerToDraw(&players[1]);
-        game.setPlayerToInteractFor(&players[1]);
-    }
-    else if (event.hasKey(SDL_SCANCODE_2)) {
-        drawManager->setPlayerToDraw(&players[2]);
-        game.setPlayerToInteractFor(&players[2]);
-    }
-    else if (event.hasKey(SDL_SCANCODE_3)) {
-        drawManager->setPlayerToDraw(&players[3]);
-        game.setPlayerToInteractFor(&players[3]);
-    }
-
-    // WIN MISSION
-    if (event.hasKey(SDL_SCANCODE_F2)) {
-        game.setMissionWon();
-    }
-
-    // LOSE MISSION
-    if (event.hasKey(SDL_SCANCODE_F3)) {
-        game.setMissionLost();
-    }
-
-    // GIVE CREDITS TO ALL PLAYERS
-    if (event.hasKey(SDL_SCANCODE_F4)) {
-        for (int i = 0; i < AI_WORM; i++) {
-            players[i].setCredits(5000);
-        }
-    }
-
-    // SPAWN ENEMY AIR UNIT
-    if (event.hasKey(SDL_SCANCODE_F8)) {
-        int mc = humanPlayer.getGameControlsContext()->getMouseCell();
-        UNIT_CREATE(
-            mc,
-            ORNITHOPTER,
-            1,
-            false,
-            false
-        );
-    }
-
-    //DESTROY UNIT OR BUILDING
-    if (event.hasKeys(SDL_SCANCODE_F4, SDL_SCANCODE_LSHIFT)) {
-        int mc = humanPlayer.getGameControlsContext()->getMouseCell();
-        if (mc > -1) {
-            int idOfUnitAtCell = global_map.getCellIdUnitLayer(mc);
-            if (idOfUnitAtCell > -1) {
-                unit[idOfUnitAtCell].die(true, false);
-            }
-
-            int idOfStructureAtCell = global_map.getCellIdStructuresLayer(mc);
-            if (idOfStructureAtCell > -1) {
-                structure[idOfStructureAtCell]->die();
-            }
-
-            idOfUnitAtCell = global_map.getCellIdWormsLayer(mc);
-            if (idOfUnitAtCell > -1) {
-                unit[idOfUnitAtCell].die(false, false);
-            }
-
-            idOfUnitAtCell = global_map.getCellIdAirUnitLayer(mc);
-            if (idOfUnitAtCell > -1) {
-                unit[idOfUnitAtCell].die(false, false);
-            }
-        }
-    }
-
-    //DESTROY UNIT OR BUILDING
-    if (event.hasKeys(SDL_SCANCODE_F5, SDL_SCANCODE_LSHIFT)) {
-        int mc = humanPlayer.getGameControlsContext()->getMouseCell();
-        if (mc > -1) {
-            int idOfUnitAtCell = global_map.getCellIdUnitLayer(mc);
-            if (idOfUnitAtCell > -1) {
-                cUnit &pUnit = unit[idOfUnitAtCell];
-                int damageToTake = pUnit.getHitPoints() - 25;
-                if (damageToTake > 0) {
-                    pUnit.takeDamage(damageToTake, -1, -1);
-                }
-            }
-        }
-    }
-    else {
-        // REVEAL MAP
-        if (event.hasKey(SDL_SCANCODE_F5)) {
-            for (int i = 0; i < AI_WORM; i++) {
-                global_map.clear_all(i);
-            }
-        }
-    }
-
-    if (event.hasKey(SDL_SCANCODE_F6)) {
-        // kill all carry-all's
-        const std::vector<int> &myUnitsForType = humanPlayer.getAllMyUnitsForType(CARRYALL);
-        for (auto &unitId : myUnitsForType) {
-            cUnit &pUnit = unit[unitId];
-            pUnit.die(true, false);
-        }
-    }
-}
-
-void cGame::setMousePosition(int w, int h)
-{
-    m_mouse->setCursorPosition(window, w,h);
-}
-
-void cGame::execute(AbstractMentat &mentat)
-{
-    if (game.isState(GAME_BRIEFING)) {
-        // proceed, play mission (it is already loaded before we got here)
-        game.setNextStateToTransitionTo(GAME_PLAYING);
-        drawManager->missionInit();
-
-        // CENTER MOUSE
-        game.setMousePosition(game.m_screenW / 2, game.m_screenH / 2);
-
-        game.initiateFadingOut();
-
-        game.playMusicByType(MUSIC_PEACE);
-        return;
-    }
-
-    if (game.m_skirmish) {
-        if (game.isState(GAME_WINBRIEF) || game.isState(GAME_LOSEBRIEF)) {
-            // regardless of drawStateWinning or drawStateLosing, always go back to main menu
-            game.setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
-            game.initSkirmish();
-            game.initiateFadingOut();
-        }
-        else {
-            logbook("cProceedButtonCommand pressed, in skirmish mode and state is not WINBRIEF nor LOSEBRIEF!?");
-        }
-        return;
-    }
-
-    // NOT a skirmish game
-
-    // won mission, transition to region selection (Select your next Conquest)
-    if (game.isState(GAME_WINBRIEF)) {
-        game.setNextStateToTransitionTo(GAME_REGION);
-
-        game.initiateFadingOut();
-        return;
-    }
-
-    // lost mission
-    if (game.isState(GAME_LOSEBRIEF)) {
-        game.missionInit();
-        // lost mission > 1, so we go back to region select
-        if (game.m_mission > 1)   {
-            game.setNextStateToTransitionTo(GAME_REGION);
-
-            game.m_mission--; // we did not win
-        }
-        else {
-            // mission 1 failed, really?..., back to mentat with briefing
-            game.setNextStateToTransitionTo(GAME_BRIEFING);
-            game.prepareMentatForPlayer();
-            game.playMusicByType(MUSIC_BRIEFING);
-            mentat.resetSpeak();
-        }
-
-        game.initiateFadingOut();
-        return;
-    }
-}
-
-
-// Fading between menu items
-void cGame::initiateFadingOut()
-{
-    // set state to fade out
-    m_fadeAction = eFadeAction::FADE_OUT; // fade out
-    m_fadeAlpha = 250;
-
-    renderDrawer->beginDrawingToTexture(screenTexture);
-    SDL_RenderCopy(renderer, actualRenderer->tex,nullptr, nullptr);
-    renderDrawer->endDrawingToTexture();
-}
-
-// this shows the you have lost bmp at screen, after mouse press the mentat debriefing state will begin
-void cGame::drawStateLosing()
-{
-    if (screenTexture)
-        renderDrawer->renderSprite(screenTexture,0,0);
-
-    auto tex = ctx->getGraphicsContext()->gfxinter->getTexture(BMP_LOSING);
-    int posW = (m_screenW-tex->w)/2;
-    int posH = (m_screenH-tex->h)/2;
-    renderDrawer->renderSprite(tex,posW, posH);
-    renderDrawer->renderSprite(gfxdata->getTexture(MOUSE_NORMAL), m_mouse->getX(), m_mouse->getY());
-
-    if (m_mouse->isLeftButtonClicked()) {
-        m_state = GAME_LOSEBRIEF;
-
-        createAndPrepareMentatForHumanPlayer(!m_skirmish);
-
-        // FADE OUT
-        initiateFadingOut();
-    }
-}
-
-// this shows the you have won bmp at screen, after mouse press the mentat debriefing state will begin
-void cGame::drawStateWinning()
-{
-    if (screenTexture)
-        renderDrawer->renderSprite(screenTexture,0,0);
-        
-    auto tex = ctx->getGraphicsContext()->gfxinter->getTexture(BMP_WINNING);
-    int posW = (m_screenW-tex->w)/2;
-    int posH = (m_screenH-tex->h)/2;
-    renderDrawer->renderSprite(tex,posW, posH);
-    renderDrawer->renderSprite(gfxdata->getTexture(MOUSE_NORMAL), m_mouse->getX(), m_mouse->getY());
-
-    if (m_mouse->isLeftButtonClicked()) {
-        // Mentat will be happy, after that enter "Select your next Conquest"
-        m_state = GAME_WINBRIEF;
-
-        createAndPrepareMentatForHumanPlayer(!m_skirmish);
-
-        // FADE OUT
-        initiateFadingOut();
-    }
-}
-
-void cGame::takeBackGroundScreen()
-{
-    renderDrawer->beginDrawingToTexture(screenTexture);
-    SDL_RenderCopy(renderer, actualRenderer->tex,nullptr, nullptr);
-    renderDrawer->endDrawingToTexture();
-}
-
-std::shared_ptr<s_TerrainInfo> cGame::getTerrainInfo() const
-{
-    return m_TerrainInfo;
-}
\ No newline at end of file


=== PORT: src/controls/cGameControlsContext.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/controls/cGameControlsContext.cpp
stdout:
diff --git a/src/controls/cGameControlsContext.cpp b/src/controls/cGameControlsContext.cpp
index b7479ffd..4bcc8700 100644
--- a/src/controls/cGameControlsContext.cpp
+++ b/src/controls/cGameControlsContext.cpp
@@ -1,29 +1,64 @@
-#include "cGameControlsContext.h"
+/**
+ * @file cGameControlsContext.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cGameControlsContext.h"
+#include "game/cGameSettings.h"
+#include "gameobjects/structures/cAbstractStructure.h"
+#include "gameobjects/structures/cStructures.h"
+#include "gameobjects/units/cUnits.h"
+#include "gameobjects/map/cMap.h"
 #include "data/gfxdata.h"
-#include "d2tmc.h"
 #include "managers/cDrawManager.h"
+#include "gameobjects/map/cMapCamera.h"
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "include/sGameServices.h"
+#include "utils/cStructureUtils.h"
+#include "utils/Log.h"
+#include "context/GameContext.hpp"
+
+#include "controls/mousestates/cMouseNormalState.h"
+#include "controls/mousestates/cMouseUnitsSelectedState.h"
+#include "controls/mousestates/cMouseRepairState.h"
+#include "controls/mousestates/cMousePlaceState.h"
+#include "controls/mousestates/cMouseDeployState.h"
+
+#include "include/cAssert.h"
+#include "drawers/cMiniMapDrawer.h"
+#include "sidebar/cSideBar.h"
 
 cGameControlsContext::cGameControlsContext(cPlayer *player, cMouse *mouse) :
     m_mouseHoveringOverStructureId(-1),
     m_mouseHoveringOverUnitId(-1),
     m_mouseOnBattleField(false),
-    m_drawToolTip(false),
     m_mouseCell(-99),
+    m_mouseCellClamped(0),
     m_player(player),
     m_state(MOUSESTATE_SELECT),
     m_prevState(MOUSESTATE_SELECT),
     m_prevStateBeforeRepair(MOUSESTATE_SELECT),
     m_mouse(mouse),
-    m_mouseNormalState(new cMouseNormalState(player, this, m_mouse)),
-    m_mouseUnitsSelectedState(new cMouseUnitsSelectedState(player, this, m_mouse)),
-    m_mouseRepairState(new cMouseRepairState(player, this, m_mouse)),
-    m_mousePlaceState(new cMousePlaceState(player, this, m_mouse)),
-    m_mouseDeployState(new cMouseDeployState(player, this, m_mouse)),
+    m_mouseNormalState(std::make_unique<cMouseNormalState>(player, this, m_mouse)),
+    m_mouseUnitsSelectedState(std::make_unique<cMouseUnitsSelectedState>(player, this, m_mouse)),
+    m_mouseRepairState(std::make_unique<cMouseRepairState>(player, this, m_mouse)),
+    m_mousePlaceState(std::make_unique<cMousePlaceState>(player, this, m_mouse)),
+    m_mouseDeployState(std::make_unique<cMouseDeployState>(player, this, m_mouse)),
     m_prevTickMouseAtBattleField(false)
 {
-    assert(player && "Expected player in cGameControlsContext constructor");
-    assert(mouse && "Expected mouse in cGameControlsContext constructor");
+    d2tm_assert(player!=nullptr && "Expected player in cGameControlsContext constructor");
+    d2tm_assert(mouse!=nullptr && "Expected mouse in cGameControlsContext constructor");
 }
 
 cGameControlsContext::~cGameControlsContext()
@@ -32,87 +67,101 @@ cGameControlsContext::~cGameControlsContext()
     m_player = nullptr;
     m_mouse = nullptr;
 
-    // created these, so delete
-    delete m_mouseNormalState;
-    delete m_mouseUnitsSelectedState;
-    delete m_mouseRepairState;
-    delete m_mousePlaceState;
-    delete m_mouseDeployState;
+    // smart pointers handle cleanup
 }
 
+void cGameControlsContext::serviceInit(sGameServices *services)
+{
+    m_objects = services->objects;
+    m_mapCamera = services->mapCamera;
+    m_settings = services->settings;
+    m_drawManager = services->drawManager;
+    m_eventEmitter = services->eventEmitter;
+    m_structureUtils = services->structureUtils;
+    m_infos = services->info;
+    m_audioContext = services->ctx->getAudioContext();
+    m_mapViewport = services->mapViewport;
+}
 
 void cGameControlsContext::updateMouseCell(const cPoint &coords)
 {
     if (coords.y < cSideBar::TopBarHeight) {
-        m_mouseCell = MOUSECELL_TOPBAR; // at the top bar or higher, so no mouse cell id.
+        m_mouseCell = MOUSE_CELL_HOVER_TOPBAR; // at the top bar or higher, so no mouse cell id.
         m_mouseOnBattleField = false;
         return;
     }
 
-    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
-        m_mouseCell = MOUSECELL_MINIMAP; // on minimap
+    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
+        m_mouseCell = MOUSE_CELL_HOVER_MINIMAP; // on minimap
         m_mouseOnBattleField = false;
         return;
     }
 
-    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
-        m_mouseCell = MOUSECELL_SIDEBAR; // on sidebar
+    if (coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth)) {
+        m_mouseCell = MOUSE_CELL_HOVER_SIDEBAR; // on sidebar
         m_mouseOnBattleField = false;
         return;
     }
     m_mouseOnBattleField = true;
     m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
+    if (m_mouseCell < 0) { // clamp mouse cell to map
+        m_mouseCellClamped = getMouseCellFromScreenClamped(coords.x, coords.y);
+    }
 }
 
 int cGameControlsContext::getMouseCellFromScreen(int mouseX, int mouseY) const
 {
-    int absMapX = mapCamera->getAbsMapMouseX(mouseX);
-    int absMapY = mapCamera->getAbsMapMouseY(mouseY);
-    return mapCamera->getCellFromAbsolutePosition(absMapX, absMapY);
+    int absMapX = m_mapCamera->getAbsMapMouseX(mouseX);
+    int absMapY = m_mapCamera->getAbsMapMouseY(mouseY);
+    return m_mapCamera->getCellFromAbsolutePosition(absMapX, absMapY);
 }
 
-void cGameControlsContext::determineToolTip()
+int cGameControlsContext::getMouseCellFromScreenClamped(int mouseX, int mouseY) const
 {
-    // @Mira : magical call to key ...
-    // @mira: this function activate drawToolTip with GUI branch
-    // m_drawToolTip = false;
-    // if (key[SDL_SCANCODE_T] && isMouseOnBattleField()) { // TODO: this gets removed later, when we redo tooltips anyway
-    // m_drawToolTip = true;
-    // }
+    int absMapX = m_mapCamera->getAbsMapMouseX(mouseX);
+    int absMapY = m_mapCamera->getAbsMapMouseY(mouseY);
+    return m_mapCamera->getCellFromAbsolutePositionClamped(absMapX, absMapY);
 }
 
 void cGameControlsContext::determineHoveringOverStructureId()
 {
     m_mouseHoveringOverStructureId = -1;
 
-    if (!global_map.isVisible(m_mouseCell, this->m_player)) {
+    if (!m_objects->getMap()->isVisible(m_mouseCell, this->m_player)) {
         return; // cell not visible
     }
 
-    m_mouseHoveringOverStructureId = global_map.getCellIdStructuresLayer(m_mouseCell);
+    int structureId = m_objects->getMap()->getCellIdStructuresLayer(m_mouseCell);
+    if (structureId > -1) {
+        cAbstractStructure *pStructure = m_objects->getStructures()[structureId];
+        if (pStructure && m_objects->getMap()->isHiddenByFogOfWar(pStructure)) {
+            return; // hidden in the fog of war, only a remembered (visual) structure is shown there
+        }
+    }
+    m_mouseHoveringOverStructureId = structureId;
 }
 
 void cGameControlsContext::determineHoveringOverUnitId()
 {
     if (m_mouseHoveringOverUnitId > -1) {
-        cUnit &aUnit = unit[m_mouseHoveringOverUnitId];
-        if (aUnit.isValid()) {
-            aUnit.bHovered = false;
+        cUnit *aUnit = m_objects->getUnit(m_mouseHoveringOverUnitId);
+        if (aUnit->isValid()) {
+            aUnit->rendering.bHovered = false;
         }
     }
     m_mouseHoveringOverUnitId = -1;
     int mc = getMouseCell();
-    tCell *cellOfMouse = global_map.getCell(mc);
+    tCell *cellOfMouse = m_objects->getMap()->getCell(mc);
     if (cellOfMouse == nullptr) return; // mouse is not on battlefield
 
-    if (!global_map.isVisible(mc, this->m_player)) {
+    if (!m_objects->getMap()->isVisible(mc, this->m_player)) {
         return; // cell not visible
     }
 
     if (cellOfMouse->id[MAPID_UNITS] > -1) {
         int iUnitId = cellOfMouse->id[MAPID_UNITS];
 
-        if (!unit[iUnitId].isHidden()) {
+        if (!m_objects->getUnit(iUnitId)->isHidden()) {
             m_mouseHoveringOverUnitId = iUnitId;
         }
 
@@ -123,9 +172,13 @@ void cGameControlsContext::determineHoveringOverUnitId()
     }
 
     if (m_mouseHoveringOverUnitId > -1) {
-        cUnit &aUnit = unit[m_mouseHoveringOverUnitId];
-        if (aUnit.isValid()) {
-            aUnit.bHovered = true;
+        cUnit *aUnit = m_objects->getUnit(m_mouseHoveringOverUnitId);
+        if (m_objects->getMap()->isHiddenByFogOfWar(aUnit)) {
+            m_mouseHoveringOverUnitId = -1; // hidden in the fog of war
+            return;
+        }
+        if (aUnit->isValid()) {
+            aUnit->rendering.bHovered = true;
         }
     }
 }
@@ -135,7 +188,7 @@ cAbstractStructure *cGameControlsContext::getStructurePointerWhereMouseHovers()
     if (m_mouseHoveringOverStructureId < 0) {
         return nullptr;
     }
-    return structure[m_mouseHoveringOverStructureId];
+    return m_objects->getStructures()[m_mouseHoveringOverStructureId];
 }
 
 void cGameControlsContext::onMouseMovedTo(const s_MouseEvent &event)
@@ -143,7 +196,6 @@ void cGameControlsContext::onMouseMovedTo(const s_MouseEvent &event)
     updateMouseCell(event.coords);
     bool mouseOnBattleField = isMouseOnBattleField();
     if (mouseOnBattleField) {
-        determineToolTip();
         determineHoveringOverStructureId();
         determineHoveringOverUnitId();
 
@@ -250,7 +302,8 @@ void cGameControlsContext::setMouseState(eMouseState newState)
             m_prevState = m_prevStateBeforeRepair;
         }
 
-        logbook(std::format("setMouseState() : changing state from [{}] to [{}] (prevState=[{}], prevStateBeforeRepair=[{}])", mouseStateString(m_state), mouseStateString(newState), mouseStateString(m_prevState), mouseStateString(m_prevStateBeforeRepair)));
+        Logger::info(COMP_NONE, "cGameControlsContext::setMouseState", "changing state from [{}] to [{}] (prevState=[{}], prevStateBeforeRepair=[{}])", mouseStateString(m_state), mouseStateString(newState), mouseStateString(m_prevState), mouseStateString(m_prevStateBeforeRepair));
+        onBlurMouseStateEvent();
         m_state = newState;
         switch (m_state) {
             case MOUSESTATE_SELECT:


=== PORT: src/controls/cMouse.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/controls/cMouse.cpp
stdout:
diff --git a/src/controls/cMouse.cpp b/src/controls/cMouse.cpp
index 7e69e469..a0151c59 100644
--- a/src/controls/cMouse.cpp
+++ b/src/controls/cMouse.cpp
@@ -1,184 +1,222 @@
-#include "cMouse.h"
+/**
+ * @file cMouse.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cMouse.h"
+#include "game/cGameSettings.h"
 #include "controls/cGameControlsContext.h"
-#include "d2tmc.h"
+#include "observers/cInputObserver.h"
 #include "data/gfxdata.h"
 #include "drawers/SDLDrawer.hpp"
-#include "drawers/cTextDrawer.h"
-#include "player/cPlayer.h"
 #include "sidebar/cSideBar.h"
 #include "utils/d2tm_math.h"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
-#include <SDL2/SDL.h>
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "utils/common.h"
+#include "utils/Log.h"
+#include <SDL3/SDL.h>
 #include <iostream>
+#include "include/cAssert.h"
+#include "context/GraphicsContext.hpp"
+#include "utils/cRectangle.h"
 
 cMouse::cMouse(GameContext *ctx) :
     m_ctx(ctx),
-    m_textDrawer(ctx->getTextContext()->getBeneTextDrawer()),
-    coords(cPoint(0,0))
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_coords(cPoint(0,0))
 {
-    leftButtonPressed=false;
-    rightButtonPressed=false;
-    leftButtonReleased=false;
-    rightButtonReleased=false;
-    mouseScrolledUp=false;
-    mouseScrolledDown=false;
-    leftButtonClickedInPreviousFrame = false;
-    rightButtonClickedInPreviousFrame = false;
-    _mouseObserver = nullptr; // set later
-    debugLines = std::vector<std::string>();
-    didMouseMove = false;
+    d2tm_assert(m_ctx!=nullptr);
+    d2tm_assert(m_sdlDrawer!=nullptr);
+    m_leftButtonPressed=false;
+    m_rightButtonPressed=false;
+    m_leftButtonReleased=false;
+    m_rightButtonReleased=false;
+    m_mouseScrolledUp=false;
+    m_mouseScrolledDown=false;
+    m_leftButtonDoubleClicked = false;
+    m_leftButtonClickedInPreviousFrame = false;
+    m_rightButtonClickedInPreviousFrame = false;
+    m_mouseObserver = nullptr; // set later
+    m_didMouseMove = false;
     init();
 }
 
 cMouse::~cMouse()
 {
-    _mouseObserver = nullptr; // we do not own this, so don't delete
+    m_mouseObserver = nullptr; // we do not own this, so don't delete
 }
 
 void cMouse::init()
 {
-    mouse_tile = MOUSE_NORMAL;
-
-    mouse_co_x1 = -1;
-    mouse_co_y1 = -1;
-    mouse_co_x2 = -1;
-    mouse_co_y2 = -1;
+    m_mouseTile = MOUSE_NORMAL;
 
-    mouse_mv_x1 = -1;
-    mouse_mv_y1 = -1;
-    mouse_mv_x2 = -1;
-    mouse_mv_y2 = -1;
+    m_mouseCoX1 = -1;
+    m_mouseCoY1 = -1;
+    m_mouseCoX2 = -1;
+    m_mouseCoY2 = -1;
 
-    debugLines.clear();
+    m_mouseMvX1 = -1;
+    m_mouseMvY1 = -1;
+    m_mouseMvX2 = -1;
+    m_mouseMvY2 = -1;
 }
 
 void cMouse::handleEvent(const SDL_Event &event)
 {
+    SDL_Renderer *renderer = m_sdlDrawer->getRenderer();
     switch (event.type) {
-        case SDL_MOUSEBUTTONDOWN:
+        case SDL_EVENT_MOUSE_BUTTON_DOWN: {
+            float px, py;
+            SDL_RenderCoordinatesFromWindow(renderer, event.button.x, event.button.y, &px, &py);
             if (event.button.button == SDL_BUTTON_LEFT) {
-                leftButtonPressed = true;
-                coordsOnClick.x = event.motion.x;
-                coordsOnClick.y = event.motion.y;
+                m_leftButtonPressed = (event.button.clicks == 1);
+                m_coordsOnClick.x = static_cast<int>(px);
+                m_coordsOnClick.y = static_cast<int>(py);
             }
             if (event.button.button == SDL_BUTTON_RIGHT) {
-                rightButtonPressed = true;
-                coordsOnClick.x = event.motion.x;
-                coordsOnClick.y = event.motion.y;
+                m_rightButtonPressed = true;
+                m_coordsOnClick.x = static_cast<int>(px);
+                m_coordsOnClick.y = static_cast<int>(py);
             }
             break;
-        case SDL_MOUSEBUTTONUP:
+        }
+        case SDL_EVENT_MOUSE_BUTTON_UP: {
+            float px, py;
+            SDL_RenderCoordinatesFromWindow(renderer, event.button.x, event.button.y, &px, &py);
             if (event.button.button == SDL_BUTTON_LEFT) {
-                leftButtonPressed = false;
-                leftButtonReleased = true;
-                int dist = (coordsOnClick.x - event.motion.x)*(coordsOnClick.x - event.motion.x) + (coordsOnClick.y - event.motion.y)*(coordsOnClick.y - event.motion.y);
-                if (dist < 16) {
-                    // std::cout << "left click" << std::endl;
-                    leftButtonClicked = true;
+                m_leftButtonPressed = false;
+                m_leftButtonReleased = true;
+                int dx = m_coordsOnClick.x - static_cast<int>(px);
+                int dy = m_coordsOnClick.y - static_cast<int>(py);
+                if (dx*dx + dy*dy < 16) {
+                    if (event.button.clicks == 2) {
+                        m_leftButtonDoubleClicked = true;
+                    } else {
+                        m_leftButtonClicked = true;
+                    }
                 }
             }
             if (event.button.button == SDL_BUTTON_RIGHT) {
-                rightButtonPressed = false;
-                rightButtonReleased = true;
-                int dist = (coordsOnClick.x - event.motion.x)*(coordsOnClick.x - event.motion.x) + (coordsOnClick.y - event.motion.y)*(coordsOnClick.y - event.motion.y);
-                if (dist < 16) {
-                    // std::cout << "right click" << std::endl;
-                    rightButtonClicked = true;
+                m_rightButtonPressed = false;
+                m_rightButtonReleased = true;
+                int dx = m_coordsOnClick.x - static_cast<int>(px);
+                int dy = m_coordsOnClick.y - static_cast<int>(py);
+                if (dx*dx + dy*dy < 16) {
+                    m_rightButtonClicked = true;
                 }
             }
             break;
-        case SDL_MOUSEMOTION:
-            coords.x = event.motion.x;
-            coords.y = event.motion.y;
-            didMouseMove = true;
+        }
+        case SDL_EVENT_MOUSE_MOTION: {
+            float px, py;
+            SDL_RenderCoordinatesFromWindow(renderer, event.motion.x, event.motion.y, &px, &py);
+            m_coords.x = static_cast<int>(px);
+            m_coords.y = static_cast<int>(py);
+            m_didMouseMove = true;
             break;
-        case SDL_MOUSEWHEEL:
-            if (event.wheel.y > 0) mouseScrolledUp = true;
-            if (event.wheel.y < 0) mouseScrolledDown = true;
+        }
+        case SDL_EVENT_MOUSE_WHEEL:
+            if (event.wheel.y > 0) m_mouseScrolledUp = true;
+            if (event.wheel.y < 0) m_mouseScrolledDown = true;
             break;
     }
 }
 
 void cMouse::updateState()
 {
-    debugLines.clear();
-
-    if (leftButtonClickedInPreviousFrame == true)
-        leftButtonClicked = false;
-    if (rightButtonClickedInPreviousFrame == true)
-        rightButtonClicked = false;
+    if (m_leftButtonClickedInPreviousFrame == true)
+        m_leftButtonClicked = false;
+    if (m_rightButtonClickedInPreviousFrame == true)
+        m_rightButtonClicked = false;
 
     // mouse moved
-    if (_mouseObserver) {
-        s_MouseEvent event {eMouseEventType::MOUSE_MOVED_TO, coords};
+    if (m_mouseObserver) {
+        s_MouseEvent event {eMouseEventType::MOUSE_MOVED_TO, m_coords};
 
-        if (didMouseMove) {
-            s_MouseEvent event {eMouseEventType::MOUSE_MOVED_TO, coords};
-            _mouseObserver->onNotifyMouseEvent(event);
+        if (m_didMouseMove) {
+            s_MouseEvent event {eMouseEventType::MOUSE_MOVED_TO, m_coords};
+            m_mouseObserver->onNotifyMouseEvent(event);
         }
 
-        if (mouseScrolledUp) {
+        if (m_mouseScrolledUp) {
             event.eventType = eMouseEventType::MOUSE_SCROLLED_UP;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
         }
 
-        if (mouseScrolledDown) {
+        if (m_mouseScrolledDown) {
             event.eventType = eMouseEventType::MOUSE_SCROLLED_DOWN;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
         }
 
-        if (leftButtonPressed) {
+        if (m_leftButtonPressed) {
             event.eventType = eMouseEventType::MOUSE_LEFT_BUTTON_PRESSED;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
             // std::cout << "emit left pressed" << std::endl;
         }
 
-        if (leftButtonReleased) {
+        if (m_leftButtonDoubleClicked) {
+            event.eventType = eMouseEventType::MOUSE_LEFT_BUTTON_DOUBLE_CLICKED;
+            m_mouseObserver->onNotifyMouseEvent(event);
+        } else if (m_leftButtonReleased) {
             event.eventType = eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
             // std::cout << "emit left released" << std::endl;
         }
 
-        if (rightButtonPressed) {
+        if (m_rightButtonPressed) {
             event.eventType = eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
             // std::cout << "emit right pressed" << std::endl;
         }
 
-        if (rightButtonReleased) {
+        if (m_rightButtonReleased) {
             event.eventType = eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED;
-            _mouseObserver->onNotifyMouseEvent(event);
+            m_mouseObserver->onNotifyMouseEvent(event);
             // std::cout << "emit right click" << std::endl;
         }
     }
 
     // HACK HACK:
     // make -1 to -2, so that we can prevent placeIt/deployIt=false when just stopped viewport dragging
-    if (mouse_mv_x2 == -1) {
-        mouse_mv_x2 = -2;
+    if (m_mouseMvX2 == -1) {
+        m_mouseMvX2 = -2;
     }
-    if (mouse_mv_y2 == -1) {
-        mouse_mv_y2 = -2;
+    if (m_mouseMvY2 == -1) {
+        m_mouseMvY2 = -2;
     }
-    didMouseMove = false;
-    leftButtonReleased = false;
-    rightButtonReleased = false;
-    mouseScrolledDown = false;
-    mouseScrolledUp = false;
-    leftButtonClickedInPreviousFrame = leftButtonClicked;
-    rightButtonClickedInPreviousFrame = rightButtonClicked;
+    m_didMouseMove = false;
+    m_leftButtonReleased = false;
+    m_leftButtonDoubleClicked = false;
+    m_rightButtonReleased = false;
+    m_mouseScrolledDown = false;
+    m_mouseScrolledUp = false;
+    m_leftButtonClickedInPreviousFrame = m_leftButtonClicked;
+    m_rightButtonClickedInPreviousFrame = m_rightButtonClicked;
 }
 
 void cMouse::setCursorPosition(SDL_Window *_windows, int x, int y)
 {
-    SDL_WarpMouseInWindow(_windows, x, y); // allegro function
-    if (_mouseObserver) {
+    float wx, wy;
+    SDL_RenderCoordinatesToWindow(m_sdlDrawer->getRenderer(), static_cast<float>(x), static_cast<float>(y), &wx, &wy);
+    SDL_WarpMouseInWindow(_windows, wx, wy);
+    if (m_mouseObserver) {
         s_MouseEvent event {
             eMouseEventType::MOUSE_MOVED_TO,
             cPoint(x,y)};
-        _mouseObserver->onNotifyMouseEvent(event);
+        m_mouseObserver->onNotifyMouseEvent(event);
     }
 }
 
@@ -199,41 +237,41 @@ bool cMouse::isOverRectangle(cRectangle *rectangle)
  */
 bool cMouse::isMapScrolling()
 {
-    return mouse_mv_x1 > -1 && mouse_mv_y1 > -1 && mouse_mv_x2 > -1 && mouse_mv_y2 > -1;
+    return m_mouseMvX1 > -1 && m_mouseMvY1 > -1 && m_mouseMvX2 > -1 && m_mouseMvY2 > -1;
 }
 
 bool cMouse::isBoxSelecting()
 {
-    return mouse_co_x1 > -1 && mouse_co_y1 > -1 &&
-           mouse_co_x2 != mouse_co_x1 && mouse_co_y2 != mouse_co_y1 &&
-           mouse_co_x2 > -1 && mouse_co_y2 > -1;
+    return m_mouseCoX1 > -1 && m_mouseCoY1 > -1 &&
+           m_mouseCoX2 != m_mouseCoX1 && m_mouseCoY2 != m_mouseCoY1 &&
+           m_mouseCoX2 > -1 && m_mouseCoY2 > -1;
 }
 
 void cMouse::resetDragViewportInteraction()
 {
-    if (mouse_mv_x1 > -1 || mouse_mv_y1 > -1 || mouse_mv_x2 > -1 || mouse_mv_y2 > -1) {
-        mouse_mv_x1 = -1;
-        if (mouse_mv_x2 > -1) mouse_mv_x2 = -1;
+    if (m_mouseMvX1 > -1 || m_mouseMvY1 > -1 || m_mouseMvX2 > -1 || m_mouseMvY2 > -1) {
+        m_mouseMvX1 = -1;
+        if (m_mouseMvX2 > -1) m_mouseMvX2 = -1;
 
-        mouse_mv_y1 = -1;
-        if (mouse_mv_y2 > -1) mouse_mv_y2 = -1;
+        m_mouseMvY1 = -1;
+        if (m_mouseMvY2 > -1) m_mouseMvY2 = -1;
     }
 }
 
 void cMouse::dragViewportInteraction()
 {
-    if (mouse_mv_x1 < 0 || mouse_mv_y1 < 0) {
-        mouse_mv_x1 = coords.x;
-        mouse_mv_y1 = coords.y;
+    if (m_mouseMvX1 < 0 || m_mouseMvY1 < 0) {
+        m_mouseMvX1 = m_coords.x;
+        m_mouseMvY1 = m_coords.y;
     }
     else {
         // mouse mv 1st coordinates filled
         // when mouse is deviating from this coordinate, draw a line
 
-        if (ABS_length(coords.x, coords.y, mouse_mv_x1, mouse_mv_y1) > 4) {
+        if (ABS_length(m_coords.x, m_coords.y, m_mouseMvX1, m_mouseMvY1) > 4) {
             // assign 2nd coordinates
-            mouse_mv_x2 = coords.x;
-            mouse_mv_y2 = coords.y;
+            m_mouseMvX2 = m_coords.x;
+            m_mouseMvY2 = m_coords.y;
         }
     }
 }
@@ -243,22 +281,18 @@ void cMouse::boxSelectLogic(int mouseCell)
 // When the mouse is pressed, we will check if the first coordinates are filled in
     // if so, we will update the second coordinates. If the player holds his mouse we
     // keep updating the second coordinates and create a rectangle to select units with.
-    if (mouse_co_x1 > -1 && mouse_co_y1 > -1) {
-        if (abs(coords.x - mouse_co_x1) > 4 && abs(coords.y - mouse_co_y1) > 4) {
+    if (m_mouseCoX1 > -1 && m_mouseCoY1 > -1) {
+        if (abs(m_coords.x - m_mouseCoX1) > 4 && abs(m_coords.y - m_mouseCoY1) > 4) {
             // assign 2nd coordinates
-            mouse_co_x2 = coords.x;
-            if (coords.x > game.m_screenW - cSideBar::SidebarWidth) {
-                mouse_co_x2 = game.m_screenW - cSideBar::SidebarWidth - 1;
+            m_mouseCoX2 = m_coords.x;
+            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
+                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
             }
 
-            mouse_co_y2 = coords.y;
-            if (mouse_co_y2 < cSideBar::TopBarHeight) {
-                mouse_co_y2 = cSideBar::TopBarHeight;
+            m_mouseCoY2 = m_coords.y;
+            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
+                m_mouseCoY2 = cSideBar::TopBarHeight;
             }
-
-            // and draw the selection box
-            //_rect(bmp_screen, mouse_co_x1, mouse_co_y1, mouse_co_x2, mouse_co_y2, game.getColorFadeSelected(255, 255, 255));
-            renderDrawer->renderRectColor(mouse_co_x1, mouse_co_y1, mouse_co_x2-mouse_co_x1, mouse_co_y2-mouse_co_y1, game.getColorFadeSelected(255, 255, 255));
         }
 
         // Note that we have to fix up the coordinates when checking 'within border'
@@ -266,8 +300,8 @@ void cMouse::boxSelectLogic(int mouseCell)
     }
     else if (mouseCell > -1) {
         // no first coordinates set, so do that here.
-        mouse_co_x1 = coords.x;
-        mouse_co_y1 = coords.y;
+        m_mouseCoX1 = m_coords.x;
+        m_mouseCoY1 = m_coords.y;
     }
 }
 
@@ -277,110 +311,103 @@ cRectangle cMouse::getBoxSelectRectangle()
     int max_x, max_y;
 
     // sort out borders:
-    if (mouse_co_x1 < mouse_co_x2) {
-        min_x = mouse_co_x1;
-        max_x = mouse_co_x2;
+    if (m_mouseCoX1 < m_mouseCoX2) {
+        min_x = m_mouseCoX1;
+        max_x = m_mouseCoX2;
     }
     else {
-        max_x = mouse_co_x1;
-        min_x = mouse_co_x2;
+        max_x = m_mouseCoX1;
+        min_x = m_mouseCoX2;
     }
 
     // Y coordinates
-    if (mouse_co_y1 < mouse_co_y2) {
-        min_y = mouse_co_y1;
-        max_y = mouse_co_y2;
+    if (m_mouseCoY1 < m_mouseCoY2) {
+        min_y = m_mouseCoY1;
+        max_y = m_mouseCoY2;
     }
     else {
-        max_y = mouse_co_y1;
-        min_y = mouse_co_y2;
+        max_y = m_mouseCoY1;
+        min_y = m_mouseCoY2;
     }
     return cRectangle(min_x, min_y, (max_x-min_x), (max_y-min_y));
 }
 
 void cMouse::resetBoxSelect()
 {
-    mouse_co_x1 = -1;
-    mouse_co_y1 = -1;
-    mouse_co_x2 = -1;
-    mouse_co_y2 = -1;
+    m_mouseCoX1 = -1;
+    m_mouseCoY1 = -1;
+    m_mouseCoX2 = -1;
+    m_mouseCoY2 = -1;
 }
 
 bool cMouse::isTile(int value)
 {
-    return mouse_tile == value;
+    return m_mouseTile == value;
+}
+
+void cMouse::setMouseObserver(cInputObserver *mouseObserver)
+{
+    m_mouseObserver = mouseObserver;
+    d2tm_assert(m_mouseObserver != nullptr);
 }
 
+
 void cMouse::draw()
 {
-    int mouseDrawX = coords.x;
-    int mouseDrawY = coords.y;
+    int mouseDrawX = m_coords.x;
+    int mouseDrawY = m_coords.y;
 
-    if (mouse_tile > -1) {
+    if (m_mouseTile > -1) {
         // adjust coordinates of drawing according to the specific mouse sprite/tile
-        if (mouse_tile == MOUSE_DOWN) {
+        if (m_mouseTile == MOUSE_DOWN) {
             mouseDrawY -= 16;
         }
-        else if (mouse_tile == MOUSE_RIGHT) {
+        else if (m_mouseTile == MOUSE_RIGHT) {
             mouseDrawX -= 16;
         }
-        else if (mouse_tile == MOUSE_MOVE || mouse_tile == MOUSE_RALLY) {
+        else if (m_mouseTile == MOUSE_MOVE || m_mouseTile == MOUSE_RALLY) {
             mouseDrawX -= 16;
             mouseDrawY -= 16;
         }
-        else if (mouse_tile == MOUSE_ATTACK) {
+        else if (m_mouseTile == MOUSE_ATTACK) {
             mouseDrawX -= 16;
             mouseDrawY -= 16;
         }
-        else if (mouse_tile == MOUSE_REPAIR) {
+        else if (m_mouseTile == MOUSE_REPAIR) {
             mouseDrawX -= 16;
             mouseDrawY -= 16;
         }
-        else if (mouse_tile == MOUSE_FORBIDDEN) {
+        else if (m_mouseTile == MOUSE_FORBIDDEN) {
             mouseDrawX -= 16;
             mouseDrawY -= 16;
         }
-        else if (mouse_tile == MOUSE_PICK) {
+        else if (m_mouseTile == MOUSE_PICK) {
             mouseDrawX -= 16;
             mouseDrawY -= 16;
         }
         else {
         }
-
-        if (game.isDebugMode()) {
-            if (game.isState(GAME_PLAYING)) {
-                int mouseCell = players[HUMAN].getGameControlsContext()->getMouseCell(); // Ugh :/
-                m_textDrawer->drawText(0, cSideBar::TopBarHeight + 1, std::format("MouseCell {}", mouseCell));
-            }
-        }
     }
 
-    renderDrawer->renderSprite(gfxdata->getTexture(mouse_tile),mouseDrawX, mouseDrawY);
-
-    if (game.isDebugMode()) {
-        int y = mouseDrawY;
-        for (auto line: debugLines) {
-            m_textDrawer->drawText(mouseDrawX + 32, y, line.c_str());
-            y += m_textDrawer->getFontHeight() + 2;
-        }
-    }
+    auto gfxdata = m_ctx->getGraphicsContext()->gfxdata;
+    m_sdlDrawer->renderSprite(gfxdata->getTexture(m_mouseTile),mouseDrawX, mouseDrawY);
 }
 
 bool cMouse::isNormalRightClick()
 {
     // < -1 means we have had this evaluation before :/
     // poor man's solution as opposed to events
-    return mouse_mv_x2 < -1 && mouse_mv_y2 < -1;
+    return m_mouseMvX2 < -1 && m_mouseMvY2 < -1;
 }
 
 int cMouse::getMouseDragDeltaX()
 {
-    return mouse_mv_x2 - mouse_mv_x1;
+    return m_mouseMvX2 - m_mouseMvX1;
 }
 
 int cMouse::getMouseDragDeltaY()
 {
-    return mouse_mv_y2 - mouse_mv_y1;
+    return m_mouseMvY2 - m_mouseMvY1;
 }
 
 cPoint cMouse::getMouseCoords() {
@@ -389,20 +416,20 @@ cPoint cMouse::getMouseCoords() {
 
 cPoint cMouse::getDragLineStartPoint()
 {
-    return cPoint(mouse_mv_x1, mouse_mv_y1);
+    return cPoint(m_mouseMvX1, m_mouseMvY1);
 }
 
 cPoint cMouse::getDragLineEndPoint()
 {
-    return cPoint(mouse_mv_x2, mouse_mv_y2);
+    return cPoint(m_mouseMvX2, m_mouseMvY2);
 }
 
 void cMouse::setTile(int value)
 {
-    if (value != mouse_tile) {
-        logbook(std::format("cMouse::setTile(): Changing mouse tile from {} ({}) to {} ({})", mouse_tile,
-                            mouseTileName(mouse_tile).c_str(), value, mouseTileName(value).c_str()));
-        mouse_tile = value;
+    if (value != m_mouseTile) {
+        Logger::info(COMP_NONE, "cMouse::setTile", "Changing mouse tile from {} ({}) to {} ({})", m_mouseTile,
+                     mouseTileName(m_mouseTile).c_str(), value, mouseTileName(value).c_str());
+        m_mouseTile = value;
     }
 }
 
@@ -426,7 +453,3 @@ std::string cMouse::mouseTileName(int tile)
     return "UNKNOWN";
 }
 
-void cMouse::addDebugLine(std::string basicString)
-{
-    this->debugLines.push_back(basicString);
-}


=== PORT: src/gameobjects/map/cMapCamera.cpp ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/map/cMapCamera.cpp
stdout:
diff --git a/src/gameobjects/map/cMapCamera.cpp b/src/gameobjects/map/cMapCamera.cpp
new file mode 100644
index 00000000..bd828bf1
--- /dev/null
+++ b/src/gameobjects/map/cMapCamera.cpp
@@ -0,0 +1,463 @@
+/**
+ * @file cMapCamera.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
+#include "cMapCamera.h"
+
+#include "controls/cMouse.h"
+#include "controls/eKeyAction.h"
+#include "data/gfxdata.h"
+#include "sidebar/cSideBar.h"
+#include "gameobjects/map/MapGeometry.hpp"
+#include "game/cGameSettings.h"
+#include "gameobjects/map/cMap.h"
+#include <algorithm>
+#include "include/cAssert.h"
+
+namespace {
+constexpr auto kMapBoundaryScrollSpeed = 5.0f;
+}
+
+cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
+    m_moveSpeedDrag(moveSpeedDrag),
+    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
+    m_cameraEdgeMove(cameraEdgeMove),
+    m_pMap(theMap),
+    m_mapGeometry(theMap->getGeometry()),
+    m_gameSettings(gameSettings),
+    m_mouse(mouse)
+{
+    d2tm_assert(theMap != nullptr);
+    d2tm_assert(gameSettings != nullptr);
+    d2tm_assert(mouse != nullptr);
+    m_viewportStartX = m_viewportStartY = 32;
+    m_zoomLevel = std::clamp(m_gameSettings->getWorldScaleFactor(), 0.25f, 4.0f);
+
+    int widthOfSidebar = cSideBar::SidebarWidth;
+    m_heightOfTopBar = cSideBar::TopBarHeight;
+
+    m_windowWidth= m_gameSettings->getScreenW() - widthOfSidebar;
+    m_windowHeight= m_gameSettings->getScreenH() - m_heightOfTopBar;
+
+    m_viewportWidth=m_windowWidth;
+    m_viewportHeight=m_windowHeight;
+
+    m_moveX = 0.0f;
+    m_moveY = 0.0f;
+
+    m_keyPressedDown = false;
+    m_keyPressedUp = false;
+    m_keyPressedLeft = false;
+    m_keyPressedRight = false;
+
+    calibrate();
+}
+
+cMapCamera::~cMapCamera()
+{
+}
+
+void cMapCamera::resetZoom()
+{
+    setZoomLevel(m_gameSettings->getWorldScaleFactor());
+}
+
+void cMapCamera::trackToAbsPosition(float absX, float absY)
+{
+    m_viewportStartX = absX - (m_viewportWidth / 2.0f);
+    m_viewportStartY = absY - (m_viewportHeight / 2.0f);
+    keepViewportWithinReasonableBounds();
+}
+
+void cMapCamera::zoomOutToFit(const cRectangle& bounds)
+{
+    float zoomToFit = std::min(
+        static_cast<float>(m_windowWidth) / bounds.getWidth(),
+        static_cast<float>(m_windowHeight) / bounds.getHeight()
+    );
+    if (zoomToFit < m_zoomLevel) {
+        setZoomLevel(zoomToFit);
+    }
+}
+
+void cMapCamera::setZoomLevel(float zoom)
+{
+    if (zoom < 0.25f) zoom = 0.25f;
+    if (zoom > 4.0f) zoom = 4.0f;
+    m_zoomLevel = zoom;
+    calibrate();
+    keepViewportWithinReasonableBounds();
+}
+
+void cMapCamera::zoomIn()
+{
+    if (m_zoomLevel < 4.0) {
+        m_zoomLevel += 0.1;
+        adjustViewport(m_mouse->getX(), m_mouse->getY());
+    }
+}
+
+void cMapCamera::adjustViewport(float screenX, float screenY)
+{
+    int oldViewportWidth = m_viewportWidth;
+    int oldViewportHeight = m_viewportHeight;
+
+    calibrate();
+
+    int diffViewportWidth = oldViewportWidth - m_viewportWidth;
+    int diffViewportHeight = oldViewportHeight - m_viewportHeight;
+
+    float nMouseX = screenX / m_windowWidth;
+    float nMouseY = (screenY - m_heightOfTopBar) / m_windowHeight;
+
+    m_viewportStartX += diffViewportWidth * nMouseX;
+    m_viewportStartY += diffViewportHeight * nMouseY;
+
+    keepViewportWithinReasonableBounds();
+}
+
+void cMapCamera::zoomOut()
+{
+    if (m_zoomLevel > 0.25) {
+        m_zoomLevel -= 0.1;
+        adjustViewport(m_mouse->getX(), m_mouse->getY());
+    }
+}
+
+void cMapCamera::calibrate()
+{
+    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
+    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
+
+    m_viewportWidth = divideByZoomLevel(m_windowWidth);
+    m_viewportHeight = divideByZoomLevel(m_windowHeight);
+}
+
+void cMapCamera::keepViewportWithinReasonableBounds()
+{
+    int halfViewportWidth = m_viewportWidth / 2;
+    int halfViewportHeight = m_viewportHeight / 2;
+
+    if (m_viewportStartX < -halfViewportWidth) {
+        m_viewportStartX = -halfViewportWidth;
+    }
+
+    if (m_viewportStartY < -halfViewportHeight) {
+        m_viewportStartY = -halfViewportHeight;
+    }
+
+    int maxWidth = (m_pMap->getGeometry()->getWidth() * TILESIZE_WIDTH_PIXELS) + halfViewportWidth;
+    if (getViewportEndX() > maxWidth) {
+        m_viewportStartX = maxWidth - m_viewportWidth;
+    }
+
+    int maxHeight = (m_pMap->getGeometry()->getHeight() * TILESIZE_HEIGHT_PIXELS) + halfViewportHeight;
+    if ((getViewportEndY()) > maxHeight) {
+        m_viewportStartY = maxHeight - m_viewportHeight;
+    }
+}
+
+void cMapCamera::centerAndJumpViewPortToCell(int cell)
+{
+    // fix any boundaries
+    if (cell < 0) cell = 0;
+    if (cell >= m_pMap->getMaxCells()) cell = (m_pMap->getMaxCells()-1);
+
+    int mapCellX = m_mapGeometry->getAbsoluteXPositionFromCell(cell);
+    int mapCellY = m_mapGeometry->getAbsoluteYPositionFromCell(cell);
+
+    // determine the half of our screen
+    int halfViewportWidth = m_viewportWidth / 2;
+    int halfViewportHeight = m_viewportHeight / 2;
+
+    // determine the new X and Y position, absolute map coordinates
+    int newViewPortX = mapCellX - halfViewportWidth;
+    int newViewPortY = mapCellY - halfViewportHeight;
+
+    // for now, snap it to 32x32 grid
+    newViewPortX = (newViewPortX / 32) * 32;
+    newViewPortY = (newViewPortY / 32) * 32;
+
+    jumpTo(newViewPortX, newViewPortY);
+
+    calibrate();
+
+    keepViewportWithinReasonableBounds();
+}
+
+void cMapCamera::thinkFast()
+{
+    // update viewport coordinates
+    m_viewportStartX = m_viewportStartX + m_moveX;
+    m_viewportStartY = m_viewportStartY + m_moveY;
+
+    keepViewportWithinReasonableBounds();
+
+}
+
+void cMapCamera::jumpTo(int theX, int theY)
+{
+    m_viewportStartX = theX;
+    m_viewportStartY = theY;
+    calibrate();
+}
+
+void cMapCamera::setViewportPosition(int x, int y)
+{
+    jumpTo(x, y);
+    keepViewportWithinReasonableBounds();
+}
+
+void cMapCamera::saveViewportBookmark(int bookmarkNumber)
+{
+    if (bookmarkNumber < 1 || bookmarkNumber > MaxViewportBookmarks) return;
+
+    sViewportBookmark &bookmark = m_viewportBookmarks[bookmarkNumber - 1];
+    bookmark.isSet = true;
+    bookmark.x = m_viewportStartX;
+    bookmark.y = m_viewportStartY;
+    bookmark.zoomLevel = m_zoomLevel;
+}
+
+void cMapCamera::jumpToViewportBookmark(int bookmarkNumber)
+{
+    if (bookmarkNumber < 1 || bookmarkNumber > MaxViewportBookmarks) return;
+
+    const sViewportBookmark &bookmark = m_viewportBookmarks[bookmarkNumber - 1];
+    if (!bookmark.isSet) return;
+
+    setZoomLevel(bookmark.zoomLevel);
+    setViewportPosition(static_cast<int>(bookmark.x), static_cast<int>(bookmark.y));
+}
+
+void cMapCamera::resetViewportBookmarks()
+{
+    m_viewportBookmarks.fill(sViewportBookmark{});
+}
+
+int cMapCamera::getCellFromAbsolutePosition(int x, int y)
+{
+    return m_mapGeometry->getCellWithMapDimensions((x / 32), (y / 32));
+}
+
+int cMapCamera::getCellFromAbsolutePositionClamped(int x, int y)
+{
+    int cx, cy;
+    cPoint::split(cx, cy) = m_mapGeometry->fixCoordinatesToBeWithinPlayableMap((x / 32), (y / 32));
+    return m_mapGeometry->makeCell(cx, cy);
+}
+
+void cMapCamera::onNotifyMouseEvent(const s_MouseEvent &event)
+{
+    // MOUSE WHEEL scrolling causes zooming in/out
+    switch (event.eventType) {
+        case eMouseEventType::MOUSE_MOVED_TO:
+            onMouseMovedTo(event);
+            break;
+        case eMouseEventType::MOUSE_SCROLLED_DOWN:
+            zoomOut();
+            break;
+        case eMouseEventType::MOUSE_SCROLLED_UP:
+            zoomIn();
+            break;
+        case eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED:
+            onMouseRightButtonPressed(event);
+            break;
+        case eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED:
+            onMouseRightButtonClicked(event);
+            break;
+        default:
+            break;
+    }
+}
+
+void cMapCamera::onMouseMovedTo(const s_MouseEvent &event)
+{
+    // mouse is 'moving by pressing right mouse button', this supersedes behavior with edges
+    if (!m_mouse->isMapScrolling() && m_cameraEdgeMove) {
+
+        int mouseX = event.coords.x;
+        int mouseY = event.coords.y;
+
+        if (mouseX <= 2) {
+            setMoveX(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_LEFT);
+        }
+        else if (mouseX >= (m_gameSettings->getScreenW() - 2)) {
+            setMoveX(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_RIGHT);
+        }
+        else {
+            if (!m_keyPressedLeft && !m_keyPressedRight) {
+                setMoveX(0.0f, m_moveSpeedBorderOrKeys);
+            }
+        }
+
+        if (mouseY <= 2) {
+            setMoveY(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_UP);
+        }
+        else if (mouseY >= (m_gameSettings->getScreenH() - 2)) {
+            setMoveY(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_DOWN);
+        }
+        else {
+            if (!m_keyPressedUp && !m_keyPressedDown) {
+                setMoveY(0.0f, m_moveSpeedBorderOrKeys);
+            }
+        }
+    }
+}
+
+void cMapCamera::onNotifyKeyboardEvent(const cKeyboardEvent &event)
+{
+    switch (event.getType()) {
+        case eKeyEventType::HOLD:
+            onKeyHold(event);
+            break;
+        case eKeyEventType::PRESSED:
+            onKeyPressed(event);
+            break;
+        default:
+            break;
+    }
+}
+
+void cMapCamera::onMouseRightButtonPressed(const s_MouseEvent &)
+{
+    m_moveX = 0.0f;
+    m_moveY = 0.0f;
+
+    // mouse is 'moving by pressing right mouse button', this supersedes behavior with borders
+    if (m_mouse->isMapScrolling()) {
+        // difference in pixels (- means up/left, + means down/right)
+        int diffX = m_mouse->getMouseDragDeltaX();
+        int diffY = m_mouse->getMouseDragDeltaY();
+
+        // now calculate the speed in which we want to do this, the further
+        // away (greater distance) the faster.
+        float factorX = static_cast<float>(abs(diffX)) / (m_windowWidth / 2);
+        float factorY = static_cast<float>(abs(diffY)) / (m_windowHeight / 2);
+
+        // now we know factor, we only want to move so fast in pixels, so clamp/keep the diffX/Y between sane
+        // values. If we don't do this, the scrolling is too fast. Also take m_zoomLevel into account so when we
+        // zoom in, it won't go faster. And if we have zoomed out, it will be faster, but relatively the same speed as
+        // zoom factor 1.0
+        diffX = divideByZoomLevel(std::clamp(diffX, -24, 24));
+        diffY = divideByZoomLevel(std::clamp(diffY, -24, 24));
+
+        float resultX = diffX * factorX;
+        float resultY = diffY * factorY;
+
+        setMoveX(resultX, m_moveSpeedDrag);
+        setMoveY(resultY, m_moveSpeedDrag);
+
+        // reset keyboard state, as this supersedes keyboard movement
+        m_keyPressedDown = false;
+        m_keyPressedUp = false;
+        m_keyPressedLeft = false;
+        m_keyPressedRight = false;
+
+        return;
+    }
+}
+
+void cMapCamera::setMoveX(float x, float moveSpeed)
+{
+    m_moveX = x * moveSpeed;
+}
+
+void cMapCamera::setMoveY(float y, float moveSpeed)
+{
+    m_moveY = y * moveSpeed;
+}
+
+void cMapCamera::onKeyHold(const cKeyboardEvent &event)
+{
+    // mouse is 'moving by pressing right mouse button', this supersedes reacting to keypress
+    if (!m_mouse->isMapScrolling()) {
+        if (event.isAction(eKeyAction::SCROLL_LEFT)) {
+            setMoveX(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_LEFT);
+            m_keyPressedLeft = true;
+        }
+
+        if (event.isAction(eKeyAction::SCROLL_UP)) {
+            setMoveY(-kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_UP);
+            m_keyPressedUp = true;
+        }
+
+        if (event.isAction(eKeyAction::SCROLL_RIGHT)) {
+            setMoveX(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_RIGHT);
+            m_keyPressedRight = true;
+        }
+
+        if (event.isAction(eKeyAction::SCROLL_DOWN)) {
+            setMoveY(kMapBoundaryScrollSpeed, m_moveSpeedBorderOrKeys);
+            m_mouse->setTile(MOUSE_DOWN);
+            m_keyPressedDown = true;
+        }
+    }
+}
+
+void cMapCamera::onKeyPressed(const cKeyboardEvent &event)
+{
+    if (event.isAction(eKeyAction::SCROLL_LEFT)) {
+        setMoveX(0.0f, m_moveSpeedBorderOrKeys);
+        m_keyPressedLeft = false;
+    }
+
+    if (event.isAction(eKeyAction::SCROLL_UP)) {
+        setMoveY(0.0f, m_moveSpeedBorderOrKeys);
+        m_keyPressedUp = false;
+    }
+
+    if (event.isAction(eKeyAction::SCROLL_RIGHT)) {
+        setMoveX(0.0f, m_moveSpeedBorderOrKeys);
+        m_keyPressedRight = false;
+    }
+
+    if (event.isAction(eKeyAction::SCROLL_DOWN)) {
+        setMoveY(0.0f, m_moveSpeedBorderOrKeys);
+        m_keyPressedDown = false;
+    }
+
+    int saveBookmarkNumber = event.getSaveViewportBookmarkNumber();
+    if (saveBookmarkNumber > 0) {
+        saveViewportBookmark(saveBookmarkNumber);
+    }
+
+    int jumpBookmarkNumber = event.getJumpToViewportBookmarkNumber();
+    if (jumpBookmarkNumber > 0) {
+        jumpToViewportBookmark(jumpBookmarkNumber);
+    }
+}
+
+void cMapCamera::onMouseRightButtonClicked(const s_MouseEvent &)
+{
+    m_moveX = 0.0f;
+    m_moveY = 0.0f;
+}
+
+int cMapCamera::getWindowXPositionFromCellWithOffset(int cell, int offset) {
+    int absoluteXPosition = m_mapGeometry->getAbsoluteXPositionFromCell(cell);
+    return getWindowXPositionWithOffset(absoluteXPosition, offset);
+}
+
+int cMapCamera::getWindowYPositionFromCellWithOffset(int cell, int offset) {
+    int absoluteYPosition = m_mapGeometry->getAbsoluteYPositionFromCell(cell);
+    return getWindowYPositionWithOffset(absoluteYPosition, offset);
+}


=== PORT: src/gameobjects/map/cMapCamera.h ===
$ git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/map/cMapCamera.h
stdout:
diff --git a/src/gameobjects/map/cMapCamera.h b/src/gameobjects/map/cMapCamera.h
new file mode 100644
index 00000000..53088b49
--- /dev/null
+++ b/src/gameobjects/map/cMapCamera.h
@@ -0,0 +1,281 @@
+/**
+ * @file cMapCamera.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
+/*
+ * cMapCamera.h
+ *
+ *  A map camera is 'looking' at the map. Using this camera (or viewport) we can determine
+ *  what to draw, how big, etc.
+ *
+ *  Using a camera technique we can easily adjust the drawing logic whenever the resolution
+ *  of the game changes.
+ *
+ */
+
+#pragma once
+
+// #include "cMap.h"
+
+#include "observers/cInputObserver.h"
+#include "utils/cRectangle.h"
+#include <array>
+#include <cmath>
+
+class cMap;
+class MapGeometry;
+class cGameSettings;
+class cMouse;
+
+class cMapCamera : cInputObserver {
+
+public:
+    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse);
+
+    ~cMapCamera();
+
+    void onNotifyMouseEvent(const s_MouseEvent &event) override;
+    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
+
+    void thinkFast();
+
+    void resetZoom();
+
+    void setZoomLevel(float zoom);
+
+    void zoomOutToFit(const cRectangle& bounds);
+
+    void jumpTo(int theX, int theY);
+
+    void moveTo(int theX, int theY);
+
+    /**
+     * Returns the pixel coordinate on the window to draw onto. Use this function to convert absolute
+     * coordinates into window coordinates so you can draw something.
+     * @param absoluteXPosition
+     * @return
+     */
+    int getWindowXPosition(int absoluteXPosition) {
+        return getWindowXPositionWithOffset(absoluteXPosition, 0);
+    }
+
+    int getWindowYPosition(int absoluteYPosition) {
+        return getWindowYPositionWithOffset(absoluteYPosition, 0);
+    }
+
+    int getWindowXPositionFromCell(int cell) {
+        return getWindowXPositionFromCellWithOffset(cell, 0);
+    }
+
+    int getWindowYPositionFromCell(int cell) {
+        return getWindowYPositionFromCellWithOffset(cell, 0);
+    }
+
+    int getWindowXPositionFromCellWithOffset(int cell, int offset);
+    int getWindowYPositionFromCellWithOffset(int cell, int offset);
+
+    /**
+     * Translates an absolute X position into a position on the window. The offset is added after translating
+     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
+     * @param absoluteXPosition
+     * @param offset
+     * @return
+     */
+    int getWindowXPositionWithOffset(int absoluteXPosition, int offset) {
+        return std::round(factorZoomLevel((absoluteXPosition - m_viewportStartX) + offset));
+    }
+
+    /**
+     * Translates an absolute Y position into a position on the window. The offset is added after translating
+     * between absolute x coordinate to window coordinate. Zoom level is applied at last.
+     * @param absoluteYPosition
+     * @param offset
+     * @return
+     */
+    int getWindowYPositionWithOffset(int absoluteYPosition, int offset) {
+        return std::round(factorZoomLevel((absoluteYPosition - m_viewportStartY) + offset) + m_heightOfTopBar);
+    }
+
+    // These methods need to use zoomfactor to properly calculate the position on the map
+    int getAbsMapMouseX(int mouseX) {
+        int iMouseX = divideByZoomLevel(mouseX);
+        return iMouseX + getViewportStartX();
+    }
+
+    int getAbsMapMouseY(int mouseY) {
+        int iMouseY = divideByZoomLevel(mouseY - m_heightOfTopBar);
+        return iMouseY + getViewportStartY();
+    }
+
+    int getViewportStartX() {
+        return m_viewportStartX;
+    }
+
+    int getViewportStartY() {
+        return m_viewportStartY;
+    }
+
+    int getViewportEndX() {
+        return m_viewportStartX + m_viewportWidth;
+    }
+
+    int getViewportEndY() {
+        return m_viewportStartY + m_viewportHeight;
+    }
+
+    int getViewportWidth() {
+        return m_viewportWidth;
+    }
+
+    int getViewportHeight() {
+        return m_viewportHeight;
+    }
+
+    int getViewportCenterX() {
+        return m_viewportStartX + (m_viewportWidth / 2);
+    }
+
+    int getViewportCenterY() {
+        return m_viewportStartY + (m_viewportHeight / 2);
+    }
+
+    void centerAndJumpViewPortToCell(int cell);
+
+    static constexpr int MaxViewportBookmarks = 5;
+
+    /**
+     * Saves the current viewport position and zoom level into the given bookmark slot (1-5).
+     */
+    void saveViewportBookmark(int bookmarkNumber);
+
+    /**
+     * Jumps to the viewport position and zoom level stored in the given bookmark slot (1-5).
+     * Does nothing if that slot has never been saved.
+     */
+    void jumpToViewportBookmark(int bookmarkNumber);
+
+    /**
+     * Clears all viewport bookmarks. Called when a new mission/skirmish starts.
+     */
+    void resetViewportBookmarks();
+
+    void trackToAbsPosition(float absX, float absY);
+
+    float getZoomedTileWidth() const {
+        return m_tileWidth;
+    }
+
+    float getZoomedTileHeight() const {
+        return m_tileHeight;
+    }
+
+    float factorZoomLevel(int value) {
+        return value * m_zoomLevel;
+    }
+
+    float factorZoomLevel(float value) {
+        return value * m_zoomLevel;
+    }
+
+    float divideByZoomLevel(int value) {
+        return value / m_zoomLevel;
+    }
+
+    float divideByZoomLevel(float value) {
+        return value / m_zoomLevel;
+    }
+
+    int getWindowWidth() {
+        return m_windowWidth;
+    }
+
+    int getWindowHeight() {
+        return m_windowHeight;
+    }
+
+    float getZoomLevel() {
+        return m_zoomLevel;
+    }
+
+    int getCellFromAbsolutePosition(int x, int y);
+    int getCellFromAbsolutePositionClamped(int x, int y);
+
+    void setViewportPosition(int x, int y);
+
+private:
+    // rendering coordinates, they are manipulated by zooming
+    float m_viewportStartX;
+    float m_viewportStartY;
+    int m_viewportWidth;
+    int m_viewportHeight;
+
+    // used for moving
+    float m_moveX;
+    float m_moveY;
+    float m_moveSpeedDrag;
+    float m_moveSpeedBorderOrKeys;
+    bool m_cameraEdgeMove;
+
+    bool m_keyPressedUp;
+    bool m_keyPressedDown;
+    bool m_keyPressedLeft;
+    bool m_keyPressedRight;
+
+    int m_heightOfTopBar;
+    int m_windowWidth;
+    int m_windowHeight;
+
+    // Zoom level, 1 == normal, > 1 is zooming in. < 1 is zooming out.
+    float m_zoomLevel;
+
+    // the calculated width and height, taking zoomlevel into account
+    float m_tileHeight;
+    float m_tileWidth;
+
+    // the map this camera is viewing
+    cMap *m_pMap;
+    MapGeometry *m_mapGeometry = nullptr;
+    cGameSettings *m_gameSettings;
+    cMouse *m_mouse;
+
+    void adjustViewport(float screenX, float screenY);
+
+    // Calculates viewport and tile width/height
+    void calibrate();
+
+    void keepViewportWithinReasonableBounds();
+
+    void zoomIn();
+    void zoomOut();
+
+    void onMouseMovedTo(const s_MouseEvent &event);
+
+    void onMouseRightButtonClicked(const s_MouseEvent &event);
+    void onMouseRightButtonPressed(const s_MouseEvent &event);
+
+    void setMoveX(float x, float moveSpeed);
+    void setMoveY(float y, float moveSpeed);
+
+    void onKeyHold(const cKeyboardEvent &event);
+    void onKeyPressed(const cKeyboardEvent &event);
+
+    struct sViewportBookmark {
+        bool isSet = false;
+        float x = 0.0f;
+        float y = 0.0f;
+        float zoomLevel = 1.0f;
+    };
+
+    std::array<sViewportBookmark, MaxViewportBookmarks> m_viewportBookmarks;
+};


=== Камера: git grep ===
Ранее собранные точные команды и stdout для поиска методов камеры в PORT сохранены без изменения в `.tmp/p5cr2/git-grep-port.txt`.

$ git grep -n -F findTileIndex( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::cMapCamera( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:32:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
$ git grep -n -F cMapCamera::resetZoom( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:71:void cMapCamera::resetZoom()
$ git grep -n -F cMapCamera::zoomIn( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:103:void cMapCamera::zoomIn()
$ git grep -n -F cMapCamera::zoomOut( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:130:void cMapCamera::zoomOut()
$ git grep -n -F cMapCamera::centerAndJumpViewPortToCell( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:171:void cMapCamera::centerAndJumpViewPortToCell(int cell)
$ git grep -n -F cMapCamera::thinkFast( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:199:void cMapCamera::thinkFast()
$ git grep -n -F cMapCamera::jumpTo( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:209:void cMapCamera::jumpTo(int theX, int theY)
$ git grep -n -F cMapCamera::setViewportPosition( 832c953a94a632d57872349013f7ed1a37434715 -- src
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:216:void cMapCamera::setViewportPosition(int x, int y)
$ git grep -n -F cMapCamera::getCellFromWindowPosition( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::refreshMouseHover( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::getAbsMapMouseX( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::getAbsMapMouseY( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::getTileDrawWidth( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)
$ git grep -n -F cMapCamera::getTileDrawHeight( 832c953a94a632d57872349013f7ed1a37434715 -- src
(совпадений нет)

## 2. Ветвления HD в FORK1

```tsv
путь	путь@9208dcf:строка	условие	ветка «да»	ветка «нет»
```
# P5CR2, дорожка 3: журнал проверки пунктов 2–4


### Пункт 2 — инвентарь условий if / else if / ?: по полным файлам

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'if[[:space:]]*\(|else[[:space:]]+if|\?' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:68:    if (hasDrawnCurrentCredits() || initial) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:75:        // TODO: make it 'roll' instead of 'jump' to the newest credits?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:79:        if (newCurrentCredits != previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:83:            if (diff > 200) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:86:            else if (diff > 20) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:95:        if (currentCredits > previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:98:        else if (currentCredits < previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:106:        if (TIMER_money > 20) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:107:            if (rollSpeed > 0.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:110:            if (rollSpeed < 0.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:120:        if (rollSpeed < 3.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:142:        if (offset_direction[i] == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:143:            if (currentId == CREDITS_NONE || previousId == CREDITS_NONE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:151:            if (currentCredits > previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:154:            else if (previousCredits > currentCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:159:            if (currentId == previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:166:        if (offset_credit[i] > 18.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:169:            if (soundsMade < 7) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:250:    if (c == '0') return CREDITS_0;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:251:    if (c == '1') return CREDITS_1;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:252:    if (c == '2') return CREDITS_2;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:253:    if (c == '3') return CREDITS_3;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:254:    if (c == '4') return CREDITS_4;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:255:    if (c == '5') return CREDITS_5;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:256:    if (c == '6') return CREDITS_6;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:257:    if (c == '7') return CREDITS_7;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:258:    if (c == '8') return CREDITS_8;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:259:    if (c == '9') return CREDITS_9;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:278://			if (currentId > previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:280://			} else if (currentId < previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.h:56:    int rolled; // how many credits did get rolled over?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:22:    if (text.empty()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:38:    if (drawer->getTextLength(text) <= maximumWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:53:    if (name == localization::text("Hi-Tech", "Авиазавод")) return localization::text("Hi-Tech", "Авиазавод");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:54:    if (name == localization::text("Spice Refinery", "Переработчик пряности")) return localization::text("Refinery", "Переработчик");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:55:    if (name == localization::text("MCV", "Мобильная база")) return localization::text("MCV", "Мобильная база");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:56:    if (name == localization::text("Light Infantry", "Отряд пехоты")) return localization::text("Infantry", "Пехота");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:57:    if (name == localization::text("Troopers", "Отряд ракетчиков")) return localization::text("Troopers", "Ракетчики");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:74:    if (listIDToDraw == eListTypeAsInt(eListType::LIST_CONSTYARD)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:117:    if (pressed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:121:    if (id < 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:123:        logbook("ERROR UNABLE TO DRAW LIST BECAUSE ID IS NOT VALID!?");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:154:        list->isAvailable() ? 255 : 96
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:156:    if (!list->isAvailable()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:168:        pressed ? active : border
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:170:    if (pressed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:180:    else if (list->isFlashing()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:219:    // is building an item in the list?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:238:        if (item == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:243:        if (card.getEndY() <= layout.cards.getY() ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:261:        if (shouldDrawStructureSize) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:266:        if (item->isBuilding()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:269:            if (!item->isDoneBuilding() || iFrame < 31) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:295:                if (item->shouldPlaceIt()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:298:                    ) ? Color{225, 48, 42, 255} : Color::white();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:306:                else if (item->shouldDeployIt()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:309:                    ) ? Color{225, 48, 42, 255} : Color::white();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:330:                if (isBuildingItemInList[i2] < 0) continue;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:331:                if (i2 == item->getSubList()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:337:            if (!item->isAvailable() || isBuildingSameSubListItem) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:350:                if (item->isPendingUpgrading()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:361:                if (item->isPendingBuilding()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:379:            if (list->getType() == eListType::LIST_STARPORT) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:382:                if (cannotPayIt) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:401:            if (list->getLastClickedId() == i) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:413:        if (listIsStarport) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:418:        if (showAmount) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:423:            if (amountToShow < 10) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:442:        if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:443:            if (m_renderListIds) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:453:        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:459:            if (item->isFlashing()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:485:    if (iW == 2 && iH == 2) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:489:    if (iW == 3 && iH == 2) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:493:    if (iW == 3 && iH == 3) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:506:    if (x >= drawX &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:520:    if (!layout.cards.isPointWithin(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:526:        if (item == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:530:        if (card.getY() < layout.cards.getY() ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:534:        if (card.isPointWithin(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:612:    if (m_smallTextDrawer->getTextLength(name) <= textWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:634:                ? candidateWord
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:636:            if (secondLine.empty() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:642:                    ? candidateWord
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:649:            firstLine.empty() ? name : firstLine,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:658:        if (secondLine.empty()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:687:    if (item->getBuildCost() > 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:737:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:741:    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:753:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:757:    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:769:    if (m_player == nullptr || m_player->getSideBar() == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:774:    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:803:    if (layout.maxScrollRow(list->getItemCount()) <= 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:821:    if (m_player == nullptr ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:828:    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:832:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:837:    if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:841:    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_UP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:845:    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:849:    if (event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:858:    if (event.coords.y < thumb.getY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:861:    else if (event.coords.y > thumb.getEndY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:882:    if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:889:    if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:41:    if (m_state == messages::eMessageDrawerState::COMBAT) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:49:            ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:57:            ? music.panel.getEndX() + 8
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:80:            ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:83:        if (m_alpha > -1 && messageTextWidth > 0 && messageContentWidth > 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:85:            if (messageTextWidth <= messageContentWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:96:                if (scale >= 0.5F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:115:    if (m_alpha > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:130:    if (m_fadeState == messages::eMessageDrawerFadingState::FADE_IN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:133:        if (m_TIMER_message > m_timeMessageIsVisible) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:134:            if (!m_keepMessage) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:141:        if (m_alpha > 254) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:149:    if (m_alpha < 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:154:    if (m_alpha < 1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:175:    if (m_bmpBar != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:232:    if (m_bmpBar) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:73:    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:76:    if (!m_map) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:80:    if (m_status == eMinimapStatus::NOTAVAILABLE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:84:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:89:    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:94:    if (m_status == eMinimapStatus::LOWPOWER) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:113:    if (m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:114:        if (m_status == eMinimapStatus::NOTAVAILABLE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:122:    if (m_status == eMinimapStatus::NOTAVAILABLE) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:127:    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:128:        if (!hasRadarAndEnoughPower) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:137:    if (m_status == eMinimapStatus::POWERDOWN || m_status == eMinimapStatus::LOWPOWER) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:138:        if (hasRadarAndEnoughPower) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:149:    if (m_status == eMinimapStatus::POWERDOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:150:        if (m_iStaticFrame < STAT21) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:157:    else if (m_status == eMinimapStatus::POWERUP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:158:        if (m_iStaticFrame > STAT01) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:204:            //@mira where is map ?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:207:            if (m_map->isVisible(iCll, m_player->getId())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:213:            if (!m_map->isWithinBoundaries(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:240:    if (startX < m_RectFullMinimap.getX()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:244:    if (startY < m_RectFullMinimap.getY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:248:    if (startX + minimapWidth > m_RectFullMinimap.getEndX()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:251:    if (startY + minimapHeight > m_RectFullMinimap.getEndY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:268:            if (!m_map->isWithinBoundaries(x, y)) continue;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:272:            if (!m_map->isVisible(iCll, m_player->getId())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:281:            if (idOfStructureAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:283:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:284:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:290:            if (idOfUnitAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:292:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:293:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:299:            if (idOfAirUnitAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:301:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:302:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:308:            if (idOfWormAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:309:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:316:            if (iColor.r == black.r && iColor.g == black.g && iColor.b == black.b) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:369:    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:373:        if (m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.h:67:    //@mira : where is map ? Where is this initialisation ?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:69:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:81:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:113:    if (m_player->isHouse(ATREIDES)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:116:    if (m_player->isHouse(HARKONNEN)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:119:    if (m_player->isHouse(ORDOS)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:127:    if (m_player->isHouse(ATREIDES)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:130:    if (m_player->isHouse(HARKONNEN)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:133:    if (m_player->isHouse(ORDOS)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:182:    if (crest != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:216:    if (!m_player->hasRadarAndEnoughPower() && crest != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:253:        ? m_player->getErrorFadingColor()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:316:        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:325:        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:338:    if (selectedListId >= 0 && selectedListId < cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:366:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:384:    if (selectedList != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:390:        if (listId == selectedListId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:394:        if (list->isAvailable() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:400:    if (selectedList != nullptr &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:97:    if (game.m_drawUsages) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:107:        if (unit[i].isValid()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:115:        if (pStructure) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:123:        if (pBullet.bAlive) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:131:        if (pParticle.isValid()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:155:    if (humanPlayer.selected_structure < 0) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:157:    if (!theStructure) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:159:    if (rallyPointCell < 0) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:198:    // TODO: move drawing this into mouse state draw function ??
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:199:    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:200:    if (!m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:203:    if (itemToPlace == nullptr) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:212:    // TODO: replace messageDrawer with drawMessageBar?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:222:    if (context->shouldDrawToolTip()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:234:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:275:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:278:    if (game.getMouse()->isLeftButtonClicked() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:300:        ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:307:    if (!layout.visible) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:310:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:328:    if (layout.showsLabel()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:333:               m_smallTextDrawer->getTextLength(name + (truncated ? ellipsis : std::string{})) > layout.label.getWidth() - 10) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:351:        if (!name.empty() && truncated) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:383:    if ((mouse->isLeftButtonPressed() || mouse->isLeftButtonClicked()) && mouseOverSlider) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:386:    if (!mouse->isLeftButtonPressed() && !mouse->isLeftButtonClicked()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:389:    if (m_speedSliderDragging) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:399:        if (requestedGlobalSpeed != globalSpeed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:412:    if (mouse->isLeftButtonClicked()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:413:        if (mouse->isOverRectangle(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:417:        else if (mouse->isOverRectangle(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:480:    if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:481:        if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:484:        if (event.hasKey(SDL_SCANCODE_G)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:492:    if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:495:        if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:498:        if (event.hasKey(SDL_SCANCODE_G)) {
```

Exit code: 0.

### Пункт 2 — все упоминания функций drawHd по полным файлам

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'drawHd[A-Za-z0-9_]*' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:259:        drawHdCard(item, iDrawX, iDrawY);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:467:    drawHdScrollbar(list, layout);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:551:void cBuildingListDrawer::drawHdCard(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:781:void cBuildingListDrawer::drawHdScrollbar(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.h:57:    void drawHdCard(cBuildingListItem *item, int x, int y);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.h:58:    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:72:    drawHdSidebar();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:75:void cSideBarDrawer::drawHdSidebar()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:106:    drawHdRadarPanel();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:107:    drawHdCapacities();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:108:    drawHdBuildingLists();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:139:void cSideBarDrawer::drawHdRadarPanel()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:236:void cSideBarDrawer::drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:306:void cSideBarDrawer::drawHdCapacities()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:314:    drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:323:    drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:333:void cSideBarDrawer::drawHdBuildingLists()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:41:    void drawHdSidebar();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:42:    void drawHdBuildingLists();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:43:    void drawHdRadarPanel();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:44:    void drawHdCapacities();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:45:    void drawHdMeter(
```

Exit code: 0.

### Пункт 2 — cSideBarDrawer::draw и вызов drawHdSidebar

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '64,76p'
```

```text
    64	}
    65	
    66	// draws the sidebar on screen
    67	void cSideBarDrawer::draw()
    68	{
    69	    if (uiaudit::isEnabled()) {
    70	        UiAuditAccess::recordSidebarClicks(*this);
    71	    }
    72	    drawHdSidebar();
    73	}
    74	
    75	void cSideBarDrawer::drawHdSidebar()
    76	{
```

Exit code: 0.

### Пункт 2 — вызов drawHdCard внутри полного draw-list участка

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '225,266p'
```

```text
   225	
   226	    renderDrawer->setClippingFor(
   227	        layout.cards.getX(),
   228	        layout.cards.getY(),
   229	        layout.cards.getEndX(),
   230	        layout.cards.getEndY()
   231	    );
   232	
   233	    // Draw the visible icon rows. HD positions come from HudLayout so drawing
   234	    // and hit testing cannot drift apart.
   235	    for (int i = 0; i < end; i++) {
   236	        cBuildingListItem *item = list->getItem(i);
   237	
   238	        if (item == nullptr) {
   239	            continue; // allow gaps in the list data structure (just not with rendering)
   240	        }
   241	
   242	        const cRectangle card = layout.cardRect(i, scrollRow);
   243	        if (card.getEndY() <= layout.cards.getY() ||
   244	            card.getY() >= layout.cards.getEndY()) {
   245	            continue;
   246	        }
   247	        iDrawX = card.getX();
   248	        iDrawY = card.getY();
   249	
   250	        int iDrawXEnd = iDrawX + withOfIcon;
   251	        int iDrawYEnd = iDrawY + heightOfIcon;
   252	
   253	        // asumes drawing for human player
   254	        bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());
   255	
   256	        // icon id must be set , assert it.
   257	        assert(item->getIconId() > -1);
   258	
   259	        drawHdCard(item, iDrawX, iDrawY);
   260	
   261	        if (shouldDrawStructureSize) {
   262	            drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
   263	        }
   264	
   265	        // when this item is being built.
   266	        if (item->isBuilding()) {
```

Exit code: 0.

### Пункт 2 — безусловный вызов drawHdScrollbar после отрисовки карточек

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '450,472p'
```

```text
   450	
   451	        // draw rectangle when mouse hovers over icon
   452	        auto m_mouse = game.getMouse();
   453	        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
   454	            renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
   455	            renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
   456	        }
   457	        else {
   458	            Color color = list->getFlashingColor();
   459	            if (item->isFlashing()) {
   460	                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
   461	                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
   462	            }
   463	        }
   464	    }
   465	
   466	    renderDrawer->resetClippingFor();
   467	    drawHdScrollbar(list, layout);
   468	}
   469	
   470	/**
   471	 * Draw the amount of squares a structure would take. The X and Y coordinates are the top
   472	 * left coordinates of an icon.
```

Exit code: 0.

### Пункт 2 — безусловные вызовы HD-подфункций боковой панели

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '101,111p'
```

```text
   101	        layout.sidebar.getX() + 5,
   102	        game.m_screenH,
   103	        Color{166, 124, 44, 255}
   104	    );
   105	
   106	    drawHdRadarPanel();
   107	    drawHdCapacities();
   108	    drawHdBuildingLists();
   109	}
   110	
   111	Texture *cSideBarDrawer::getHouseCrest() const
```

Exit code: 0.

# Дополнение к RECON по пунктам 2–4

В `track3-evidence.md` уже сохранены выводы команд для каждой строки трёх TSV. Здесь зафиксирована классификация полного списка `drawHd` и указаны соответствующие секции исходного журнала.

## Пункт 2: классификация всех `drawHd`-упоминаний

Полный вывод `git grep -n -E 'drawHd[A-Za-z0-9_]*'` по десяти файлам дорожки 1 и `src/managers/cDrawManager.cpp` находится в секции «Пункт 2 — все упоминания функций drawHd по полным файлам» файла `track3-evidence.md`. Полный инвентарь `if`, `else if` и `?` находится в секции перед ним. Проверенные места вызова классифицируются так:

| Место | Вызов | Классификация |
| --- | --- | --- |
| `src/drawers/cSideBarDrawer.cpp:72` | `drawHdSidebar()` | Вызов идёт после закрытого условия `uiaudit::isEnabled()`; условие вызывает только запись кликов. Сам HD-вызов безусловный. Вывод исходника сохранён в секции «cSideBarDrawer::draw и вызов drawHdSidebar». |
| `src/drawers/cSideBarDrawer.cpp:106–108` | `drawHdRadarPanel()`, `drawHdCapacities()`, `drawHdBuildingLists()` | Безусловные вызовы внутри `drawHdSidebar()`. Их исходник сохранён в секции «безусловные вызовы HD-подфункций боковой панели». |
| `src/drawers/cSideBarDrawer.cpp:314, 323` | `drawHdMeter()` | Оба вызова идут подряд в `drawHdCapacities()` и не разделяются условием. Точный вывод команды приведён ниже. |
| `src/drawers/cBuildingListDrawer.cpp:259` | `drawHdCard(...)` | Прямой вызов внутри цикла; перед ним есть проверки пропуска пустого и невидимого элемента, но в их ветках нет вызова другой функции рисования. Вызов и окружение сохранены в секции «вызов drawHdCard внутри полного draw-list участка». |
| `src/drawers/cBuildingListDrawer.cpp:467` | `drawHdScrollbar(...)` | Безусловный вызов после цикла и сброса clipping. Вывод сохранён в секции «безусловный вызов drawHdScrollbar после отрисовки карточек». |

Остальные совпадения полного поиска — объявления и определения функций в `.h`/`.cpp`, а не вызовы в ветвлениях. Поэтому `hd-branches.tsv` содержит только заголовок: ни одна ветка `if`, `else if` или `?:` не содержит вызова `drawHd...` как альтернативу иной функции рисования или пустой ветке.

### Точный вывод для вызовов `drawHdMeter`

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '306,336p'
```

```text
   306	void cSideBarDrawer::drawHdCapacities()
   307	{
   308	    const HudLayout layout = HudLayout::create(
   309	        game.m_screenW,
   310	        game.m_screenH
   311	    );
   312	    const int produced = std::max(0, m_player->getPowerProduced());
   313	    const int used = std::max(0, m_player->getPowerUsage());
   314	    drawHdMeter(
   315	        layout.powerMeter,
   316	        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
   317	        used,
   318	        produced,
   319	        Color{72, 202, 103, 255},
   320	        !m_player->bEnoughPower()
   321	    );
   322	
   323	    drawHdMeter(
   324	        layout.spiceMeter,
   325	        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
   326	        std::max(0, m_player->getCredits()),
   327	        std::max(1, static_cast<int>(m_player->getMaxCredits())),
   328	        Color{218, 139, 47, 255},
   329	        !m_player->bEnoughSpiceCapacityToStoreCredits()
   330	    );
   331	}
   332	
   333	void cSideBarDrawer::drawHdBuildingLists()
   334	{
   335	    m_sidebar = m_player->getSideBar();
   336	    const int selectedListId = m_sidebar->getSelectedListID();
```

## Пункт 3: покрытие команд

В `track3-evidence.md` раздел «строки с литералами .png/.bmp и вызовами loadHdUiTexture» содержит вывод поиска по всем 25 путям. Для всех девяти имён есть отдельные блоки `git ls-tree -r --name-only REV | grep -F '<имя>'` для FORK1 и PORT; для семи имён с найденными ресурсами есть `git cat-file -s FORK1:<путь>` и отдельная проверка первого содержимого через `git cat-file -p`. Первая строка LFS-пойнтера приведена для каждого из десяти найденных путей; у двух шаблонов BMP пути отсутствуют, поэтому blob для них не существует. Фильтры sardaukar сохранены отдельно для обеих ревизий и возвращают пустой вывод.

## Пункт 4: покрытие команд и формул

В `track3-evidence.md` для обеих ревизий есть:

- `git grep` результатов присваивания `m_windowWidth`, `m_windowHeight`, `m_viewportWidth` и `m_viewportHeight`, а также строки конструктора;
- `git show` исходника конструктора и `calibrate`, откуда взяты формулы ширины/высоты окна и viewport;
- полный stdout заданного поиска мест создания `cMapCamera`, включая вызов в `cGame::setupGame`; непосредственно строки с аргументами дополнительно показаны командами `git show`;
- `git grep` по проверкам областей мыши и вывод `git show` для полных тел `updateMouseCell` и `boxSelectLogic` в FORK1 и PORT.

Таким образом, фактические команды и исходный вывод к каждой строке `camera-mouse.tsv` уже присутствуют в `track3-evidence.md`; таблицы не менялись.

## 3. Картинки HUD

```tsv
имя	путь@9208dcf:строка	функция	путь в FORK1	путь в PORT	размер blob FORK1	указатель git-lfs
outcome_victory_en.png	src/cGame_logic.cpp@9208dcf:2542; вызов src/cGame_logic.cpp@9208dcf:2549	cGame::getHdOutcomeTexture(bool victory)	resources/bin/data/hd4/outcome_victory_en.png	resources/bin/data/hd4/outcome_victory_en.png	resources/bin/data/hd4/outcome_victory_en.png=132 байт	resources/bin/data/hd4/outcome_victory_en.png: version https://git-lfs.github.com/spec/v1
outcome_victory_ru.png	src/cGame_logic.cpp@9208dcf:2543; вызов src/cGame_logic.cpp@9208dcf:2549	cGame::getHdOutcomeTexture(bool victory)	resources/bin/data/hd4/outcome_victory_ru.png	resources/bin/data/hd4/outcome_victory_ru.png	resources/bin/data/hd4/outcome_victory_ru.png=132 байт	resources/bin/data/hd4/outcome_victory_ru.png: version https://git-lfs.github.com/spec/v1
outcome_defeat_en.png	src/cGame_logic.cpp@9208dcf:2546; вызов src/cGame_logic.cpp@9208dcf:2549	cGame::getHdOutcomeTexture(bool victory)	resources/bin/data/hd4/outcome_defeat_en.png	resources/bin/data/hd4/outcome_defeat_en.png	resources/bin/data/hd4/outcome_defeat_en.png=132 байт	resources/bin/data/hd4/outcome_defeat_en.png: version https://git-lfs.github.com/spec/v1
outcome_defeat_ru.png	src/cGame_logic.cpp@9208dcf:2547; вызов src/cGame_logic.cpp@9208dcf:2549	cGame::getHdOutcomeTexture(bool victory)	resources/bin/data/hd4/outcome_defeat_ru.png	resources/bin/data/hd4/outcome_defeat_ru.png	resources/bin/data/hd4/outcome_defeat_ru.png=132 байт	resources/bin/data/hd4/outcome_defeat_ru.png: version https://git-lfs.github.com/spec/v1
hud_house_atreides.png	src/drawers/cSideBarDrawer.cpp@9208dcf:32; вызов src/drawers/cSideBarDrawer.cpp@9208dcf:31	cSideBarDrawer::cSideBarDrawer(...)	resources/bin/data/hd4/hud_house_atreides.png; resources/hd/master4/ui/hud_house_atreides.png	resources/bin/data/hd4/hud_house_atreides.png	resources/bin/data/hd4/hud_house_atreides.png=131 байт; resources/hd/master4/ui/hud_house_atreides.png=131 байт	resources/bin/data/hd4/hud_house_atreides.png: version https://git-lfs.github.com/spec/v1; resources/hd/master4/ui/hud_house_atreides.png: version https://git-lfs.github.com/spec/v1
hud_house_harkonnen.png	src/drawers/cSideBarDrawer.cpp@9208dcf:37; вызов src/drawers/cSideBarDrawer.cpp@9208dcf:36	cSideBarDrawer::cSideBarDrawer(...)	resources/bin/data/hd4/hud_house_harkonnen.png; resources/hd/master4/ui/hud_house_harkonnen.png	resources/bin/data/hd4/hud_house_harkonnen.png	resources/bin/data/hd4/hud_house_harkonnen.png=131 байт; resources/hd/master4/ui/hud_house_harkonnen.png=131 байт	resources/bin/data/hd4/hud_house_harkonnen.png: version https://git-lfs.github.com/spec/v1; resources/hd/master4/ui/hud_house_harkonnen.png: version https://git-lfs.github.com/spec/v1
hud_house_ordos.png	src/drawers/cSideBarDrawer.cpp@9208dcf:42; вызов src/drawers/cSideBarDrawer.cpp@9208dcf:41	cSideBarDrawer::cSideBarDrawer(...)	resources/bin/data/hd4/hud_house_ordos.png; resources/hd/master4/ui/hud_house_ordos.png	resources/bin/data/hd4/hud_house_ordos.png	resources/bin/data/hd4/hud_house_ordos.png=131 байт; resources/hd/master4/ui/hud_house_ordos.png=131 байт	resources/bin/data/hd4/hud_house_ordos.png: version https://git-lfs.github.com/spec/v1; resources/hd/master4/ui/hud_house_ordos.png: version https://git-lfs.github.com/spec/v1
{}x{}_{:0>4}.bmp	src/cGame_logic.cpp@9208dcf:1944	cGame::saveBmpScreenToDisk()	—	—	—	—
screenshot{}.bmp	src/cGame_logic.cpp@9208dcf:1956	cGame::saveBmpScreenToDisk()	—	—	—	—
```
### Пункт 3 — строки с литералами .png/.bmp и вызовами loadHdUiTexture во всех 25 файлах

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E '"[^"]+\.(png|bmp)"|loadHdUiTexture' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp src/managers/cDrawManager.h src/map/cMapCamera.cpp src/map/cMapCamera.h src/sidebar/cBuildingList.cpp src/sidebar/cBuildingList.h src/sidebar/cBuildingListFactory.cpp src/sidebar/cBuildingListItem.cpp src/sidebar/cBuildingListItem.h src/sidebar/cBuildingListUpdater.cpp src/sidebar/cSideBar.cpp src/sidebar/cSideBar.h src/cGame_logic.cpp src/controls/cGameControlsContext.cpp src/controls/cMouse.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1944:    std::string filename = std::format("{}x{}_{:0>4}.bmp", m_screenW, m_screenH, m_screenshot);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1956:    std::string name = std::format("screenshot{}.bmp",m_screenshot);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2542:                "outcome_victory_en.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2543:                "outcome_victory_ru.png"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2546:                "outcome_defeat_en.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2547:                "outcome_defeat_ru.png"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2549:        texture = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:31:    m_houseCrests[0] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:32:        "hud_house_atreides.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:36:    m_houseCrests[1] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:37:        "hud_house_harkonnen.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:41:    m_houseCrests[2] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:42:        "hud_house_ordos.png",
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_victory_en.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_victory_en.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_victory_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_victory_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_defeat_en.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_defeat_en.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_defeat_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_defeat_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_atreides.png' || true
```

```text
resources/bin/data/hd4/hud_house_atreides.png
resources/hd/master4/ui/hud_house_atreides.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_atreides.png' || true
```

```text
resources/bin/data/hd4/hud_house_atreides.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_harkonnen.png' || true
```

```text
resources/bin/data/hd4/hud_house_harkonnen.png
resources/hd/master4/ui/hud_house_harkonnen.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_harkonnen.png' || true
```

```text
resources/bin/data/hd4/hud_house_harkonnen.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_ordos.png' || true
```

```text
resources/bin/data/hd4/hud_house_ordos.png
resources/hd/master4/ui/hud_house_ordos.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_ordos.png' || true
```

```text
resources/bin/data/hd4/hud_house_ordos.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F {}x{}_{:0>4}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F '{}x{}_{:0>4}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F {}x{}_{:0>4}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F '{}x{}_{:0>4}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F screenshot{}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'screenshot{}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F screenshot{}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'screenshot{}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — sardaukar-пути с тематикой HUD/герба FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -i -E 'sardaukar' | grep -i -E 'hud|crest|house|emblem|logo' || true
```

```text

```

Exit code: 0.

### Пункт 3 — sardaukar-пути с тематикой HUD/герба PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -i -E 'sardaukar' | grep -i -E 'hud|crest|house|emblem|logo' || true
```

```text

```

Exit code: 0.

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_en.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_victory_en.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_en.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_ru.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_victory_ru.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_ru.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_en.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_defeat_en.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_en.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_ru.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_defeat_ru.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_ru.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_atreides.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_atreides.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_atreides.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_atreides.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_atreides.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_atreides.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_harkonnen.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_harkonnen.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_harkonnen.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_harkonnen.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_harkonnen.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_harkonnen.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_ordos.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_ordos.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_ordos.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_ordos.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_ordos.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_ordos.png
```

```text
version https://git-lfs.github.com/spec/v1
```

## 4. Поле боя, камера и мышь

```tsv
ревизия	функция	строки	формула	место создания
FORK1	cMapCamera::cMapCamera(...)	src/map/cMapCamera.cpp@9208dcf:37-64	окно: ширина = screenW − SidebarWidth, высота = screenH − TopBarHeight; viewport сначала получает размеры окна, затем calibrate делит их на zoom level; src/map/cMapCamera.cpp@9208dcf:49-53, src/map/cMapCamera.cpp@9208dcf:122-123	—
FORK1	cMapCamera::calibrate()	src/map/cMapCamera.cpp@9208dcf:117-124	viewportWidth = divideByZoomLevel(windowWidth); viewportHeight = divideByZoomLevel(windowHeight); src/map/cMapCamera.cpp@9208dcf:122-123	—
FORK1	cGame::setupGame()	src/cGame_logic.cpp@9208dcf:1219	(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove)	да
FORK1	cGameControlsContext::updateMouseCell(...)	src/controls/cGameControlsContext.cpp@9208dcf:46-73	y < TopBarHeight → верхняя панель; затем command-bar isMouseOver(coords), minimap isMouseOver(), x > screenW − SidebarWidth; иначе battlefield=true и cellFromScreen(x,y); src/controls/cGameControlsContext.cpp@9208dcf:48-72	—
FORK1	cMouse::boxSelectLogic(...)	src/controls/cMouse.cpp@9208dcf:241-272	при x > screenW − SidebarWidth конец выделения ограничен screenW − SidebarWidth − 1; при y < TopBarHeight конец по y ограничен TopBarHeight; src/controls/cMouse.cpp@9208dcf:250-256	—
PORT	cMapCamera::cMapCamera(...)	src/gameobjects/map/cMapCamera.cpp@832c953:32-65	окно: ширина = settings.screenW − SidebarWidth, высота = settings.screenH − TopBarHeight; viewport сначала получает размеры окна, затем calibrate делит их на zoom level; src/gameobjects/map/cMapCamera.cpp@832c953:49-54, src/gameobjects/map/cMapCamera.cpp@832c953:143-144	—
PORT	cMapCamera::calibrate()	src/gameobjects/map/cMapCamera.cpp@832c953:138-145	viewportWidth = divideByZoomLevel(windowWidth); viewportHeight = divideByZoomLevel(windowHeight); src/gameobjects/map/cMapCamera.cpp@832c953:143-144	—
PORT	cGame::setupGame()	src/game/cGame_logic.cpp@832c953:850	(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get())	да
PORT	cGameControlsContext::updateMouseCell(...)	src/controls/cGameControlsContext.cpp@832c953:86-110	y < TopBarHeight → верхняя панель; затем minimap isMouseOver(), x > settings.screenW − SidebarWidth; иначе battlefield=true и cellFromScreen(x,y), при cell < 0 вычисляется clamped cell; src/controls/cGameControlsContext.cpp@832c953:88-108	—
PORT	cMouse::boxSelectLogic(...)	src/controls/cMouse.cpp@832c953:279-306	при x > settings.screenW − SidebarWidth конец выделения ограничен settings.screenW − SidebarWidth − 1; при y < TopBarHeight конец по y ограничен TopBarHeight; src/controls/cMouse.cpp@832c953:288-294	—
```
### Пункт 4 — присваивания размеров видимой области камеры FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cMapCamera::cMapCamera|m_window(Width|Height)[[:space:]]*=|m_viewport(Width|Height)[[:space:]]*=' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/map/cMapCamera.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:37:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:49:    m_windowWidth= game.m_screenW - widthOfSidebar;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:50:    m_windowHeight= game.m_screenH - m_heightOfTopBar;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:52:    m_viewportWidth=m_windowWidth;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:53:    m_viewportHeight=m_windowHeight;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:122:    m_viewportWidth = divideByZoomLevel(m_windowWidth);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:123:    m_viewportHeight = divideByZoomLevel(m_windowHeight);
```

Exit code: 0.

### Пункт 4 — все результаты заданного поиска мест создания cMapCamera FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'make_unique<cMapCamera>|new cMapCamera\(|cMapCamera\(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1219:    mapCamera = new cMapCamera(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:37:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:66:cMapCamera::~cMapCamera()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h:23:    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h:25:    ~cMapCamera();
```

Exit code: 0.

### Пункт 4 — проверки регионов указателя в cMouse/cGameControlsContext FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cGameControlsContext::updateMouseCell|cMouse::boxSelectLogic|SidebarWidth|TopBarHeight|getMiniMapDrawer\(\)->isMouseOver' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/cMouse.cpp src/controls/cGameControlsContext.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:46:void cGameControlsContext::updateMouseCell(const cPoint &coords)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:48:    if (coords.y < cSideBar::TopBarHeight) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:60:    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:66:    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:241:void cMouse::boxSelectLogic(int mouseCell)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:250:            if (coords.x > game.m_screenW - cSideBar::SidebarWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:251:                mouse_co_x2 = game.m_screenW - cSideBar::SidebarWidth - 1;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:255:            if (mouse_co_y2 < cSideBar::TopBarHeight) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:256:                mouse_co_y2 = cSideBar::TopBarHeight;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:353:                m_textDrawer->drawText(0, cSideBar::TopBarHeight + 1, std::format("MouseCell {}", mouseCell));
```

Exit code: 0.

### Пункт 4 — присваивания размеров видимой области камеры PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cMapCamera::cMapCamera|m_window(Width|Height)[[:space:]]*=|m_viewport(Width|Height)[[:space:]]*=' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/map/cMapCamera.cpp || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:32:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:50:    m_windowWidth= m_gameSettings->getScreenW() - widthOfSidebar;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:51:    m_windowHeight= m_gameSettings->getScreenH() - m_heightOfTopBar;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:53:    m_viewportWidth=m_windowWidth;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:54:    m_viewportHeight=m_windowHeight;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:143:    m_viewportWidth = divideByZoomLevel(m_windowWidth);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:144:    m_viewportHeight = divideByZoomLevel(m_windowHeight);
```

Exit code: 0.

### Пункт 4 — все результаты заданного поиска мест создания cMapCamera PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'make_unique<cMapCamera>|new cMapCamera\(|cMapCamera\(' 832c953a94a632d57872349013f7ed1a37434715 -- src || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp:850:    m_mapCamera = std::make_unique<cMapCamera>(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get());
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:32:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:67:cMapCamera::~cMapCamera()
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.h:44:    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.h:46:    ~cMapCamera();
```

Exit code: 0.

### Пункт 4 — проверки регионов указателя в cMouse/cGameControlsContext PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cGameControlsContext::updateMouseCell|cMouse::boxSelectLogic|SidebarWidth|TopBarHeight|getMiniMapDrawer\(\)->isMouseOver' 832c953a94a632d57872349013f7ed1a37434715 -- src/controls/cMouse.cpp src/controls/cGameControlsContext.cpp || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:86:void cGameControlsContext::updateMouseCell(const cPoint &coords)
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:88:    if (coords.y < cSideBar::TopBarHeight) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:94:    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:100:    if (coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth)) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:279:void cMouse::boxSelectLogic(int mouseCell)
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:288:            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:289:                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:293:            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:294:                m_mouseCoY2 = cSideBar::TopBarHeight;
```

Exit code: 0.

### Пункт 4 — код конструктора камеры 9208dcf

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | nl -ba | sed -n '37,64p'
```

```text
    37	cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
    38	    m_moveSpeedDrag(moveSpeedDrag),
    39	    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    40	    m_cameraEdgeMove(cameraEdgeMove),
    41	    m_pMap(theMap)
    42	{
    43	    m_viewportStartX = m_viewportStartY = 32;
    44	    m_zoomLevel = game.getWorldScaleFactor();
    45	
    46	    int widthOfSidebar = cSideBar::SidebarWidth;
    47	    m_heightOfTopBar = cSideBar::TopBarHeight;
    48	
    49	    m_windowWidth= game.m_screenW - widthOfSidebar;
    50	    m_windowHeight= game.m_screenH - m_heightOfTopBar;
    51	
    52	    m_viewportWidth=m_windowWidth;
    53	    m_viewportHeight=m_windowHeight;
    54	
    55	    m_moveX = 0.0f;
    56	    m_moveY = 0.0f;
    57	
    58	    m_keyPressedDown = false;
    59	    m_keyPressedUp = false;
    60	    m_keyPressedLeft = false;
    61	    m_keyPressedRight = false;
    62	
    63	    calibrate();
    64	}
```

Exit code: 0.

### Пункт 4 — код calibrate камеры 9208dcf

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | nl -ba | sed -n '117,124p'
```

```text
   117	void cMapCamera::calibrate()
   118	{
   119	    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
   120	    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
   121	
   122	    m_viewportWidth = divideByZoomLevel(m_windowWidth);
   123	    m_viewportHeight = divideByZoomLevel(m_windowHeight);
   124	}
```

Exit code: 0.

### Пункт 4 — код конструктора камеры 832c953

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '32,65p'
```

```text
    32	cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
    33	    m_moveSpeedDrag(moveSpeedDrag),
    34	    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    35	    m_cameraEdgeMove(cameraEdgeMove),
    36	    m_pMap(theMap),
    37	    m_mapGeometry(theMap->getGeometry()),
    38	    m_gameSettings(gameSettings),
    39	    m_mouse(mouse)
    40	{
    41	    d2tm_assert(theMap != nullptr);
    42	    d2tm_assert(gameSettings != nullptr);
    43	    d2tm_assert(mouse != nullptr);
    44	    m_viewportStartX = m_viewportStartY = 32;
    45	    m_zoomLevel = std::clamp(m_gameSettings->getWorldScaleFactor(), 0.25f, 4.0f);
    46	
    47	    int widthOfSidebar = cSideBar::SidebarWidth;
    48	    m_heightOfTopBar = cSideBar::TopBarHeight;
    49	
    50	    m_windowWidth= m_gameSettings->getScreenW() - widthOfSidebar;
    51	    m_windowHeight= m_gameSettings->getScreenH() - m_heightOfTopBar;
    52	
    53	    m_viewportWidth=m_windowWidth;
    54	    m_viewportHeight=m_windowHeight;
    55	
    56	    m_moveX = 0.0f;
    57	    m_moveY = 0.0f;
    58	
    59	    m_keyPressedDown = false;
    60	    m_keyPressedUp = false;
    61	    m_keyPressedLeft = false;
    62	    m_keyPressedRight = false;
    63	
    64	    calibrate();
    65	}
```

Exit code: 0.

### Пункт 4 — код calibrate камеры 832c953

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '138,145p'
```

```text
   138	void cMapCamera::calibrate()
   139	{
   140	    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
   141	    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
   142	
   143	    m_viewportWidth = divideByZoomLevel(m_windowWidth);
   144	    m_viewportHeight = divideByZoomLevel(m_windowHeight);
   145	}
```

Exit code: 0.

### Пункт 4 — cGame::setupGame и создание камеры FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '1000,1012p;1216,1222p'
```

```text
  1000	/**
  1001		Setup the game
  1002	
  1003		Should not be called twice.
  1004	*/
  1005	bool cGame::setupGame()
  1006	{
  1007	    cLogger *logger = cLogger::getInstance();
  1008	    logger->setDebugMode(m_debugMode);
  1009	    logger->logHeader("Dune II - The Maker");
  1010	    logger->logCommentLine(""); // whitespace
  1011	
  1012	    logger->logHeader("Version information");
  1216	    IniGameRessources::install_terrain(m_TerrainInfo);
  1217	
  1218	    delete mapCamera;
  1219	    mapCamera = new cMapCamera(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove);
  1220	
  1221	    cIni::installGame(m_gameFilename);
  1222	    // Now we are ready for the menu state
```

Exit code: 0.

### Пункт 4 — cGame::setupGame и создание камеры PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp | nl -ba | sed -n '696,704p;846,854p'
```

```text
   696	/**
   697		Setup the game
   698	
   699		Should not be called twice.
   700	*/
   701	bool cGame::setupGame()
   702	{
   703	    Logger::g_loggerInstance->setDebug(m_gameSettings->m_debugMode);
   704	
   846	    infoCreator.installInfos(*m_infoContext);
   847	
   848	    m_mapCamera.reset();
   849	
   850	    m_mapCamera = std::make_unique<cMapCamera>(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get());
   851	    m_services->mapCamera = m_mapCamera.get();
   852	    m_structureUtils->serviceInit(m_services.get());
   853	
   854	    m_cIni->installGame(m_gameFilename);
```

Exit code: 0.

### Пункт 4 — updateMouseCell FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '46,73p'
```

```text
    46	void cGameControlsContext::updateMouseCell(const cPoint &coords)
    47	{
    48	    if (coords.y < cSideBar::TopBarHeight) {
    49	        m_mouseCell = MOUSECELL_TOPBAR; // at the top bar or higher, so no mouse cell id.
    50	        m_mouseOnBattleField = false;
    51	        return;
    52	    }
    53	
    54	    if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
    55	        m_mouseCell = MOUSECELL_COMMAND_BAR;
    56	        m_mouseOnBattleField = false;
    57	        return;
    58	    }
    59	
    60	    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
    61	        m_mouseCell = MOUSECELL_MINIMAP; // on minimap
    62	        m_mouseOnBattleField = false;
    63	        return;
    64	    }
    65	
    66	    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
    67	        m_mouseCell = MOUSECELL_SIDEBAR; // on sidebar
    68	        m_mouseOnBattleField = false;
    69	        return;
    70	    }
    71	    m_mouseOnBattleField = true;
    72	    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
    73	}
```

Exit code: 0.

### Пункт 4 — updateMouseCell PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '86,110p'
```

```text
    86	void cGameControlsContext::updateMouseCell(const cPoint &coords)
    87	{
    88	    if (coords.y < cSideBar::TopBarHeight) {
    89	        m_mouseCell = MOUSE_CELL_HOVER_TOPBAR; // at the top bar or higher, so no mouse cell id.
    90	        m_mouseOnBattleField = false;
    91	        return;
    92	    }
    93	
    94	    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
    95	        m_mouseCell = MOUSE_CELL_HOVER_MINIMAP; // on minimap
    96	        m_mouseOnBattleField = false;
    97	        return;
    98	    }
    99	
   100	    if (coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth)) {
   101	        m_mouseCell = MOUSE_CELL_HOVER_SIDEBAR; // on sidebar
   102	        m_mouseOnBattleField = false;
   103	        return;
   104	    }
   105	    m_mouseOnBattleField = true;
   106	    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
   107	    if (m_mouseCell < 0) { // clamp mouse cell to map
   108	        m_mouseCellClamped = getMouseCellFromScreenClamped(coords.x, coords.y);
   109	    }
   110	}
```

Exit code: 0.

### Пункт 4 — boxSelectLogic FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp | nl -ba | sed -n '241,272p'
```

```text
   241	void cMouse::boxSelectLogic(int mouseCell)
   242	{
   243	// When the mouse is pressed, we will check if the first coordinates are filled in
   244	    // if so, we will update the second coordinates. If the player holds his mouse we
   245	    // keep updating the second coordinates and create a rectangle to select units with.
   246	    if (mouse_co_x1 > -1 && mouse_co_y1 > -1) {
   247	        if (abs(coords.x - mouse_co_x1) > 4 && abs(coords.y - mouse_co_y1) > 4) {
   248	            // assign 2nd coordinates
   249	            mouse_co_x2 = coords.x;
   250	            if (coords.x > game.m_screenW - cSideBar::SidebarWidth) {
   251	                mouse_co_x2 = game.m_screenW - cSideBar::SidebarWidth - 1;
   252	            }
   253	
   254	            mouse_co_y2 = coords.y;
   255	            if (mouse_co_y2 < cSideBar::TopBarHeight) {
   256	                mouse_co_y2 = cSideBar::TopBarHeight;
   257	            }
   258	
   259	            // and draw the selection box
   260	            //_rect(bmp_screen, mouse_co_x1, mouse_co_y1, mouse_co_x2, mouse_co_y2, game.getColorFadeSelected(255, 255, 255));
   261	            renderDrawer->renderRectColor(mouse_co_x1, mouse_co_y1, mouse_co_x2-mouse_co_x1, mouse_co_y2-mouse_co_y1, game.getColorFadeSelected(255, 255, 255));
   262	        }
   263	
   264	        // Note that we have to fix up the coordinates when checking 'within border'
   265	        // for units (when X2 < X1 for example!)
   266	    }
   267	    else if (mouseCell > -1) {
   268	        // no first coordinates set, so do that here.
   269	        mouse_co_x1 = coords.x;
   270	        mouse_co_y1 = coords.y;
   271	    }
   272	}
```

Exit code: 0.

### Пункт 4 — boxSelectLogic PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp | nl -ba | sed -n '279,306p'
```

```text
   279	void cMouse::boxSelectLogic(int mouseCell)
   280	{
   281	// When the mouse is pressed, we will check if the first coordinates are filled in
   282	    // if so, we will update the second coordinates. If the player holds his mouse we
   283	    // keep updating the second coordinates and create a rectangle to select units with.
   284	    if (m_mouseCoX1 > -1 && m_mouseCoY1 > -1) {
   285	        if (abs(m_coords.x - m_mouseCoX1) > 4 && abs(m_coords.y - m_mouseCoY1) > 4) {
   286	            // assign 2nd coordinates
   287	            m_mouseCoX2 = m_coords.x;
   288	            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
   289	                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
   290	            }
   291	
   292	            m_mouseCoY2 = m_coords.y;
   293	            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
   294	                m_mouseCoY2 = cSideBar::TopBarHeight;
   295	            }
   296	        }
   297	
   298	        // Note that we have to fix up the coordinates when checking 'within border'
   299	        // for units (when X2 < X1 for example!)
   300	    }
   301	    else if (mouseCell > -1) {
   302	        // no first coordinates set, so do that here.
   303	        m_mouseCoX1 = m_coords.x;
   304	        m_mouseCoY1 = m_coords.y;
   305	    }
   306	}
```

Exit code: 0.

## Итоги


- Пункт 2: `drawHd-branches.tsv` содержит заголовок без строк. Во всех заданных полных файлах `drawHd`-вызовы не стоят в ветви `if`, `else if` или `?:`, где противоположная ветвь вызывает другую функцию рисования или ничего не рисует. `drawHdSidebar`, `drawHdCard` и `drawHdScrollbar` вызываются без такого переключающего условия.

- Пункт 3: в 25 перечисленных файлах найдены семь изображений HUD, передаваемых в `loadHdUiTexture`, и два строковых шаблона с суффиксом `.bmp` для скриншотов. Для каждого имени сохранены результаты `ls-tree` по обеим ревизиям; для существующих путей в FORK1 сохранены размеры `cat-file -s` и проверка признака LFS.

- Пункт 4: `updateMouseCell` классифицирует верхнюю панель, мини-карту, боковую панель и поле боя; `boxSelectLogic` ограничивает прямоугольник выделения границами поля. В каждой ревизии записаны конструктор и `calibrate`, фактический вызов создания камеры и обе функции мыши.

- По фильтру sardaukar: FORK1 — 0 путей; PORT — 0 путей.

## Итог выборочной сверки помощника 4

# Выборочная сверка

## Помощник 1 — `fork-hunks-1.tsv`

### 1. `src/drawers/CreditsDrawer.cpp@9208dcf:37-43`
Факт из таблицы: ширина полосы вычисляется по логическому размеру текстуры для HD-плотности.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp | sed -n '37,43p'
```

Вывод:
```text
    previousCredits = 0;

    // center credits bar within sidebar
    int widthCreditsBar = m_gfxinter->getLogicalWidth(CREDITS_BAR);
    drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
    drawY = 0;
}
```

Вердикт: совпало

### 2. `src/drawers/cBuildingListDrawer.cpp@9208dcf:97-104`
Факт из таблицы: размер рамки наведения берётся из геометрии кнопки списка.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '97,104p'
```

Вывод:
```text
    int y = list->getButtonDrawY();
    int id = list->getButtonIconIdUnpressed();

    int width = list->getButtonWidth();
    int height = list->getButtonHeight();

    Color color = m_player->getSelectFadingColor();
```

Вердикт: совпало

### 3. `src/drawers/cBuildingListDrawer.cpp@9208dcf:220-237`
Факт из таблицы: рисование списка ограничено областью карточек, размеры и вертикальная раскладка взяты из HudLayout.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '220,237p'
```

Вывод:
```text
    std::array<int, 6> isBuildingItemInList = list->isBuildingItem();

    // Start drawing the 'icons grid'
    int withOfIcon = getCardWidth();
    int heightOfIcon = getCardHeight();

    renderDrawer->setClippingFor(
        layout.cards.getX(),
        layout.cards.getY(),
        layout.cards.getEndX(),
        layout.cards.getEndY()
    );

    // Draw the visible icon rows. HD positions come from HudLayout so drawing
    // and hit testing cannot drift apart.
    for (int i = 0; i < end; i++) {
        cBuildingListItem *item = list->getItem(i);
```

Вердикт: совпало

### 4. `src/drawers/cBuildingListDrawer.cpp@9208dcf:354-360`
Факт из таблицы: надпись о занятом строительстве локализована.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '354,360p'
```

Вывод:
```text
                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);

                    Color red = Color{255, 0, 0,255};
                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
                }

                // Pending building (ie: a build is progressing, blocking the upgrade)
```

Вердикт: не совпало

## Помощник 2 — `fork-hunks-2.tsv`

### 1. `src/managers/cDrawManager.cpp@9208dcf:2-8`
Факт из таблицы: подключены средства аудита интерфейса.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '2,8p'
```

Вывод:
```text

#include "controls/cGameControlsContext.h"
#include "d2tmc.h"
#include "debug/UiAudit.hpp"
#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
```

Вердикт: совпало

### 2. `src/managers/cDrawManager.cpp@9208dcf:77-82`
Факт из таблицы: вызов старой панели параметров удалён из отрисовки боевого состояния.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '77,82p'
```

Вывод:
```text
    // GUI
    drawSidebar();

    renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
    drawStructurePlacing();
    renderDrawer->resetClippingFor();
```

Вердикт: не совпало

### 3. `src/managers/cDrawManager.cpp@9208dcf:86-97`
Факт из таблицы: добавлены музыкальные элементы верхней строки и командная строка, удалена старая отрисовка полосы параметров.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '86,97p'
```

Вывод:
```text

    // THE MESSAGE
    drawMessage();
    drawTopBarMusicControls();

    drawNotifications();

    m_commandBarDrawer.draw();

    renderDrawer->resetClippingFor();

    if (game.m_drawUsages) {
```

Вердикт: совпало

### 4. `src/managers/cDrawManager.cpp@9208dcf:456-462`
Факт из таблицы: события мыши передаются командной строке.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '456,462p'
```

Вывод:
```text
void cDrawManager::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_sidebarDrawer.onNotifyMouseEvent(event);
    m_commandBarDrawer.onNotifyMouseEvent(event);
}

void cDrawManager::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

Вердикт: совпало

## Помощник 3 — `hud-images.tsv` и `camera-mouse.tsv`

### 1. `src/cGame_logic.cpp@9208dcf:2542` (`hud-images.tsv`)
Факт из таблицы: в `getHdOutcomeTexture` используется имя `outcome_victory_en.png`.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2542p'
```

Вывод:
```text
                "outcome_victory_en.png",
```

Вердикт: совпало

### 2. `src/cGame_logic.cpp@9208dcf:2543` (`hud-images.tsv`)
Факт из таблицы: в `getHdOutcomeTexture` используется имя `outcome_victory_ru.png`.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2543p'
```

Вывод:
```text
                "outcome_victory_ru.png"
```

Вердикт: совпало

### 3. `src/map/cMapCamera.cpp@9208dcf:37-64` (`camera-mouse.tsv`)
Факт из таблицы: окно камеры получает размеры экрана за вычетом боковой и верхней панелей; viewport получает размеры окна, после чего вызывается калибровка масштаба.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '37,64p'
```

Вывод:
```text
cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
    m_moveSpeedDrag(moveSpeedDrag),
    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    m_cameraEdgeMove(cameraEdgeMove),
    m_pMap(theMap)
{
    m_viewportStartX = m_viewportStartY = 32;
    m_zoomLevel = game.getWorldScaleFactor();

    int widthOfSidebar = cSideBar::SidebarWidth;
    m_heightOfTopBar = cSideBar::TopBarHeight;

    m_windowWidth= game.m_screenW - widthOfSidebar;
    m_windowHeight= game.m_screenH - m_heightOfTopBar;

    m_viewportWidth=m_windowWidth;
    m_viewportHeight=m_windowHeight;

    m_moveX = 0.0f;
    m_moveY = 0.0f;

    m_keyPressedDown = false;
    m_keyPressedUp = false;
    m_keyPressedLeft = false;
    m_keyPressedRight = false;

    calibrate();
}
```

Вердикт: совпало

### 4. `src/controls/cGameControlsContext.cpp@9208dcf:46-73` (`camera-mouse.tsv`)
Факт из таблицы: координаты мыши классифицируются как верхняя панель, командная строка, миникарта или боковая панель; иначе выбирается клетка поля боя.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | sed -n '46,73p'
```

Вывод:
```text
void cGameControlsContext::updateMouseCell(const cPoint &coords)
{
    if (coords.y < cSideBar::TopBarHeight) {
        m_mouseCell = MOUSECELL_TOPBAR; // at the top bar or higher, so no mouse cell id.
        m_mouseOnBattleField = false;
        return;
    }

    if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
        m_mouseCell = MOUSECELL_COMMAND_BAR;
        m_mouseOnBattleField = false;
        return;
    }

    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
        m_mouseCell = MOUSECELL_MINIMAP; // on minimap
        m_mouseOnBattleField = false;
        return;
    }

    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
        m_mouseCell = MOUSECELL_SIDEBAR;
        m_mouseOnBattleField = false;
        return;
    }
    m_mouseOnBattleField = true;
    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
}
```

Вердикт: совпало

Итог по 12 строкам spotcheck: 10 вердиктов «совпало» и 2 вердикта «не совпало», что подтверждено командами `rg -c`.

После выборки дорожка 1 уточнила описание строки `src/drawers/cBuildingListDrawer.cpp@9208dcf:354-360`: участок заменяет `Upgrading` вызовом `localization::text("Upgrade", "Улучшение")`. Новая формулировка и вывод кода сохранены в `track1-evidence.md`; выборочный файл сохраняет первоначальный вердикт. Для строки `src/managers/cDrawManager.cpp@9208dcf:77-82` вывод `git diff BASE FORK1` подтверждает удалённую строку `drawOptionBar()`, а `spotcheck.md` сохраняет результат команды, показавшей только новую сторону участка.

## Чтение

Полностью отдельным вызовом прочитан `/srv/dune/tasks/load-check/PORT_PLAN.md`, включая раздел 4 (строку П5), «Содержание шагов», описания П5, П5в, П5г, П7, П8, П9 и П10. Дополнительных правил, норм или контрактов, нужных для выполнения пунктов 1–4, в задании и прочитанном плане не обнаружено: нужные ревизии, пути, фильтры, словарь шагов и форматы вывода заданы прямо в задании.

## Решено исполнителем

Имя ключа сводного подсчёта → имя заголовка TSV `путь в FORK1`; файл `.tmp/p5cr2/summarize_tables.py:9`, `row["путь"]` → `row["путь в FORK1"]`; основание — заголовок таблиц и первый вывод `KeyError: 'путь'`.

## Не проверено

Сборки, CTest и запуск игры не выполнялись, поскольку они запрещены заданием.
