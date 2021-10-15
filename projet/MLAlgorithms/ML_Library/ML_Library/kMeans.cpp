#include "include.h"

using namespace Eigen;
using namespace std;

extern "C" {

	SUPEREXPORT MatrixXd* kMeans(MatrixXd X, int k, int it)
	{
		srand(time(NULL));
		bool changeCentroids = true;
		if (k > X.rows())
			return NULL;

		MatrixXd* centroids = new MatrixXd(k, X.cols());
		int* references = new int[X.rows()];
		Eigen::MatrixXd tmp(1, X.cols());
		double* tmpNorms = new double[k];
		int* usedCentroid = new int[k];
		int sizeUsed = 0;
		int tmpRand = 0;

		//init centroids with X samples
		for (int i = 0; i < k; i++)
		{
			do {
				tmpRand = (int)(rand() % X.rows());

			} while (checkUsed(usedCentroid, tmpRand, sizeUsed) != 0);

			usedCentroid[sizeUsed] = tmpRand;
			sizeUsed++;
			(*centroids).row(i) = (X).block(tmpRand, 0, 1, X.cols());
		}
		int p = 0;

		while ((it == -1 && changeCentroids == true) || (it != -1 && p < it)) // arret
		{
			changeCentroids = false;
			// assign K centroid for each sample
			for (int i = 0; i < X.rows(); i++)
			{
				for (int j = 0; j < k; j++)
				{
					tmp = (X).block(i, 0, 1, X.cols()) - (*centroids).block(j, 0, 1, centroids->cols());
					tmpNorms[j] = tmp.norm();
				}
				references[i] = getMinInArray(tmpNorms, k);
			}


			// reassign centroids
			MatrixXd tmpAdd(1, X.cols());
			for (int i = 0; i < k; i++)
			{
				int c = 0;
				for (int n = 0; n < X.cols(); n++)
					tmpAdd(0, n) = 0;

				for (int j = 0; j < X.rows(); j++)
				{
					if (references[j] == i)
					{
						for (int m = 0; m < X.cols(); m++)
						{
							tmpAdd(0, m) += X(j, m);
						}
						c++;
					}
				}
				for (int b = 0; b < X.cols(); b++)
				{
					tmpAdd(0, b) = tmpAdd(0, b) / c;
				}
				if ((*centroids).row(i) != tmpAdd.row(0))
					changeCentroids == true;
				(*centroids).row(i) = tmpAdd.row(0);
			}
			p++;
		}
		return (centroids);
	}
}

int checkUsed(int *tab, int tmp, int sizeUsed)
{
	if (sizeUsed == 0)
		return (0);
	for (int i = 0; i < sizeUsed; i++)
	{
		if (tab[i] == tmp)
			return (-1);
	}
	return (0);
}
int getMinInArray(double *Arr, int size)
{
	int min = 0;
	for (int i = 1; i < size; i++)
	{
		if (Arr[i] < Arr[min])
			min = i;
	}
	return (min);
}