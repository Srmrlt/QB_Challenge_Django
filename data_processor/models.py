from django.db import models


class ManifestDate(models.Model):
    id = models.AutoField(primary_key=True, db_comment='[PK]')
    date = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.id}> {self.date}'


class Exchange(models.Model):
    id = models.AutoField(primary_key=True, db_comment='[PK]')
    date = models.ForeignKey(ManifestDate, on_delete=models.CASCADE, related_name='exchanges')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.id}> {self.name} / {self.date}'


class Instrument(models.Model):
    id = models.AutoField(primary_key=True, db_comment='[PK]')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='instruments')
    name = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=100)
    levels = models.CharField(max_length=100)
    iid = models.IntegerField()
    available_interval_begin = models.TimeField()
    available_interval_end = models.TimeField()
    objects = models.Manager()

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.id}> {self.name} / {self.exchange}'
