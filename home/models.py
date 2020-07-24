from django.db import models

# Create your models here.


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    # text field is used to store big contents
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)


# we write this def str becaz in db we see contact object 1, contat object 2 so to remove this we write def str n return message from so that we know who will send the msg n it is inside the class of Contact

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email
