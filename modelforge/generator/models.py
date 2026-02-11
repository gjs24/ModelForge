

from django.db import models

class GeneratedModel(models.Model):
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50)
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()
    output_file = models.FileField(
        upload_to="generated_models/",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name

