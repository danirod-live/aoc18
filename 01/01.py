
def infinite_stream_of_frequencies(freqs):
    while True:
        for freq in freqs:
            yield freq

acc = 0
seen_freqs = {}

data = [int(x) for x in open('input.txt').readlines()]
stream = infinite_stream_of_frequencies(data)
while True:
    freq = next(stream)
    acc += freq
    if acc in seen_freqs:
        print(acc)
        break
    else:
        seen_freqs[acc] = 1
