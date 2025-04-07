
from reports.handlers import HandlersReport
from exceptions import InvalidReportNameError

REPORTS = {
    "handlers": HandlersReport
}


def get_report(name: str):
    report_class = REPORTS.get(name.lower())
    if not report_class:
        raise InvalidReportNameError(name)
    return report_class()
