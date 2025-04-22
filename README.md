# On the Application of Negative Harmony to Melody for Symbolic Music Processing

![Project Icon](assets/icon.png)

This repository contains the accompanying code for the paper "**On the Application of Negative Harmony to Melody for Symbolic Music Processing**," authored by R. Giampiccolo, A. Bernardini, and A. Sarti, and accepted for pubblication in _Computer Music Journal_. This research explores the concept of negative harmony, a theoretical framework for inverting harmonic structures, and applies it to melody for symbolic music processing unveiling the not-bijective nature of the transformation. We present different algorithms that transform melodies by mirroring them around a specific reciprocation axis within a specified key, generating novel musical ideas and variations. Our experiments demonstrate the potential of negative harmony as a creative tool in music composition and analysis.

## Abstract

Many composers and musicians are employing the theory of negative harmony for rekindling their music, sometimes even unconsciously. Quite surprisingly, this theory is not discussed yet in the field of music processing. In this paper, we address and present negative harmony from a mathematical perspective, considering it as a geometric transformation applied to the pitch space. We then analyze, for the first time, how it is possible to derive negative melodies, unveiling the not-bijective nature of the transformation. Our discussion is corroborated with examples drawn from diverse musical genres and forms, such as chorales and piano performances, offering new insights with the ultimate goal of fostering creativity. Finally, we develop and make freely available an audio plug-in that applies such transformations in real-time as a creative tool for musicians and composers who want to delve into and take inspiration from the "dark side of harmony."

## Code

The code implementing the proposed algorithm for applying negative harmony to melodies is provided in this repository. It includes:

- **Melody Processing Scripts**: Scripts to process symbolic music files (e.g., MIDI) and apply the negative harmony transformations.
- **Examples and Demos**: Example melodies and their negative harmony transformations are available on our [GitHub page](https://riccardogiampiccolo.github.io/negative-melody/).

### Requirements

- Python 3.8+
- Required packages:
  - numpy
  - pretty_midi

### Usage

In order to reciprocate a given MIDI file, you can use the following line of code in your terminal:

`python main.py [-m MIDI_FILE_NAME.mid] [-g GENERATOR] [-o OCTAVE] [--mode MODE]`

**Modes**

| Mode | Name                | Description                                                                 | Parameters Required          |
|------|---------------------|-----------------------------------------------------------------------------|------------------------------|
| `le` | Levy                | Reciprocation according to Levy's theory                                    | `-m`, `-g`, `--mode`         |
| `fa` | Fixed Axis          | Reciprocation with respect to a fixed axis                                  | `-m`, `-g`, `-o`, `--mode`   |
| `so` | Same Octave         | Reciprocation to obtain the negative in the same octave                     | `-m`, `-g`, `--mode`         |
| `cn` | Closest Negative    | Reciprocation to obtain the closest negative                                | `-m`, `-g`, `--mode`         |
| `ca` | Closeset Axis       | Reciprocation with respect to the closest axis                              | `-m`, `-g`, `--mode`         |

**Options**

| Short | Long Form     | Type   | Values/Range                          | Default | Description                          |
|-------|---------------|--------|---------------------------------------|---------|--------------------------------------|
| `-m`  | `--midi`      | string | Valid MIDI file name contained in the "midi" folder                       | `""`    | Input MIDI file path                 |
| `-g`  | `--generator` | string | `C`, `C#`, `D`, `D#`, `E`, `F`, `F#`,<br>`G`, `G#`, `A`, `A#`, `B` | `"C"` | Root musical key                  |
| `-o`  | `--octave`    | int    | `0`-`10`                              | `4`     | Output octave                        |
|       | `--mode`      | string | `ca`, `cn`, `le`, `fa`, `so`          | `"ca"`  | Generation algorithm (required)      |


### Error Conditions

The script will raise errors for:
- Invalid mode selection
- Octave outside 0-10 range
- Invalid musical key specification
- Missing input file (when specified)


## Audio Plug-in

In addition to the algorithm, we have developed an audio plug-in that applies the proposed symbolic music processing algorithms in real-time. This plug-in allows musicians and composers to experiment with negative harmony directly within their digital audio workstations (DAWs). The plug-in features:

- **Real-time Processing**: Apply negative harmony transformations to live input or pre-recorded tracks.
- **Customizable Parameters**: Adjust the central axis, key, and other parameters to tailor the harmonic inversion to specific needs.
- **User-friendly Interface**: An intuitive interface for easy integration into existing workflows.

The audio plug-in will be made available upon pubblication of the paper.

For further details and updates, please refer to the documentation and release notes in this repository. Thank you for your interest in our work!
