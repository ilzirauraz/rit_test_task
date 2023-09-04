import json
import os
from dataclasses import dataclass
from typing import Generator
from typing import Optional

from db import SQLiteDB
from queries import create_query, save_query

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

db = SQLiteDB(config['db']['name'])


@dataclass
class Company:
    name: str
    okved: str
    inn: int
    kpp: int
    address: str


DIR_PATH = ''


def parse(data: dict) -> Optional[Company]:
    if is_from_city(data):
        okved = data.get('data', {}) \
            .get('СвОКВЭД', {}) \
            .get('СвОКВЭДОсн', {}) \
            .get('КодОКВЭД', '')
        if not is_it_company(okved):
            return
        address = data.get('data', {}) \
            .get('СвАдресЮЛ', {})

        return Company(
            name=data.get('full_name'),
            inn=int(data.get('inn')),
            kpp=int(data.get('kpp')),
            okved=okved,
            address=json.dumps(address, ensure_ascii=False)
        )


def is_it_company(okved: str):
    return okved.startswith('61')


def is_from_city(data: dict, name: str = 'Хабаровск') -> bool:
    return data.get('data') \
               .get('СвАдресЮЛ', {}) \
               .get('АдресРФ', {}) \
               .get('Город', {}) \
               .get('НаимГород', '').capitalize() == name.capitalize()


def companies_gen() -> Generator[Company, None, None]:
    path = config['dir_path']['egrul']
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        with open(file_path) as f:
            data_lst: list[dict] = json.load(f)
            for data in data_lst:
                company_info = parse(data)
                if company_info is not None:
                    yield company_info


def main():
    for company_data in companies_gen():
        save(company_data)


def save(company: Company):
    db.execute(save_query, (company.name, company.okved, company.inn, company.kpp, company.address))


if __name__ == '__main__':
    db.execute(create_query)
    main()
