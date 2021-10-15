#include "include.h"
#include <stdlib.h> 

using namespace Eigen;

extern "C" {

	SUPEREXPORT void deletePMC(t_pmc* W)
	{
		for (int l = 0; l < W->nbLayer; l++)
		{
			for (int n = 0; n < W->layers[l].nbNeurone; n++)
			{
				if (l >= 1)
				{
					delete W->layers[l].neurones[n].weights;
				}

			}
			free((t_neurone*)(W->layers[l].neurones));
		}
		if (W->layers != NULL)
			free((t_layer*)(W->layers));
		if (W != NULL)
			free(W);
	}
	SUPEREXPORT double* predictPMCRegression(
		t_pmc * W,
		Eigen::VectorXd * X
	)
	{
		return (predictPMC(W, X, 1));
	}

	SUPEREXPORT double* predictPMCClassification(
		t_pmc * W,
		Eigen::VectorXd * X
	)
	{
		return (predictPMC(W, X, 0));
	}

	SUPEREXPORT double fitPMCRegression(
		t_pmc * W,
		Eigen::MatrixXd * X,
		Eigen::MatrixXd * Y,
		int SampleCount,
		int inputCountPerSample,
		double alpha, // Learning Rate
		int epochs, // Nombre d'iteration
		int display // interval affichage
	)
	{
		return (fitPMC(W, X, Y, SampleCount, inputCountPerSample, alpha, epochs, display, 1));
	}

	SUPEREXPORT double fitPMCClassification(
		t_pmc * W,
		Eigen::MatrixXd * X,
		Eigen::MatrixXd * Y,
		int SampleCount,
		int inputCountPerSample,
		double alpha, // Learning Rate
		int epochs, // Nombre d'iteration
		int display // interval affichage
	)
	{
		return (fitPMC(W, X, Y, SampleCount, inputCountPerSample, alpha, epochs, display, 0));
	}

	SUPEREXPORT void* createPMCModel(int* structure, int nbLayer, int inputCountPerSample)
	{

		srand(time(NULL));
		try
		{
			nbLayer += 1;
			inputCountPerSample += 1;
			t_pmc* pmc = NULL;
			if ((pmc = (t_pmc*)malloc(sizeof(t_pmc) * 1)) == NULL)
				throw std::bad_alloc();
			pmc->nbLayer = nbLayer;
			if ((pmc->layers = (t_layer*)malloc(sizeof(t_layer) * nbLayer)) == NULL)
				throw std::bad_alloc();


			//initialisation de la couche 0 (inputs)
			if ((pmc->layers[0].neurones = (t_neurone*)malloc(sizeof(t_neurone) * inputCountPerSample)) == NULL)
				return (NULL);
			pmc->layers[0].nbNeurone = inputCountPerSample;

			for (int idxLayer = 1; idxLayer < nbLayer; idxLayer++)
			{
				if ((pmc->layers[idxLayer].neurones = (t_neurone*)malloc(sizeof(t_neurone) * structure[idxLayer - 1])) == NULL)
					return (NULL);
				pmc->layers[idxLayer].nbNeurone = structure[idxLayer - 1];
				for (int idxNeurone = 0; idxNeurone < structure[idxLayer - 1]; idxNeurone++)
				{
					int nbWeights;
					if (idxLayer == 1)
						nbWeights = inputCountPerSample;
					else
						nbWeights = structure[idxLayer - 2] + 1;
					pmc->layers[idxLayer].neurones[idxNeurone].weights = new Eigen::VectorXd(nbWeights);
					for (int idxWeights = 0; idxWeights < nbWeights; idxWeights++)
					{
						(*pmc->layers[idxLayer].neurones[idxNeurone].weights)(idxWeights) = (rand() / (double)RAND_MAX) * (1.0 - (-1.0)) - 1.0;
						//(*pmc->layers[idxLayer].neurones[idxNeurone].weights)(idxWeights) = 0.5;
					}
				}
			}
			return (pmc);
		}
		catch (const std::exception & ex)
		{
			std::cout << "Error occurred: " << ex.what() << std::endl;
			return NULL;
		}
	}
}

void fillFirstLayerWithInputs(t_pmc * W, Eigen::VectorXd * input)
{
	for (int i = 0; i < input->size(); i++)
	{
		W->layers[0].neurones[i].result = (*input)(i);
	}
}

void calculateNeuroneOutput(t_neurone * neurone, Eigen::VectorXd * input, unsigned int isLinear)
{
	Eigen::VectorXd tmp(input->size());

	tmp = (*input).transpose() * (*neurone->weights);
	if (isLinear == 1)
		(*neurone).result = tmp.sum();
	else
		(*neurone).result = tanh(tmp.sum());
}

Eigen::VectorXd* getLayerOuptut(t_layer * layer, int bias)
{
	if (bias == 1)
	{
		Eigen::VectorXd* layerResult = new Eigen::VectorXd((layer->nbNeurone + 1));
		(*layerResult)(0) = 1;
		for (int idxNeurone = 1; idxNeurone < layer->nbNeurone + 1; idxNeurone++)
		{
			(*layerResult)(idxNeurone) = (*layer).neurones[idxNeurone - 1].result;
		}
		return (layerResult);
	}
	else
	{
		Eigen::VectorXd* layerResult = new Eigen::VectorXd((layer->nbNeurone));
		for (int idxNeurone = 0; idxNeurone < layer->nbNeurone; idxNeurone++)
		{
			(*layerResult)(idxNeurone) = (*layer).neurones[idxNeurone].result;
		}
		return (layerResult);
	}
}

double* predictPMC(t_pmc * W, Eigen::VectorXd * X, unsigned int isLinear)
{
	Eigen::VectorXd* tmpLayerResult;
	try {
		fillFirstLayerWithInputs(W, X);
		for (unsigned int idxLayer = 1; idxLayer < W->nbLayer; idxLayer++)
		{
			if (idxLayer - 1 == 0)
				tmpLayerResult = getLayerOuptut(&(*W).layers[idxLayer - 1], 0);
			else
				tmpLayerResult = getLayerOuptut(&(*W).layers[idxLayer - 1], 1);
			for (unsigned int idxNeurone = 0; idxNeurone < (*W).layers[idxLayer].nbNeurone; idxNeurone++)
			{
				if (idxLayer == (*W).nbLayer - 1)
					calculateNeuroneOutput(&(*W).layers[idxLayer].neurones[idxNeurone], tmpLayerResult, isLinear);
				else
					calculateNeuroneOutput(&(*W).layers[idxLayer].neurones[idxNeurone], tmpLayerResult, 0);
			}
		}
		double* ret = new double(W->layers[(*W).nbLayer - 1].nbNeurone);

		for (int i = 0; i < W->layers[(*W).nbLayer - 1].nbNeurone; i++)
		{
			
			ret[i] = (*W).layers[(*W).nbLayer - 1].neurones[i].result;
			//if (isLinear == 0)
			//	ret[i] = ret[i] >= 0 ? 1.0 : -1.0;
		}
		return (ret);
	}
	catch (const std::exception & ex)
	{
		std::cout << "Error occurred: " << ex.what() << std::endl;
		return (NULL);
	}
	catch (const runtime_error & error)
	{
		std::cout << "Error occurred: " << error.what() << std::endl;
		return (NULL);
	}
}

double fitPMC(
	t_pmc * W,
	Eigen::MatrixXd * X,
	Eigen::MatrixXd * Y,
	int SampleCount,
	int inputCountPerSample,
	double alpha, // Learning Rate
	int epochs, // Nombre d'it�ration
	int display, // interval affichage
	int isLinear
)
{
	cout << "START" << endl;
	inputCountPerSample = inputCountPerSample + 1;
	double* predictOutput;
	double* expectedOutput;
	Eigen::MatrixXd tmpMatrixX(1, inputCountPerSample);
	Eigen::VectorXd tmpVectorX(inputCountPerSample);
	Eigen::VectorXd expectedOutputVector((*Y).cols());

	try {
		//displayPmc(W);
		cout << (*Y).cols() << (*W).layers[(*W).nbLayer - 1].nbNeurone << endl;
		if ((*Y).cols() != (*W).layers[(*W).nbLayer - 1].nbNeurone)
			throw std::exception("erreur Y n'est pas de la meme taille que les neurones");
		for (int i = 0; i < epochs; i++)
		{
			if (i % display == 0)
				cout << "current epochs  : " << i << " on " << epochs << endl;
			for (int k = 0; k < SampleCount; k++)
			{
				tmpMatrixX = (*X).block(k, 0, 1, inputCountPerSample);
				tmpVectorX = (Map<VectorXd>(tmpMatrixX.data(), tmpMatrixX.cols()));

				predictOutput = predictPMC(W, &tmpVectorX, isLinear);
				//cout << "sampl" << k << endl;
				expectedOutputVector = (*Y).block(k, 0, 1, (*Y).cols());
				//cout << "vecto" << expectedOutputVector << endl;
				if (isLinear == 0)
				{
					for (int idxOutput = 0; idxOutput < expectedOutputVector.size(); idxOutput++)
					{
						(*W).layers[(*W).nbLayer - 1].neurones[idxOutput].sigma = (1 - pow(predictOutput[idxOutput], 2)) * (predictOutput[idxOutput] - expectedOutputVector(idxOutput));
						//cout << "res sigma" << (1 - pow(predictOutput[idxOutput], 2)) * (predictOutput[idxOutput] - expectedOutputVector(idxOutput)) << endl;
						//cout << "predict Out " << predictOutput[idxOutput] << endl;
						//cout << "expetct Out " << expectedOutputVector(idxOutput) << endl;
					}
				}
				else
				{
					for (int idxOutput = 0; idxOutput < expectedOutputVector.size(); idxOutput++)
						(*W).layers[(*W).nbLayer - 1].neurones[idxOutput].sigma = predictOutput[idxOutput] - expectedOutputVector(idxOutput);
				}
				for (int l = (*W).nbLayer - 1; l > 1; l--)
				{

					int i = 0;
					while (i < (*W).layers[l - 1].nbNeurone)
					{
						double total = 0;
						for (unsigned int j = 0; j < (*W).layers[l].nbNeurone; j++)
						{
							total += (*W->layers[l].neurones[j].weights)((int)i + 1) * (*W).layers[l].neurones[j].sigma;
						}
						double sigmaBefore = (1 - pow((*W).layers[l - 1].neurones[i].result, 2)) * total;
						//cout << "total " << total << endl;
						//cout << "res" << (*W).layers[l - 1].neurones[i].result << endl;

						(*W).layers[l - 1].neurones[i].sigma = sigmaBefore;
						i++;
					}
				}

				for (unsigned int l = 1; l < (*W).nbLayer; l++)
				{
					for (int idxNeurone = 0; idxNeurone < (*W).layers[l].nbNeurone; idxNeurone++)
					{

						for (unsigned int idxWeights = 0; idxWeights < (*W).layers[l].neurones[idxNeurone].weights->size(); idxWeights++)
						{
							(*W->layers[l].neurones[idxNeurone].weights)(idxWeights) -= alpha * (*W).layers[l - 1].neurones[idxWeights].result * (*W).layers[l].neurones[idxNeurone].sigma;
						}
					}
				}
			}
			
		}
	}
	catch (const std::exception & ex)
	{
		std::cout << "Error occurred: " << ex.what() << std::endl;
		return (0);
	}
}

void displayPmc(t_pmc * W)
{
	for (int l = 0; l < W->nbLayer; l++)
	{

		cout << "Layer : " << l << " contains : " << W->layers[l].nbNeurone << " neurones" << endl;
		for (int n = 0; n < W->layers[l].nbNeurone; n++)
		{
			cout << "	neurone : " << n << " result : " << std::setprecision(9) << W->layers[l].neurones[n].result << endl;
			if (l >= 1)
			{
				cout << "	neurone : " << n << " sigma : " << std::setprecision(9) << W->layers[l].neurones[n].sigma << endl;
				for (int w = 0; w < W->layers[l].neurones[n].weights->size(); w++)
				{
					cout << "		  weight : " << w << " value : " << std::setprecision(9) << (*W->layers[l].neurones[n].weights)(w) << endl;
				}
			}
		}
	}
}
