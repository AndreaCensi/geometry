
from . import (DifferentiableManifold, SO3, SO2, R1, R2, R3, SE2, SE3, S2, S1, T1,
    T2, T3, so2, so3, se2, se3, np, Tran2, tran2, tran3, Tran3, tran1)
from .. import (S1_project_from_S2, S2_from_S1, S1_project_from_R2,
    S2_project_from_R3, se2_from_so2, so2_project_from_se2, se3_from_so3,
    so3_project_from_se3, SE3_from_SO3, SE2_from_SO2, SO2_project_from_SE2,
    SO3_project_from_SE3, R2_project_from_SE2, SE2_from_R2, SE3_from_R3,
    R3_project_from_SE3, SO2_project_from_SO3, SO3_from_SO2, so2_project_from_so3,
    so3_from_so2, SE2_project_from_SE3, se2_project_from_se3, se3_from_se2,
    SE3_from_SE2, SO2_from_angle, angle_from_SO2)
from geometry.spheres import normalize_pi

    
def embedding(small, big, embed_in, project_from, desc=None):
    DifferentiableManifold.embedding(small, big, embed_in, project_from, type='user',
                                     desc=desc)

def isomorphism(A, B, a_to_b, b_to_a, desc=None):
    DifferentiableManifold.isomorphism(A, B, a_to_b, b_to_a, type='user', desc=desc)

embedding(R1, R2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embedding(R2, R3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

embedding(SO2, SO3, SO3_from_SO2, SO2_project_from_SO3)
embedding(so2, so3, so3_from_so2, so2_project_from_so3)

embedding(SO2, SE2, SE2_from_SO2, SO2_project_from_SE2)
embedding(SO3, SE3, SE3_from_SO3, SO3_project_from_SE3)

embedding(so3, se3, se3_from_so3, so3_project_from_se3)
embedding(so2, se2, se2_from_so2, so2_project_from_se2)

embedding(se2, se3, se3_from_se2, se2_project_from_se3)
embedding(SE2, SE3, SE3_from_SE2, SE2_project_from_SE3)

embedding(S1, S2, S2_from_S1, S1_project_from_S2)

embedding(S1, R2, lambda x: x, S1_project_from_R2)
embedding(S2, R3, lambda x: x, S2_project_from_R3)

embedding(R2, SE2, SE2_from_R2, R2_project_from_SE2)
embedding(R3, SE3, SE3_from_R3, R3_project_from_SE3)
    
isomorphism(T1, S1, lambda a: np.array([np.cos(float(a)), np.sin(float(a))]),
                lambda b: normalize_pi(np.array([np.arctan2(b[1], b[0])])))
isomorphism(T1, SO2, lambda x: SO2_from_angle(x[0]),
                    lambda y: np.array([angle_from_SO2(y)]))


embedding(T1, T2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embedding(T2, T3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

# TODO: more tori?
embedding(T1, R1, lambda x: x, lambda x: T1.normalize(x)) 
embedding(T2, R2, lambda x: x, lambda x: T2.normalize(x))
embedding(T3, R3, lambda x: x, lambda x: T3.normalize(x))
    
#
#isomorphism(Tran1, R1, lambda x: x[0:1, -1],
#                lambda b: np.array([[1, b[0]], [0, 1]]))
#
#isomorphism(Tran2, R2, lambda x: x[0:2, -1],
#                lambda b: np.array([[1, 0, b[0]],
#                                    [0, 1, b[1]],
#                                    [0, 0, 1.0]]))
#
#isomorphism(Tran3, R3, lambda x: x[0:3, -1],
#                lambda b: np.array([[1, 0, 0, b[0]],
#                                    [0, 1, 0, b[1]],
#                                    [0, 0, 1, b[2]],
#                                    [0, 0, 0, 1]]))

embedding(tran1, tran2, lambda b: np.array([[0, 0, b[0, -1]],
                                         [0, 0, 0],
                                         [0, 0, 0]]),
                    lambda b: np.array([[0, b[0, -1]],
                                        [0, 0]]))
                
                     
embedding(tran2, tran3, lambda b: np.array([[0, 0, 0, b[0, -1]],
                                         [0, 0, 0, b[1, -1]],
                                         [0, 0, 0, 0],
                                         [0, 0, 0, 0]]),
                    lambda b: np.array([[0, 0, b[0, -1]],
                                         [0, 0, b[1, -1]],
                                         [0, 0, 0]]))


embedding(tran2, se2, lambda x: x,
                 lambda b: np.array([[0, 0, b[0, 2]],
                                     [0, 0, b[1, 2]],
                                     [0, 0, 0]]))
                
embedding(tran3, se3, lambda x: x,
                    lambda b: np.array([[0, 0, 0, b[0, -1]],
                                        [0, 0, 0, b[1, -1]],
                                        [0, 0, 0, b[2, -1]],
                                        [0, 0, 0, 0]]))


embedding(Tran2, SE2, lambda x: x,
                 lambda b: np.array([[1, 0, b[0, 2]],
                                     [0, 1, b[1, 2]],
                                     [0, 0, 1]]))
                
embedding(Tran3, SE3, lambda x: x,
                    lambda b: np.array([[1, 0, 0, b[0, -1]],
                                        [0, 1, 0, b[1, -1]],
                                        [0, 0, 1, b[2, -1]],
                                        [0, 0, 0, 1]]))


