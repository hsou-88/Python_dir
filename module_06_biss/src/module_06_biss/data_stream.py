from typing import Any
from abc import ABC, abstractmethod


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


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    print("Registering Numeric Processor")
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
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
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Registering other data processors")
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        numeric.output()
    for _ in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
