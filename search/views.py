import csv
import datetime
import json
import logging
import math
import os
from collections import OrderedDict

import pysolr
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from indicator.models import Indicator
from search.graphic_data import GraphicData

solr = pysolr.Solr(
    settings.HAYSTACK_CONNECTIONS["default"]["URL"],
    timeout=settings.HAYSTACK_CONNECTIONS["default"]["SOLR_TIMEOUT"],
)


def search(request):
    fqs = []
    filters = {}
    search_query = request.GET.get("q", None)
    search_field = request.GET.get("search-field", None)
    fqfilters = request.GET.get("filters", None)
    facet_name = request.GET.get("more_facet_name", None)
    facet_count = request.GET.get("more_facet_count", None)
    sort_by = request.GET.get("selectSortKey", "geo_priority asc")

    if search_query == "" or not search_query:
        search_query = "*:*"

    if search_field:
        search_query = search_field

    # Page
    try:
        page = abs(int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        return Http404("Not a valid number for page.")

    rows = int(request.GET.get("itensPage", settings.SEARCH_PAGINATION_ITEMS_PER_PAGE))

    start_offset = (page - 1) * rows

    filters["start"] = start_offset
    filters["rows"] = rows

    if facet_name and facet_count:
        filters["f." + facet_name + ".facet.limit"] = facet_count

    if fqfilters:
        fqs = fqfilters.split("|")

    fqs = ['%s:"%s"' % (fq.split(":")[0], fq.split(":")[1]) for fq in fqs]

    fqs.append('record_status:"PUBLISHED"')

    # Adiciona o Solr na pesquisa
    search_results = solr.search(search_query, fq=fqs, sort=sort_by, **filters)

    # Cria um dicionário ordenado dos facets considerando a lista settings.SEARCH_FACET_LIST
    facets = search_results.facets["facet_fields"]
    ordered_facets = OrderedDict()

    for facet in settings.SEARCH_FACET_LIST:
        ordered_facets[facet] = facets.get(facet, "")

    if request.GET.get("raw"):
        return JsonResponse(search_results.raw_response, safe=False)

    wt = request.GET.get("wt")
    if wt == "csv":
        filename = "%s_%s.csv" % (
            "download_csv_",
            datetime.datetime.today().strftime("%d_%m_%Y"),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="%s"' % (filename)

        t = loader.get_template("csv_template.txt")
        c = {"search_results": search_results}
        response.write(t.render(c))
        return response

    total_pages = int(math.ceil(float(search_results.hits) / rows))

    return render(
        request,
        "search.html",
        {
            "search_query": "" if search_query == "*:*" else search_query,
            "search_results": search_results,
            "facets": ordered_facets,
            "page": page,
            "fqfilters": fqfilters if fqfilters else "",
            "start_offset": start_offset,
            "itensPage": rows,
            "wt": wt if wt else "HTML",
            "settings": settings,
            "total_pages": total_pages,
            "selectSortKey": sort_by,
        },
    )


def _get_indicator(request, indicator_slug):
    # check if the slug is not a database id else redirect to slug url format
    try:
        return Indicator.get(indicator_slug, record_status="PUBLISHED")
    except Indicator.DoesNotExist:
        raise Http404("Indicator does not exist")


def indicator_detail(request, indicator_slug):
    indicator = _get_indicator(request, indicator_slug)
    if indicator.slug != indicator_slug:
        return redirect(
            reverse(
                "search:indicator_detail",
                kwargs={"indicator_slug": indicator.slug}
            ),
            permanent=True,
        )
    
    summarized = json.loads(indicator.summarized)
    
    return render(
        request,
        "indicator/indicator_detail.html",
        {
            "object": indicator,
            "chart_keys": summarized.get("keys"),
            "chart_series": summarized.get("series"),
         },
    )


def indicator_summarized(request, indicator_slug):
    indicator = _get_indicator(request, indicator_slug)

    filename, ext = os.path.splitext(os.path.basename(indicator.raw_data.name))
    filename = filename + ".csv"

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="%s"' % filename},
    )

    for item in indicator.summarized["items"]:
        fieldnames = indicator.summarized["table_header"]
        break
    logging.info(indicator.summarized["table_header"])

    writer = csv.DictWriter(response, fieldnames=fieldnames)

    writer.writeheader()
    for item in indicator.summarized["items"]:
        try:
            writer.writerow(item)
        except:
            logging.info(item)
    return response


def indicator_raw_data(request, indicator_slug):
    indicator = _get_indicator(request, indicator_slug)

    filename = os.path.basename(indicator.raw_data.name)
    response = HttpResponse(indicator.raw_data, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=%s" % filename
    return response
