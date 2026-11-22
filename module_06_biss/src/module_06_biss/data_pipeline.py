from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.items: list[str] = []
        self.index: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        try:
            item = self.items.pop(0)
        except IndexError:
            raise IndexError("NO Data in the Processor") from None
        index_pop = self.index
        self.index += 1
        return (index_pop, item)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return isinstance(data, (int, float)) and not isinstance(data, bool)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        values = data if isinstance(data, list) else [data]
        converted = [str(value) for value in values]
        self.items.extend(converted)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(item, str)
                for item in data
            )
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Non Text data")
        values = data if isinstance(data, list) else [data]
        self.items.extend(values)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and self.validate(item)
                for item in data
            )
        return isinstance(data, dict) and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in data.items()
        )

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        if not self.validate(data):
            raise ValueError("Non Dict data")
        values = data if isinstance(data, list) else [data]
        converted: list[str] = []
        for value in values:
            if "log_level" in value and "log_message" in value:
                converted.append(
                    f"{value['log_level']}: {value['log_message']}"
                )
            else:
                converted.append(str(value))
        self.items.extend(converted)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


def require_export_data(value: object) -> list[tuple[int, str]]:
    if not isinstance(value, list):
        raise TypeError("Export data must be a list")
    checked: list[tuple[int, str]] = []
    ranks: set[int] = set()
    for entry in value:
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise TypeError("Each export entry must be a (rank, value) tuple")
        rank, text = entry
        if not isinstance(rank, int) or isinstance(rank, bool):
            raise TypeError("Export ranks must be integers")
        if rank < 0:
            raise ValueError("Export ranks must not be negative")
        if not isinstance(text, str):
            raise TypeError("Export values must be strings")
        if rank in ranks:
            raise ValueError("Export ranks must be unique")
        ranks.add(rank)
        checked.append((rank, text))
    return checked


def require_output_count(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("Output count must be an integer")
    if value < 0:
        raise ValueError("Output count must not be negative")
    return value


def require_export_plugin(value: object) -> None:
    if not callable(getattr(value, "process_output", None)):
        raise TypeError("Export plugin must provide process_output()")


class PipelineExportError(RuntimeError):
    pass


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields: list[str] = []
        for _, value in require_export_data(data):
            if any(char in value for char in ',"\r\n'):
                value = '"' + value.replace('"', '""') + '"'
            fields.append(value)
        print("CSV Output:")
        print(",".join(fields))


class JSONExportPlugin:
    def escape_string(self, value: str) -> str:
        escaped: list[str] = []
        for char in value:
            if char == '"':
                escaped.append('\\"')
            elif char == "\\":
                escaped.append("\\\\")
            elif ord(char) < 32 or 0xD800 <= ord(char) <= 0xDFFF:
                escaped.append(f"\\u{ord(char):04x}")
            else:
                escaped.append(char)
        return '"' + "".join(escaped) + '"'

    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields = [
            f'{self.escape_string(f"item_{rank}")}: '
            f'{self.escape_string(value)}'
            for rank, value in require_export_data(data)
        ]
        print("JSON Output:")
        print("{" + ", ".join(fields) + "}")


def require_processor(value: object) -> DataProcessor:
    if not isinstance(value, DataProcessor):
        raise TypeError("Expected a DataProcessor instance")
    items = getattr(value, "items", None)
    index = getattr(value, "index", None)
    if not isinstance(items, list) or not all(
        isinstance(item, str) for item in items
    ):
        raise ValueError("Processor must have a list of string items")
    if not isinstance(index, int) or isinstance(index, bool) or index < 0:
        raise ValueError("Processor rank must be a non-negative integer")
    return value


def require_stream(value: object) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError("The stream must be a list")
    return value


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        checked = require_processor(proc)
        if any(registered is checked for registered in self.processors):
            raise ValueError("Processor is already registered")
        self.processors.append(checked)

    def process_stream(self, stream: list[Any]) -> None:
        for data in require_stream(stream):
            handled = False
            for proc in self.processors:
                saved_items = proc.items.copy()
                saved_index = proc.index
                try:
                    if proc.validate(data):
                        proc.ingest(data)
                        handled = True
                        break
                except Exception as error:
                    proc.items[:] = saved_items
                    proc.index = saved_index
                    print(
                        f"DataStream processor error: "
                        f"{type(error).__name__}: {error}"
                    )
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{data}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            remaining = len(proc.items)
            total = proc.index + remaining
            name = type(proc).__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        limit = require_output_count(nb)
        require_export_plugin(plugin)
        for proc in self.processors:
            saved_items = proc.items.copy()
            saved_index = proc.index
            try:
                count = min(limit, len(proc.items))
                data = [proc.output() for _ in range(count)]
                plugin.process_output(data)
            except Exception as error:
                proc.items[:] = saved_items
                proc.index = saved_index
                raise PipelineExportError(
                    f"Export failed for {type(proc).__name__}; "
                    "processor data and rank were restored"
                ) from error


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    first_batch: list[Any] = [
        "Hello world", [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42, ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()
    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21, ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168], "World hello",
    ]
    print(f"Send another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()
    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
