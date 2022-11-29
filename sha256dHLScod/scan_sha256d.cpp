#include "sha256d.h"
#include <stdio.h>
bool valid_hash(const unsigned int hash[8], const unsigned int target[8]){


	if (hash[7] > target[7]) return false;
	if (hash[7] < target[7]) return true;
	if (hash[6] > target[6]) return false;
	if (hash[6] < target[6]) return true;
	if (hash[5] > target[5]) return false;
	if (hash[5] < target[5]) return true;
	if (hash[4] > target[4]) return false;
	if (hash[4] < target[4]) return true;
	if (hash[3] > target[3]) return false;
	if (hash[3] < target[3]) return true;
	if (hash[2] > target[2]) return false;
	if (hash[2] < target[2]) return true;
	if (hash[1] > target[1]) return false;
	if (hash[1] < target[1]) return true;
	if (hash[0] > target[0]) return false;
	return true;
}


void scan_sha256d(unsigned char headerPrefix[76],unsigned int target[8],unsigned int *actualNonce,unsigned int *goldenNonce,unsigned char actualHash[32]){
	#pragma HLS INTERFACE mode=s_axilite port=headerPrefix
	#pragma HLS INTERFACE mode=s_axilite port=target
	#pragma HLS INTERFACE mode=s_axilite port=actualNonce
	#pragma HLS INTERFACE mode=s_axilite port=goldenNonce
	#pragma HLS INTERFACE mode=s_axilite port=actualHash
	#pragma HLS INTERFACE mode=s_axilite port=return

	static unsigned nonce = 0;
	static unsigned int gNonce = 0;
	int i;
	unsigned char header[80],hashed[32];
	unsigned int targ[8];
	for(i = 0;i<76;i++ ){
#pragma HLS UNROLL
		header[i] = headerPrefix[i];
	}
	header[79] = (nonce << 24) >> 24;
	header[78] = (nonce << 16) >> 24;
	header[77] = (nonce << 8) >> 24;
	header[76] = nonce >> 24;
	for(i = 0;i<8;i++){
#pragma HLS UNROLL
		targ[i] = target[i];
	}
	sha256d(header,hashed);
	if(valid_hash((const unsigned int*)hashed,targ) == true){
		gNonce = nonce;
	}
	*actualNonce = nonce;
	nonce = nonce + 1;
	*goldenNonce = gNonce;
	for(i = 0;i<32;i++){
#pragma HLS UNROLL
		actualHash[i] = hashed[i];
	}
}
