	

#include "include.h"
#include <Eigen/Dense>

extern "C" {
	SUPEREXPORT void *getDatasetY(char* str, unsigned int numberImage)
	{
		size_t pos = 0;
		std::string token;
		std::string s = str;

		unsigned int imageIdx = 0;
		Eigen::MatrixXd* retMatrix = new Eigen::MatrixXd(numberImage, 1);
		while ((pos = s.find(",")) != std::string::npos) {
			token = s.substr(0, pos);

			size_t start = token.find_last_of("/") + 1;
			string filename = token.erase(0, start);

			size_t delim = filename.find("_");
			string age = filename.substr(0, delim);

			(*retMatrix)(imageIdx) = std::stoi(age);
			s.erase(0, pos + 1);
			imageIdx++;
		}
		if (s.length() != 0)
		{
			size_t start = s.find_last_of("/") + 1;
			string filename = s.erase(0, start);

			size_t delim = filename.find("_");
			string age = filename.substr(0, delim);

			(*retMatrix)(imageIdx) = std::stoi(age);
		}
		return retMatrix;
	}

	SUPEREXPORT void *getDatasetX(char *str, unsigned int sizeImage, unsigned int numberImage, unsigned int component)
	{
		size_t pos = 0;
		std::string token;
		std::string s = str;
		unsigned int imageIdx = 0;
		unsigned int inputCountPerSample = (sizeImage * component) + 1;
		Eigen::MatrixXd *retMatrix = new Eigen::MatrixXd(numberImage, inputCountPerSample);
		while ((pos = s.find(",")) != std::string::npos) {
			token = s.substr(0, pos);
			
			(*retMatrix)(imageIdx, 0) = 1;
			getPixelsFromImage(token, component, retMatrix, imageIdx);

			s.erase(0, pos + 1);
			imageIdx++;
		}
		if (s.length() != 0)
		{
			(*retMatrix)(imageIdx, 0) = 1;
			getPixelsFromImage(s, component, retMatrix, imageIdx);
		}
		return retMatrix;
	}
}

Eigen::MatrixXd convertArrayToMatrix(int SampleCount, int inputCountPerSample, double *Array)
{
	Eigen::MatrixXd retMatrix(SampleCount, inputCountPerSample);
	int i = 0;
	for (int x = 0; x < SampleCount; x++)
	{
		for (int y = 0; y < inputCountPerSample; y++)
		{
			retMatrix(x, y) = Array[i];
			i++;
		}
	}
	return (retMatrix);
}

void convertMatrixToSimpleArray(Eigen::MatrixXd W, double *arr) {
	int col = W.cols();
	int row = W.rows();
	int j = 0;
	
	for (int x = 0; x < row; x++)
	{
		for (int y = 0; y < col; y++)
		{
			arr[j] = W(x, y);
			j++;

		}
	}
}
//bool matrixMultiplicationPossible(Eigen::MatrixXd matrixA, Eigen::MatrixXd matrixB)
//{
//	if (matrixA.rows() == matrixB.cols())
//		return (true);
//	return (false);
//}