---
name: google-play-production-access
description: Take an Android app from Google Play closed testing to a public production listing, after the 14-day / 12-tester requirement is met. Covers the production access questionnaire (with drafted answers), promoting the existing build rather than uploading a new one, the country and privacy-policy traps, and what to check after approval. Use when applying for production access, promoting a closed test to production, filling the Play production questionnaire, or when a Play listing URL returns 404 because the app was never promoted. Hebrew: הגשה ל-Production בגוגל פליי, בקשת גישה לסביבת הייצור, קידום מבדיקה סגורה, שאלון 14 הימים.
---

# הגשת אפליקציה ל-Production ב-Google Play

נגזר מהגשה אמיתית שבוצעה ב-`rotem-ya/WhoIsThere` באוגוסט 2026, אחרי שהאפליקציה
ישבה חודש ב-Closed testing ולא הייתה בחנות הציבורית. **כל מלכודת כאן נתקלנו
בה או נמנענו ממנה בפועל** — זה לא תיאור של המסך.

---

## מתי זה רלוונטי

חשבון מפתח **אישי** שנפתח אחרי נובמבר 2023 לא יכול לפרסם ל-Production עד
שהוא עומד בשלושה תנאים במקביל:

1. גרסה פורסמה ל-Closed testing
2. **12 בודקים לפחות** הצטרפו
3. הבדיקה רצה **14 ימים רצופים** עם 12+ בודקים

הקונסולה מציגה את שלושתם עם ✓ ירוק כשהם מולאו, ואז נפתח כפתור
**"Apply for production access"**. עד אז אין מה לעשות חוץ מלשמור על מספר
הבודקים.

> **הדבר החשוב ביותר בשלב ההמתנה:** ירידה מתחת ל-12 בודקים מאפסת את המניין.
> לא לגעת בקבוצת הבודקים, גם לא אחרי ההגשה.

**סימן היכר שזה המצב שלך:** `play.google.com/store/apps/details?id=<package>`
מחזיר 404 בחלון אנונימי, למרות שהאפליקציה "אושרה". אישור ב-Closed testing
אינו פרסום.

---

## שלב 1 — לאסוף עובדות לפני שנוגעים בטופס

אל תמלא את השאלון מהזיכרון או מתיעוד. שלוש עובדות חייבות לבוא מהמקור:

| עובדה | מאיפה | למה דווקא משם |
|---|---|---|
| מספר הבודקים | Testing → Closed testing → Testers | מספר שחולק על המסך של גוגל הוא מה שמעכב בדיקה |
| מה הבודקים דיווחו | ערוץ המשוב האמיתי שלך | ראה שלב 2, זו השאלה שנקראת |
| מה שינית בעקבותיהם | הקומיטים / ה-changelog | צריך להיות ספציפי, לא "שיפרנו יציבות" |

---

## שלב 2 — השאלון

חמש שאלות פתוחות. **תשובות באנגלית**, גם כשהממשק בעברית: מי שקורא אותן קורא
אנגלית.

### מה באמת נבדק כאן

גוגל מנסה להבין שרצת בדיקה אמיתית ולא אספת 12 חשבונות כדי לעבור מסך. לכן:

**⚠️ המלכודת הגדולה: להפריד בין מה שהבודקים מצאו לבין מה שאתה מצאת.**
השאלה היא מה **הבודקים** תרמו. תשובה שמייחסת להם עבודה שעשית בעצמך היא בדיוק
מה שנופל בבדיקה. אצלנו, מתוך שישה תיקונים שנראו כמו "משוב", רק **שלושה** באמת
הגיעו מבודקים — והשאר עברו לשאלת המוכנות, שם הם עדיין נחשבים.

**⚠️ מלכודת שנייה: אל תטען טענה שאינך יכול לגבות.** הנוסח הראשון שלנו אמר
"הקבוצה נשארה מעל 12 לאורך כל התקופה". לא היה לנו רישום שמוכיח את זה, וגוגל
ממילא סימנה את התנאי כמולא מהנתונים שלה — כלומר המשפט לא הוסיף כלום וכן הוסיף
סיכון. ירד.

### תבניות תשובה

החלף את מה שבסוגריים בעובדות שלך. **אל תשאיר ניסוח כללי** — הספציפיות היא
כל העניין.

**How did you recruit your testers?**
```
[Friends, family, and people from <community/group>]. The app is
[a Hebrew word game made for an Israeli audience], so the testers match that
audience and played it the way real users would rather than as a favour. [N]
testers are enrolled in the closed track.
```

**How did you keep your testers engaged?**
```
[The game is multiplayer, so testers kept coming back to play against each
other rather than to file reports.] Over the test we added [a daily reward, a
weekly leaderboard, and push invitations], so there was a reason to open the
app on an ordinary day and not only when we asked.

Feedback did not depend on people writing to us. There is a "Send feedback"
button in the app, and it uploads a crash report with the last part of the
device log automatically whenever it crashes. That is how we heard about
problems from testers who never sent a message.
```

**What feedback did you receive about core functionality?**
```
[List only what testers actually produced. Three concrete defects with real
symptoms beat ten vague ones.]

- [A crash when sharing from an iPad, caused by a missing anchor for the
  share sheet.]
- [A crash when an ad failed to load, where the failure reached the top level.]
- [A crash on a database transaction when the connection dropped mid-round.]

Not one of these was reported by hand. They were found because the app sends
its own logs.
```

**What changes did you make as a result?**
```
[Say which are in the build being submitted and which are not. "All fixed" is
a claim about a specific build and is easy to get wrong.]

[Two of the three are fixed in the version being submitted: <how>. The third
is fixed and is in the next release rather than this one. It was identified
from a log, reproduced, and closed against a specific change; it is not an
open issue we are shipping past.]
```

**How do you know the app is ready for production?**
```
[The strongest evidence available. Ours was: the same app is already live on
the Apple App Store, approved <date>, so this build line has been through a
full store review and is in front of real users on another platform.]

[Then your own QA: everything you found yourself belongs here, not in the
feedback answer.]

Behind that: an automated test suite that runs on every change, crash
reporting with device logs, and a remote configuration system that lets us
switch content or settings off without shipping an update.
```

### שדות קצרים

| שדה | מה לענות |
|---|---|
| Target audience | מה שכבר מוגדר ב-Content rating, אל תסתור אותו |
| Monetisation | **לאמת בקוד, לא לזכור.** "אין IAP" זו טענה שקל להיכשל בה — בדוק שאין ספריית רכישות בגרסה המוגשת |
| Countries | ראה שלב 3 |

---

## שלב 3 — מדינות: הצ'קבוקס שנראה תמים

**אל תסמן את כל המדינות אוטומטית.**

EU-27 גורר דרישות **DSA**: פרטי סוחר (שם, כתובת, מייל, טלפון) שמוצגים בדף
החנות. אם הם לא מולאו, סימון המדינות **חוסם את השחרור בשלב מאוחר** — אחרי
שכבר חיכית לאישור, לא לפני.

**כלל:** אם האלפא רצה בלי EU-27, להשאיר בלי EU-27. לוודא רק שמדינת היעד
העיקרית ברשימה. אפשר להוסיף אותן בכל רגע אחרי ההשקה — זו לא דלת שנסגרת.

---

## שלב 4 — בדיקות לפני השחרור

שלושת הראשונים כבר מולאו באישור המקורי. **הרביעי הוא היחיד שסביר שבור.**

- [ ] Store listing מלא
- [ ] Content rating
- [ ] Data safety
- [ ] 🔴 **כתובת מדיניות הפרטיות — לפתוח בחלון אנונימי ולוודא שהיא נטענת**

### למה דווקא הפרטיות

זה כשל שקט קלאסי: הכתובת הוזנה פעם, עבדה, ומאז **הסביבה שמסביבה השתנתה**.
אצלנו הריפו הפך לפרטי, GitHub Pages נכבה איתו, וכל כתובת
`<user>.github.io/<repo>/...` התחילה להחזיר 404. הבדיקה של גוגל נופלת על
מדיניות לא נגישה, אחרי שחיכית שבוע.

**לבדוק גם:** כתובת ה-support, ואם יש דף הורדה או קישור שיווקי בליסטינג.

---

## שלב 5 — אחרי אישור גוגל

הבקשה נבדקת ידנית. **צפוי עדכון במייל תוך עד 7 ימים.**

1. Production → **Create new release**
2. 🔴 **אל תעלה קובץ. `Add from library`** ובחר את הגרסה שכבר עברה בדיקה
   בטראק הסגור.
3. Release notes — ראה למטה
4. Review + start rollout, **100%**. הקהל הקיים זניח, אין מה לפרוס בהדרגה.
5. השחרור הראשון עובר **בדיקה של גוגל בפני עצמה**, שעות עד ימים

### למה לא להעלות בילד חדש

הגרסה בטראק הסגור היא זו שרצה 14 יום מול בודקים אמיתיים. בילד חדש הוא קוד
שאיש לא בדק, ובמקרה שלנו גם לא היה אפשרי לייצר (סודות חתימה חסרים). **קידום
מהספרייה הוא ברירת המחדל הנכונה, לא פשרה.**

### Release notes לשחרור ראשון — לא מה שחשבת

**זו ההופעה הראשונה של האפליקציה בחנות הציבורית.** כל מי שיקרא רואה אותה
בפעם הראשונה.

❌ אל תדביק "מה חדש" מגרסה קודמת. רשימת תיקוני באגים מגרסה שאיש מהקוראים לא
התקין היא לא חדשות, היא רעש.

✅ תאר **מה האפליקציה עושה**, בשלוש-ארבע שורות.

### האימות שמסיים

```
play.google.com/store/apps/details?id=<package>
```

בחלון אנונימי. אין 404 — האפליקציה בחנות, וכל קישור שיווקי מתחיל לעבוד.

---

## מוקש נפרד: targetSdk

לגוגל יש דדליין שנתי ל-targetSdk. **בילד שמתפרסם לפני התאריך פטור; כל עדכון
אחריו לא.**

זה הופך את ההגשה לדחופה **יותר**, לא פחות: אם השחרור מחליק מעבר לתאריך, תצטרך
בילד חדש עם ה-SDK החדש **בנוסף** לאישור, באותו שבוע. לבדוק את התאריך מול לוח
הזמנים הצפוי (עד 7 ימים לבקשה + ימים לבדיקת השחרור) לפני שמניחים שיש זמן.

---

## אחרי שהחנויות באוויר

- אם יש באפליקציה מנגנון "עדכון זמין" שמשווה מול מספר גרסה מרוחק — **לעדכן
  אותו רק עכשיו**, לא קודם. הוא מצהיר מה **חי בחנות**, לא מה קומפל.
- לוודא שהוא משווה מול המספר הנכון: מספר בילד פנימי ו-versionCode של Play
  יכולים להתפצל, וזו טעות שקטה.

---

## טבלת תקלות

| מה רואים | הסיבה |
|---|---|
| דף החנות 404 למרות "אושר" | אושר ב-Closed testing, מעולם לא קודם ל-Production |
| הכפתור "Apply for production access" אפור | אחד משלושת התנאים לא מולא. הקונסולה מראה איזה |
| המניין התאפס | מספר הבודקים ירד מתחת ל-12 |
| הבקשה נדחתה בלי הסבר ברור | לרוב תשובות כלליות מדי או טענה שסותרת נתון שלגוגל יש |
| השחרור נחסם על DSA | סומנו מדינות EU-27 בלי פרטי סוחר |
| הבדיקה נופלת על מדיניות פרטיות | הכתובת בליסטינג כבר לא נטענת |

---

## מה לדווח בסוף

תאריך האישור, מספר הגרסה שקודמה, ו**הטקסט המלא של כל הערה מגוגל, מילה במילה**.
אל תסכם שגיאות בניסוח שלך — הניסוח המדויק הוא מה שקובע מה צריך לתקן.
