# coding: utf8

from __future__ import unicode_literals
from nltk.tag import stanford
from .SequenceTagger import SequenceTagger


class SequencePOSTagger(SequenceTagger):
	pass


class POSTagger(stanford.POSTagger):
	"""
	>>> tagger = POSTagger(path_to_jar='resources/stanford-postagger.jar', path_to_model='resources/persian.tagger')
	>>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
	[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]
	"""

	def __init__(self, path_to_jar, path_to_model, *args, **kwargs):
		self._SEPARATOR = '/'
		super(stanford.POSTagger, self).__init__(encoding='utf8', path_to_jar=path_to_jar, path_to_model=path_to_model, *args, **kwargs)

	def tag_sents(self, sentences):
		refined = map(lambda s: [w.replace(' ', '_') for w in s], sentences)
		return super(stanford.POSTagger, self).tag_sents(refined)
