#include "include.h"
//#include <windows.h>
//#include <iostream>
//#include "osqp.h"

using namespace Eigen;
using namespace std;

extern "C" {
	SUPEREXPORT double predictLinearRegression(Eigen::MatrixXd* W, Eigen::MatrixXd* X);
	SUPEREXPORT double predictLinearClassification(Eigen::MatrixXd* W, Eigen::MatrixXd* X);

	//SUPEREXPORT void testOSQP(Eigen::SparseMatrix<double> spMatrix)
	//{
	//	// Load problem data
	//	//c_float P_x[25] = { 2.0, 3.0, -4.0, -5.0, -8.0, 3.0, 5.0, -6.0, -9.0, -12.0, -4.0, -6.0, 8.0, 10.0, 16.0, -5.0, -9.0, 10.0, 17.0, 20.0, -8.0, -12.0, 16.0, 20.0, 32.0, };
	//	//c_int   P_nnz = 25;
	//	//c_int   P_i[4] = { 0, 1, 0, 1, };
	//	//c_int   P_p[3] = { 0, 2, 4, };
	//	c_float q[5] = { -1.0, -1.0, -1.0, -1.0, -1.0};
	//	c_float A_x[4] = { -1.0  };
	//	c_int   A_nnz = 4;
	//	c_int   A_i[4] = { 0, 1, 0, 2, };
	//	c_int   A_p[3] = { 0, 2, 4, };
	//	c_float l[1] = { 0.0 };
	//	//c_float u[3] = { 1.0, 0.7, 0.7, };


	//	// Problem settings
	//	OSQPSettings* settings = (OSQPSettings*)c_malloc(sizeof(OSQPSettings));

	//	// Structures
	//	OSQPWorkspace* work; // Workspace
	//	OSQPData* data;      // OSQPData
	//	// Populate data
	//	data = (OSQPData*)c_malloc(sizeof(OSQPData));
	//	data->n = 1; //nb variables
	//	data->m = 2; // nb constraints
	//	data->P = csc_matrix(data->n, data->n, spMatrix.nonZeros(), spMatrix.valuePtr(), (c_int *)spMatrix.outerIndexPtr(), (c_int*)spMatrix.innerIndexPtr());
	//	data->q = q;
	//	data->A = csc_matrix(data->m, data->n, A_nnz, A_x, A_i, A_p);
	//	data->l = l;
	//	data->u = NULL;

	//	// Define Solver settings as default
	//	osqp_set_default_settings(settings);
	//	settings->alpha = 1.0;

	//	// Setup workspace
	//	work = osqp_setup(data, settings);

	//	// Solve Problem
	//	osqp_solve(work);

	//	// Clean workspace
	//	osqp_cleanup(work);
	//	c_free(data->A);
	//	c_free(data->P);
	//	c_free(data);
	//	c_free(settings);
	//}

	//SUPEREXPORT void fitSvm(Eigen::MatrixXd *X, Eigen::MatrixXd *Y)
	//{

	//	OSQPWorkspace* work;
	//	Eigen::MatrixXd *bigMatrix = new Eigen::MatrixXd(X->rows(), X->rows());

	//	for (int i = 0; i < X->rows(); i++)
	//	{
	//		cout << "i " << i << endl;
	//		for (int j = 0; j < X->rows(); j++)
	//		{
	//			double tmp = ((*X).row(i) * (*X).row(j).transpose()).sum();
	//			(*bigMatrix)(i, j) =  tmp * (*Y)(i, 0) * (*Y)(j, 0);
	//		}
	//	}
	//	
	//	SparseMatrix<double> spMatrix = bigMatrix->sparseView();

	//	testOSQP(spMatrix);
	//	/*cout << (*bigMatrix) << endl;*/
	//}
	SUPEREXPORT void deleteSVMModel(Eigen::VectorXd* W)
	{
		delete W;
	}

	SUPEREXPORT void *fitSvm(Eigen::MatrixXd* X, Eigen::MatrixXd* Y, Eigen::VectorXd *alphas)
	{
		Eigen::VectorXd tmpW = Eigen::VectorXd::Zero(X->cols());
		for (int i = 0; i < alphas->size(); i++)
		{
			if ((*alphas)(i) - 0.000001 < 0.00000001)
			{
				(*alphas)(i) = 0;
			}
		}
		for (int i = 0; i < X->rows(); i++)
		{
			tmpW += (*alphas)(i) * (*Y)(i, 0) * (*X).row(i);
		}

		Eigen::VectorXd *W = new Eigen::VectorXd(X->cols() + 1);
		int idxAlpha = -1;
		for (int i = 0; i < alphas->size(); i++)
		{
			if ((*alphas)(i) - 0.000001 > 0.00000001)
			{
				idxAlpha = i;	
				break;
			}
		}
		if (idxAlpha == -1)
		{
			cout << "no support vector found" << endl;
			return NULL;
		}

		Eigen::MatrixXd tmpMatrixX(1, (*X).cols());
		Eigen::VectorXd tmpVectorX((*X).cols());

		tmpMatrixX = (*X).block(idxAlpha, 0, 1, X->cols());
		tmpVectorX = (Map<VectorXd>(tmpMatrixX.data(), tmpMatrixX.cols()));
	
		(*W)(0) = (1 / (*Y)(idxAlpha, 0)) - (tmpW.adjoint() * tmpVectorX);
		for (int i = 0; i < tmpW.size(); i++)
		{
			(*W)(i + 1) = tmpW(i);
		}
		return (W);
	}

	SUPEREXPORT double fitSvmKernelTrick(Eigen::MatrixXd* X, Eigen::MatrixXd* Y, Eigen::VectorXd* alphas)
	{
		
		for (int i = 0; i < alphas->size(); i++)
		{
			if ((*alphas)(i) - 0.000001 < 0.00000001)
			{
				(*alphas)(i) = 0;
			}
		}

		int idxAlpha = -1;
		for (int i = 0; i < alphas->size(); i++)
		{
			if ((*alphas)(i) - 0.000001 > 0.00000001)
			{
				idxAlpha = i;
				break;
			}
		}
		if (idxAlpha == -1)
		{
			cout << "no support vector found" << endl;
			return NULL;
		}
		
		Eigen::MatrixXd tmpMatrixX(1, (*X).cols());
		Eigen::VectorXd tmpVectorX((*X).cols());

		tmpMatrixX = (*X).block(idxAlpha, 0, 1, X->cols());
		tmpVectorX = (Map<VectorXd>(tmpMatrixX.data(), tmpMatrixX.cols()));


		double tmp;
		for (int i = 0; i < X->rows(); i++)
		{
			tmp += (*alphas)(i) * (*Y)(i, 0) * kernelTrick((*X).row(i), tmpVectorX);
		}
		return ((1 / (*Y)(idxAlpha, 0)) - tmp);


	}

	SUPEREXPORT double predictSvmKernelTrickClassification(Eigen::MatrixXd* X, Eigen::MatrixXd* Y, Eigen::VectorXd* XPredict, Eigen::VectorXd* alphas, double W0)
	{
		for (int i = 0; i < alphas->size(); i++)
		{
			if ((*alphas)(i) - 0.000001 < 0.00000001)
			{
				(*alphas)(i) = 0;
			}
		}
		double res = 0;

		for (int i = 0; i < X->rows(); i++)
		{
			res += (*alphas)(i) * (*Y)(i, 0) * kernelTrick((*X).row(i), *XPredict);
		}

		return (res + W0);// >= 0 ? 1.0 : -1.0;

	}

	SUPEREXPORT double predictSvmClassification(Eigen::VectorXd* WVector, Eigen::MatrixXd* X)
	{
		Eigen::MatrixXd* W = new Eigen::MatrixXd(WVector->size(), 1);

		for (int i = 0; i < WVector->size(); i++)
			(*W)(i, 0) = (*WVector)(i);
		return predictLinearClassification(W, X);
	}

	SUPEREXPORT double predictSvmRegression(Eigen::VectorXd* WVector, Eigen::MatrixXd* X)
	{

		Eigen::MatrixXd* W = new Eigen::MatrixXd(WVector->size(), 1);
		for (int i = 0; i < WVector->size(); i++)
			(*W)(i, 0) = (*WVector)(i);
		return predictLinearRegression(W, X);
	}
}

double kernelTrick(Eigen::VectorXd m, Eigen::VectorXd n)
{
	double MM = (m).transpose() * (m);
	double NN = (n).transpose() * (n);
	return (exp(-MM) * exp(-NN) * exp(2 * (n).transpose() * (m)));
	
}