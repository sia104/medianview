"""Web entry point for MedianView."""

from base64 import b64encode
from io import BytesIO

from flask import Flask, abort, render_template_string, request
from PIL import Image, UnidentifiedImageError

from medianview.filter import median_filter_3x3

UPLOAD_PAGE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>MedianView</title></head>
<body>
  <h1>MedianView</h1>
  <form method="post" enctype="multipart/form-data">
    <input name="image" type="file" accept="image/png,image/jpeg" required>
    <button type="submit">Apply median filter</button>
  </form>
</body>
</html>
"""

RESULT_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>MedianView</title>
  <style>.comparison { display: flex; align-items: flex-start; }</style>
</head>
<body>
  <h1>MedianView</h1>
  <div class="comparison">
    <img id="original-image" src="data:{{ original_type }};base64,{{ original }}">
    <img id="filtered-image" src="data:image/png;base64,{{ filtered }}">
  </div>
</body>
</html>
"""


def create_app() -> Flask:
    """Create the MedianView application."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        if request.method == "GET":
            return render_template_string(UPLOAD_PAGE)

        upload = request.files.get("image")
        if upload is None:
            abort(400)

        original_bytes = upload.read()
        try:
            with Image.open(BytesIO(original_bytes)) as image:
                if image.format not in {"PNG", "JPEG"} or image.mode != "RGB":
                    abort(400)
                image.load()
                filtered = median_filter_3x3(image)
                original_type = "image/png" if image.format == "PNG" else "image/jpeg"
        except (OSError, UnidentifiedImageError):
            abort(400)

        filtered_bytes = BytesIO()
        filtered.save(filtered_bytes, format="PNG")
        return render_template_string(
            RESULT_PAGE,
            original=b64encode(original_bytes).decode("ascii"),
            original_type=original_type,
            filtered=b64encode(filtered_bytes.getvalue()).decode("ascii"),
        )

    return app


def main() -> None:
    """Run the development server."""
    create_app().run()


if __name__ == "__main__":
    main()
