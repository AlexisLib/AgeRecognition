#include "include.h"
#include <stdlib.h> 
#include <vector>

using namespace Eigen;
using namespace std;

extern "C" {
	SUPEREXPORT void* createPMCModel(int* structure, int nbLayer);
	SUPEREXPORT void displayPmcModel(t_pmcData* PMC)
	{
		cout << "STRUCT :" << endl;
		for (int k = 0; k < PMC->lenStructure; k++)
		{
			cout << PMC->structure[k] << ", ";
		}
		cout << endl;
		cout << "PMC :" << endl;
		for (int l = 1; l < PMC->lenStructure; l++)
		{
			cout << "layer " << l << endl;
			for (int j = 1; j < PMC->structure[l] + 1; j++)
			{
				cout << "	neurones " << j << endl;
				for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
				{
					cout << "		weights " << PMC->W[l][j][i] << endl;
				}
			}
		}
	}


	SUPEREXPORT void deletePMCModel(t_pmcData* PMC)
	{
		
		delete[] PMC->output;
		delete[] PMC->sigma;

		for (int l = 1; l < PMC->lenStructure; l++)
		{
			for (int j = 1; j < PMC->structure[l] + 1; j++)
			{
				delete PMC->Wold[l][j];
				delete PMC->W[l][j];
			}
			delete PMC->W[l];
			delete PMC->Wold[l];
		}
		delete PMC;
	}

	SUPEREXPORT void savePMCInCSV(char *path, t_pmcData* PMC)
	{
		ofstream fd;

		fd.open(path);

		// save structure
		for (int k = 0; k < PMC->lenStructure; k++)
		{
			fd << PMC->structure[k]  << ";";
		}
		fd << endl;

		// save weights
		for (int l = 1; l < PMC->lenStructure; l++)
		{
			for (int j = 1; j < PMC->structure[l] + 1; j++)
			{
				for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
				{
					fd << PMC->W[l][j][i] << ";";
				}
			}
			fd << endl;
		}
		fd.close();
	}

	SUPEREXPORT void loadPMCWithCSV(char *path, t_pmcData* PMC)
	{
		size_t pos = 0;
		std::string token;
		unsigned int i = 0;

		//// get input count per sample (on filename)
		std::ifstream fd(path);
		

		if (!fd) {
			cout << "Unable to open file";
			exit(1);
		}
		std::string line = "";
		getline(fd, line);
		
		for (int l = 1; l < PMC->lenStructure; l++)
		{
			std::string line = "";
			getline(fd, line);
			for (int j = 1; j < PMC->structure[l] + 1; j++)
			{

				for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
				{
					pos = line.find(";");
					token = line.substr(0, pos);
					PMC->W[l][j][i] = stod(token);
					line.erase(0, pos + 1);
				}
			}
		}

		fd.close();
		//return (PMC);
	}

	SUPEREXPORT void* createPMCModel(int* structure, int nbLayer)
	{
		t_pmcData* PMC;
		try
		{
			srand(time(NULL));
			PMC = new t_pmcData[1];
			PMC->W = new double** [nbLayer];
			PMC->Wold = new double** [nbLayer];
			PMC->structure = new int[nbLayer];

			PMC->structure = structure;
			PMC->lenStructure = nbLayer;
			for (int l = 1; l < nbLayer; l++)
			{
				PMC->W[l] = new double* [(size_t)structure[l] + 1]; // neurones ajout biais
				PMC->Wold[l] = new double* [(size_t)structure[l] + 1];
				for (int j = 1; j < structure[l] + 1; j++)
				{
					PMC->W[l][j] = new double[(size_t)structure[l - 1] + 1]; // poids
					PMC->Wold[l][j] = new double[(size_t)structure[l - 1] + 1];
					for (int i = 0; i < structure[l - 1] + 1; i++)
					{
						PMC->W[l][j][i] =  (rand() / (double)RAND_MAX) * (1.0 - (-1.0)) - 1.0;
						PMC->Wold[l][j][i] = 0;
					}
				}
			}
			allocate(PMC);
			return PMC;
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return NULL;
		}
	}

	SUPEREXPORT void* getPMCStructure(char* path)
	{
		t_pmcData* PMC;
		srand(time(NULL));

		size_t pos = 0;
		std::string token;
		unsigned int i = 0;
		// get input count per sample (on filename)
		std::ifstream fd(path);
		std::vector<int> v;

		if (!fd) {
			cout << "Unable to open file";
			exit(1);
		}
		std::string line = "";
		getline(fd, line);

		while ((pos = line.find(";")) != std::string::npos) {
			token = line.substr(0, pos);
			v.push_back(stoi(token));
			line.erase(0, pos + 1);
		}

		int* pmcStructure = &v[0];
		return pmcStructure;
	}

	SUPEREXPORT double* predictPMCRegression(t_pmcData* PMC, Eigen::VectorXd* X,  int res)
	{
		return (predictPMC(PMC, X, 1, res));
	}

	SUPEREXPORT double* predictPMCClassification(t_pmcData* PMC, Eigen::VectorXd* X, int res)
	{
		return (predictPMC(PMC, X, 0, res));
	}

	SUPEREXPORT double fitPMCRegression(t_pmcData* PMC, Eigen::MatrixXd* X, Eigen::MatrixXd* Y, int SampleCount, double alpha, int epochs, int display)
	{
		int inputCountPerSample = PMC->structure[0] + 1;
		Eigen::MatrixXd tmpMatrixX(1, inputCountPerSample);
		Eigen::MatrixXd tmpMatrixY(1, (*Y).cols());
		Eigen::VectorXd tmpVectorX(inputCountPerSample);
		Eigen::VectorXd expectedOutputVector((*Y).cols());

		try {
			if ((*Y).cols() != PMC->structure[PMC->lenStructure - 1])
				throw std::exception("erreur Y n'est pas de la meme taille que les neurones");


			for (int i = 0; i < epochs; i++)
			{
				if (display != -1 && i % display == 0)
					cout << "current epochs  : " << i << " on " << epochs << endl;

				for (int k = 0; k < SampleCount; k++)
				{
					int nb = rand() % SampleCount;

					tmpMatrixX = (*X).block(nb, 0, 1, inputCountPerSample);
					tmpVectorX = (Map<VectorXd>(tmpMatrixX.data(), tmpMatrixX.cols()));

					predictPMC(PMC, &tmpVectorX, 1, 0);

					tmpMatrixY = (*Y).block(nb, 0, 1, (*Y).cols());
					expectedOutputVector = (Map<VectorXd>(tmpMatrixY.data(), tmpMatrixY.cols()));

					for (int n = 1; n < PMC->structure[PMC->lenStructure - 1] + 1; n++)
					{
						PMC->sigma[PMC->lenStructure - 1][n] = (PMC->output[PMC->lenStructure - 1][n] - expectedOutputVector[n - 1]);
					}
					//update sigmas
					for (int l = PMC->lenStructure - 1; l > 1; l--) // voir 1 
					{
						for (int i = 1; i < PMC->structure[l - 1] + 1; i++)
						{
							double res = 0;
							for (int j = 1; j < PMC->structure[l] + 1; j++)
							{
								res += PMC->W[l][j][i] * PMC->sigma[l][j];
							}
							double newSigma = (1 - pow(PMC->output[l - 1][i], 2)) * res;
							PMC->sigma[l - 1][i] = newSigma;
						}
					}
					// update poids
					for (int l = 1; l < PMC->lenStructure; l++)
					{
						for (int j = 1; j < PMC->structure[l] + 1; j++)
						{
							for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
							{
								double fix = alpha * PMC->output[l - 1][i] * PMC->sigma[l][j] + 0.9 * PMC->Wold[l][j][i];
								PMC->W[l][j][i] -= fix;
								PMC->Wold[l][j][i] = fix;
							}
						}
					}
				}
			}
			return (0);
		}
		catch (const runtime_error & error)
		{
			std::cout << "Error occurred: " << error.what() << std::endl;
			return (NULL);
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return (-1);
		}
	}
	SUPEREXPORT double fitPMCClassification(t_pmcData* PMC, Eigen::MatrixXd* X, Eigen::MatrixXd* Y, int SampleCount, double alpha, int epochs, int display)
	{
		int inputCountPerSample = PMC->structure[0] + 1;
		Eigen::MatrixXd tmpMatrixX(1, inputCountPerSample);
		Eigen::MatrixXd tmpMatrixY(1, (*Y).cols());
		Eigen::VectorXd tmpVectorX(inputCountPerSample);
		Eigen::VectorXd expectedOutputVector((*Y).cols());
		

		try {
			if ((*Y).cols() != PMC->structure[PMC->lenStructure - 1])
				throw std::exception("erreur Y n'est pas de la meme taille que les neurones");

			for (int i = 0; i < epochs; i++)
			{
				if (display != -1 && i % display == 0)
					cout << "current epochs  : " << i << " on " << epochs << endl;
				
				for (int k = 0; k < SampleCount; k++)
				{
					int nb = rand() % SampleCount;
					tmpMatrixX = (*X).block(nb, 0, 1, inputCountPerSample);
					tmpVectorX = (Map<VectorXd>(tmpMatrixX.data(), tmpMatrixX.cols()));
					predictPMC(PMC, &tmpVectorX, 0, 0);

					tmpMatrixY = (*Y).block(nb, 0, 1, (*Y).cols());
					expectedOutputVector = (Map<VectorXd>(tmpMatrixY.data(), tmpMatrixY.cols()));

					for (int n = 1; n < PMC->structure[PMC->lenStructure - 1] + 1; n++)
					{
						PMC->sigma[PMC->lenStructure - 1][n] = (double)((1 - pow(PMC->output[PMC->lenStructure - 1][n], 2)) * (PMC->output[PMC->lenStructure - 1][n] - expectedOutputVector[n - 1]));
					}
					//update sigmas
					for (int l = PMC->lenStructure - 1; l > 1; l--) // voir 1 
					{
						for (int i = 1; i < PMC->structure[l - 1] + 1; i++)
						{
							double res = 0;
							for (int j = 1; j < PMC->structure[l] + 1; j++)
							{
								res += PMC->W[l][j][i] * PMC->sigma[l][j];
							}
							double newSigma = (1 - pow(PMC->output[l - 1][i], 2)) * res;
							PMC->sigma[l - 1][i] = newSigma;
						}
					}
					// update poids
					for (int l = 1; l < PMC->lenStructure; l++)
					{
						for (int j = 1; j < PMC->structure[l] + 1; j++)
						{
							for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
							{
								PMC->W[l][j][i] -= alpha * PMC->output[l - 1][i] * PMC->sigma[l][j];
							}
						}
					}
				}
			}
			return (0);
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return (-1);
		}
	}

	SUPEREXPORT void deleteResult(double *res)
	{
		delete[] res;
	}
}

double* predictPMC(t_pmcData* PMC, Eigen::VectorXd* X, int isLinear, int res)
{
	try {

		addInputsInPMC(PMC, X);
		for (int l = 1; l < PMC->lenStructure; l++)
		{
			for (int j = 1; j < PMC->structure[l] + 1; j++)
			{
				double tmpTotal = 0;
				for (int i = 0; i < PMC->structure[l - 1] + 1; i++)
				{
					tmpTotal += PMC->W[l][j][i] * PMC->output[l - 1][i];
				}
				if (l == PMC->lenStructure - 1 && isLinear == 1)
					PMC->output[l][j] = tmpTotal;
				else
					PMC->output[l][j] = tanh(tmpTotal);

			}
		}
		if (res == 1)
		{
			double* ret = new double[PMC->structure[PMC->lenStructure - 1]];
			for (int i = 1; i < PMC->structure[PMC->lenStructure - 1] + 1; i++)
			{
				ret[i - 1] = (double)PMC->output[PMC->lenStructure - 1][i];
			}
			return ret;
		}
		return (NULL);
	}
	catch (const runtime_error & error)
	{
		std::cout << "Error occurred: " << error.what() << std::endl;
		return (NULL);
	}
	catch (const std::exception & ex)
	{
		std::cout << "Error occurred: " << ex.what() << std::endl;
		return (NULL);
	}
}

void addInputsInPMC(t_pmcData* PMC, Eigen::VectorXd* input)
{
	for (int i = 0; i < input->size(); i++)
	{
		PMC->output[0][i] = (*input)(i);
	}
}

void displayOutput(t_pmcData* PMC)
{
	cout << "OUTPUTS :" << endl;
	for (int l = 0; l < PMC->lenStructure; l++)
	{
		cout << "layer " << l << endl;
		for (int j = 0; j < PMC->structure[l] + 1; j++)
		{
			cout << std::setprecision(9) << PMC->output[l][j] << endl;
		}
	}
}

void displaySigmas(t_pmcData* PMC)
{
	cout << "SIGMAS :" << endl;
	for (int l = 1; l < PMC->lenStructure; l++)
	{
		cout << "layer " << l << endl;
		for (int j = 1; j < PMC->structure[l] + 1; j++)
		{
			cout << "	" << std::setprecision(9) << PMC->sigma[l][j] << endl;
		}
	}
}


//  [2, 3 , 1]
void allocate(t_pmcData* PMC)
{
	PMC->output = new double *[PMC->lenStructure];
	PMC->sigma = new double *[PMC->lenStructure];
	for (int l = 0; l < PMC->lenStructure; l++)
	{	
		PMC->output[l] = new double[PMC->structure[l] + 1];
		PMC->output[l][0] = 1;
		// sigma ne commence que à l >= 1
		if (l >= 1)
			PMC->sigma[l] = new double[PMC->structure[l] + 1];
	}
}
