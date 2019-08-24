from django.db import models

# Create a table named Company, primary_key is prebuilt: pk/id

class Company(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=32)
    logo = models.CharField(max_length=512)

    def __str__(self):
        return str(self.pk) + ' ' + self.name + ' ' + self.type

# Create another table named Jobs, Company's primary key as foreign key of table Jobs, and when the object in Company was deleted,
# object in Jobs will also be deleted according to Foreign Key
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    num_of_workers = models.IntegerField(default=1)



