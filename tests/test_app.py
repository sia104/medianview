from io import BytesIO

import pytest
from flask import Flask
from PIL import Image

from medianview import create_app


@pytest.fixture
def app() -> Flask:
    application = create_app()
    application.config.update(TESTING=True)
    return application


def encoded_image(image_format: str) -> BytesIO:
    image = Image.new("RGB", (3, 2), color=(20, 40, 60))
    encoded = BytesIO()
    image.save(encoded, format=image_format)
    encoded.seek(0)
    return encoded


def test_initial_page_has_one_image_upload(app: Flask) -> None:
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.text.count('type="file"') == 1
    assert "original-image" not in response.text
    assert "filtered-image" not in response.text


@pytest.mark.parametrize(
    ("image_format", "filename", "media_type"),
    [("PNG", "input.png", "image/png"), ("JPEG", "input.jpg", "image/jpeg")],
)
def test_upload_displays_original_then_filtered_image(
    app: Flask, image_format: str, filename: str, media_type: str
) -> None:
    response = app.test_client().post(
        "/",
        data={"image": (encoded_image(image_format), filename, media_type)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert f"data:{media_type};base64," in response.text
    assert "data:image/png;base64," in response.text
    assert response.text.index('id="original-image"') < response.text.index(
        'id="filtered-image"'
    )
