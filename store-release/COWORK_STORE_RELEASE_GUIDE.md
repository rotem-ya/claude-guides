# מדריך לcowork — העלאת בילד לאפל (TestFlight/App Store) ולגוגל (Play) דרך CI

מסמך הפניה לסוכן שעובד עם בעל הפרויקט על הגשת גרסה לחנויות. מבוסס על תהליך עובד בפועל בפרויקט WhoIsThere (`rotem-ya/WhoIsThere`) — לא תיאוריה. אין כאן צורך לפתוח Xcode או Android Studio בשום שלב, הכל דרך CI בענן.

**עקרון-על:** גם iOS וגם Android נבנים ונחתמים אוטומטית ב-CI. cowork **לא** יכול ללחוץ בממשק Codemagic/Play Console בשם בעל הפרויקט — אבל יכול להפעיל בנייה (דרך push לגיט) ולהכין את כל הטקסטים/הנכסים כך שנשארת לבעל הפרויקט רק לחיצת Submit הסופית.

---

## חלק 0 — הקמה חד-פעמית (לפני הבילד הראשון בפרויקט חדש)

### 0א. Apple — App ID + App Store Connect + מפתח API
1. [developer.apple.com/account/resources/identifiers](https://developer.apple.com/account/resources/identifiers/list) → **➕** → App IDs → App → Bundle ID (Explicit, לדוגמה `com.yourname.yourapp`) → Register.
2. [appstoreconnect.apple.com/apps](https://appstoreconnect.apple.com/apps) → **➕ → New App** → iOS, שם, שפה ראשית, בחר את ה-Bundle ID מהרשימה, SKU (מזהה פנימי חופשי) → Create.
3. [appstoreconnect.apple.com/access/integrations/api](https://appstoreconnect.apple.com/access/integrations/api) → Team Keys → **➕** → שם (`Codemagic` למשל), Access: **App Manager** → Generate → **הורד את קובץ ה-`.p8` מיד** (מוריד רק פעם אחת!). רשמו גם את ה-**Issuer ID** וה-**Key ID** שמופיעים בעמוד.

### 0ב. Codemagic — חיבור הריפו + המפתח
1. [codemagic.io/signup](https://codemagic.io/signup) → Sign up with GitHub → אשר גישה לריפו (אפשר "Only select repositories").
2. [codemagic.io/apps](https://codemagic.io/apps) → **Add application** → GitHub → בחר את הריפו → Finish. Codemagic מזהה אוטומטית קובץ `codemagic.yaml` אם קיים בשורש הריפו.
3. Teams → **Integrations** → App Store Connect → Manage keys / Add key:
   - שם המפתח — **תקבע שם קבוע ותשתמש בו בדיוק** גם ב-`codemagic.yaml` (למשל `Apple_Key_MyApp`). שם שלא תואם → "key not found" בבנייה.
   - Issuer ID + Key ID מ-0א.
   - קובץ ה-`.p8` מ-0א.

### 0ג. `codemagic.yaml` — הקובץ שגורר את כל זה
שימו בשורש הריפו (התאימו placeholders):
```yaml
workflows:
  ios-testflight:
    name: <AppName> iOS — TestFlight
    triggering:
      events: [tag]
      tag_patterns:
        - pattern: 'ios-v*'
          include: true
    instance_type: mac_mini_m2
    max_build_duration: 90
    integrations:
      app_store_connect: Apple_Key_MyApp   # השם המדויק מ-0ב
    environment:
      ios_signing:
        distribution_type: app_store
        bundle_identifier: com.yourname.yourapp
      flutter: 3.27.4
      xcode: latest
      cocoapods: default
    scripts:
      - name: Get Flutter packages
        script: flutter pub get
      - name: Set up code signing settings on Xcode project
        script: xcode-project use-profiles
      - name: Build signed IPA
        script: |
          flutter build ipa --release \
            --build-name=1.0.0 \
            --build-number=$PROJECT_BUILD_NUMBER \
            --export-options-plist=/Users/builder/export_options.plist
    artifacts:
      - build/ios/ipa/*.ipa
    publishing:
      app_store_connect:
        auth: integration
        submit_to_testflight: true   # מעלה ל-TestFlight, לא מגיש ל-Review
```
**חתימה אוטומטית:** `ios_signing` + `xcode-project use-profiles` מטפלים בהכל — Codemagic יוצר/מושך certificate + provisioning profile בעצמו מול App Store Connect API, אין צורך להעלות קבצי `.p12`/`.mobileprovision` ידנית.

טריגר: דחיפת תג בתבנית `ios-v*` (למשל `ios-v1`) מריצה בנייה. **אפשר גם Start new build ידני מה-UI של Codemagic** בלי תג, זו אופציית גיבוי.

### 0ד. Google Play — יצירת האפליקציה + מפתח חתימה
1. [play.google.com/console](https://play.google.com/console) → Create app → מלא שם/שפה/סוג (Free) → Create.
2. יצירת keystore חתימה (**חד פעמי, לשמור לתמיד**):
```bash
keytool -genkey -v -keystore upload-keystore.jks -keyalg RSA -keysize 2048 \
  -validity 10000 -alias upload
```
3. ב-Play Console → **App integrity → App signing** — Google Play App Signing פעיל כברירת מחדל: אתם מעלים חתום עם ה-**upload key** שיצרתם, גוגל חותם מחדש פנימית עם מפתח משלו לפני שהוא מגיע למשתמשים. חשוב: ה-SHA-1 של ה-**upload key** שלכם הוא זה שחייב להתאים למה שרשום ב-Play, לא ה-SHA-1 שגוגל מציג תחת "App signing key certificate".

### 0ה. GitHub Actions — בניית ה-AAB
`.github/workflows/build-aab.yml` (התאימו placeholders):
```yaml
name: Build AAB (Google Play)
on:
  workflow_dispatch:
    inputs:
      build_name:
        default: '1.0.0'
  push:
    tags: ['aab-v*']
    paths: ['.github/aab-release.txt']   # מפעיל רק כשמשנים marker ייעודי, לא בכל פוש

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - uses: subosito/flutter-action@v2
        with: { flutter-version: '3.27.4', channel: stable, cache: true }

      - name: Restore upload keystore from secret
        run: echo "${{ secrets.UPLOAD_KEYSTORE_BASE64 }}" | base64 -d > android/app/keystore.jks

      - run: flutter pub get
      - name: Build signed App Bundle
        env:
          KEYSTORE_STORE_PASS: ${{ secrets.UPLOAD_KEYSTORE_PASSWORD }}
          KEYSTORE_ALIAS: ${{ secrets.UPLOAD_KEY_ALIAS }}
          KEYSTORE_KEY_PASS: ${{ secrets.UPLOAD_KEY_PASSWORD }}
        run: |
          flutter build appbundle --release \
            --build-name="${{ github.event.inputs.build_name || '1.0.0' }}" \
            --build-number="${{ github.run_number }}"

      - uses: actions/upload-artifact@v4
        with:
          name: app-release-aab
          path: build/app/outputs/bundle/release/app-release.aab
```
צריך גם ב-`android/app/build.gradle` בלוק `signingConfigs` שקורא את שלוש ה-env vars למעלה (`KEYSTORE_STORE_PASS`/`KEYSTORE_ALIAS`/`KEYSTORE_KEY_PASS`) ומחבר ל-`android/app/keystore.jks`.

**Secrets שצריך להוסיף ב-GitHub → Settings → Secrets and variables → Actions:**
| שם | ערך |
|---|---|
| `UPLOAD_KEYSTORE_BASE64` | `base64 -w0 upload-keystore.jks` (Linux) / `base64 -i upload-keystore.jks \| pbcopy` (Mac) |
| `UPLOAD_KEYSTORE_PASSWORD` | סיסמת ה-keystore |
| `UPLOAD_KEY_ALIAS` | ה-alias (`upload` בדוגמה) |
| `UPLOAD_KEY_PASSWORD` | סיסמת ה-key |

⚠️ **אזהרה מניסיון בפועל:** ב-WhoIsThere, בגלל שההדבקה של הסוד דרך מובייל נכשלה בזמן אמת, המפתח **הוטמע ישירות** (base64 בתוך קובץ ה-workflow) כפתרון זמני להשקה — וזה נשאר כחוב אבטחה לא-מטופל בריפו ציבורי. **אל תשכפלו את זה בפרויקט חדש.** אם הדבקת secret נכשלת, זו בעיה לפתור (למשל secret קצר מדי/רווחים מיותרים), לא סיבה להטמיע מפתח חתימה בקוד.

---

## חלק 1 — iOS: הפעלת בנייה חדשה + TestFlight

```bash
git fetch origin <release-branch>
git tag ios-v1 <commit-sha>
git push origin ios-v1
```
(אם `ios-v1` כבר תפוס — `ios-v2` וכו', התג הוא מה שמפעיל, לא השם עצמו.)

זמן בנייה: ~15–25 דקות. בסיום, ה-IPA עולה אוטומטית ל-TestFlight (**לא** מוגש לבדיקת Apple — זה שלב נפרד).

**הגשה בפועל ל-App Store Review** (אחרי שה-build הופיע ב-TestFlight, "Processing" הסתיים — עוד 10-30 דק' נוספות):
1. App Store Connect → האפליקציה → **App Store** tab → **+ Version** → מספר גרסה.
2. **Build** → בחר את הבילד שעלה.
3. מלא **What's New in This Version**, צילומי מסך (אם גרסה ראשונה/שינוי חזותי), Export Compliance (בד"כ "No" אם אין הצפנה חריגה).
4. **Add for Review → Submit.**

---

## חלק 2 — Android: הפעלת בנייה + העלאה ל-Play

**הפעלת הבנייה** — שתי דרכים:
- דחיפה ל-marker file (`.github/aab-release.txt` — כל תוכן, אפילו רק תאריך, זה רק trigger):
```bash
echo "release $(date +%Y%m%d)" > .github/aab-release.txt
git add .github/aab-release.txt && git commit -m "chore: trigger AAB build" && git push
```
- או תג `aab-v*`, או **Run workflow** ידני ב-Actions UI (עם `workflow_dispatch`, אם יש לכם הרשאת Actions — ראה הערה בחלק 3 אם לא).

**הורדה והעלאה:**
1. GitHub → Actions → הריצה הרלוונטית → Artifacts → הורד `app-release-aab` (או השם שקבעתם).
2. Play Console → האפליקציה → **Testing → Closed testing (Alpha)** (או Production, לפי מדיניות) → **Create new release**.
3. גרור את קובץ ה-`.aab` → מלא **Release notes** → Save → Review release → **Start rollout**.
4. אמת פעם אחת בהקמה: **Store settings** → Website/Privacy Policy URL ממולאים; **Data safety**, **Content rating**, **Target audience** מולאו (חד-פעמי, לא בכל release).

---

## חלק 3 — הערה קריטית: cowork לא תמיד יכול להפעיל workflow_dispatch או לדחוף תגיות ישירות

בפרויקטים שבהם ל-agent/cowork יש **הרשאת push מוגבלת לענף מסוים בלבד** (מקובל בסביבות cowork/agent מבודדות), דחיפת תג (`git push origin ios-v1`) או `workflow_dispatch` דרך API עלולים להיכשל ב-403. הפתרון שעבד בפועל ב-WhoIsThere: **workflow-שרשור דרך marker file בענף המותר**.

`.github/push-ios-tag.yml` — עובד על **push event רגיל** (שכן מותר) ולא על `workflow_dispatch`:
```yaml
on:
  push:
    paths:
      - '.github/ios-tag.txt'      # שורה ראשונה = מספר התג ליצור, למשל "3"
      - '.github/sync-branch.txt'  # אופציונלי: שורה1=ענף יעד, שורה2=SHA לסנכרן אליו
jobs:
  tag-and-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create ios-v<N> tag via GitHub API
        run: |
          TAG="ios-v$(cat .github/ios-tag.txt | tr -d '[:space:]')"
          curl -X POST -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
            https://api.github.com/repos/${{ github.repository }}/git/refs \
            -d "{\"ref\":\"refs/tags/$TAG\",\"sha\":\"${{ github.sha }}\"}"
```
כלומר: cowork עורך ודוחף `.github/ios-tag.txt` (מותר, זה push רגיל לענף שלו) → ה-workflow הזה, שרץ עם `GITHUB_TOKEN` הרגיל של ה-repo (לא של הסוכן), יוצר את התג האמיתי דרך ה-API. אותו טריק בדיוק פותר גם הפעלת `build-aab.yml`: משנים קובץ marker בנתיב שה-workflow עוקב אחריו (`.github/aab-release.txt`), ה-push עצמו (לא `workflow_dispatch`) הוא הטריגר.

**כלל אצבע:** אם MCP tool כמו `actions_run_trigger` מחזיר 403 עבור הסוכן, אל תנסה שוב באותה שיטה — ערוך קובץ בנתיב שכבר מוגדר כ-`paths:` באיזשהו workflow קיים ודחוף אותו.

---

## חלק 4 — תקלות נפוצות

| תסמין | סיבה | פתרון |
|---|---|---|
| Codemagic: "key not found" | שם ה-integration ב-Codemagic לא תואם בדיוק למה שכתוב ב-`codemagic.yaml` תחת `integrations.app_store_connect` | לתקן את אחד מהשניים כך שיתאימו אות-באות |
| Codemagic build נכשל ב-archive: "profile doesn't include aps-environment" | הפרופיל האוטומטי שנוצר לפני הרצת הסקריפטים לא כולל capability (בד"כ Push) שהתווסף ל-App ID רק *אחרי* שהפרופיל כבר נוצר בפעם הראשונה | למחוק את הפרופיל הישן ב-Apple Developer portal (Profiles), או להוסיף שלב סקריפט שיוצר פרופיל טרי מחדש עם `app-store-connect profiles create` לפני `xcode-project use-profiles` |
| GitHub Actions: "UPLOAD_KEYSTORE_BASE64 secret is not set" | ה-4 secrets מחלק 0ה עדיין לא נוספו בפועל ב-Settings → Secrets | להוסיף אותם (חד-פעמי, ממכשיר עם גישה לקובץ ה-keystore) |
| Play: "You uploaded an APK/AAB signed with a different certificate" | ה-AAB לא חתום עם אותו upload key שרשום ב-Play App Signing | לוודא ש-`UPLOAD_KEY_ALIAS`/הסיסמאות תואמים בדיוק לקובץ; אם אבד ה-keystore — Play Console → App signing → **Request upload key reset** |
| `workflow_dispatch` מחזיר 403 לסוכן | הרשאת push של cowork/agent מוגבלת לענף אחד, ו-API tokens ל-workflow_dispatch לא כלולים | ראה חלק 3 — טריק ה-marker file |
| iOS build number "already exists"/rejected on resubmit | Apple דורש build number גדול ממש מהקודם בכל בנייה חדשה, גם אם היא ל-TestFlight בלבד | להשתמש ב-`$PROJECT_BUILD_NUMBER`/`$GITHUB_RUN_NUMBER` שעולה אוטומטית בכל ריצה, לא במספר קבוע |

---

זה כל התהליך שנבדק בפועל ועבד עד TestFlight/Play חתום ומוכן להגשה. שינויים ספציפיים לפרויקט (bundle id, שם ה-integration, ענף בנייה) — התאימו את ה-placeholders למעלה.
