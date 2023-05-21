import numpy as np

def normal_from_points(points):
    n = len(points)
    if n > 3:
        centroid = np.mean([[p.x, p.y, p.z] for p in points], axis=0)
        C = np.zeros((3, 3))
        for p in points:
            C += np.outer([p.x - centroid[0], p.y - centroid[1], p.z - centroid[2]],
                          [p.x - centroid[0], p.y - centroid[1], p.z - centroid[2]])
        eigenvalues, eigenvectors = np.linalg.eig(C / n)
        idx = np.argmin(eigenvalues)
        return list(eigenvectors[:, idx])
    else:
        return None