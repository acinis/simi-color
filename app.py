version_info: tuple[int, int, int] = (0, 1, 0)
__version__: str = ".".join(map(str, version_info))

import sys
import math


def eprint(
    *values: object, sep: str | None = " ", end: str | None = "\n", flush: bool = True
) -> None:
    """Like standard `print` but uses standard error stream and flushes by default."""
    return print(*values, sep=sep, end=end, file=sys.stderr, flush=flush)


class Color:
    """Simple class representing a RGB color."""

    @classmethod
    def _validate_component(cls, component: int) -> int:
        if component < 0:
            raise ValueError(f"Color components cannot be negative")
        if component > 255:
            raise ValueError(f"Color components cannot be greater than 255")
        return component

    def __init__(self, r: int, g: int, b: int):
        """Initialize color from given R, G and B components."""
        self.r = r
        self.g = g
        self.b = b

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        self._r = Color._validate_component(value)

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        self._g = Color._validate_component(value)

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = Color._validate_component(value)

    @classmethod
    def from_hex_string(cls, data: str) -> Color:
        """Create color instance from hexadecimal string in format RRGGBB."""
        if len(data) != 6:
            raise ValueError(f"Unsupported hexadecimal string format: {data}")
        try:
            r = int(data[0:2], 16)
            g = int(data[2:4], 16)
            b = int(data[4:6], 16)
        except ValueError as e:
            raise ValueError(f"Invalid value for color component(s): {e}")
        return Color(r, g, b)

    def __eq__(self, other: object) -> bool:
        """Custom equality operator implementation."""
        if not isinstance(other, Color):
            return NotImplemented
        return self.r == other.r and self.g == other.g and self.b == other.b

    @classmethod
    def from_dec_string(cls, data: str) -> Color:
        """Create color instance from decimal comma-separated string in format r,g,b."""
        components: list[str] = data.split(",")
        if len(components) != 3:
            raise ValueError(
                f"Unsupported decimal comma-separated string format: {data}"
            )
        try:
            r = int(components[0])
            g = int(components[1])
            b = int(components[2])
        except ValueError as e:
            raise ValueError(f"Invalid value for color component(s): {e}")
        return Color(r, g, b)

    @classmethod
    def from_string(cls, data: str) -> Color:
        """
        Create color instance from string. Supported formats are as in methods:
            - `from_hex_string()`
            - `from_dec_string()`
        """
        if "," in data:
            return Color.from_dec_string(data)
        else:
            return Color.from_hex_string(data)


def color_distance(color1: Color, color2: Color) -> float:
    """
    Using color-cube model, compute distance between two points using red, green and
    blue components as point coordinates.
    """
    distance = math.sqrt(
        (color2.r - color1.r) ** 2
        + (color2.g - color1.g) ** 2
        + (color2.b - color1.b) ** 2
    )
    return distance


def color_similarity(color1: Color, color2: Color) -> int:
    """Compute percentage of similarity between two colors."""
    MAX_DISTANCE = color_distance(Color(0, 0, 0), Color(255, 255, 255))
    distance: float = color_distance(color1, color2)
    # `difference` and `similarity` are in percents
    # `similarity` is simply an inverted percentage of `difference`
    difference: int = round(distance / MAX_DISTANCE * 100)
    if difference > 100:
        difference = 100
    similarity = 100 - difference
    return similarity


def main(argv: list[str]) -> int:
    """Compute percentage of similarity between two colors on command line."""
    if len(argv) > 1 and argv[1] == "--help":
        print(
            f"Usage: {argv[0]} COLOR_1 COLOR_2\n"
            f"\n"
            f"Compute percentage of similarity between two colors.\n"
            f"\n"
            f"Note that 100 percent of similarity will be reported only for identical colors.\n"
            f"For example, for colors 0,0,0 and 0,0,1 this tool will output 99.\n"
            f"\n"
            f"Version v{__version__}"
        )
        return 0
    if len(argv) != 3:
        eprint(f"error: Invalid command line usage, see `{argv[0]} --help`")
        return 1

    color1_data = argv[1]
    color2_data = argv[2]

    try:
        color1 = Color.from_string(color1_data)
        color2 = Color.from_string(color2_data)
    except ValueError as e:
        eprint(f"error: {e}")
        return 1

    similarity = color_similarity(color1, color2)

    # Adjust full similarity (100%) so that it occurs only if the colors are identical
    if similarity == 100 and (color1 != color2):
        similarity = 99

    print(similarity)

    return 0


if __name__ == "__main__":
    code = main(sys.argv)
    sys.exit(code)
