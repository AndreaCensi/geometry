
from . import (SO3, SO2, R1, R2, R3, SE2, SE3, S2, S1, T1, T2, T3, so2, so3, se2,
    se3, np)
from .. import (S1_project_from_S2, S2_from_S1, S1_project_from_R2,
    S2_project_from_R3, se2_from_so2, so2_project_from_se2, se3_from_so3,
    so3_project_from_se3, SE3_from_SO3, SE2_from_SO2, SO2_project_from_SE2,
    SO3_project_from_SE3, R2_project_from_SE2, SE2_from_R2, SE3_from_R3,
    R3_project_from_SE3, SO2_project_from_SO3, SO3_from_SO2, so2_project_from_so3,
    so3_from_so2)

    
def embed(small, big, embed_in, project_from):
    small.embed_relation(big, embed_in, project_from)

embed(R1, R2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embed(R2, R3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

embed(SO2, SO3, SO3_from_SO2, SO2_project_from_SO3)
embed(so2, so3, so3_from_so2, so2_project_from_so3)

embed(SO2, SE2, SE2_from_SO2, SO2_project_from_SE2)
embed(SO3, SE3, SE3_from_SO3, SO3_project_from_SE3)

embed(so3, se3, se3_from_so3, so3_project_from_se3)
embed(so2, se2, se2_from_so2, so2_project_from_se2)

embed(S1, S2, S2_from_S1, S1_project_from_S2)

embed(S1, R2, lambda x: x, S1_project_from_R2)
embed(S2, R3, lambda x: x, S2_project_from_R3)

embed(R2, SE2, SE2_from_R2, R2_project_from_SE2)
embed(R3, SE3, SE3_from_R3, R3_project_from_SE3)
    

embed(T1, T2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embed(T2, T3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

# TODO: more tori?
embed(T1, R1, lambda x: x, lambda x: T1.normalize(x)) 
embed(T2, R2, lambda x: x, lambda x: T2.normalize(x))
embed(T3, R3, lambda x: x, lambda x: T3.normalize(x))
    

