# Contributing / المساهمة

Thanks for improving Photo Sorter AI. Keep changes focused, privacy-preserving, and covered by tests.

1. Fork/branch from `main`.
2. Install `python -m pip install -e ".[dev]"`.
3. Run `ruff check .` and `pytest -q`.
4. Add tests for behavior changes and update both README language sections when user-facing behavior changes.
5. Open a focused pull request explaining the problem, solution, and validation.

Do not commit photos containing personal information, secrets, credentials, generated environments, or large binary fixtures. Create synthetic test images instead.

## العربية
نرحب بالمساهمات المركزة والآمنة. ثبّت اعتماديات التطوير، شغّل `ruff check .` و`pytest -q`، وأضف اختبارًا لأي تغيير سلوكي. عند تغيير سلوك المستخدم حدّث قسمي README الإنجليزي والعربي. لا ترفع صورًا شخصية أو أسرارًا أو ملفات بيئة مولدة؛ استخدم صور اختبار اصطناعية.

Author / المؤلف: Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2
