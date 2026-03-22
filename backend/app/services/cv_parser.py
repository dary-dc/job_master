from fastapi import UploadFile

_ALLOWED_EXTENSIONS = {"txt", "md"}


async def parse_text_upload(file: UploadFile, label: str) -> str:
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in _ALLOWED_EXTENSIONS:
        raise ValueError(
            f"{label} must be one of: {', '.join(sorted(_ALLOWED_EXTENSIONS))}. "
            f"Received file: {filename or 'unnamed'}"
        )

    content = await file.read()
    if not content:
        raise ValueError(f"{label} is empty")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    text = text.strip()
    if not text:
        raise ValueError(f"{label} has no readable text")
    return text


async def parse_cv(file: UploadFile) -> str:
    return await parse_text_upload(file, label="cv")
