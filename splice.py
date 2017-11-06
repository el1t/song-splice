from pydub import AudioSegment
from pydub.utils import make_chunks
from random import sample, shuffle, random
from itertools import tee, chain
bpm = 160
bps = bpm / 60
ms_per_beat = 1000 / bps
ticks_per_beat = int(ms_per_beat)
ticks_per_quarter_beat = int(ms_per_beat / 4)
ms_per_beat = int(ms_per_beat)


def pairwise(iterable):
	"""s -> (s0,s1), (s1,s2), (s2, s3), ..."""
	a, b = tee(iterable)
	next(b, None)
	return zip(a, b)


def chance(item):
	if random() < 0.3:
		# shuffle quarter-beats
		item = make_chunks(item, ticks_per_quarter_beat)
		shuffle(item)
		item = sum(item)
	if random() < 0.1:
		# reverse current bar
		item = item.reverse()
	if item.max_dBFS > -3.5:
		# Quieter!
		item -= item.max_dBFS + 3.5
	return item


def main():
	# Split into sections (intro, buildup, drop, etc.)
	sections = [5, 11, 35, 47, 60, 60+23, 60+47, 120, 120+12]  # , 120+22]
	ending = [120+36, 120+47]

	song = AudioSegment.from_mp3('song.mp3')

	def seconds_to_beat(s): return int(s * bps)

	chunk_sections = map(seconds_to_beat, sections)
	chunks = make_chunks(song, ticks_per_beat)
	acc = []
	for start, end in chain(pairwise(chunk_sections), [map(seconds_to_beat, ending)]):
		acc += map(chance, sample(chunks[start:end], end - start))

	# Combine, apply fades, and export
	sum(acc).fade_in(4 * ms_per_beat).fade_out(8 * ms_per_beat).export('out.mp3', format='mp3')


if __name__ == '__main__':
	main()
