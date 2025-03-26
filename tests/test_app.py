"""Basic test module for demonstration."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_basic_addition() -> None:
    """
    Test that basic addition works correctly.
    
    This is a simple test to verify that 1 + 1 equals 2.
    """
    result = 1 + 1
    assert result == 2 