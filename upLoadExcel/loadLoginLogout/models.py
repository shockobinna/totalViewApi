# from django.db import models

# class TotalViewApiDB(models.Model):
#     IDUSUARIO = models.IntegerField() 
#     DATA_REFERENCIA = models.DateField()
#     LOGIN = models.DateTimeField()
#     LOGOUT = models.DateTimeField()
#     PLATAFORMA = models.CharField(max_length=255)
#     ATUALIZACAO = models.DateTimeField()

#     @classmethod
#     def get_record_count(cls):
#         return cls.objects.count()

from django.db import models

class TotalViewApiDB(models.Model):
    IDUSUARIO = models.IntegerField() 
    DATA_REFERENCIA = models.DateField(null=True, blank=True)
    LOGIN = models.DateTimeField(null=True, blank=True)
    LOGOUT = models.DateTimeField(null=True, blank=True)
    PLATAFORMA = models.CharField(max_length=255, null=True, blank=True)
    ATUALIZACAO = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_record_count(cls):
        return cls.objects.count()


