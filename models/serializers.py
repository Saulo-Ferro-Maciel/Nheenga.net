from rest_framework.serializers import ModelSerializer as MS
from blog.models import Banco_De_Imagens

class Photo(MS):
    model = Banco_De_Imagens
    fields=['id','image']