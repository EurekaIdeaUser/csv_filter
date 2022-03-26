def remove_punct (l):
	return list(map(lambda s: s.replace('-', ' '), l))

cold_kws = remove_punct([
'card',
'cartridge',
'hepatitis', 
'hiv',
'home',
'kit',
'test',
])

avg_kws = remove_punct([
'cassette',
'detection',
'device',
'viral',
])

warm_kws = remove_punct([
'ag',
'antibody',
'antigen',
'assay',
'clia',
'collodial gold',
'combo',
'fast',
'fia',
'igg',
'igm',
'immunoassay',
'immunochromatographic',
'immunochromatography',
'immunofluorescence',
'immunology',
'lateral flow',
'nasal',
'nasopharyngeal',
'oral',
'plasma',
'protein ',
'qag',
'rapid',
'reagent',
'saliva',
'self test',
'serum',
'sputum',
'strip',
'swab',
'whole blood',
])

hot_kws = remove_punct([
'abcheck',
'access',
'accu-tell',
'accucare',
'accurate', # overmatcher?
'acon',
'acro',
'actim',
'activxpress',
'acura seed',
'acuraseed',
'adexusdx',
'advia centaur',
'advia',
'aehealth',
'aeskulisasars',
'affidx',
'afias',
'ag-q', # not in MRL
'alinityi',
'allcheck',
'alpine',
'altamed',
'amela',
'amp',
'andlucky',
'angcard',
'answer',
'anti', # overmatcher?
'anylab',
'architect',
'aria',
'arista',
'arkan',
'arsonic',
'artron',
'asan',
'aspen',
'assure',
'atellica',
'atomo',
'basall',
'bd',
'beckman',
'beright',
'binaxnow',
'biocard',
'bioclin',
'biocredit',
'bioeasy',
'biohermes',
'biohit',
'biomedomics',
'bionare',
'bioquick',
'biosci',
'bioscience',
'biosynex',
'bioteke',
'biotical',
'biotime',
'biozek',
'bmt',
'bnibt',
'boson',
'bpro',
'bz',
'cadila',
'carestart',
'careus',
'celer',
'cellex',
'cellife',
'celltrion',
'certest',
'check',
'chembio',
'cl',
'clarity',
'clearepi',
'clinitest',
'clip', # not in MRL
'clungene',
'covab',
'covclear',
'covida-19', # not in MRL
'covidfast',
'covidx',
'covifind',
'covirat',
'coviself',
'covscan',
'diakey',
'diaquick',
'dpp',
'drop-tech',
'dsi',
'dynamiker',
'eclusis',
'ecotest',
'edgexpress',
'edinburgh',
'ekomed',
'elecsys',
'elisa',
'elisafe',
'ellume',
'encode',
'epithod',
'erbalisa',
'erbaqik',
'espline',
'euroimmun',
'excalibur',
'exdia',
'ezdx',
'fastbio',
'fastclear',
'fastep',
'finecare',
'flowflex',
'fluoro-check',
'fm new',
'fora',
'frend',
'fuji',
'futurecare',
'gazelle',
'gblisa',
'genbody',
'genedia',
'genefinder',
'genomic',
'genrui',
'gensure',
'gline',
'gmate',
'green spring',
'gsd',
'healgen',
'hecin',
'helix',
'hiscl',
'hough',
'humasis',
'ichroma',
'iflash',
'imcov',
'immtek',
'immunoarrow',
'immunofine',
'immunoquick',
'immupass',
'imunoace',
'indicaid',
'indoswab',
'innoscreen',
'innova',
'instantsure',
'instaxplor',
'insti',
'inteliswab',
'is covid-19',
'istoc',
'ivdlab',
'jinjian',
'joysbio',
'juschek',
'kavach',
'kawach',
'kdx',
'kewei',
'kiamgenics',
'kifatest',
'kimia',
'kmb',
'konsung',
'ky-bio',
'lambra',
'landwind',
'leadgene',
'liaison',
'livzon',
'look spot',
'lordmeg',
'lumipulse',
'lumira',
'lumivi',
'lyher',
'maglumi',
'maripoc',
'mark-b', # 'mark' in MRL w/o 'b'
'mdx',
'medicheck',
'medsan',
'medtest',
'meriscreen',
'mexacare',
'microlisa',
'midaspot',
'mindray',
'mologic',
'mytest',
'nadal',
'nanjing',
'nantong',
'navica',
'nd',
'neocheck',
'new', # overmatcher?
'newlungene',
'newsha',
'ng',
'nids',
'ninonasal',
'nirmidas',
'nova test',
'novegent',
'nowcheck',
'ntbio',
'nulife',
'ol',
'omnia',
'one step',
'onemed',
'onsite',
'optra',
'orawell',
'osar',
'ovios',
'p4detect',
'panbio',
'pantest',
'pathkits',
'pathocatch',
'pbcheck',
'pcl',
'perkinelmer',
'pinpoint',
'pixotest',
'platelia',
'pocroc',
'polymed',
'prodetect',
'prolisa',
'prorast',
'qiareach',
'qualisa',
'quampas',
'quick chaser',
'quickkit',
'quicknavi',
'quickprofile',
'quickvue',
'rabwiz',
'radi',
'rapcov',
'rapicov',
'rapid covid', # overmatcher?
'rapid response', # overmatcher?
'rapid sars-cov-2', # overmatcher?
'reopentest',
'resars',
'resilient & rápido', # in MRL as "resilient rpido"
'reszon',
'rida',
'rightsign',
'roche',
'romed',
'safety',
'saic',
'salocor',
'sampinute',
'schebo',
'sd biosensor',
'seinofy',
'sensit',
'sensitest',
'sgti-flex',
'siemens',
'sienna-clarity',
'simoa',
'simtomax',
'smart', # overmatcher?
'sofia',
'spera',
'spring health',
'standard', # overmatcher?
'star', # overmatcher?
'strongstep',
'sure status',
'sure',  # overmatcher?
'surescreen',
'taishan',
'tbg',
'tell me',
'tempo',
'test-it',
'testsea',
'tigsun',
'trueline',
'trurapid',
'trustline',
'uji cepad',
'ultracovi',
'unicell',
'v-chek',
'v-code',
'verasure',
'veri-q',
'verino',
'vida',
'vidas',
'vitrogen',
'vitros',
'vivadiag',
'voxel',
'vstrip',
'vtrust',
'wantai',
'wesail',
'wholepower',
'willi',
'wiz',
'wondfo',
'wonmed',
'xamin',
'ybio',
])


def create_mw_kw_map(kw_list):
	mw_kws = list(filter(lambda kw: len(kw.split(' ')) > 1, kw_list))
	mw_map = {}
	for kw in mw_kws:
		kwl = kw.split(' ')
		key = kwl[0]
		# rest_l = kwl[1:]
		# rest_s = ' '.join(rest_l)
		rest_s = set(kwl)
		if key in mw_map:
			mw_map[key].append(rest_s)
		else:
			mw_map[key] = [rest_s]
	return mw_map

kw_configs = [
	{
		'terms': set(hot_kws),
		'mw_map': create_mw_kw_map(hot_kws),
		'weight': 20,
	},
	{
		'terms': set(warm_kws),
		'mw_map': create_mw_kw_map(warm_kws),
		'weight': 4,
	},
	{
		'terms': set(avg_kws),
		'mw_map': create_mw_kw_map(avg_kws),
		'weight': 1,
	},
	{
		'terms': set(cold_kws),
		'mw_map': create_mw_kw_map(cold_kws),
		'weight': 0,
	},
]

def get_kw_match_score(match_set):
	score = 0
	score_report = {}
	# track used kws to skip terms that've already been counted
	used_set = set()
	# print(match_set)
	for kw_config in kw_configs:
		# print('\n---   Looking at weight: ', kw_config['weight'], score, used_set)
		for kw in match_set:
			# print('\n - considering kw: ', kw, score, used_set, '\n')
			if kw in used_set:
				# print(kw, 'was already found')
				# move on to next kw in loop
				continue 
			
			if kw in kw_config['terms']:
				# print('found ', kw, ' score was ', score)
				score += kw_config['weight']
				score_report[kw] = kw_config['weight']
				used_set.add(kw)
				# print('now ', score, ' used set ', used_set)
				# move on to next kw in loop
				continue 
				
			elif kw in kw_config['mw_map']:
				# print('in elif')
				# check if kw is starting term of a multi-word kw
				for kw_set in kw_config['mw_map'][kw]:
					# print('potential mw match with terms: ', kw_set)
					# if yes, check if all terms in the mw kw are in the matched set
					if len(match_set&kw_set) >= len(kw_set):
						# print('found ', kw_set, ' score was ', score)
						score += kw_config['weight']
						score_report['_'.join(kw_set)] = kw_config['weight']
						# add all terms in the mw kw to the used_set
						used_set = used_set|kw_set
						# print('now ', score, ' used set ', used_set)
						# match found, so end this loop and move to next kw in loop
						break
					# print('not found')

	# print('done matching', score, match_set, used_set)
	unused_set = match_set - used_set
	# print(unused_set)
	score += len(unused_set)
	if len(unused_set) > 0:
		score_report[','.join(unused_set)] = '1ea'
	# print('final ', score, str(score_report))
	return (score, str(score_report))