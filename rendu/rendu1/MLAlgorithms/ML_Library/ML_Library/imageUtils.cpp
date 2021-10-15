#include "include.h"
#include <Eigen/Dense>

void getPixelsFromImage(string imagePath, int component, Eigen::MatrixXd *datasetX, unsigned int imageIdx)
{
	Mat image;
	image = imread(imagePath, component);
	int i = 1;
	int fullSize = image.rows * image.cols * component;
	int* pixelArray = new int[fullSize];

	for (int x = 0; x < image.rows; x++)
	{
		for (int y = 0; y < image.cols; y++)
		{
			unsigned char* p = image.ptr(x, y); // order B G R 
			for (int c = 0; c < component; c++)
			{
				int tmp = p[c];
				(*datasetX)(imageIdx, i) = tmp;
				i++;
			}
		}
	}
}


void displayPixelArray(int *pixelArray, int imageSize, int component)
{
	for (int k = 0; k < imageSize; k = k + component)
	{
		if (component == 1)
			std::cout << "COLOR : " << pixelArray[k] << endl;
		else
		{
			std::cout << "BLUE: " << pixelArray[k];
			std::cout << ", GREEN : " << pixelArray[k + 1];
			std::cout << ", RED " << pixelArray[k + 2] << endl;
		}
	}
}

void savePixelsInCSV(string path, int *pixelArray, int *imageSize, int component)
{
	ofstream fd;
	cout << "aa";

	size_t start = path.find_last_of("/") + 1;
	size_t end = path.find_last_of(".");
	string csvPath = path.substr(start, end - start) + ".csv";
	//cout << csvPath << endl;
	fd.open("/home/hadarak/LotteCSV/" + csvPath);

	int size = imageSize[0] * imageSize[1] * component;

	for (int i = 0; i < size - 1; i++)
	{
		fd << pixelArray[i];
		fd << ";";
	}
	fd.close();
}
//
