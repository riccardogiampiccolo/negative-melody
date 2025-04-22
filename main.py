import os
import argparse
import numpy as np
from collections import deque
import pretty_midi as pm
from typing import List, Optional
import warnings

warnings.filterwarnings("ignore")


def get_negative_note(note: pm.Note, fa_oct: int, mode: str, scale_labels: List[str], verbose=False):
    nt_name_oct = pm.note_number_to_name(note.pitch)
    nt_name = nt_name_oct[:-1]
    nt_oct = int(nt_name_oct[-1])
    if 'b' in nt_name:
        nt_name = nt_name[:-1] + '#'

    num_semitones = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])  # num of semitones wrt tonic
    dict_notes = {**{scale_labels[i]: num_semitones[i] for i in range(12)}}

    s = scale_labels.index(nt_name)
    dist = np.abs(s - 3.5)
    num_semitones_neg = 3.5 + dist if s < 3.5 else 3.5 - dist  # always wrt to tonic
    neg_label = list(dict_notes.keys())[list(dict_notes.values())[int(num_semitones_neg)]]

    # dist_to_oct_neg = dict_notes[neg_label] - dict_notes[nt_name]
    # dist_to_neg = dist_to_oct_neg
    dist_to_neg = 7 - 2 * s
    if dict_notes['C'] < 3.5:
        if s < dict_notes['C']:
            dist_to_oct_neg = - 5 - 2 * s
        elif 8 - dict_notes['C'] > s >= dict_notes['C']:
            dist_to_oct_neg = dist_to_neg
        elif s >= 8 - dict_notes['C']:
            dist_to_oct_neg = 19 - 2 * s

    elif 3.5 < dict_notes['C'] <= 7:
        if s <= 7 - dict_notes['C']:
            dist_to_oct_neg = - 5 - 2 * s
        elif dict_notes['C'] > s > 7 - dict_notes['C']:
            dist_to_oct_neg = dist_to_neg
        elif s >= dict_notes['C']:
            dist_to_oct_neg = 19 - 2 * s

    elif 11 > dict_notes['C'] > 7:
        if s < dict_notes['C']:
            dist_to_oct_neg = dist_to_neg
        elif 19 - dict_notes['C'] >= s >= dict_notes['C']:
            dist_to_oct_neg = 19 - 2 * s
        elif s > 19 - dict_notes['C']:
            dist_to_oct_neg = 31 - 2 * s

    elif dict_notes['C'] == 11:
        if s <= 8:
            dist_to_oct_neg = dist_to_neg
        elif dict_notes['C'] > s > 8:
            dist_to_oct_neg = 19 - 2 * s
        elif s >= dict_notes['C']:
            dist_to_oct_neg = 31 - 2 * s

    dist_to_nneg = 12 + dist_to_oct_neg
    dist_to_pneg = - (12 - dist_to_oct_neg)
    deltas_to_neg = np.array([dist_to_oct_neg, dist_to_pneg, dist_to_nneg])

    dist_to_axis = 3.5 - dict_notes[nt_name]
    dist_to_naxis = 12 + dist_to_axis
    dist_to_paxis = - (12 - dist_to_axis)
    deltas_to_axis = np.array([dist_to_axis, dist_to_paxis, dist_to_naxis])

    dist_oct = fa_oct - nt_oct

    if mode == 'le':
        delta_pitch = dist_to_neg
    elif mode == 'so':
        delta_pitch = dist_to_oct_neg
    elif mode == 'fa':
        delta_pitch = dist_to_neg + 24 * dist_oct
    elif mode == 'cn':
        delta_pitch = deltas_to_neg[np.abs(deltas_to_neg).argmin()]
    elif mode == 'ca':
        # delta_pitch = deltas_to_neg[np.abs(deltas_to_axis).argmin()]
        delta_pitch = int(2 * deltas_to_axis[np.abs(deltas_to_axis).argmin()])

    if verbose:
        print(f'The negative of {nt_name} is {neg_label}')
        print(f'|--- Current root: {scale_labels[0]}')
        print(f'|--- Current negative mode: {mode}')
        print(f'|--- Current scale: {scale_labels}')
        print(f'|--- Distance to !axis: {dist_to_axis}')
        print(f'|--- Distance to previous !axis: {dist_to_paxis}')
        print(f'|--- Distance to next !axis: {dist_to_naxis}')
        print(f'|--- Distance to !note: {dist_to_oct_neg}')
        print(f'|--- Distance to previous !note: {dist_to_pneg}')
        print(f'|--- Distance to next !note: {dist_to_nneg}')
        print(f'|--- Distance between octaves: {dist_oct}')
        print(f'|------ Delta pitch: {delta_pitch}\n')

    return delta_pitch, neg_label


def main(midi_name: str = None, generator: str = None, fa_oct: Optional[int] = None, mode: str = 'ca'):
    if not os.path.isdir('neg'):
        os.mkdir('neg')

    midi_path = 'midi/' + midi_name
    print(f'Input MIDI file: {midi_path}')

    mid = pm.PrettyMIDI(midi_path)

    # ----- Negative ----- #

    note_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    C_chromatic_scale = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    dict_notes = {**{note_labels[i]: C_chromatic_scale[i] for i in range(12)}}

    shift = dict_notes['C'] - dict_notes[generator]
    notes_shifted = deque(note_labels)
    notes_shifted.rotate(shift)

    # Create a copy of the midi stream
    neg_mid = mid

    for inst in range(len(neg_mid.instruments)):
        if neg_mid.instruments[inst].is_drum is not True:
            for idx, nt in enumerate(mid.instruments[inst].notes):
                delta_pitch, neg_label = get_negative_note(note=nt, fa_oct=fa_oct, mode=mode,
                                                           scale_labels=list(notes_shifted), verbose=False)
                neg_note_pitch = nt.pitch + delta_pitch
                if neg_note_pitch < 0 or neg_note_pitch > 127:
                    neg_note_pitch = 1
                neg_mid.instruments[inst].notes[idx].pitch = neg_note_pitch

    neg_mid.write(f'neg/neg_fa_O={fa_oct}_{midi_name}' if mode == 'fa' else f'neg/neg_{mode}_{midi_name}.mid')

    print('*** Process completed! ***')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--mode', type=str, default='ca')
    parser.add_argument('-m', '--midi', type=str, default='')
    parser.add_argument('-g', '--generator', type=str, default='C')
    parser.add_argument('-o', '--octave', type=int, default=4)

    args = vars(parser.parse_args())
    print(args)

    if args['mode'] not in ['ca', 'cn', 'le', 'fa', 'so']:
        raise RuntimeError('Mode not recognized! Use: \'le\', \'fa\', \'so\', \'ca\', or \'cn\'.')
    if args['octave'] not in np.arange(11):
        raise RuntimeError('Octave not recognized! Octave should be an integer between 0 and 10.')
    if args['generator'] not in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
        raise RuntimeError('Generator not recognized! Use a generator in the set [\'C\', \'C#\', \'D\', \'D#\', \'E\','
                           ' \'F\', \'F#\', \'G\', \'G#\', \'A\', \'A#\', \'B\'].')

    main(midi_name=args['midi'],
         generator=args['generator'],
         fa_oct=args['octave'],
         mode=args['mode'])
