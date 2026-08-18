# Locales

NanoMD Designer uses Qt Linguist for internationalization.

Workflow:

```bash
# extract strings
pyside6-lupdate src/nanomd -ts src/nanomd/locales/nanomd_zh_CN.ts src/nanomd/locales/nanomd_en.ts
# translate the .ts files (Qt Linguist), then release
pyside6-lrelease src/nanomd/locales/*.ts
```

The app follows the Windows display language by default and allows switching
between 中文 / English at runtime.
