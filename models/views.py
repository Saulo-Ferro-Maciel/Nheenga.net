from django.shortcuts import render
from blog.serializers import Photo as P
from blog.models import Banco_De_Imagens as BI

from rest_framework.views import APIView as AV
from rest_framework.response import Response
from rest_framework import status

from blog import forms
from django.views.generic.edit import FormView as FW

import smtplib
import email.message
from datetime import datetime,date
from pytz import timezone
# Create your views here.

def enviar_email(nome,email2,mensagem):
    
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y — %H:%M')
    data = data_e_hora_sao_paulo_em_texto
    data= str(data)
    corpo_email = f"""
        <p style="text-align: center; color:#7b68ee;font-size: 13px;">Data de Envio: {data}</p><hr>
        <h4 style=color:#20b2aa;><b>NOME DO CLIENTE:</b><br></h4>
        <p>{nome}</p><hr>
        <p style=color:#20b2aa;><b>MENSAGEM RECEBIDA DO CLIENTE:</b></p>
        <p>{mensagem}</p><hr>
        <p style=color:#20b2aa;><b>EMAIL DE RETORNO AO CLIENTE:</b><br>{email2}<hr>
    """

    msg = email.message.Message()
    msg['Subject'] = f"Mesagem de: {nome}"
    msg['From'] = 'panapanasoftware@gmail.com'
    msg['To'] = 'panapanasoftware@gmail.com'
    password = 'rbjrnkocqdadnvvx' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
    
def form_manual(request):
    if request.method == 'POST':
        nome=request.POST.get('nome',None)
        email2=request.POST.get('email',None)
        mensagem=request.POST.get('Sua mensagem')
        print(nome,email2,mensagem)
        enviar_email(nome,email2,mensagem)
    return render(request, 'contatos.html')

class PhotoListCreate(AV):
    name='photo_list_create'

    def get(self,request):
        photo = BI.objects.all()
        serialize = P(photo, many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)

    def post(self,request):
        serialize = P(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_202_ACCEPTED)
        return Response(serialize.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
class PhotoListDelete(AV):
    name='photo_list_delete'

    def put(self,request,pk):
        try:
            image = BI.objects.get(pk=pk)
            data = request.data
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        image.remover_imagem()
        image.Imagens_Para_Corpo_Da_Matéria = data['image']
        image.save()
        serialize = P(image)
        return Response(serialize.data, status=status.HTTP_200_OK)
        
    def delete(self,request,pk):
        try:
            image = BI.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

