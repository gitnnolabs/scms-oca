from django.db.utils import DataError

from scholarly_articles import models


class ArticleSaveError(Exception):
    ...

class JournalSaveError(Exception):
    ...

class ContributorSaveError(Exception):
    ...

class AffiliationSaveError(Exception):
    ...


def get_params(row, attribs):
    params = {}
    for att in attribs:
        if row.get(att):
            params[att] = row.get(att)
    return params


def load_article(row):
    articles = models.ScholarlyArticles.objects.filter(doi=row.get('doi'))
    try:
        article = articles[0]
    except IndexError:
        article = models.ScholarlyArticles()
        article.doi = row.get('doi')
        article.year = row.get('year')
        article.journal = load_journal(row)
        for author in row.get('z_authors') or []:
            contributor = get_one_contributor(author)
            article.contributors.add(contributor)
        try:
            article.save()
        except (DataError, TypeError) as e:
            raise ArticleSaveError(e)

    return article


def load_journal(row):
    attribs = ['journal_issns', 'journal_issn_l', 'journal_name']
    params = get_params(row, attribs)

    journals = models.Journals.objects.filter(**params)
    try:
        journal = journals[0]
    except IndexError:
        journal = models.Journals()
        journal.journal_is_in_doaj = row.get('journal_is_in_doaj')
        journal.journal_issns = row.get('journal_issns')
        journal.journal_issn_l = row.get('journal_issn_l')
        journal.journal_name = row.get('journal_name')
        journal.publisher = row.get('publisher')
        try:
            journal.save()
        except (DataError, TypeError) as e:
            raise JournalSaveError(e)

    return journal


def get_one_contributor(author):
    attribs = ['family', 'given']
    params = get_params(author, attribs)
    if author.get('ORCID'):
        params['orcid'] = author.get('ORCID')
    elif author.get('affiliation'):
        try:
            aff = models.Affiliations.objects.filter(name=author.get('affiliation')[0].get('name'))
            params['affiliation'] = aff[0]
        except IndexError:
            pass

    contributors = models.Contributors.objects.filter(**params)
    try:
        contributor = contributors[0]
    except IndexError:
        contributor = models.Contributors()
        contributor.family = author.get('family')
        contributor.given = author.get('given')
        contributor.orcid = author.get('ORCID')
        contributor.authenticated_orcid = author.get('authenticated-orcid')
        if author.get('affiliation'):
            try:
                aff = load_affiliation(author['affiliation'][0]['name'])
                contributor.affiliation = aff
            except KeyError:
                pass
        try:
            contributor.save()
        except (DataError, TypeError) as e:
            raise ContributorSaveError(e)

    return contributor


def load_affiliation(affiliation_name):
    if affiliation_name:
        affiliations = models.Affiliations.objects.filter(name=affiliation_name)
    try:
        affiliation = affiliations[0]
    except IndexError:
        affiliation = models.Affiliations()
        if affiliation_name:
            affiliation.name = affiliation_name
        try:
            affiliation.save()
        except (DataError, TypeError) as e:
            raise AffiliationSaveError(e)

    return affiliation


def run(from_year=1900, resource_type='journal-article'):
    #pagination
    rawunpaywall = models.RawUnpaywall.objects.filter(year__gte=from_year, resource_type=resource_type)
    for item in rawunpaywall:
        if not item.is_paratext:
            try:
                load_article(item.json)
            except (ArticleSaveError, JournalSaveError, ContributorSaveError, AffiliationSaveError) as e:
                error = models.ErrorLog()
                error.document_id = item
                error.error_type = str(type(e))
                error.error_message = str(e)[:255]
                try:
                    error.save()
                except (DataError, TypeError):
                    pass


if __name__ == '__main__':
    run()
