import csv
import datetime
import gzip
import io
from typing import Literal

import aiohttp
from starlette import status


class BlockchairClient:
    """Клиент для работы с Blockchair."""

    dumps_base_url: str = "https://gz.blockchair.com/bitcoin"
    """Базовый URL для дампов."""

    async def get_dump(
        self,
        date: datetime.date,
        dump_type: Literal["transactions", "inputs", "outputs"],
    ) -> csv.DictReader | None:
        """Получает дамп транзакций за день."""
        date_str = date.strftime("%Y%m%d")
        url = f"{self.dumps_base_url}/{dump_type}/blockchair_bitcoin_{dump_type}_{date_str}.tsv.gz"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                compressed_data = await response.read()
                decompressed_data = gzip.decompress(compressed_data)
                text_data = decompressed_data.decode()

                return csv.DictReader(io.StringIO(text_data), delimiter="\t")
