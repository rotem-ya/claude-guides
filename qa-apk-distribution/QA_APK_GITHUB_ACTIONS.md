# APK בדיקה (sideload) דרך GitHub Actions — קישור הורדה קבוע

מדריך לקלוד. מבוסס על `.github/workflows/build-apk.yml` הפעיל בפועל ב-`rotem-ya/WhoIsThere` (נבדק מול הקוד בזמן הכתיבה, לא מהזיכרון).

**מה זה פותר:** רותם צריך לבדוק כל שינוי על מכשיר אנדרואיד אמיתי, לעתים קרובות דרך Termux (ראה `work-habits/WORK_HABITS.md`) — בלי דפדפן נוח, בלי כניסה ל-Play Console, בלי סבלנות ל-unzip. הפתרון: קישור הורדה **קבוע** שמתעדכן אוטומטית בכל push, מוריד APK מוכן להתקנה ישירה.

**חשוב להבחין:** זה **לא** תחליף לבילד שעולה לחנות (Play/App Store) — ראה `store-release/COWORK_STORE_RELEASE_GUIDE.md` לזה. זה מסלול נפרד לגמרי, ל-sideload בלבד, עם keystore נפרד ולא-רגיש.

---

## הרעיון המרכזי: שני tag_name קבועים במקום release חדש בכל פעם

הטריק הוא ב-[`softprops/action-gh-release`](https://github.com/softprops/action-gh-release) עם **אותו `tag_name` קבוע** בכל ריצה (למשל `qa-latest`), ו-`make_latest`. במקום ליצור release חדש (וכתובת חדשה) בכל בילד, זה **מחליף את הקבצים המצורפים לאותו release קיים** — כך שהכתובת הבאה **אף פעם לא משתנה**:
```
https://github.com/<owner>/<repo>/releases/download/qa-latest/app-release.apk
```
זה שונה מהותית מ-`actions/upload-artifact` (שגם קיים ב-workflow, לצד זה) — artifact פג תוקף אחרי כמה ימים ודורש login+session ל-GitHub כדי להוריד; release attachment **לא פג תוקף** ולא דורש session פעיל, רק את הקישור.

## שני ערוצים מקבילים

WhoIsThere משתמש בשני tag שונים בו-זמנית, לצרכים שונים:
- **`qa-latest`** — מתעדכן רק מ-`main`. "מה שבאמת יציב עכשיו".
- **`qa-launch`** — מתעדכן מרשימת ענפי-הפיתוח הפעילים (hardcoded ב-`if`, ראה תקלה נפוצה למטה). "הפיצ'רים הכי חדשים, עוד לא ב-main".

בפרויקט חדש עם ענף פיתוח יחיד (ראה `global-account/ACCOUNT_INFO.md` — מוסכמת ענף-אחד) אולי מספיק ערוץ אחד; שני ערוצים משתלמים כשיש הפרדה בין "יציב" ל"הכי עדכני".

## ה-workflow המלא (מדויק, מה-repo)

```yaml
name: Build APK
on:
  push:
    branches: [ main, claude/** ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write   # חובה — כדי ש-softprops/action-gh-release יוכל ליצור/לעדכן release

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - uses: subosito/flutter-action@v2
        with: { flutter-version: '3.27.4', channel: stable, cache: true }

      - name: Create local.properties
        run: |
          FLUTTER_SDK=$(dirname $(dirname $(which flutter)))
          echo "flutter.sdk=$FLUTTER_SDK" > android/local.properties
          echo "sdk.dir=$ANDROID_SDK_ROOT" >> android/local.properties

      - name: Restore QA keystore
        run: echo "<base64 של קובץ keystore ה-QA>" | base64 -d > android/app/keystore.jks

      - run: flutter clean && rm -rf ~/.pub-cache
      - run: flutter pub get
      - run: dart run flutter_launcher_icons   # רק אם רלוונטי לפרויקט

      - name: Analyze (לא חוסם בילד QA)
        run: flutter analyze || true

      - name: Build release APK
        env:
          KEYSTORE_STORE_PASS: "<סיסמת ה-QA keystore>"
          KEYSTORE_ALIAS: "<alias>"
          KEYSTORE_KEY_PASS: "<סיסמת ה-key>"
        run: flutter build apk --release

      - uses: actions/upload-artifact@v4
        with:
          name: app-release-apk
          path: build/app/outputs/flutter-apk/app-release.apk
          retention-days: 3   # רק גיבוי זמני — הקישור האמיתי הוא ה-release למטה

      - name: Publish to qa-latest (stable link)
        if: github.ref == 'refs/heads/main'
        uses: softprops/action-gh-release@v2
        with:
          tag_name: qa-latest
          name: QA build (latest)
          body: "Latest QA APK — commit ${{ github.sha }}"
          files: build/app/outputs/flutter-apk/app-release.apk
          make_latest: true

      - name: Publish to qa-launch (active dev branch, stable link)
        if: github.ref == 'refs/heads/<שם-ענף-הפיתוח-הפעיל>'
        uses: softprops/action-gh-release@v2
        with:
          tag_name: qa-launch
          name: QA build (launch branch — latest features)
          body: "Latest launch APK — branch ${{ github.ref_name }}, commit ${{ github.sha }}"
          files: build/app/outputs/flutter-apk/app-release.apk
          make_latest: false
```

## keystore ה-QA — לא ה-upload key האמיתי

**קריטי להבחין:** ה-keystore כאן הוא ייעודי ל-sideload בלבד, **לא** קשור בשום צורה ל-upload key של Play (ראה `global-account/SECRETS_POINTER.md` וטבלת "פר-אפליקציה מול משותף" שם). ל-Google Play אין שום מושג על ה-keystore הזה — מכשיר שמתקין APK חתום איתו **לא יכול** לקבל עדכון בהמשך מ-Play (חתימות שונות), וזה בסדר גמור כי זו כל הנקודה: זה ערוץ נפרד, ל-sideload, לא לחנות.

בגלל שהמפתח הזה לא-רגיש (לא נותן גישה לחנות בשם אף אחד), ב-WhoIsThere הוא **מוטמע ישירות בקוד ה-workflow** (base64), לא ב-Secrets — וזה בסדר, בניגוד מוחלט לאזהרה על ה-upload key האמיתי ב-`store-release/COWORK_STORE_RELEASE_GUIDE.md`. **אל תבלבלו בין השניים** בפרויקט חדש: אם אין ודאות מוחלטת שמפתח נתון הוא QA-בלבד ולא upload key אמיתי, מתייחסים אליו כרגיש.

## תקלות נפוצות

| מה קרה | תיקון |
|---|---|
| ה-`if: github.ref == 'refs/heads/...'` ל-`qa-launch` נשאר עם שם ענף ישן אחרי שהתחילו לעבוד על ענף חדש | לעדכן את התנאי (או להוסיף עוד שורת `\|\|`) בכל פעם שענף הפיתוח הפעיל משתנה — ב-WhoIsThere זה נצבר לשלושה תנאי `||` עם ענפים היסטוריים שרובם כבר לא בשימוש |
| APK מותקן אבל האנדרואיד חוסם ("לא הותקנה מ-Play Store") | להפעיל "התקן אפליקציות ממקורות לא ידועים" עבור האפליקציה שממנה מורידים (דפדפן/קבצים) — חד-פעמי למכשיר |
| מנסים לעדכן APK שהותקן מ-Play עם ה-APK הזה, או ההפך | נכשל תמיד — חתימות שונות (QA מול upload key). להסיר את הישן לפני התקנת השני |
| `permissions: contents: write` חסר בקובץ | `softprops/action-gh-release` נכשל בלי הרשאה מפורשת לכתוב release; זו לא ברירת מחדל ב-workflow שנוצר מאפס |
