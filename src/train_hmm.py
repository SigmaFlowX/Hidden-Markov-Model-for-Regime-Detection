from hmmlearn import hmm

def train_hmm(X, n_states, n_iter, verbose=True):
    model = hmm.GaussianHMM(n_components=n_states, covariance_type="full", n_iter=n_iter, verbose=verbose)
    model.fit(X)
    return model
