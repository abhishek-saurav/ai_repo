import tensorflow as tf
import matplotlib.pyplot as plt

print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("Training samples : " + str(x_train.shape[0]))
print("Test samples     : " + str(x_test.shape[0]))

print("Normalizing data...")
x_train = x_train / 255.0
x_test = x_test / 255.0

print("Building model...")
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation="relu"))
model.add(tf.keras.layers.Dense(10, activation="softmax"))

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training model...")
model.fit(x_train, y_train, epochs=5)

print("Evaluating model...")
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy: " + str(test_acc))

print("Making predictions...")
predictions = model.predict(x_test)

print("Displaying first image and prediction...")
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.title("Predicted: " + str(predictions[0].argmax()))
plt.show()
