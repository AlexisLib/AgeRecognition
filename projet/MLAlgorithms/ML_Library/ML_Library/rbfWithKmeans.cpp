#include "include.h"

using namespace Eigen;
using namespace std;

extern "C" {
	SUPEREXPORT MatrixXd* kMeans(MatrixXd X, int k, int it);
	SUPEREXPORT void deleteRBFModel(t_rbfData* RBF)
	{
		//if (RBF->W != NULL)
		//	delete RBF->W;
		//if (RBF->X != NULL)
		//	delete RBF->X;
		delete RBF;
	}
	SUPEREXPORT void* createRBFModel(int inputCountPerSample)
	{
		srand(time(NULL));

		//inputCountPerSample = inputCountPerSample  + 1;
		t_rbfData* RBF = new t_rbfData[1];

		RBF->inputCountPerSample = inputCountPerSample;
		RBF->W = NULL;
		RBF->X = NULL;
		RBF->centroids = NULL;
		return (RBF);

	}


	SUPEREXPORT void fitRBFRegression(t_rbfData * RBF, MatrixXd * X, MatrixXd * Y, double gamma, int k, int it)
	{
		RBF->centroids = kMeans(*X, k, it);
		RBF->W = new Eigen::MatrixXd(k, 1);
		RBF->X = new Eigen::MatrixXd(X->rows(), X->cols());
		RBF->gamma = gamma;
		Eigen::MatrixXd tmp(1, X->cols());

		RBF->X = X;
		Eigen::MatrixXd phi(X->rows(), k);

		for (int i = 0; i < X->rows(); i++)
		{
			for (int j = 0; j < k; j++)
			{

				//cout << "AA" << endl;
				tmp = (*X).block(i, 0, 1, X->cols()) - ((*RBF->centroids)).block(j, 0, 1, (*RBF->centroids).cols());
				//cout << "BB" << endl;
				phi(i, j) = exp(-RBF->gamma * pow(tmp.norm(), 2));
				//cout << "DD" << endl;
			}
		}
		//cout << "EE" << endl;
		Eigen::MatrixXd phiInv = (phi).completeOrthogonalDecomposition().pseudoInverse();
		(*RBF->W) = phiInv * (*Y);
	}

	SUPEREXPORT void fitRBFClassification(t_rbfData * RBF, MatrixXd * X, MatrixXd * Y, double gamma, int k, int it)
	{
		fitRBFRegression(RBF, X, Y, gamma, k, it);
	}
	SUPEREXPORT double predictRBFRegression(t_rbfData * RBF, VectorXd * XPredict)
	{
		//cout << "Test" << endl;
		MatrixXd gauss(1, RBF->centroids->rows());
		for (int i = 0; i < RBF->centroids->rows(); i++)
		{
			//cout << "Test2" << endl;
			Eigen::MatrixXd tmp(1, XPredict->cols());

			//cout << "Test3" << endl;
			//cout << (*XPredict).transpose().rows() << " " << (*XPredict).transpose().cols() << endl;
			//cout << (*RBF->centroids).block(i, 0, 1, RBF->centroids->cols()).rows() << " " << (*RBF->centroids).block(i, 0, 1, RBF->centroids->cols()).cols() << endl;
			tmp = (*XPredict).transpose() - (*RBF->centroids).block(i, 0, 1, RBF->centroids->cols());
			//cout << "Test4" << endl;
			gauss(0, i) = exp(-RBF->gamma * pow(tmp.norm(), 2));
//			cout << "Test5" << endl;
		}
	//	cout << "Test6" << endl;
	//	cout << (*RBF->W) << endl;
	//	cout << "Test7" << endl;
	//	cout << (*RBF->W).sum() << endl;
		return (gauss * (*RBF->W)).sum();
	}

	SUPEREXPORT double predictRBFClassification(t_rbfData * RBF, VectorXd * XPredict)
	{
		return predictRBFRegression(RBF, XPredict) >= 0 ? 1.0 : -1.0;
	}
}