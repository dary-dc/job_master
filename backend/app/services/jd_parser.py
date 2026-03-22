from fastapi import UploadFile

from app.services.cv_parser import parse_text_upload


async def parse_jd(file: UploadFile) -> str:
    return await parse_text_upload(file, label="jd")


async def parse_career_dump(file: UploadFile) -> str:
    return await parse_text_upload(file, label="career_dump")
