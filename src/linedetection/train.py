import tensorflow as tf
from tensorflow import keras
import processdata
import numpy as np

x_train, y_train = processdata.picdata()

x_val = x_train[108:30]
x_train = x_train[0:108]

y_val = y_train[108:30]
y_train = y_train[0:108]

y_train = np.asarray(y_train).astype('int8').reshape((-1,1))
y_val = np.asarray(y_val).astype('int8').reshape((-1,1))

# (x_train, y_train), (x_val, y_val) = keras.datasets.fashion_mnist.load_data()
# print(x_val[0])
def preprocess(x, y):
  x = tf.cast(x, tf.float32) / 255.0
  y = tf.cast(y, tf.int64)

  return x, y

def create_dataset(xs, ys, n_classes=6):
  ys = tf.one_hot(ys, depth=n_classes)
  return tf.data.Dataset.from_tensor_slices((xs, ys)) \
    .map(preprocess) \
      .batch(18)
    # .shuffle(len(ys)) \
    

print(np.shape(x_train))
train_dataset = create_dataset(x_train, y_train)
val_dataset = create_dataset(x_val, y_val)

print("Traindataset")
print(train_dataset)
print(np.shape(train_dataset))

model = keras.Sequential([
    keras.layers.Reshape((960, 400), input_shape=(960,400)),
    keras.layers.Dense(units=256, activation='relu'),
    keras.layers.Dense(units=192, activation='relu'),
    keras.layers.Dense(units=128, activation='relu'),
    kera  .layers.Dense(units=6, activation='softmax')
])

model.compile(optimizer='adam', 
              loss=tf.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(
    train_dataset.repeat(), 
    epochs=10, 
    steps_per_epoch=500,
    validation_data=val_dataset.repeat(), 
    validation_steps=2
)

predictions = model.predict(val_dataset)
model.summary()

print(np.argmax(predictions[0]))


