from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Input


def build_resnet50(input_name: str, image_height: int, image_width: int, number_of_classes: int,
                   weights: str = "imagenet"):
    # Get base model
    base_model = ResNet50(include_top=False, weights=weights,
                          input_tensor=Input(name=input_name, shape=(image_height, image_width, 3)))

    # Add final layers
    x = base_model.output
    x = Flatten()(x)
    layer_name = "fc%d" % number_of_classes
    predictions = Dense(number_of_classes, activation='softmax', name=layer_name)(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    return model


