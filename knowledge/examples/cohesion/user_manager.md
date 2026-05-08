# Low Cohesion Example

class UserManager:
  - login()
  - resize_image()
  - export_pdf()
  - send_email()

## Interpretation

Methods operate on unrelated domains.

Likely violates Single Responsibility Principle.

## Signals

- Low attribute overlap
- Mixed domain concerns
- Large public API

## Suggested Refactors

- Extract ImageService
- Extract EmailService
- Extract ExportService