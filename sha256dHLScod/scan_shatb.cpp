#include "scan_sha256d.h"
#include <stdio.h>
int main(){
	unsigned int target[8];
	target[0] = 0;
	target[1] = 0;
	target[2] = 0;
	target[3] = 0;
	target[4] = 0;
	target[5] = 0;
	target[6] = 0;
	target[7] = 0x5b000000;

	unsigned char pre_head[76] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xff};
	unsigned char actH[32];
	unsigned int actual,golden;

	scan_sha256d(pre_head,target,&actual,&golden,actH);
	scan_sha256d(pre_head,target,&actual,&golden,actH);
	scan_sha256d(pre_head,target,&actual,&golden,actH);
	scan_sha256d(pre_head,target,&actual,&golden,actH);



	printf("actual %d golden %d \n",actual,golden);
	for(int i = 0;i<32;i++){
		printf("%x",actH[i]);
	}
	//res: 2 1    df85946d17837130dbf883bdb14ac106351e734916b8f9287a3ba8c5a94ed





}
