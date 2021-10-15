#include "include.h"

using namespace Eigen;
using namespace std;

extern "C" {

	SUPEREXPORT void deleteNaiveRBFModel(t_rbfData* RBF)
	{
		delete RBF;

	}

	SUPEREXPORT void* createNaiveRBFModel(int inputCountPerSample)
	{
		srand(time(NULL));

		inputCountPerSample = inputCountPerSample + 1;
		t_rbfData* RBF = new t_rbfData[1];

		RBF->inputCountPerSample = inputCountPerSample;
		RBF->W = NULL;
		RBF->X = NULL;
		return (RBF);
	}

	SUPEREXPORT void fitNaiveRBFRegression(t_rbfData * RBF, MatrixXd * X, MatrixXd * Y, double gamma)
	{
		RBF->W = new Eigen::MatrixXd(RBF->inputCountPerSample, 1);
		RBF->X = new Eigen::MatrixXd(X->rows(), X->cols());
		RBF->gamma = gamma;
		Eigen::MatrixXd tmp(1, X->cols());

		RBF->X = X;
		Eigen::MatrixXd phi(X->rows(), X->rows());

		for (int i = 0; i < X->rows(); i++)
		{
			for (int j = 0; j < X->rows(); j++)
			{

				tmp = (*X).block(i, 0, 1, X->cols()) - (*X).block(j, 0, 1, X->cols());
				phi(i, j) = exp(-RBF->gamma * pow(tmp.norm(), 2));
			}
		}

		Eigen::MatrixXd phiInv = (phi).completeOrthogonalDecomposition().pseudoInverse();
		(*RBF->W) = phiInv * (*Y);
	}

	SUPEREXPORT void fitNaiveRBFClassification(t_rbfData* RBF, MatrixXd* X, MatrixXd* Y, double gamma)
	{
		fitNaiveRBFRegression(RBF, X, Y, gamma);
	}
	SUPEREXPORT double predictNaiveRBFRegression(t_rbfData * RBF, VectorXd * XPredict)
	{
		MatrixXd gauss(1, RBF->X->rows());
		for (int i = 0; i < RBF->X->rows(); i++)
		{
			Eigen::MatrixXd tmp(1, RBF->X->cols());
			
			//tmp = (*RBF->X).block(i, 0, 1, RBF->X->cols()) - (*XPredict).transpose();
			tmp = (*XPredict).transpose() - (*RBF->X).block(i, 0, 1, RBF->X->cols());
			gauss(0, i) = exp(-RBF->gamma * pow(tmp.norm(), 2));
		}
		return (gauss * (*RBF->W)).sum();
	}

	SUPEREXPORT double predictNaiveRBFClassification(t_rbfData* RBF, VectorXd* XPredict)
	{
		return predictNaiveRBFRegression(RBF, XPredict) >= 0 ? 1.0 : -1.0;
	}

	SUPEREXPORT void saveRBFWeightsInCSV(char* path, t_rbfData * RBF)
	{
		ofstream fd;

		fd.open(path);

		fd << RBF->X->rows() << ";" << RBF->X->cols() << endl;

		// write X
		for (int x = 0; x < RBF->X->rows(); x++)
		{
			for (int y = 0; y < RBF->X->cols() ; y++)
			{
				fd << (*RBF->X)(x, y);
				fd << ";";
			}
		}
		fd << endl;
		// write W
		for (int x = 0; x < RBF->W->rows(); x++)
		{
			
			fd << (*RBF->W)(x, 0);
			fd << ";";
		}
		fd.close();
	}
	
	SUPEREXPORT void *loadRBFWeightsWithCSV(char* path, unsigned int inputCountPerSample)
	{
		t_rbfData* RBF = new t_rbfData[1];
		std::string token;
		unsigned int x;
		unsigned int y;
		size_t pos = 0;
		double value;
		int XCol;
		int XRow;

		std::ifstream fd(path);

		if (!fd) {
			cout << "Unable to open file";
			exit(1);
		}

		RBF->inputCountPerSample = inputCountPerSample;
		
		//get X size
		std::string line = "";
		getline(fd, line);

		pos = line.find(";"); //cou;rty
		XRow = stod(line.substr(0, pos));
		line.erase(0, pos + 1);
		XCol = stod(line.substr(0));

		// get X values
		RBF->X = new Eigen::MatrixXd(XRow, XCol);

		line = "";
		x = 0;
		y = 0;
		getline(fd, line);
		while ((pos = line.find(";")) != std::string::npos) {
			token = line.substr(0, pos);
			value = stod(token);
			(*RBF->X)(x, y) = value;
			line.erase(0, pos + 1);
			y++;

			if (y >= XCol) {
				y = 0;
				x++;
			}
		}

		// get W values
		RBF->W = new Eigen::MatrixXd(inputCountPerSample, 1);

		x = 0;
		line = "";
		getline(fd, line);
		while ((pos = line.find(";")) != std::string::npos) {
			token = line.substr(0, pos);
			value = stod(token);
			(*RBF->W)(x, 0) = value;
			line.erase(0, pos + 1);
			x++;
		}

		
		return (RBF);
		
	}
}