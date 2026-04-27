# Musiplexity: Classifying Music by Genre Using Data Analysis and Machine Learning

This is project I conducted as part of an internship with the Patriot Machine Learning Research Group at Francis Marion University. This research analyzes how well machines can sort musical selections into predetermined genres using persistent homology and k-means clustering.

Persistent homology is a method within topological data analysis that studies features within graphical planes. Speficially, this targets persistent features at different spatial scales to separate important aspects from noise. For thsi project, I utilized the Viteoris-Rips complex, which is a method that analyzes these features as "holes." Given a set of points, we can form a simplex (a simple n-dimensional shape) by defining a distance from each of these points and creating a relationship with all other points that fall within this diameter.

Below is a simple example of the Viteoris-Rips complex. Here we have two sets of points that form squares with different spatial dimensions. When our distance or radius is zero, there are no relationships between the points. However, as we increase the radius, we begin to see the simplex form. With a distance of two radii, line segments or edges are formed within the set of points that form the smaller dimensional square, whereas the set of points that form the larger dimensional square still have no perceived relationship. With a radii of three, the smaller dimensional square is fully formed and what was now once a "hole" is fully realized as a simplex.

![Example of Vietoris-Rips Complex](./images/vietoris_rips_complex.png "Example of Vietoris-Rips Complex")
