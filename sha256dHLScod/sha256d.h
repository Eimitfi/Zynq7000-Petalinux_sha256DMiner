#pragma once

#include <stdbool.h>
#include "sha256impl.h"

#define MAXDATASIZE 80
#define HASHSIZE 32     // A SHA256 hash is 32 bytes long (256 bits:)

void sha256d( unsigned char data[MAXDATASIZE],  // input: data to be hashed
			 unsigned char digest[HASHSIZE] );  // output: hash digest of input data
