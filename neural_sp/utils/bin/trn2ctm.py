#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 Kyoto University (Hirofumi Inaguma)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"Convert a trn file to a ctm file based on a stm segmentation."

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('trn', type=str,
                    help='trn file')
parser.add_argument('--stm', type=str,
                    help='stm file')
args = parser.parse_args()


def main():

    stm_segments = {}
    with open(args.stm, 'r') as f:
        for line in f:
            line = line.strip()

            if line[0] == ';':
                continue

            speaker = line.split()[0]
            start_t = float(line.split()[3])
            end_t = float(line.split()[4])
            if speaker not in stm_segments.keys():
                stm_segments[speaker] = {}
            stm_segments[speaker][start_t] = end_t

    with open(args.trn, 'r') as f:
        for line in f:
            # line = unicode(line, 'utf-8').strip()
            line = line.strip()
            words = line.split()[:-1]
            utt_id = line.split()[-1].replace('(', '').replace(')', '')
            speaker = '_'.join(utt_id.split('-')[0].split('_')[:-1])
            channel = utt_id.split('-')[0].split('_')[-1]
            start_f, end_f = utt_id.split('-')[1:]
            start_t = round(int(start_f) / 100, 2)
            # end_t = round(int(end_f) / 100, 2)

            # Fix end time based on the stm file
            if start_t in stm_segments[speaker].keys():
                end_t = stm_segments[speaker][start_t]
            else:
                end_t = stm_segments[speaker][round(start_t + 0.01, 2)]

            duration_t = end_t - start_t
            if len(words) > 0:
                duration_t /= len(words)

            assert channel in ['A', 'B']
            conf = 1.  # dummy

            for w in words:
                print('%s %s %.2f %.2f %s %.3f' % (speaker, channel, start_t, duration_t, w, conf))
                start_t += duration_t


if __name__ == '__main__':
    main()
