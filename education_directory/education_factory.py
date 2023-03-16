from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from core.users import user_factory
from education_directory import models
from education_directory.choices import attendance_type, classification, status
from usefulmodels.usefulmodels_factory import ActionFactory, PraticeFactory

factory.Faker._DEFAULT_LOCALE = "pt_BR"


class EducationFactory(DjangoModelFactory):
    class Meta:
        model = models.EducationDirectory

    # Foreign Key
    creator = factory.SubFactory(user_factory.UserFactory)

    title = factory.Sequence(lambda n: "Title %03d" % n)
    description = factory.Faker("sentence", nb_words=50)
    link = factory.Faker("url")

    start_date = factory.LazyFunction(datetime.now)
    end_date = factory.LazyFunction(datetime.now)
    start_time = factory.LazyFunction(datetime.now)
    end_time = factory.LazyFunction(datetime.now)

    practice = factory.SubFactory(PraticeFactory)
    action = factory.SubFactory(ActionFactory)

    classification = factory.Iterator([c[0] for c in classification])

    attendance = factory.Iterator([at[0] for at in attendance_type])

    record_status = factory.Iterator([s[0] for s in status])

    source = factory.Sequence(lambda n: "Source %03d" % n)

    @factory.post_generation
    def locations(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for location in extracted:
                self.locations.add(location)

    @factory.post_generation
    def institutions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for inst in extracted:
                self.institutions.add(inst)
