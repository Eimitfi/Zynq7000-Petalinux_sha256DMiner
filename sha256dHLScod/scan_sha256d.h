#pragma once
#include "sha256impl.h"
void scan_sha256d(unsigned char headerPrefix[76],unsigned int target[8],unsigned int *actualNonce,unsigned int *goldenNonce,unsigned char actualHash[32]);
