import numpy as np
import time
import pandas as pd

from sklearn.metrics import confusion_matrix
import seaborn as sns

import matplotlib.pyplot as plt

px = 1 / plt.rcParams['figure.dpi']

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_prime(x):
    value = sigmoid(x)
    return value * (1 - value)


sigmoid_np = np.vectorize(sigmoid)
sigmoid_prime_np = np.vectorize(sigmoid_prime)


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)


def relu(x):
    return np.maximum(0, x);

relu_np = np.vectorize(relu)

def relu_prime(x):
    return np.where(x > 0, x, 0);

relu_prime_np = np.vectorize(relu_prime);


def cross_entropy(y_true, y_pred):
    epsilon = 1e-9
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    loss = -np.sum(y_true * np.log(y_pred)) / y_true.shape[0]
    return loss


# Neural Network class
class NeuralNetworkSigmoid:
    def __init__(self, layer_sizes, eta):
        self.layer_sizes = layer_sizes
        self.eta = eta

        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            self.weights.append(np.random.rand(layer_sizes[i], layer_sizes[i + 1]) - 0.5)
            self.biases.append(np.random.rand(layer_sizes[i + 1]) - 0.5)

    def forward(self, x):

        self.activations = [x]
        self.z_values = []

        for w, b in zip(self.weights, self.biases):
            z = self.activations[-1] @ w + b
            self.z_values.append(z)
            if w is self.weights[-1]:
                a = softmax(z)
            else:
                a = sigmoid_np(z)
            self.activations.append(a)

        return self.activations[-1]

    def backpropagation(self, x, y, p_off):
        self.forward(x)


        dropout_masks = [
            np.random.choice([0, 1], size=a.shape, p=[p_off, 1 - p_off])
            if i < len(self.activations) - 2 else np.ones_like(a)
            for i, a in enumerate(self.activations)
        ]


        delta = self.activations[-1] - y


        nabla_w = []
        nabla_b = []
        for i in reversed(range(len(self.weights))):
            nabla_w.insert(0, self.activations[i].T @ delta )
            nabla_b.insert(0, np.sum(delta, axis=0))

            if i > 0:
                delta = np.multiply( sigmoid_prime_np(self.z_values[i - 1]) , (delta @ self.weights[i].T)  )
                delta = np.multiply(delta, dropout_masks[i])


        for i in range(len(self.weights)):
            self.weights[i] -= self.eta * nabla_w[i]
            self.biases[i] -= self.eta * nabla_b[i]

    def train(self, x, y, dx_test, dy_test, epochs, batch_size, p_off):

        testing_error_arr=[];
        training_error_arr=[];
        index=[];

        df = pd.DataFrame({"": [0]}, index=[1]);
        df.plot();

        y_pred = np.argmax(self.forward(dx_test), axis=1);
        labels = np.argmax(dy_test, axis=1);
        """
        cf_matrix = confusion_matrix(y_pred, labels);
        
        sns.set(font_scale=0.1)
        sns.heatmap(cf_matrix / np.sum(cf_matrix), annot=True,
                    cmap='Blues', center=0, fmt='.2f', annot_kws={"size": 6},
                    cbar_kws={"shrink": 0.5, }).figure.savefig('confusion matrix heatmap_initial');
        """
        testing_error_arr=[ self.accuracy(dx_test, dy_test) ];
        training_error_arr=[ self.accuracy(x, y) ];
        index=[1];
        cnt = 0;
        for current_epoch in range( 1 , epochs + 1 ):
            """
            cnt += 1;
            if (cnt == 1):
                testing_error_arr.append(self.accuracy(dx_test, dy_test));
                training_error_arr.append(self.accuracy(x, y));
                index.append(len(index) + 1);

                df = pd.DataFrame({"": [0]}, index=[1]);
                df.plot();

                y_pred = np.argmax(self.forward(dx_test), axis=1);
                labels = np.argmax(dy_test, axis=1);
                
                cf_matrix = confusion_matrix(y_pred, labels);
                
                sns.set(font_scale=0.1)
                sns.heatmap(cf_matrix / np.sum(cf_matrix), annot=True,
                            cmap='Blues', center=0, fmt='.4f', annot_kws={"size": 6},
                            cbar_kws={"shrink": 0.5, }).figure.savefig('confusion matrix heatmap_secondary');
                """

            start_time = time.time()

            print(f"Epoch {current_epoch}")


            permutation = np.random.permutation(x.shape[0])
            x, y = x[permutation], y[permutation]


            batches_x = np.array_split(x, len(x) // batch_size)
            batches_y = np.array_split(y, len(y) // batch_size)



            for x_batch, y_batch in zip(batches_x, batches_y):
                self.backpropagation(x_batch, y_batch, p_off)


            end_time = time.time()
            acc = self.accuracy(dx_test, dy_test)

            testing_error_arr.append(acc);
            training_error_arr.append( self.accuracy(x, y) );
            index.append( int(len(index))+1 );

            print(f"Accuracy: {acc:.4f}")
            print(f"Time per epoch: {end_time - start_time:.2f}s")

            if acc >= 0.95:
                print("Achieved 95% accuracy. Stopping training.")
                break
        if (len(self.layer_sizes) > 2):
            True;
            # plt.figure(figsize=(640 * px, 480 * px))
            # df = pd.DataFrame({"testing Accuracy": testing_error_arr,
            #                    "training Accuracy": training_error_arr
            #                    },
            #                   index=index
            #                   );
            # fig = df.plot(title="Training Plot");
            # plt.savefig(
            #     'training_plot.png'
            # );
        else:
            True;
            # plt.figure(figsize=(640 * px, 480 * px))
            # df = pd.DataFrame({"testing Accuracy": testing_error_arr,
            #                    "training Accuracy": training_error_arr
            #                    },
            #                   index=index
            #                   );
            # fig = df.plot(title="Training Plot");
            # plt.savefig(
            #     'training_plot_no_hidden.png'
            # );

        y_pred = np.argmax(self.forward(dx_test), axis=1);
        labels = np.argmax(dy_test, axis=1);
        cf_matrix = confusion_matrix(y_pred, labels);

        print( len( y_pred[ y_pred == 4 ] ) )

        if(len(self.layer_sizes)>2 ):
            True;
            # sns.set(font_scale=0.1)
            # fig=sns.heatmap(cf_matrix / np.sum(cf_matrix), annot=True,
            #             cmap='Blues', center=0, fmt='.3f',annot_kws={"size": 6},   cbar_kws={"shrink": 0.5, } );
            # plt.savefig('confusion_matrix_heatmap.png');
        else:
            True;
            # sns.set(font_scale=0.1)
            # fig=sns.heatmap(cf_matrix / np.sum(cf_matrix), annot=True,
            #             cmap='Blues', center=0, fmt='.3f', annot_kws={"size": 6},
            #             cbar_kws={"shrink": 0.5, });
            # plt.savefig('confusion_matrix_heatmap_no_hidden.png');
    def accuracy(self, x, y):
        predictions = np.argmax(self.forward(x), axis=1)
        labels = np.argmax(y, axis=1)
        return np.mean(predictions == labels)

    def compute_loss(self, y_true, y_pred):
        return cross_entropy(y_true, y_pred);



def normalize(dx):
  a=dx.min()
  b=dx.max()
  dx = (dx-a)/(b-a)
  return dx;


def one_hot_encode(y, number):
  newDy = np.zeros((y.size, number));
  newDy[np.arange(y.size), y] = 1;
  return newDy;