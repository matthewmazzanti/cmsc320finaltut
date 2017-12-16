#ifndef REPEATS
#define REPEATS


#include <iostream>
#include <seqan/index.h>
#include <vector>
#include <string>


struct REPEAT {
    std::vector<unsigned> occur;
    long length = 0;
    std::string sequence;
};

std::vector<REPEAT> supermax(const char *sequence,int min);

#endif
