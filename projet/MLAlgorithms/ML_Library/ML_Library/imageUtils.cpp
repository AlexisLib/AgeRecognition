#include "include.h"
#include <Eigen/Dense>

using namespace std;
using namespace cv;

void getPixelsFromImage(string imagePath, int component, Eigen::MatrixXd *datasetX, unsigned int imageIdx, unsigned int sizeImageW, unsigned int sizeImageH, int is255)
{
	Mat image;
	image = imread(imagePath, component);
	int i = 1;
	int fullSize = image.rows * image.cols * component;
	int *pixelArray = new int[fullSize];

	if (sizeImageH != image.rows || sizeImageW != image.cols)
	{
		cout << "invalid image size " << imagePath << " " << image.rows << endl;
		return;
	}
	for (int x = 0; x < image.rows; x++)
	{
		for (int y = 0; y < image.cols; y++)
		{
			unsigned char* p = image.ptr(x, y); // order B G R 
			for (int c = 0; c < component; c++)
			{
				double tmp = p[c];
				if (is255 == 0)
					(*datasetX)(imageIdx, i) = tmp;
				else
					(*datasetX)(imageIdx, i) = tmp/255;
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
