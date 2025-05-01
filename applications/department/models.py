from django.db import models


app_name='department'

#Model Department
class Department(models.Model):
    TYPE_DEPARTMENT = [
        ('F', 'Firefighters'),
        ('P', 'Police'),
    ]

    code_department = models.CharField(max_length=10, primary_key=True, editable=False)
    type_department = models.CharField(max_length=1, choices=TYPE_DEPARTMENT)
    name_department = models.CharField(max_length=50)
    jurisdiction = models.JSONField()
    city_center_lat = models.FloatField()
    city_center_lon = models.FloatField()
    phone = models.BigIntegerField()

    def save(self, *args, **kwargs):
        if not self.code_department:
            # Buscar el último número usado para este tipo
            last = Department.objects.filter(type_department=self.type_department) \
                .order_by('-code_department') \
                .first()
            
            if last:
                # Obtener número desde 'F5' → 5
                last_number = int(last.code_department[1:])
            else:
                last_number = 0

            new_number = last_number + 1
            self.code_department = f"{self.type_department}{new_number}"

        super().save(*args, **kwargs)
    def __str__(self):
        return f"Departmento: #{self.code_department}, Nombre: {self.type_department} {self.name_department}"
