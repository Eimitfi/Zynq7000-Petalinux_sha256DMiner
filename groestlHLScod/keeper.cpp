/*#include "mainTest.h"
#include "sph_groestl.h"
#include "string.h"

void *myMemset(void *s, int c,  unsigned int len)
{
    unsigned char* p=(unsigned char*)s;
    while(len--)
    {
        *p++ = (unsigned char)c;
    }
    return s;
}

bit valid_hash( const uint32 hash[8], const uint32 target[8] )
{
	//for(int i = 0;i<8;i++){
		//std::cout << std::hex << hash[i] << std::endl;
	//}
   const uint64 *h = (const uint64*)hash;
   const uint64 *t = (const uint64*)target;
   if ( h[3] > t[3] ) return 0;
   if ( h[3] < t[3] ) return 1;
   if ( h[2] > t[2] ) return 0;
   if ( h[2] < t[2] ) return 1;
   if ( h[1] > t[1] ) return 0;
   if ( h[1] < t[1] ) return 1;
   if ( h[0] > t[0] ) return 0;
   return 1;
}

void scan_hash(volatile const uint8 pref_header[76],volatile const uint32 target[8], uint32 nonceRes[1]){
#pragma HLS INTERFACE s_axilite port=pref_header
#pragma HLS INTERFACE s_axilite port=target
#pragma HLS INTERFACE s_axilite port=nonceRes
#pragma HLS INTERFACE s_axilite port=return

	uint8 state[32];
	uint8 header[80];
	for(int i = 0; i<76;i++){
		header[i] = pref_header[i];
	}

	//2158421300 is the nonce
	uint32 nonce = 0;
	while(nonce < 4294967295){
		header[79] = (nonce << 24) >> 24;
		header[78] = (nonce << 16) >> 24;
		header[77] = (nonce << 8) >> 24;
		header[76] = nonce >> 24;
	    sph_groestl512_context groestl1, groestl2;
	    uint32_t hash[16];
	    sph_groestl512_init( &groestl1 );
	    sph_groestl512(&groestl1, (const void*)header, 80);
	    sph_groestl512_close(&groestl1, hash);
	    sph_groestl512_init( &groestl2 );
	    sph_groestl512(&groestl2, hash, 64);
	    sph_groestl512_close(&groestl2, hash);
	    //myMemcpy(state, hash, 32);
	    memcpy(state,hash,32);

		if(valid_hash((uint32 *)state, (uint32 *)target) == (bit)1){
			nonceRes[0] = nonce;
		}
		nonce++ ;
	}
	return;
}
*/
