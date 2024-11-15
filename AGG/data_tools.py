"""
    Copyright (C) 2023, Christopher Paul Ley
    Asynchronous Graph Generator

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np


def random_index(data_len: int, sparsity: float):
    idx = np.arange(0, data_len)
    subset_size = int(np.floor(data_len) * sparsity)
    np.random.shuffle(idx)
    removed = idx[:subset_size]
    remainder = idx[subset_size:]
    removed.sort()
    remainder.sort()
    return removed, remainder
