import numpy as np
from scipy.io import wavfile
from scipy import signal
import sounddevice as sd

# Types: 'vowel', 'nasal', 'liquid', 'fricative', 'stop', 'affricate'
PHONEME_DATA = {
    # VOWELS
    'AA': [730, 1090, 2440, 1.0, 0.7, 0.3, 0.15, 'vowel'],
    'AE': [660, 1720, 2410, 1.0, 0.8, 0.3, 0.15, 'vowel'],
    'AH': [640, 1190, 2390, 1.0, 0.7, 0.3, 0.12, 'vowel'],
    'AO': [570, 840,  2410, 1.0, 0.6, 0.3, 0.15, 'vowel'],
    'AW': [640, 1190, 2390, 1.0, 0.7, 0.3, 0.20, 'vowel'],
    'AY': [730, 1090, 2440, 1.0, 0.7, 0.3, 0.20, 'vowel'],
    'EH': [530, 1840, 2480, 1.0, 0.8, 0.3, 0.12, 'vowel'],
    'ER': [490, 1350, 1690, 1.0, 0.7, 0.4, 0.15, 'vowel'],
    'EY': [400, 2000, 2550, 1.0, 0.8, 0.3, 0.18, 'vowel'],
    'IH': [390, 1990, 2550, 1.0, 0.8, 0.3, 0.10, 'vowel'],
    'IY': [270, 2290, 3010, 1.0, 0.9, 0.4, 0.15, 'vowel'],
    'OW': [500, 700,  2600, 1.0, 0.6, 0.3, 0.18, 'vowel'],
    'OY': [570, 840,  2410, 1.0, 0.6, 0.3, 0.20, 'vowel'],
    'UH': [440, 1020, 2240, 1.0, 0.6, 0.3, 0.12, 'vowel'],
    'UW': [300, 870,  2240, 1.0, 0.6, 0.3, 0.15, 'vowel'],
    
    # NASALS (voiced, nasal formants)
    'M':  [280, 1200, 2500, 0.9, 0.4, 0.2, 0.08, 'nasal'],
    'N':  [280, 1700, 2600, 0.9, 0.4, 0.2, 0.07, 'nasal'],
    'NG': [280, 2200, 2600, 0.9, 0.4, 0.2, 0.09, 'nasal'],
    
    # LIQUIDS (voiced, vowel-like)
    'L':  [300, 1300, 3000, 0.8, 0.5, 0.3, 0.07, 'liquid'],
    'R':  [420, 1300, 1600, 0.8, 0.5, 0.3, 0.08, 'liquid'],
    
    # SEMIVOWELS (voiced, very short)
    'W':  [300, 610,  2200, 0.8, 0.5, 0.3, 0.08, 'liquid'],
    'Y':  [280, 2250, 3000, 0.8, 0.6, 0.3, 0.06, 'liquid'],
    
    # VOICED FRICATIVES (mix of voice + noise)
    'V':  [200, 1000, 2500, 0.3, 0.3, 0.3, 0.09, 'fricative', {'voiced': True, 'freq': 2000}],
    'DH': [200, 1400, 2500, 0.3, 0.3, 0.3, 0.07, 'fricative', {'voiced': True, 'freq': 3500}],
    'Z':  [200, 1500, 2500, 0.3, 0.4, 0.4, 0.10, 'fricative', {'voiced': True, 'freq': 5000}],
    'ZH': [200, 1500, 2000, 0.3, 0.4, 0.4, 0.11, 'fricative', {'voiced': True, 'freq': 3000}],
    
    # UNVOICED FRICATIVES (pure noise)
    'F':  [200, 1000, 2500, 0.4, 0.4, 0.4, 0.10, 'fricative', {'voiced': False, 'freq': 2500}],
    'TH': [200, 1400, 2500, 0.4, 0.4, 0.4, 0.09, 'fricative', {'voiced': False, 'freq': 4000}],
    'S':  [200, 1500, 2500, 0.4, 0.5, 0.5, 0.12, 'fricative', {'voiced': False, 'freq': 6000}],
    'SH': [200, 1500, 2000, 0.4, 0.5, 0.5, 0.12, 'fricative', {'voiced': False, 'freq': 3500}],
    'HH': [200, 1500, 2500, 0.3, 0.3, 0.3, 0.08, 'fricative', {'voiced': False, 'freq': 2000}],
    
    # VOICED STOPS (silence + voiced burst)
    'B':  [200, 1000, 2500, 0.6, 0.4, 0.3, 0.08, 'stop', {'voiced': True, 'closure': 0.04, 'freq': 500}],
    'D':  [200, 1700, 2500, 0.6, 0.4, 0.3, 0.07, 'stop', {'voiced': True, 'closure': 0.04, 'freq': 2000}],
    'G':  [200, 2500, 3000, 0.6, 0.4, 0.3, 0.08, 'stop', {'voiced': True, 'closure': 0.05, 'freq': 2500}],
    
    # UNVOICED STOPS (silence + unvoiced burst)
    'P':  [200, 1000, 2500, 0.7, 0.5, 0.3, 0.09, 'stop', {'voiced': False, 'closure': 0.05, 'freq': 500}],
    'T':  [200, 1700, 2500, 0.7, 0.5, 0.3, 0.08, 'stop', {'voiced': False, 'closure': 0.05, 'freq': 3000}],
    'K':  [200, 2500, 3000, 0.7, 0.5, 0.3, 0.09, 'stop', {'voiced': False, 'closure': 0.06, 'freq': 3500}],
    
    # AFFRICATES (stop + fricative)
    'CH': [200, 1500, 2000, 0.6, 0.5, 0.4, 0.13, 'affricate', {'voiced': False, 'closure': 0.04, 'freq': 3500}],
    'JH': [200, 1500, 2000, 0.6, 0.5, 0.4, 0.13, 'affricate', {'voiced': True, 'closure': 0.04, 'freq': 3000}],
}

class FormantSynthesizer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.pitch = 120  # Hz
        
    def generate_glottal_pulse(self, duration):
        """Generate excitation source (vocal cord vibration)"""
        num_samples = int(self.sample_rate * duration)
        t = np.arange(num_samples) / self.sample_rate
        
        pulse_period = 1.0 / self.pitch
        excitation = np.zeros(num_samples)
        
        pulse_samples = int(self.sample_rate * pulse_period)
        pulse = np.zeros(pulse_samples)
        
        rise_len = int(pulse_samples * 0.4)
        pulse[:rise_len] = np.linspace(0, 1, rise_len) ** 2
        
        fall_len = int(pulse_samples * 0.16)
        pulse[rise_len:rise_len+fall_len] = np.linspace(1, 0, fall_len)
        
        num_pulses = int(duration / pulse_period) + 1
        for i in range(num_pulses):
            start = i * pulse_samples
            end = min(start + pulse_samples, num_samples)
            if start < num_samples:
                excitation[start:end] = pulse[:end-start]
            
        return excitation
    
    def generate_noise(self, duration):
        """Generate white noise for unvoiced sounds"""
        num_samples = int(self.sample_rate * duration)
        return np.random.randn(num_samples)
    
    def highpass_filter(self, audio, cutoff=500):
        """High-pass filter for fricatives"""
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='high')
        return signal.filtfilt(b, a, audio)
    
    def bandpass_filter(self, audio, center_freq, bandwidth=1000):
        """Band-pass filter for fricative coloring"""
        nyquist = self.sample_rate / 2
        low = max((center_freq - bandwidth/2) / nyquist, 0.01)
        high = min((center_freq + bandwidth/2) / nyquist, 0.99)
        b, a = signal.butter(3, [low, high], btype='band')
        return signal.filtfilt(b, a, audio)
    
    def formant_filter(self, audio, frequency, bandwidth):
        """Apply resonant filter at formant frequency"""
        r = np.exp(-np.pi * bandwidth / self.sample_rate)
        theta = 2 * np.pi * frequency / self.sample_rate
        
        a = [1.0, -2*r*np.cos(theta), r**2]
        b = [1 - r**2]
        
        return signal.lfilter(b, a, audio)
    
    def synthesize_vowel(self, f1, f2, f3, amp1, amp2, amp3, duration):
        """Synthesize vowel or vowel-like sound"""
        excitation = self.generate_glottal_pulse(duration)
        
        audio = np.zeros_like(excitation)
        audio += amp1 * self.formant_filter(excitation, f1, 60)
        audio += amp2 * self.formant_filter(excitation, f2, 90)
        audio += amp3 * self.formant_filter(excitation, f3, 120)
        
        return audio
    
    def synthesize_nasal(self, f1, f2, f3, amp1, amp2, amp3, duration):
        """Synthesize nasal consonant (like vowel but with anti-resonance)"""
        excitation = self.generate_glottal_pulse(duration)
        
        audio = np.zeros_like(excitation)
        audio += amp1 * self.formant_filter(excitation, f1, 100)
        audio += amp2 * self.formant_filter(excitation, f2, 150)
        audio += amp3 * self.formant_filter(excitation, f3, 200)
        
        # Add nasal murmur (low frequency component)
        audio += 0.3 * self.formant_filter(excitation, 250, 100)
        
        return audio
    
    def synthesize_fricative(self, f1, f2, f3, amp1, amp2, amp3, duration, 
                            voiced=False, freq=3000):
        """Synthesize fricative (noise-based)"""
        if voiced:
            # Mix voiced excitation with noise
            excitation = 0.3 * self.generate_glottal_pulse(duration) + \
                        0.7 * self.generate_noise(duration)
        else:
            # Pure noise
            excitation = self.generate_noise(duration)
        
        # Shape noise with bandpass filter
        audio = self.bandpass_filter(excitation, freq, 2000)
        
        # Apply formants (lighter than vowels)
        audio += amp1 * 0.3 * self.formant_filter(excitation, f1, 200)
        audio += amp2 * 0.3 * self.formant_filter(excitation, f2, 200)
        
        return audio
    
    def synthesize_stop(self, f1, f2, f3, amp1, amp2, amp3, duration, voiced=False, closure=0.05, freq=2000):
        """Synthesize stop consonant (silence + burst)"""
        closure_samples = int(self.sample_rate * closure)
        burst_duration = duration - closure
        burst_samples = int(self.sample_rate * burst_duration)
        
        # Silence during closure
        silence = np.zeros(closure_samples)
        
        # Burst (short duration, not full burst_duration)
        short_burst_duration = min(burst_duration * 0.3, 0.03)  # Max 30ms
        
        if voiced:
            burst = 0.5 * self.generate_glottal_pulse(short_burst_duration) + \
                0.5 * self.generate_noise(short_burst_duration)
        else:
            burst = self.generate_noise(short_burst_duration)
        
        # Pad to full burst duration
        burst = np.pad(burst, (0, burst_samples - len(burst)))
        
        # Shape burst
        if len(burst) > 0:
            burst = self.bandpass_filter(burst, freq, 2000)
            # Exponential decay envelope on burst
            envelope = np.exp(-np.linspace(0, 5, len(burst)))
            burst = burst * envelope
        
        return np.concatenate([silence, burst])
    
    def synthesize_affricate(self, f1, f2, f3, amp1, amp2, amp3, duration,
                            voiced=False, closure=0.04, freq=3000):
        """Synthesize affricate (stop + fricative)"""
        closure_samples = int(self.sample_rate * closure)
        fric_duration = duration - closure
        
        # Silence
        silence = np.zeros(closure_samples)
        
        # Fricative portion
        fricative = self.synthesize_fricative(f1, f2, f3, amp1, amp2, amp3,
                                              fric_duration, voiced, freq)
        
        return np.concatenate([silence, fricative])
    
    def synthesize_phoneme(self, params):
        """Route to appropriate synthesis method based on phoneme type"""
        f1, f2, f3, amp1, amp2, amp3, duration, ptype = params[:8]
        extra = params[8] if len(params) > 8 else {}
        
        if ptype == 'vowel':
            audio = self.synthesize_vowel(f1, f2, f3, amp1, amp2, amp3, duration)
        elif ptype == 'nasal':
            audio = self.synthesize_nasal(f1, f2, f3, amp1, amp2, amp3, duration)
        elif ptype == 'liquid':
            audio = self.synthesize_vowel(f1, f2, f3, amp1, amp2, amp3, duration)
        elif ptype == 'fricative':
            audio = self.synthesize_fricative(
                f1, f2, f3, amp1, amp2, amp3, duration,
                extra.get('voiced', False), extra.get('freq', 3000)
            )
        elif ptype == 'stop':
            audio = self.synthesize_stop(
                f1, f2, f3, amp1, amp2, amp3, duration,
                extra.get('voiced', False), extra.get('closure', 0.05),
                extra.get('freq', 2000)
            )
        elif ptype == 'affricate':
            audio = self.synthesize_affricate(
                f1, f2, f3, amp1, amp2, amp3, duration,
                extra.get('voiced', False), extra.get('closure', 0.04),
                extra.get('freq', 3000)
            )
        else:
            audio = np.zeros(int(self.sample_rate * duration))
        
        # Apply envelope
        fade_samples = min(int(0.005 * self.sample_rate), len(audio) // 4)
        if fade_samples > 0 and len(audio) > 0:
            envelope = np.ones(len(audio))
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            audio = audio * envelope
        
        return audio
    
    def synthesize(self, phonemes):
        """Synthesize a list of phonemes"""
        audio_segments = []
        
        for i, phoneme in enumerate(phonemes):
            # Remove stress markers (0, 1, 2) from CMU phonemes
            phoneme = phoneme.rstrip('012')
            
            if phoneme not in PHONEME_DATA:
                print(f"Warning: Unknown phoneme '{phoneme}', adding silence")
                audio_segments.append(np.zeros(int(self.sample_rate * 0.05)))
                continue
            
            params = PHONEME_DATA[phoneme]
            audio = self.synthesize_phoneme(params)
            audio_segments.append(audio)
        
        # Concatenate all segments
        if not audio_segments:
            return np.zeros(self.sample_rate)
        
        audio = np.concatenate(audio_segments)
        
        # Normalize
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.8
        
        return audio
    
    def pitch_shift(self, audio, percent):
        """
        Pitch shift audio by a given percentage.
        Positive percent = pitch up, Negative percent = pitch down.
        
        :param audio: input audio array
        :param percent: percentage to shift (e.g., 10 for 10% higher, -10 for 10% lower)
        :return: pitch-shifted audio
        """
        # Calculate pitch ratio
        if percent == 0.0:
            return audio

        ratio = 1.0 + (percent / 100.0)
        
        # Resample to change pitch (shorter = higher pitch, longer = lower pitch)
        new_length = int(len(audio) / ratio)
        return signal.resample(audio, new_length)
    
    def generate_silence(self, milliseconds):
        """Generate silence for specified duration in milliseconds"""
        duration_seconds = milliseconds / 1000.0
        num_samples = int(self.sample_rate * duration_seconds)
        return np.zeros(num_samples)
    
    def save_wav(self, audio, filename):
        """Save audio as WAV file"""
        audio_int = np.int16(audio * 32767)
        wavfile.write(filename, self.sample_rate, audio_int)
        print(f"Saved to {filename}")

    def play(self, audio, blocking=True):
        """Play audio directly through speakers"""
        sd.play(audio, self.sample_rate)
        if blocking:
            sd.wait()


if __name__ == "__main__":
    synth = FormantSynthesizer()
    
    test_words = {
        'this is dylans text to speech synthesizer': 'DH IH1 S IH1 Z D IH1 L AH0 N Z T EH1 K S T T UW1 S P IY1 CH S IH1 N TH AH0 S AY2 Z ER0'.split(),
        'sahara please set me free': 'S AH0 HH EH1 R AH0 P L IY1 Z S EH1 T M IY1 F R IY1'.split(),
        'its me five nights at freddys ar ar ar ar': 'IH1 T S M IY1 F AY1 V N AY1 T S AE1 T F R EH1 D IY0 Z AA1 R AA1 R AA1 R AA1 R'.split(),
    }
    
    for word, phonemes in test_words.items():
        print(f"Synthesizing: {word}")
        audio = synth.synthesize(phonemes)
        synth.save_wav(audio, f'test_word_files/{word}.wav')
    
    print("\nDone!")