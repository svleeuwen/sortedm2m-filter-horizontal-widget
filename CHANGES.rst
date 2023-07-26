Changelog
=========
2.0.1
 - Remove margin that has side effects with default fk selector
 - Cleanup of unneeded compatibility code

2.0.0
 - Support for Django 3.5<
 - Add DEFAULT_AUTO_FIELD settings
 - Replace README with markdown version
 - Replace setup.py with pyproject.toml using poetry
 - Fix margin
 - Remove lib dir in example project. Should be installed manually.
 - Add .idea to gitignore

1.3.2:
 - Fix incorrect class name

1.3.1:
 - Fix duplicate "Add another" button in stacked inline (#12)

1.3:
 - Handle responsive css introduced in django 2.0
 - Handle removal of old JS cross-browser utilities introduced in django 2.0

1.2.1:
 - Add workaround to have verbose_name reference (#1)
 - Fix Select and Clear All button (#2)
 - Fix translation for Clear All button (#3)

1.2:
 - Implement new admin style introduced in Django 1.9
 - Remove all images since buttons are now handled with css
 - Get button active and hover states working
 - Add example project

1.1:
 - Use admin_prefix to find image, in case user changes STATIC_URL setting
 - Add version requirements per Django version

1.0:
 - Fixed bugs with popup closing.
 - Added support for Django 1.10+
