from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.text import Truncator

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)            #updates every time you make changes


    class Meta:
        abstract = True         #by this, in our databse there will be no class name BaseModel 


class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator')      # 1-to-many relations
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField(upload_to='blogs')

    def short_description(self):
        return Truncator(self.description).words(50)
