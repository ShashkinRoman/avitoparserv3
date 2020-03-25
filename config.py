import os
from builtins import object
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()


class Ads:
    """ Принимает урлы каждого из объявлений
    и информацю для последующей записи в бд """
    def __init__(self):
        self.urls_ads = []
        self.info_ads =[]


def avito_request():
    """ декодируем, чтобы русские символы корректо вставлялись в урл
    :return: запрос на русском в кодировке UTF-8 """
    decode_request = os.getenv('request_avito')
    request_avito = decode_request.encode('cp1251').decode('utf8')
    return request_avito


class Urls(object):
    """ В зависимости от object_parse выбирает вариант сборки урла
    возвращает шаблон урла каталога """
    def __init__(self):
        self.object_parse = os.getenv('object_parse')

    def urls(self, region, avito_request):
        if self.object_parse == 'beauty':
            url = 'https://www.avito.ru/' + region\
                  + '/predlozheniya_uslug/krasota_zdorove?q='\
                  + avito_request + '&p='

        if self.object_parse == 'nedvij_studii_vtorich':
            url = 'https://www.avito.ru/' + region \
                  + '/kvartiry/prodam/studii/vtorichka-ASgBAQICAUSSA8YQAkDKCBT~WOYHFIxS' \
                  + avito_request + '?p='
        return url


Base = declarative_base()


class InformationFromAds(Base):
    __tablename__ = os.getenv('tablename')
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    title = Column(String)
    price = Column(String)
    place = Column(String)
    description = Column(String)
    type_ads = Column(String)
    region = Column(String)
    url = Column(String)


def session_db():
    engine = create_engine('sqlite:///' + os.getenv('database_name') + '.db')
    session_object = sessionmaker()
    session_object.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = session_object()
    return session


def main():
    av_request = avito_request()
    regions = os.getenv('regions')
    ads_obj = Ads()
    # object_parse = os.getenv('object_parse') #указываем для выбора формы урла
    url_generator = Urls()
    session = session_db()
    return av_request, regions, ads_obj, url_generator, session


if __name__ == '__main__':
    main()
