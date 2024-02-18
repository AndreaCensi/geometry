import numpy as np

__all__ = [
    "assert_allclose",
    "check_allclose",
]

try:
    from numpy.testing import assert_allclose
except ImportError:

    def assert_allclose(actual, desired, rtol=1e-7, atol=0, err_msg="", verbose=True):
        """Backporting assert_allclose from Numpy 1.5 to 1.4"""
        from numpy.testing import assert_array_compare

        def compare(x, y):
            return np.allclose(x, y, rtol=rtol, atol=atol)

        actual, desired = np.asanyarray(actual), np.asanyarray(desired)
        header = "Not equal to tolerance rtol=%g, atol=%g" % (rtol, atol)
        assert_array_compare(compare, actual, desired, err_msg=str(err_msg), verbose=verbose, header=header)


def check_allclose(actual, desired, rtol: float = 1e-7, atol: float = 0, err_msg: str = "", verbose: bool = True) -> None:
    if not np.allclose(actual, desired, rtol=rtol, atol=atol):
        err_msg += "\n%s != %s " % (actual, desired)
        raise Exception(err_msg)
