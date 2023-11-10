from django.test import TestCase, override_settings
from django.db.models import Q

from crm.models.copmanies import Company
# from models.copmanies import *

class CompanyTestCase(TestCase):
    @override_settings(DEBUG=True)
    def test_i(self):
        search_term = "11"
        query = Q(name__icontains=search_term) | Q(inn__icontains=search_term)
        query |= Q(legal__kpp__icontains=search_term) | Q(legal__ogrn__icontains=search_term)
        query |= Q(individual__ogrn__icontains=search_term)
        query |= Q(person__personal_id__icontains=search_term)
        companies = Company.objects.filter(query).distinct()
        print(companies)