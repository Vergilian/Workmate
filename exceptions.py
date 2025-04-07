class LogAnalyzerError(Exception):
    """Базовый класс исключений для лог-анализатора."""
    pass


class InvalidReportNameError(LogAnalyzerError):
    def __init__(self, report_name: str):
        super().__init__(f"Report '{report_name}' is not a valid report.")


class FileNotFoundError(LogAnalyzerError):
    def __init__(self, path: str):
        super().__init__(f"File '{path}' does not exist.")
