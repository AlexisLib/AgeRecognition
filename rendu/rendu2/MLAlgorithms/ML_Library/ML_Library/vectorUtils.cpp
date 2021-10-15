#include "include.h"

extern "C" {
	SUPEREXPORT void *datasetToVector(double *dataset, unsigned int size, unsigned int bias)
	{
		if (bias == 1)
		{
			size = size + 1;
			//cout << size << endl;
			Eigen::VectorXd* retVector = new Eigen::VectorXd(size);
			(*retVector)(0) = 1;
			for (int x = 1; x < size; x++)
			{
				(*retVector)(x) = dataset[x - 1];
			}
			return retVector;
		}
		else
		{
			Eigen::VectorXd* retVector = new Eigen::VectorXd(size);
			for (int x = 0; x < size; x++)
			{
				(*retVector)(x) = dataset[x];
			}
			return retVector;
		}
	}
}