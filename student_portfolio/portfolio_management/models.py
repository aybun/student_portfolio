# # from django.db import models
#
# from djongo import models
# from django import forms
#
#
# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     class Meta:
#         abstract = True
#
#
# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = (
#             'name', 'tagline'
#         )
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#
#
# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = (
#             'name', 'email'
#         )
#
#
# class Entry(models.Model):
#     blog = models.EmbeddedField(
#         model_container=Blog,
#         model_form_class=BlogForm
#     )
#
#     headline = models.CharField(max_length=255)
#     authors = models.ArrayField(
#         model_container=Author,
#         model_form_class=AuthorForm
#     )
#
#     objects = models.DjongoManager()
#
#
