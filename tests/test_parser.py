
from log_parser import parse_log_file

def test_parse_log_file(tmp_path):
    log_content = """
    [INFO] django.request "GET /api/v1/orders/"
    [ERROR] django.request "GET /api/v1/orders/"
    [DEBUG] django.request "GET /admin/dashboard/"
    """
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content)

    result = parse_log_file(str(log_file))
    assert result["/api/v1/orders/"]["INFO"] == 1
    assert result["/api/v1/orders/"]["ERROR"] == 1
    assert result["/api/v1/orders/"]["DEBUG"] == 0  # DEBUG отсутствует, значит 0
    assert result["/api/v1/orders/"]["WARNING"] == 0  # WARNING отсутствует, значит 0
    assert result["/api/v1/orders/"]["CRITICAL"] == 0  # CRITICAL отсутствует, значит 0

    assert result["/admin/dashboard/"]["DEBUG"] == 1
    assert result["/admin/dashboard/"]["INFO"] == 0  # INFO отсутствует
    assert result["/admin/dashboard/"]["ERROR"] == 0  # ERROR отсутствует
    assert result["/admin/dashboard/"]["WARNING"] == 0  # WARNING отсутствует
    assert result["/admin/dashboard/"]["CRITICAL"] == 0  # CRITICAL отсутствует

    assert result["__total__"]["requests"] == 3
