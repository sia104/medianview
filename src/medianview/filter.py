"""Deterministic image filtering for MedianView."""

from typing import cast

from PIL import Image


def _bounded(value: int, upper_bound: int) -> int:
    return min(max(value, 0), upper_bound)


def median_filter_3x3(image: Image.Image) -> Image.Image:
    """Apply a channel-wise 3x3 median filter using replicated edges."""
    if image.mode != "RGB":
        raise ValueError("median_filter_3x3 requires an RGB image")

    width, height = image.size
    output_pixels: list[tuple[int, int, int]] = []

    for y in range(height):
        for x in range(width):
            channels: tuple[list[int], list[int], list[int]] = ([], [], [])
            for offset_y in (-1, 0, 1):
                source_y = _bounded(y + offset_y, height - 1)
                for offset_x in (-1, 0, 1):
                    source_x = _bounded(x + offset_x, width - 1)
                    pixel = cast(
                        tuple[int, int, int], image.getpixel((source_x, source_y))
                    )
                    for channel, value in zip(channels, pixel, strict=True):
                        channel.append(value)

            output_pixels.append(
                cast(
                    tuple[int, int, int],
                    tuple(sorted(values)[4] for values in channels),
                )
            )

    filtered = Image.new("RGB", image.size)
    filtered.putdata(output_pixels)
    return filtered
