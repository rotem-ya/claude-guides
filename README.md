# claude-guides

מדריכי הקמה עמידים לזמן, לשימוש חוזר בין פרויקטים, מיועדים לקלוד (או לכל אדם) שמתחיל פרויקט חדש ורוצה לשכפל תשתית שכבר עבדה בפרויקט קודם.

כל מדריך נבדק מול קוד אמיתי בזמן הכתיבה (לא מהזיכרון), ומצוין בכל קובץ מאיזה ריפו נלקח.

## מדריכים קיימים

- [`firebase-auth/FIREBASE_AUTH_SETUP_GUIDE.md`](firebase-auth/FIREBASE_AUTH_SETUP_GUIDE.md) — הקמת Firebase Authentication עם Google Sign-In ו-Apple Sign-In בפרויקט Flutter חדש. מקור: `rotem-ya/WhoIsThere`.
- [`store-release/COWORK_STORE_RELEASE_GUIDE.md`](store-release/COWORK_STORE_RELEASE_GUIDE.md) — הקמת CI להעלאת בילד ל-TestFlight/App Store (Codemagic) ול-Google Play (GitHub Actions), כולל תבנית לעקיפת מגבלות push של סוכן. מקור: `rotem-ya/WhoIsThere`.
- [`global-account/ACCOUNT_INFO.md`](global-account/ACCOUNT_INFO.md) — מזהים גלובליים שחוזרים בין אפליקציות (Team ID, חשבונות, מוסכמות שמות). **לא מכיל סודות.**
- [`global-account/SECRETS_POINTER.md`](global-account/SECRETS_POINTER.md) — טבלה של איפה מפתחות/סיסמאות אמיתיים שמורים בפועל, לפי אפליקציה. **מכיל רק מיקומים, אף פעם לא ערכים.**
- [`writing-style/NO_AI_TELLS_STYLE.md`](writing-style/NO_AI_TELLS_STYLE.md) — כללי כתיבה לכל טקסט גלוי למשתמש (מסכים, פוש, תיאורי חנות וכו'), כולל איסור מוחלט על מקף ארוך (—). לא חל על קוד/קומיטים/תיעוד פנימי.

## הוספת מדריך חדש

תיקייה נפרדת לכל נושא, קובץ `.md` אחד לפחות שמתחיל בהקשר (מאיזה פרויקט/קוד המדריך נגזר) ומסתיים בטבלת תקלות נפוצות אם רלוונטי. עדכנו את הרשימה למעלה.

## `global-account/` — כלל ברזל

מותר: Team ID, שמות חשבונות, כתובות מייל, מוסכמות שמות, "איפה למצוא X". **אסור, לעולם:** מפתח API, תוכן קובץ `.p8`, סיסמת keystore, JSON של service account, או כל ערך שאם ידלוף מאפשר גישה/חתימה בשם החשבון. אם לא בטוחים אם משהו מותר, ההנחה היא שהוא אסור, שואלים קודם.
