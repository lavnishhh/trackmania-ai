import pandas as pd
import tensorflow as tf

# Load data
df = pd.read_csv("data_cleaned.csv")

del df['prev_input']

# Split data
train_df = df.sample(frac=0.8, random_state=0)
test_df = df.drop(train_df.index)

# label to value
train_labels = pd.get_dummies(train_df["input"]).values
test_labels = pd.get_dummies(test_df["input"]).values

# inputs
train_inputs = train_df.drop("input", axis=1).values
test_inputs = test_df.drop("input", axis=1).values

# Create a sequential model in tensorflow
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(train_inputs.shape[1], activation="relu", input_shape=(train_inputs.shape[1],)))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(2, activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(train_inputs, train_labels, epochs=30, batch_size=32)
test_loss, test_acc = model.evaluate(test_inputs, test_labels)
print("Test accuracy:", test_acc)

model.save('model.h5')
