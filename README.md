# Photo Sorter AI

A privacy-first Python tool for organizing photo libraries locally. It analyzes real image content, creates perceptual fingerprints for visual-similarity discovery, reads EXIF capture dates when available, and builds safe preview-first copy/move plans.

> **Why “AI”?** The project uses lightweight computer-vision-style perceptual hashing to compare visual structure. It does **not** claim to use a neural model or recognize people/objects.

## Why it exists
Large photo folders become difficult to browse, while cloud organizers may require uploads. Photo Sorter AI keeps processing on your computer and makes every destructive action explicit.

## Features
- JPEG, PNG, WebP, BMP and TIFF discovery.
- EXIF-aware orientation and `DateTimeOriginal` extraction with file-time fallback.
- Perceptual 64-bit image fingerprints and configurable similarity clustering.
- Organize by `YYYY-MM` capture date or portrait/landscape/square orientation.
- Preview is the default; `--apply` is required to write files.
- Copy by default; moving requires both `--apply --move`.
- SHA-256 source revalidation immediately before each operation.
- Copy verification, temporary-file writes, collision-safe names and JSON manifest.
- Hidden files and symlinks are excluded by default.
- Machine-readable JSON preview and a reusable Python API.

## Requirements & installation
Python 3.10+.

```bash
git clone https://github.com/rad03i2/photo-sorter-ai.git
cd photo-sorter-ai
python -m pip install -e .
```

For development: `python -m pip install -e ".[dev]"`.

## Usage
Preview organization by capture month:

```bash
photo-sorter ~/Pictures ./Sorted
```

Organize by orientation, then execute the safe copy:

```bash
photo-sorter ~/Pictures ./Sorted --mode orientation
photo-sorter ~/Pictures ./Sorted --mode orientation --apply --manifest run.json
```

Move originals only when intentionally requested:

```bash
photo-sorter ~/Pictures ./Sorted --apply --move --manifest move.json
```

Find visually similar groups:

```bash
photo-sorter ~/Pictures ./Sorted --similar --threshold 8
```

Use `--json` for a JSON plan, `--no-recursive` for only the top directory, and `--include-hidden` to include hidden paths.

### Python API
```python
from pathlib import Path
from photo_sorter_ai import analyze, cluster, discover

photos = [analyze(p) for p in discover(Path("Pictures"))]
similar_groups = cluster(photos, threshold=8)
```

## Preview guidance
This is a CLI application, so screenshots are optional. A useful project preview should show the preview output and the resulting `Sorted/YYYY-MM/` folders; never publish screenshots containing private photo thumbnails or personal paths.

## Configuration
No environment variables, accounts, API keys, network services or configuration files are required. CLI flags are the complete configuration surface.

## Project structure
```text
src/photo_sorter_ai/core.py   analysis, hashing, planning, execution
src/photo_sorter_ai/cli.py    command-line interface
src/photo_sorter_ai/__init__.py public API
tests/                        automated tests
.github/workflows/ci.yml      cross-platform CI
```

## Testing
```bash
ruff check .
pytest -q
```
Tests cover image analysis, discovery rules, perceptual clustering, collision handling, copy execution, manifests and changed-source protection.

## Security & privacy
Images never leave the local machine. The tool does not perform face recognition. Preview is non-writing; copy is the default action. `--move` deletes each source only after a byte-level SHA-256 verification of its completed copy. Review plans before applying them and keep independent backups of irreplaceable photos.

## Limitations
Perceptual hashing is a similarity heuristic, not semantic image understanding. A single global threshold cannot perfectly classify every edited/cropped image. EXIF dates may be missing or incorrect; filesystem modification time is then used. RAW camera formats and video are not supported. The current similarity clustering is greedy and intended for personal-sized collections rather than million-image indexes.

## Optional roadmap
Optional future work may include RAW metadata adapters, scalable nearest-neighbor indexing, user-approved semantic models, and an interactive desktop UI. These are not current features.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports should follow [SECURITY.md](SECURITY.md).

## License
MIT — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية — Photo Sorter AI

أداة Python محلية وتركّز على الخصوصية لتنظيم مكتبات الصور. تحلل محتوى الصور فعليًا، وتنشئ بصمة إدراكية لاكتشاف الصور المتشابهة بصريًا، وتقرأ تاريخ الالتقاط من EXIF عند توفره، ثم تبني خطة آمنة يمكن معاينتها قبل أي نسخ أو نقل.

> كلمة AI هنا تشير إلى أسلوب خفيف لتحليل التشابه البصري بواسطة **perceptual hashing**؛ المشروع لا يدّعي استخدام شبكة عصبية ولا يتعرف على الأشخاص أو الأشياء.

## لماذا المشروع؟
مجلدات الصور الكبيرة تصبح صعبة التصفح، وبعض الحلول السحابية تتطلب رفع الصور. هذا المشروع يبقي المعالجة على جهازك ويجعل العمليات التي قد تغير ملفاتك صريحة واختيارية.

## المزايا
- اكتشاف JPEG وPNG وWebP وBMP وTIFF.
- تصحيح اتجاه EXIF وقراءة `DateTimeOriginal` مع استخدام وقت تعديل الملف عند غياب التاريخ.
- بصمة بصرية 64-bit وتجميع الصور المتشابهة بعتبة قابلة للتعديل.
- تنظيم حسب شهر الالتقاط `YYYY-MM` أو حسب الاتجاه: أفقي/عمودي/مربع.
- المعاينة هي الوضع الافتراضي، ولا تُكتب الملفات إلا مع `--apply`.
- النسخ هو الافتراضي؛ النقل يحتاج `--apply --move` معًا.
- إعادة التحقق من SHA-256 للمصدر قبل التنفيذ والتحقق من النسخة بعد الكتابة.
- أسماء آمنة عند التعارض، كتابة مؤقتة وManifest بصيغة JSON.
- تجاهل الملفات المخفية والروابط الرمزية افتراضيًا.
- إخراج JSON وواجهة Python قابلة لإعادة الاستخدام.

## المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/photo-sorter-ai.git
cd photo-sorter-ai
python -m pip install -e .
```

للتطوير: `python -m pip install -e ".[dev]"`.

## الاستخدام
معاينة التنظيم حسب شهر الالتقاط:
```bash
photo-sorter ~/Pictures ./Sorted
```
التنظيم حسب الاتجاه ثم تنفيذ النسخ:
```bash
photo-sorter ~/Pictures ./Sorted --mode orientation
photo-sorter ~/Pictures ./Sorted --mode orientation --apply --manifest run.json
```
للبحث عن مجموعات متشابهة بصريًا:
```bash
photo-sorter ~/Pictures ./Sorted --similar --threshold 8
```
استخدم `--json` لخطة JSON و`--no-recursive` لمنع البحث داخل المجلدات الفرعية و`--include-hidden` لإدخال المسارات المخفية.

## الإعداد
لا يحتاج المشروع إلى حساب أو مفاتيح API أو إنترنت أو متغيرات بيئة. جميع الإعدادات متاحة عبر خيارات سطر الأوامر.

## بنية المشروع والاختبارات
المحرك في `src/photo_sorter_ai/core.py`، والواجهة في `cli.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`. للتأكد محليًا:
```bash
ruff check .
pytest -q
```
تغطي الاختبارات التحليل والاكتشاف والتشابه وتعارض الأسماء والتنفيذ والـManifest وحماية المصدر إذا تغير بعد المعاينة.

## الخصوصية والأمان
لا تُرفع الصور إلى أي خدمة، ولا يوجد تعرف على الوجوه. المعاينة لا تكتب ملفات، والنسخ هو الوضع الافتراضي. عند اختيار النقل لا يُحذف المصدر إلا بعد اكتمال النسخة والتحقق من SHA-256. راجع الخطة واحتفظ بنسخة احتياطية مستقلة للصور المهمة.

## القيود
البصمة الإدراكية أداة تشابه وليست فهمًا دلاليًا للصورة، وقد تحتاج العتبة إلى ضبط للصور المعدلة أو المقصوصة. قد تكون بيانات EXIF غائبة أو غير دقيقة. صيغ RAW والفيديو غير مدعومة حاليًا، والتجميع الحالي مناسب للمكتبات الشخصية وليس لفهارس بملايين الصور.

## تطوير اختياري مستقبلًا
يمكن مستقبلًا إضافة دعم metadata لملفات RAW وفهرسة تشابه واسعة النطاق ونماذج دلالية يوافق عليها المستخدم وواجهة سطح مكتب. هذه ليست مزايا حالية.

## المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) للأمان. المشروع مرخص برخصة MIT الموجودة في [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
