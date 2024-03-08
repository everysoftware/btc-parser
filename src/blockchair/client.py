import datetime
import gzip
import os
from typing import Literal

import aiohttp
from aiohttp import ClientPayloadError
from starlette import status


class BlockchairClient:
    """Клиент для работы с Blockchair."""

    dumps_base_url: str = "https://gz.blockchair.com/bitcoin"
    """Базовый URL для дампов."""
    block_size: int = 1024 * 1024  # 1 MB
    """Размер блока для чтения и записи файла."""

    def unzip(self, file_path: str, out_file_path: str) -> str:
        """Распаковывает файл."""
        with gzip.open(file_path, "rb") as f_in, open(out_file_path, "wb") as f_out:
            chunk = f_in.read(self.block_size)
            while chunk:
                f_out.write(chunk)
                chunk = f_in.read(self.block_size)
        return out_file_path

    async def load_dump(
        self,
        date: datetime.date,
        dump_type: Literal["transactions", "inputs", "outputs"],
    ) -> str | None:
        """Получает дамп транзакций за день и сохраняет его в файл."""
        date_str = date.strftime("%Y%m%d")
        basename = f"blockchair_bitcoin_{dump_type}_{date_str}.tsv"

        url = f"{self.dumps_base_url}/{dump_type}/{basename}.gz"
        file_path = f"dumps/{basename}.gz"
        out_file_path = f"dumps/{basename}"

        if os.path.exists(out_file_path):
            return out_file_path

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                try:
                    with open(file_path, "wb") as f:
                        chunk = await response.content.read(self.block_size)
                        while chunk:
                            f.write(chunk)
                            chunk = await response.content.read(self.block_size)
                except ClientPayloadError:
                    raise

        return self.unzip(file_path, out_file_path)
