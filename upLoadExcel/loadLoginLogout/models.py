from django.db import models

class TotalViewApiDB(models.Model):
    IDUSUARIO = models.IntegerField(primary_key=True)
    DATA_REFERENCIA = models.DateField()
    LOGIN = models.DateTimeField()
    LOGOUT = models.DateTimeField()
    PLATAFORMA = models.CharField(max_length=255)
    ATUALIZACAO = models.DateTimeField()

    @classmethod
    def get_record_count(cls):
        return cls.objects.count()

