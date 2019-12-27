import os


class ClassificationConfig:
    RAW_IMAGE_KEY = os.environ.get("IMAGE_COLUMN_NAME", 'image')
    RAW_LABEL_KEY = os.environ.get("LABEL_COLUMN_NAME", 'label')

    IMAGE_KEY = RAW_IMAGE_KEY + '_xf_input'
    LABEL_KEY = RAW_LABEL_KEY + '_xf_input'

    IMAGE_HEIGHT = int(os.environ.get("IMAGE_HEIGHT", 256))
    IMAGE_WIDTH = int(os.environ.get("IMAGE_WIDTH", 256))
    NUMBER_OF_CLASSES = int(os.environ.get('NUMBER_OF_CLASSES', 6))
    MODEL_NAME = os.environ.get('MODEL_NAME', 'image-type')
    TRAIN_BATCH_SIZE = int(os.environ.get('TRAIN_BATCH_SIZE', 4))
    EVAL_BATCH_SIZE = int(os.environ.get('EVAL_BATCH_SIZE', 2))
