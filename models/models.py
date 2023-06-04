from django.db import models
from django.contrib.auth.models import User as usr
from django.core.exceptions import ValidationError

#from ckeditor.fields import RichTextField as rtf
from ckeditor_uploader.fields import RichTextUploadingField as rtuf

from random import randint
from datetime import datetime,date
from pytz import timezone
import os, uuid

def checkIfFileLessThanBytes( value):
    filesize= value.size
    BYTES=86698000
    filesize_h= value.height
    filesize_w=value.width
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']

    if not ext.lower() in valid_extensions:
        raise ValidationError(f"Wrong file type, send only '.jpeg' or '.png'!")
    else:
        if filesize < BYTES:
            if filesize_h > 720 or filesize_w > 1280 :
                raise ValidationError(f"Exceeded size, please add an image up to 1280X720 pixels")
            else:
                if filesize_h <= 100 or filesize_w <= 530:
                    raise ValidationError(f"Exceeded size, please add an image up to 1280X720 pixels and larger than 530X100 pixels")
            return value
        else:
            raise ValidationError(f"File larger than 500 KB, max limit exceeded")

def helpTexts():
    
    b,c=0,['good morning'.capitalize(),'good afternoon'.capitalize(),'goodnight'.capitalize()]
    d,e=0,0
    a=0

    jornal=['"If a dog bites a man, there is no news; if a man bites a dog, there is news." —Charles Anderson Dana (1819-1897)',
    '"Modern journalism has one thing going for it. By offering us the opinion of the ignorant, it keeps us up to date with the inauguration of the community." —Oscar Wilde',
    '"I call journalism anything that is less interesting tomorrow than today." — André Gide',
    '''"Journalism is publishing what others don't want published. Everything else is publicity." - Unknown author''',
    '"The principle that journalism must be taught and that it is not rational to let the journalist form himself." —Antonio Gramsci',
    '"Without journalism there is no revolution." —Juarez Alves',
    '"Give me a lever and a fulcrum and I will lift the world" - Archimedes',
    '"Many people owe the greatness of their lives to the problems they had to overcome." —Robert Baden Powell',
    '''"If you think it's possible to have a perfect life, you will live in eternal frustration. Ups and downs, joys and sorrows, enthusiasm and disappointments are an integral part of our existence. " —Robert Baden Powell''',
    '''"Some people read "War and Peace" and think it's a simple novel. Other people read a pack of gum and unlock the secrets of the universe" - Lex Luthor''',
    '"Everything is worth it when the soul is not small." —Fernando Pessoa',
    '"Wise is he who knows the limits of his own ignorance." —Socrates', 
    '"Who commits an injustice is always more unhappy than the wronged." - Plato',
    '“The noblest pleasure is the joy of understanding” - Leonardo Da Vinci',
    ]
    a= randint(0,len(jornal))

    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y — %H:%M')
    data = data_e_hora_sao_paulo_em_texto

    hora= int(data_e_hora_sao_paulo.strftime('%H'))

    if hora>=1 and hora<12:
        d=c[0]
        e='Carpe Diem — Latin '
    if hora>=12 and hora<20:
        d=c[1]
        e='Puranga Karuka — Nheengathú'
    if (hora>=20 and hora<=24) or hora==0:
        d=c[2]
        e='Bonan Nokton — Esperanto'

    b = f'''<h2><big>📰 {d} 👋</big></h2>
        <strong>
            {e}
        </strong>
        <address><strong>
            {f'{data}'}
        </strong></address>
        <em>
            <p>{jornal[a]}</p>
        </em>
        <address><u><cite>
            Have a good job, don't forget to delete this message before writing the article!
        </cite></u></address>
        <address><u><cite><font style="vertical-align:inherit"><font style="vertical-align:inherit"><img alt="coração" src="http://127.0.0.1:8000/static/ckeditor/ckeditor/plugins/smiley/images/heart.png" style="height:23px; width:23px" title="coração" /><img alt="piscar" src="http://127.0.0.1:8000/static/ckeditor/ckeditor/plugins/smiley/images/wink_smile.png" style="height:23px; width:23px" title="piscar" /></font></font></cite></u></address>
        
        '''
    return b 

def upload_imageFormater(instance, filename):
    return f"{str(uuid.uuid4())}--{filename}"

class Banco_De_Imagens(models.Model):
    Imagens_Para_Corpo_Da_Matéria=models.ImageField(upload_to=upload_imageFormater,blank=False,validators=[checkIfFileLessThanBytes])
    Nome_da_Imagem=models.CharField(max_length=210,help_text="Maximum limit of 210 characters", db_index=True,default='')
    slug=models.SlugField(max_length=210,unique=True,db_index=True,null=True, blank=True)
    
    def has_image(self):
        return self.Imagens_Para_Corpo_Da_Matéria != None and self.Imagens_Para_Corpo_Da_Matéria != ""
    
    def remover_imagem(self):
        if self.has_image():
            if os.path.isfile(self.Imagens_Para_Corpo_Da_Matéria.path):
                os.remove(self.Imagens_Para_Corpo_Da_Matéria.path)
        self.Imagens_Para_Corpo_Da_Matéria = None
    
    def dlete(self):
        self.remover_imagem()
        super().delete()

    def __str__(self):
        return self.Nome_da_Imagem

class Gênero(models.Model):
    Gênero_ou_Chapéu = models.CharField(max_length=210, db_index=True)
    slug=models.SlugField(max_length=210,unique=True,db_index=True,null=True, blank=True)

    def __str__(self):
        return self.Gênero_ou_Chapéu

class Poste(models.Model):
    Data_de_Ultima_Publicação=models.DateField(auto_now=True)
    Data_de_Publicação=models.DateField(default=date.today(),null=True,blank=True)
    Gênero_ou_Chapéu= models.ForeignKey(Gênero, on_delete=models.CASCADE,related_name='posts')
    Autor=models.ForeignKey(usr, on_delete=models.PROTECT)
    Título=models.CharField(max_length=210, help_text="Maximum limit of 210 characters", db_index=True)
    slug=models.SlugField(max_length=210,unique=True,db_index=True,null=True, blank=True)
    Subtítulo_ou_Sutiã=models.CharField(max_length=325, help_text="Maximum limit of 325 characters")
    Texto_ou_Pirâmide_Invertida=rtuf(blank=True, null=True, default=helpTexts())
    Imagem_de_Capa=models.ImageField(upload_to=f'postes/%Y/%m/%d/',blank=False,validators=[checkIfFileLessThanBytes])

    class Meta:
        index_together=(('id','slug'),)

    def __str__(self):
        return self.Título
    