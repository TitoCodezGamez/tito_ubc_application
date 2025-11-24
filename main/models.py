from django.db import models

class Response(models.Model):
	name = models.CharField(max_length=100, unique=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class FormEntry(models.Model):
	response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True, blank=True, related_name='entries')
	name = models.CharField(max_length=100)
	text = models.TextField()
	dropdown = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.response.name if self.response else 'New Response'} | {self.name}: {self.text[:30]}{'...' if len(self.text) > 30 else ''}"
