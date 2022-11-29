#ifndef __MAINH__
#define __MAINH__
#include "ap_int.h"
#include <stdint.h>


typedef ap_uint<32> uint32;
typedef ap_uint<64> uint64;
typedef ap_uint<8> uint8;
typedef ap_uint<1> bit;

void scan_hash( uint8 pref_header[76],volatile uint8 pref_headerO[76],volatile uint32 target[8],volatile uint32 targetO[8], volatile uint32 *nonceRes,volatile uint32 hashed[8]);
void *myMemset(void *s, int c,  unsigned int len);
#endif
