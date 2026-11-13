# Пункт 4. Дома и данные кампании

### Количество совпадений `sardaukar` в PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git grep -n -i -w 'sardaukar' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | wc -l
```

Вывод:

```text
94
```

### Совпадения `sardaukar` в PORT (первые 80)

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git grep -n -i -w 'sardaukar' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src | head -80
```

Вывод:

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/AudioContext.cpp:144:        else if (humanHouse == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/AudioContext.cpp:145:            sampleId = MIDI_MENTAT_HAR; // no @SARDAUKAR srd music, so use harkonnen one
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/MusicJukeBox.cpp:51:        case SARDAUKAR: return "briefing/sardaukar";
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/MusicJukeBox.cpp:80:                            "briefing/atreides", "briefing/harkonnen", "briefing/ordos", "briefing/sardaukar"}) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/MusicJukeBox.hpp:26:// BRIEFING has one per house: briefing/atreides, briefing/harkonnen, briefing/ordos and briefing/sardaukar.
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:889:    specialInfos[SPECIAL_DEATHHAND].house = Harkonnen | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1161:    upgradeInfos[UPGRADE_TYPE_CONSTYARD_SLAB4].house = Atreides | Harkonnen | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1176:    upgradeInfos[UPGRADE_TYPE_CONSTYARD_RTURRET].house = Atreides | Harkonnen | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1192:    upgradeInfos[UPGRADE_TYPE_LIGHTFCTRY_QUAD].house = Atreides | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1210:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_MVC].house = Atreides | Ordos | Harkonnen | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1226:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_LAUNCHER].house = Atreides | Harkonnen | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1241:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_SIEGETANK].house = Atreides | Harkonnen | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1272:    upgradeInfos[UPGRADE_TYPE_HITECH_ORNI].house = Atreides | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1287:    upgradeInfos[UPGRADE_TYPE_WOR_TROOPERS].house = Harkonnen | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1304:    upgradeInfos[UPGRADE_TYPE_BARRACKS_INFANTRY].house = Atreides | Ordos | Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1319:    // HEAVY FACTORY: Sardaukar - Allow building Sonic Tank
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1321:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_SAR_SONICTANK].house = Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1338:    // HEAVY FACTORY: Sardaukar - Allow building Deviator
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1340:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVIATOR].house = Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1357:    // HEAVY FACTORY: Sardaukar - Allow building Devastator
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/cInfoContextCreator.cpp:1359:    upgradeInfos[UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVASTATOR].house = Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp:153:    if (m_player->isHouse(SARDAUKAR)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp:170:    if (m_player->isHouse(SARDAUKAR)) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cSideBarDrawer.cpp:171:        return "SARDAUKAR";
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:29:constexpr std::array<const char*, HOUSE_COUNT> HOUSE_SECTIONS = {"Atreides", "Harkonnen", "Ordos", "Sardaukar"};
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:168:    return house == ATREIDES || house == HARKONNEN || house == ORDOS || house == SARDAUKAR;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:207:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:393:    if (player->getHouse() == HARKONNEN || player->getHouse() == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:466:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:613:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:788:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:997:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1206:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1279:            else if (player->getHouse() == HARKONNEN || player->getHouse() == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1469:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1568:        if (player->getHouse() != HARKONNEN && player->getHouse() != SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cHousesInfo.cpp:29:        {SARDAUKAR,    "HOUSE: SARDAUKAR"},
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cHousesInfo.cpp:62:    // Sardaukar
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cHousesInfo.cpp:63:    m_houseInfo[SARDAUKAR].minimap_color = Color(255,0,255);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cHousesInfo.cpp:64:    m_houseInfo[SARDAUKAR].colors = {{{242, 105, 242}, {206, 72, 206}, {170, 48, 170},
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:338:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:743:    if (house == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:747:    // TODO other m_houseInfo (Sardaukar, etc)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:787:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:788:            return eHouseBitFlag::Sardaukar;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:833:    else if (house == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:834:        return "Sardaukar";
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:1803:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:1823:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:1842:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.cpp:1861:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayerDifficultySettings.cpp:95:        case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayerDifficultySettings.cpp:98:                       1.25f, // Sardaukar builds even slower than Harkonnen
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cOrderProcesser.cpp:119:        else if (m_player->getHouse() == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cOrderProcesser.cpp:120:            soundIdToPlay = SOUND_VOICE_06_ATR;    // no @SARDAUKAR srd voice yet, matches the atreides fallback used for voice lines elsewhere
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cOrderProcesser.cpp:136:        else if (m_player->getHouse() == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/structures/cOrderProcesser.cpp:137:            soundIdToPlay = (SOUND_ATR_S1 + (seconds - 1));    // no @SARDAUKAR srd voice yet, matches the atreides fallback used for voice lines elsewhere
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.cpp:126:    drawHdHouseCard(houseSardaukar, bmp_HouseSardaukar, "SARDAUKAR");
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.cpp:258:        m_mentatFlow->prepareToTellAboutHouse(SARDAUKAR);
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:89:            else if (house == SARDAUKAR)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:105:            else if (house == SARDAUKAR)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp:123:            else if (house == SARDAUKAR)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.cpp:64:    } else if (house == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:874:                std::vector<int> available = {HARKONNEN, ATREIDES, ORDOS, SARDAUKAR};
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:890:                    available = {HARKONNEN, ATREIDES, ORDOS, SARDAUKAR};
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1141:                    sSkirmishPlayer.iHouse = SARDAUKAR;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:1231:                if (sSkirmishPlayer.iHouse > SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:82:    } else if (house == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cTellHouseState.cpp:84:        m_cIni->loadBriefing(SARDAUKAR, 0, eScenarioIniSection::DESCRIPTION, m_mentat.get());
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:75:inline constexpr int AI_CPU4 = 4; // 4 = CPU (Sardaukar)	== ALLIES WITH EVERYBODY (EXCEPT PLAYER)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:104:inline constexpr int SARDAUKAR = 4;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:107:inline constexpr int CORRINO = 7; // == SARDAUKAR!!!   ---- in this code we use this 'house' for sandworms
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:153:// Heavy Factory: Sardaukar only
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:154:inline constexpr int UPGRADE_TYPE_HEAVYFCTRY_SAR_SONICTANK = 10; // upgrade for Sardaukar to get Sonic Tank
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:155:inline constexpr int UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVIATOR = 11; // upgrade for Sardaukar to get Deviator
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:156:inline constexpr int UPGRADE_TYPE_HEAVYFCTRY_SAR_DEVASTATOR = 12; // upgrade for Sardaukar to get Devastator
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/enums/HouseFlags.h:15:    Sardaukar = 0x08,
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingListUpdater.cpp:179:        else if (house == SARDAUKAR) {
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingListUpdater.cpp:230:            case SARDAUKAR:
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/sidebar/cBuildingListUpdater.cpp:290:			if (house == SARDAUKAR) {
```

### Объявления/упоминания констант домов в PORT (первые 30)

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git grep -n -E '\b(ATREIDES|HARKONNEN|ORDOS|SARDAUKAR|FREMEN|MERCENARY)\b *=|\b(ATREIDES|HARKONNEN|ORDOS|SARDAUKAR|FREMEN|MERCENARY)\b *,' acddd297b21ec200c7090dd2f1b73e014e2b74c0 -- src/include src/game | head -30
```

Вывод:

```text
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:101:inline constexpr int HARKONNEN = 1;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:102:inline constexpr int ATREIDES = 2;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:103:inline constexpr int ORDOS = 3;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:104:inline constexpr int SARDAUKAR = 4;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:105:inline constexpr int FREMEN = 5;
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h:106:inline constexpr int MERCENARY = 6;
```

### Пути вне `src/` в PORT (первые 120)

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git ls-tree -r --name-only acddd297b21ec200c7090dd2f1b73e014e2b74c0 | grep -i -E 'campaign|mission|region|mentat' | grep -v '^src/' | head -120
```

Вывод:

```text
docs/upstream/p2/hd4_alignment_sdl_mentat_hd4.tsv
resources/bin/campaign/atreides/mission1.ini
resources/bin/campaign/atreides/mission2.ini
resources/bin/campaign/atreides/mission3.ini
resources/bin/campaign/atreides/mission4.ini
resources/bin/campaign/atreides/mission5.ini
resources/bin/campaign/atreides/mission6.ini
resources/bin/campaign/atreides/mission7.ini
resources/bin/campaign/atreides/mission8.ini
resources/bin/campaign/briefings/mentata.ini
resources/bin/campaign/briefings/mentath.ini
resources/bin/campaign/briefings/mentato.ini
resources/bin/campaign/briefings/mentats.ini
resources/bin/campaign/harkonnen/mission1.ini
resources/bin/campaign/harkonnen/mission2.ini
resources/bin/campaign/harkonnen/mission3.ini
resources/bin/campaign/harkonnen/mission4.ini
resources/bin/campaign/harkonnen/mission5.ini
resources/bin/campaign/harkonnen/mission6.ini
resources/bin/campaign/harkonnen/mission7.ini
resources/bin/campaign/harkonnen/mission8.ini
resources/bin/campaign/info.txt
resources/bin/campaign/maps/dune2.ini
resources/bin/campaign/maps/scena001.ini
resources/bin/campaign/maps/scena002.ini
resources/bin/campaign/maps/scena003.ini
resources/bin/campaign/maps/scena004.ini
resources/bin/campaign/maps/scena005.ini
resources/bin/campaign/maps/scena006.ini
resources/bin/campaign/maps/scena007.ini
resources/bin/campaign/maps/scena008.ini
resources/bin/campaign/maps/scena009.ini
resources/bin/campaign/maps/scena010.ini
resources/bin/campaign/maps/scena011.ini
resources/bin/campaign/maps/scena012.ini
resources/bin/campaign/maps/scena013.ini
resources/bin/campaign/maps/scena014.ini
resources/bin/campaign/maps/scena015.ini
resources/bin/campaign/maps/scena016.ini
resources/bin/campaign/maps/scena017.ini
resources/bin/campaign/maps/scena018.ini
resources/bin/campaign/maps/scena019.ini
resources/bin/campaign/maps/scena020.ini
resources/bin/campaign/maps/scena021.ini
resources/bin/campaign/maps/scena022.ini
resources/bin/campaign/maps/scenf022.ini
resources/bin/campaign/maps/scenh001.ini
resources/bin/campaign/maps/scenh002.ini
resources/bin/campaign/maps/scenh003.ini
resources/bin/campaign/maps/scenh004.ini
resources/bin/campaign/maps/scenh005.ini
resources/bin/campaign/maps/scenh006.ini
resources/bin/campaign/maps/scenh007.ini
resources/bin/campaign/maps/scenh008.ini
resources/bin/campaign/maps/scenh009.ini
resources/bin/campaign/maps/scenh010.ini
resources/bin/campaign/maps/scenh011.ini
resources/bin/campaign/maps/scenh012.ini
resources/bin/campaign/maps/scenh013.ini
resources/bin/campaign/maps/scenh014.ini
resources/bin/campaign/maps/scenh015.ini
resources/bin/campaign/maps/scenh016.ini
resources/bin/campaign/maps/scenh017.ini
resources/bin/campaign/maps/scenh018.ini
resources/bin/campaign/maps/scenh019.ini
resources/bin/campaign/maps/scenh020.ini
resources/bin/campaign/maps/scenh021.ini
resources/bin/campaign/maps/scenh022.ini
resources/bin/campaign/maps/sceno001.ini
resources/bin/campaign/maps/sceno002.ini
resources/bin/campaign/maps/sceno003.ini
resources/bin/campaign/maps/sceno004.ini
resources/bin/campaign/maps/sceno005.ini
resources/bin/campaign/maps/sceno006.ini
resources/bin/campaign/maps/sceno007.ini
resources/bin/campaign/maps/sceno008.ini
resources/bin/campaign/maps/sceno009.ini
resources/bin/campaign/maps/sceno010.ini
resources/bin/campaign/maps/sceno011.ini
resources/bin/campaign/maps/sceno012.ini
resources/bin/campaign/maps/sceno013.ini
resources/bin/campaign/maps/sceno014.ini
resources/bin/campaign/maps/sceno015.ini
resources/bin/campaign/maps/sceno016.ini
resources/bin/campaign/maps/sceno017.ini
resources/bin/campaign/maps/sceno018.ini
resources/bin/campaign/maps/sceno019.ini
resources/bin/campaign/maps/sceno020.ini
resources/bin/campaign/maps/sceno021.ini
resources/bin/campaign/maps/sceno022.ini
resources/bin/campaign/maps/scens001.ini
resources/bin/campaign/maps/scens002.ini
resources/bin/campaign/maps/scens003.ini
resources/bin/campaign/maps/scens004.ini
resources/bin/campaign/maps/scens005.ini
resources/bin/campaign/maps/scens006.ini
resources/bin/campaign/maps/scens007.ini
resources/bin/campaign/maps/scens008.ini
resources/bin/campaign/maps/scens009.ini
resources/bin/campaign/maps/scens010.ini
resources/bin/campaign/maps/scens011.ini
resources/bin/campaign/maps/scens012.ini
resources/bin/campaign/maps/scens013.ini
resources/bin/campaign/maps/scens014.ini
resources/bin/campaign/maps/scens015.ini
resources/bin/campaign/maps/scens016.ini
resources/bin/campaign/maps/scens017.ini
resources/bin/campaign/maps/scens018.ini
resources/bin/campaign/maps/scens019.ini
resources/bin/campaign/maps/scens020.ini
resources/bin/campaign/maps/scens021.ini
resources/bin/campaign/maps/scens022.ini
resources/bin/campaign/maps/timenn.ini
resources/bin/campaign/ordos/mission1.ini
resources/bin/campaign/ordos/mission2.ini
resources/bin/campaign/ordos/mission3.ini
resources/bin/campaign/ordos/mission4.ini
resources/bin/campaign/ordos/mission5.ini
resources/bin/campaign/ordos/mission6.ini
resources/bin/campaign/ordos/mission7.ini
```

### Пути вне `src/` в FORK1 (первые 120)

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -i -E 'campaign|mission|region|mentat' | grep -v '^src/' | head -120
```

Вывод:

```text
resources/bin/campaign/atreides/mission1.ini
resources/bin/campaign/atreides/mission2.ini
resources/bin/campaign/atreides/mission3.ini
resources/bin/campaign/atreides/mission4.ini
resources/bin/campaign/atreides/mission5.ini
resources/bin/campaign/atreides/mission6.ini
resources/bin/campaign/atreides/mission7.ini
resources/bin/campaign/atreides/mission8.ini
resources/bin/campaign/briefings/mentata.ini
resources/bin/campaign/briefings/mentath.ini
resources/bin/campaign/briefings/mentato.ini
resources/bin/campaign/harkonnen/mission1.ini
resources/bin/campaign/harkonnen/mission2.ini
resources/bin/campaign/harkonnen/mission3.ini
resources/bin/campaign/harkonnen/mission4.ini
resources/bin/campaign/harkonnen/mission5.ini
resources/bin/campaign/harkonnen/mission6.ini
resources/bin/campaign/harkonnen/mission7.ini
resources/bin/campaign/harkonnen/mission8.ini
resources/bin/campaign/info.txt
resources/bin/campaign/maps/dune2.ini
resources/bin/campaign/maps/scena001.ini
resources/bin/campaign/maps/scena002.ini
resources/bin/campaign/maps/scena003.ini
resources/bin/campaign/maps/scena004.ini
resources/bin/campaign/maps/scena005.ini
resources/bin/campaign/maps/scena006.ini
resources/bin/campaign/maps/scena007.ini
resources/bin/campaign/maps/scena008.ini
resources/bin/campaign/maps/scena009.ini
resources/bin/campaign/maps/scena010.ini
resources/bin/campaign/maps/scena011.ini
resources/bin/campaign/maps/scena012.ini
resources/bin/campaign/maps/scena013.ini
resources/bin/campaign/maps/scena014.ini
resources/bin/campaign/maps/scena015.ini
resources/bin/campaign/maps/scena016.ini
resources/bin/campaign/maps/scena017.ini
resources/bin/campaign/maps/scena018.ini
resources/bin/campaign/maps/scena019.ini
resources/bin/campaign/maps/scena020.ini
resources/bin/campaign/maps/scena021.ini
resources/bin/campaign/maps/scena022.ini
resources/bin/campaign/maps/scenf022.ini
resources/bin/campaign/maps/scenh001.ini
resources/bin/campaign/maps/scenh002.ini
resources/bin/campaign/maps/scenh003.ini
resources/bin/campaign/maps/scenh004.ini
resources/bin/campaign/maps/scenh005.ini
resources/bin/campaign/maps/scenh006.ini
resources/bin/campaign/maps/scenh007.ini
resources/bin/campaign/maps/scenh008.ini
resources/bin/campaign/maps/scenh009.ini
resources/bin/campaign/maps/scenh010.ini
resources/bin/campaign/maps/scenh011.ini
resources/bin/campaign/maps/scenh012.ini
resources/bin/campaign/maps/scenh013.ini
resources/bin/campaign/maps/scenh014.ini
resources/bin/campaign/maps/scenh015.ini
resources/bin/campaign/maps/scenh016.ini
resources/bin/campaign/maps/scenh017.ini
resources/bin/campaign/maps/scenh018.ini
resources/bin/campaign/maps/scenh019.ini
resources/bin/campaign/maps/scenh020.ini
resources/bin/campaign/maps/scenh021.ini
resources/bin/campaign/maps/scenh022.ini
resources/bin/campaign/maps/sceno001.ini
resources/bin/campaign/maps/sceno002.ini
resources/bin/campaign/maps/sceno003.ini
resources/bin/campaign/maps/sceno004.ini
resources/bin/campaign/maps/sceno005.ini
resources/bin/campaign/maps/sceno006.ini
resources/bin/campaign/maps/sceno007.ini
resources/bin/campaign/maps/sceno008.ini
resources/bin/campaign/maps/sceno009.ini
resources/bin/campaign/maps/sceno010.ini
resources/bin/campaign/maps/sceno011.ini
resources/bin/campaign/maps/sceno012.ini
resources/bin/campaign/maps/sceno013.ini
resources/bin/campaign/maps/sceno014.ini
resources/bin/campaign/maps/sceno015.ini
resources/bin/campaign/maps/sceno016.ini
resources/bin/campaign/maps/sceno017.ini
resources/bin/campaign/maps/sceno018.ini
resources/bin/campaign/maps/sceno019.ini
resources/bin/campaign/maps/sceno020.ini
resources/bin/campaign/maps/sceno021.ini
resources/bin/campaign/maps/sceno022.ini
resources/bin/campaign/maps/seed/1000.map
resources/bin/campaign/maps/seed/103.map
resources/bin/campaign/maps/seed/106.map
resources/bin/campaign/maps/seed/113.map
resources/bin/campaign/maps/seed/117.map
resources/bin/campaign/maps/seed/12.map
resources/bin/campaign/maps/seed/122.map
resources/bin/campaign/maps/seed/123.map
resources/bin/campaign/maps/seed/1498.map
resources/bin/campaign/maps/seed/150.map
resources/bin/campaign/maps/seed/157.map
resources/bin/campaign/maps/seed/16.map
resources/bin/campaign/maps/seed/173.map
resources/bin/campaign/maps/seed/175.map
resources/bin/campaign/maps/seed/182.map
resources/bin/campaign/maps/seed/200.map
resources/bin/campaign/maps/seed/203.map
resources/bin/campaign/maps/seed/207.map
resources/bin/campaign/maps/seed/2106.map
resources/bin/campaign/maps/seed/223.map
resources/bin/campaign/maps/seed/233.map
resources/bin/campaign/maps/seed/24.map
resources/bin/campaign/maps/seed/2437.map
resources/bin/campaign/maps/seed/250.map
resources/bin/campaign/maps/seed/2620.map
resources/bin/campaign/maps/seed/2674.map
resources/bin/campaign/maps/seed/268.map
resources/bin/campaign/maps/seed/269.map
resources/bin/campaign/maps/seed/27.map
resources/bin/campaign/maps/seed/275.map
resources/bin/campaign/maps/seed/298.map
resources/bin/campaign/maps/seed/300.map
```
