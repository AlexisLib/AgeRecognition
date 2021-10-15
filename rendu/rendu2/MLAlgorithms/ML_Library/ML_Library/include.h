#ifndef INCLUDE_H_
#define INCLUDE_H_


//C++ LIB
#include <iostream>
#include <fstream>
#include <time.h>
#include <exception>
#include <typeinfo>
#include <iomanip>
#include <stdexcept>
#include <math.h>  



//OpenCV 
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <Eigen/Dense>

#include "pmc.h"

using namespace std;
using namespace cv;

#if _WIN32
#define SUPEREXPORT __declspec(dllexport)
#else
#define SUPEREXPORT 
#endif


////	matrixUtils.cpp
Eigen::MatrixXd convertArrayToMatrix(int SampleCount, int inputCountPerSample, double *Array);
void convertMatrixToSimpleArray(Eigen::MatrixXd matrix, double *arr);
int isMatrixColColinear(Eigen::MatrixXd* matrix);
int isMatrixLineColinear(Eigen::MatrixXd* matrix);
void fixColinearity(Eigen::MatrixXd* matrix);
int isColinear(Eigen::MatrixXd* matrix);

////	imageUtils.cpp
void getPixelsFromImage(string imagePath, int component, Eigen::MatrixXd *datasetX,
	unsigned int imageIdx, unsigned int sizeImageW, unsigned int sizeImageH);

////	pmc.cpp
Eigen::VectorXd* getLayerOuptut(t_layer* layer, int bias);
void calculateNeuroneOutput(t_neurone* neurone, Eigen::VectorXd* input, unsigned int isLinear);
double* predictPMC(t_pmc* W, Eigen::VectorXd* X, unsigned int isLinear);
double fitPMC(t_pmc* W, Eigen::MatrixXd* X, Eigen::MatrixXd* Y, int SampleCount, int inputCountPerSample, double alpha, int epochs, int display, int isLinear);
void displayPmc(t_pmc* W);
void fillFirstLayerWithInputs(t_pmc* W, Eigen::VectorXd* input);

#endif // !"INCLUDE_H"