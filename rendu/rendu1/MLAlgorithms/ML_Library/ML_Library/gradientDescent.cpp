#include "include.h"

extern "C" {

	SUPEREXPORT double fit_regression_gd(
		double* arrayWeight,
		double* XTrain,
		double* YTrain,
		int sampleCount,
		int inputCountPerSample 
	)
	{
		int nb_epoch = 100;
		double lr = 1.1;

		Eigen::MatrixXd X = convertArrayToMatrix(sampleCount, inputCountPerSample, XTrain);
		Eigen::MatrixXd Y = convertArrayToMatrix(sampleCount, 1, YTrain);
		Eigen::MatrixXd W = convertArrayToMatrix(inputCountPerSample, 1, arrayWeight);
		Eigen::MatrixXd mat(0, 0);
		Eigen::MatrixXd result = Eigen::MatrixXd::Constant(inputCountPerSample, 1, 0);

		//W << 0.1, 0.1, 0.1;


		for (int epo = 0; epo < nb_epoch; epo++) {
			result = Eigen::MatrixXd::Constant(inputCountPerSample, 1, 0);
			for (int j = 0; j < inputCountPerSample; j++) {
				for (int i = 0; i < sampleCount; i++) {
					mat = X.block(i, 0, 1, inputCountPerSample) * W;
					result(j, 0) += -X(i, j) * (Y(i, 0) - mat(0, 0));
				}
			}


			for (int i = 0; i < inputCountPerSample; i++) {
				result(i, 0) = result(i, 0) * (float(1) / sampleCount);
				W(i, 0) = W(i, 0) - lr * result(i, 0);
			}
		}


		std::cout << "W : " << std::endl;
		std::cout << W << std::endl;
		std::cout << "--" << std::endl;

		convertMatrixToSimpleArray(W, arrayWeight);


		return 0.42;
	}

}