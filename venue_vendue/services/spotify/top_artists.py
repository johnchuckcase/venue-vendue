from urllib.parse import urlencode
import requests
import logging

from venue_vendue.db import Session
from venue_vendue.data_models.spotify.top_artists import TopArtistsDataModel

# token = 'BQCDbryF1r3xNd_CMQUBOCOF0y-iTZPt8FVtQIktC9HGKIV8RpgKqDxt5wL7kHArACR-Csmm8aHsQiv5NNBBLHoypSGXAhJ2ToJOQtYp0eoNXkthxhZY00TuTltbN5Vt7WUHxU_YGgEuktYDxGcT7DLX15I3'
# headers = {'Authorization': f'''Bearer {token}'''}
# resource_url = 'https://api.spotify.com/v1/me/top/artists'


class TopArtistsService:

    RESOURCE_URL = 'https://api.spotify.com/v1/me/top/artists'
    DATA_MODEL = TopArtistsDataModel

    @classmethod
    def session(cls):
        return Session()

    @classmethod
    def sync_with_remote(cls):
        token = 'BQBg51i1JjKSZ5IPRG1c6nPM7VoIVqf-sbG_vR4go0GznWChYDqSmAKw1cjZiLoXuQLiERvzyVbhPNfYYTxw0vgk3rQ6bSQ0kwBXHxi9hl_Aov3EbGpwqA3Iu6u7BKqFWIdYqPAD18gOz_Qzlw_LZZaG0d-c'
        headers = {'Authorization': f'''Bearer {token}'''}
        session = cls.session()
        sql_records = cls.session().query(cls.DATA_MODEL).all()
        for time_range in ['short_term', 'medium_term', 'long_term']:
            query = {'time_range': time_range, 'limit': 50}

            # query API for all artists in time range
            resp = requests.get(f'{cls.RESOURCE_URL}?{urlencode(query)}', headers=headers)

            # query DB for all artists
            import pytest
            pytest.set_trace()
            for rank, obj in enumerate(resp.json()['items']):
                sql_record = next((sql_record for sql_record in sql_records
                                   if obj['id'] == sql_record.id and time_range == sql_record.time_range), None)

                # if artist is already in DB. Will be replaced later
                if sql_record:
                    sql_records.remove(sql_record)
                    new_record = sql_record
                # otherwise create new sql record based on api response object
                else:
                    new_record = cls.DATA_MODEL()
                    for col in cls.DATA_MODEL.__table__.columns.keys():
                        if col in obj:
                            setattr(new_record, col, obj[col])
                    new_record.time_range = time_range
                    new_record.rank = rank

                if new_record != sql_record:
                    session.add(new_record)

        for sql_record in sql_records:
            session.delete(sql_record)
        try:
            session.commit()
        except InvalidRequestError as e:
            logging.error(e)
