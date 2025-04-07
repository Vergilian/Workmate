import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor  # Используем только ThreadPoolExecutor
from reports import get_report
from log_parser import parse_log_file
from utils import merge_results
from exceptions import InvalidReportNameError, FileNotFoundError, LogAnalyzerError


def validate_files(file_paths: list[str]) -> None:
    for path in file_paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)


def main():
    parser = argparse.ArgumentParser(description="Analyze Django logs.")
    parser.add_argument("logs", nargs="+", help="Paths to log files")
    parser.add_argument("--report", required=True, help="Name of the report to generate")
    args = parser.parse_args()

    try:
        validate_files(args.logs)

        report = get_report(args.report)
        if not report:
            raise InvalidReportNameError(args.report)

        # Обработка с использованием ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            parsed_logs = list(executor.map(parse_log_file, args.logs))

        # Объединение данных и генерация отчёта
        merged_data = merge_results(parsed_logs)
        report.generate(merged_data)

    except LogAnalyzerError as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()


