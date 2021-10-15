#include "include.h"

using namespace Eigen;
using namespace std;


extern "C" {

	// Initialisation random weight [-1,1]
	SUPEREXPORT void *createLinearModel(int inputCountPerSample)
	{
		srand(time(NULL));

		inputCountPerSample = inputCountPerSample + 1;
		Eigen::MatrixXd *W = new Eigen::MatrixXd(inputCountPerSample, 1);

		for (int i = 0; i < inputCountPerSample; i++) {
			(*W)(i, 0) = (rand() / (double)RAND_MAX) * (1.0 - (-1.0)) - 1.0;
		}
		return W;
	}

	SUPEREXPORT double fitLinearRegression(
		Eigen::MatrixXd *W,
		Eigen::MatrixXd *X,
		Eigen::MatrixXd *Y,
		int SampleCount,
		int inputCountPerSample
	)
	{
		try {
			fixColinearity(X);
			inputCountPerSample = inputCountPerSample + 1;
			Eigen::MatrixXd Xtranspose(inputCountPerSample, SampleCount);

			Xtranspose = (*X).transpose();

			Eigen::MatrixXd pinv = (*X).completeOrthogonalDecomposition().pseudoInverse();
			(*W) = pinv * (*Y);
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return (0);
		}
		return 0.42;
	}

	SUPEREXPORT double predictLinearRegression(
		Eigen::MatrixXd *W,
		Eigen::MatrixXd *X
	)
	{
		try {
			double ret = 0.0;
			Eigen::MatrixXd R(1, 1);

			R =  (*X) * (*W);
			return (double)R(0, 0);
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return (-1);
		}
		catch (const runtime_error & error)
		{
			std::cout << "Error occurred: " << error.what() << std::endl;
			return (-2);
		}
	}

	SUPEREXPORT void deleteLinearModel(Eigen::MatrixXd* arrayWeight)
	{
		arrayWeight->resize(0, 0);
		delete arrayWeight;
	}

	SUPEREXPORT void deleteDatasetMatrix(Eigen::MatrixXd* pMatrixX, Eigen::MatrixXd* pMatrixY)
	{
		pMatrixX->resize(0, 0);
		delete pMatrixX;
		pMatrixY->resize(0, 0);
		delete pMatrixY;
	}
}