# Blockchair Bitcoin Parser

Это простой парсер для [Blockchair](https://blockchair.com/). Он написан на Python и использует библиотеку
`requests` для выполнения HTTP-запросов к API.

## Принцип работы

Ответ API представляет собой JSON-объект, содержащий информацию о блоке, транзакции или адресе.

Пример транзакции:

```json
{
  "block_id": 833405,
  "id": 973321721,
  "hash": "6803ad15315f760b3442f48cd38c6f5232c0eb21d3eeaf6ee0b1edb45fe7a4c1",
  "date": "2024-03-06",
  "time": "2024-03-06 12:08:19",
  "size": 742,
  "weight": 2167,
  "version": 2,
  "lock_time": 0,
  "is_coinbase": false,
  "has_witness": true,
  "input_count": 4,
  "output_count": 7,
  "input_total": 227106,
  "input_total_usd": 144.89363,
  "output_total": 207506,
  "output_total_usd": 132.38882,
  "fee": 19600,
  "fee_usd": 12.5048,
  "fee_per_kb": 26415.094,
  "fee_per_kb_usd": 16.852829,
  "fee_per_kwu": 9044.763,
  "fee_per_kwu_usd": 5.770559,
  "cdd_total": 0.0035087371875
}
```

Параметры транзакции:
* **block_id**: Идентификатор блока, в котором была включена транзакция.
* **id**: Уникальный идентификатор транзакции.
* **hash**: Хеш транзакции.
* **date**: Дата, когда транзакция была включена в блок.
* **time**: Время, когда транзакция была включена в блок.
* **size**: Размер транзакции в байтах.
* **weight**: Вес транзакции (важен для определения комиссии за транзакцию).
* **version**: Версия протокола биткоина, используемая в транзакции.
* **lock_time**: Время блокировки транзакции. Если это значение равно 0, транзакция может быть включена в любой новый блок.
* **is_coinbase**: Флаг, указывающий, является ли транзакция coinbase (т.е. транзакция, которая создает новые биткоины).
* **has_witness**: Флаг, указывающий, использует ли транзакция SegWit (отдельные свидетельства транзакции).
* **input_count**: Количество входов транзакции.
* **output_count**: Количество выходов транзакции.
* **input_total**: Общая сумма входов транзакции в сатоши.
* **input_total_usd**: Общая сумма входов транзакции в долларах США.
* **output_total**: Общая сумма выходов транзакции в сатоши.
* **output_total_usd**: Общая сумма выходов транзакции в долларах США.
* **fee**: Комиссия за транзакцию в сатоши.
* **fee_usd**: Комиссия за транзакцию в долларах США.
* **fee_per_kb**: Комиссия за транзакцию на килобайт в сатоши.
* **fee_per_kb_usd**: Комиссия за транзакцию на килобайт в долларах США.
* **fee_per_kwu**: Комиссия за транзакцию на весовую единицу (kwu) в сатоши.
* **fee_per_kwu_usd**: Комиссия за транзакцию на весовую единицу (kwu) в долларах США.
* **cdd_total**: Общее количество дней, уничтоженных монетами (Coin Days Destroyed, CDD). Это мера экономической активности
  в сети биткоина.

## Installation

To install the parser, simply clone the repository and install the required packages using pip:

```bash
git clone
cd blockchair-bitcoin-parser
pip install -r requirements.txt
```

## Usage

To use the parser, simply run the `main.py` file and pass the desired parameters as command line arguments. For example,
to get the latest block, run:

```bash
python main.py -l
```

To get the block with a specific hash, run:

```bash
python main.py -b <block_hash>
```

To get the transaction with a specific hash, run:

```bash
python main.py -t <transaction_hash>
```

To get the address with a specific hash, run:

```bash
python main.py -a <address_hash>
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
