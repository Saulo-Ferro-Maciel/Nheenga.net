from django import forms as fms

class faleConosco(fms.Form):
    Seu_nome=fms.CharField(required=True)
    Seu_email=fms.EmailField(required=True)
    Sua_mensagem=fms.Textarea()