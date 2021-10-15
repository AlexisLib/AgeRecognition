#include "include.h"

extern "C" {
	SUPEREXPORT double predictLinearRegression(Eigen::MatrixXd* W, Eigen::MatrixXd* X);
	SUPEREXPORT double predictLinearClassification(
		Eigen::MatrixXd *W,
		Eigen::MatrixXd *X
	)
	{
		return predictLinearRegression(W, X) >= 0 ? 1.0 : -1.0;
	}

	SUPEREXPORT double fitLinearClassification(
		Eigen::MatrixXd *W,
		Eigen::MatrixXd *X,
		Eigen::MatrixXd *Y,
		int SampleCount,
		int inputCountPerSample,
		double alpha, // Learning Rate
		int epochs, // Nombre d'itération
		int display // interval affichage
	)
	{
		inputCountPerSample = inputCountPerSample + 1;
		double predictOutput;
		double expectedOutput;
		Eigen::MatrixXd tmpX(1, inputCountPerSample);

		try {
			for (int i = 0; i < epochs; i++)
			{
				if (i % display == 0)
					cout << "current epochs  : " << i << " on " << epochs << endl;
				for (int k = 0; k < SampleCount; k++)
				{	
					tmpX = (*X).block(k, 0, 1, inputCountPerSample);
					predictOutput = predictLinearClassification(W, &tmpX);
					expectedOutput = (*Y)(k, 0);
					(*W) = (*W) + (alpha * (expectedOutput - predictOutput)) * tmpX.transpose();
				}
			}
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return (0);
		}
	}
}