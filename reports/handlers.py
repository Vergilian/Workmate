from reports.base import Report
from typing import Dict
from collections import defaultdict

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class HandlersReport(Report):
    def generate(self, data: Dict) -> None:
        print(f"\nTotal requests: {data.get('__total__', {}).get('requests', 0)}\n")

        handlers = [h for h in data.keys() if h != "__total__"]
        handlers.sort()

        header = f"{'HANDLER':<24}" + "".join(f"{lvl:<8}" for lvl in LEVELS)
        print(header)

        totals = defaultdict(int)

        for handler in handlers:
            row = f"{handler:<24}"
            for lvl in LEVELS:
                count = data[handler].get(lvl, 0)
                totals[lvl] += count
                row += f"{count:<8}"
            print(row)

        total_row = " " * 24 + "".join(f"{totals[lvl]:<8}" for lvl in LEVELS)
        print(total_row)
