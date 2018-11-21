# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np

from cirq import protocols, ops, line, circuits


def assert_decompose_is_consistent_with_unitary(val: Any):
    """Uses `val._unitary_` to check `val._phase_by_`'s behavior."""

    expected = protocols.unitary(val)
    qubit_count = len(expected).bit_length() - 1
    if isinstance(val, ops.Operation):
        qubits = val.qubits
        dec = protocols.decompose_once(val, default=None)
    else:
        qubits = tuple(line.LineQubit.range(qubit_count))
        dec = protocols.decompose_once_with_qubits(val, qubits, default=None)
    if dec is None:
        # If there's no decomposition, it's vacuously consistent.
        return

    actual = circuits.Circuit.from_ops(dec).to_unitary_matrix(
        qubit_order=qubits)

    assert np.allclose(actual, expected, atol=1e-8)