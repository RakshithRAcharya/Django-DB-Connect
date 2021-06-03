from django.db import models

server_choices = [('mysql', 'MySQL'), ('postgre', 'PostgreSQL'), ('oracle','OracleDB'), ('sql server','SQL Server')]
# Create your models here.
class DB(models.Model):
    db_server = models.CharField(max_length=30, choices=server_choices, help_text='select one of the options')
    db_host = models.CharField(max_length=100, help_text='ex: localhost/85.64.34.21')
    db_name = models.CharField(max_length=100, help_text='database name')
    db_port = models.IntegerField(help_text='port number')
    db_login_username = models.CharField(max_length=255, help_text='database username')
    db_login_password = models.CharField(max_length=100, blank=True, help_text='database password')

    def __str__(self):
        return self.db_server + ' ' + self.db_login_username 
