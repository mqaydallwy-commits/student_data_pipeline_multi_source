# Multi-Source Data Pipeline

مشروع Pipeline بسيط يقرأ البيانات من أربعة مصادر، ينظفها، يفحص جودتها، ثم يخزن المخرجات النهائية في MongoDB داخل Collections منفصلة.

## Sources

1. API: `https://dummyjson.com/products`
2. MongoDB: `mongodb://localhost:27017/`
   - Database: `university_ai`
   - Collection: `students`
3. CSV: `data/raw/tudents.csv`
4. PostgreSQL:
   - Database: `PostgreSQL`
   - Table: `students`

## Output Collections in MongoDB

داخل قاعدة البيانات `university_ai`:

- `api_products_clean`
- `mongodb_students_clean`
- `csv_students_clean`
- `postgresql_students_clean`

## Cleaning

- حذف الصفوف المكررة تماماً.
- تحويل الأعمدة الرقمية المعروفة إلى أرقام.
- القيم الرقمية المفقودة/غير الصالحة تعالج بالوسيط Median.
- القيم النصية المفقودة تعالج بالـ Mode.
- GPA خارج 0 إلى 4 يستبدل بوسيط GPA الصحيح.
- Age خارج 16 إلى 80 يستبدل بوسيط العمر الصحيح.
- Price السالب يعالج بوسيط الأسعار الصحيحة.
- Rating خارج 0 إلى 5 يعالج بوسيط القيم الصحيحة.
- الصف لا يحذف إلا إذا بقي يحتوي قيمة لا يمكن إصلاحها بعد المعالجة.

## قبل التشغيل

شغّل MongoDB وPostgreSQL محلياً.

افتح `src/config.py` وعدّل كلمة مرور PostgreSQL:

```python
"password": "CHANGE_ME"
```

وإذا كان username أو port مختلفاً، عدله في نفس الملف.

## Install

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Flow

Source -> Extract -> Transform -> Quality -> Load to MongoDB
