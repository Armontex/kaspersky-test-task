import aiofiles
from fastapi import UploadFile


async def write_file(input_path: str, file: UploadFile):
    async with aiofiles.open(input_path, mode="wb") as buffer:
        while content := await file.read(1024 * 1024):
            await buffer.write(content)
