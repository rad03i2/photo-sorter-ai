# Security Policy / سياسة الأمان

## Supported version
The latest `main` branch is supported.

## Reporting
Please report security concerns privately through GitHub's repository security reporting features when available. Do not publish sensitive exploit details in a public issue.

## Security model
Photo Sorter AI is local-only and requires no network access, credentials, or API keys. It excludes symlinks by default, previews before writing, re-hashes sources before execution, verifies copied bytes, and requires explicit `--move` before deleting originals. These controls reduce risk but are not a substitute for backups.

Never process untrusted images with an outdated Pillow version. Keep dependencies updated and review a plan before applying it.

## العربية
يعمل المشروع محليًا ولا يحتاج شبكة أو بيانات دخول أو مفاتيح API. يتجاهل الروابط الرمزية افتراضيًا، ويعرض معاينة قبل الكتابة، ويعيد حساب بصمة المصدر قبل التنفيذ ويتحقق من النسخة، ولا يحذف الأصل إلا عند طلب `--move` صراحةً. هذه الحماية لا تغني عن النسخ الاحتياطي.

أبلغ عن الثغرات بصورة خاصة عبر ميزات الأمان في GitHub عند توفرها، ولا تنشر تفاصيل حساسة في Issue عامة.
