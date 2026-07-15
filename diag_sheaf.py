"""
diag_sheaf.py — isolate the cause of the S-TTSA smoke failure.
Runs four experiments. Reads the machinery from sheaf_features.py.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.decomposition import PCA
from sheaf_features import (
    MASTER_SEED, N_NODES, STALK_DIM, BOTTOM_K, SHEAF_TARGET_DIM, subseed,
    build_graph_topology, init_rotors, identity_rotors, haar_orthogonal, qf,
    assemble_laplacian, stiefel_ttsa_step,
)

EDGES = build_graph_topology(np.random.default_rng(subseed("topology")))
def rng():  # fresh, identically-seeded generator per synthetic
    return np.random.default_rng(MASTER_SEED)

# ---- learning variants (fixed pass count, so we can sweep convergence) ----
def learn_energy(train, seed, n_passes):
    rot = init_rotors(np.random.default_rng(seed)); lr = 1e-2
    for _ in range(n_passes):
        rot = stiefel_ttsa_step(rot, EDGES, train, lr); lr *= 0.995
    return rot

def learn_hebbian(train, seed, n_passes):          # the twin's rule: outer(x_u,x_v) - Q
    rot = init_rotors(np.random.default_rng(seed)); lr = 1e-2
    for p in range(n_passes):
        new = rot.copy()
        for k, (u, v) in enumerate(EDGES):
            corr = (train[:, u, :].T @ train[:, v, :]) / train.shape[0]
            new[k] = rot[k] - lr * (corr - rot[k])
        rot = new
        if (p + 1) % 20 == 0:
            rot = np.stack([qf(q) for q in rot])   # periodic re-orth (as the twin does)
    return np.stack([qf(q) for q in rot])

# ---- readout: bottom-K (harmonic) or top-K (residual) ----
def feats(stalks, rot, harmonic=True):
    _, ev = np.linalg.eigh(assemble_laplacian(EDGES, rot))
    V = ev[:, :BOTTOM_K] if harmonic else ev[:, -BOTTOM_K:]
    return stalks.reshape(len(stalks), -1) @ V

# ---- two synthetics ----
def make_relational(n, r):     # class = DIFFERENT edge relations (energy's worst case)
    Ra = haar_orthogonal(STALK_DIM, np.random.default_rng(1))
    Rb = haar_orthogonal(STALK_DIM, np.random.default_rng(2))
    def gen(Rc, m):
        out = np.zeros((m, N_NODES, STALK_DIM))
        for i in range(m):
            x = r.standard_normal((N_NODES, STALK_DIM))
            for u, v in EDGES: x[v] = Rc @ x[u] + 0.35 * r.standard_normal(STALK_DIM)
            out[i] = x
        return out
    return np.concatenate([gen(Ra, n), gen(Rb, n)]), np.r_[np.zeros(n), np.ones(n)].astype(int)

def make_valued(n, r):         # class = STALK-VALUE offset, SHARED relations (MI-like)
    R0 = haar_orthogonal(STALK_DIM, np.random.default_rng(0))
    off = np.zeros((N_NODES, STALK_DIM)); off[:, 0] = 1.0
    def gen(sign, m):
        out = np.zeros((m, N_NODES, STALK_DIM))
        for i in range(m):
            x = r.standard_normal((N_NODES, STALK_DIM))
            for u, v in EDGES: x[v] = R0 @ x[u] + 0.35 * r.standard_normal(STALK_DIM)
            out[i] = x + sign * 0.5 * off
        return out
    return np.concatenate([gen(1, n), gen(-1, n)]), np.r_[np.zeros(n), np.ones(n)].astype(int)

def cv(X, y, make_rot, harmonic=True):
    skf = StratifiedKFold(5, shuffle=True, random_state=MASTER_SEED); acc = []
    for tr, te in skf.split(X, y):
        rot = make_rot(X[tr])
        Ftr = feats(X[tr], rot, harmonic); Fte = feats(X[te], rot, harmonic)
        p = PCA(SHEAF_TARGET_DIM, random_state=42).fit(Ftr)
        clf = LogisticRegression(max_iter=1000).fit(p.transform(Ftr), y[tr])
        acc.append(clf.score(p.transform(Fte), y[te]))
    return float(np.mean(acc))

RAND  = lambda tr: init_rotors(np.random.default_rng(subseed("rand")))
IDENT = lambda tr: identity_rotors()
N = 60

print("E1  convergence sweep  (energy, class-in-relations, bottom-K)")
X, y = make_relational(N, rng())
print(f"    S-rand={cv(X,y,RAND):.3f}   R_GL={cv(X,y,IDENT):.3f}")
for npass in (20, 50, 100, 200, 500):
    a = cv(X, y, lambda tr, n=npass: learn_energy(tr, subseed("ttsa"), n))
    print(f"    S-TTSA @ {npass:>4} passes = {a:.3f}")

print("\nE2  synthetic model  (energy full=500, bottom-K)")
for name, mk in (("relations", make_relational), ("values", make_valued)):
    X, y = mk(N, rng())
    print(f"    [{name:9}] S-TTSA={cv(X,y,lambda tr: learn_energy(tr,subseed('t'),500)):.3f}"
          f"  S-rand={cv(X,y,RAND):.3f}  R_GL={cv(X,y,IDENT):.3f}")

print("\nE3  readout  (energy full, class-in-relations)")
X, y = make_relational(N, rng()); mk = lambda tr: learn_energy(tr, subseed("t"), 500)
print(f"    bottom-K(harmonic)={cv(X,y,mk,True):.3f}   top-K(residual)={cv(X,y,mk,False):.3f}")

print("\nE4  rule: energy vs Hebbian  (full=500, bottom-K)")
for name, mk in (("relations", make_relational), ("values", make_valued)):
    X, y = mk(N, rng())
    ae = cv(X, y, lambda tr: learn_energy(tr, subseed("e"), 500))
    ah = cv(X, y, lambda tr: learn_hebbian(tr, subseed("h"), 500))
    print(f"    [{name:9}] energy={ae:.3f}   hebbian={ah:.3f}")
