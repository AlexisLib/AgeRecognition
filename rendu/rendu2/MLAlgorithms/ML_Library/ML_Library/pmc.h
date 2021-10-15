#include <Eigen/Dense>
typedef struct s_neurone
{
	double       sigma;
	double		result;
	Eigen::VectorXd	*weights;
}				t_neurone;

typedef struct s_layer
{
	unsigned int nbNeurone;
	t_neurone	*neurones;
}				t_layer;

typedef struct s_pmc
{
	unsigned int nbLayer;
	t_layer		*layers;
}				t_pmc;


