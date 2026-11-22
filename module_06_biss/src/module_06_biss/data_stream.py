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
        for value in values:
            self.items.append(str(value))


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
        for value in values:
            self.items.append(value)


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
        for value in values:
            if "log_level" in value and "log_message" in value:
                self.items.append(
                    f"{value['log_level']}: {value['log_message']}"
                )
            else:
                self.items.append(str(value))


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            for proc in self.processors:
                if proc.validate(data):
                    proc.ingest(data)
                    break
            else:
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
