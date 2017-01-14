import numpy

MAX_ITERATIONS = 100
INFINITY = 1000


class Point:
    def __init__(self, coordinates, label=None):
        # self.x = x
        # self.y = y
        self.coordinates = coordinates
        self.label = label

    def __str__(self):
        return '{coordinates} labeled {label}'.format(
            coordinates=self.coordinates,
            label=self.label
        )

    def __repr__(self):
        return str(self)


# Function: K Means
# -------------
# K-Means is an algorithm that takes in a dataset and a constant
# k and returns k centroids (which define clusters of data in the
# dataset which are similar to one another).
def kmeans(data_set, k):
    # Initialize centroids randomly
    numFeatures = data_set.getNumFeatures()
    centroids = getRandomCentroids(numFeatures, k)

    # Initialize book keeping vars.
    iterations = 0
    old_centroids = None

    # Run the main k-means algorithm
    while not should_stop(old_centroids, centroids, iterations):
        # Save old centroids for convergence test. Book keeping.
        old_centroids = centroids
        iterations += 1

        # Assign labels to each datapoint based on centroids
        labels = get_labels(data_set, centroids)

        # Assign centroids based on datapoint labels
        centroids = get_centroids(data_set, labels, k)

    # We can get the labels too by calling get_labels(data_set, centroids)
    return centroids


# Function: Should Stop
# -------------
# Returns True or False if k-means is done. K-means terminates either
# because it has run a maximum number of iterations OR the centroids
# stop changing.
def should_stop(old_centroids, centroids, iterations):
    if iterations > MAX_ITERATIONS:
        return True
    return old_centroids == centroids


# Function: Get Labels
# -------------
# Returns a label for each piece of data in the dataset.
def get_labels(data_set, centroids):
    # For each element in the dataset, choose the closest centroid.
    # Make that centroid the element's label.
    labels = {}
    for point in data_set:
        distances = [
            (centroid, get_distance(point, centroid))
            for centroid in centroids
        ]
        min_dist = sorted(distances, key=lambda pair: pair[1])[0]
        # print(sorted(distances, key=lambda pair: pair[1]))
        # print(min_dist)
        point.label = min_dist[0]
        labels[point] = min_dist[0]
        # print(point)
        # print('**********************************************************')
    return labels


# Function: Get Centroids
# -------------
# Returns k random centroids, each of dimension n.
def get_centroids(data_set, labels, k):
    # Each centroid is the geometric mean of the points that
    # have that centroid's label. Important: If a centroid is empty (no points have
    # that centroid's label) you should randomly re-initialize it.
    pass


def get_distance(point, other):
    """Calculate Euclidean Distance."""
    return numpy.sqrt(sum((point.coordinates - other.coordinates) ** 2))


def load_points(filename):
    with open(filename, 'r') as data:
        return [Point(numpy.array(list(
            map(float, line.replace('\n', '').split('\t')))))
            for line in data.readlines()]


def main():
    points = load_points('normal/normal.txt')
    print(get_distance(points[0], points[1]))
    centroids = [Point(numpy.array([4.5, 4.5])), Point(numpy.array([4.3, 4.3])), Point(numpy.array([4.7, 4.7]))]
    print(get_labels(points, centroids))
    print('---------------------------------------------------------------------------')
    print(points)


if __name__ == '__main__':
    main()
