# coding=utf-8
from .differentiable_manifold import DifferentiableManifold
from .manifold_relations import ManifoldRelations as MR

SYMBOL_ISOMORPHISM = '~'  # XXX: not used
SYMBOL_EMBEDDING = '<'
SYMBOL_PROJECTION = '>'
__all__ = ['compute_manifold_relations']


def compute_manifold_relations(manifolds):
    isomorphisms, embeddings = find_embedding_relations(manifolds)
    create_isomorphisms(isomorphisms)
    create_embeddings(embeddings)

    if False:  # XXX: old code below
        for m1 in manifolds:
            for m2 in MR.all_isomorphisms(m1):
                print('%5s ~ %5s  via %s' % (m1, m2,
                                             MR.get_isomorphism(m1, m2).steps))

            for m2 in MR.all_embeddings(m1):
                print('%5s < %5s  via %s' % (m1, m2,
                                             MR.get_embedding(m1, m2).steps))


def find_embedding_relations(manifolds):
    visited = set()

    class AutoVivification(dict):

        def __getitem__(self, item):
            try:
                return dict.__getitem__(self, item)
            except KeyError:
                value = self[item] = type(self)()
                return value

    isomorphisms = AutoVivification()
    embeddings = AutoVivification()

    def visit(m1):
        if m1 in visited:
            return
        visited.add(m1)
        # first level
        for m2 in MR.all_isomorphisms(m1):
            isomorphisms[m1][m2] = [(m1, SYMBOL_ISOMORPHISM, m2)]
        # second level
        for m2 in MR.all_isomorphisms(m1):
            visit(m2)
            for m3 in isomorphisms[m2]:
                if not m3 in isomorphisms[m1] and m3 != m1:
                    isomorphisms[m1][m3] = (isomorphisms[m1][m2] +
                                            isomorphisms[m2][m3])
        # first level
        for m2 in MR.all_embeddings(m1):
            embeddings[m1][m2] = [(m1, SYMBOL_EMBEDDING, m2)]
        # second level (direct)
        for m2 in list(embeddings[m1].keys()):
            visit(m2)
            for m3 in embeddings[m2]:
                if not m3 in embeddings[m1]:
                    embeddings[m1][m3] = (embeddings[m1][m2] +
                                          embeddings[m2][m3])
        # second level (with iso)
        for m2 in list(isomorphisms[m1].keys()):
            visit(m2)
            for m3 in embeddings[m2]:
                if not m3 in embeddings[m1]:
                    embeddings[m1][m3] = (isomorphisms[m1][m2] +
                                          embeddings[m2][m3])
#            # finally, each isomorphism is an embedding
#            if not m2 in embeddings[m1]:
#                embeddings[m1][m2] = [ (m1, SYMBOL_ISOMORPHISM, m2) ]

    for m1 in manifolds:
        visit(m1)

    return isomorphisms, embeddings


def create_isomorphisms(isomorphisms):
    for m1 in isomorphisms:
        for m2 in isomorphisms[m1]:
            steps = isomorphisms[m1][m2]

            m1_to_m2 = steps2function(steps)
            m2_to_m1 = steps2function(reverse_steps(steps))
            desc = str(steps)

            # also create embedding
            if len(steps) == 1:
                DifferentiableManifold.embedding(
                   m1, m2, m1_to_m2, m2_to_m1, itype='isomorphism',
                   steps=steps, desc=desc)
                continue
            DifferentiableManifold.isomorphism(
               m1, m2, m1_to_m2, m2_to_m1, itype='derived',
               steps=steps, desc=desc)


def create_embeddings(embeddings):
    for m1 in embeddings:
        for m2 in embeddings[m1]:
            steps = embeddings[m1][m2]
            if len(steps) == 1:
                continue

            m1_to_m2 = steps2function(steps)
            m2_to_m1 = steps2function(reverse_steps(steps))
            desc = str(steps)
            DifferentiableManifold.embedding(
               m1, m2, m1_to_m2, m2_to_m1, itype='derived',
               steps=steps, desc=desc)


def reverse_steps(steps):

    def reverse_step(step):
        A, op, B = step
        rev_op = {SYMBOL_EMBEDDING: SYMBOL_PROJECTION,
                  SYMBOL_PROJECTION: SYMBOL_EMBEDDING,
                  SYMBOL_ISOMORPHISM: SYMBOL_ISOMORPHISM}[op]
        return B, rev_op, A

    return [reverse_step(step) for step in reversed(steps)]


def steps2function(steps):
    functions = []
    for m1, operation, m2 in steps:
        if operation == SYMBOL_EMBEDDING:
            functions.append(MR.get_embedding(m1, m2).A_to_B)
        elif operation == SYMBOL_PROJECTION:
            functions.append(MR.get_projection(m1, m2).A_to_B)
        elif operation == SYMBOL_ISOMORPHISM:
            functions.append(MR.get_isomorphism(m1, m2).A_to_B)

    if len(functions) == 1:
        return functions[0]

    def conversion(x):
        try:
            for f in functions:
                x = f(x)
            return x
        except:
            print('error during %s' % steps)
            print(' functions %s' % functions)
            raise

    return conversion
