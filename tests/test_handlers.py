from reports.handlers import HandlersReport

def test_handlers_report_output(capsys):
    data = {
        "/test/": {"INFO": 2, "ERROR": 1},
        "__total__": {"requests": 3}
    }
    report = HandlersReport()
    report.generate(data)
    captured = capsys.readouterr()
    assert "Total requests: 3" in captured.out
    assert "/test/" in captured.out
    assert "2" in captured.out and "1" in captured.out
