import numpy as np
import pytest

from Adaptive_filters import NLMS_filter, RLS_filter


@pytest.fixture
def signals():
    reference_noise = np.sin(np.linspace(0, 4 * np.pi, 100))
    clean_signal = np.cos(np.linspace(0, 2 * np.pi, 100))
    mixed_signal = clean_signal + reference_noise

    return reference_noise, clean_signal, mixed_signal


@pytest.mark.parametrize("filter_function", [NLMS_filter, RLS_filter])
def test_filter_preserves_signal_length(filter_function, signals):
    noise, _, mixed = signals

    result = filter_function(noise, mixed, order=2)

    assert len(result) == len(mixed)


@pytest.mark.parametrize("filter_function", [NLMS_filter, RLS_filter])
def test_filter_returns_only_finite_values(filter_function, signals):
    noise, _, mixed = signals

    result = filter_function(noise, mixed, order=2)

    assert np.all(np.isfinite(result))


@pytest.mark.parametrize("filter_function", [NLMS_filter, RLS_filter])
def test_zero_reference_noise_does_not_change_signal(filter_function):
    mixed = np.array([1.0, 2.0, 3.0, 4.0])
    noise = np.zeros_like(mixed)

    result = filter_function(noise, mixed, order=2)

    np.testing.assert_allclose(result, mixed)


@pytest.mark.regression
def test_nlms_does_not_modify_its_input_arrays(signals):
    noise, _, mixed = signals
    original_noise = noise.copy()
    original_mixed = mixed.copy()

    NLMS_filter(noise, mixed, order=2)

    np.testing.assert_array_equal(noise, original_noise)
    np.testing.assert_array_equal(mixed, original_mixed)


@pytest.mark.regression
@pytest.mark.parametrize(
    ("filter_function", "arguments"),
    [
        (NLMS_filter, {"mu": 0.2, "order": 4}),
        (RLS_filter, {"forget_fact": 0.99, "order": 4}),
    ],
)
def test_filter_reduces_controlled_correlated_noise(
    filter_function,
    arguments,
):
    sample_numbers = np.arange(500)

    clean_signal = np.sin(2 * np.pi * 0.01 * sample_numbers)
    reference_noise = 0.5 * np.sin(
        2 * np.pi * 0.10 * sample_numbers
    )
    mixed_signal = clean_signal + reference_noise

    filtered_signal = filter_function(
        reference_noise,
        mixed_signal,
        **arguments,
    )

    error_before = np.mean(
        (mixed_signal - clean_signal) ** 2
    )
    error_after = np.mean(
        (filtered_signal - clean_signal) ** 2
    )

    assert error_after < error_before