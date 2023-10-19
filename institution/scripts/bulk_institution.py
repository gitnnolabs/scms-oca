import csv
import os

from django.contrib.auth import get_user_model

from institution import models
from location.models import Location
from usefulmodels.models import State, City, Country

User = get_user_model()


def load_or_up_date(inst, row, creator, source):
    inst.name = row.get("Name").title()
    inst.institution_type = row.get("Institution Type")
    inst.acronym = row.get("Acronym")
    inst.source = source
    inst.level_1 = row.get("Level_1")
    inst.level_2 = row.get("Level_2")
    inst.level_3 = row.get("Level_3")

    if not inst.location:
        if source == "MEC":
            state_name = State.get_or_create(
                acronym=row.get("State Acronym"), user=creator
            ).name
            city_name = None
        else:
            state_name = State.get_or_create(name=row.get("state"), user=creator).name
            city_name = City.get_or_create(name=row.get("city"), user=creator).name
        inst.location = Location.get_or_create(
            user=creator,
            location_country="Brasil",
            location_state=state_name,
            location_city=city_name,
        )
    inst.creator = creator


def load_official_institution(creator, row, line, source):
    try:
        if not row.get("Name"):
            raise ValueError("'Name' is absent")

        # nao foi usado Institution.get_or_create porque exige city, state e country
        # e como a fonte de dados pode ter ou não, poderia acabar criando
        # registros indesejáveis
        try:
            inst = models.Institution.objects.get(name__iexact=row.get("Name"))
        except models.Institution.DoesNotExist:
            inst = models.Institution()
            load_or_up_date(inst, row, creator, source)
            inst.save()
        else:
            if not inst.source:
                inst.source = source
                inst.save()

    except Exception as ex:
        print("Import error: %s, Line: %s" % (ex, str(line + 2)))
    else:
        print(inst.name, inst.acronym)
        print("File imported successfully!")


def run(*args):
    user_id = args[0] if args else 1

    user = User.objects.get(id=user_id)

    for item in [
        ["mec_1", ";", "MEC"],
        ["mec_2", ";", "MEC"],
        ["ror_brazil", ";", "ROR"],
        ["ror_others", ";", "ROR"],
    ]:
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + f"/../fixtures/institutions_{item[0]}.csv",
            "r",
        ) as csvfile:
            data = csv.DictReader(csvfile, delimiter=item[1])

            for line, row in enumerate(data):
                load_official_institution(
                    creator=user, row=row, line=line, source=item[2]
                )
