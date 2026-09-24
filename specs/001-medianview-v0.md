# MedianView V0 Specification

Status: Approved by human

## Purpose

MedianView is a Python web application that lets a user upload one image, applies
a fixed 3x3 median filter, and displays the original and filtered images
side-by-side.

## Scope

V0 must:

- Be a Python web application named MedianView.
- Let a user upload one image.
- Apply a fixed 3x3 median filter to that image.
- Display the original image and filtered image side-by-side, with the original
  first and the filtered result second.

The required V0 input domain is 8-bit RGB PNG and JPEG images. This defines the
input needed to make the requested workflow testable; behavior for other image
formats or pixel modes is not specified. JPEG EXIF metadata, including
orientation, is out of scope and no behavior is required for it.

## Image Processing Requirements

- Apply a 3x3 median filter independently to the red, green, and blue channels.
- For each output channel value, use the median of the nine values in the 3x3
  neighborhood centered on the corresponding input pixel.
- At image boundaries, extend the nearest edge pixel outward (edge replication)
  to form a complete 3x3 neighborhood.
- Preserve the input image's pixel dimensions.
- Given the same decoded RGB pixels, the filtered pixel values must be identical
  across repeated runs.
- The 3x3 filter size is fixed and is not user-configurable.

## User-visible Behavior

- Before an image is submitted, the upload control is available.
- After a required-domain image is submitted, the page shows the original on
  the left and the filtered result on the right.

## Acceptance Criteria

1. Opening the application provides a control for uploading one image.
2. Uploading an 8-bit RGB PNG or JPEG displays the original on the left and a
   filtered result on the right.
3. Every filtered pixel matches the channel-wise median and edge-replication
   rules above, including corner and edge pixels.
4. The filtered image has the same width and height as the input.
5. Processing the same image more than once produces identical filtered
   pixels.
6. The filter size cannot be changed by the user.
7. `pytest`, `ruff`, and `mypy` pass before merge.

## Test Expectations

- Unit tests must verify the median calculation with known RGB pixel matrices,
  including interior, edge, and corner pixels.
- Unit tests must verify unchanged dimensions and deterministic repeated output.
- Integration tests must upload an 8-bit RGB PNG and an 8-bit RGB JPEG and
  verify that both images are displayed in the required order.
- Tests must not depend on network access, wall-clock timing, or random image
  data without a fixed seed.

## Implementation Constraints

- The application and tests must be written in Python except for minimal
  presentation assets required by the web interface.
- The implementation may choose the Python web and image libraries, provided
  they satisfy this specification and the repository quality gates.
- Implementation must not begin until a human explicitly approves this
  specification.

## Optional Recommendations

These are possible improvements, not approved requirements. They are not part
of acceptance and must not be implemented unless separately requested or added
to an approved specification:

- Show clear errors for empty, unsupported, or undecodable uploads.
- Add labels that identify the original and filtered images.
- Preserve the uploaded image's aspect ratio in both displayed images.
- Adapt the comparison layout for narrow screens.
- Keep the upload control available after processing so another image can be
  submitted.
- Avoid persistent storage of uploaded and generated images.
