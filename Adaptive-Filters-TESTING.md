# Testing the Adaptive Noise-Cancellation Filters

## Purpose and scope

This test suite checks the numerical behavior of the `NLMS_filter` and `RLS_filter` functions in `Adaptive_filters.py`.

The automated tests currently cover deterministic NumPy inputs.

## Current expectations

| ID | Expected behavior |
|---|---|
| EXP-001 | A filter returns the same number of samples it receives. |
| EXP-002 | Valid deterministic inputs produce only finite output values. |
| EXP-003 | Zero reference noise leaves the mixed signal unchanged. |
| EXP-004 | A controlled correlated-noise example has lower mean squared error after filtering. |
| EXP-005 | NLMS does not modify the caller's input arrays. |


## Main risks

| Risk | Possible failure | Impact | Test evidence |
|---|---|---|---|
| RISK-001 | A filter changes the output length | Downstream processing may fail | EXP-001 |
| RISK-002 | Numerical instability produces NaN or infinity | Output becomes unusable | EXP-002 |
| RISK-003 | Filtering changes a signal when no reference noise exists | Signal may be unnecessarily distorted | EXP-003 |
| RISK-004 | Filtering increases rather than reduces controlled correlated noise | The primary function is not achieved | EXP-004 regression cases |
| RISK-005 | A function unexpectedly changes its inputs | Other code may receive corrupted data | EXP-005 regression case |

## Test approach

- Tests call the filter functions directly, so they are unit tests.
- Fixed mathematical signals are used instead of random data, making results reproducible locally and in CI.
- Pytest fixtures share representative signal data without sharing mutable test state.
- Parametrization applies the same behavioral expectations to NLMS and RLS without duplicating test code.
- Controlled noise reduction is marked for regression because it protects the filters' primary behavior under a repeatable reference scenario.
- The NLMS input-mutation check is marked for regression because it protects an important interface guarantee from future changes.
- Approximate array comparisons use NumPy's testing helpers rather than exact floating-point equality.

## Risk-based regression selection

The regression subset contains the cases with the clearest combination of impact and repeatability:

- RISK-004: a change must not cause NLMS or RLS to stop reducing the controlled correlated noise. Parametrization produces one regression case for each filter.
- RISK-005: NLMS must not introduce an unexpected side effect by modifying caller-owned input arrays.

The remaining unit cases still provide regression protection whenever the full suite runs, but they are not part of the explicitly marked, risk-prioritized subset. New cases should be added to that subset when a genuine defect is fixed or a newly identified risk justifies permanent protection.

## Automated tests

| Test function | Executed cases | Purpose |
|---|---:|---|
| `test_filter_preserves_signal_length` | 2 | Checks EXP-001 for NLMS and RLS |
| `test_filter_returns_only_finite_values` | 2 | Checks EXP-002 for NLMS and RLS |
| `test_zero_reference_noise_does_not_change_signal` | 2 | Checks EXP-003 for NLMS and RLS |
| `test_filter_reduces_controlled_correlated_noise` | 2 | Checks EXP-004 for NLMS and RLS as regression cases |
| `test_nlms_does_not_modify_its_input_arrays` | 1 | Checks EXP-005 as a regression case |

## Continuous integration

The GitHub Actions workflow runs for pushes and pull requests. It creates a clean Ubuntu environment, installs Python 3.12 and `requirements.txt`, selects a non-interactive Matplotlib backend, then runs Pytest with terminal coverage, XML coverage, and JUnit output.

This provides repeatable feedback when the implementation or tests change. A failed workflow blocks the claim that the repository's automated checks pass, but it does not prove that every real-world noise-cancellation scenario works.

## Current verified result

Local verification on 2026-09-05 produced:

- 9 of 9 executed test cases passed.
- The marked regression subset passed 3 cases: controlled noise reduction with NLMS, controlled noise reduction with RLS, and NLMS input integrity.
- Measured line/branch coverage for `Adaptive_filters.py`: 64.29%.
- The untested lines are primarily the performance-reporting and plotting helpers.

## Next steps

The current suite does not cover:

- Empty, differently sized, non-numeric, NaN, or infinite input arrays.
- Invalid `order`, `mu`, `forget_fact`, or `epsilon` values.
- Multiple noise types and signal-to-noise ratios.
- Long-running numerical stability or execution time.
- Recorded audio, microphones, room acoustics, or real-time constraints.
- `show_performance_metrics`, `plot`, or the complete `LMS_main.py` demonstration.
