#include "sha256d.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // for overloaded memcpy() function

void sha256d( unsigned char data[MAXDATASIZE],  // input: data to be hashed
             // input: length of memory region to hash (bytes)
			 unsigned char digest[HASHSIZE] ) {
	   // output: hash digest of input data



	// We work on buffers of up to 64 bytes - hard-coded into SHA256 algorithm
	unsigned char seg_buf[80];	   // 64byte segment buffer
	int i=0;
	for(i = 0;i<80;i++){
		seg_buf[i] = data[i];
	}
	// Initialize the SHA256 context
	SHA256_CTX sha256ctx;
	sha256_init(&sha256ctx);
	sha256_update(&sha256ctx,(const void*)seg_buf,80);
	sha256_final(&sha256ctx, (unsigned char*)seg_buf);
	sha256_init(&sha256ctx);
	sha256_update(&sha256ctx,(const void *)seg_buf,32);
	sha256_final(&sha256ctx, (unsigned char*)seg_buf);

	for(i =0;i<HASHSIZE;i++){
#pragma HLS UNROLL
		digest[i] = seg_buf[i];
	}
}
