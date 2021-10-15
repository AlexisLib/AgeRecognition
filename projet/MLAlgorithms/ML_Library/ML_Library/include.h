
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
#include "rbf.h"


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
void getPixelsFromImage(std::string imagePath, int component, Eigen::MatrixXd *datasetX,
	unsigned int imageIdx, unsigned int sizeImageW, unsigned int sizeImageH, int is255);
double kernelTrick(Eigen::VectorXd m, Eigen::VectorXd n);
void displaySigmas(t_pmcData* PMC);
void displayOutput(t_pmcData* PMC);
void addInputsInPMC(t_pmcData* PMC, Eigen::VectorXd* input);
void allocate(t_pmcData* PMC);
double* predictPMC(t_pmcData* PMC, Eigen::VectorXd* X, int isLinear, int res);
int checkUsed(int* tab, int tmp, int sizeUsed);
int getMinInArray(double* Arr, int size);

#endif // !"INCLUDE_H"