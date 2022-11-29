#include "myfunctions.h"
int main()
{
	u32int state[8];
	u32int edata[20];
	printf("start test...");
	for ( int i = 0; i < 19; i++ )
		        edata[i] = 0;

	top(edata,state);
	for(int i=0; i<8;i++){
		printf("%d\n",state[i]);
	}

}
