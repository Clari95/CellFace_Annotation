from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings

# Models based on https://wiki.tum.de/display/ldv/Database


class Dataset(models.Model):
    """
        Dataset table, loosely following the schema of meta data of:
            - https://wiki.tum.de/pages/viewpage.action?spaceKey=ldv&title=HDF5
    """
    # id is generated automatically
    name = models.CharField(max_length=200)
    path = models.FilePathField(path=settings.MEDIA_ROOT,
                                allow_files=True,
                                allow_folders=False,
                                recursive=True,
                                max_length=200,
                                unique=True)

    # TODO: uncomment the lines below and run python manage.py makemigrations and python manage.py migrate
    # # some meta attributes
    # n_files = models.IntegerField()
    # # [height, width] is converted into two IntegerFields
    # img_size_height = models.IntegerField()
    # img_size_width = models.IntegerField()
    # type = models.CharField(max_length=200)
    # version = models.FloatField()
    #
    # # changed this _xml_ into several of the XML key-values
    # # TODO: validate with client if these are the wanted ones
    # xml = models.CharField(max_length=1000)
    # # attempt below at reproducing necessary values based on talks with Stephan
    # operator = models.CharField(max_length=200)
    # date = models.DateTimeField()
    # height_raw = models.IntegerField()
    # width_raw = models.IntegerField()
    # manufacturer = models.CharField(max_length=200)
    # model = models.CharField(max_length=200)
    # serial_number = models.CharField(max_length=100)
    # depth_of_field = models.FloatField()
    # depth_of_investigation = models.FloatField()
    # low_frequency = models.IntegerField()
    # down_sampling_factor = models.FloatField()


class PhaseDataset(models.Model):
    """
        Table for Phase data, loosely following the schema of meta data of:
            - https://wiki.tum.de/pages/viewpage.action?spaceKey=ldv&title=HDF5
    """
    # id is generated automatically
    name = models.CharField(max_length=200)
    path = models.FilePathField(path=settings.MEDIA_ROOT,
                                allow_files=True,
                                allow_folders=False,
                                recursive=True,
                                max_length=200,
                                # unique=True
                                )
    raw = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)
    background_subtraction = models.BooleanField()
    crop_min = models.FloatField()
    crop_max = models.FloatField()


class Attribute(models.Model):
    """
        Attribute table, generic table to store possible additions of attributes to:
            - https://wiki.tum.de/display/ldv/Database
    """
    dataset = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)
    attr_name = models.CharField(max_length=200)
    attr_value = models.CharField(max_length=200)

    class Meta:
        unique_together = [["dataset", "attr_name"]]


class Tag(models.Model):
    """
        Tag table.
    """
    tag_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DatasetTag(models.Model):
    """
        Dataset-Tag association, each dataset can have multiple tags.
    """
    dataset = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["dataset", "tag"]]


class Project(models.Model):
    """
        Project model, specifies which person/project owns a given dataset.
    """
    dataset = models.OneToOneField(to=Dataset, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
