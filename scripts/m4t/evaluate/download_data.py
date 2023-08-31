# Copyright (c) Meta Platforms, Inc. and affiliates
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import logging
import os
from seamless_communication.datasets.huggingface import Speech2SpeechFleursDatasetBuilder
import torch


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s -- %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def make_directories(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def download_datasets(languages, num_datasets_per_language, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for lang in languages:
        lang_output_dir = os.path.join(output_directory, lang)
        lang_source_audio_dir = os.path.join(lang_output_dir, 'source_audio')
        lang_target_text_dir = os.path.join(lang_output_dir, 'target_text')
        lang_source_text_dir = os.path.join(lang_output_dir, 'source_text')
        lang_target_audio_dir = os.path.join(lang_output_dir, 'target_audio')

        make_directories(
            lang_output_dir,
            lang_source_audio_dir,
            lang_target_text_dir,
            lang_source_text_dir,
            lang_target_audio_dir
        )

        logger.info(f"Downloading datasets for language: {lang}")

        dataset_builder = Speech2SpeechFleursDatasetBuilder(
            source_lang=lang,
            target_lang=lang,
            split="test",
            skip_source_audio=False,
            skip_target_audio=False,
            audio_dtype=torch.float32,
            dataset_cache_dir=None,
            speech_tokenizer=None,
        )

        dataset_count = 0

        for lang_pair_sample in dataset_builder:
            source_sample = lang_pair_sample.source
            target_sample = lang_pair_sample.target

            #TODO Figure out how to save audio files correctly
            source_audio = source_sample.waveform.numpy().tobytes()
            target_audio = target_sample.waveform.numpy().tobytes()

            source_text = source_sample.text
            target_text = target_sample.text

            source_audio_path = os.path.join(lang_source_audio_dir, f"source_{dataset_count}.wav")
            target_audio_path = os.path.join(lang_target_audio_dir, f"target_{dataset_count}.wav")

            source_text_path = os.path.join(lang_source_text_dir, f"source_{dataset_count}.txt")
            target_text_path = os.path.join(lang_target_text_dir, f"target_{dataset_count}.txt")

            with open(source_audio_path, 'wb') as source_file:
                source_file.write(source_audio)

            with open(target_audio_path, 'wb') as target_file:
                target_file.write(target_audio)

            with open(source_text_path, 'w') as source_file:
                source_file.write(source_text)

            with open(target_text_path, 'w') as target_file:
                target_file.write(target_text)

            logger.info(f"Dataset {dataset_count} - Source Audio Path: {source_audio_path}")
            logger.info(f"Dataset {dataset_count} - Source Language: {source_sample.lang}")
            logger.info(f"Dataset {dataset_count} - Target Language: {target_sample.lang}")
            logger.info(f"Dataset {dataset_count} - Target Text: {target_text}")
            print("=" * 100)

            dataset_count += 1
            if dataset_count >= num_datasets_per_language:
                break

        logger.info(f"Downloaded and saved {dataset_count} datasets for language: {lang}")
        print("=" * 100)
# Languages : Hindi & Afrikaans

languages = ["hi_in", 'af_za']
num_datasets_per_language = 10
output_directory = "./downloaded_data"

download_datasets(languages, num_datasets_per_language, output_directory)
