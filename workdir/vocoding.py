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

def identical(a):
        return a

def convert_mono(mono_audio, samplerate: float,
                 f0_converter=identical, sp_converter=identical):
    # https://stackoverflow.com/questions/26778079/valueerror-ndarray-is-not-c-contiguous-in-cython
	f0, sp, ap = pw.wav2world(mono_audio.copy(order='C'), samplerate)
	converted_sp = np.zeros_like(sp)

	for f in range(converted_sp.shape[1]):
		converted_sp[:, f] = sp[:, sp_converter(f)]

	return pw.synthesize(f0_converter(f0), converted_sp, ap, samplerate)

ch1 = convert_mono(data[:, 0], samplerate, lambda f0: f0, lambda sp_v: int(sp_v/1.2))
ch2 = convert_mono(data[:, 1], samplerate, lambda f0: f0, lambda sp_v: int(sp_v/1.2))

result = np.dstack([ch1, ch2])[0,:,:]
sf.write(OUT_FILE, result, samplerate)
