#include "include.h"
using namespace Eigen;

extern "C" {
	SUPEREXPORT void deleteVector(Eigen::VectorXd *vector)
	{
		vector->resize(0);
		delete vector;
	}

	SUPEREXPORT void *datasetToVector(double *dataset, unsigned int size, unsigned int bias)
	{
		if (bias == 1)
		{
			size = size + 1;
			Eigen::VectorXd* retVector = new Eigen::VectorXd(size);
			(*retVector)(0) = 1;
			for (unsigned int x = 1; x < size; x++)
			{
				(*retVector)(x) = dataset[x - 1];
			}
			return retVector;
		}
		else
		{
			Eigen::VectorXd* retVector = new Eigen::VectorXd(size);
			for (unsigned int x = 0; x < size; x++)
			{
				(*retVector)(x) = dataset[x];
			}
			return retVector;
		}
	}

	SUPEREXPORT void* matrixToVector(Eigen::MatrixXd* X, unsigned int inputCountPerSample, unsigned int bias)
	{
		if (bias == 1)
			inputCountPerSample++;
		Eigen::MatrixXd tmpMatrixX(1, inputCountPerSample);
		Eigen::VectorXd* retVector = new Eigen::VectorXd(inputCountPerSample);

		tmpMatrixX = (*X).block(0, 0, 1, inputCountPerSample);
		*retVector = (Map<VectorXd>(X->data(), X->cols()));

		return retVector;
	}
}