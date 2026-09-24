from PIL import Image

from medianview.filter import median_filter_3x3


def test_median_filter_handles_interior_edges_and_corners() -> None:
    pixels = [
        (9, 1, 5),
        (1, 9, 4),
        (8, 2, 3),
        (2, 8, 2),
        (7, 3, 1),
        (3, 7, 9),
        (6, 4, 8),
        (4, 6, 7),
        (5, 5, 6),
    ]
    image = Image.new("RGB", (3, 3))
    image.putdata(pixels)

    filtered = median_filter_3x3(image)

    assert filtered.getpixel((1, 1)) == (5, 5, 5)
    assert filtered.getpixel((0, 0)) == (7, 3, 4)
    assert filtered.getpixel((1, 0)) == (7, 3, 4)


def test_median_filter_preserves_dimensions_and_is_deterministic() -> None:
    image = Image.new("RGB", (4, 2))
    image.putdata(
        [
            (12, 22, 32),
            (90, 80, 70),
            (1, 2, 3),
            (250, 240, 230),
            (42, 52, 62),
            (5, 15, 25),
            (100, 110, 120),
            (200, 190, 180),
        ]
    )

    first = median_filter_3x3(image)
    second = median_filter_3x3(image)

    assert first.size == image.size
    assert first.tobytes() == second.tobytes()
