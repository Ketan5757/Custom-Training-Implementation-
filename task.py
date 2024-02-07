import tensorflow as tf
import numpy as np
import os

## Replace {your-gcs-bucket} !!
BUCKET_ROOT = '/gcs/project-kohn-11014674'

# Define variables
NUM_CLASSES = 5
EPOCHS = 10
BATCH_SIZE = 32

IMG_HEIGHT = 180
IMG_WIDTH = 180

DATA_DIR = f'{BUCKET_ROOT}/flower_photos'


def create_datasets(data_dir, batch_size):
    '''Creates train and validation datasets.'''

    train_dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=batch_size)

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=batch_size)

    train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
    validation_dataset = validation_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_dataset, validation_dataset


def create_model():
    '''Creates model.'''

    model = tf.keras.Sequential([
        tf.keras.layers.Resizing(IMG_HEIGHT, IMG_WIDTH),
        tf.keras.layers.Rescaling(1. / 255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    return model


# CREATE DATASETS
train_dataset, validation_dataset = create_datasets(DATA_DIR, BATCH_SIZE)

# CREATE/COMPILE MODEL
model = create_model()
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# TRAIN MODEL
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)

# SAVE MODEL
model.save(f'{BUCKET_ROOT}/model_output')