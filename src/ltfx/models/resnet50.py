from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Input


def build_resnet50(height, width, n_classes):
    # Get base model
    base_model = ResNet50(include_top=False, weights="imagenet",
                          input_tensor=Input(name='image_xf_input', shape=(height, width, 3)))

    # Add final layers
    x = base_model.output
    x = Flatten()(x)
    predictions = Dense(n_classes, activation='softmax', name='fc6')(x)

    # This is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)

    return model


