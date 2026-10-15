# claude-guides

מדריכי הקמה עמידים לזמן, לשימוש חוזר בין פרויקטים, מיועדים לקלוד (או לכל אדם) שמתחיל פרויקט חדש ורוצה לשכפל תשתית שכבר עבדה בפרויקט קודם.

כל מדריך נבדק מול קוד אמיתי בזמן הכתיבה (לא מהזיכרון), ומצוין בכל קובץ מאיזה ריפו נלקח.

## מדריכים קיימים

- [`token-kit/`](token-kit/README.md) — **ערכה שמותקנת בכל פרויקט, חדש וקיים**: מפת קוד אוטומטית (כל פונקציה ומחלקה עם טווח השורות שלה), hook שמכין את סשן הענן לפני ההודעה הראשונה, וכללי עבודה שחוסכים טוקנים בלי לוותר על איכות. בפרויקט חדש: "תתקין token-kit מ-claude-guides". מקור: `rotem-ya/Mida`, אוקטובר 2026.

- [`firebase-auth/FIREBASE_AUTH_SETUP_GUIDE.md`](firebase-auth/FIREBASE_AUTH_SETUP_GUIDE.md) — הקמת Firebase Authentication עם Google Sign-In ו-Apple Sign-In בפרויקט Flutter חדש. מקור: `rotem-ya/WhoIsThere`.
- [`store-release/COWORK_STORE_RELEASE_GUIDE.md`](store-release/COWORK_STORE_RELEASE_GUIDE.md) — הקמת CI להעלאת בילד ל-TestFlight/App Store וכעת גם Google Play דרך Codemagic (AAB+IPA לחנויות), כולל תבנית לעקיפת מגבלות push של סוכן. מקור: `rotem-ya/WhoIsThere`.
- [`qa-apk-distribution/QA_APK_GITHUB_ACTIONS.md`](qa-apk-distribution/QA_APK_GITHUB_ACTIONS.md) — APK בדיקה (sideload, לא לחנות) דרך GitHub Actions עם קישור הורדה קבוע שמתעדכן אוטומטית בכל push, נפרד לגמרי מה-CI של החנויות. מקור: `rotem-ya/WhoIsThere`.
- [`windows-store/WINDOWS_MSIX_STORE_GUIDE.md`](windows-store/WINDOWS_MSIX_STORE_GUIDE.md) — בנייה של Flutter לחלונות ב-GitHub Actions (בלי מחשב Windows), אריזת MSIX והגשה ל-Microsoft Store, כולל שלושת המכשולים שקורים כמעט תמיד (ה-CMake של Firebase, מכסת artifacts, analyze שיוצא 1 על info), אילו plugins אין להם מימוש בחלונות ולמה זה נכשל רק בזמן ריצה, ומלכודות UX שהופכות אפליקציית מחשב לאפליקציית טלפון מוגדלת. מקור: `rotem-ya/quick-sign`.
- [`google-play-production-access/SKILL.md`](google-play-production-access/SKILL.md) — **Skill בר-הפעלה** (לא רק מדריך): הוצאת אפליקציה מ-Closed testing ל-Production ב-Google Play אחרי שעברו 14 הימים ו-12 הבודקים — השאלון עם תשובות מוכנות, קידום הגרסה הקיימת במקום העלאת בילד חדש, מלכודת ה-EU-27/DSA, כתובת מדיניות פרטיות שנשברת בשקט, ולמה ה-release notes לשחרור ראשון הם לא "מה חדש". מקור: `rotem-ya/WhoIsThere`, אוגוסט 2026.
- [`global-account/ACCOUNT_INFO.md`](global-account/ACCOUNT_INFO.md) — מזהים גלובליים שחוזרים בין אפליקציות (Team ID, חשבונות, מוסכמות שמות). **לא מכיל סודות.**
- [`global-account/SECRETS_POINTER.md`](global-account/SECRETS_POINTER.md) — טבלה של איפה מפתחות/סיסמאות אמיתיים שמורים בפועל, לפי אפליקציה. **מכיל רק מיקומים, אף פעם לא ערכים.**
- [`writing-style/NO_AI_TELLS_STYLE.md`](writing-style/NO_AI_TELLS_STYLE.md) — כללי כתיבה לכל טקסט גלוי למשתמש (מסכים, פוש, תיאורי חנות וכו'), כולל איסור מוחלט על מקף ארוך (—). לא חל על קוד/קומיטים/תיעוד פנימי.
- [`work-habits/WORK_HABITS.md`](work-habits/WORK_HABITS.md) — איך רותם עובד מול קלוד קוד: קצב עבודה (משימה אחת בכל פעם, push רק אחרי כמה משימות), AskUserQuestion לבחירות, תיאום בין סשנים מקבילים, handoff בין ריפואים, הרשאות push/tag/workflow של סוכן, עבודה מ-Termux על אנדרואיד. מקור: `rotem-ya/WhoIsThere`.

## Skills — איך משתמשים

`google-play-production-access/` הוא **Skill של קלוד קוד**, לא מדריך לקריאה.
כדי שקלוד יפעיל אותו לבד כשהנושא עולה, מעתיקים את התיקייה אל הפרויקט:

```bash
mkdir -p .claude/skills
cp -r /path/to/claude-guides/google-play-production-access .claude/skills/
```

אפשר גם `~/.claude/skills/` כדי שיהיה זמין בכל הפרויקטים. מזהים Skill לפי
`SKILL.md` עם frontmatter (`name` + `description`) בראש הקובץ — ה-`description`
הוא מה שקובע מתי קלוד מפעיל אותו, ולכן הוא מנוסח עם המילים שבהן באמת שואלים,
בעברית ובאנגלית.

מדריך רגיל (`.md` בלי frontmatter) נשאר משהו שקוראים או מפנים אליו ידנית.

## הוספת מדריך חדש

תיקייה נפרדת לכל נושא, קובץ `.md` אחד לפחות שמתחיל בהקשר (מאיזה פרויקט/קוד המדריך נגזר) ומסתיים בטבלת תקלות נפוצות אם רלוונטי. עדכנו את הרשימה למעלה.

## `global-account/` — כלל ברזל

מותר: Team ID, שמות חשבונות, כתובות מייל, מוסכמות שמות, "איפה למצוא X". **אסור, לעולם:** מפתח API, תוכן קובץ `.p8`, סיסמת keystore, JSON של service account, או כל ערך שאם ידלוף מאפשר גישה/חתימה בשם החשבון. אם לא בטוחים אם משהו מותר, ההנחה היא שהוא אסור, שואלים קודם.
