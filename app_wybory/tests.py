from django.test import TestCase
from app_wybory.models  import *
from django.db.models import Sum
# Create your tests here.

class EdycjaTestCase(TestCase):
    def test_glosy_wazne(self):
        for obwod in Obwod.objects.all():
            self.assertEqual(WynikKandydata.objects.filter(obwod=obwod).aggregate(Sum('wynik'))['wynik__sum'],
                             WynikStatystyki.objects.get(obwod=obwod).wynik)

      