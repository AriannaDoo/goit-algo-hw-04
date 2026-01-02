from __future__ import annotations

import random
import timeit
from sorts import merge_sort, insertion_sort


def build_datasets(n: int, seed: int = 42) -> dict[str, list[int]]:
    rng = random.Random(seed)

    random_list = [rng.randint(-10**6, 10**6) for _ in range(n)]
    sorted_list = sorted(random_list)
    reversed_list = sorted_list[::-1]

    # майже відсортований: зробимо кілька випадкових свапів
    nearly_sorted = sorted_list[:]
    swaps = max(1, n // 100)  # ~1% перестановок
    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]

    return {
        "random": random_list,
        "sorted": sorted_list,
        "reversed": reversed_list,
        "nearly_sorted": nearly_sorted,
    }


def time_algorithm(name: str, func, data: list[int], repeats: int = 5) -> float:
    # timeit: кожен запуск отримає нову копію data (щоб не мутувати)
    timer = timeit.Timer(lambda: func(data[:]))
    total = min(timer.repeat(repeat=repeats, number=1))
    return total


def main() -> None:
    print("Benchmark: insertion_sort vs merge_sort vs timsort (sorted)")
    sizes = [100, 1000, 5000]  # можна змінити (але insertion_sort на 50k буде боляче)

    algorithms = {
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "timsort(sorted)": lambda a: sorted(a),
    }

    for n in sizes:
        print(f"\n=== N = {n} ===")
        datasets = build_datasets(n)

        # sanity check на одному наборі
        sample = datasets["random"]
        ref = sorted(sample)
        assert insertion_sort(sample) == ref
        assert merge_sort(sample) == ref

        for ds_name, ds in datasets.items():
            print(f"\nDataset: {ds_name}")
            for alg_name, alg in algorithms.items():
                t = time_algorithm(alg_name, alg, ds, repeats=5)
                print(f"{alg_name:16} -> {t:.6f} sec")


if __name__ == "__main__":
    main()
