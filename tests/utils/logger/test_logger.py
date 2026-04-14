from collections.abc import Generator

from vibra.utils import LogLevel, log


def test_log(
    capture_logs: Generator[list[str]], log_level: LogLevel, message: str
) -> None:
    log(message, log_level)
    logs = list(capture_logs)
    assert message in logs[0]
    assert log_level.name in logs[0]
