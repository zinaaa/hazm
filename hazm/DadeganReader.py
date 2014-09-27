# coding: utf8

from __future__ import unicode_literals
import codecs
from nltk.parse import DependencyGraph


def coarse_pos_e(tags):
	"""
	Coarse POS tags of Dadegan corpus:
		N: Noun, V: Verb, ADJ: Adjective, ADV: Adverb, PR: Pronoun, PREP: Preposition, POSTP: Postposition, CONJ: Conjunction, PUNC: Punctuation, ADR: Address Term, IDEN: Title, PART: Particle, POSNUM: Post-noun Modifier, PREM: Pre-modifier, PRENUM: Pre-noun Numeral, PSUS: Pseudo-sentence, SUBR: Subordinating Clause

	>>> coarse_pos_e(['N', 'IANM'])
	'N'
	"""

	map = {'N': 'N', 'V': 'V', 'ADJ': 'AJ', 'ADV': 'ADV', 'PR': 'PRO', 'PREM': 'DET', 'PREP': 'P', 'POSTP': 'POSTP', 'PRENUM': 'NUM', 'CONJ': 'CONJ', 'PUNC': 'PUNC'}
	return map.get(tags[0], '') + ('e' if 'EZ' in tags else '')


class DadeganReader():
	"""
	interfaces [Persian Dependency Treebank](http://dadegan.ir/perdt/download)
	"""

	def __init__(self, conll_file='corpora/dadegan.conll', pos_map=coarse_pos_e):
		self._conll_file = conll_file
		self._pos_map = pos_map if pos_map else lambda tags: ','.join(tags)

	def _sentences(self):
		text = codecs.open(self._conll_file, encoding='utf8').read()

		# refine text
		text = text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')

		for item in text.replace(' ', '_').split('\n\n'):
			if item.strip():
				yield item

	def trees(self):
		for sentence in self._sentences():
			tree = DependencyGraph(sentence)

			for node in tree.nodelist[1:]:
				node['mtag'] = [node['ctag'], node['tag']]

			for node in tree.nodelist[1:]:
				if node['rel'] in ('MOZ', 'NPOSTMOD'):
					tree.nodelist[node['head']]['mtag'].append('EZ')

			for node in tree.nodelist[1:]:
				node['mtag'] = self._pos_map(node['mtag'])

			yield tree

	def sents(self):
		"""
		>>> next(dadegan.sents())
		[('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]
		"""

		for tree in self.trees():
			yield [(node['word'], node['mtag']) for node in tree.nodelist[1:]]