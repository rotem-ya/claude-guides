# token-kit: פחות טוקנים, פחות זמן, אותה איכות

**זו שיטת העבודה בכל הריפואים מעכשיו (רותם, 15.10.2026).** התיקייה הזו היא Skill (`SKILL.md`) וגם הכלים שהוא מתקין.

ערכה אחת לכל פרויקט, חדש או קיים. היא גורמת לסשן של Claude Code למצוא את הקוד שהוא צריך בלי לקרוא קבצים שלמים, להתחיל לעבוד בלי שלב התקנה, ולעבוד בסשנים קצרים.

## למה

נמדד ב-15.10.2026 על פרויקט גדול: סשן אחד רץ 22 שעות וההקשר שלו הגיע ל-733 אלף טוקנים. כ-70% מהעלות הלכו על קריאה חוזרת של אותו הקשר בכל תור. כל פלט שנכנס לשיחה נקרא שוב בכל תור עד סוף הסשן. לכן החיסכון הגדול מגיע משני דברים: סשנים קצרים, וכל קריאה קטנה ככל האפשר.

## מה בפנים

| קובץ | מה הוא עושה |
|---|---|
| `SKILL.md` | הסקיל: השיטה, ומה לעשות בריפו שאין בו עדיין את הערכה (להתקין). |
| `codemap.py` (+ `codemap_ts.cjs`) | מפת קוד שנוצרת אוטומטית (שנייה בערך). `docs/codemap/INDEX.md` עם שורה לכל אזור, ומפה לכל אזור: כל פונקציה, מחלקה וטיפוס עם טווח השורות שלה והבדיקות שמייבאות את הקובץ. `find <regex>` ו-`outline <file>` עונים על "איפה X" בשורה אחת. Python (ast, מדויק), TypeScript/JavaScript (המפענח של TypeScript כשהוא מותקן בפרויקט, אחרת התאמת סוגריים), Dart. |
| `session-start.sh` | Hook שרץ בתחילת כל סשן ענן: מתקין תלויות (pip, npm/pnpm/yarn לפי ה-lockfile, בלי לשנות אותו, flutter pub get) ובונה את המפה. מדפיס שורה אחת בלבד. פרויקט עם צרכים מיוחדים שם אותם ב-`.claude/hooks/setup.sh`. |
| `RULES.md` | בלוק הכללים שנכנס ל-`CLAUDE.md` של כל פרויקט (בין הסימונים `token-kit:start` / `token-kit:end`). |
| `AGENTS_BLOCK.md` | אותו דבר בקצרה ל-`AGENTS.md`, שאותו קוראים Codex, Cursor, Copilot, Gemini וכלים אחרים. |
| `install.py` | מתקין או מעדכן הכול בפרויקט. אפשר להריץ שוב ושוב. |
| `package.py` | בונה את `dist/token-kit.zip` להעלאה לחשבון. |
| `test_codemap.py` | הבדיקות של הערכה: `python3 -m pytest -q token-kit`. |

## איך זה מגיע לכל סשן, חשבון וכלי

| מי | איך הוא מקבל את השיטה |
|---|---|
| כל סשן Claude Code, מכל חשבון, שפותח ריפו מותקן | הסקיל בתוך הריפו (`.claude/skills/token-kit/`), ה-hook (`.claude/settings.json`) והכללים ב-`CLAUDE.md`. אין צורך בשום פעולה. |
| מחשב מקומי שפתח ריפו מותקן | ה-hook מעתיק את הסקיל ל-`~/.claude/skills/token-kit/`, כך שהוא זמין גם בפרויקטים חדשים במחשב הזה. |
| חשבון claude.ai (כולל סשני ענן בפרויקט חדש) | מעלים פעם אחת לכל חשבון את `dist/token-kit.zip`: Customize ← Skills ← Upload. מאז כל סשן של החשבון מכיר את השיטה, ובריפו חדש הוא מתקין אותה. |
| Codex, Cursor, Copilot, Gemini וכו' | `AGENTS.md` בריפו: אותם כללים, ו"להריץ `python3 tools/codemap.py` קודם" (אין להם hook). |

## התקנה בפרויקט (קיים או חדש)

אומרים לקלוד: **"תתקין token-kit מ-claude-guides"**. הוא עושה:

```bash
# אם claude-guides לא בסשן: add_repo owner=rotem-ya repo=claude-guides
python3 /path/to/claude-guides/token-kit/install.py /path/to/project
# בודק, ואז commit + push
```

`install.py` מעתיק את הסקיל ל-`.claude/skills/token-kit/`, יוצר את `tools/codemap.py` (מפעיל את העותק שבסקיל), מוסיף את ה-hook ל-`.claude/`, מוסיף את `docs/codemap/` ל-`.gitignore`, כותב את בלוק הכללים ל-`CLAUDE.md` ול-`AGENTS.md` (ויוצר אותם אם אין), ובונה את המפה פעם אחת. hook שהפרויקט כתב בעצמו לא נדרס; הסקריפט אומר מה להוסיף.

בפרויקט חדש: אחרי ההתקנה מוסיפים ל-`CLAUDE.md` מעל הבלוק כמה שורות: מה הפרויקט, מאיפה מתחילים לקרוא, והפקודות (בדיקות, lint, build).

## עדכון

משנים את הקבצים כאן (וגם את הבדיקות), מעלים את `VERSION` ב-`codemap.py`, מריצים `python3 token-kit/package.py`, ואז `install.py` שוב בכל פרויקט (וה-zip מחדש בחשבונות). בלוק הכללים מוחלף במקום, לא משוכפל.

## התאמה

- `.codemap.json` בשורש הפרויקט: `{"exclude": ["glob", ...], "include": ["glob", ...]}`. ברירת המחדל מדלגת על בדיקות (הן ממופות לפי מה שהן מייבאות), `node_modules`, `dist`, `build`, `static`, `migrations`, קבצי `.d.ts` ותיקיות הפלטפורמה של Flutter.
- `CODEMAP_OUT=<dir>` כותב את המפה לתיקייה אחרת.

## איפה זה מותקן

| פרויקט | הערה |
|---|---|
| `rotem-ya/Law-Manager`, `rotem-ya/procurement`, `rotem-ya/asmade`, `rotem-ya/Sketch2CAD` | ההתקנה הרגילה (15.10.2026) |
| `rotem-ya/Mida` | ההתקנה הרגילה, עם `.codemap.json` שמדלג על `docs/` (15.10.2026 החליפה את `tools/codemap.cjs`) |
