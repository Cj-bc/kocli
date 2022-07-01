# References:
# https://qiita.com/ohtaman/items/84426cee09c2ba4abc22#声を変換してみる
# https://pysoundfile.readthedocs.io/en/latest/
# https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder/blob/master/pyworld/pyworld.pyx
import pyworld as pw
import soundfile as sf
import numpy as np

import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), "test-rec.wav")
OUT_FILE = os.path.join(os.path.dirname(__file__), "converted.wav")

data, samplerate = sf.read(INPUT_FILE)

def convert_mono(mono_audio, samplerate):
    # https://stackoverflow.com/questions/26778079/valueerror-ndarray-is-not-c-contiguous-in-cython
	f0, sp, ap = pw.wav2world(mono_audio.copy(order='C'), samplerate)
	converted_sp = np.zeros_like(sp)

	for f in range(converted_sp.shape[1]):
		converted_sp[:, f] = sp[:, int(f/1.2)]

	return pw.synthesize(f0, converted_sp, ap, samplerate)

ch1 = convert_mono(data[:, 0], samplerate)
ch2 = convert_mono(data[:, 1], samplerate)

result = np.dstack([ch1, ch2])[0,:,:]
sf.write(OUT_FILE, result, samplerate)
