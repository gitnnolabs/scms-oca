from scholarly_articles import models

from datetime import date


def load(row):
    try:
        if row.get('doi'):
            rawunpaywall = models.RawUnpaywall.objects.filter(doi=row['doi'])
            if len(rawunpaywall) == 0:
                rawunpaywall = models.RawUnpaywall()
                rawunpaywall.doi = row['doi']
                rawunpaywall.harvesting_creation = date.today()
            else:
                return

        rawunpaywall.is_paratext = row.get('is_paratext')
        rawunpaywall.year = row.get('year')
        rawunpaywall.resource_type = row.get('genre')
        try:
            rawunpaywall.update = row.get('updated')[:10]
        except TypeError:
            pass
        rawunpaywall.json = row
        rawunpaywall.save()
    except KeyError:
        pass
