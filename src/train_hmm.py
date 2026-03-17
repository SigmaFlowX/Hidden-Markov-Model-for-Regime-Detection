from hmmlearn import hmm

def train_hmm(X, n_states, n_iter):
    model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=n_iter)
    model.fit(X)
    return model
