from typing import List, Dict
from collections import defaultdict


def merge_results(results: List[Dict]) -> Dict:
    merged = defaultdict(lambda: defaultdict(int))

    for res in results:
        for handler, levels in res.items():
            for level, count in levels.items():
                merged[handler][level] += count

    return merged
