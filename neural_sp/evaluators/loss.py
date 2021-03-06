#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 Kyoto University (Hirofumi Inaguma)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"""Evaluate a model by loss."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tqdm import tqdm


def eval_loss(models, dataset, decode_params, progressbar=False):
    """Evaluate a model by loss.

    Args:
        models (list): the models to evaluate
        dataset: An instance of a `Dataset' class
        decode_params (dict):
        progressbar (bool): if True, visualize the progressbar
    Returns:
        loss_mean (float): average loss

    """
    # Reset data counter
    dataset.reset()

    model = models[0]
    # TODO(hirofumi): ensemble decoding

    total_loss = 0
    if progressbar:
        pbar = tqdm(total=len(dataset))
    while True:
        batch, is_new_epoch = dataset.next(decode_params['batch_size'])

        assert not dataset.is_test
        loss, loss_acc_fwd, loss_acc_bwd, loss_acc_sub = model(
            batch['xs'], batch['ys'], batch['ys_sub'], is_eval=True)

        total_loss += loss.item() * len(batch['utt_ids'])

        if progressbar:
            pbar.update(len(batch['utt_ids']))

        if is_new_epoch:
            break

    if progressbar:
        pbar.close()

    # Reset data counters
    dataset.reset()

    loss_mean = total_loss / len(dataset)

    return loss_mean
