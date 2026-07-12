# מזהים גלובליים — לא סודות

מזהים שחוזרים בין כמה מהאפליקציות שלי, לא ספציפיים לפרויקט אחד. הכלל: **רק דברים שאם ידלפו לא מאפשרים למישהו להתחזות, לחתום, או לגשת בשם החשבון**. שם חשבון, Team ID, כתובת מייל, מוסכמת שמות — כן. מפתח API, קובץ `.p8`, סיסמת keystore, JSON של service account — לא, לעולם לא כאן (ראה `SECRETS_POINTER.md`).

**כל צ'ט קלוד קוד שמגלה מזהה גלובלי אמיתי (לא רק לפרויקט הנוכחי) — מוסיף אותו כאן.** אם לא בטוחים ב-100% שהערך נכון/עדיין בתוקף, מסמנים "לא מאומת" ולא מוחקים את הצורך לבדוק.

## חשבונות
- **GitHub:** `rotem-ya` (github.com/rotem-ya)
- **Google / Firebase — כתובת חשבון הבעלים:** `rot4735@gmail.com`. לא מאומת שזו כתובת הבעלים המדויקת בכל פרויקט Firebase בודד — יש לוודא ב-console.firebase.google.com → Project settings → Users and permissions לפני שמסתמכים על זה במשימת IAM.
- **Apple Developer Team ID:** מועמד לא-מאומת `3X9M84JZD7` (עלה פעם אחת בבדיקת הגדרת APNs, מעולם לא אושר בכתב). **לוודא** ב-[developer.apple.com/account](https://developer.apple.com/account) → Membership לפני כל שימוש בפועל (secrets, provisioning וכו').
- **אימייל תמיכה/פרטיות משותף:** `askthekids.app@gmail.com` — בפועל משמש גם את WhoIsThere ולא רק את משפחת "ask the kids" (askthekids-hebrew/english/editor), כנראה תיבת תמיכה כללית לכמה אפליקציות. לפני שמשתמשים בו באפליקציה חדשה — לוודא מול רותם שזו עדיין הכוונה, לא סתם שנשאר מהעתקה.

## מוסכמות
- **Bundle ID / Application ID:** בדרך כלל `com.rotem.<appname>`. שימו לב: ב-WhoIsThere אנדרואיד ו-iOS לא זהים בטעות היסטורית (`com.whoisthere.app` מול `com.rotem.whoisthere`) — בפרויקט חדש עדיף לשמור על אותו מזהה בשתי הפלטפורמות (ראה `firebase-auth/FIREBASE_AUTH_SETUP_GUIDE.md`).
- **ענף פיתוח יחיד מאוחד** לכל פרויקט (לא ריבוי ענפים מקבילים) — דפוס עבודה שחזר על עצמו וחסך בלבול, ראה CLAUDE.md של WhoIsThere.

## מה עדיין לא כאן
זה מסמך שמתחיל קטן ומתמלא עם הזמן. דברים סבירים שיתווספו כשיתגלו/יאומתו: מזהה מפרסם AdMob (אם משותף בין אפליקציות), חשבון Codemagic, ספק דומיין/DNS אם קיים אחד משותף.
