#include <Eigen/Dense>

typedef struct s_pmcData
{
	double** sigma;
	double	***W;
	double*** Wold;
	int		*structure;
	int		lenStructure;
	double  **output;
	
}				t_pmcData;

