from __future__ import annotations
import os
import yaml
from absl import logging
from dataclasses import dataclass


@dataclass
class ClassificationConfig:
    raw_image_key: str = 'image'
    raw_label_key: str = 'label'
    image_key: str = 'image_tf'
    label_key: str = 'label_tf'
    image_width: int = 256
    image_height: int = 256
    number_of_classes: int = 2
    model_name: str = 'classification_model'
    pretrained: str = 'imagenet'
    train_batch_size: int = 32
    train_steps: int = 10
    eval_batch_size: int = 8
    eval_steps: int = 5


    @classmethod
    def from_env(cls) -> ClassificationConfig:
        try:
            filename = os.environ['LTFX_CONFIG_FILE']
            return cls.from_file(filename)
        except KeyError as e:
            logging.error("Unable to read file from env " + str(e))
        return cls()


    @classmethod
    def from_file(cls, filename) -> ClassificationConfig:
        logging.info("Reading configuration from file %s" % filename)
        with open(filename, 'r') as fp:
            config = yaml.load(fp)

        os.environ['LTFX_CONFIG_FILE'] = filename
        classification_config = cls()

        for key, value in config.get('model', {}).items():
            if hasattr(classification_config, key) and getattr(classification_config, key, None) is not None:
                old_value = getattr(classification_config, key, None)
                logging.info("Overriding config value key {} from {} to {}".format(key, old_value, value))
            setattr(classification_config, key, value)

        logging.info("Config loaded!!")
        return classification_config
