#include "include.h"
#include <Eigen/Dense>

void getPixelsFromImage(string imagePath, int component, Eigen::MatrixXd *datasetX, unsigned int imageIdx, unsigned int sizeImageW, unsigned int sizeImageH)
{
	Mat image;
	image = imread(imagePath, component);
	int i = 1;
	int fullSize = image.rows * image.cols * component;
	int *pixelArray = new int[fullSize];

	if (sizeImageH != image.rows || sizeImageW != image.cols)
	{
		cout << "invalid image size" << imagePath << endl;
		return;
	}
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
