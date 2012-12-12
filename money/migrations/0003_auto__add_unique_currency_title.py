# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Currency', fields ['title']
        db.create_unique('money_currency', ['title'])


    def backwards(self, orm):
        # Removing unique constraint on 'Currency', fields ['title']
        db.delete_unique('money_currency', ['title'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'money.currency': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'money.distribution': {
            'Meta': {'object_name': 'Distribution'},
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['money.Transaction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rest': ('django.db.models.fields.FloatField', [], {}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'distributions'", 'null': 'True', 'to': "orm['money.Transaction']"})
        },
        'money.template': {
            'Meta': {'object_name': 'Template'},
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destinations'", 'null': 'True', 'to': "orm['money.Wallet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sources'", 'null': 'True', 'to': "orm['money.Wallet']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'templates'", 'to': "orm['auth.User']"})
        },
        'money.transaction': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Transaction'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination_amount': ('django.db.models.fields.FloatField', [], {}),
            'gain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'rest': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'source_amount': ('django.db.models.fields.FloatField', [], {}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': "orm['money.Template']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': "orm['auth.User']"})
        },
        'money.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'currency': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['money.Currency']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wallets'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['money']