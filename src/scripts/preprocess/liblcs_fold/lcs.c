#include <stdio.h>
#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))

int LCSLength(long unsigned X[], long unsigned Y[], long unsigned m, long unsigned n)
{
    // int L[m+1][n+1];
    // unsigned int s = sizeof(int) * (unsigned int)(m+1) * (unsigned int)(n+1);
    // int (*L)[n+1] = (int**)malloc(s);

    //	142502976000
    //            30703543852
    //            638772780
    // printf("m %lu n %lu %lu\n", m, n, m*n*4);
    // 37604966400
    // 
    int th = 299999999 * 4;
    //        399980880
    int th1 = 299999999;
    if ((m*n*4) > th)
    {
	printf("adjust m %lu n %lu\n", m, n);

	if (m > th1 && n > th1)
	    m = 999999;

	if (m>n) 
	    // m = MIN(m, n);
	    m = th1 / n;
	else 
	    n = th1 / m;
	printf("m %lu n %lu\n", m, n);
    }

    int** L = new int*[m+1];
    for(int i = 0; i < m+1; ++i)
        L[i] = new int[n+1];

    int i, j;
    for(i=0; i<=m; i++)
    {
        for(j=0; j<=n; j++)
        {
            if(i==0 || j==0)
                L[i][j] = 0;
            else if(X[i-1]==Y[j-1])
                L[i][j] = L[i-1][j-1]+1;
            else
                L[i][j] = MAX(L[i-1][j],L[i][j-1]);
        }
    }
    int tt = L[m][n];

    for (i = 0; i < m+1; i++)
        delete [] L[i];

    delete [] L;

    return tt;
}
