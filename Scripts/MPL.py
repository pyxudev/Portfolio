import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from numpy.random import seed

class Perceptron(object):
	#パーセプトロン
	def __init__(self, eta = 0.01, n_iter = 10):
		self.eta = eta
		#学習率(0-1]
		self.n_iter = n_iter
		#学習回数

	def fit(self, X, y):
		"""トレーニングデーターに適合させる
		X　トレーニングデータ、配列構造
		y　目的変数、配列構造
		"""

		self.w_ = np.zeros(X.shape[1] + 1)
		#一次配列
		self.errors_ = []
		#リスト、誤差分類数

		for _ in range(self.n_iter):
			#トレーニングデータ反復
			errors = 0

			for xi, target in zip(X, y):
				update = self.eta * (target - self.predict(xi))
				#サンプルごとに重み更新
				self.w_[1:] += update * xi
				#重み更新
				self.w_[0] += update
				#w0の更新、⊿w=ρ(y^i-hy^i)		
				errors += int(update != 0.0)
				#更新が0以外のとき誤としてカウント

			self.errors_.append(errors)
			#反復ごとの誤差を収納

		return self

	def net_input(self, X):
		return np.dot(X, self.w_[1:]) + self.w_[0]
		#総入力

	def predict(self, X):
		return np.where(self.net_input(X) >= 0.0, 1, -1)
		#１ステップ後のクラスラベルを戻す

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header = None)
df.tail()

y = df.iloc[0:100, 4].values
#1-100行目の変数の抽出
y = np.where(y == 'Iris-setosa', -1, 1)
#Iris-setosaを-1,Iris-virginicaを1に変換
X = df.iloc[0:100, [0, 2]].values

plt.scatter(X[:50, 0], X[:50, 1], color = 'red', marker = 'o', label = 'setosa')
#品種setosaのプロット、赤O
plt.scatter(X[50:100, 0], X[50:100, 1], color = 'blue', marker = 'x', label = 'versicolor')
#品種versicolorのプロット、青X
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
#軸ラベルの設定
plt.legend(loc = 'upper left')
#凡例の設定
plt.show()

ppn = Perceptron(eta = 0.1, n_iter = 10)
#インスタンス化
ppn.fit(X, y)
#トレーニングデータへのモデル適合
plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker = 'o')
#エポックと誤分類誤差の関係の折れ線グラフをプロット
plt.xlabel('Epochs')
plt.ylabel('Number of misclassifications')
#軸グラフの設定
plt.show()

def plot_decision_regions(X, y, classifier, resolution = 0.02):
	markers = ('s', 'x', 'o', '^', 'v')
	colors = ('red', 'blue', 'lightgreen', 'gray', 'cray')
	cmap = ListedColormap(colors[:len(np.unique(y))])
	x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
	Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
	Z = Z.reshape(xx1.shape)
	plt.contourf(xx1, xx2, Z, alpha = 0.4, cmap = cmap)
	plt.xlim(xx1.min(), xx1.max())
	plt.ylim(xx2.min(), xx2.max())

	for idx, cl in enumerate(np.unique(y)):
		plt.scatter(x = X[y == cl, 0], y = X[y == cl, 1], alpha = 0.8, c = cmap(idx), marker = markers[idx], label = cl)

plot_decision_regions(X, y, classifier = ppn)
plt.xlabel('sepal length[cm]')
plt.ylabel('petal length[cm]')
plt.legend(loc = 'upper left')
plt.show()

class AdalineGD(object):
	def __init__(self, eta = 0.01, n_iter = 50):
		self.eta = eta
		self.n_iter = n_iter

	def fit(self, X, y):
		self.w_ = np.zeros(1 + X.shape[1])
		self.cost_ = []

		for i in range(self.n_iter):
			output = self.net_input(X)
			errors = (y - output)
			self.w_[1:] += self.eta * X.T.dot(errors)
			self.w_[0] += self.eta * errors.sum()
			cost = (errors ** 2).sum() / 2
			self.cost_.append(cost)

		return self

	def net_input(self, X):
		return np.dot(X, self.w_[1:]) + self.w_[0]

	def activation(self, X):
		return self.net_input(X)

	def predict(self, X):
		return np.where(self.activation(X) >= 0.0, 1, -1)

fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (8, 4))
ada1 = AdalineGD(n_iter = 10, eta = 0.01).fit(X, y)
ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker = 'o')
ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('log(sum-squared-error)')
ax[0].set_title('Adaline - Learning rate 0.01')
ada2 = AdalineGD(n_iter = 10, eta = 0.0001).fit(X, y)
ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker = 'o')
ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('log(sum-squared-error)')
ax[1].set_title('Adaline - Learning rate 0.0001')
plt.show()

X_std = np.copy(X)
X_std[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
X_std[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()

ada = AdalineGD(n_iter = 15, eta = 0.01)
ada.fit(X_std, y)
plot_decision_regions(X_std, y, classifier = ada)
plt.title('Adaline - Grandient Desecent')
plt.xlabel('sepal length [standaedized]')
plt.ylabel('petal length [standaedized]')
plt.legend(loc = 'upper left')
plt.show()

plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker = 'o')
plt.xlabel('Epochs')
plt.ylabel('sum-squared-error')
plt.show()

class AdalineSGD(object):
	def __init__(self, eta = 0.01, n_iter = 10, shuffle = True, random_state = None):
		self.eta = eta
		self.n_iter = n_iter
		self.w_initialized = False
		self.shuffle = shuffle

		if random_state:
			seed(random_state)

	def fit(self, X, y):
		self._initialize_weights(X.shape[1])
		self.cost_ = []

		for i in range(self.n_iter):
			
			if self.shuffle:
				X, y = self._shuffle(X, y)

			cost = []

			for xi, target in zip(X, y):
				cost.append(self._update_weights(xi, target))

			avg_cost = sum(cost) / len(y)
			self.cost_.append(avg_cost)

		return self

	def partial_fit(self, X, y):

		if not self.w_initialized:
			self.w_initialize_weights(X.shape[1])

		if y.ravel().shape[0] > 1:
			
			for xi, target in zip(X, y):
				self._initialize_weights(xi, target)

		else:
			self._update_weights(X, y)

		return self

	def _shuffle(self, X, y):
		r = np.random.permutation(len(y))

		return X[r], y[r]

	def _initialize_weights(self, m):
		self.w_ = np.zeros(1 + m)
		self.w_initialized = True

	def _update_weights(self, xi, target):
		output = self.net_input(xi)
		error = (target - output)
		self.w_[1:] += self.eta * xi.dot(error)
		self.w_[0] += self.eta * error
		cost = 0.5 * error**2

		return cost

	def net_input(self, X):

		return np.dot(X, self.w_[1:]) + self.w_[0]

	def activation(self, X):

		return self.net_input(X)

	def predict(self, X):

		return np.where(self.activation(X) >= 0.0, 1, -1)

ada = AdalineSGD(n_iter = 15, eta = 0.01, random_state = 1)
ada.fit(X_std, y)
plot_decision_regions(X_std, y, classifier = ada)
plt.title('Adaline - Stochastic Gradient Descent')
plt.xlabel('sepal length [standardize]')
plt.ylabel('petal length [standardize]')
plt.legend(loc = 'upper left')
plt.tight_layout()
plt.show()

plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker = 'o')
plt.xlabel('Epochs')
plt.ylabel('Average Cost')
plt.show()