"""M0 smoke tests: all core subpackages import cleanly."""


def test_core_imports() -> None:
    import nanomd.core.analysis  # noqa: F401
    import nanomd.core.builders  # noqa: F401
    import nanomd.core.forcefields  # noqa: F401
    import nanomd.core.models  # noqa: F401
    import nanomd.core.project  # noqa: F401
    import nanomd.core.scan  # noqa: F401
    import nanomd.core.validator  # noqa: F401
    import nanomd.core.writers  # noqa: F401
    import nanomd.core.wsl_bridge  # noqa: F401
    import nanomd.gui  # noqa: F401


def test_version() -> None:
    from nanomd import __version__

    assert __version__ == "0.1.0"
