#include "repeats.h"

using namespace seqan;

std::vector<REPEAT> supermax(const char *sequence, int min)
{
	String<char> myString = sequence;

	typedef Index< String<char> > TMyIndex;
	TMyIndex myIndex(myString);

	Iterator< TMyIndex, SuperMaxRepeats >::Type myRepeatIterator(myIndex, min);

    std::vector<REPEAT> repeats;
	while (!atEnd(myRepeatIterator))
	{
        REPEAT rep;

		for(unsigned i = 0; i < countOccurrences(myRepeatIterator); ++i) {
            rep.occur.push_back(getOccurrences(myRepeatIterator)[i]);
        }
        rep.length = repLength(myRepeatIterator);
        rep.sequence = std::string(representative(myRepeatIterator));

        repeats.push_back(rep);
		++myRepeatIterator;
	}

    return repeats;
}
