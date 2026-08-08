# Flutter לחלונות: בנייה, אריזת MSIX והגשה ל-Microsoft Store

מקור: `rotem-ya/quick-sign`, אוגוסט 2026. כל מה שכאן נבדק מול ריצות CI אמיתיות,
לא מהזיכרון. הריפו כבר היה עם `windows/` מתבנית Flutter, מה שחסר היה התשתית
מסביב.

המדריך מניח פרויקט Flutter קיים שרץ באנדרואיד/iOS/web, ורוצים ממנו גם אפליקציית
מחשב שנמכרת בחנות.

---

## למה דווקא דרך החנות ולא הפצה ישירה

זו לא שאלה של נוחות אלא של מכירות. קובץ `.exe` לא חתום מפעיל את SmartScreen,
שמציג "Windows protected your PC" ומסתיר את כפתור ההרצה מאחורי "More info".
עבור מוצר בכמה דולרים זה קטלני.

חתימה עצמאית דורשת תעודת OV/EV בכמה מאות דולרים בשנה. **בחנות מיקרוסופט חותמת
את החבילה בתהליך האישור**, בלי עלות נוספת מעבר לדמי החשבון החד-פעמיים. לכן
`store: true` בהגדרות ה-msix דווקא **משאיר את החבילה לא חתומה** בכוונה. זה לא
באג.

---

## בנייה ב-CI, בלי מחשב Windows

GitHub Actions מריץ `windows-latest`, אז אין צורך שלמישהו בצוות יהיה מחשב
Windows כדי לבנות ולארוז.

```yaml
jobs:
  build:
    runs-on: windows-latest
    env:
      CMAKE_POLICY_VERSION_MINIMUM: "3.5"   # ראה "מכשול 1" למטה
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with: { channel: stable, cache: true }
      - run: flutter config --enable-windows-desktop
      - run: flutter pub get
      - run: flutter analyze --no-pub --no-fatal-infos   # ראה "מכשול 3"
      - run: flutter build windows --release
      - name: Package as MSIX
        continue-on-error: true
        run: dart run msix:create --output-name myapp
```

בניית Windows לוקחת בערך 5 עד 6 דקות, והריצה כולה כ-10.

---

## שלושה מכשולים שיקרו כמעט בוודאות

### מכשול 1: ה-CMake של Firebase

אם בפרויקט יש `firebase_core` (או כל חבילת Firebase), הבנייה תמות עוד לפני שהיא
נוגעת בקוד שלכם:

```
CMake Error at .../firebase_cpp_sdk_windows/CMakeLists.txt:17
  Compatibility with CMake < 3.5 has been removed from CMake.
```

ה-SDK של Firebase ל-C++ מצהיר על `cmake_minimum_required` עתיק, ו-CMake 4
שמותקן על ה-runner הסיר את התאימות. הפתרון הוא בדיוק מה ש-CMake מציע בשגיאה:

```yaml
env:
  CMAKE_POLICY_VERSION_MINIMUM: "3.5"
```

זה חל על ה-SDK המצורף בלבד. הקבצים של Flutter עצמו כבר מבקשים 3.14.

### מכשול 2: מכסת אחסון של artifacts

```
Failed to CreateArtifact: Artifact storage quota has been hit.
```

**הבנייה מצליחה ורק ההעלאה נכשלת**, אז זה נראה כמו בנייה שבורה כשזה בעצם דיסק
מלא. המכסה היא לפי **חשבון** ולא לפי ריפו, וריפו פרטי צורך אותה בעוד ציבורי לא.

הפתרון: לפרסם ל-**GitHub Release** במקום artifact. נכסי release לא נספרים
במכסה, ונותנים קישור הורדה יציב שמתעדכן בכל בנייה.

```yaml
      - name: Zip the portable build
        run: >
          Compress-Archive -Path build/windows/x64/runner/Release/*
          -DestinationPath myapp-windows.zip -Force
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: windows-preview
          files: |
            myapp-windows.zip
            build/windows/x64/runner/Release/*.msix
```

צריך `permissions: contents: write` ברמת ה-job.

### מכשול 3: `flutter analyze` מפיל את הבנייה על lint שולי

`flutter analyze` מחזיר קוד יציאה 1 על **כל** ממצא, כולל `info`. אם מוסיפים
אותו כשער לפני הבנייה, שלושה lints ישנים שאף אחד לא התכוון לתקן יעצרו הכל.
`--no-fatal-infos` משאיר שגיאות ואזהרות קטלניות ומרפה מ-infos.

מלכודת: בבדיקה מקומית קל להריץ `flutter analyze | grep error` ולהתעלם מקוד
היציאה, ואז לא לראות את הבעיה עד שה-CI נופל.

---

## אילו plugins עובדים בחלונות

לבדוק לפי `flutter: plugin: platforms:` ב-pubspec של כל חבילה בתוך ה-pub cache,
לא לפי הזיכרון. במקרה של quick-sign:

| עובד | לא עובד ב-Windows |
| --- | --- |
| `file_picker`, `printing`, `share_plus` | `google_sign_in` (macOS בלבד) |
| `path_provider`, `shared_preferences` | `sign_in_with_apple` (iOS/macOS) |
| `pdfx`, `image_picker` | `receive_sharing_intent` (נייד בלבד) |
| כל חבילות Firebase | |
| כל חבילה שהיא Dart טהור (Syncfusion, `signature`, `image`) | |

**הסכנה האמיתית:** plugin בלי מימוש ל-Windows **לא מפיל את הבנייה**. הוא
מתקמפל יפה וזורק `MissingPluginException` אצל המשתמש. לכן חייבים לחסום את
נקודות הקריאה בקוד, לא להסתמך על הקומפיילר.

הדפוס שעבד, שכדאי להעתיק: קובץ עזר שמדבר ב**יכולות** ולא בפלטפורמות, כך
שנקודות הקריאה נקראות "האם יש כאן מצלמה" ולא חוזרות על בדיקות מערכת הפעלה.

```dart
class PlatformSupport {
  static bool get isMobile => !kIsWeb && (Platform.isAndroid || Platform.isIOS);
  static bool get isDesktop =>
      !kIsWeb && (Platform.isWindows || Platform.isMacOS || Platform.isLinux);

  static bool get hasCamera => isMobile;
  static bool get hasShareIntents => isMobile;
  static bool get hasGoogleSignIn => kIsWeb || isMobile || _isMacOS;
}
```

שימו לב במיוחד לתנאים ישנים שנכתבו כ-`if (kIsWeb) return;`. הכוונה שלהם כמעט
תמיד הייתה "רק בנייד", והם שקטים ושגויים ברגע שנוסף יעד דסקטופ.

---

## ארבע מלכודות UX שהופכות אפליקציית מחשב לאפליקציית טלפון מוגדלת

אלה לא באגים בקומפיילר. הן פוגעות רק בלקוח שמשלם.

1. **פריסת נייד במסך רחב.** אם יש תנאי `kIsWeb` שמפעיל פריסה רחבה, דסקטופ
   ייפול לפריסת הטלפון. התנאי צריך להיות `kIsWeb || isDesktop` יחד עם מבחן
   רוחב.
2. **הסתרת סרגלים אוטומטית.** דפוס נפוץ בנייד הוא לעבור למסך מלא כשנפתח מסמך,
   והקשה מחזירה את הסרגלים. במחשב זה נראה כמו אפליקציה שקרסה, כי אין שום רמז
   שלחיצה תחזיר אותם. כל קורא PDF בדסקטופ משאיר את הסרגל.
3. **כותרת החלון היא שם ה-target ב-CMake.** `windows/runner/main.cpp` מכיל
   `window.Create(L"my_app", ...)`, וזה מה שמופיע בשורת המשימות וב-Alt-Tab.
4. **`windows/runner/Runner.rc` נשאר על ברירות המחדל של התבנית:**
   `CompanyName` הוא `com.example` ו-`ProductName` הוא שם ה-target. זה גלוי
   במאפייני הקובץ של ה-exe.

---

## `msix_config` ב-pubspec

```yaml
dev_dependencies:
  msix: ^3.16.7

msix_config:
  display_name: MyApp
  publisher_display_name: <Package/Properties/PublisherDisplayName>
  identity_name: <Package/Identity/Name>
  publisher: <Package/Identity/Publisher>     # מחרוזת CN=... מלאה
  msix_version: 1.0.0.0
  logo_path: assets/icon/icon.png
  capabilities: internetClient
  store: true
```

שלושת ערכי הזהות מגיעים מ-Partner Center אחרי שריון השם, תחת **זהות המוצר**.

- `identity_name` מקבל **אותיות, ספרות, נקודות ומקפים בלבד**. קו תחתון נדחה
  על ידי הוולידטור של `msix`, וזה מפיל ריצה שלמה אחרי שהבנייה כבר הצליחה.
- `publisher` חייב להיות זהה **תו בתו** לשריון. אי-התאמה היא הסיבה הנפוצה
  ביותר לדחיית הגשה ראשונה.
- בלי הערכים האמיתיים, `msix:create` עדיין מייצר חבילה חתומה עצמית שנוחה
  לבדיקה מקומית. לכן כדאי `continue-on-error: true` על שלב האריזה, ולהעלות
  את ה-zip **לפני** האריזה, כדי שבעיית זהות מול החנות לא תסתיר בנייה תקינה.

---

## מה נדרש בהגשה עצמה

- שריון שם ב-Partner Center (חשבון מפתח יחיד, תשלום חד-פעמי נמוך)
- תיאור קצר ותיאור מלא. **זה טקסט גלוי למשתמש**, אז הוא כפוף ל-
  [`writing-style/NO_AI_TELLS_STYLE.md`](../writing-style/NO_AI_TELLS_STYLE.md),
  כולל האיסור על מקף ארוך. לא להעתיק את הטקסט של Google Play כמו שהוא: הוא
  מדבר על "בטלפון שלך" ועל שיתוף ממערכת ההפעלה, שלא קיימים במחשב.
- צילום מסך אחד לפחות, 1366x768 ומעלה. צילומי טלפון ייראו שגויים.
- לוגו 300x300
- **כתובת ציבורית למדיניות פרטיות**, חובה ברגע שמצהירים על `internetClient`
- שאלון דירוג גיל
- מחיר. אישור לוקח בין כמה שעות לכמה ימים.

---

## איך לבדוק את ה-UI בלי מחשב Windows

לא תחליף לבדיקה אמיתית, אבל תופס הרבה. אם לפרויקט יש גם build ל-web, הוא מריץ
את אותו קוד Flutter ואת אותה פריסה רחבה. מגישים אותו מקומית ומריצים Chromium
דרך Playwright ב-1366x768.

שני דברים שחייבים, אחרת מקבלים מסך לבן ובלי שגיאות:
- CanvasKit דורש WebGL, ובלי GPU צריך
  `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`
- Flutter מאתחל אסינכרונית. לחכות 15 עד 20 שניות לפני צילום.

ככה נתפסה מלכודת 2 למעלה, אחרי שהיא שרדה בנייה ירוקה, analyze נקי וכל הטסטים.
**קומפילציה מוכיחה שהקוד תקין, לא שהמוצר עובד.** רינדור PDF במיוחד לא עובר:
בדפדפן זה pdf.js, ובחלונות זה backend אחר לגמרי של `pdfx`.

---

## תקלות נפוצות

| תסמין | סיבה | פתרון |
| --- | --- | --- |
| `Compatibility with CMake < 3.5 has been removed` | ה-SDK של Firebase ל-C++ | `CMAKE_POLICY_VERSION_MINIMUM=3.5` ב-env של ה-job |
| `Failed to CreateArtifact: quota has been hit` | מכסת אחסון לפי חשבון, ריפו פרטי צורך אותה | לפרסם ל-release במקום artifact |
| הבנייה נופלת מיד אחרי analyze בלי שגיאות בפלט | `flutter analyze` יוצא 1 גם על `info` | `--no-fatal-infos` |
| `invalid identity name` | קו תחתון ב-`identity_name` | אותיות, ספרות, נקודות ומקפים בלבד |
| החבילה נדחית בהגשה | `publisher` לא זהה תו בתו לשריון | להעתיק מ-Partner Center שוב |
| האפליקציה נבנית ואז קורסת אצל המשתמש | plugin בלי מימוש ל-Windows, נכשל בזמן ריצה | לחסום את נקודות הקריאה, לא לסמוך על הקומפיילר |
| SmartScreen מזהיר על ה-exe | החבילה לא חתומה | מסלול החנות, מיקרוסופט חותמת באישור |
| כותרת החלון היא שם ה-target | ברירת מחדל של התבנית | `main.cpp` ו-`Runner.rc` |
| מסך לבן ב-Chromium headless | CanvasKit בלי WebGL | דגלי swiftshader |
