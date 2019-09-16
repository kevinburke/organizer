# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import json
from organizer.importing import DatasetImporter
from organizer.exporting import DatasetExporter
from filtering.models import FilterNode

class ImportSource(models.Model):
    name = models.CharField(max_length=255)
    backend = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    configuration = models.TextField(blank=True, null=True)
    lastRun = models.DateTimeField(blank=True, null=True)

    def make_importer(self):
        importCls = DatasetImporter.get_plugin(self.backend)
        return importCls(json.loads(self.configuration))

    def __unicode__(self):
        return '%s: %s' % (self.name, self.backend)

class ExportSink(models.Model):
    name = models.CharField(max_length=255)
    backend = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    configuration = models.TextField(blank=True, null=True)
    lastRun = models.DateTimeField(blank=True, null=True)
    filter = models.ForeignKey(FilterNode)

    def make_exporter(self):
        importCls = DatasetExporter.get_plugin(self.backend)
        return importCls(self.filter.results, json.loads(self.configuration))

    def __unicode__(self):
        return '%s: %s' % (self.name, self.backend)
