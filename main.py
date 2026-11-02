"""Console application that compares town clocks with the Grand Clock Tower."""

import math
import re
import sys

GRAND_CLOCK_TIME = "15:00"
URGENT_THRESHOLD_MINUTES = 120
TOWN_CLOCKS = ("Clock 1", "Clock 2", "Clock 3", "Clock 4")


def parse_time(clock_time: str) -> int:
    """Convert a time in HH:MM format to minutes after midnight."""
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", clock_time):
        raise ValueError(f"Invalid time {clock_time!r}; expected HH:MM (00:00-23:59).")

    hours, minutes = clock_time.split(":")
    return int(hours) * 60 + int(minutes)


def calculate_offset(clock_time: str, grand_clock_time: str) -> int:
    """Return the clock's difference in minutes from the Grand Clock Tower."""
    return parse_time(clock_time) - parse_time(grand_clock_time)


def find_urgent_clocks(clock_offsets: dict[str, int]) -> dict[str, int]:
    """Return clocks whose absolute offset exceeds the fixed urgent threshold."""
    urgent_clocks = {
        name: offset
        for name, offset in clock_offsets.items()
        if abs(offset) > URGENT_THRESHOLD_MINUTES
    }
    return urgent_clocks


def classify_clock(offset: int) -> str:
    """Classify a clock by its difference from the Grand Clock Tower."""
    if offset == 0:
        return "In line"
    if abs(offset) > URGENT_THRESHOLD_MINUTES:
        return "High priority"
    return "Low priority"


def format_offset(offset: int) -> str:
    """Describe an offset, including its sign and whether the clock is ahead."""
    if offset > 0:
        return f"+{offset} minutes (ahead)"
    if offset < 0:
        return f"{offset} minutes (behind)"
    return "0 minutes (synchronized)"


def render_clock(clock_time: str) -> str:
    """Draw a small ASCII clock face showing the supplied time."""
    minutes_after_midnight = parse_time(clock_time)
    hours, minutes = divmod(minutes_after_midnight, 60)
    size = 15
    center = size // 2
    radius = 5
    grid = [[" " for _ in range(size)] for _ in range(size)]

    for y in range(size):
        for x in range(size):
            if abs(math.hypot(x - center, y - center) - radius) < 0.6:
                grid[y][x] = "."

    grid[0][center - 1:center + 1] = list("12")
    grid[center][0] = "9"
    grid[center][size - 1] = "3"
    grid[size - 1][center] = "6"

    def draw_hand(angle_degrees: float, length: float, marker: str) -> None:
        angle = math.radians(angle_degrees)
        end_x = round(center + length * math.sin(angle))
        end_y = round(center - length * math.cos(angle))
        x, y = center, center
        dx, dy = abs(end_x - x), abs(end_y - y)
        step_x = 1 if x < end_x else -1
        step_y = 1 if y < end_y else -1
        error = dx - dy

        while (x, y) != (end_x, end_y):
            grid[y][x] = marker
            doubled_error = 2 * error
            if doubled_error > -dy:
                error -= dy
                x += step_x
            if doubled_error < dx:
                error += dx
                y += step_y

    draw_hand((hours % 12) * 30 + minutes * 0.5, 2.5, "H")
    draw_hand(minutes * 6, 4, "M")
    grid[center][center] = "+"

    return "\n".join("".join(row) for row in grid)


def read_clock_time(name: str) -> str:
    """Ask for a clock time and retry until it uses a valid HH:MM format."""
    while True:
        clock_time = input(f"Enter the time for {name} (HH:MM): ").strip()
        try:
            parse_time(clock_time)
        except ValueError as error:
            print(f"{error} Please try again.", file=sys.stderr)
        else:
            return clock_time


def main() -> int:
    """Print the time difference for each town clock."""
    try:
        clock_times = {
            name: read_clock_time(name)
            for name in TOWN_CLOCKS
        }
        grand_minutes = parse_time(GRAND_CLOCK_TIME)
        print(f"Grand Clock Tower: {GRAND_CLOCK_TIME}")
        print(render_clock(GRAND_CLOCK_TIME))

        clock_offsets = {}
        for name, clock_time in clock_times.items():
            offset = calculate_offset(clock_time, GRAND_CLOCK_TIME)
            clock_offsets[name] = offset
            print(f"{name} ({clock_time}): {format_offset(offset)}")
            print(render_clock(clock_time))

        urgent_clocks = find_urgent_clocks(clock_offsets)
        print("H = hour hand; M = minute hand")
        clocks_to_adjust = sum(offset != 0 for offset in clock_offsets.values())
        print(f"Clocks to adjust: {clocks_to_adjust} of {len(clock_times)}")
        print(
            f"Urgent adjustment threshold: more than "
            f"{URGENT_THRESHOLD_MINUTES} minutes"
        )
        print(f"Urgent clocks: {len(urgent_clocks)} of {len(clock_times)}")
        if urgent_clocks:
            for name, offset in urgent_clocks.items():
                direction = "forward" if offset < 0 else "backward"
                print(
                    f"{name}: adjust {abs(offset)} minutes {direction} "
                    "to match the Grand Clock Tower."
                )
        else:
            print("No clock exceeds the urgent adjustment threshold.")

        print("\nFinal summary:")
        for name, offset in clock_offsets.items():
            classification = classify_clock(offset)
            if offset == 0:
                adjustment = "no adjustment needed"
            else:
                direction = "forward" if offset < 0 else "backward"
                adjustment = f"adjust {abs(offset)} minutes {direction}"
            print(
                f"{name}: {abs(offset)} minutes difference; {adjustment}; "
                f"classification: {classification}."
            )
    except EOFError:
        print("Error: input ended before all clock times were entered.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
