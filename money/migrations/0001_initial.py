# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table('money_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('money', ['Currency'])

        # Adding model 'Wallet'
        db.create_table('money_wallet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('currency', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['money.Currency'], unique=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('money', ['Wallet'])

        # Adding model 'Template'
        db.create_table('money_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sources', null=True, to=orm['money.Wallet'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destinations', null=True, to=orm['money.Wallet'])),
        ))
        db.send_create_signal('money', ['Template'])

        # Adding model 'Transaction'
        db.create_table('money_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['money.Template'])),
            ('rate', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('source_amount', self.gf('django.db.models.fields.FloatField')()),
            ('destination_amount', self.gf('django.db.models.fields.FloatField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rest', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gain', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('money', ['Transaction'])

        # Adding model 'Distribution'
        db.create_table('money_distribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(related_name='distributions', null=True, to=orm['money.Transaction'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['money.Transaction'])),
            ('rest', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('money', ['Distribution'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table('money_currency')

        # Deleting model 'Wallet'
        db.delete_table('money_wallet')

        # Deleting model 'Template'
        db.delete_table('money_template')

        # Deleting model 'Transaction'
        db.delete_table('money_transaction')

        # Deleting model 'Distribution'
        db.delete_table('money_distribution')


    models = {
        'money.currency': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinations'", 'null': 'True', 'to': "orm['money.Wallet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sources'", 'null': 'True', 'to': "orm['money.Wallet']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'})
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
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': "orm['money.Template']"})
        },
        'money.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'currency': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['money.Currency']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['money']