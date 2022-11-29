#include "mainTest.h"
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

//target {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0x00000000,0x00000000,0x00000000,0x00000002}
//se letto i singoli 32 bit sono swappati (02000000)

void scan_hash( uint8 pref_header[76],volatile uint8 pref_headerO[76],volatile uint32 target[8],volatile uint32 targetO[8], volatile uint32 *nonceRes,volatile uint32 hashed[8]){
#pragma HLS INTERFACE s_axilite port=pref_header
#pragma HLS INTERFACE s_axilite port=pref_headerO
#pragma HLS INTERFACE s_axilite port=target
#pragma HLS INTERFACE s_axilite port=targetO
#pragma HLS INTERFACE s_axilite port=nonceRes
#pragma HLS INTERFACE s_axilite port=hashed
#pragma HLS INTERFACE s_axilite port=return

	static uint32 nonce = 2164694287 ;
	static uint32 nonceLastResult = 0xaabbccdd;
	static uint32 lastHashResult[] = {0xffff00ff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xff00ffff};
	//const unsigned char header[] = {0x00,0x00,0x00,0x20,0x6e,0x3b,0xb6,0x1b,0x20,0xc1,0x89,0x35,0xf6,0xe1,0xd2,0xba,0x74,0x53,0xed,0x09,0xce,0x7e,0xe8,0xdb,0xe3,0x34,0xa1,0x4e,0x67,0x1e,0x00,0x00,0x00,0x00,0x00,0x00,0xe5,0xb8,0x53,0x3a,0xb9,0x31,0x26,0x94,0x78,0xf7,0x96,0xd9,0x2a,0x95,0x71,0x73,0x0c,0xf6,0xc7,0xc9,0x1c,0x97,0xf8,0x4c,0x6a,0xf7,0xef,0x9d,0x3c,0x41,0x90,0xac,0xa4,0xf9,0xe8,0x61,0x53,0xda,0x20,0x1a};
	//const uint32 target[] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0x00000000,0x00000000,0x00000000,0x00000002};

	uint8 header[80];
	for(int i = 0; i<76;i++){
		header[i] = pref_header[i];
	}

	//2158421300 is the nonce
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

	//if(valid_hash((uint32*)hash, (uint32 *)target) == (bit)1){
		nonceLastResult = nonce;
		memcpy(lastHashResult,hash,32);
	//}

	nonce++;
	*nonceRes = nonceLastResult;
	for(int i=0;i<8;i++){
		hashed[i] = lastHashResult[i];
	}
	for(int i = 0;i<8;i++){
		targetO[i] = target[i];
	}
	for(int i = 0;i<76;i++){
		pref_headerO[i] = header[i];
	}

	return;
}

