from reservoir_features import reservoir_features
from pyts.datasets import load_basic_motions

bunch = load_basic_motions()
X_train, X_test, y_train, y_test = load_basic_motions(return_X_y=True)

a = reservoir_features(X_train,num_features = 18)
a.normalize()
a.filters(stride_len = [1,2], num_filters = 2)
ans = a.result_features()