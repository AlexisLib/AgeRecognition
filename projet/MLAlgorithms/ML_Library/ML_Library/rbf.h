#include <Eigen/Dense>

typedef struct s_rbfData
{
	Eigen::MatrixXd* X;
	Eigen::MatrixXd* centroids;
	Eigen::MatrixXd* W;
	double gamma;
	unsigned int inputCountPerSample;
}				t_rbfData;
