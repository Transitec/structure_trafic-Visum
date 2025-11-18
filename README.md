# structure_trafic-Visum
Le but de ce code est d'analyser des fichiers xlsx issus de Visum en termes de :¶
- structure du trafic multimodal (interne et échange) en se basant sur des matrices globales
- identification des principales relations par modes ou totaux pour l'ensemble des relations ou pour le trafic interne ou d'échange en se basant sur des matrices globales
- identification le trafic d'échange sur une pénétrante ou toutes les pénétrantes par rapport à un périmètre
Un premier prétraitement a été fait par un autre code pour transformer les matrices en listes et pour identifier pour chaque zone si elle est dans le périmètre d'étude.

Les données de base de ce code sont ainsi des fichiers xlsx. Pour des questions de propriété intellectuelle, les fichiers d'exemple présentent des valeurs aléatoires. Les colonnes suivantes sont disponibles :
origin = poche d'origine
destination = poche de destination
total = déplacements par unité de temps entre les poches d'origine et de destination
origin_in_agglomeration = valeur qui précise si la poche d'origine est dans l'agglomération
destination_in_agglomeration = valeur qui précise si la poche d'de destination est dans l'agglomération
origin_in_kern = valeur qui précise si la poche d'origine est dans le centre
destination_in_kern = valeur qui précise si la poche d'de destination est dans le centre