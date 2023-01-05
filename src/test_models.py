"""Test models.py."""

from pydantic import ValidationError
import pytest

from models import Risks


class TestRisksValidation:  # pylint: disable=too-few-public-methods
    """Check the validators of Risks."""

    class TestIsFocOrAlert:  # pylint: disable=too-few-public-methods
        """Test the check_is_foc_or_alert validator."""

        def test_is_foc(self):
            """Check it can be instantiated if is of kind 'foc'."""
            Risks(risks=["foc|others"])

        def test_is_alert(self):
            """Check it can be instantiated if is of kind 'alert'."""
            Risks(risks=["alert|others"])

        def test_no_foc_or_alert(self):
            """Check it fails if kind not in ['foc', 'alert']."""
            with pytest.raises(ValidationError):
                Risks(risks=["test|others"])
