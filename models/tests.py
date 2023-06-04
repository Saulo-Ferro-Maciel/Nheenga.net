from django.test import TestCase

# Create your tests here.
class TestarPaginas(TestCase):
    def testar_se_homepage_carrega_completa(self):
        response = self.client.get("/")
        self.assertAlmostEqual(response.status_code,200)
        self.assertTemplateUsed(response,'base.html')
        self.assertContains(response,'Nheenga')
