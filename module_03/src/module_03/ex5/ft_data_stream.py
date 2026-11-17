import random
import typing


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    players = ["alice", "bob", "charlie", "dylan"]

    actions = [
        "run",
        "eat",
        "sleep",
        "garb",
        "move",
        "climb",
        "swim",
        "release",
        "use",
    ]
    while True:
        name = random.choice(players)
        action = random.choice(actions)
        yield (name, action)


def consume_event(
        events: list[tuple[str, str]]
        ) -> typing.Generator[tuple[str, str], None, None]:
    while events:
        event_index = random.randrange(len(events))
        event = events.pop(event_index)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")
    stream = gen_event()
    for index in range(1000):
        name, action = next(stream)
        print(f"Event {index}: Player {name} did aciton {action}")

    events: list[tuple[str, str]] = []
    for _ in range(10):
        events.append(next(stream))
    print(f"Built list of 10 events: {events}")

    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
