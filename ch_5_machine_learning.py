# %%
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_digits
from sklearn.manifold import Isomap
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import validation_curve
from sklearn.model_selection import learning_curve
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import nan
from sklearn.impute import SimpleImputer
from sklearn.datasets import make_blobs
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
# from scipy import stats

# %%
iris = sns.load_dataset("iris")
iris.head()

# %%
sns.pairplot(iris, hue="species", size=1.5)

# %%
X_iris = iris.drop("species", axis=1)
X_iris.shape

# %%
y_iris = iris["species"]
y_iris.shape

# %%
rng = np.random.RandomState(42)
x = 10 * rng.rand(50)
y = 2 * x - 1 + rng.randn(50)
plt.scatter(x, y)

# %%
model = LinearRegression(fit_intercept=True)
model

# %%
X = x[:, np.newaxis]
X.shape

# %%
model.fit(X, y)

# %%
model.coef_

# %%
model.intercept_

# %%
xfit = np.linspace(-1, 11)

# %%
Xfit = xfit[:, np.newaxis]
yfit = model.predict(Xfit)

# %%
plt.scatter(x, y)
plt.plot(xfit, yfit)

# %%
Xtrain, Xtest, ytrain, ytest = train_test_split(X_iris, y_iris, random_state=1)

# %%
model = GaussianNB()
model.fit(Xtrain, ytrain)
y_model = model.predict(Xtest)

# %%
accuracy_score(ytest, y_model)

# %%
model = PCA(n_components=2)
model.fit(X_iris)
X_2D = model.transform(X_iris)

# %%
iris["PCA1"] = X_2D[:, 0]
iris["PCA2"] = X_2D[:, 1]
sns.lmplot("PCA1", "PCA2", hue="species", data=iris, fit_reg=False)

# %%
model = GaussianMixture(n_components=3, covariance_type="full")
model.fit(X_iris)
y_gmm = model.predict(X_iris)

# %%
iris["cluster"] = y_gmm
sns.lmplot("PCA1", "PCA2", data=iris, hue="species", col="cluster", fit_reg=False)

# %%
digits = load_digits()
digits.images.shape

# %%
fig, axes = plt.subplots(
    10,
    10,
    figsize=(8, 8),
    subplot_kw={"xticks": [], "yticks": []},
    gridspec_kw=dict(hspace=0.1, wspace=0.1),
)

for i, ax in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap="binary", interpolation="nearest")
    ax.text(0.5, 0.5, str(digits.target[i]), transform=ax.transAxes, color="green")


# %%
X = digits.data
X.shape

# %%
y = digits.target
y.shape

# %%
iso = Isomap(n_components=2)
iso.fit(digits.data)
data_projected = iso.transform(digits.data)
data_projected.shape

# %%
plt.scatter(
    data_projected[:, 0],
    data_projected[:, 1],
    c=digits.target,
    edgecolor="none",
    alpha=0.5,
    cmap=plt.cm.get_cmap("icefire", 10),
)
plt.colorbar(label="digit label", ticks=range(10))
plt.clim(-0.5, 9.5)

# %%
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)

# %%
model = GaussianNB()
model.fit(Xtrain, ytrain)
y_model = model.predict(Xtest)

# %%
accuracy_score(ytest, y_model)

# %%
mat = confusion_matrix(ytest, y_model)

sns.heatmap(mat, square=True, annot=True, cbar=False)
plt.xlabel("predicted value")
plt.ylabel("true value")

# %%
fig, axes = plt.subplots(
    10,
    10,
    figsize=(8, 8),
    subplot_kw={"xticks": [], "yticks": []},
    gridspec_kw=dict(hspace=0.1, wspace=0.1),
)

for i, ax in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap="binary", interpolation="nearest")
    ax.text(
        0.5,
        0.5,
        str(y_model[i]),
        transform=ax.transAxes,
        color="green" if (ytest[i] == y_model[i]) else "red",
    )

# %%
iris = load_iris()
X = iris.data
y = iris.target

# %%
model = KNeighborsClassifier(n_neighbors=1)


# %%
model.fit(X, y)
y_model = model.predict(X)

# %%
accuracy_score(y, y_model)

# %%
X1, X2, y1, y2 = train_test_split(X, y, random_state=0, train_size=0.5)

model.fit(X1, y1)

y2_model = model.predict(X2)
accuracy_score(y2, y2_model)

# %%
y2_model = model.fit(X1, y1).predict(X2)
y1_model = model.fit(X2, y2).predict(X1)
accuracy_score(y1, y1_model), accuracy_score(y2, y2_model)

# %%
cross_val_score(model, X, y, cv=5)

# %%
scores = cross_val_score(model, X, y, cv=LeaveOneOut())
scores

# %%
scores.mean()

# %%


def PolynomialRegression(degree=2, **kwargs):
    return make_pipeline(PolynomialFeatures(degree), LinearRegression(**kwargs))


# %%
def make_data(N, err=1.0, rseed=1):
    rng = np.random.RandomState(rseed)
    X = rng.rand(N, 1) ** 2
    y = 10 - 1.0 / (X.ravel() + 0.1)
    if err > 0:
        y += err * rng.randn(N)
    return X, y


X, y = make_data(40)

# %%
X_test = np.linspace(-0.1, 1.1, 500)[:, None]

plt.scatter(X.ravel(), y, color="black")
axis = plt.axis()
for degree in [1, 3, 5]:
    y_test = PolynomialRegression(degree).fit(X, y).predict(X_test)
    plt.plot(X_test.ravel(), y_test, label="degree={0}".format(degree))
plt.xlim(-0.1, 1.0)
plt.ylim(-2, 12)
plt.legend(loc="best")

# %%
degree = np.arange(0, 21)
train_score, val_score = validation_curve(
    PolynomialRegression(), X, y, "polynomialfeatures__degree", degree, cv=7
)

plt.plot(degree, np.median(train_score, 1), color="blue", label="training score")
plt.plot(degree, np.median(val_score, 1), color="red", label="validation score")
plt.legend(loc="best")
plt.ylim(0, 1)
plt.xlabel("degree")
plt.ylabel("score")

# %%
plt.scatter(X.ravel(), y)
lim = plt.axis()
y_test = PolynomialRegression(3).fit(X, y).predict(X_test)
plt.plot(X_test.ravel(), y_test)
plt.axis(lim)

# %%
X2, y2 = make_data(200)
plt.scatter(X2.ravel(), y2)

# %%
degree = np.arange(21)
train_score2, val_score2 = validation_curve(
    PolynomialRegression(), X2, y2, "polynomialfeatures__degree", degree, cv=7
)

plt.plot(degree, np.median(train_score2, 1), color="blue", label="training score")
plt.plot(degree, np.median(val_score2, 1), color="red", label="validation score")
plt.plot(degree, np.median(train_score, 1), color="blue", alpha=0.3, linestyle="dashed")
plt.legend(loc="lower center")
plt.ylim(0, 1)
plt.xlabel("degree")
plt.ylabel("score")

# %%
fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)

for i, degree in enumerate([2, 9]):
    N, train_lc, val_lc = learning_curve(
        PolynomialRegression(degree), X, y, cv=7, train_sizes=np.linspace(0.3, 1, 25)
    )

ax[i].plot(N, np.mean(train_lc, 1), color="blue", label="training score")
ax[i].plot(N, np.mean(val_lc, 1), color="red", label="validation score")
ax[i].hlines(
    np.mean([train_lc[-1], val_lc[-1]]), N[0], N[-1], color="gray", linestyle="dashed"
)

ax[i].set_ylim(0, 1)
ax[i].set_xlim(N[0], N[-1])
ax[i].set_xlabel("training size")
ax[i].set_ylabel("score")
ax[i].set_title("degree = {0}".format(degree), size=14)
ax[i].legend(loc="best")

# %%
param_grid = {
    "polynomialfeatures__degree": np.arange(21),
    "linearregression__fit_intercept": [True, False],
    "linearregression__normalize": [True, False],
}

grid = GridSearchCV(PolynomialRegression(), param_grid, cv=7)

# %%
grid.fit(X, y)

# %%
grid.best_params_

# %%
model = grid.best_estimator_

plt.scatter(X.ravel(), y)
lim = plt.axis()
y_test = model.fit(X, y).predict(X_test)
plt.plot(X_test.ravel(), y_test)
plt.axis(lim)

# %%
data = [
    {"price": 950000, "rooms": 4, "neighborhood": "Queen Anne"},
    {"price": 700000, "rooms": 3, "neighborhood": "Fremont"},
    {"price": 650000, "rooms": 3, "neighborhood": "Wallingford"},
    {"price": 600000, "rooms": 2, "neighborhood": "Fremont"},
]

# %%
vec = DictVectorizer(sparse=False, dtype=int)
vec.fit_transform(data)

# %%
vec.get_feature_names()

# %%
vec = DictVectorizer(sparse=True, dtype=int)
vec.fit_transform(data)

# %%
sample = ["problem of evil", "evil queen", "horizon problem"]

# %%
vec = CountVectorizer()
X = vec.fit_transform(sample)
X


# %%
pd.DataFrame(X.toarray(), columns=vec.get_feature_names())

# %%
vec = TfidfVectorizer()
X = vec.fit_transform(sample)
pd.DataFrame(X.toarray(), columns=vec.get_feature_names())

# %%
x = np.array([1, 2, 3, 4, 5])
y = np.array([4, 2, 1, 3, 7])
plt.scatter(x, y)

# %%
X = x[:, np.newaxis]
model = LinearRegression().fit(X, y)
yfit = model.predict(X)
plt.scatter(x, y)
plt.plot(x, yfit)

# %%
poly = PolynomialFeatures(degree=3, include_bias=False)
X2 = poly.fit_transform(X)
print(X2)

# %%
model = LinearRegression().fit(X2, y)
yfit = model.predict(X2)
plt.scatter(x, y)
plt.plot(x, yfit)

# %%
X = np.array([[nan, 0, 3], [3, 7, 9], [3, 5, 2], [4, nan, 6], [8, 8, 1]])
y = np.array([14, 16, -1, 8, -5])

# %%
imp = SimpleImputer(strategy="mean")
X2 = imp.fit_transform(X)
X2

# %%
model = LinearRegression().fit(X2, y)
model.predict(X2)

# %%
model = make_pipeline(
    SimpleImputer(strategy="mean"), PolynomialFeatures(degree=2), LinearRegression()
)


# %%
model.fit(X, y)
print(y)
print(model.predict(X))

# %%
X, y = make_blobs(100, 2, centers=2, random_state=2, cluster_std=1.5)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap="RdBu")

# %%
model = GaussianNB()
model.fit(X, y)

# %%
rng = np.random.RandomState(0)
Xnew = [-6, -14] + [14, 18] * rng.rand(2000, 2)
ynew = model.predict(Xnew)

# %%
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap="RdBu")
lim = plt.axis()
plt.scatter(Xnew[:, 0], Xnew[:, 1], c=ynew, s=20, cmap="RdBu", alpha=0.1)
plt.axis(lim)

# %%
yprob = model.predict_proba(Xnew)
yprob[-8:].round(2)

# %%
data = fetch_20newsgroups()
data.target_names

# %%
categories = [
    "talk.religion.misc",
    "soc.religion.christian",
    "sci.space",
    "comp.graphics",
]
train = fetch_20newsgroups(subset="train", categories=categories)
test = fetch_20newsgroups(subset="test", categories=categories)

# %%
print(train.data[5])

# %%
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# %%
model.fit(train.data, train.target)
labels = model.predict(test.data)

# %%
mat = confusion_matrix(test.target, labels)
sns.heatmap(
    mat.T,
    square=True,
    annot=True,
    fmt="d",
    cbar=False,
    xticklabels=train.target_names,
    yticklabels=train.target_names,
)
plt.xlabel("true label")
plt.ylabel("predicted label")

# %%


def predict_category(s, train=train, model=model):
    pred = model.predict([s])
    return train.target_names[pred[0]]


# %%
predict_category("sending a payload to the ISS")

# %%
predict_category("discussing islam vs atheism")

# %%
predict_category("determining the screen resolution")

# %%
rng = np.random.RandomState(1)
x = 10 * rng.rand(50)
y = 2 * x - 5 + rng.randn(50)
plt.scatter(x, y)


# %%
model = LinearRegression(fit_intercept=True)
model.fit(x[:, np.newaxis], y)

xfit = np.linspace(0, 10, 1000)
yfit = model.predict(xfit[:, np.newaxis])

plt.scatter(x, y)
plt.plot(xfit, yfit)

# %%
print("Model slope:", model.coef_[0])
print("Model intercept:", model.intercept_)

# %%
rng = np.random.RandomState(1)
X = 10 * rng.rand(100, 3)
y = 0.5 + np.dot(X, [1.5, -2.0, 1.0])

model.fit(X, y)
print(model.intercept_)
print(model.coef_)

# %%
x = np.array([2, 3, 4])
poly = PolynomialFeatures(3, include_bias=False)
poly.fit_transform(x[:, None])


# %%
poly_model = make_pipeline(PolynomialFeatures(7), LinearRegression())

# %%
rng = np.random.RandomState(1)
x = 10 * rng.rand(50)
y = np.sin(x) + 0.1 * rng.rand(50)

poly_model.fit(x[:, np.newaxis], y)
yfit = poly_model.predict(xfit[:, np.newaxis])

plt.scatter(x, y)
plt.plot(xfit, yfit)

# %%


class GaussianFeatures(BaseEstimator, TransformerMixin):
    """Uniformly spaced Gaussian features for 1d input"""

    def __init__(self, N, width_factor=2.0):
        self.N = N
        self.width_factor = width_factor

    @staticmethod
    def _gauss_basis(x, y, width, axis=None):
        arg = (x - y) / width
        return np.exp(-0.5 * np.sum(arg ** 2, axis))

    def fit(self, X, y=None):
        # create N centers spread along the data range
        self.centers_ = np.linspace(X.min(), X.max(), self.N)
        self.width_ = self.width_factor * (self.centers_[1] - self.centers_[0])
        return self

    def transform(self, X):
        return self._gauss_basis(
            X[:, :, np.newaxis], self.centers_, self.width_, axis=1
        )


gauss_model = make_pipeline(GaussianFeatures(20), LinearRegression())
gauss_model.fit(x[:, np.newaxis], y)
yfit = gauss_model.predict(xfit[:, np.newaxis])

plt.scatter(x, y)
plt.plot(xfit, yfit)
plt.xlim(0, 10)

# %%
model = make_pipeline(GaussianFeatures(30), LinearRegression())
model.fit(x[:, np.newaxis], y)

plt.scatter(x, y)
plt.plot(xfit, model.predict(xfit[:, np.newaxis]))

plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)

# %%


def basis_plot(model, title=None):
    fig, ax = plt.subplots(2, sharex=True)
    model.fit(x[:, np.newaxis], y)
    ax[0].scatter(x, y)
    ax[0].plot(xfit, model.predict(xfit[:, np.newaxis]))
    ax[0].set(xlabel="x", ylabel="y", ylim=(-1.5, 1.5))

    if title:
        ax[0].set_title(title)

    ax[1].plot(model.steps[0][1].centers_, model.steps[1][1].coef_)
    ax[1].set(xlabel="basis location", ylabel="coefficent", xlim=(0, 10))


model = make_pipeline(GaussianFeatures(30), LinearRegression())
basis_plot(model)

# %%
model = make_pipeline(GaussianFeatures(30), Ridge(alpha=0.1))
basis_plot(model, title="Ridge Regression")

# %%
model = make_pipeline(GaussianFeatures(30), Lasso(alpha=0.001))
basis_plot(model, title="Lasso Regression")

# %%
# Skip time series example due to data not being accessible

# %%
X, y = make_blobs(n_samples=50, centers=2, random_state=0, cluster_std=0.6)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap="autumn")


# %%
